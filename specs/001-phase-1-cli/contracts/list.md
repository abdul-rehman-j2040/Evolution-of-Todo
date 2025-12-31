# CLI Contract: List Tasks Command

**Command**: `todo list`
**Purpose**: Display all tasks or filter by status
**Spec Reference**: FR-006, User Story 1

---

## Command Signature

```bash
todo list [options]
```

### Optional Flags

| Flag | Short | Type | Default | Description |
|------|-------|------|---------|-------------|
| `--status` | `-s` | string | `all` | Filter by status (pending/completed/all) |

---

## Usage Examples

### Example 1: List all tasks
```bash
todo list
```

### Example 2: List only pending tasks
```bash
todo list --status pending
```

### Example 3: List only completed tasks
```bash
todo list -s completed
```

---

## Success Output

**Format**: ASCII table with headers and rows

```
ID | Title              | Description         | Priority | Status    | Created
---|--------------------|---------------------|----------|-----------|-------------------
1  | Buy groceries      | Milk, eggs, bread   | Medium   | Pending   | 2025-12-31 10:30
2  | Fix login bug      | Safari 401 error    | High     | Completed | 2025-12-31 11:15
3  | Deploy hotfix      |                     | High     | Pending   | 2025-12-31 12:00
```

**Columns**:
- `ID`: Task identifier (right-aligned)
- `Title`: Task title (left-aligned, truncated to 20 chars with "...")
- `Description`: Task description (left-aligned, truncated to 20 chars with "...")
- `Priority`: Priority level (left-aligned)
- `Status`: Task status (left-aligned)
- `Created`: Creation timestamp in YYYY-MM-DD HH:MM format (left-aligned)

**Truncation Rules**:
- Title/Description > 20 chars: Display first 17 chars + "..."
- Empty description: Display as empty cell (spaces)

**Exit Code**: `0`

---

## Empty List Output

**Condition**: No tasks exist or no tasks match filter

**Output (no tasks at all)**:
```
No tasks found.
```

**Output (no tasks match filter)**:
```
No pending tasks found.
```
or
```
No completed tasks found.
```

**Exit Code**: `0` (not an error)

---

## Sorting

**Default Sort Order**: By ID ascending (creation order)

**Rationale**: Simple, predictable, no additional sorting logic needed for Phase I

**Phase II Enhancement**: May add sorting by priority, status, created_at

---

## Filtering

### Filter by Status

**Flag**: `--status` or `-s`

**Valid Values**:
- `all` (default): Show all tasks regardless of status
- `pending`: Show only tasks with Status.PENDING
- `completed`: Show only tasks with Status.COMPLETED

**Case Handling**: Case-insensitive (e.g., "PENDING", "Pending", "pending" all valid)

**Invalid Value**:
```bash
todo list --status active
```

**Output**:
```
Error: Invalid status filter. Use pending, completed, or all
```

**Exit Code**: `1`

---

## Service Layer Contract

**Method**: `TodoService.list_tasks()` and `TodoService.filter_by_status()`

**Signatures**:
```python
def list_tasks(self) -> List[Todo]:
    """
    Get all tasks in creation order.

    Returns:
        List of all tasks (empty list if no tasks)
    """

def filter_by_status(self, status: Status) -> List[Todo]:
    """
    Get tasks filtered by status.

    Args:
        status: Status enum value (PENDING or COMPLETED)

    Returns:
        List of matching tasks (empty list if no matches)
    """
```

**Behavior**:
- Returns copy of list (not reference) to prevent external modification
- Empty list if no tasks (not None)
- Filtering does not modify internal state

---

## CLI Handler Implementation

**Pseudocode**:
```python
def handle_list(service: TodoService, args: argparse.Namespace) -> None:
    # Parse status filter (case-insensitive)
    status_filter = args.status.lower()

    # Get tasks based on filter
    if status_filter == "all":
        tasks = service.list_tasks()
    elif status_filter == "pending":
        tasks = service.filter_by_status(Status.PENDING)
    elif status_filter == "completed":
        tasks = service.filter_by_status(Status.COMPLETED)
    else:
        print("Error: Invalid status filter. Use pending, completed, or all", file=sys.stderr)
        sys.exit(1)

    # Handle empty result
    if not tasks:
        if status_filter == "all":
            print("No tasks found.")
        else:
            print(f"No {status_filter} tasks found.")
        sys.exit(0)

    # Display table
    print_table(tasks)
    sys.exit(0)

def print_table(tasks: List[Todo]) -> None:
    """Print tasks in ASCII table format"""
    # Header
    print("ID | Title              | Description         | Priority | Status    | Created")
    print("---|--------------------|---------------------|----------|-----------|-------------------")

    # Rows
    for task in tasks:
        title = truncate(task.title, 20)
        description = truncate(task.description, 20)
        created = task.created_at.strftime("%Y-%m-%d %H:%M")
        print(f"{task.id:<3}| {title:<19}| {description:<20}| {task.priority.value:<9}| {task.status.value:<10}| {created}")

def truncate(text: str, max_len: int) -> str:
    """Truncate text with ellipsis if too long"""
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."
```

---

## Acceptance Criteria

**From Spec (User Story 1, Scenario 2)**:

> **Given** I have added 3 tasks, **When** I view the task list, **Then** all 3 tasks are displayed with their ID, title, status, and priority in the order they were created

**Test**:
1. Run: `todo add "Task 1"`
2. Run: `todo add "Task 2"`
3. Run: `todo add "Task 3"`
4. Run: `todo list`
5. Verify: Output shows 3 tasks with IDs 1, 2, 3 in order

**From Spec (User Story 1, Scenario 3)**:

> **Given** an empty task list, **When** I view the task list, **Then** I see a message indicating no tasks exist

**Test**:
1. Start fresh CLI session (no tasks)
2. Run: `todo list`
3. Verify: Output shows "No tasks found."

---

## Phase II Compatibility

**FastAPI Endpoint** (Phase II):
```python
@app.get("/tasks", response_model=List[TodoResponse])
async def list_tasks(
    status: Optional[str] = Query(None, regex="^(pending|completed|all)$"),
    user_id: str = Depends(get_current_user)
):
    if status is None or status == "all":
        tasks = todo_service.list_tasks()
    elif status == "pending":
        tasks = todo_service.filter_by_status(Status.PENDING)
    elif status == "completed":
        tasks = todo_service.filter_by_status(Status.COMPLETED)

    return tasks
```

**Mapping**:
- CLI table format → HTTP JSON array
- CLI "No tasks found." → HTTP 200 with empty array `[]`
- Service empty list → HTTP 200 with `[]` (not 404)

---

## References

- **Spec**: FR-006, SC-002
- **User Story**: User Story 1 (Add and View Tasks)
- **Data Model**: [data-model.md](../data-model.md)
