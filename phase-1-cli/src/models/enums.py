"""Enumerations for the Todo CLI application.

Contains Priority and Status enums with string inheritance for
JSON serialization and database compatibility.
"""

from enum import Enum
from typing import Optional


class Priority(str, Enum):
    """
    Task priority levels.

    Inherits from str to enable string comparison and JSON serialization.
    """

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

    @classmethod
    def parse(cls, value: str) -> "Priority":
        """
        Convert user input to Priority enum (case-insensitive).

        Args:
            value: User input string (e.g., "high", "H", "medium", "m", "low", "l")

        Returns:
            Priority enum member

        Raises:
            ValueError: If the value doesn't match any valid priority
        """
        mapping: dict[str, Priority] = {
            "high": cls.HIGH,
            "h": cls.HIGH,
            "medium": cls.MEDIUM,
            "m": cls.MEDIUM,
            "med": cls.MEDIUM,
            "low": cls.LOW,
            "l": cls.LOW,
        }
        normalized = value.strip().lower()
        if normalized not in mapping:
            valid_options = ", ".join(["high/medium/low"])
            raise ValueError(
                f"Invalid priority: '{value}'. Use {valid_options}."
            )
        return mapping[normalized]


class Status(str, Enum):
    """
    Task completion status.

    Inherits from str for JSON serialization and database compatibility.
    """

    PENDING = "Pending"
    COMPLETED = "Completed"

    @classmethod
    def parse(cls, value: str) -> "Status":
        """
        Convert user input to Status enum (case-insensitive).

        Args:
            value: User input string (e.g., "pending", "p", "completed", "c", "done")

        Returns:
            Status enum member

        Raises:
            ValueError: If the value doesn't match any valid status
        """
        mapping: dict[str, Status] = {
            "pending": cls.PENDING,
            "p": cls.PENDING,
            "completed": cls.COMPLETED,
            "complete": cls.COMPLETED,
            "c": cls.COMPLETED,
            "done": cls.COMPLETED,
        }
        normalized = value.strip().lower()
        if normalized not in mapping:
            valid_options = ", ".join(["pending/completed"])
            raise ValueError(
                f"Invalid status: '{value}'. Use {valid_options}."
            )
        return mapping[normalized]


def validate_title(title: str) -> tuple[Optional[str], Optional[str]]:
    """
    Validate task title.

    Args:
        title: The title to validate

    Returns:
        tuple of (normalized_title, error_message)
        - On success: (normalized_title, None)
        - On failure: (None, error_message)
    """
    if not title:
        return None, "Title cannot be empty"

    normalized = title.strip()

    if not normalized:
        return None, "Title cannot be empty"

    if len(normalized) > 200:
        return None, "Title cannot exceed 200 characters"

    return normalized, None


def validate_description(
    description: str,
) -> tuple[Optional[str], Optional[str]]:
    """
    Validate task description.

    Args:
        description: The description to validate

    Returns:
        tuple of (description, error_message)
        - On success: (description, None)
        - On failure: (None, error_message)
    """
    if len(description) > 1000:
        return None, "Description cannot exceed 1000 characters"

    return description, None


def validate_id(id_str: str) -> tuple[Optional[int], Optional[str]]:
    """
    Validate task ID from CLI input.

    Args:
        id_str: String representation of the task ID

    Returns:
        tuple of (task_id, error_message)
        - On success: (task_id, None)
        - On failure: (None, error_message)
    """
    try:
        task_id = int(id_str)
    except ValueError:
        return None, "Invalid task ID. Must be a positive integer"

    if task_id <= 0:
        return None, "Invalid task ID. Must be a positive integer"

    return task_id, None
