# CLI Contract: Search Tasks by Keyword Command

**Command**: `todo search`
**Purpose**: Find tasks by keyword in title or description
**Spec Reference**: FR-012, User Story 5

---

## Command Signature

```bash
todo search <keyword>
```

### Positional Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `keyword` | string | Yes | Search term (case-insensitive) |

---

## Usage Examples

### Example 1: Search by single word
```bash
todo search groceries
```

### Example 2: Search by phrase (quoted)
```bash
todo search "bug fix"
```

### Example 3: Case-insensitive search
```bash
todo search GROCERIES
todo search Groceries
```

---

## Success Output

**Format**: ASCII table (same as `todo list`)

```
ID | Title              | Description         | Priority | Status    | Created
---|--------------------|---------------------|----------|-----------|-------------------
1  | Buy groceries      | Milk, eggs, bread   | Medium   | Pending   | 2025-12-31 10:30
3  | Order groceries    | Online delivery     | Low      | Pending   | 2025-12-31 14:00
```

**Columns**: Same as list command (ID, Title, Description, Priority, Status, Created)

**Sorting**: By ID ascending (creation order)

**Exit Code**: `0`

---

## Empty Result Output

**Condition**: No tasks match the search keyword

**Output**:
```
No tasks found matching: groceries
```

**Exit Code**: `0` (not an error - valid query with no results)

---

## Search Logic

### Matching Rules

1. **Case-Insensitive**: "Groceries", "groceries", "GROCERIES" all match
2. **Substring Match**: "gro" matches "groceries", "grow", "grocery"
3. **Title OR Description**: Matches if keyword appears in either field
4. **No Duplicates**: Each task appears once even if keyword matches both title and description
5. **Partial Words**: "fix" matches "fixing", "fixed", "prefix"
6. **Special Characters**: Treated as literals (no regex wildcards)

### Matching Algorithm

```python
def matches_keyword(task: Todo, keyword: str) -> bool:
    """Check if task matches keyword (case-insensitive substring)"""
    keyword_lower = keyword.lower()
    title_lower = task.title.lower()
    description_lower = task.description.lower()

    return keyword_lower in title_lower or keyword_lower in description_lower
```

### Example Matches

**Keyword**: "fix"

| Title | Description | Matches? | Reason |
|-------|-------------|----------|--------|
| "Fix bug" | "Login error" | Yes | "Fix" in title |
| "Hotfix deploy" | "Critical" | Yes | "fix" in title |
| "Update docs" | "Fix typos" | Yes | "Fix" in description |
| "Update code" | "Refactoring" | No | No "fix" in either field |

**Keyword**: "groceries"

| Title | Description | Matches? | Reason |
|-------|-------------|----------|--------|
| "Buy groceries" | "Milk" | Yes | "groceries" in title |
| "Shopping" | "Buy groceries online" | Yes | "groceries" in description |
| "Buy groceries" | "Also get groceries" | Yes | Matches once (no duplicate) |
| "Buy milk" | "Weekly shopping" | No | No "groceries" in either field |

---

## Special Character Handling

**No Regex Wildcards**: Search treats all characters as literals

**Examples**:
- Searching for `*` finds literal asterisk (not wildcard)
- Searching for `[test]` finds literal brackets (not character class)
- Searching for `.` finds literal period (not any character)

**Whitespace**: Multi-word searches must be quoted

```bash
# Correct: Searches for phrase "bug fix"
todo search "bug fix"

# Incorrect: Searches for "bug" and ignores "fix" (depends on shell parsing)
todo search bug fix
```

---

## Validation Rules

1. **Keyword Required**: Cannot call search without keyword argument
2. **Empty Keyword**: Treated as "no matches" (returns empty list)
3. **Whitespace Only**: Trimmed, treated as empty keyword
4. **Case Handling**: Converted to lowercase for comparison
5. **Status Independent**: Shows tasks regardless of status (pending/completed)
6. **Priority Independent**: Shows tasks regardless of priority

---

## Service Layer Contract

**Method**: `TodoService.search_tasks()`

**Signature**:
```python
def search_tasks(self, keyword: str) -> List[Todo]:
    """
    Search tasks by keyword in title or description.

    Args:
        keyword: Search term (case-insensitive substring match)

    Returns:
        List of tasks matching keyword (empty list if no matches)

    Notes:
        - Case-insensitive substring matching
        - Searches both title and description
        - Each task appears once (no duplicates)
        - Empty keyword returns empty list
        - Returns tasks in ID order (creation order)
    """
```

**Behavior**:
- Filter `self._tasks` where keyword appears in title OR description
- Case-insensitive comparison
- Return list of matching tasks (empty if no matches)
- Preserve creation order (sort by ID)

**Implementation**:
```python
def search_tasks(self, keyword: str) -> List[Todo]:
    if not keyword or not keyword.strip():
        return []

    keyword_lower = keyword.strip().lower()
    return [
        task for task in self._tasks
        if keyword_lower in task.title.lower() or keyword_lower in task.description.lower()
    ]
```

---

## CLI Handler Implementation

**Pseudocode**:
```python
def handle_search(service: TodoService, args: argparse.Namespace) -> None:
    # Get keyword from args
    keyword = args.keyword

    # Call service method
    tasks = service.search_tasks(keyword)

    # Handle empty result
    if not tasks:
        print(f"No tasks found matching: {keyword}")
        sys.exit(0)

    # Display table (same format as list command)
    print_table(tasks)
    sys.exit(0)
```

---

## Acceptance Criteria

**From Spec (User Story 5, Scenario 1)**:

> **Given** I have tasks with various titles and descriptions, **When** I search for keyword "groceries", **Then** all tasks containing "groceries" in title OR description are displayed (case-insensitive)

**Test**:
1. Run: `todo add "Buy groceries" -d "Milk, eggs"`
2. Run: `todo add "Shopping" -d "Get groceries online"`
3. Run: `todo add "Cook dinner" -d "Use ingredients"`
4. Run: `todo search groceries`
5. Verify: Tasks 1 and 2 displayed (both contain "groceries")
6. Verify: Task 3 NOT displayed (no "groceries")

**From Spec (User Story 5, Scenario 2)**:

> **Given** I search for a keyword that doesn't exist in any task, **When** I execute the search, **Then** I see a message indicating no tasks match the search term

**Test**:
1. Run: `todo add "Task 1" -d "Description 1"`
2. Run: `todo add "Task 2" -d "Description 2"`
3. Run: `todo search nonexistent`
4. Verify: Output shows "No tasks found matching: nonexistent"

**From Spec (User Story 5, Scenario 3)**:

> **Given** I search for keyword "project", **When** 5 tasks match in title and 3 match in description, **Then** all 8 unique tasks are displayed (no duplicates)

**Test**:
1. Add 8 tasks:
   - 5 with "project" in title, different descriptions
   - 3 with "project" in description, different titles
2. Run: `todo search project`
3. Verify: All 8 tasks displayed
4. Verify: No task appears twice

**Edge Case**: Task with "project" in both title AND description

**Test**:
1. Run: `todo add "Project planning" -d "Project kickoff meeting"`
2. Run: `todo search project`
3. Verify: Task appears once (not twice)

---

## Performance Considerations

### Phase I (In-Memory)

**Algorithm**: Linear scan (O(n) where n = number of tasks)

**Acceptable for**:
- Up to 100 tasks (per spec constraint)
- <2 seconds query time (SC-006)

**Implementation**: List comprehension with substring match

### Phase II (Database)

**Optimization**: Database-level text search

**PostgreSQL**:
```sql
SELECT * FROM todos
WHERE user_id = ? AND (
    LOWER(title) LIKE LOWER(CONCAT('%', ?, '%'))
    OR LOWER(description) LIKE LOWER(CONCAT('%', ?, '%'))
)
```

**SQLModel**:
```python
def search_tasks(self, keyword: str, db: Session) -> List[Todo]:
    keyword_pattern = f"%{keyword}%"
    return db.query(Todo).filter(
        or_(
            Todo.title.ilike(keyword_pattern),
            Todo.description.ilike(keyword_pattern)
        )
    ).all()
```

**Future Enhancement** (Phase V):
- Full-text search (PostgreSQL tsvector, Elasticsearch)
- Fuzzy matching (Levenshtein distance)
- Search result ranking

---

## Phase II Compatibility

**FastAPI Endpoint** (Phase II):
```python
@app.get("/tasks/search", response_model=List[TodoResponse])
async def search_tasks(
    q: str = Query(..., min_length=1, description="Search keyword"),
    user_id: str = Depends(get_current_user)
):
    tasks = todo_service.search_tasks(q)
    return tasks
```

**Alternative URL**: `GET /tasks?q=groceries` (unified with list endpoint)

**Mapping**:
- CLI `todo search groceries` → `GET /tasks/search?q=groceries`
- CLI empty result → HTTP 200 with empty array `[]`
- CLI keyword → URL query parameter (URL-encoded)

---

## References

- **Spec**: FR-012, SC-006
- **User Story**: User Story 5 (Search Tasks by Keyword)
- **Data Model**: [data-model.md](../data-model.md)
- **Research**: [research.md](../research.md) Decision 5 (State Storage)
