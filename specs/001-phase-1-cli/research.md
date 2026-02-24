# Research & Design Decisions: Phase I CLI

**Feature**: Phase I - Professional In-Memory Python Todo CLI
**Date**: 2025-12-31
**Status**: Approved

---

## Overview

This document captures the critical architecture decisions made during the planning phase of Phase I. Each decision includes context, rationale, alternatives considered, and Phase II impact analysis to ensure long-term architectural continuity.

**Key Principle**: All decisions prioritize **Phase II reusability** while maintaining **constitution compliance** (Standard Library Only, Service Pattern, Type Safety).

---

## Decision 1: Dataclass vs Pydantic for Todo Model

### Context

The user initially suggested Pydantic models, which provide runtime validation, serialization to JSON/dict, and automatic API documentation generation. However, the constitution mandates "Standard Library Only" for Phase I.

### Decision

**Use Python dataclasses (standard library)**

### Rationale

1. **Constitution Compliance**: Dataclasses are built-in (Python 3.7+), requiring no external dependencies
2. **Type Safety**: Full support for type hints and mypy --strict validation
3. **Simplicity**: Automatic generation of `__init__`, `__repr__`, `__eq__` methods
4. **Lightweight**: Minimal runtime overhead compared to Pydantic's validation layer
5. **Phase II Compatibility**: Dataclasses can be easily converted to Pydantic models or SQLModel in Phase II without changing service method signatures

### Alternatives Considered

| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| **Pydantic** | Runtime validation, JSON serialization, FastAPI integration | External dependency | Violates constitution "Standard Library Only" requirement |
| **NamedTuple** | Immutable, hashable, lightweight | Cannot update fields | Tasks need to be updated (title, description, status, priority) |
| **Plain Class** | Maximum flexibility | Manual `__init__`, `__repr__`, `__eq__` boilerplate | Dataclasses provide same functionality with less code |
| **attrs** | More features than dataclasses | External dependency | Violates constitution; dataclasses sufficient for Phase I |

### Implementation Example

```python
from dataclasses import dataclass
from datetime import datetime
from .enums import Priority, Status

@dataclass
class Todo:
    id: int
    title: str
    description: str
    priority: Priority
    status: Status
    created_at: datetime
```

### Phase II Impact

In Phase II, we can extend the dataclass to **SQLModel** (which inherits from both Pydantic BaseModel and SQLAlchemy DeclarativeBase) with minimal changes:

```python
# Phase II: SQLModel extends Pydantic and SQLAlchemy
from sqlmodel import Field, SQLModel
from datetime import datetime
from .enums import Priority, Status

class Todo(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=1000)
    priority: Priority = Field(default=Priority.MEDIUM)
    status: Status = Field(default=Status.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")  # Multi-user support
```

**Key Compatibility**:
- TodoService methods accept and return `Todo` objects in both phases
- SQLModel objects are duck-type compatible with dataclasses
- Type hints remain valid
- No service method signature changes required

---

## Decision 2: Synchronous vs Asynchronous Service Methods

### Context

The user initially suggested async methods to prepare for FastAPI in Phase II. Modern Python web frameworks like FastAPI strongly encourage async/await for I/O operations.

### Decision

**Use synchronous methods (no async/await)**

### Rationale

1. **YAGNI Principle**: Phase I has no I/O operations (in-memory only), so async provides no benefit
2. **Simplicity**: Synchronous code is easier to reason about, debug, and test
3. **No Blocking Operations**: All operations are CPU-bound list operations (<2s for 100 tasks)
4. **Phase II Compatibility**: FastAPI can wrap synchronous methods in async endpoints using `run_in_executor` or directly (FastAPI supports both sync and async route handlers)
5. **Testing**: Synchronous tests are simpler (no need for pytest-asyncio, event loops)

### Alternatives Considered

| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| **Async/Await** | Future-proof for FastAPI, modern pattern | Added complexity, requires event loop, async test fixtures | No I/O operations in Phase I; premature optimization |
| **Threading** | Parallelism for multi-core | Complexity, race conditions, GIL limits | Single-user CLI doesn't benefit from threading |
| **Multiprocessing** | True parallelism | High overhead, serialization costs | Overkill for <100 tasks in-memory operations |

### Implementation Example

```python
# Phase I: Synchronous methods
class TodoService:
    def __init__(self) -> None:
        self._tasks: List[Todo] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "", priority: Priority = Priority.MEDIUM) -> tuple[Optional[Todo], Optional[str]]:
        """Synchronous method - no await needed"""
        title = title.strip()
        if not title:
            return None, "Title cannot be empty"
        if len(title) > 200:
            return None, "Title cannot exceed 200 characters"

        todo = Todo(
            id=self._next_id,
            title=title,
            description=description,
            priority=priority,
            status=Status.PENDING,
            created_at=datetime.utcnow()
        )
        self._tasks.append(todo)
        self._next_id += 1
        return todo, None
```

### Phase II Impact

FastAPI endpoints will wrap TodoService methods. FastAPI supports both sync and async handlers, so we have flexibility:

**Option 1: Keep sync service, use async endpoints** (Recommended)
```python
# Phase II: FastAPI endpoint (async) calling sync service
from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool

@app.post("/tasks", response_model=TodoResponse)
async def create_task(task: TaskCreate, user_id: str = Depends(get_current_user)):
    # FastAPI will automatically run in threadpool if needed
    todo, error = todo_service.add_task(task.title, task.description, task.priority)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return todo
```

**Option 2: Convert service to async in Phase II** (If database I/O added)
```python
# Phase II: If we add async database operations
class TodoService:
    async def add_task(self, title: str, description: str = "") -> tuple[Optional[Todo], Optional[str]]:
        # ... validation logic (same as Phase I) ...
        async with self._db.begin():
            todo = Todo(...)
            self._db.add(todo)
            await self._db.flush()
        return todo, None
```

**Key Decision**: We'll keep sync methods in Phase I and decide in Phase II based on database library choice (SQLModel with sync or async session).

---

## Decision 3: argparse vs Click for CLI Framework

### Context

Python has multiple CLI frameworks with different feature sets and philosophies:
- **argparse**: Standard library, verbose, full control
- **Click**: Third-party, decorator-based, opinionated
- **Typer**: Third-party, type-hint based, requires Click
- **Fire**: Third-party, magic auto-generation from functions

### Decision

**Use argparse (standard library)**

### Rationale

1. **Constitution Compliance**: argparse is built-in, requiring no external dependencies
2. **Sufficient Features**: Supports subcommands, options, help text, validation
3. **Wide Knowledge**: Most Python developers familiar with argparse
4. **Type Safety**: Works with type hints via manual validation
5. **Single-Command Pattern**: Aligns with Unix philosophy (e.g., `git add`, `docker run`)
6. **No Magic**: Explicit argument parsing without hidden behavior

### Alternatives Considered

| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| **Click** | Cleaner API, decorators, automatic help | External dependency, magic behavior | Violates constitution; argparse sufficient |
| **Typer** | Type-hint based, excellent errors | External dependency, requires Click | Violates constitution; argparse sufficient |
| **Fire** | Zero boilerplate, auto-generation | External dependency, too much magic | Violates constitution; unclear CLI contracts |
| **sys.argv parsing** | No framework needed | Manual parsing, no help text, error-prone | argparse provides significant value |

### Implementation Example

```python
# Phase I: argparse with subcommands
import argparse
from .services.todo_service import TodoService

def main() -> None:
    parser = argparse.ArgumentParser(description="Todo CLI - Task Management")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("-d", "--description", default="", help="Task description")
    add_parser.add_argument("-p", "--priority", default="medium", choices=["high", "medium", "low"], help="Priority level")

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument("-s", "--status", default="all", choices=["pending", "completed", "all"], help="Filter by status")

    # ... more subparsers ...

    args = parser.parse_args()
    service = TodoService()

    if args.command == "add":
        handle_add(service, args)
    elif args.command == "list":
        handle_list(service, args)
    # ... more handlers ...
```

### Phase II Impact

CLI will remain unchanged in Phase II. The web API is a separate interface to the same TodoService:

```
Phase I: CLI → TodoService → In-Memory List
Phase II: CLI → TodoService → In-Memory List (unchanged)
          Web UI → FastAPI → TodoService → Database
```

**No migration needed**: Phase I CLI code can be left as-is or optionally updated to call the FastAPI backend as a client.

---

## Decision 4: Error Handling Pattern

### Context

Service methods need to communicate errors to the CLI layer without throwing exceptions for expected failures (e.g., task not found, validation errors). Different patterns have different trade-offs for type safety and explicitness.

### Decision

**Use Optional/Result pattern with tuple returns**

### Rationale

1. **Type Safety**: `Optional[Todo]` for single results, `tuple[Optional[Todo], Optional[str]]` for operations
2. **Explicit Handling**: Forces CLI to handle error cases (no silent failures)
3. **No Magic**: Clear contract between service and CLI layers
4. **Phase II Compatibility**: Tuples map cleanly to HTTP status codes
5. **Standard Library**: No external dependencies (no Result library needed)

### Method Signatures

```python
# Query methods return Optional (None = not found)
def get_task(self, task_id: int) -> Optional[Todo]:
    """Returns None if task not found"""

# Mutation methods return (data, error) tuple
def add_task(self, title: str, description: str = "") -> tuple[Optional[Todo], Optional[str]]:
    """Returns (Todo, None) on success or (None, error_message) on failure"""

# List methods return empty list (not None) for "no results"
def list_tasks(self) -> List[Todo]:
    """Returns empty list if no tasks"""

def filter_by_priority(self, priority: Priority) -> List[Todo]:
    """Returns empty list if no matches"""
```

### Alternatives Considered

| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| **Exceptions** | Standard Python idiom | Exceptions for control flow is anti-pattern | "Task not found" is expected, not exceptional |
| **Result Class** (success/failure) | Rust-like ergonomics, chainable | External library or custom code | Overkill for Phase I; tuples sufficient |
| **Status Enums** | Explicit status codes | Verbose, parallel type system | Overly complex for simple error cases |
| **Logging + None** | Simple | Errors hidden from caller | CLI cannot display errors to user |

### Implementation Example

```python
# Service method
def add_task(self, title: str, description: str = "") -> tuple[Optional[Todo], Optional[str]]:
    title = title.strip()
    if not title:
        return None, "Title cannot be empty"
    if len(title) > 200:
        return None, "Title cannot exceed 200 characters"

    todo = Todo(id=self._next_id, title=title, ...)
    self._tasks.append(todo)
    self._next_id += 1
    return todo, None

# CLI handler
def handle_add(service: TodoService, args: argparse.Namespace) -> None:
    todo, error = service.add_task(args.title, args.description)
    if error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    print("Task added successfully!")
    print(f"ID: {todo.id}")
    print(f"Title: {todo.title}")
    # ...
```

### Phase II Impact

FastAPI endpoints will convert tuples to HTTP responses:

```python
@app.post("/tasks", response_model=TodoResponse, status_code=201)
async def create_task(task: TaskCreate, user_id: str = Depends(get_current_user)):
    todo, error = todo_service.add_task(task.title, task.description)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return todo

@app.get("/tasks/{task_id}", response_model=TodoResponse)
async def get_task(task_id: int, user_id: str = Depends(get_current_user)):
    todo = todo_service.get_task(task_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return todo
```

**Error Mapping**:
- `(None, error_message)` → HTTP 400 Bad Request
- `None` from get_task → HTTP 404 Not Found
- `[]` from list_tasks → HTTP 200 OK with empty array
- Exceptions → HTTP 500 Internal Server Error

---

## Decision 5: State Storage in TodoService

### Context

TodoService needs to store the task collection internally. Different storage patterns affect encapsulation, testability, and Phase II migration path.

### Decision

**Instance attribute `self._tasks: List[Todo]`**

### Rationale

1. **Encapsulation**: Private attribute (`_tasks`) prevents external modification
2. **Testability**: Easy to reset state between tests by creating new service instance
3. **Stateful Service**: Maintains task collection across method calls
4. **Phase II Compatibility**: Constructor can be updated to accept database session
5. **Thread-Safe**: Each TodoService instance has its own task list (matters for testing)

### Implementation

```python
class TodoService:
    def __init__(self) -> None:
        self._tasks: List[Todo] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> tuple[Optional[Todo], Optional[str]]:
        # ... validation ...
        todo = Todo(id=self._next_id, ...)
        self._tasks.append(todo)
        self._next_id += 1
        return todo, None

    def list_tasks(self) -> List[Todo]:
        return self._tasks.copy()  # Return copy to prevent external modification
```

### Alternatives Considered

| Alternative | Pros | Cons | Rejected Because |
|-------------|------|------|------------------|
| **Global Variable** | Simple, no class needed | Poor testability, shared state | Cannot reset between tests; bad encapsulation |
| **Singleton Pattern** | Single instance guaranteed | Global state, hard to test | Unnecessary complexity; same issues as global |
| **Class Variable** | Shared across instances | All instances share state | Breaks test isolation; confusing behavior |
| **Module-level state** | Simple, no class needed | Same as global variable | Poor encapsulation; cannot inject dependencies |

### Phase II Impact

Constructor will accept database session for Phase II:

```python
# Phase II: Database-backed TodoService
from sqlmodel import Session

class TodoService:
    def __init__(self, db: Session) -> None:
        self._db = db  # Replace in-memory list with database session

    def add_task(self, title: str, description: str = "") -> tuple[Optional[Todo], Optional[str]]:
        # ... validation (same as Phase I) ...
        todo = Todo(id=None, title=title, ...)  # ID assigned by database
        self._db.add(todo)
        self._db.commit()
        self._db.refresh(todo)  # Get auto-generated ID
        return todo, None

    def list_tasks(self) -> List[Todo]:
        return self._db.query(Todo).all()
```

**Migration Path**:
1. Phase I: `TodoService()` creates instance with in-memory list
2. Phase II: `TodoService(db)` accepts database session
3. Service methods remain unchanged (same signatures, same validation logic)
4. Tests update to use database fixtures or in-memory SQLite

---

## Summary Table

| Decision | Phase I Choice | Phase II Migration | Constitution Compliance |
|----------|----------------|-------------------|------------------------|
| **Data Model** | Dataclass | Extend to SQLModel | ✅ Standard library only |
| **Async/Sync** | Synchronous | Keep sync or convert to async | ✅ No unnecessary complexity |
| **CLI Framework** | argparse | Unchanged (CLI remains) | ✅ Standard library only |
| **Error Handling** | Optional/tuple returns | Map to HTTP status codes | ✅ Type-safe, explicit |
| **State Storage** | Instance attribute list | Inject database session | ✅ Encapsulated, testable |

---

## Phase Gate Checklist

Before proceeding to `/sp.tasks`, verify:

- [x] All 5 decisions documented with rationale
- [x] Phase II impact analysis included for each decision
- [x] Alternatives considered with rejection reasons
- [x] Constitution compliance verified (Standard Library Only)
- [x] Implementation examples provided
- [x] No external dependencies introduced

**Status**: APPROVED - Ready for task breakdown
