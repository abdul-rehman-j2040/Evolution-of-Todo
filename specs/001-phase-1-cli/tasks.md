# Task Breakdown: Phase 1 - Professional In-Memory Python Todo CLI

**Feature Branch**: `001-phase-1-cli`
**Generated**: 2026-01-01
**Last Updated**: 2026-01-01
**Spec Reference**: [spec.md](./spec.md)
**Plan Reference**: [plan.md](./plan.md)

---

## Executive Summary

This document defines the atomic, testable tasks for implementing Phase 1 of the Evolution of Todo CLI. Tasks are organized into phases with clear dependencies, acceptance criteria, and complexity estimates.

**Total Tasks**: 42 (was 28)
**Estimated Total Effort**: ~3-4 hours of focused work
**Critical Path**: Setup → Models → Service Init → Add/List → MVP Complete
**Quick Win Tasks**: T-001, T-006, T-009, T-030

---

## Task Naming Convention

- **T-XXX**: Task identifier for commit messages and tracking
- **T-XXX-A/B/C**: Subtasks for complex tasks (letter suffix)
- **[P]**: Priority marker for task ordering
- **[US#]**: User Story reference (US1-US5)
- **Exact file paths**: All file paths are absolute and precise
- **Complexity**: S (5-10 min), M (15-30 min), L (30-60 min)

---

## MVP Scope (Recommended First 7 Tasks)

These tasks form the Minimum Viable Product core. Complete them first for rapid validation.

| Order | Task | Purpose | Time |
|-------|------|---------|------|
| 1 | T-001 | Project directory structure | S |
| 2 | T-006 | Priority enum | S |
| 3 | T-007 | Status enum | S |
| 4 | T-008 | Todo dataclass | S |
| 5 | T-009 | TodoService init | S |
| 6 | T-010 | add_task method | M |
| 7 | T-017-A | add command parser | S |

**MVP Verification**: After T-017-A, you can: `python -m src.cli.main add "Test task"` and see success output.

---

## Quick Wins (Can Start Immediately)

These tasks provide immediate momentum and validate the development environment:

- **T-001**: Create project directory structure - pure file/folder creation, no logic
- **T-006**: Priority enum - simple enum definition, quick win
- **T-007**: Status enum - same as Priority, can do in parallel
- **T-030**: Add command handler - satisfies "add a task" user story immediately

---

## Phase 1: Project Setup

**Purpose**: Establish project structure and configuration
**Tasks**: 5
**Dependencies**: None (can start immediately)
**Parallelizable**: T-002, T-003, T-004 can run after T-001

```
- [X] T-001 [P] Create project directory structure per implementation plan
  - **Description**: Create the phase-1-cli directory structure as defined in plan.md:
    - phase-1-cli/src/ (with __init__.py)
    - phase-1-cli/src/models/ (with __init__.py)
    - phase-1-cli/src/services/ (with __init__.py)
    - phase-1-cli/src/cli/ (with __init__.py)
    - phase-1-cli/tests/unit/ (with __init__.py)
    - phase-1-cli/tests/integration/ (with __init__.py)
  - **Inputs**: Project plan structure from plan.md
  - **Outputs**: Directory structure created at D:\Hackathons\Evolution-of-Todo\phase-1-cli\
  - **Acceptance Criteria**:
    - [ ] All 6 directories created with __init__.py files
    - [ ] Directory structure matches plan.md specification
    - [ ] Python recognizes packages (can import src)
  - **Complexity**: S (5 min)
  - **Time Estimate**: 5 minutes
  - **Dependencies**: None
  - **Quick Win**: Yes - immediate validation of project structure

- [X] T-002 Create pyproject.toml with UV configuration
  - **Description**: Create pyproject.toml with project metadata, Python version, and UV tool configuration per plan.md
  - **Inputs**: Python 3.10+ requirement, standard library only constraint
  - **Outputs**: D:\Hackathons\Evolution-of-Todo\phase-1-cli\pyproject.toml
  - **Acceptance Criteria**:
    - [ ] pyproject.toml includes [project] section with name, version, description
    - [ ] Python requirement set to >=3.10
    - [ ] [tool.uv] section configured for UV package manager
    - [ ] mypy configuration for --strict compliance
    - [ ] pytest as optional dev dependency
  - **Complexity**: S (5 min)
  - **Time Estimate**: 5 minutes
  - **Dependencies**: T-001

- [X] T-003 Create .python-version file
  - **Description**: Create .python-version file specifying Python 3.10
  - **Inputs**: Python 3.10+ requirement from spec.md
  - **Outputs**: D:\Hackathons\Evolution-of-Todo\phase-1-cli\.python-version
  - **Acceptance Criteria**:
    - [ ] File contains "3.10" (or appropriate patch version)
    - [ ] pyenv recognizes the version
  - **Complexity**: S (2 min)
  - **Time Estimate**: 2 minutes
  - **Dependencies**: T-001

- [X] T-004 Verify __init__.py files for all packages
  - **Description**: Ensure all __init__.py files exist with proper module docstrings
  - **Inputs**: Package structure from T-001
  - **Outputs**: 6 __init__.py files in src/, src/models/, src/services/, src/cli/, tests/unit/, tests/integration/
  - **Acceptance Criteria**:
    - [ ] Each __init__.py has appropriate docstring
    - [ ] All packages are importable
  - **Complexity**: S (3 min)
  - **Time Estimate**: 3 minutes
  - **Dependencies**: T-001

- [X] T-005 Create basic README placeholder
  - **Description**: Create README.md with installation instructions and usage overview from quickstart.md
  - **Inputs**: quickstart.md from contracts/ directory
  - **Outputs**: D:\Hackathons\Evolution-of-Todo\phase-1-cli\README.md
  - **Acceptance Criteria**:
    - [ ] README includes installation instructions
    - [ ] README includes basic usage examples
    - [ ] README references Python 3.10+ requirement
  - **Complexity**: S (5 min)
  - **Time Estimate**: 5 minutes
  - **Dependencies**: T-002, T-003
```

---

## Phase 2: Foundational Data Models

**Purpose**: Create core data structures used throughout the application
**Tasks**: 3
**Dependencies**: Phase 1 complete
**Parallelizable**: T-006 and T-007 can be done concurrently

```
- [X] T-006 [P] Implement Priority enum in src/models/enums.py
  - **Description**: Create Priority enum with HIGH, MEDIUM, LOW values inheriting from str
  - **Inputs**: data-model.md specification, Priority enum requirements
  - **Outputs**: D:\Hackathons\Evolution-of-Todo\phase-1-cli\src\models\enums.py
  - **Acceptance Criteria**:
    - [ ] Priority enum defined with str inheritance
    - [ ] Values: HIGH="High", MEDIUM="Medium", LOW="Low"
    - [ ] parse_priority() function for case-insensitive CLI input (accepts h/m/l shortcuts)
    - [ ] Full type hints for mypy --strict compliance
    - [ ] Docstrings for class and functions
  - **Complexity**: S (5 min)
  - **Time Estimate**: 5 minutes
  - **Dependencies**: T-004
  - **Quick Win**: Yes - simple enum definition

- [X] T-007 [P] Implement Status enum in src/models/enums.py
  - **Description**: Create Status enum with PENDING, COMPLETED values inheriting from str
  - **Inputs**: data-model.md specification, Status enum requirements
  - **Outputs**: D:\Hackathons\Evolution-of-Todo\phase-1-cli\src\models\enums.py (same file as Priority)
  - **Acceptance Criteria**:
    - [ ] Status enum defined with str inheritance
    - [ ] Values: PENDING="Pending", COMPLETED="Completed"
    - [ ] parse_status() function for case-insensitive CLI input (accepts p/c shortcuts)
    - [ ] Full type hints for mypy --strict compliance
    - [ ] Docstrings for class and functions
  - **Complexity**: S (5 min)
  - **Time Estimate**: 5 minutes
  - **Dependencies**: T-004
  - **Parallel With**: T-006 (can be done concurrently)

- [X] T-008 [P] Implement Todo dataclass in src/models/todo.py
  - **Description**: Create Todo dataclass with all 6 fields and full type hints
  - **Inputs**: data-model.md Todo specification, plan.md dataclass definition
  - **Outputs**: D:\Hackathons\Evolution-of-Todo\phase-1-cli\src\models\todo.py
  - **Acceptance Criteria**:
    - [ ] Todo dataclass with fields: id, title, description, priority, status, created_at
    - [ ] All fields have type hints
    - [ ] priority: Priority type with default Priority.MEDIUM
    - [ ] status: Status type with default Status.PENDING
    - [ ] created_at: datetime type
    - [ ] Docstring with class and attribute documentation
    - [ ] mypy --strict compliance
  - **Complexity**: S (8 min)
  - **Time Estimate**: 8 minutes
  - **Dependencies**: T-006, T-007

- [ ] T-008-A Verify Todo dataclass importable
  - **Description**: Quick verification that Todo dataclass can be imported correctly
  - **Inputs**: D:\Hackathons\Evolution-of-Todo\phase-1-cli\src\models\todo.py
  - **Outputs**: Python import verification output
  - **Acceptance Criteria**:
    - [ ] `from src.models.todo import Todo` succeeds
    - [ ] `from src.models.enums import Priority, Status` succeeds
    - [ ] Default values work: Todo(title="Test")
  - **Complexity**: S (2 min)
  - **Time Estimate**: 2 minutes
  - **Dependencies**: T-008
```

---

## Phase 3: TodoService Core

**Purpose**: Implement business logic layer with CRUD operations
**Tasks**: 9
**Dependencies**: Phase 2 complete
**Parallelizable**: T-010 through T-016 can run after T-009

```
- [X] T-009 [P] Implement TodoService.__init__() and state management
  - **Description**: Create TodoService class with _tasks list and _next_id counter
  - **Inputs**: plan.md service-layer architecture, data-model.md TodoService signatures
  - **Outputs**: D:\Hackathons\Evolution-of-Todo\phase-1-cli\src\services\todo_service.py
  - **Acceptance Criteria**:
    - [ ] TodoService class defined
    - [ ] __init__() initializes `self._tasks: List[Todo] = []` and `self._next_id: int = 1`
    - [ ] Type hints on all methods
    - [ ] Docstrings for class and methods
  - **Complexity**: S (5 min)
  - **Time Estimate**: 5 minutes
  - **Dependencies**: T-008
  - **Quick Win**: Yes - simple class setup

- [ ] T-009-A Verify TodoService instantiates correctly
  - **Description**: Quick test that TodoService can be instantiated
  - **Inputs**: D:\Hackathons\Evolution-of-Todo\phase-1-cli\src\services\todo_service.py
  - **Outputs**: Python verification output
  - **Acceptance Criteria**:
    - [ ] `from src.services.todo_service import TodoService` succeeds
    - [ ] `service = TodoService()` creates instance
    - [ ] `service._tasks` is empty list
    - [ ] `service._next_id` is 1
  - **Complexity**: S (2 min)
  - **Time Estimate**: 2 minutes
  - **Dependencies**: T-009

- [ ] T-010 [P] [US1] Implement TodoService.add_task() - validation logic
  - **Description**: Create add_task() method with title/description validation (no ID assignment yet)
  - **Inputs**: contracts/add.md service layer contract, FR-001, FR-013, FR-014 requirements
  - **Outputs**: Validation portion of add_task() in todo_service.py
  - **Acceptance Criteria**:
    - [ ] Validates title (1-200 chars, trimmed, non-empty after trim)
    - [ ] Validates description (0-1000 chars)
    - [ ] Returns (None, error_msg) on validation failure
    - [ ] Helper function: _validate_title(title: str) -> Optional[str]
    - [ ] Helper function: _validate_description(desc: str) -> Optional[str]
  - **Complexity**: S (10 min)
  - **Time Estimate**: 10 minutes
  - **Dependencies**: T-009

- [ ] T-010-A [P] [US1] Implement TodoService.add_task() - creation and ID assignment
  - **Description**: Complete add_task() with Todo creation and ID assignment
  - **Inputs**: FR-002, FR-003, FR-004, FR-005 requirements
  - **Outputs**: Full add_task() method in todo_service.py
  - **Acceptance Criteria**:
    - [ ] Signature: add_task(title: str, description: str = "", priority: Priority = Priority.MEDIUM) -> tuple[Optional[Todo], Optional[str]]
    - [ ] Assigns sequential ID starting from 1
    - [ ] Sets status to Status.PENDING
    - [ ] Sets created_at to datetime.utcnow()
    - [ ] Returns (Todo, None) on success, (None, error_msg) on failure
    - [ ] Integrates with T-010 validation
  - **Complexity**: M (15 min)
  - **Time Estimate**: 15 minutes
  - **Dependencies**: T-010

- [ ] T-010-B [US1] Verify add_task() basic scenarios
  - **Description**: Quick test of add_task() success and error paths
  - **Inputs**: T-010 implementation
  - **Outputs**: Test output showing success and error cases
  - **Acceptance Criteria**:
    - [ ] Adding valid task returns (Todo, None)
    - [ ] Adding empty title returns (None, error_msg)
    - [ ] Adding 201-char title returns (None, error_msg)
    - [ ] Task ID increments correctly (1, 2, 3...)
    - [ ] Default priority is MEDIUM
    - [ ] Default status is PENDING
  - **Complexity**: S (5 min)
  - **Time Estimate**: 5 minutes
  - **Dependencies**: T-010-A

- [ ] T-011 [P] [US1] Implement TodoService.get_task(), list_tasks(), filter_by_status()
  - **Description**: Create read methods for retrieving tasks with status filtering
  - **Inputs**: contracts/list.md service layer contract, FR-006 requirements
  - **Outputs**: get_task(), list_tasks(), and filter_by_status() methods in todo_service.py
  - **Acceptance Criteria**:
    - [ ] get_task(task_id: int) -> Optional[Todo]: Returns None if not found
    - [ ] list_tasks() -> List[Todo]: Returns all tasks in creation order
    - [ ] filter_by_status(status: Status) -> List[Todo]: Returns tasks matching status
    - [ ] Type hints on all methods
    - [ ] Docstrings for methods
  - **Complexity**: S (8 min)
  - **Time Estimate**: 8 minutes
  - **Dependencies**: T-009

- [ ] T-011-A [US1] Verify read methods
  - **Description**: Quick test of get_task, list_tasks, filter_by_status
  - **Inputs**: T-011 implementation
  - **Outputs**: Test output showing read method behavior
  - **Acceptance Criteria**:
    - [ ] get_task(1) returns None for empty list
    - [ ] list_tasks() returns empty list for empty list
    - [ ] After adding tasks, get_task returns correct task
    - [ ] filter_by_status returns only matching status
  - **Complexity**: S (3 min)
  - **Time Estimate**: 3 minutes
  - **Dependencies**: T-011

- [ ] T-012 [P] [US2] Implement TodoService.update_task() - validation
  - **Description**: Create update_task() method with field validation
  - **Inputs**: contracts/update.md service layer contract, FR-007, FR-010 requirements
  - **Outputs**: Validation portion of update_task() in todo_service.py
  - **Acceptance Criteria**:
    - [ ] Validates task exists (returns error if not found)
    - [ ] Validates title/description if provided using T-010 validators
    - [ ] Returns (None, error_msg) for validation failures
  - **Complexity**: S (8 min)
  - **Time Estimate**: 8 minutes
  - **Dependencies**: T-009, T-010

- [ ] T-012-A [P] [US2] Implement TodoService.update_task() - field updates
  - **Description**: Complete update_task() with partial update support
  - **Inputs**: FR-007 requirements for partial updates
  - **Outputs**: Full update_task() method in todo_service.py
  - **Acceptance Criteria**:
    - [ ] Signature: update_task(task_id: int, title: Optional[str] = None, description: Optional[str] = None, priority: Optional[Priority] = None) -> tuple[Optional[Todo], Optional[str]]
    - [ ] Updates only specified fields (partial update support)
    - [ ] Preserves ID, status, created_at (immutable fields)
    - [ ] Returns (updated_todo, None) on success, (None, error_msg) on failure
  - **Complexity**: M (12 min)
  - **Time Estimate**: 12 minutes
  - **Dependencies**: T-012

- [ ] T-013 [P] [US2] Implement TodoService.delete_task() method
  - **Description**: Create delete_task() method for removing tasks
  - **Inputs**: contracts/delete.md service layer contract, FR-008 requirements
  - **Outputs**: delete_task() method in todo_service.py
  - **Acceptance Criteria**:
    - [ ] Signature: delete_task(task_id: int) -> tuple[Optional[Todo], Optional[str]]
    - [ ] Validates task exists (returns error if not found)
    - [ ] Removes task from _tasks list
    - [ ] Returns deleted Todo for confirmation
    - [ ] Does NOT decrement _next_id (IDs never reused)
  - **Complexity**: S (5 min)
  - **Time Estimate**: 5 minutes
  - **Dependencies**: T-009

- [ ] T-014 [P] [US3] Implement TodoService.complete_task() method
  - **Description**: Create complete_task() method for marking tasks complete
  - **Inputs**: contracts/complete.md service layer contract, FR-009 requirements
  - **Outputs**: complete_task() method in todo_service.py
  - **Acceptance Criteria**:
    - [ ] Signature: complete_task(task_id: int) -> tuple[Optional[Todo], Optional[str]]
    - [ ] Validates task exists (returns error if not found)
    - [ ] Sets status to Status.COMPLETED
    - [ ] Idempotent: works on already-completed tasks without error
    - [ ] Preserves all other fields
  - **Complexity**: S (5 min)
  - **Time Estimate**: 5 minutes
  - **Dependencies**: T-009

- [ ] T-015 [P] [US4] Implement TodoService.filter_by_priority() method
  - **Description**: Create filter_by_priority() method for priority filtering
  - **Inputs**: contracts/filter.md service layer contract, FR-011 requirements
  - **Outputs**: filter_by_priority() method in todo_service.py
  - **Acceptance Criteria**:
    - [ ] Signature: filter_by_priority(priority: Priority) -> List[Todo]
    - [ ] Returns tasks matching priority regardless of status
    - [ ] Returns empty list if no matches
    - [ ] Preserves creation order
  - **Complexity**: S (5 min)
  - **Time Estimate**: 5 minutes
  - **Dependencies**: T-009

- [ ] T-016 [P] [US5] Implement TodoService.search_tasks() - case-insensitive matching
  - **Description**: Create search_tasks() method with case-insensitive keyword matching
  - **Inputs**: contracts/search.md service layer contract, FR-012 requirements
  - **Outputs**: search_tasks() method in todo_service.py
  - **Acceptance Criteria**:
    - [ ] Signature: search_tasks(keyword: str) -> List[Todo]
    - [ ] Case-insensitive substring matching
    - [ ] Searches both title and description
    - [ ] Returns unique tasks (no duplicates)
    - [ ] Returns empty list if no matches
    - [ ] Handles empty/whitespace-only keywords (returns empty list)
  - **Complexity**: M (15 min)
  - **Time Estimate**: 15 minutes
  - **Dependencies**: T-009

- [ ] T-016-A [US5] Verify search_tasks() behavior
  - **Description**: Quick test of search_tasks edge cases
  - **Inputs**: T-016 implementation
  - **Outputs**: Test output showing search behavior
  - **Acceptance Criteria**:
    - [ ] Empty keyword returns empty list
    - [ ] Whitespace-only keyword returns empty list
    - [ ] Matching title returns task
    - [ ] Matching description returns task
    - [ ] Case-insensitive matching works
    - [ ] No duplicates when keyword matches both title and description
  - **Complexity**: S (3 min)
  - **Time Estimate**: 3 minutes
  - **Dependencies**: T-016
```

---

## Phase 4: CLI Commands - Add and List

**Purpose**: Implement CLI commands for User Story 1 (Add and View Tasks)
**Tasks**: 6
**Dependencies**: Phase 3 complete
**Parallelizable**: T-017-A and T-018-A can run concurrently

```
- [ ] T-017 [P] [US1] Implement CLI argument parser - add command
  - **Description**: Create argparse configuration for add subcommand
  - **Inputs**: contracts/add.md CLI handler specification
  - **Outputs**: ArgumentParser configuration in D:\Hackathons\Evolution-of-Todo\phase-1-cli\src\cli\main.py
  - **Acceptance Criteria**:
    - [ ] ArgumentParser configured for "todo" command
    - [ ] add subcommand with title positional arg
    - [ ] --description/-d option for description
    - [ ] --priority/-p option for priority
    - [ ] Priority shortcuts: 'h'/'H' = High, 'm'/'M' = Medium, 'l'/'L' = Low
  - **Complexity**: S (8 min)
  - **Time Estimate**: 8 minutes
  - **Dependencies**: T-010-A

- [ ] T-017-A [P] [US1] Implement add command handler - success path
  - **Description**: Create handle_add() function for success cases
  - **Inputs**: contracts/add.md success output specification
  - **Outputs**: handle_add() function in main.py
  - **Acceptance Criteria**:
    - [ ] handle_add() parses priority case-insensitively
    - [ ] Calls TodoService.add_task()
    - [ ] Displays success output with all task fields
    - [ ] Exit code 0 for success
  - **Complexity**: S (8 min)
  - **Time Estimate**: 8 minutes
  - **Dependencies**: T-017

- [ ] T-017-B [P] [US1] Implement add command handler - error path
  - **Description**: Create handle_add() error handling
  - **Inputs**: contracts/add.md error output specification
  - **Outputs**: Error handling in handle_add()
  - **Acceptance Criteria**:
    - [ ] Displays error messages for validation failures
    - [ ] Error: "Title cannot be empty" for empty title
    - [ ] Error: "Title cannot exceed 200 characters"
    - [ ] Error: "Description cannot exceed 1000 characters"
    - [ ] Error: "Invalid priority level. Use high, medium, or low"
    - [ ] Exit code 1 for errors
  - **Complexity**: S (5 min)
  - **Time Estimate**: 5 minutes
  - **Dependencies**: T-017-A

- [ ] T-017-C [US1] Integration test - add command
  - **Description**: End-to-end test of add command
  - **Inputs**: T-017-B implementation
  - **Outputs**: CLI test execution
  - **Acceptance Criteria**:
    - [ ] `todo add "Buy groceries"` shows success output
    - [ ] `todo add "Buy groceries" -d "Milk, eggs"` works
    - [ ] `todo add ""` shows error
    - [ ] Task appears in list output
  - **Complexity**: S (5 min)
  - **Time Estimate**: 5 minutes
  - **Dependencies**: T-017-B, T-020

- [ ] T-018 [P] [US1] Implement list command - argument parser
  - **Description**: Create list subcommand with status filtering options
  - **Inputs**: contracts/list.md CLI handler specification
  - **Outputs**: list subcommand in ArgumentParser
  - **Acceptance Criteria**:
    - [ ] list subcommand with --status/-s option
    - [ ] Status choices: pending/completed/all
    - [ ] Default: all
  - **Complexity**: S (5 min)
  - **Time Estimate**: 5 minutes
  - **Dependencies**: T-011

- [ ] T-018-A [P] [US1] Implement list command handler
  - **Description**: Create handle_list() function with table output
  - **Inputs**: contracts/list.md output format specification
  - **Outputs**: handle_list() function in main.py
  - **Acceptance Criteria**:
    - [ ] handle_list() parses status filter case-insensitively
    - [ ] Calls appropriate TodoService method (list_tasks or filter_by_status)
    - [ ] Displays ASCII table with headers
    - [ ] Handles empty list with "No tasks found."
    - [ ] Truncates long titles/descriptions to 20 chars
  - **Complexity**: M (15 min)
  - **Time Estimate**: 15 minutes
  - **Dependencies**: T-018

- [ ] T-018-B [US1] Integration test - list command
  - **Description**: End-to-end test of list command
  - **Inputs**: T-018-A implementation
  - **Outputs**: CLI test execution
  - **Acceptance Criteria**:
    - [ ] `todo list` shows all tasks
    - [ ] `todo list --status pending` shows only pending
    - [ ] `todo list --status completed` shows only completed
    - [ ] Empty list shows "No tasks found."
  - **Complexity**: S (3 min)
  - **Time Estimate**: 3 minutes
  - **Dependencies**: T-018-A

- [ ] T-019 [US1] Create src/cli/__init__.py exports
  - **Description**: Create src/cli/__init__.py with proper exports
  - **Inputs**: CLI module structure
  - **Outputs**: D:\Hackathons\Evolution-of-Todo\phase-1-cli\src\cli\__init__.py
  - **Acceptance Criteria**:
    - [ ] __init__.py exports main entry point
    - [ ] Supports `python -m src.cli.main` execution
  - **Complexity**: S (2 min)
  - **Time Estimate**: 2 minutes
  - **Dependencies**: T-017

- [ ] T-020 [US1] Create src/services/__init__.py exports
  - **Description**: Create src/services/__init__.py with TodoService export
  - **Inputs**: Service module structure
  - **Outputs**: D:\Hackathons\Evolution-of-Todo\phase-1-cli\src\services\__init__.py
  - **Acceptance Criteria**:
    - [ ] __init__.py exports TodoService
    - [ ] Supports clean imports: `from src.services.todo_service import TodoService`
  - **Complexity**: S (2 min)
  - **Time Estimate**: 2 minutes
  - **Dependencies**: T-009
```

---

## Phase 5: CLI Commands - Update and Delete

**Purpose**: Implement CLI commands for User Story 2 (Update and Delete Tasks)
**Tasks**: 4
**Dependencies**: Phase 4 complete
**Parallelizable**: T-021 and T-022 can run concurrently after T-012

```
- [ ] T-021 [P] [US2] Implement update command - argument parser
  - **Description**: Create update subcommand with ID and field options
  - **Inputs**: contracts/update.md CLI handler specification
  - **Outputs**: update subcommand in ArgumentParser
  - **Acceptance Criteria**:
    - [ ] update subcommand with id positional argument
    - [ ] --title/-t, --description/-d, --priority/-p options
  - **Complexity**: S (5 min)
  - **Time Estimate**: 5 minutes
  - **Dependencies**: T-012-A

- [ ] T-021-A [P] [US2] Implement update command handler
  - **Description**: Create handle_update() function
  - **Inputs**: contracts/update.md output specification
  - **Outputs**: handle_update() function in main.py
  - **Acceptance Criteria**:
    - [ ] Validates task ID (positive integer)
    - [ ] Requires at least one field to update
    - [ ] Parses priority case-insensitively
    - [ ] Calls TodoService.update_task()
    - [ ] Displays success output with all task fields
    - [ ] Displays error messages for validation failures or not found
  - **Complexity**: M (12 min)
  - **Time Estimate**: 12 minutes
  - **Dependencies**: T-021

- [ ] T-021-B [US2] Integration test - update command
  - **Description**: End-to-end test of update command
  - **Inputs**: T-021-A implementation
  - **Outputs**: CLI test execution
  - **Acceptance Criteria**:
    - [ ] `todo update 1 --title "New title"` updates title
    - [ ] `todo update 1 -p high` updates priority
    - [ ] `todo update 999` shows "Task not found"
    - [ ] `todo update 1` (no fields) shows error
  - **Complexity**: S (3 min)
  - **Time Estimate**: 3 minutes
  - **Dependencies**: T-021-A

- [ ] T-022 [P] [US2] Implement delete command handler
  - **Description**: Create delete subcommand and handle_delete() function
  - **Inputs**: contracts/delete.md CLI handler specification
  - **Outputs**: delete command implementation in main.py
  - **Acceptance Criteria**:
    - [ ] delete subcommand with id positional argument
    - [ ] handle_delete() validates task ID (positive integer)
    - [ ] handle_delete() calls TodoService.delete_task()
    - [ ] Displays success output with ID and title
    - [ ] Displays error messages for not found or invalid ID
  - **Complexity**: S (8 min)
  - **Time Estimate**: 8 minutes
  - **Dependencies**: T-013

- [ ] T-022-A [US2] Integration test - delete command
  - **Description**: End-to-end test of delete command
  - **Inputs**: T-022 implementation
  - **Outputs**: CLI test execution
  - **Acceptance Criteria**:
    - [ ] `todo delete 1` removes task and shows success
    - [ ] `todo delete 999` shows "Task not found"
    - [ ] Deleted task no longer appears in list
  - **Complexity**: S (3 min)
  - **Time Estimate**: 3 minutes
  - **Dependencies**: T-022
```

---

## Phase 6: CLI Commands - Complete

**Purpose**: Implement CLI command for User Story 3 (Mark Tasks Complete)
**Tasks**: 2
**Dependencies**: Phase 5 complete

```
- [ ] T-023 [P] [US3] Implement complete command - argument parser and handler
  - **Description**: Create complete subcommand and handle_complete() function
  - **Inputs**: contracts/complete.md CLI handler specification
  - **Outputs**: complete command implementation in main.py
  - **Acceptance Criteria**:
    - [ ] complete subcommand with id positional argument
    - [ ] handle_complete() validates task ID (positive integer)
    - [ ] handle_complete() calls TodoService.complete_task()
    - [ ] Displays success output with ID, title, and new status
    - [ ] Idempotent: works on already-completed tasks without error
    - [ ] Displays error messages for not found or invalid ID
  - **Complexity**: S (8 min)
  - **Time Estimate**: 8 minutes
  - **Dependencies**: T-014

- [ ] T-023-A [US3] Integration test - complete command
  - **Description**: End-to-end test of complete command
  - **Inputs**: T-023 implementation
  - **Outputs**: CLI test execution
  - **Acceptance Criteria**:
    - [ ] `todo complete 1` marks task complete
    - [ ] `todo complete 1` again succeeds (idempotent)
    - [ ] Completed task shows "Completed" status in list
    - [ ] `todo complete 999` shows "Task not found"
  - **Complexity**: S (3 min)
  - **Time Estimate**: 3 minutes
  - **Dependencies**: T-023
```

---

## Phase 7: CLI Commands - Filter

**Purpose**: Implement CLI command for User Story 4 (Filter Tasks by Priority)
**Tasks**: 2
**Dependencies**: Phase 6 complete

```
- [ ] T-024 [P] [US4] Implement filter command - argument parser and handler
  - **Description**: Create filter subcommand and handle_filter() function
  - **Inputs**: contracts/filter.md CLI handler specification
  - **Outputs**: filter command implementation in main.py
  - **Acceptance Criteria**:
    - [ ] filter subcommand with priority positional argument
    - [ ] handle_filter() parses priority case-insensitively (accepts h/m/l)
    - [ ] handle_filter() calls TodoService.filter_by_priority()
    - [ ] Displays ASCII table with matching tasks
    - [ ] Shows "No tasks found with priority: X" for empty results
    - [ ] Displays error for invalid priority value
  - **Complexity**: S (10 min)
  - **Time Estimate**: 10 minutes
  - **Dependencies**: T-015

- [ ] T-024-A [US4] Integration test - filter command
  - **Description**: End-to-end test of filter command
  - **Inputs**: T-024 implementation
  - **Outputs**: CLI test execution
  - **Acceptance Criteria**:
    - [ ] `todo filter high` shows only high priority tasks
    - [ ] `todo filter medium` shows only medium priority tasks
    - [ ] `todo filter low` shows only low priority tasks
    - [ ] Empty result shows "No tasks found with priority: X"
    - [ ] Invalid priority shows error
  - **Complexity**: S (3 min)
  - **Time Estimate**: 3 minutes
  - **Dependencies**: T-024
```

---

## Phase 8: CLI Commands - Search

**Purpose**: Implement CLI command for User Story 5 (Search Tasks by Keyword)
**Tasks**: 2
**Dependencies**: Phase 7 complete

```
- [ ] T-025 [P] [US5] Implement search command - argument parser
  - **Description**: Create search subcommand with keyword argument
  - **Inputs**: contracts/search.md CLI handler specification
  - **Outputs**: search subcommand in ArgumentParser
  - **Acceptance Criteria**:
    - [ ] search subcommand with keyword positional argument
  - **Complexity**: S (3 min)
  - **Time Estimate**: 3 minutes
  - **Dependencies**: T-016

- [ ] T-025-A [P] [US5] Implement search command handler
  - **Description**: Create handle_search() function
  - **Inputs**: contracts/search.md output specification
  - **Outputs**: handle_search() function in main.py
  - **Acceptance Criteria**:
    - [ ] handle_search() calls TodoService.search_tasks() with keyword
    - [ ] Displays ASCII table with matching tasks
    - [ ] Shows "No tasks found matching: X" for empty results
    - [ ] Case-insensitive substring matching
    - [ ] Searches both title and description
  - **Complexity**: M (12 min)
  - **Time Estimate**: 12 minutes
  - **Dependencies**: T-025

- [ ] T-025-B [US5] Integration test - search command
  - **Description**: End-to-end test of search command
  - **Inputs**: T-025-A implementation
  - **Outputs**: CLI test execution
  - **Acceptance Criteria**:
    - [ ] `todo search groceries` finds tasks with "groceries" in title
    - [ ] `todo search milk` finds tasks with "milk" in description
    - [ ] `todo search nonexistent` shows "No tasks found matching"
    - [ ] Case-insensitive search works (GROCERIES finds groceries)
  - **Complexity**: S (3 min)
  - **Time Estimate**: 3 minutes
  - **Dependencies**: T-025-A
```

---

## Phase 9: Integration and Verification

**Purpose**: Final integration testing and documentation
**Tasks**: 4
**Dependencies**: Phase 8 complete (or partial for MVP)

```
- [ ] T-026 Update README.md with complete usage documentation
  - **Description**: Update README.md with all command examples and installation instructions
  - **Inputs**: quickstart.md, all CLI contracts
  - **Outputs**: D:\Hackathons\Evolution-of-Todo\phase-1-cli\README.md
  - **Acceptance Criteria**:
    - [ ] Installation section with UV setup
    - [ ] Usage section with all 7 command examples
    - [ ] Command reference table
    - [ ] Exit code documentation
  - **Complexity**: S (10 min)
  - **Time Estimate**: 10 minutes
  - **Dependencies**: T-017-B, T-018-A, T-021-A, T-022, T-023, T-024, T-025-A

- [ ] T-027 Run mypy type checking
  - **Description**: Verify all code passes mypy --strict
  - **Inputs**: All source files
  - **Outputs**: mypy output with 0 errors
  - **Acceptance Criteria**:
    - [ ] mypy src/ --strict passes with 0 errors
    - [ ] All type hints are correct and complete
  - **Complexity**: S (5 min)
  - **Time Estimate**: 5 minutes
  - **Dependencies**: T-001 through T-025

- [ ] T-028 [P] Full user story verification
  - **Description**: Run complete end-to-end tests for all user story acceptance criteria
  - **Inputs**: spec.md user story scenarios
  - **Outputs**: Verification evidence and PHR documentation
  - **Acceptance Criteria**:
    - [ ] User Story 1: Add task, view list, empty list scenarios
    - [ ] User Story 2: Update task, delete task, error handling scenarios
    - [ ] User Story 3: Complete task, idempotent completion scenarios
    - [ ] User Story 4: Filter by priority scenarios
    - [ ] User Story 5: Search by keyword scenarios
    - [ ] All exit codes correct (0 success, 1 errors)
    - [ ] Verify no business logic imports in cli/main.py (only imports from services, models)
    - [ ] Document thread-safety: Phase I is single-user CLI, no thread-safety guarantees required
  - **Complexity**: M (20 min)
  - **Time Estimate**: 20 minutes
  - **Dependencies**: T-026, T-027

- [ ] T-029 [P] Final cleanup and validation
  - **Description**: Final validation and cleanup
  - **Inputs**: All implementation files
  - **Outputs**: Clean project ready for PR
  - **Acceptance Criteria**:
    - [ ] All __init__.py files have proper docstrings
    - [ ] All public classes/functions have docstrings
    - [ ] No debug/print statements left in code
    - [ ] Code follows PEP 8 style guidelines
    - [ ] Project is ready for PR against main branch
  - **Complexity**: S (10 min)
  - **Time Estimate**: 10 minutes
  - **Dependencies**: T-028
```

---

## User Story Task Summary

| User Story | Tasks | Description |
|------------|-------|-------------|
| US1: Add and View | T-010, T-010-A, T-010-B, T-011, T-011-A, T-017, T-017-A, T-017-B, T-017-C, T-018, T-018-A, T-018-B, T-019, T-020 | Add tasks, list tasks with filtering |
| US2: Update and Delete | T-012, T-012-A, T-013, T-021, T-021-A, T-021-B, T-022, T-022-A | Update task details, delete tasks |
| US3: Mark Complete | T-014, T-023, T-023-A | Mark tasks as complete |
| US4: Filter by Priority | T-015, T-024, T-024-A | Filter tasks by priority level |
| US5: Search by Keyword | T-016, T-016-A, T-025, T-025-A, T-025-B | Search tasks by keyword |

---

## Dependency Graph (Visual)

```
Phase 1 (Setup)
    |
    +-- T-001 (Quick Win)
    |       |
    |       +-- T-002 --> T-005
    |       +-- T-003 --> T-005
    |       +-- T-004 --> T-006, T-007
    |
    +-- T-005 --> (Phase 2 starts)

Phase 2 (Foundational Models)
    |
    +-- T-006 (Quick Win) ----+
    +-- T-007 (Parallel) -----+--> T-008 --> T-008-A --> (Phase 3 starts)

Phase 3 (TodoService Core)
    |
    +-- T-009 (Quick Win) --> T-009-A
    |       |
    |       +-- T-010 --> T-010-A --> T-010-B
    |       +-- T-011 --> T-011-A
    |       +-- T-012 --> T-012-A
    |       +-- T-013
    |       +-- T-014
    |       +-- T-015
    |       +-- T-016 --> T-016-A
    |
    +-- T-020 (services __init__.py)
            |
            +-- (Phase 4 starts)

Phase 4 (CLI - Add/List) - PARALLELIZABLE
    |
    +-- T-017 --> T-017-A --> T-017-B --> T-017-C
    +-- T-018 --> T-018-A --> T-018-B
    +-- T-019
    +-- T-020 (already done)

Phase 5 (CLI - Update/Delete) - CAN RUN IN PARALLEL
    |
    +-- T-021 --> T-021-A --> T-021-B
    +-- T-022 --> T-022-A

Phase 6 (CLI - Complete)
    |
    +-- T-023 --> T-023-A

Phase 7 (CLI - Filter)
    |
    +-- T-024 --> T-024-A

Phase 8 (CLI - Search)
    |
    +-- T-025 --> T-025-A --> T-025-B

Phase 9 (Integration)
    |
    +-- T-026 (README update)
    +-- T-027 (mypy check)
    |
    +-- T-028 (Full verification)
    +-- T-029 (Cleanup)
```

---

## Parallel Execution Opportunities

The following tasks can be executed in parallel for faster completion:

1. **T-006 and T-007**: Priority and Status enums can be implemented concurrently (both are simple enum definitions)

2. **T-010 through T-016**: All TodoService methods can be implemented in parallel after T-009-A is complete (they all depend only on service initialization)

3. **T-017 and T-018**: Add and list command parsers can be implemented concurrently

4. **T-017-A and T-018-A**: Add and list command handlers can be implemented concurrently

5. **T-021 and T-022**: Update and delete commands can be implemented concurrently

6. **T-021-A and T-022**: Update handler and delete command can run in parallel

7. **T-019 and T-020**: Both __init__.py files can be created concurrently

**Recommended Parallel Workflow**:
- Phase 1: Sequential (T-001 creates structure)
- Phase 2: Parallel T-006 + T-007, then T-008
- Phase 3: Parallel all methods after T-009-A
- Phase 4: Parallel T-017 and T-018
- Phase 5: Parallel T-021 and T-022
- Phase 6-8: Sequential (each depends on previous CLI work)

---

## Complexity Distribution

| Complexity | Tasks | Time Range | Description |
|------------|-------|------------|-------------|
| **S** (Small) | 30 tasks | 2-10 min each | Simple, straightforward implementation |
| **M** (Medium) | 10 tasks | 12-20 min | Requires validation logic or integration |
| **L** (Large) | 2 tasks | 20-30 min | Complex verification or full user story |

**Distribution**: 30 Small (71%), 10 Medium (24%), 2 Large (5%)

**Total Estimated Time**: ~3-4 hours of focused work

---

## Acceptance Criteria Checklist

Before marking any task complete, verify:

- [ ] Code follows the exact file path specified
- [ ] Type hints are complete (mypy --strict compliant)
- [ ] Docstrings are present for all public classes and functions
- [ ] Error handling matches contract specifications
- [ ] Exit codes are correct (0 for success, 1 for errors)
- [ ] Integration tests pass against the specification (for -A and -C tasks)
- [ ] No business logic in CLI layer (only argument parsing and output formatting)
- [ ] TodoService methods are synchronous (no async/await)
- [ ] Service layer can be imported and used independently of CLI

---

## Quick Start Guide

### Day 1: MVP (2 hours)

1. **Hour 1**: T-001 through T-010-A (Setup + Add task)
2. **Hour 2**: T-017 through T-017-B (CLI add command) + T-020 (services init)

**Validate**: `python -m src.cli.main add "Hello World"` works!

### Day 2: List and Read (1 hour)

3. T-011, T-011-A (Read methods)
4. T-018, T-018-A, T-018-B (List command)

**Validate**: `python -m src.cli.main list` shows your task!

### Day 3-4: Remaining Features (1-2 hours)

5. T-012, T-012-A, T-021, T-021-A (Update)
6. T-013, T-022 (Delete)
7. T-014, T-023 (Complete)
8. T-015, T-024 (Filter)
9. T-016, T-025, T-025-A (Search)

### Day 5: Integration (1 hour)

10. T-026, T-027, T-028, T-029 (Final verification)

---

## Next Steps

After all tasks complete:

1. Create a PR against the main branch
2. Include task IDs in commit messages (e.g., `feat: T-010 Implement TodoService.add_task()`)
3. Link PR to this tasks.md document
4. Run final integration verification (T-028)
5. Document verification evidence in PHR

---

*Generated by Spec-Kit Plus /sp.tasks command*
*Enhanced for better atomicity, embedded testing, and MVP scope identification*
