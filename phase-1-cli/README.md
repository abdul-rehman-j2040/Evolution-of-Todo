# Phase 1 CLI - Professional In-Memory Python Todo CLI

A professional command-line todo application built with Python 3.10+.

## Features

- Add tasks with title, description, and priority
- List tasks with status filtering
- Update and delete tasks
- Mark tasks as complete
- Filter by priority level
- Search by keyword

## Requirements

- Python 3.10+
- UV package manager (recommended)

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd Evolution-of-Todo/phase-1-cli

# Create virtual environment
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies (none required for core functionality)
# Optional: pip install pytest mypy
```

## Usage

```bash
# Add a task
python -m src.cli.main add "Buy groceries"

# Add a task with description and priority
python -m src.cli.main add "Fix bug" -d "Login error on Safari" -p high

# List all tasks
python -m src.cli.main list

# List only pending tasks
python -m src.cli.main list --status pending

# Mark task as complete
python -m src.cli.main complete 1

# Delete a task
python -m src.cli.main delete 2

# Filter by priority
python -m src.cli.main filter high

# Search tasks
python -m src.cli.main search groceries
```

## Architecture

This project follows a service-layer architecture:

- **src/models/**: Data models (Todo, Priority, Status)
- **src/services/**: Business logic (TodoService)
- **src/cli/**: Command-line interface (argparse)

## License

MIT
