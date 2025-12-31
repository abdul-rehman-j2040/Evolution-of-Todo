# CLI Contract: Update Task Command

**Command**: `todo update`
**Purpose**: Modify task title, description, or priority
**Spec Reference**: FR-007, FR-010, User Story 2

---

## Command Signature

```bash
todo update <id> [options]
```

### Positional Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | integer | Yes | Task ID to update |

### Optional Flags

| Flag | Short | Type | Default | Description |
|------|-------|------|---------|-------------|
| `--title` | `-t` | string | (unchanged) | New task title (1-200 characters) |
| `--description` | `-d` | string | (unchanged) | New task description (0-1000 characters) |
| `--priority` | `-p` | string | (unchanged) | New priority level (high/medium/low) |

**Note**: At least one flag must be provided

---

## Usage Examples

### Example 1: Update title only
```bash
todo update 1 --title "Buy organic groceries"
```

### Example 2: Update description only
```bash
todo update 1 -d "Whole milk, free-range eggs"
```

### Example 3: Update priority only
```bash
todo update 1 --priority high
```

### Example 4: Update multiple fields
```bash
todo update 1 -t "Buy groceries" -d "Whole milk, eggs" -p high
```

---

## Success Output

**Format**: Structured confirmation with all task details (including unchanged fields)

```
Task updated successfully!
ID: 1
Title: Buy organic groceries
Description: Milk, eggs, bread
Priority: Medium
Status: Pending
Created: 2025-12-31 10:30:45
```

**Fields**:
- `ID`: Unchanged (tasks cannot be renumbered)
- `Title`: Updated value or original if not specified
- `Description`: Updated value or original if not specified
- `Priority`: Updated value or original if not specified
- `Status`: Unchanged (use `todo complete` to change status)
- `Created`: Unchanged (original creation timestamp preserved)

**Exit Code**: `0`

---

## Error Cases

### Error 1: Task Not Found

**Input**:
```bash
todo update 999 --title "New title"
```

**Output**:
```
Error: Task with ID 999 not found
```

**Exit Code**: `1`

**Rationale**: Cannot update non-existent task (FR-015)

---

### Error 2: Invalid Task ID

**Input**:
```bash
todo update 0 --title "New title"
todo update -1 --title "New title"
todo update abc --title "New title"
```

**Output**:
```
Error: Invalid task ID. Must be a positive integer
```

**Exit Code**: `1`

**Rationale**: Task IDs must be positive integers

---

### Error 3: No Fields Provided

**Input**:
```bash
todo update 1
```

**Output**:
```
Error: At least one field must be specified (--title, --description, --priority)
```

**Exit Code**: `1`

**Rationale**: Update command requires at least one field to update

---

### Error 4: Title Validation Errors

**Input**:
```bash
todo update 1 --title ""
todo update 1 --title "   "
todo update 1 --title "<201 characters>"
```

**Output** (same as add command):
```
Error: Title cannot be empty
Error: Title cannot exceed 200 characters
```

**Exit Code**: `1`

**Rationale**: Same validation rules as add command (FR-013)

---

### Error 5: Description Validation Errors

**Input**:
```bash
todo update 1 --description "<1001 characters>"
```

**Output**:
```
Error: Description cannot exceed 1000 characters
```

**Exit Code**: `1`

**Rationale**: Same validation rules as add command (FR-014)

---

### Error 6: Invalid Priority

**Input**:
```bash
todo update 1 --priority urgent
```

**Output**:
```
Error: Invalid priority level. Use high, medium, or low
```

**Exit Code**: `1`

**Rationale**: Same validation rules as add command (FR-010)

---

## Validation Rules

1. **Task ID**: Must be positive integer and exist in collection
2. **At Least One Field**: Cannot call update without any flags
3. **Title Validation**: Same as add command (non-empty after trim, ≤200 chars)
4. **Description Validation**: Same as add command (≤1000 chars)
5. **Priority Validation**: Same as add command (valid enum value)
6. **Partial Updates**: Only specified fields are updated; others remain unchanged
7. **Immutable Fields**: ID, status, created_at cannot be modified via update command

---

## Service Layer Contract

**Method**: `TodoService.update_task()`

**Signature**:
```python
def update_task(
    self,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[Priority] = None
) -> tuple[Optional[Todo], Optional[str]]:
    """
    Update task fields by ID.

    Args:
        task_id: ID of task to update
        title: New title (if provided, will be trimmed and validated)
        description: New description (if provided, will be validated)
        priority: New priority (if provided)

    Returns:
        (updated_todo, None) on success
        (None, error_message) on failure (task not found or validation error)

    Notes:
        - Only provided fields are updated (None = no change)
        - ID, status, created_at are immutable
        - Updates modify task in-place in self._tasks list
    """
```

**Behavior**:
- Find task by ID in `self._tasks`
- Return `(None, "Task with ID {id} not found")` if not found
- Validate title if provided (same as add_task)
- Validate description if provided (same as add_task)
- Update only specified fields (None = no change)
- ID, status, created_at remain unchanged
- Return updated Todo object

---

## CLI Handler Implementation

**Pseudocode**:
```python
def handle_update(service: TodoService, args: argparse.Namespace) -> None:
    # Validate task ID
    task_id, error = validate_id(args.id)
    if error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    # Check at least one field provided
    if not any([args.title, args.description, args.priority]):
        print("Error: At least one field must be specified (--title, --description, --priority)", file=sys.stderr)
        sys.exit(1)

    # Parse priority if provided (case-insensitive)
    priority = None
    if args.priority:
        try:
            priority = parse_priority(args.priority)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    # Call service method
    todo, error = service.update_task(
        task_id=task_id,
        title=args.title,
        description=args.description,
        priority=priority
    )

    # Handle error
    if error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    # Display success (same format as add)
    print("Task updated successfully!")
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

**From Spec (User Story 2, Scenario 1)**:

> **Given** a task exists with ID 1, **When** I update its title to "Buy organic groceries" and description to "Whole milk, free-range eggs, whole grain bread", **Then** the task's title and description are updated while preserving its ID, priority, status, and created timestamp

**Test**:
1. Run: `todo add "Buy groceries" -d "Milk, eggs, bread"`
2. Capture original ID, priority, status, created_at
3. Run: `todo update 1 -t "Buy organic groceries" -d "Whole milk, free-range eggs, whole grain bread"`
4. Verify: Title and description updated
5. Verify: ID, priority, status, created_at unchanged

**From Spec (User Story 2, Scenario 3)**:

> **Given** I attempt to update a non-existent task ID, **When** I execute the update command, **Then** I receive a clear error message stating the task was not found

**Test**:
1. Run: `todo update 999 --title "New title"`
2. Verify: Output shows "Error: Task with ID 999 not found"
3. Verify: Exit code 1

---

## Phase II Compatibility

**FastAPI Endpoint** (Phase II):
```python
@app.patch("/tasks/{task_id}", response_model=TodoResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    user_id: str = Depends(get_current_user)
):
    todo, error = todo_service.update_task(
        task_id=task_id,
        title=task_update.title,
        description=task_update.description,
        priority=task_update.priority
    )
    if error:
        if "not found" in error.lower():
            raise HTTPException(status_code=404, detail=error)
        else:
            raise HTTPException(status_code=400, detail=error)
    return todo
```

**Mapping**:
- CLI success (exit 0) → HTTP 200 OK
- CLI "Task not found" (exit 1) → HTTP 404 Not Found
- CLI validation error (exit 1) → HTTP 400 Bad Request
- Service tuple `(Todo, None)` → HTTP 200 with Todo JSON
- Service tuple `(None, error)` → HTTP 404 or 400 with error detail

---

## References

- **Spec**: FR-007, FR-010, FR-013, FR-014, FR-015, SC-003
- **User Story**: User Story 2 (Update and Delete Tasks)
- **Data Model**: [data-model.md](../data-model.md)
- **Research**: [research.md](../research.md) Decision 4 (Error Handling)
