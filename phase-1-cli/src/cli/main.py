"""Interactive CLI interface for the Todo application.

Provides a menu-driven interface for managing tasks.
"""

import sys
from datetime import datetime
from typing import List, Optional

from src.models.enums import Priority, Status, validate_id
from src.services.todo_service import TodoService


def format_datetime(dt: datetime) -> str:
    """Format datetime for display."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def render_table(tasks: List["Todo"]) -> str:
    """
    Render tasks as an ASCII table.

    Args:
        tasks: List of Todo items to display

    Returns:
        Formatted table string
    """
    if not tasks:
        return "No tasks found."

    # Calculate column widths
    id_width = max(3, len("ID"))
    title_width = max(20, max(len(t.title) for t in tasks) + 2)
    desc_width = max(20, max(len(t.description) for t in tasks) + 2)
    priority_width = max(8, len("Priority"))
    status_width = max(8, len("Status"))
    created_width = len("Created")

    # Header
    header = (
        f"{'ID':<{id_width}} | "
        f"{'Title':<{title_width}} | "
        f"{'Description':<{desc_width}} | "
        f"{'Priority':<{priority_width}} | "
        f"{'Status':<{status_width}} | "
        f"{'Created':<{created_width}}"
    )
    separator = (
        f"{'-' * id_width}-+-"
        f"{'-' * title_width}-+-"
        f"{'-' * desc_width}-+-"
        f"{'-' * priority_width}-+-"
        f"{'-' * status_width}-+-"
        f"{'-' * created_width}"
    )

    # Rows
    rows = []
    for task in tasks:
        title = task.title[:title_width - 3] + "..." if len(task.title) > title_width - 3 else task.title
        desc = task.description[:desc_width - 3] + "..." if len(task.description) > desc_width - 3 else task.description
        rows.append(
            f"{task.id:<{id_width}} | "
            f"{title:<{title_width}} | "
            f"{desc:<{desc_width}} | "
            f"{task.priority.value:<{priority_width}} | "
            f"{task.status.value:<{status_width}} | "
            f"{format_datetime(task.created_at):<{created_width}}"
        )

    return "\n".join([header, separator] + rows)


def print_banner() -> None:
    """Print the application banner."""
    print("\n" + "=" * 50)
    print("         TODO APPLICATION")
    print("=" * 50)


def print_menu() -> None:
    """Print the main menu."""
    print("\n----------- MAIN MENU -----------")
    print("1.  Add Task")
    print("2.  View All Tasks")
    print("3.  View Pending Tasks")
    print("4.  View Completed Tasks")
    print("5.  Update Task")
    print("6.  Mark Task as Complete")
    print("7.  Delete Task")
    print("8.  Filter by Priority")
    print("9.  Search Tasks")
    print("0.  Exit")
    print("-------------------------------")


def get_input(prompt: str) -> str:
    """Get input from user with a prompt."""
    return input(prompt).strip()


def add_task(service: TodoService) -> None:
    """Add a new task."""
    print("\n--- ADD TASK ---")
    title = get_input("Enter task title: ")
    if not title:
        print("Error: Title cannot be empty!")
        return

    description = get_input("Enter description (optional): ")
    priority_input = get_input("Enter priority (high/medium/low) [default: medium]: ").lower()

    try:
        priority = Priority.parse(priority_input) if priority_input else Priority.MEDIUM
    except ValueError:
        print("Invalid priority. Using MEDIUM.")
        priority = Priority.MEDIUM

    task, error = service.add_task(title=title, description=description, priority=priority)

    if error:
        print(f"Error: {error}")
    else:
        print(f"\nTask added successfully!")
        print(f"ID: {task.id} | Title: {task.title} | Priority: {task.priority.value}")


def view_tasks(service: TodoService, filter_status: Optional[Status] = None) -> None:
    """View all tasks or filtered by status."""
    print("\n--- TASKS ---")
    if filter_status:
        tasks = service.filter_by_status(filter_status)
        status_name = "Pending" if filter_status == Status.PENDING else "Completed"
        print(f"Showing {status_name} tasks:")
    else:
        tasks = service.list_tasks()
        print("All tasks:")

    if not tasks:
        print("No tasks found.")
    else:
        print(render_table(tasks))


def update_task(service: TodoService) -> None:
    """Update an existing task."""
    print("\n--- UPDATE TASK ---")
    tasks = service.list_tasks()
    if not tasks:
        print("No tasks to update.")
        return

    print(render_table(tasks))

    task_id_input = get_input("\nEnter task ID to update: ")
    task_id, error = validate_id(task_id_input)
    if error:
        print(f"Error: {error}")
        return

    task = service.get_task(task_id)  # type: ignore[arg-type]
    if not task:
        print(f"Error: Task with ID {task_id} not found.")
        return

    print(f"\nCurrent: {task.title} | {task.description} | {task.priority.value}")

    new_title = get_input("Enter new title (press Enter to keep current): ")
    new_desc = get_input("Enter new description (press Enter to keep current): ")
    priority_input = get_input("Enter new priority (high/medium/low, press Enter to keep current): ").lower()

    priority = None
    if priority_input:
        try:
            priority = Priority.parse(priority_input)
        except ValueError:
            print("Invalid priority. Keeping current.")

    task, error = service.update_task(
        task_id=task_id,  # type: ignore[arg-type]
        title=new_title if new_title else None,
        description=new_desc if new_desc else None,
        priority=priority,
    )

    if error:
        print(f"Error: {error}")
    else:
        print(f"\nTask updated successfully!")


def complete_task(service: TodoService) -> None:
    """Mark a task as complete."""
    print("\n--- MARK COMPLETE ---")
    tasks = service.list_tasks()
    if not tasks:
        print("No tasks to complete.")
        return

    pending = service.filter_by_status(Status.PENDING)
    if not pending:
        print("All tasks are already completed!")
        return

    print(render_table(pending))

    task_id_input = get_input("\nEnter task ID to mark as complete: ")
    task_id, error = validate_id(task_id_input)
    if error:
        print(f"Error: {error}")
        return

    task, error = service.complete_task(task_id)  # type: ignore[arg-type]

    if error:
        print(f"Error: {error}")
    else:
        print(f"\nTask marked as complete!")
        print(f"ID: {task.id} | Title: {task.title} | Status: {task.status.value}")


def delete_task(service: TodoService) -> None:
    """Delete a task."""
    print("\n--- DELETE TASK ---")
    tasks = service.list_tasks()
    if not tasks:
        print("No tasks to delete.")
        return

    print(render_table(tasks))

    task_id_input = get_input("\nEnter task ID to delete: ")
    task_id, error = validate_id(task_id_input)
    if error:
        print(f"Error: {error}")
        return

    confirm = get_input(f"Delete task {task_id}? (y/n): ").lower()
    if confirm != 'y':
        print("Delete cancelled.")
        return

    task, error = service.delete_task(task_id)  # type: ignore[arg-type]

    if error:
        print(f"Error: {error}")
    else:
        print(f"\nTask deleted!")
        print(f"ID: {task.id} | Title: {task.title}")


def filter_by_priority(service: TodoService) -> None:
    """Filter tasks by priority."""
    print("\n--- FILTER BY PRIORITY ---")
    print("Options: high, medium, low")
    priority_input = get_input("Enter priority to filter: ").lower()

    try:
        priority = Priority.parse(priority_input)
    except ValueError:
        print("Error: Invalid priority!")
        return

    tasks = service.filter_by_priority(priority)

    print(f"\nTasks with priority: {priority.value}")
    if not tasks:
        print("No tasks found with this priority.")
    else:
        print(render_table(tasks))


def search_tasks(service: TodoService) -> None:
    """Search tasks by keyword."""
    print("\n--- SEARCH TASKS ---")
    keyword = get_input("Enter search keyword: ")

    if not keyword:
        print("Error: Please enter a keyword!")
        return

    tasks = service.search_tasks(keyword)

    print(f"\nResults for '{keyword}':")
    if not tasks:
        print("No tasks found matching your search.")
    else:
        print(render_table(tasks))


def run_interactive() -> None:
    """Run the interactive todo application."""
    service = TodoService()

    while True:
        print_banner()
        print_menu()

        choice = get_input("Enter your choice (0-9): ")

        if choice == "0":
            print("\nGoodbye! Thanks for using Todo App!")
            break
        elif choice == "1":
            add_task(service)
        elif choice == "2":
            view_tasks(service)
        elif choice == "3":
            view_tasks(service, filter_status=Status.PENDING)
        elif choice == "4":
            view_tasks(service, filter_status=Status.COMPLETED)
        elif choice == "5":
            update_task(service)
        elif choice == "6":
            complete_task(service)
        elif choice == "7":
            delete_task(service)
        elif choice == "8":
            filter_by_priority(service)
        elif choice == "9":
            search_tasks(service)
        else:
            print("\nInvalid choice! Please enter a number from 0 to 9.")

        input("\nPress Enter to continue...")


def main() -> int:
    """Main entry point."""
    run_interactive()
    return 0


if __name__ == "__main__":
    sys.exit(main())
