# CLI Contract: Delete Task Command

**Command**: `todo delete`
**Purpose**: Remove a task from the collection by ID
**Spec Reference**: FR-008, User Story 2

---

## Command Signature

```bash
todo delete <id>
```

### Positional Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | integer | Yes | Task ID to delete |

---

## Usage Examples

### Example 1: Delete a task
```bash
todo delete 1
```

### Example 2: Delete with explicit ID
```bash
todo delete 5
```

---

## Success Output

**Format**: Structured confirmation with deleted task details

```
Task deleted successfully!
ID: 1
Title: Buy groceries
```

**Fields**:
- `ID`: ID of deleted task
- `Title`: Title of deleted task (for confirmation)

**Rationale**: Showing deleted task details helps user confirm they deleted the correct task (especially important since deletion is irreversible in Phase I)

**Exit Code**: `0`

---

## Error Cases

### Error 1: Task Not Found

**Input**:
```bash
todo delete 999
```

**Output**:
```
Error: Task with ID 999 not found
```

**Exit Code**: `1`

**Rationale**: Cannot delete non-existent task (FR-015)

---

### Error 2: Invalid Task ID

**Input**:
```bash
todo delete 0
todo delete -1
todo delete abc
```

**Output**:
```
Error: Invalid task ID. Must be a positive integer
```

**Exit Code**: `1`

**Rationale**: Task IDs must be positive integers

---

## Validation Rules

1. **Task ID**: Must be positive integer
2. **Task Existence**: Task with given ID must exist in collection
3. **Irreversible**: No undo in Phase I (task permanently removed from in-memory list)
4. **ID Gap**: Deleting task 2 leaves IDs 1, 3, 4, ... (gaps are expected)
5. **No Cascade**: Deletion has no side effects (no related data in Phase I)

---

## Service Layer Contract

**Method**: `TodoService.delete_task()`

**Signature**:
```python
def delete_task(self, task_id: int) -> tuple[Optional[Todo], Optional[str]]:
    """
    Delete task by ID.

    Args:
        task_id: ID of task to delete

    Returns:
        (deleted_todo, None) on success
        (None, error_message) if task not found

    Notes:
        - Task removed from self._tasks list
        - Deletion is permanent (no undo in Phase I)
        - ID gaps are expected after deletion
        - self._next_id NOT decremented (IDs always increment)
    """
```

**Behavior**:
- Find task by ID in `self._tasks`
- Return `(None, "Task with ID {id} not found")` if not found
- Remove task from `self._tasks` list
- Return deleted Todo object for confirmation message
- Do NOT decrement `self._next_id` (IDs never reused)

**Implementation**:
```python
def delete_task(self, task_id: int) -> tuple[Optional[Todo], Optional[str]]:
    for i, task in enumerate(self._tasks):
        if task.id == task_id:
            deleted_task = self._tasks.pop(i)
            return deleted_task, None
    return None, f"Task with ID {task_id} not found"
```

---

## CLI Handler Implementation

**Pseudocode**:
```python
def handle_delete(service: TodoService, args: argparse.Namespace) -> None:
    # Validate task ID
    task_id, error = validate_id(args.id)
    if error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    # Call service method
    todo, error = service.delete_task(task_id)

    # Handle error
    if error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    # Display success
    print("Task deleted successfully!")
    print(f"ID: {todo.id}")
    print(f"Title: {todo.title}")
    sys.exit(0)
```

---

## Acceptance Criteria

**From Spec (User Story 2, Scenario 2)**:

> **Given** a task exists with ID 2, **When** I delete it, **Then** the task is removed from the list and subsequent view commands do not show it

**Test**:
1. Run: `todo add "Task 1"`
2. Run: `todo add "Task 2"`
3. Run: `todo add "Task 3"`
4. Run: `todo list` (verify 3 tasks: IDs 1, 2, 3)
5. Run: `todo delete 2`
6. Verify: Output shows "Task deleted successfully! ID: 2 Title: Task 2"
7. Run: `todo list`
8. Verify: Only tasks 1 and 3 appear (task 2 removed)

**From Spec (User Story 2, Scenario 4)**:

> **Given** I attempt to delete a non-existent task ID, **When** I execute the delete command, **Then** I receive a clear error message stating the task was not found

**Test**:
1. Run: `todo delete 999`
2. Verify: Output shows "Error: Task with ID 999 not found"
3. Verify: Exit code 1

---

## ID Gap Behavior

**Scenario**: User adds 3 tasks, then deletes task 2

**Before Deletion**:
```
ID | Title
---|-------
1  | Task 1
2  | Task 2
3  | Task 3
```

**After `todo delete 2`**:
```
ID | Title
---|-------
1  | Task 1
3  | Task 3
```

**Next Task Added** (`todo add "Task 4"`):
```
ID | Title
---|-------
1  | Task 1
3  | Task 3
4  | Task 4
```

**Rationale**: IDs are never reused. `self._next_id` always increments, even after deletion. This ensures:
- Unique IDs across session
- No confusion if user references old ID
- Simple implementation (no complex ID reuse logic)
- Phase II compatibility (database auto-increment works same way)

---

## Phase I Limitations

**No Confirmation Prompt**: Phase I does not ask "Are you sure?" before deletion. This is acceptable for simplicity, but may be added in Phase V with undo functionality.

**No Undo**: Deleted tasks cannot be recovered in Phase I (no history, no archive). Phase V may add task archiving instead of deletion.

**No Soft Delete**: Tasks are permanently removed from in-memory list. Phase II+ may implement soft delete (status: ARCHIVED) for audit trails.

---

## Phase II Compatibility

**FastAPI Endpoint** (Phase II):
```python
@app.delete("/tasks/{task_id}", response_model=TodoResponse)
async def delete_task(
    task_id: int,
    user_id: str = Depends(get_current_user)
):
    todo, error = todo_service.delete_task(task_id)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return todo  # Return deleted task for confirmation
```

**Mapping**:
- CLI success (exit 0) → HTTP 200 OK (returns deleted task JSON)
- CLI "Task not found" (exit 1) → HTTP 404 Not Found
- Service tuple `(Todo, None)` → HTTP 200 with deleted Todo JSON
- Service tuple `(None, error)` → HTTP 404 with error detail

**Alternative**: Some REST APIs use HTTP 204 No Content for successful deletion (no body returned). We chose 200 with body to match CLI confirmation behavior.

---

## References

- **Spec**: FR-008, FR-015, SC-003
- **User Story**: User Story 2 (Update and Delete Tasks)
- **Data Model**: [data-model.md](../data-model.md)
- **Research**: [research.md](../research.md) Decision 4 (Error Handling)
