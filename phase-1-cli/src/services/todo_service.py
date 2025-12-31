"""TodoService - Business logic layer for Todo CRUD operations.

This module contains the TodoService class which manages all task operations.
"""

from datetime import datetime
from typing import List, Optional

from src.models.enums import Priority, Status, validate_description, validate_title
from src.models.todo import Todo


class TodoService:
    """
    Service class for managing Todo items.

    Provides CRUD operations for tasks with in-memory storage.
    All methods are synchronous (no async/await) for Phase I simplicity.
    """

    def __init__(self) -> None:
        """Initialize the TodoService with empty task list."""
        self._tasks: List[Todo] = []
        self._next_id: int = 1

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
    ) -> tuple[Optional[Todo], Optional[str]]:
        """
        Add a new task.

        Args:
            title: Task title (1-200 chars, required)
            description: Optional task description (0-1000 chars)
            priority: Task priority (defaults to MEDIUM)

        Returns:
            tuple of (Todo, None) on success, or (None, error_message) on failure
        """
        # Validate title
        normalized_title, error = validate_title(title)
        if error:
            return None, error

        # Validate description
        _, error = validate_description(description)
        if error:
            return None, error

        # Create and store task
        task_id = self._next_id
        self._next_id += 1

        task = Todo.create(
            task_id=task_id,
            title=normalized_title,  # type: ignore[arg-type]
            description=description,
            priority=priority,
        )
        self._tasks.append(task)

        return task, None

    def get_task(self, task_id: int) -> Optional[Todo]:
        """
        Get a task by ID.

        Args:
            task_id: The task ID to look up

        Returns:
            Todo if found, None if not found
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def list_tasks(self) -> List[Todo]:
        """
        List all tasks in creation order.

        Returns:
            List of all tasks
        """
        return self._tasks.copy()

    def filter_by_status(self, status: Status) -> List[Todo]:
        """
        Filter tasks by status.

        Args:
            status: Status to filter by

        Returns:
            List of tasks with matching status
        """
        return [task for task in self._tasks if task.status == status]

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[Priority] = None,
    ) -> tuple[Optional[Todo], Optional[str]]:
        """
        Update a task's fields.

        Args:
            task_id: ID of task to update
            title: New title (optional)
            description: New description (optional)
            priority: New priority (optional)

        Returns:
            tuple of (updated_Todo, None) on success, or (None, error_message)
        """
        # Find task
        task = self.get_task(task_id)
        if task is None:
            return None, f"Task with ID {task_id} not found"

        # Validate and update title
        if title is not None:
            normalized_title, error = validate_title(title)
            if error:
                return None, error
            task.title = normalized_title  # type: ignore[assignment]

        # Validate and update description
        if description is not None:
            _, error = validate_description(description)
            if error:
                return None, error
            task.description = description

        # Update priority
        if priority is not None:
            task.priority = priority

        return task, None

    def delete_task(self, task_id: int) -> tuple[Optional[Todo], Optional[str]]:
        """
        Delete a task by ID.

        Args:
            task_id: ID of task to delete

        Returns:
            tuple of (deleted_Todo, None) on success, or (None, error_message)
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                deleted = self._tasks.pop(i)
                return deleted, None

        return None, f"Task with ID {task_id} not found"

    def complete_task(self, task_id: int) -> tuple[Optional[Todo], Optional[str]]:
        """
        Mark a task as complete.

        Args:
            task_id: ID of task to complete

        Returns:
            tuple of (updated_Todo, None) on success, or (None, error_message)
        """
        task = self.get_task(task_id)
        if task is None:
            return None, f"Task with ID {task_id} not found"

        task.status = Status.COMPLETED
        return task, None

    def filter_by_priority(self, priority: Priority) -> List[Todo]:
        """
        Filter tasks by priority level.

        Args:
            priority: Priority level to filter by

        Returns:
            List of tasks with matching priority
        """
        return [task for task in self._tasks if task.priority == priority]

    def search_tasks(self, keyword: str) -> List[Todo]:
        """
        Search tasks by keyword (case-insensitive).

        Searches both title and description.

        Args:
            keyword: Search term (case-insensitive substring match)

        Returns:
            List of matching tasks (empty if no matches)
        """
        if not keyword.strip():
            return []

        normalized_keyword = keyword.lower()
        seen: set[int] = set()
        results: List[Todo] = []

        for task in self._tasks:
            # Check if keyword matches title or description
            if (
                normalized_keyword in task.title.lower()
                or normalized_keyword in task.description.lower()
            ):
                # Avoid duplicates
                if task.id not in seen:
                    seen.add(task.id)
                    results.append(task)

        return results
