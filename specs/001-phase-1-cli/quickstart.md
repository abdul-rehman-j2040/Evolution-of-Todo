# Quickstart Guide: Phase I Todo CLI

**Feature**: Phase I - Professional In-Memory Python Todo CLI
**Date**: 2025-12-31
**Audience**: End users and developers

---

## Overview

This CLI application provides professional task management with priorities, filtering, and search capabilities. All data is stored in-memory during the session (no persistence in Phase I).

**Key Features**:
- Add, update, delete tasks
- Mark tasks as complete
- Filter by priority (High, Medium, Low)
- Search by keyword
- Clean command-line interface

---

## Prerequisites

### Required Software

**Python 3.10 or higher**:
- Windows: Download from [python.org](https://www.python.org/downloads/)
- macOS: `brew install python@3.10`
- Linux: `sudo apt install python3.10` (Ubuntu/Debian)

**UV Package Manager** (recommended):
```bash
pip install uv
```

**Alternative**: Standard pip/venv (if UV not available)

---

## Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/your-org/Evolution-of-Todo.git
cd Evolution-of-Todo/phase-1-cli
```

### Step 2: Create Virtual Environment

**Using UV** (recommended):
```bash
uv venv
```

**Using standard venv**:
```bash
python -m venv .venv
```

### Step 3: Activate Virtual Environment

**Windows**:
```bash
.venv\Scripts\activate
```

**macOS/Linux**:
```bash
source .venv/bin/activate
```

### Step 4: Install Dependencies

**Phase I has no external dependencies** (standard library only)

Optional (for testing):
```bash
pip install pytest mypy black
```

---

## Basic Usage

### Running Commands

**Full Command**:
```bash
python -m src.cli.main <command> [arguments] [options]
```

**Create Alias** (optional, for convenience):

**macOS/Linux** (add to `~/.bashrc` or `~/.zshrc`):
```bash
alias todo='python -m src.cli.main'
```

**Windows** (PowerShell profile):
```powershell
function todo { python -m src.cli.main @args }
```

After creating alias:
```bash
todo add "Buy groceries"
todo list
```

---

## Command Reference

### 1. Add Task

**Purpose**: Create a new task with title, optional description, and priority

**Syntax**:
```bash
todo add <title> [--description <text>] [--priority <level>]
```

**Examples**:
```bash
# Minimal (title only, defaults: priority=medium, status=pending)
todo add "Buy groceries"

# With description
todo add "Buy groceries" --description "Milk, eggs, bread"

# With description and priority
todo add "Fix login bug" -d "Safari returns 401 on valid credentials" -p high

# Using shorthand flags
todo add "Deploy hotfix" -d "Production down" -p h
```

**Output**:
```
Task added successfully!
ID: 1
Title: Buy groceries
Description: Milk, eggs, bread
Priority: Medium
Status: Pending
Created: 2025-12-31 10:30:45
```

---

### 2. List Tasks

**Purpose**: Display all tasks or filter by status

**Syntax**:
```bash
todo list [--status <status>]
```

**Examples**:
```bash
# List all tasks
todo list

# List only pending tasks
todo list --status pending

# List only completed tasks
todo list -s completed
```

**Output**:
```
ID | Title              | Description         | Priority | Status    | Created
---|--------------------|---------------------|----------|-----------|-------------------
1  | Buy groceries      | Milk, eggs, bread   | Medium   | Pending   | 2025-12-31 10:30
2  | Fix login bug      | Safari 401 error    | High     | Completed | 2025-12-31 11:15
```

**Empty List**:
```
No tasks found.
```

---

### 3. Update Task

**Purpose**: Modify task title, description, or priority

**Syntax**:
```bash
todo update <id> [--title <text>] [--description <text>] [--priority <level>]
```

**Examples**:
```bash
# Update title only
todo update 1 --title "Buy organic groceries"

# Update description only
todo update 1 -d "Whole milk, free-range eggs"

# Update priority only
todo update 1 --priority high

# Update multiple fields
todo update 1 -t "Buy groceries" -d "Whole milk, eggs" -p high
```

**Output**:
```
Task updated successfully!
ID: 1
Title: Buy organic groceries
Description: Whole milk, free-range eggs
Priority: High
Status: Pending
Created: 2025-12-31 10:30:45
```

**Note**: ID, status, and created timestamp remain unchanged

---

### 4. Delete Task

**Purpose**: Permanently remove a task

**Syntax**:
```bash
todo delete <id>
```

**Examples**:
```bash
# Delete task by ID
todo delete 2
```

**Output**:
```
Task deleted successfully!
ID: 2
Title: Fix login bug
```

**Warning**: Deletion is permanent (no undo in Phase I)

---

### 5. Mark Task Complete

**Purpose**: Change task status from Pending to Completed

**Syntax**:
```bash
todo complete <id>
```

**Examples**:
```bash
# Mark task as complete
todo complete 1
```

**Output**:
```
Task marked as complete!
ID: 1
Title: Buy groceries
Status: Completed
```

**Note**: Marking an already completed task as complete is idempotent (no error)

---

### 6. Filter by Priority

**Purpose**: Display tasks filtered by priority level

**Syntax**:
```bash
todo filter <priority>
```

**Examples**:
```bash
# Show high priority tasks
todo filter high

# Show medium priority tasks
todo filter medium

# Show low priority tasks
todo filter low

# Case-insensitive
todo filter HIGH
```

**Output**:
```
ID | Title              | Description         | Priority | Status    | Created
---|--------------------|---------------------|----------|-----------|-------------------
2  | Fix login bug      | Safari 401 error    | High     | Completed | 2025-12-31 11:15
5  | Deploy hotfix      |                     | High     | Pending   | 2025-12-31 12:00
```

**Empty Result**:
```
No tasks found with priority: High
```

---

### 7. Search by Keyword

**Purpose**: Find tasks by keyword in title or description

**Syntax**:
```bash
todo search <keyword>
```

**Examples**:
```bash
# Search by single word
todo search groceries

# Search by phrase (use quotes)
todo search "bug fix"

# Case-insensitive
todo search GROCERIES
```

**Output**:
```
ID | Title              | Description         | Priority | Status    | Created
---|--------------------|---------------------|----------|-----------|-------------------
1  | Buy groceries      | Milk, eggs, bread   | Medium   | Pending   | 2025-12-31 10:30
3  | Order groceries    | Online delivery     | Low      | Pending   | 2025-12-31 14:00
```

**Empty Result**:
```
No tasks found matching: groceries
```

**Note**: Searches both title and description (case-insensitive substring match)

---

## Common Workflows

### Workflow 1: Daily Task Management

```bash
# Start of day: View pending tasks
todo list --status pending

# Add new task
todo add "Complete project report" -d "Due Friday" -p high

# Work on task, then mark complete
todo complete 1

# End of day: Review completed tasks
todo list --status completed
```

---

### Workflow 2: Prioritize Work

```bash
# View all high priority tasks
todo filter high

# Add urgent task
todo add "Fix production bug" -p high

# Upgrade existing task priority
todo update 3 --priority high

# Work through high priority tasks first
todo complete 2
todo complete 5
```

---

### Workflow 3: Task Organization

```bash
# Add tasks with categories in description
todo add "Buy groceries" -d "Category: Personal"
todo add "Fix bug" -d "Category: Work"

# Search by category
todo search "Category: Work"

# Update task details
todo update 1 --description "Category: Personal | Weekly shopping"
```

---

## Error Handling

### Common Errors

**1. Empty Title**
```bash
todo add ""
# Error: Title cannot be empty
```

**2. Title Too Long**
```bash
todo add "<201 characters>"
# Error: Title cannot exceed 200 characters
```

**3. Task Not Found**
```bash
todo update 999 --title "New title"
# Error: Task with ID 999 not found
```

**4. Invalid Priority**
```bash
todo add "Task" --priority urgent
# Error: Invalid priority level. Use high, medium, or low
```

**5. Invalid Task ID**
```bash
todo complete abc
# Error: Invalid task ID. Must be a positive integer
```

---

## Tips and Best Practices

### 1. Use Descriptive Titles

**Good**: `"Fix login bug on Safari browser"`
**Bad**: `"Fix bug"`

### 2. Add Context in Descriptions

```bash
todo add "Deploy v2.0" -d "Checklist: Run tests, update docs, notify team"
```

### 3. Set Priorities Appropriately

- **High**: Urgent and important (production issues, deadlines)
- **Medium**: Important but not urgent (most regular tasks)
- **Low**: Nice-to-have, non-urgent (cleanup, optimizations)

### 4. Review Tasks Regularly

```bash
# Daily review
todo list --status pending

# Weekly review (clear completed)
todo list --status completed
```

### 5. Use Search for Long Task Lists

```bash
# Find all tasks related to a project
todo search "Project Alpha"

# Find all tasks with specific keyword
todo search meeting
```

---

## Keyboard Shortcuts (Shell)

### Bash/Zsh History

```bash
# Repeat last command
!!

# Search command history
Ctrl + R

# Navigate history
Up/Down arrows
```

### Command Editing

```bash
# Move to beginning/end of line
Ctrl + A / Ctrl + E

# Delete word
Ctrl + W

# Clear line
Ctrl + U
```

---

## Limitations (Phase I)

### No Persistence
- Tasks lost when application closes
- No save/load functionality
- Phase II will add database storage

### No Multi-User Support
- Single user per session
- No user authentication
- Phase II will add user accounts

### No Undo
- Deleted tasks cannot be recovered
- Updates cannot be reverted
- Phase V may add task history

### No Due Dates
- Cannot set task deadlines
- No reminders or notifications
- Phase V will add due date tracking

---

## Troubleshooting

### Issue: Command Not Found

**Problem**:
```bash
todo add "Task"
# todo: command not found
```

**Solution**:
1. Check alias is set: `alias todo`
2. Use full command: `python -m src.cli.main add "Task"`
3. Verify virtual environment activated: `which python`

---

### Issue: Module Not Found

**Problem**:
```bash
python -m src.cli.main add "Task"
# ModuleNotFoundError: No module named 'src'
```

**Solution**:
1. Verify current directory: `pwd` (should be `phase-1-cli/`)
2. Check project structure: `ls src/`
3. Ensure `__init__.py` files exist in all directories

---

### Issue: Invalid Python Version

**Problem**:
```bash
python --version
# Python 3.8.10
```

**Solution**:
1. Install Python 3.10+
2. Use explicit version: `python3.10 -m src.cli.main`
3. Update alias to use correct Python

---

## Next Steps

### For Users

1. **Daily Use**: Integrate into daily task management workflow
2. **Feedback**: Report bugs or feature requests
3. **Phase II**: Await web interface with persistence

### For Developers

1. **Run Tests**: `pytest tests/` (if tests implemented)
2. **Type Check**: `mypy src/ --strict`
3. **Format Code**: `black src/`
4. **Contribute**: See [CONTRIBUTING.md](../../CONTRIBUTING.md)

---

## Support

**Documentation**: [README.md](../../README.md)
**Specifications**: [spec.md](./spec.md), [plan.md](./plan.md)
**Contracts**: [contracts/](./contracts/)

**Phase II Preview**: Web interface with database persistence coming soon!

---

## Appendix: Command Summary

| Command | Purpose | Example |
|---------|---------|---------|
| `add` | Create new task | `todo add "Task" -d "Description" -p high` |
| `list` | Show all/filtered tasks | `todo list --status pending` |
| `update` | Modify task | `todo update 1 --title "New title"` |
| `delete` | Remove task | `todo delete 2` |
| `complete` | Mark as complete | `todo complete 1` |
| `filter` | Show by priority | `todo filter high` |
| `search` | Find by keyword | `todo search groceries` |

**Priority Levels**: high, medium, low (case-insensitive, shorthand: h, m, l)
**Status Values**: pending, completed
**ID Range**: Positive integers starting at 1
