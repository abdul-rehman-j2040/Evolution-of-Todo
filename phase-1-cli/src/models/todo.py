"""Todo dataclass representing a single task item."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .enums import Priority, Status


@dataclass
class Todo:
    """
    Represents a single task/todo item.

    Attributes:
        id: Unique sequential identifier (starts at 1)
        title: Task title (1-200 characters)
        description: Optional task description (0-1000 characters)
        priority: Priority level (High, Medium, Low)
        status: Task status (Pending, Completed)
        created_at: UTC timestamp of task creation
    """

    id: int
    title: str
    description: str
    priority: Priority
    status: Status
    created_at: datetime

    @classmethod
    def create(
        cls,
        task_id: int,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
    ) -> "Todo":
        """
        Factory method to create a new Todo with defaults.

        Args:
            task_id: Unique identifier assigned by TodoService
            title: Task title (already validated and trimmed)
            description: Optional task description
            priority: Priority level (defaults to MEDIUM)

        Returns:
            New Todo instance with PENDING status and current timestamp
        """
        return cls(
            id=task_id,
            title=title,
            description=description,
            priority=priority,
            status=Status.PENDING,
            created_at=datetime.utcnow(),
        )
