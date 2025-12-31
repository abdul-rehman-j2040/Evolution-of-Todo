"""CLI interface for the Todo application.

Provides argparse-based command interface for managing tasks.
"""

import argparse
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


def handle_add(args: argparse.Namespace) -> int:
    """
    Handle the 'add' command.

    Args:
        args: Parsed arguments from argparse

    Returns:
        Exit code (0 for success, 1 for error)
    """
    service = TodoService()

    # Parse priority
    try:
        priority = Priority.parse(args.priority) if args.priority else Priority.MEDIUM
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Add task
    task, error = service.add_task(
        title=args.title,
        description=args.description or "",
        priority=priority,
    )

    if error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print("Task added successfully!")
    print(f"ID: {task.id}")
    print(f"Title: {task.title}")
    print(f"Description: {task.description}")
    print(f"Priority: {task.priority.value}")
    print(f"Status: {task.status.value}")
    print(f"Created: {format_datetime(task.created_at)}")

    return 0


def handle_list(args: argparse.Namespace) -> int:
    """
    Handle the 'list' command.

    Args:
        args: Parsed arguments from argparse

    Returns:
        Exit code (0 for success, 1 for error)
    """
    service = TodoService()

    # Parse status filter
    status_filter = None
    if args.status and args.status != "all":
        try:
            status_filter = Status.parse(args.status)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    # Get tasks
    if status_filter:
        tasks = service.filter_by_status(status_filter)
    else:
        tasks = service.list_tasks()

    # Render output
    if args.json:
        import json
        data = [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "priority": t.priority.value,
                "status": t.status.value,
                "created": format_datetime(t.created_at),
            }
            for t in tasks
        ]
        print(json.dumps(data, indent=2))
    else:
        print(render_table(tasks))

    return 0


def handle_update(args: argparse.Namespace) -> int:
    """
    Handle the 'update' command.

    Args:
        args: Parsed arguments from argparse

    Returns:
        Exit code (0 for success, 1 for error)
    """
    service = TodoService()

    # Validate ID
    task_id, error = validate_id(str(args.id))
    if error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    # Check at least one field is provided
    if not args.title and not args.description and not args.priority:
        print("Error: At least one field (--title, --description, --priority) must be specified", file=sys.stderr)
        return 1

    # Parse priority if provided
    priority = None
    if args.priority:
        try:
            priority = Priority.parse(args.priority)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    # Update task
    task, error = service.update_task(
        task_id=task_id,  # type: ignore[arg-type]
        title=args.title,
        description=args.description,
        priority=priority,
    )

    if error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print("Task updated successfully!")
    print(f"ID: {task.id}")
    print(f"Title: {task.title}")
    print(f"Description: {task.description}")
    print(f"Priority: {task.priority.value}")
    print(f"Status: {task.status.value}")
    print(f"Created: {format_datetime(task.created_at)}")

    return 0


def handle_delete(args: argparse.Namespace) -> int:
    """
    Handle the 'delete' command.

    Args:
        args: Parsed arguments from argparse

    Returns:
        Exit code (0 for success, 1 for error)
    """
    service = TodoService()

    # Validate ID
    task_id, error = validate_id(str(args.id))
    if error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    # Delete task
    task, error = service.delete_task(task_id)  # type: ignore[arg-type]

    if error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print("Task deleted successfully!")
    print(f"ID: {task.id}")
    print(f"Title: {task.title}")

    return 0


def handle_complete(args: argparse.Namespace) -> int:
    """
    Handle the 'complete' command.

    Args:
        args: Parsed arguments from argparse

    Returns:
        Exit code (0 for success, 1 for error)
    """
    service = TodoService()

    # Validate ID
    task_id, error = validate_id(str(args.id))
    if error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    # Complete task
    task, error = service.complete_task(task_id)  # type: ignore[arg-type]

    if error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print("Task marked as complete!")
    print(f"ID: {task.id}")
    print(f"Title: {task.title}")
    print(f"Status: {task.status.value}")

    return 0


def handle_filter(args: argparse.Namespace) -> int:
    """
    Handle the 'filter' command.

    Args:
        args: Parsed arguments from argparse

    Returns:
        Exit code (0 for success, 1 for error)
    """
    service = TodoService()

    # Parse priority
    try:
        priority = Priority.parse(args.priority)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Filter tasks
    tasks = service.filter_by_priority(priority)

    # Render output
    if args.json:
        import json
        data = [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "priority": t.priority.value,
                "status": t.status.value,
                "created": format_datetime(t.created_at),
            }
            for t in tasks
        ]
        print(json.dumps(data, indent=2))
    else:
        if tasks:
            print(render_table(tasks))
        else:
            print(f"No tasks found with priority: {priority.value}")

    return 0


def handle_search(args: argparse.Namespace) -> int:
    """
    Handle the 'search' command.

    Args:
        args: Parsed arguments from argparse

    Returns:
        Exit code (0 for success, 1 for error)
    """
    service = TodoService()

    # Search tasks
    tasks = service.search_tasks(args.keyword)

    # Render output
    if args.json:
        import json
        data = [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "priority": t.priority.value,
                "status": t.status.value,
                "created": format_datetime(t.created_at),
            }
            for t in tasks
        ]
        print(json.dumps(data, indent=2))
    else:
        if tasks:
            print(render_table(tasks))
        else:
            print(f"No tasks found matching: {args.keyword}")

    return 0


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the todo CLI."""
    parser = argparse.ArgumentParser(
        prog="todo",
        description="Professional In-Memory Python Todo CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title (1-200 characters)")
    add_parser.add_argument("-d", "--description", help="Task description (0-1000 characters)")
    add_parser.add_argument("-p", "--priority", choices=["high", "medium", "low", "h", "m", "l"],
                           help="Task priority (default: medium)")
    add_parser.set_defaults(handler=handle_add)

    # list command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("-s", "--status", choices=["pending", "completed", "all"],
                            default="all", help="Filter by status (default: all)")
    list_parser.add_argument("--json", action="store_true", help="Output as JSON")
    list_parser.set_defaults(handler=handle_list)

    # update command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", help="Task ID to update")
    update_parser.add_argument("-t", "--title", help="New task title")
    update_parser.add_argument("-d", "--description", help="New task description")
    update_parser.add_argument("-p", "--priority", choices=["high", "medium", "low", "h", "m", "l"],
                              help="New task priority")
    update_parser.set_defaults(handler=handle_update)

    # delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", help="Task ID to delete")
    delete_parser.set_defaults(handler=handle_delete)

    # complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as complete")
    complete_parser.add_argument("id", help="Task ID to complete")
    complete_parser.set_defaults(handler=handle_complete)

    # filter command
    filter_parser = subparsers.add_parser("filter", help="Filter tasks by priority")
    filter_parser.add_argument("priority", choices=["high", "medium", "low", "h", "m", "l"],
                              help="Priority level to filter by")
    filter_parser.add_argument("--json", action="store_true", help="Output as JSON")
    filter_parser.set_defaults(handler=handle_filter)

    # search command
    search_parser = subparsers.add_parser("search", help="Search tasks by keyword")
    search_parser.add_argument("keyword", help="Search keyword")
    search_parser.add_argument("--json", action="store_true", help="Output as JSON")
    search_parser.set_defaults(handler=handle_search)

    return parser


def main() -> int:
    """Main entry point for the todo CLI."""
    parser = create_parser()
    args = parser.parse_args()

    if not hasattr(args, "handler"):
        parser.print_help()
        return 1

    return args.handler(args)


if __name__ == "__main__":
    sys.exit(main())
