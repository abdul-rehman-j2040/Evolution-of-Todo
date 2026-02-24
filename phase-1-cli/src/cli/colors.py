"""Color and formatting utilities for the Todo CLI application.

Provides ANSI color codes and emoji helpers for terminal output.
"""

# ANSI Color Codes
class Colors:
    """Terminal color codes."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Background colors
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"


# Emoji helpers
class Emojis:
    """Emoji icons for the application."""
    TASK = "📋"
    ADD = "➕"
    VIEW = "👀"
    PENDING = "⏳"
    COMPLETED = "✅"
    UPDATE = "✏️"
    DELETE = "🗑️"
    FILTER = "🔍"
    SEARCH = "🔎"
    HIGH_PRIORITY = "🔴"
    MEDIUM_PRIORITY = "🟡"
    LOW_PRIORITY = "🟢"
    EXIT = "🚪"
    SUCCESS = "🎉"
    ERROR = "❌"
    WARNING = "⚠️"
    INFO = "ℹ️"
    STAR = "⭐"
    HEART = "❤️"
    CHECK = "✔️"
    BELL = "🔔"


def colorize(text: str, color: str) -> str:
    """
    Apply color to text.

    Args:
        text: The text to colorize
        color: ANSI color code

    Returns:
        Colorized text with reset code at the end
    """
    return f"{color}{text}{Colors.RESET}"


def bold(text: str) -> str:
    """Make text bold."""
    return colorize(text, Colors.BOLD)


def success(text: str) -> str:
    """Format text as success (green)."""
    return colorize(text, Colors.GREEN)


def error(text: str) -> str:
    """Format text as error (red)."""
    return colorize(text, Colors.RED)


def warning(text: str) -> str:
    """Format text as warning (yellow)."""
    return colorize(text, Colors.YELLOW)


def info(text: str) -> str:
    """Format text as info (cyan)."""
    return colorize(text, Colors.CYAN)


def priority_color(priority: "Priority") -> str:
    """Get color for priority level."""
    from src.models.enums import Priority
    if priority == Priority.HIGH:
        return Colors.RED
    elif priority == Priority.MEDIUM:
        return Colors.YELLOW
    else:
        return Colors.GREEN


def priority_emoji(priority: "Priority") -> str:
    """Get emoji for priority level."""
    from src.models.enums import Priority
    if priority == Priority.HIGH:
        return Emojis.HIGH_PRIORITY
    elif priority == Priority.MEDIUM:
        return Emojis.MEDIUM_PRIORITY
    else:
        return Emojis.LOW_PRIORITY


def status_emoji(status: "Status") -> str:
    """Get emoji for status."""
    from src.models.enums import Status
    if status == Status.COMPLETED:
        return Emojis.COMPLETED
    else:
        return Emojis.PENDING


def priority_colored(text: str, priority: "Priority") -> str:
    """Colorize text based on priority."""
    return colorize(text, priority_color(priority))


def status_colored(text: str, status: "Status") -> str:
    """Colorize text based on status."""
    from src.models.enums import Status
    if status == Status.COMPLETED:
        return colorize(text, Colors.GREEN)
    else:
        return colorize(text, Colors.YELLOW)
