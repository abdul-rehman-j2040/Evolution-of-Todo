# CLI Contract: Filter Tasks by Priority Command

**Command**: `todo filter`
**Purpose**: Display tasks filtered by priority level
**Spec Reference**: FR-011, User Story 4

---

## Command Signature

```bash
todo filter <priority>
```

### Positional Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `priority` | string | Yes | Priority level (high/medium/low) |

---

## Usage Examples

### Example 1: Filter high priority tasks
```bash
todo filter high
```

### Example 2: Filter medium priority tasks
```bash
todo filter medium
```

### Example 3: Filter low priority tasks
```bash
todo filter low
```

### Example 4: Case-insensitive input
```bash
todo filter HIGH
todo filter Med
```

---

## Success Output

**Format**: ASCII table (same as `todo list`)

```
ID | Title              | Description         | Priority | Status    | Created
---|--------------------|---------------------|----------|-----------|-------------------
2  | Fix login bug      | Safari 401 error    | High     | Completed | 2025-12-31 11:15
5  | Deploy hotfix      |                     | High     | Pending   | 2025-12-31 12:00
```

**Columns**: Same as list command (ID, Title, Description, Priority, Status, Created)

**Sorting**: By ID ascending (creation order)

**Exit Code**: `0`

---

## Empty Result Output

**Condition**: No tasks match the priority filter

**Output**:
```
No tasks found with priority: High
```

**Exit Code**: `0` (not an error - valid query with no results)

---

## Error Cases

### Error 1: Invalid Priority

**Input**:
```bash
todo filter urgent
todo filter critical
todo filter 1
```

**Output**:
```
Error: Invalid priority level. Use high, medium, or low
```

**Exit Code**: `1`

**Rationale**: Priority must be valid enum value (FR-010)

---

## Validation Rules

1. **Priority Required**: Cannot call filter without priority argument
2. **Case-Insensitive**: Accepts "high", "High", "HIGH", "h", "H"
3. **Shorthand Accepted**: "h" → High, "m" → Medium, "l" → Low
4. **Status Independent**: Shows tasks regardless of status (both pending and completed)
5. **Empty Result**: Returns empty list (not error) if no matches

---

## Service Layer Contract

**Method**: `TodoService.filter_by_priority()`

**Signature**:
```python
def filter_by_priority(self, priority: Priority) -> List[Todo]:
    """
    Get tasks filtered by priority level.

    Args:
        priority: Priority enum value (HIGH, MEDIUM, or LOW)

    Returns:
        List of tasks matching priority (empty list if no matches)

    Notes:
        - Filters across all statuses (pending and completed)
        - Returns tasks in ID order (creation order)
        - Empty list if no matches (not None)
    """
```

**Behavior**:
- Filter `self._tasks` where `task.priority == priority`
- Return list of matching tasks (empty if no matches)
- Preserve creation order (sort by ID)

**Implementation**:
```python
def filter_by_priority(self, priority: Priority) -> List[Todo]:
    return [task for task in self._tasks if task.priority == priority]
```

---

## CLI Handler Implementation

**Pseudocode**:
```python
def handle_filter(service: TodoService, args: argparse.Namespace) -> None:
    # Parse priority (case-insensitive)
    try:
        priority = parse_priority(args.priority)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Call service method
    tasks = service.filter_by_priority(priority)

    # Handle empty result
    if not tasks:
        print(f"No tasks found with priority: {priority.value}")
        sys.exit(0)

    # Display table (same format as list command)
    print_table(tasks)
    sys.exit(0)
```

---

## Acceptance Criteria

**From Spec (User Story 4, Scenario 1)**:

> **Given** I have tasks with mixed priorities, **When** I filter by priority "High", **Then** only tasks with priority "High" are displayed

**Test**:
1. Run: `todo add "Task 1" -p high`
2. Run: `todo add "Task 2" -p medium`
3. Run: `todo add "Task 3" -p high`
4. Run: `todo add "Task 4" -p low`
5. Run: `todo filter high`
6. Verify: Only tasks 1 and 3 displayed (both High priority)

**From Spec (User Story 4, Scenario 2)**:

> **Given** I have 10 tasks, **When** I filter by priority "Low", **Then** only tasks with priority "Low" are displayed, regardless of their status

**Test**:
1. Add 10 tasks with mixed priorities (3 High, 4 Medium, 3 Low)
2. Mark 1 Low priority task as completed
3. Run: `todo filter low`
4. Verify: 3 Low priority tasks shown (including the completed one)
5. Verify: Status column shows mix of Pending and Completed

**From Spec (User Story 4, Scenario 3)**:

> **Given** no tasks match the priority filter, **When** I apply the filter, **Then** I see a message indicating no tasks match the filter criteria

**Test**:
1. Run: `todo add "Task 1" -p high`
2. Run: `todo add "Task 2" -p high`
3. Run: `todo filter low`
4. Verify: Output shows "No tasks found with priority: Low"

---

## Filter Logic

**Inclusive**: Shows tasks regardless of status (pending or completed)

**Exact Match**: Priority must exactly match (not partial)

**Example Collection**:
```
ID | Title    | Priority | Status
---|----------|----------|----------
1  | Task 1   | High     | Pending
2  | Task 2   | Medium   | Pending
3  | Task 3   | High     | Completed
4  | Task 4   | Low      | Pending
5  | Task 5   | Medium   | Completed
```

**Filter Results**:
- `todo filter high` → Tasks 1, 3 (both High, regardless of status)
- `todo filter medium` → Tasks 2, 5 (both Medium, regardless of status)
- `todo filter low` → Task 4 (only Low priority)

---

## Comparison with List Command

| Feature | `todo list` | `todo filter <priority>` |
|---------|-------------|--------------------------|
| **Purpose** | Show all/filtered by status | Show filtered by priority |
| **Filter** | Status (pending/completed/all) | Priority (high/medium/low) |
| **Default** | Shows all tasks | Requires priority argument |
| **Empty Result** | "No tasks found." | "No tasks found with priority: X" |
| **Status Filter** | Optional `--status` flag | Shows all statuses |

**Note**: `todo list` does NOT support priority filtering. Use `todo filter` for that.

---

## Phase II Compatibility

**FastAPI Endpoint** (Phase II):
```python
@app.get("/tasks", response_model=List[TodoResponse])
async def list_tasks(
    priority: Optional[str] = Query(None, regex="^(high|medium|low)$"),
    status: Optional[str] = Query(None, regex="^(pending|completed)$"),
    user_id: str = Depends(get_current_user)
):
    # Unified endpoint supporting both priority and status filters
    tasks = todo_service.list_tasks()

    if priority:
        priority_enum = parse_priority(priority)
        tasks = [t for t in tasks if t.priority == priority_enum]

    if status:
        status_enum = parse_status(status)
        tasks = [t for t in tasks if t.status == status_enum]

    return tasks
```

**Alternative**: Separate endpoints
- `GET /tasks?priority=high` (filter by priority)
- `GET /tasks?status=pending` (filter by status)
- `GET /tasks?priority=high&status=pending` (combined filters)

**Mapping**:
- CLI `todo filter high` → `GET /tasks?priority=high`
- CLI empty result → HTTP 200 with empty array `[]`
- CLI invalid priority → HTTP 400 Bad Request

---

## References

- **Spec**: FR-011, SC-005
- **User Story**: User Story 4 (Filter Tasks by Priority)
- **Data Model**: [data-model.md](../data-model.md) (Priority enum)
- **Research**: [research.md](../research.md) Decision 4 (Error Handling)
