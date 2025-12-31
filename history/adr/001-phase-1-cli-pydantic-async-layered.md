# ADR-001: Phase I Architecture Decisions - Dataclass, Synchronous Service, and Layered Architecture

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-01-01
- **Feature:** 001-phase-1-cli
- **Context:** Phase I establishes the foundational architecture for the Evolution of Todo ecosystem with an in-memory Python CLI. Three foundational decisions must be made: (1) data model representation, (2) service method patterns, and (3) architectural layering. These decisions must comply with the constitution's "Standard Library Only" constraint while enabling seamless Phase II migration to FastAPI + SQLModel.

## Decision

Three foundational architecture decisions for Phase I CLI implementation:

### 1. Data Model: Python dataclasses (no Pydantic)

The Todo model and related enums (Priority, Status) will use Python `dataclass` decorator from the standard library.

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class Priority(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class Status(str, Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"

@dataclass
class Todo:
    id: int
    title: str
    description: str
    priority: Priority
    status: Status
    created_at: datetime
```

### 2. Service Pattern: Synchronous methods in TodoService

All TodoService methods will be synchronous (no async/await) for Phase I.

```python
class TodoService:
    def __init__(self) -> None:
        self._tasks: List[Todo] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "", priority: Priority = Priority.MEDIUM) -> tuple[Optional[Todo], Optional[str]]:
        """Synchronous method - no async/await"""

    def get_task(self, task_id: int) -> Optional[Todo]:
        """Synchronous method - no async/await"""
```

### 3. Layered Architecture: Three-layer pattern

The application follows a strict three-layer architecture:

| Layer | Location | Responsibility | Contains Business Logic |
|-------|----------|----------------|-------------------------|
| Models | `src/models/` | Data structures and enums | No - pure data representation |
| Services | `src/services/` | Business logic and operations | Yes - all CRUD operations |
| CLI | `src/cli/` | User interface and argument parsing | No - only I/O handling |

## Consequences

### Positive

1. **Constitution Compliance**: Using dataclasses (standard library) satisfies the "Standard Library Only" constraint for Phase I without exceptions.

2. **Zero Dependencies**: The Phase I CLI requires no external packages, ensuring maximum portability and minimal attack surface.

3. **Phase II Migration Path**: SQLModel (Pydantic + SQLAlchemy) can extend dataclasses with minimal changes. The Todo dataclass will become a SQLModel model inheriting similar structure:
   ```python
   # Phase II migration (conceptual)
   from sqlmodel import SQLModel, Field

   class Todo(SQLModel, table=True):
       id: int | None = Field(default=None, primary_key=True)
       title: str
       description: str
       priority: str
       status: str
       created_at: datetime
   ```

4. **FastAPI Sync Compatibility**: FastAPI supports synchronous route handlers natively. Phase II endpoints can call TodoService methods directly without wrapping in `run_in_executor`:
   ```python
   @app.post("/tasks")
   def create_task(task: TaskCreate):
       # Direct sync call - FastAPI handles it
       todo, error = todo_service.add_task(task.title, task.description)
   ```

5. **Testability**: Synchronous code is easier to test without async test frameworks. Unit tests can use standard pytest without pytest-asyncio.

6. **Separation of Concerns**: CLI layer contains no business logic - only argument parsing and output formatting. All validation and state changes occur in TodoService.

7. **Maintainability**: Developers can locate logic by layer (models for data, services for operations, CLI for interface) without hunting through monolithic code.

### Negative

1. **Validation Overhead**: Pydantic provides automatic runtime validation with clear error messages. With dataclasses, validation must be implemented manually in service methods.

2. **Future Migration Effort**: Phase II will require refactoring dataclasses to SQLModel. While structurally similar, field types and decorators differ.

3. **No Async Benefits**: If Phase I requirements expand to include I/O (file system, network calls), the synchronous pattern would need refactoring.

4. **Manual Type Coercion**: Pydantic automatically coerces types (e.g., string "1" to int 1). Dataclasses require explicit conversion in the CLI layer.

## Alternatives Considered

### Data Model Alternatives

| Alternative | Why Rejected |
|-------------|--------------|
| Pydantic models | Violates "Standard Library Only" constraint. External dependency not permitted in Phase I. Can be adopted in Phase II when SQLModel is required. |
| NamedTuple | Immutability prevents task updates. Tasks require mutable state (status changes, title updates). |
| Plain Python class | Requires manual implementation of `__init__`, `__repr__`, `__eq__`. Dataclasses generate these automatically. |
| TypedDict | No runtime validation, poor IDE support for instantiation. |

### Service Pattern Alternatives

| Alternative | Why Rejected |
|-------------|--------------|
| Async/await methods | Premature optimization. In-memory list operations are CPU-bound, not I/O-bound. Async adds complexity without benefit. |
| Threading | Single-user CLI has no concurrency requirements. Threading would complicate debugging without value. |
| Trio async framework | External dependency violation. Adds learning curve for minimal benefit. |

### Architecture Layering Alternatives

| Alternative | Why Rejected |
|-------------|--------------|
| Monolithic CLI (all logic in main.py) | Violates Constitution Principle VI (Decoupled Logic). No testability, no Phase II reusability. |
| Two-layer (models + CLI only) | Business logic would leak into CLI layer. Violates separation of concerns. |
| Dependency injection framework | External dependency violation. Manual dependency injection sufficient for Phase I complexity. |

## References

- Feature Spec: `specs/001-phase-1-cli/spec.md`
- Implementation Plan: `specs/001-phase-1-cli/plan.md`
- Constitution: `.specify/memory/constitution.md`
- Related ADRs: None (this is the first ADR)
- Phase II Plan: FastAPI backend with SQLModel, inheriting Phase I TodoService pattern
