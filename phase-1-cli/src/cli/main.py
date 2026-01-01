"""Interactive CLI interface for the Todo application.

Provides a menu-driven interface for managing tasks.
"""

import sys
from datetime import datetime
from typing import List, Optional

from src.cli.colors import (
    Emojis,
    Colors,
    bold,
    success,
    error,
    warning,
    info,
    priority_color,
    priority_emoji,
    status_emoji,
    priority_colored,
    status_colored,
)
from src.models.enums import Priority, Status, validate_id
from src.services.todo_service import TodoService


def format_datetime(dt: datetime) -> str:
    """Format datetime for display."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def render_table(tasks: List["Todo"]) -> str:
    """
    Render tasks as an ASCII table with colors and emojis.

    Args:
        tasks: List of Todo items to display

    Returns:
        Formatted table string with colors and emojis
    """
    if not tasks:
        return info("No tasks found.")

    # Calculate column widths
    id_width = max(3, len("ID"))
    title_width = max(20, max(len(t.title) for t in tasks) + 2)
    desc_width = max(20, max(len(t.description) for t in tasks) + 2)
    priority_width = max(12, len("Priority"))
    status_width = max(12, len("Status"))
    created_width = len("Created")

    # Header with emojis
    header = (
        f"{bold('ID'):<{id_width}} | "
        f"{bold('Title'):<{title_width}} | "
        f"{bold('Description'):<{desc_width}} | "
        f"{bold('Priority'):<{priority_width}} | "
        f"{bold('Status'):<{status_width}} | "
        f"{bold('Created'):<{created_width}}"
    )
    separator = (
        f"{'-' * id_width}-+-"
        f"{'-' * title_width}-+-"
        f"{'-' * desc_width}-+-"
        f"{'-' * priority_width}-+-"
        f"{'-' * status_width}-+-"
        f"{'-' * created_width}"
    )

    # Rows with colors and emojis
    rows = []
    for task in tasks:
        title = task.title[:title_width - 3] + "..." if len(task.title) > title_width - 3 else task.title
        desc = task.description[:desc_width - 3] + "..." if len(task.description) > desc_width - 3 else task.description
        emoji = priority_emoji(task.priority)
        colored_priority = priority_colored(task.priority.value, task.priority)
        colored_status = status_colored(task.status.value, task.status)
        status_icon = status_emoji(task.status)
        rows.append(
            f"{task.id:<{id_width}} | "
            f"{title:<{title_width}} | "
            f"{desc:<{desc_width}} | "
            f"{emoji} {colored_priority:<{priority_width - 2}} | "
            f"{status_icon} {colored_status:<{status_width - 2}} | "
            f"{format_datetime(task.created_at):<{created_width}}"
        )

    return "\n".join([header, separator] + rows)


def print_banner() -> None:
    """Print the application banner with colors."""
    print(f"\n{Colors.BRIGHT_CYAN}{'=' * 50}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}         TODO APPLICATION         {Colors.RESET}")
    print(f"{Colors.BRIGHT_CYAN}{'=' * 50}{Colors.RESET}")


def print_menu() -> None:
    """Print the main menu with emojis."""
    print(f"\n{bold('----------- MAIN MENU -----------')}")
    print(f"{Emojis.ADD}  1.  Add Task")
    print(f"{Emojis.VIEW}  2.  View All Tasks")
    print(f"{Emojis.PENDING}  3.  View Pending Tasks")
    print(f"{Emojis.COMPLETED}  4.  View Completed Tasks")
    print(f"{Emojis.UPDATE}  5.  Update Task")
    print(f"{Emojis.CHECK}  6.  Mark Task as Complete")
    print(f"{Emojis.DELETE}  7.  Delete Task")
    print(f"{Emojis.FILTER}  8.  Filter by Priority")
    print(f"{Emojis.SEARCH}  9.  Search Tasks")
    print(f"{Emojis.EXIT}  0.  Exit")
    print(f"{bold('-------------------------------')}")


def get_input(prompt: str) -> str:
    """Get input from user with a prompt."""
    return input(prompt).strip()


def add_task(service: TodoService) -> None:
    """Add a new task with colored output."""
    print(f"\n{bold(Emojis.ADD + ' --- ADD TASK ---')}")
    title = get_input("Enter task title: ")
    if not title:
        print(f"{error('Error: Title cannot be empty!')}")
        return

    description = get_input("Enter description (optional): ")
    priority_input = get_input("Enter priority (high/medium/low) [default: medium]: ").lower()

    try:
        priority = Priority.parse(priority_input) if priority_input else Priority.MEDIUM
    except ValueError:
        print(f"{warning('Invalid priority. Using MEDIUM.')}")
        priority = Priority.MEDIUM

    task, error = service.add_task(title=title, description=description, priority=priority)

    if error:
        print(f"{error('Error:')}{error}")
    else:
        emoji = priority_emoji(priority)
        print(f"\n{success(Emojis.SUCCESS + ' Task added successfully!')}")
        print(f"{Emojis.TASK} ID: {task.id} | Title: {task.title} | {emoji} {task.priority.value}")


def view_tasks(service: TodoService, filter_status: Optional[Status] = None) -> None:
    """View all tasks or filtered by status with colors."""
    print(f"\n{bold(Emojis.VIEW + ' --- TASKS ---')}")
    if filter_status:
        tasks = service.filter_by_status(filter_status)
        status_name = "Pending" if filter_status == Status.PENDING else "Completed"
        status_icon = Emojis.PENDING if filter_status == Status.PENDING else Emojis.COMPLETED
        print(f"{status_icon} Showing {status_name} tasks:")
    else:
        tasks = service.list_tasks()
        print(f"{Emojis.TASK} All tasks:")

    if not tasks:
        print(info("No tasks found."))
    else:
        print(render_table(tasks))


def update_task(service: TodoService) -> None:
    """Update an existing task with colored output."""
    print(f"\n{bold(Emojis.UPDATE + ' --- UPDATE TASK ---')}")
    tasks = service.list_tasks()
    if not tasks:
        print(info("No tasks to update."))
        return

    print(render_table(tasks))

    task_id_input = get_input("\nEnter task ID to update: ")
    task_id, error = validate_id(task_id_input)
    if error:
        print(f"{error('Error:')}{error}")
        return

    task = service.get_task(task_id)  # type: ignore[arg-type]
    if not task:
        print(f"{error('Error: Task with ID ' + str(task_id) + ' not found.')}")
        return

    priority_icon = priority_emoji(task.priority)
    print(f"\nCurrent: {task.title} | {task.description} | {priority_icon} {task.priority.value}")

    new_title = get_input("Enter new title (press Enter to keep current): ")
    new_desc = get_input("Enter new description (press Enter to keep current): ")
    priority_input = get_input("Enter new priority (high/medium/low, press Enter to keep current): ").lower()

    priority = None
    if priority_input:
        try:
            priority = Priority.parse(priority_input)
        except ValueError:
            print(f"{warning('Invalid priority. Keeping current.')}")

    task, error = service.update_task(
        task_id=task_id,  # type: ignore[arg-type]
        title=new_title if new_title else None,
        description=new_desc if new_desc else None,
        priority=priority,
    )

    if error:
        print(f"{error('Error:')}{error}")
    else:
        print(f"\n{success(Emojis.SUCCESS + ' Task updated successfully!')}")


def complete_task(service: TodoService) -> None:
    """Mark a task as complete with colored output."""
    print(f"\n{bold(Emojis.CHECK + ' --- MARK COMPLETE ---')}")
    tasks = service.list_tasks()
    if not tasks:
        print(info("No tasks to complete."))
        return

    pending = service.filter_by_status(Status.PENDING)
    if not pending:
        print(success(Emojis.SUCCESS + " All tasks are already completed!"))
        return

    print(render_table(pending))

    task_id_input = get_input("\nEnter task ID to mark as complete: ")
    task_id, error = validate_id(task_id_input)
    if error:
        print(f"{error('Error:')}{error}")
        return

    task, error = service.complete_task(task_id)  # type: ignore[arg-type]

    if error:
        print(f"{error('Error:')}{error}")
    else:
        print(f"\n{success(Emojis.SUCCESS + ' Task marked as complete!')}")
        print(f"{Emojis.COMPLETED} ID: {task.id} | Title: {task.title} | Status: {task.status.value}")


def delete_task(service: TodoService) -> None:
    """Delete a task with colored output."""
    print(f"\n{bold(Emojis.DELETE + ' --- DELETE TASK ---')}")
    tasks = service.list_tasks()
    if not tasks:
        print(info("No tasks to delete."))
        return

    print(render_table(tasks))

    task_id_input = get_input("\nEnter task ID to delete: ")
    task_id, error = validate_id(task_id_input)
    if error:
        print(f"{error('Error:')}{error}")
        return

    confirm = get_input(f"Delete task {task_id}? (y/n): ").lower()
    if confirm != 'y':
        print(f"{warning('Delete cancelled.')}")
        return

    task, error = service.delete_task(task_id)  # type: ignore[arg-type]

    if error:
        print(f"{error('Error:')}{error}")
    else:
        print(f"\n{success(Emojis.SUCCESS + ' Task deleted!')}")
        print(f"{Emojis.DELETE} ID: {task.id} | Title: {task.title}")


def filter_by_priority(service: TodoService) -> None:
    """Filter tasks by priority with colored output."""
    print(f"\n{bold(Emojis.FILTER + ' --- FILTER BY PRIORITY ---')}")
    print("Options: high (h), medium (m), low (l)")
    priority_input = get_input("Enter priority to filter: ").lower()

    try:
        priority = Priority.parse(priority_input)
    except ValueError:
        print(f"{error('Error: Invalid priority!')}")
        return

    tasks = service.filter_by_priority(priority)
    priority_icon = priority_emoji(priority)

    print(f"\n{priority_icon} Tasks with priority: {priority.value}")
    if not tasks:
        print(info("No tasks found with this priority."))
    else:
        print(render_table(tasks))


def search_tasks(service: TodoService) -> None:
    """Search tasks by keyword with colored output."""
    print(f"\n{bold(Emojis.SEARCH + ' --- SEARCH TASKS ---')}")
    keyword = get_input("Enter search keyword: ")

    if not keyword:
        print(f"{error('Error: Please enter a keyword!')}")
        return

    tasks = service.search_tasks(keyword)

    print(f"\n{Emojis.SEARCH} Results for '{keyword}':")
    if not tasks:
        print(info("No tasks found matching your search."))
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
            print(f"\n{success(Emojis.EXIT + ' Goodbye! Thanks for using Todo App!')}")
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
            print(f"\n{warning('Invalid choice! Please enter a number from 0 to 9.')}")

        input("\nPress Enter to continue...")


def main() -> int:
    """Main entry point."""
    run_interactive()
    return 0


if __name__ == "__main__":
    sys.exit(main())
