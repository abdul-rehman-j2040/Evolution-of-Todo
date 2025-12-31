# CLI Contract: Add Task Command

**Command**: `todo add`
**Purpose**: Create a new task with title, optional description, and priority
**Spec Reference**: FR-001 to FR-005, User Story 1

---

## Command Signature

```bash
todo add <title> [options]
```

### Positional Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `title` | string | Yes | Task title (1-200 characters) |

### Optional Flags

| Flag | Short | Type | Default | Description |
|------|-------|------|---------|-------------|
| `--description` | `-d` | string | `""` | Task description (0-1000 characters) |
| `--priority` | `-p` | string | `medium` | Priority level (high/medium/low) |

---

## Usage Examples

### Example 1: Minimal (title only)
```bash
todo add "Buy groceries"
```

### Example 2: With description
```bash
todo add "Buy groceries" --description "Milk, eggs, bread"
```

### Example 3: With description and priority
```bash
todo add "Fix login bug" -d "Safari returns 401 on valid credentials" -p high
```

### Example 4: High priority shorthand
```bash
todo add "Deploy hotfix" -p h
```

---

## Success Output

**Format**: Structured confirmation with all task details

```
Task added successfully!
ID: 1
Title: Buy groceries
Description: Milk, eggs, bread
Priority: Medium
Status: Pending
Created: 2025-12-31 10:30:45
```

**Fields**:
- `ID`: Auto-generated sequential integer (starts at 1)
- `Title`: User-provided title (trimmed)
- `Description`: User-provided description or empty
- `Priority`: Enum value (High/Medium/Low)
- `Status`: Always "Pending" for new tasks
- `Created`: UTC timestamp in YYYY-MM-DD HH:MM:SS format

**Exit Code**: `0`

---

## Error Cases

### Error 1: Empty Title

**Input**:
```bash
todo add ""
todo add "   "
```

**Output**:
```
Error: Title cannot be empty
```

**Exit Code**: `1`

**Rationale**: Title is required field (FR-013)

---

### Error 2: Title Too Long

**Input**:
```bash
todo add "<201 characters>"
```

**Output**:
```
Error: Title cannot exceed 200 characters
```

**Exit Code**: `1`

**Rationale**: Title limited to 200 characters (FR-013)

---

### Error 3: Description Too Long

**Input**:
```bash
todo add "Task" --description "<1001 characters>"
```

**Output**:
```
Error: Description cannot exceed 1000 characters
```

**Exit Code**: `1`

**Rationale**: Description limited to 1000 characters (FR-014)

---

### Error 4: Invalid Priority

**Input**:
```bash
todo add "Task" --priority urgent
todo add "Task" -p critical
```

**Output**:
```
Error: Invalid priority level. Use high, medium, or low
```

**Exit Code**: `1`

**Rationale**: Priority must be valid enum value (FR-010)

**Valid Values**: high, h, medium, m, med, low, l (case-insensitive)

---

## Validation Rules

1. **Title Trimming**: Leading/trailing whitespace automatically removed before validation
2. **Empty Check**: Title validated after trimming (empty string rejected)
3. **Length Validation**: Character count checked against limits
4. **Priority Normalization**: User input converted to enum (case-insensitive)
5. **Default Values**: Description defaults to `""`, priority defaults to `Priority.MEDIUM`

---

## Service Layer Contract

**Method**: `TodoService.add_task()`

**Signature**:
```python
def add_task(
    self,
    title: str,
    description: str = "",
    priority: Priority = Priority.MEDIUM
) -> tuple[Optional[Todo], Optional[str]]:
    """
    Add a new task to the in-memory collection.

    Args:
        title: Task title (will be trimmed)
        description: Optional task description
        priority: Priority level (defaults to MEDIUM)

    Returns:
        (Todo, None) on success
        (None, error_message) on validation failure
    """
```

**Behavior**:
- Validates title (non-empty after trim, ≤200 chars)
- Validates description (≤1000 chars)
- Assigns sequential ID starting from 1
- Sets status to `Status.PENDING`
- Sets created_at to `datetime.utcnow()`
- Appends to `self._tasks` list
- Increments `self._next_id`

---

## CLI Handler Implementation

**Pseudocode**:
```python
def handle_add(service: TodoService, args: argparse.Namespace) -> None:
    # Parse priority (case-insensitive)
    try:
        priority = parse_priority(args.priority)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Call service method
    todo, error = service.add_task(args.title, args.description, priority)

    # Handle error
    if error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    # Display success
    print("Task added successfully!")
    print(f"ID: {todo.id}")
    print(f"Title: {todo.title}")
    print(f"Description: {todo.description}")
    print(f"Priority: {todo.priority.value}")
    print(f"Status: {todo.status.value}")
    print(f"Created: {todo.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    sys.exit(0)
```

---

## Acceptance Criteria

**From Spec (User Story 1, Scenario 1)**:

> **Given** the CLI is launched, **When** I add a task with title "Buy groceries" and description "Milk, eggs, bread", **Then** the task is stored with a unique ID, the provided title and description, default priority "Medium", status "Pending", and current timestamp

**Test**:
1. Run: `todo add "Buy groceries" -d "Milk, eggs, bread"`
2. Verify: Output shows ID=1, Title="Buy groceries", Description="Milk, eggs, bread", Priority="Medium", Status="Pending"
3. Run: `todo list`
4. Verify: Task appears in list with correct details

---

## Phase II Compatibility

**FastAPI Endpoint** (Phase II):
```python
@app.post("/tasks", response_model=TodoResponse, status_code=201)
async def create_task(
    task: TaskCreate,
    user_id: str = Depends(get_current_user)
):
    todo, error = todo_service.add_task(
        title=task.title,
        description=task.description,
        priority=task.priority
    )
    if error:
        raise HTTPException(status_code=400, detail=error)
    return todo
```

**Mapping**:
- CLI success (exit 0) → HTTP 201 Created
- CLI validation error (exit 1) → HTTP 400 Bad Request
- Service tuple `(Todo, None)` → HTTP 201 with Todo JSON
- Service tuple `(None, error)` → HTTP 400 with error detail

---

## References

- **Spec**: FR-001, FR-002, FR-003, FR-004, FR-005, FR-013, FR-014
- **User Story**: User Story 1 (Add and View Tasks)
- **Data Model**: [data-model.md](../data-model.md)
- **Research**: [research.md](../research.md) Decision 4 (Error Handling)
