# CLI Contract: Complete Task Command

**Command**: `todo complete`
**Purpose**: Mark a task as completed
**Spec Reference**: FR-009, User Story 3

---

## Command Signature

```bash
todo complete <id>
```

### Positional Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | integer | Yes | Task ID to mark complete |

---

## Usage Examples

### Example 1: Mark task complete
```bash
todo complete 1
```

### Example 2: Mark multiple tasks complete
```bash
todo complete 2
todo complete 3
todo complete 5
```

---

## Success Output

**Format**: Structured confirmation with task details

```
Task marked as complete!
ID: 1
Title: Buy groceries
Status: Completed
```

**Fields**:
- `ID`: ID of completed task
- `Title`: Title of completed task (for confirmation)
- `Status`: New status (always "Completed")

**Exit Code**: `0`

---

## Error Cases

### Error 1: Task Not Found

**Input**:
```bash
todo complete 999
```

**Output**:
```
Error: Task with ID 999 not found
```

**Exit Code**: `1`

**Rationale**: Cannot mark non-existent task as complete (FR-015)

---

### Error 2: Invalid Task ID

**Input**:
```bash
todo complete 0
todo complete -1
todo complete abc
```

**Output**:
```
Error: Invalid task ID. Must be a positive integer
```

**Exit Code**: `1`

**Rationale**: Task IDs must be positive integers

---

## Idempotency

**Behavior**: Marking an already completed task as complete is idempotent (no error)

**Input** (task 1 already completed):
```bash
todo complete 1
```

**Output** (same as normal success):
```
Task marked as complete!
ID: 1
Title: Buy groceries
Status: Completed
```

**Exit Code**: `0`

**Rationale**: User's intent achieved (task is complete), no need to fail. This aligns with idempotent HTTP PUT/PATCH operations.

---

## Validation Rules

1. **Task ID**: Must be positive integer
2. **Task Existence**: Task with given ID must exist in collection
3. **Idempotent**: Marking completed task as complete again succeeds (no error)
4. **Immutable Fields**: Only status changes; all other fields preserved
5. **No Undo**: Phase I does not support marking task as incomplete (one-way operation)

---

## Service Layer Contract

**Method**: `TodoService.complete_task()`

**Signature**:
```python
def complete_task(self, task_id: int) -> tuple[Optional[Todo], Optional[str]]:
    """
    Mark task as completed by ID.

    Args:
        task_id: ID of task to mark complete

    Returns:
        (updated_todo, None) on success
        (None, error_message) if task not found

    Notes:
        - Updates task.status to Status.COMPLETED
        - All other fields (id, title, description, priority, created_at) unchanged
        - Idempotent: marking completed task as complete again succeeds
        - Updates task in-place in self._tasks list
    """
```

**Behavior**:
- Find task by ID in `self._tasks`
- Return `(None, "Task with ID {id} not found")` if not found
- Set `task.status = Status.COMPLETED`
- Return updated Todo object
- No error if already completed

**Implementation**:
```python
def complete_task(self, task_id: int) -> tuple[Optional[Todo], Optional[str]]:
    task = self.get_task(task_id)
    if task is None:
        return None, f"Task with ID {task_id} not found"

    task.status = Status.COMPLETED
    return task, None
```

---

## CLI Handler Implementation

**Pseudocode**:
```python
def handle_complete(service: TodoService, args: argparse.Namespace) -> None:
    # Validate task ID
    task_id, error = validate_id(args.id)
    if error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    # Call service method
    todo, error = service.complete_task(task_id)

    # Handle error
    if error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    # Display success
    print("Task marked as complete!")
    print(f"ID: {todo.id}")
    print(f"Title: {todo.title}")
    print(f"Status: {todo.status.value}")
    sys.exit(0)
```

---

## Acceptance Criteria

**From Spec (User Story 3, Scenario 1)**:

> **Given** a task with ID 1 has status "Pending", **When** I mark it as complete, **Then** its status changes to "Completed" while all other attributes remain unchanged

**Test**:
1. Run: `todo add "Buy groceries"`
2. Verify: Status is "Pending" (via `todo list`)
3. Run: `todo complete 1`
4. Verify: Output shows "Task marked as complete! ID: 1 ... Status: Completed"
5. Run: `todo list`
6. Verify: Task 1 status is "Completed", all other fields unchanged

**From Spec (User Story 3, Scenario 2)**:

> **Given** a task with ID 2 is already "Completed", **When** I mark it as complete again, **Then** it remains "Completed" with no error

**Test**:
1. Run: `todo add "Task 2"`
2. Run: `todo complete 2`
3. Run: `todo complete 2` (again)
4. Verify: Output shows success (no error)
5. Verify: Task 2 status remains "Completed"

**From Spec (User Story 3, Scenario 3)**:

> **Given** I have 5 tasks (3 pending, 2 completed), **When** I view the list, **Then** I can clearly distinguish which tasks are pending and which are completed

**Test**:
1. Add 5 tasks (IDs 1-5)
2. Run: `todo complete 2`
3. Run: `todo complete 4`
4. Run: `todo list`
5. Verify: Tasks 2 and 4 show Status "Completed", others show "Pending"
6. Run: `todo list --status pending`
7. Verify: Only tasks 1, 3, 5 shown
8. Run: `todo list --status completed`
9. Verify: Only tasks 2, 4 shown

---

## Phase I Limitations

**No "Uncomplete"**: Phase I does not support marking task as incomplete (going from Completed back to Pending). This is intentional simplicity. Phase V may add status transitions.

**No Completion Timestamp**: Phase I does not track when task was completed (only `created_at` exists). Phase V may add `completed_at` field.

**No Completion Notes**: Cannot add notes when marking complete. Phase V may add completion comments.

---

## Phase II Compatibility

**FastAPI Endpoint** (Phase II):
```python
@app.patch("/tasks/{task_id}/complete", response_model=TodoResponse)
async def complete_task(
    task_id: int,
    user_id: str = Depends(get_current_user)
):
    todo, error = todo_service.complete_task(task_id)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return todo
```

**Alternative Approach** (RESTful PATCH):
```python
@app.patch("/tasks/{task_id}", response_model=TodoResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,  # Contains status field
    user_id: str = Depends(get_current_user)
):
    # Allow updating status via general update endpoint
    ...
```

**Mapping**:
- CLI success (exit 0) → HTTP 200 OK
- CLI "Task not found" (exit 1) → HTTP 404 Not Found
- Service tuple `(Todo, None)` → HTTP 200 with updated Todo JSON
- Service tuple `(None, error)` → HTTP 404 with error detail

---

## References

- **Spec**: FR-009, FR-015, SC-004
- **User Story**: User Story 3 (Mark Tasks Complete)
- **Data Model**: [data-model.md](../data-model.md) (Status enum)
- **Research**: [research.md](../research.md) Decision 4 (Error Handling)
