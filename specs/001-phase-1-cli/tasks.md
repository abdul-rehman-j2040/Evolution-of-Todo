# Task Breakdown: Phase 1 - Professional In-Memory Python Todo CLI

**Feature Branch**: `001-phase-1-cli`
**Generated**: 2026-01-01
**Spec Reference**: [spec.md](./spec.md)
**Plan Reference**: [plan.md](./plan.md)

---

## Executive Summary

This document defines the atomic, testable tasks for implementing Phase 1 of the Evolution of Todo CLI. Tasks are organized into phases with clear dependencies, acceptance criteria, and complexity estimates.

**Total Tasks**: 28
**Estimated Total Effort**: M (Medium)
**Critical Path**: Setup → Models → Service → CLI Commands

---

## Task Naming Convention

- **T-XXX**: Task identifier for commit messages and tracking
- **[P]**: Priority marker for task ordering
- **[US#]**: User Story reference (US1-US5)
- **Exact file paths**: All file paths are absolute and precise

---

## Phase 1: Project Setup

**Purpose**: Establish project structure and configuration
**Tasks**: 5
**Dependencies**: None (can start immediately)

```
- [ ] T-001 Create project directory structure per implementation plan
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
    - All 6 directories created with __init__.py files
    - Directory structure matches plan.md specification
    - Python recognizes packages (can import src)
  - **Complexity**: S
  - **Dependencies**: None

- [ ] T-002 Create pyproject.toml with UV configuration
  - **Description**: Create pyproject.toml with project metadata, Python version, and UV tool configuration per plan.md
  - **Inputs**: Python 3.10+ requirement, standard library only constraint
  - **Outputs**: D:\Hackathons\Evolution-of-Todo\phase-1-cli\pyproject.toml
  - **Acceptance Criteria**:
    - pyproject.toml includes [project] section with name, version, description
    - Python requirement set to >=3.10
    - [tool.uv] section configured for UV package manager
    - mypy configuration for --strict compliance
    - pytest as optional dev dependency
  - **Complexity**: S
  - **Dependencies**: T-001

- [ ] T-003 Create .python-version file
  - **Description**: Create .python-version file specifying Python 3.10
  - **Inputs**: Python 3.10+ requirement from spec.md
  - **Outputs**: D:\Hackathons\Evolution-of-Todo\phase-1-cli\.python-version
  - **Acceptance Criteria**:
    - File contains "3.10" (or appropriate patch version)
    - pyenv recognizes the version
  - **Complexity**: S
  - **Dependencies**: T-001

- [ ] T-004 Create __init__.py files for all packages
  - **Description**: Ensure all __init__.py files exist with proper module docstrings
  - **Inputs**: Package structure from T-001
  - **Outputs**: 6 __init__.py files in src/, src/models/, src/services/, src/cli/, tests/unit/, tests/integration/
  - **Acceptance Criteria**:
    - Each __init__.py has appropriate docstring
    - All packages are importable
  - **Complexity**: S
  - **Dependencies**: T-001

- [ ] T-005 [P] Create basic configuration and README placeholder
  - **Description**: Create README.md with installation instructions and usage overview from quickstart.md
  - **Inputs**: quickstart.md from contracts/ directory
  - **Outputs**: D:\Hackathons\Evolution-of-Todo\phase-1-cli\README.md
  - **Acceptance Criteria**:
    - README includes installation instructions
    - README includes basic usage examples
    - README references Python 3.10+ requirement
  - **Complexity**: S
  - **Dependencies**: T-002, T-003
```

---

## Phase 2: Foundational Data Models

**Purpose**: Create core data structures used throughout the application
**Tasks**: 3
**Dependencies**: Phase 1 complete

```
- [ ] T-006 [P] Implement Priority enum in src/models/enums.py
  - **Description**: Create Priority enum with HIGH, MEDIUM, LOW values inheriting from str
  - **Inputs**: data-model.md specification, Priority enum requirements
  - **Outputs**: D:\Hackathons\Evolution-of-Todo\phase-1-cli\src\models\enums.py
  - **Acceptance Criteria**:
    - Priority enum defined with str inheritance
    - Values: HIGH="High", MEDIUM="Medium", LOW="Low"
    - parse_priority() function for case-insensitive CLI input (accepts h/m/l shortcuts)
    - Full type hints for mypy --strict compliance
    - Docstrings for class and functions
  - **Complexity**: S
  - **Dependencies**: T-004

- [ ] T-007 [P] Implement Status enum in src/models/enums.py
  - **Description**: Create Status enum with PENDING, COMPLETED values inheriting from str
  - **Inputs**: data-model.md specification, Status enum requirements
  - **Outputs**: D:\Hackathons\Evolution-of-Todo\phase-1-cli\src\models\enums.py (same file as Priority)
  - **Acceptance Criteria**:
    - Status enum defined with str inheritance
    - Values: PENDING="Pending", COMPLETED="Completed"
    - parse_status() function for case-insensitive CLI input (accepts p/c shortcuts)
    - Full type hints for mypy --strict compliance
    - Docstrings for class and functions
  - **Complexity**: S
  - **Dependencies**: T-004

- [ ] T-008 [P] Implement Todo dataclass in src/models/todo.py
  - **Description**: Create Todo dataclass with all 6 fields and full type hints
  - **Inputs**: data-model.md Todo specification, plan.md dataclass definition
  - **Outputs**: D:\Hackathons\Evolution-of-Todo\phase-1-cli\src\models\todo.py
  - **Acceptance Criteria**:
    - Todo dataclass with fields: id, title, description, priority, status, created_at
    - All fields have type hints
    - priority: Priority type with default Priority.MEDIUM
    - status: Status type with default Status.PENDING
    - created_at: datetime type
    - Docstring with class and attribute documentation
    - mypy --strict compliance
  - **Complexity**: S
  - **Dependencies**: T-006, T-007
```

---

## Phase 3: TodoService Core

**Purpose**: Implement business logic layer with CRUD operations
**Tasks**: 7
**Dependencies**: Phase 2 complete

```
- [ ] T-009 [P] Implement TodoService.__init__() and state management
  - **Description**: Create TodoService class with _tasks list and _next_id counter
  - **Inputs**: plan.md service-layer architecture, data-model.md TodoService signatures
  - **Outputs**: D:\Hackathons\Evolution-of-Todo\phase-1-cli\src\services\todo_service.py
  - **Acceptance Criteria**:
    - TodoService class defined
    - __init__() initializes `self._tasks: List[Todo] = []` and `self._next_id: int = 1`
    - Type hints on all methods
    - Docstrings for class and methods
  - **Complexity**: S
  - **Dependencies**: T-008

- [ ] T-010 [P] [US1] Implement TodoService.add_task() method
  - **Description**: Create add_task() method with validation and ID assignment
  - **Inputs**: contracts/add.md service layer contract, FR-001 to FR-005 requirements
  - **Outputs**: add_task() method in todo_service.py
  - **Acceptance Criteria**:
    - Signature: add_task(title: str, description: str = "", priority: Priority = Priority.MEDIUM) -> tuple[Optional[Todo], Optional[str]]
    - Validates title (1-200 chars, trimmed, non-empty after trim)
    - Validates description (0-1000 chars)
    - Assigns sequential ID starting from 1
    - Sets status to Status.PENDING
    - Sets created_at to datetime.utcnow()
    - Returns (Todo, None) on success, (None, error_msg) on failure
  - **Complexity**: M
  - **Dependencies**: T-009

- [ ] T-011 [P] [US1] Implement TodoService.get_task(), list_tasks(), and filter_by_status() methods
  - **Description**: Create read methods for retrieving tasks with status filtering
  - **Inputs**: contracts/list.md service layer contract, FR-006 requirements
  - **Outputs**: get_task(), list_tasks(), and filter_by_status() methods in todo_service.py
  - **Acceptance Criteria**:
    - get_task(task_id: int) -> Optional[Todo]: Returns None if not found
    - list_tasks() -> List[Todo]: Returns all tasks in creation order
    - filter_by_status(status: Status) -> List[Todo]: Returns tasks matching status (all/pending/completed)
    - Type hints on all methods
    - Docstrings for methods
  - **Complexity**: S
  - **Dependencies**: T-009

- [ ] T-012 [P] [US2] Implement TodoService.update_task() method
  - **Description**: Create update_task() method for modifying task fields
  - **Inputs**: contracts/update.md service layer contract, FR-007, FR-010 requirements
  - **Outputs**: update_task() method in todo_service.py
  - **Acceptance Criteria**:
    - Signature: update_task(task_id: int, title: Optional[str] = None, description: Optional[str] = None, priority: Optional[Priority] = None) -> tuple[Optional[Todo], Optional[str]]
    - Validates task exists (returns error if not found)
    - Validates title/description if provided
    - Updates only specified fields (partial update support)
    - Preserves ID, status, created_at (immutable fields)
    - Returns (updated_todo, None) on success, (None, error_msg) on failure
  - **Complexity**: M
  - **Dependencies**: T-009

- [ ] T-013 [P] [US2] Implement TodoService.delete_task() method
  - **Description**: Create delete_task() method for removing tasks
  - **Inputs**: contracts/delete.md service layer contract, FR-008 requirements
  - **Outputs**: delete_task() method in todo_service.py
  - **Acceptance Criteria**:
    - Signature: delete_task(task_id: int) -> tuple[Optional[Todo], Optional[str]]
    - Validates task exists (returns error if not found)
    - Removes task from _tasks list
    - Returns deleted Todo for confirmation
    - Does NOT decrement _next_id (IDs never reused)
  - **Complexity**: S
  - **Dependencies**: T-009

- [ ] T-014 [P] [US3] Implement TodoService.complete_task() method
  - **Description**: Create complete_task() method for marking tasks complete
  - **Inputs**: contracts/complete.md service layer contract, FR-009 requirements
  - **Outputs**: complete_task() method in todo_service.py
  - **Acceptance Criteria**:
    - Signature: complete_task(task_id: int) -> tuple[Optional[Todo], Optional[str]]
    - Validates task exists (returns error if not found)
    - Sets status to Status.COMPLETED
    - Idempotent: works on already-completed tasks without error
    - Preserves all other fields
  - **Complexity**: S
  - **Dependencies**: T-009

- [ ] T-015 [P] [US4] Implement TodoService.filter_by_priority() method
  - **Description**: Create filter_by_priority() method for priority filtering
  - **Inputs**: contracts/filter.md service layer contract, FR-011 requirements
  - **Outputs**: filter_by_priority() method in todo_service.py
  - **Acceptance Criteria**:
    - Signature: filter_by_priority(priority: Priority) -> List[Todo]
    - Returns tasks matching priority regardless of status
    - Returns empty list if no matches
    - Preserves creation order
  - **Complexity**: S
  - **Dependencies**: T-009

- [ ] T-016 [P] [US5] Implement TodoService.search_tasks() method
  - **Description**: Create search_tasks() method for keyword search
  - **Inputs**: contracts/search.md service layer contract, FR-012 requirements
  - **Outputs**: search_tasks() method in todo_service.py
  - **Acceptance Criteria**:
    - Signature: search_tasks(keyword: str) -> List[Todo]
    - Case-insensitive substring matching
    - Searches both title and description
    - Returns unique tasks (no duplicates)
    - Returns empty list if no matches
    - Handles empty/whitespace-only keywords
  - **Complexity**: M
  - **Dependencies**: T-009
```

---

## Phase 4: CLI Commands - Add and List

**Purpose**: Implement CLI commands for User Story 1 (Add and View Tasks)
**Tasks**: 4
**Dependencies**: Phase 3 complete

```
- [ ] T-017 [P] [US1] Implement CLI argument parser and add command handler
  - **Description**: Create CLI main module with argparse and add command
  - **Inputs**: contracts/add.md CLI handler specification
  - **Outputs**: D:\Hackathons\Evolution-of-Todo\phase-1-cli\src\cli\main.py
  - **Acceptance Criteria**:
    - argparse.ArgumentParser configured for "todo" command
    - add subcommand with title positional arg, --description/-d and --priority/-p options
    - Priority shortcuts: 'h'/'H' = High, 'm'/'M' = Medium, 'l'/'L' = Low
    - handle_add() function that:
      - Parses priority case-insensitively (accepts full names and shortcuts)
      - Calls TodoService.add_task()
      - Displays success output with all task fields
      - Displays error messages for validation failures
      - Returns appropriate exit codes (0 for success, 1 for errors)
  - **Complexity**: M
  - **Dependencies**: T-010

- [ ] T-018 [P] [US1] Implement list command handler
  - **Description**: Create list command with status filtering
  - **Inputs**: contracts/list.md CLI handler specification
  - **Outputs**: list command implementation in main.py
  - **Acceptance Criteria**:
    - list subcommand with --status/-s option (pending/completed/all, default: all)
    - handle_list() function that:
      - Parses status filter case-insensitively
      - Calls appropriate TodoService method (list_tasks or filter_by_status)
      - Displays ASCII table with headers
      - Handles empty list with appropriate message
      - Truncates long titles/descriptions to 20 chars
  - **Complexity**: M
  - **Dependencies**: T-011

- [ ] T-019 [US1] Implement CLI __init__.py exports
  - **Description**: Create src/cli/__init__.py with proper exports
  - **Inputs**: CLI module structure
  - **Outputs**: D:\Hackathons\Evolution-of-Todo\phase-1-cli\src\cli\__init__.py
  - **Acceptance Criteria**:
    - __init__.py exports main entry point
    - Supports `python -m src.cli.main` execution
  - **Complexity**: S
  - **Dependencies**: T-017, T-018

- [ ] T-020 [US1] Implement services __init__.py exports
  - **Description**: Create src/services/__init__.py with TodoService export
  - **Inputs**: Service module structure
  - **Outputs**: D:\Hackathons\Evolution-of-Todo\phase-1-cli\src\services\__init__.py
  - **Acceptance Criteria**:
    - __init__.py exports TodoService
    - Supports clean imports: `from src.services.todo_service import TodoService`
  - **Complexity**: S
  - **Dependencies**: T-009
```

---

## Phase 5: CLI Commands - Update and Delete

**Purpose**: Implement CLI commands for User Story 2 (Update and Delete Tasks)
**Tasks**: 2
**Dependencies**: Phase 4 complete

```
- [ ] T-021 [P] [US2] Implement update command handler
  - **Description**: Create update command for modifying task fields
  - **Inputs**: contracts/update.md CLI handler specification
  - **Outputs**: update command implementation in main.py
  - **Acceptance Criteria**:
    - update subcommand with:
      - id positional argument
      - --title/-t, --description/-d, --priority/-p options
    - handle_update() function that:
      - Validates task ID (positive integer)
      - Requires at least one field to update
      - Parses priority case-insensitively
      - Calls TodoService.update_task()
      - Displays success output with all task fields
      - Displays error messages for validation failures or not found
  - **Complexity**: M
  - **Dependencies**: T-012

- [ ] T-022 [P] [US2] Implement delete command handler
  - **Description**: Create delete command for removing tasks
  - **Inputs**: contracts/delete.md CLI handler specification
  - **Outputs**: delete command implementation in main.py
  - **Acceptance Criteria**:
    - delete subcommand with id positional argument
    - handle_delete() function that:
      - Validates task ID (positive integer)
      - Calls TodoService.delete_task()
      - Displays success output with ID and title
      - Displays error messages for not found or invalid ID
  - **Complexity**: S
  - **Dependencies**: T-013
```

---

## Phase 6: CLI Commands - Complete

**Purpose**: Implement CLI command for User Story 3 (Mark Tasks Complete)
**Tasks**: 1
**Dependencies**: Phase 5 complete

```
- [ ] T-023 [P] [US3] Implement complete command handler
  - **Description**: Create complete command for marking tasks as done
  - **Inputs**: contracts/complete.md CLI handler specification
  - **Outputs**: complete command implementation in main.py
  - **Acceptance Criteria**:
    - complete subcommand with id positional argument
    - handle_complete() function that:
      - Validates task ID (positive integer)
      - Calls TodoService.complete_task()
      - Displays success output with ID, title, and new status
      - Idempotent: works on already-completed tasks without error
      - Displays error messages for not found or invalid ID
  - **Complexity**: S
  - **Dependencies**: T-014
```

---

## Phase 7: CLI Commands - Filter

**Purpose**: Implement CLI command for User Story 4 (Filter Tasks by Priority)
**Tasks**: 1
**Dependencies**: Phase 6 complete

```
- [ ] T-024 [P] [US4] Implement filter command handler
  - **Description**: Create filter command for priority-based filtering
  - **Inputs**: contracts/filter.md CLI handler specification
  - **Outputs**: filter command implementation in main.py
  - **Acceptance Criteria**:
    - filter subcommand with priority positional argument
    - handle_filter() function that:
      - Parses priority case-insensitively (accepts h/m/l)
      - Calls TodoService.filter_by_priority()
      - Displays ASCII table with matching tasks
      - Shows "No tasks found with priority: X" for empty results
      - Displays error for invalid priority value
  - **Complexity**: S
  - **Dependencies**: T-015
```

---

## Phase 8: CLI Commands - Search

**Purpose**: Implement CLI command for User Story 5 (Search Tasks by Keyword)
**Tasks**: 1
**Dependencies**: Phase 7 complete

```
- [ ] T-025 [P] [US5] Implement search command handler
  - **Description**: Create search command for keyword-based task search
  - **Inputs**: contracts/search.md CLI handler specification
  - **Outputs**: search command implementation in main.py
  - **Acceptance Criteria**:
    - search subcommand with keyword positional argument
    - handle_search() function that:
      - Calls TodoService.search_tasks() with keyword
      - Displays ASCII table with matching tasks
      - Shows "No tasks found matching: X" for empty results
      - Case-insensitive substring matching
      - Searches both title and description
  - **Complexity**: M
  - **Dependencies**: T-016
```

---

## Phase 9: Integration and Verification

**Purpose**: Final integration testing and documentation
**Tasks**: 3
**Dependencies**: Phase 8 complete

```
- [ ] T-026 Update README.md with complete usage documentation
  - **Description**: Update README.md with all command examples and installation instructions
  - **Inputs**: quickstart.md, all CLI contracts
  - **Outputs**: D:\Hackathons\Evolution-of-Todo\phase-1-cli\README.md
  - **Acceptance Criteria**:
    - Installation section with UV setup
    - Usage section with all 7 command examples
    - Command reference table
    - Exit code documentation
  - **Complexity**: S
  - **Dependencies**: T-017 through T-025

- [ ] T-027 Run mypy type checking
  - **Description**: Verify all code passes mypy --strict
  - **Inputs**: All source files
  - **Outputs**: mypy output with 0 errors
  - **Acceptance Criteria**:
    - mypy src/ --strict passes with 0 errors
    - All type hints are correct and complete
  - **Complexity**: S
  - **Dependencies**: T-001 through T-025

- [ ] T-028 [P] Final integration verification
  - **Description**: Run end-to-end tests for all user story acceptance criteria
  - **Inputs**: spec.md user story scenarios
  - **Outputs**: Verification evidence and PHR documentation
  - **Acceptance Criteria**:
    - User Story 1: Add task, view list, empty list scenarios
    - User Story 2: Update task, delete task, error handling scenarios
    - User Story 3: Complete task, idempotent completion scenarios
    - User Story 4: Filter by priority scenarios
    - User Story 5: Search by keyword scenarios
    - All exit codes correct (0 success, 1 errors)
    - Verify no business logic imports in cli/main.py (only imports from services, models)
    - Document thread-safety: Phase I is single-user CLI, no thread-safety guarantees required
  - **Complexity**: M
  - **Dependencies**: T-026, T-027
```

---

## User Story Task Summary

| User Story | Tasks | Description |
|------------|-------|-------------|
| US1: Add and View Tasks | T-010, T-011, T-017, T-018, T-019, T-020 | Add tasks, list tasks with filtering |
| US2: Update and Delete | T-012, T-013, T-021, T-022 | Update task details, delete tasks |
| US3: Mark Complete | T-014, T-023 | Mark tasks as complete |
| US4: Filter by Priority | T-015, T-024 | Filter tasks by priority level |
| US5: Search by Keyword | T-016, T-025 | Search tasks by keyword |

---

## Dependency Graph

```
Phase 1 (Setup)
    |
    +-- T-001 --> T-002, T-003, T-004
    |               |
    |               +-- T-002 --> T-005
    |               |
    |               +-- T-004 --> T-006, T-007 (Phase 2)
    |
    +-- T-005 --> (Phase 3 starts)

Phase 2 (Foundational Models)
    |
    +-- T-006, T-007 --> T-008 (Todo dataclass)
    |
    +-- T-008 --> (Phase 3 starts)

Phase 3 (TodoService Core)
    |
    +-- T-009 (Service init)
    |       |
    |       +-- T-010 --> add_task
    |       +-- T-011 --> get_task, list_tasks
    |       +-- T-012 --> update_task
    |       +-- T-013 --> delete_task
    |       +-- T-014 --> complete_task
    |       +-- T-015 --> filter_by_priority
    |       +-- T-016 --> search_tasks
    |
    +-- T-020 (services __init__.py)
            |
            +-- (Phase 4 starts)

Phase 4-8 (CLI Commands)
    |
    +-- T-017 (add) --> T-019 (CLI init)
    +-- T-018 (list) -/
    |
    +-- T-021 (update) --> (Phase 5)
    +-- T-022 (delete) -/
    |
    +-- T-023 (complete) --> (Phase 6)
    |
    +-- T-024 (filter) --> (Phase 7)
    |
    +-- T-025 (search) --> (Phase 8)

Phase 9 (Integration)
    |
    +-- T-026 (README update)
    +-- T-027 (mypy check)
    |
    +-- T-028 (Final verification)
```

---

## Parallel Execution Opportunities

The following tasks can be executed in parallel:

1. **T-006 and T-007**: Priority and Status enums can be implemented concurrently (both are simple enum definitions)

2. **T-010, T-011, T-012, T-013, T-014, T-015, T-016**: All TodoService methods can be implemented in parallel after T-009 is complete

3. **T-017 and T-018**: Add and list command handlers can be implemented concurrently

4. **T-019, T-020**: Both __init__.py files can be created concurrently

---

## Complexity Distribution

| Complexity | Tasks | Description |
|------------|-------|-------------|
| **S** (Small) | T-001, T-002, T-003, T-004, T-005, T-006, T-007, T-008, T-009, T-011, T-013, T-014, T-015, T-019, T-020, T-022, T-023, T-024, T-026, T-027 | Simple, straightforward implementation |
| **M** (Medium) | T-010, T-012, T-016, T-017, T-018, T-021, T-025, T-028 | Requires validation logic, multiple return paths, or integration |

**Distribution**: 20 Small (71%), 8 Medium (29%), 0 Large/XL

---

## Acceptance Criteria Checklist

Before marking any task complete, verify:

- [ ] Code follows the exact file path specified
- [ ] Type hints are complete (mypy --strict compliant)
- [ ] Docstrings are present for all public classes and functions
- [ ] Error handling matches contract specifications
- [ ] Exit codes are correct (0 for success, 1 for errors)
- [ ] Integration tests pass against the specification
- [ ] No business logic in CLI layer (only argument parsing and output formatting)
- [ ] TodoService methods are synchronous (no async/await)
- [ ] Service layer can be imported and used independently of CLI

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
