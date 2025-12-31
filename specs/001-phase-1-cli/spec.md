# Feature Specification: Phase I - Professional In-Memory Python Todo CLI

**Feature Branch**: `001-phase-1-cli`
**Created**: 2025-12-31
**Status**: Draft
**Input**: User description: "Phase I: Professional In-Memory Python Todo CLI (The Logic Foundation)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add and View Tasks (Priority: P1)

As a professional managing daily work, I need to quickly add tasks with titles and descriptions, and view my complete task list so I can keep track of what needs to be done.

**Why this priority**: This is the foundation of any todo app - without the ability to add and view tasks, no other functionality matters. This represents the MVP (Minimum Viable Product).

**Independent Test**: Can be fully tested by launching the CLI, adding 3 tasks with different titles and descriptions, viewing the list, and verifying all tasks appear with correct information.

**Acceptance Scenarios**:

1. **Given** the CLI is launched, **When** I add a task with title "Buy groceries" and description "Milk, eggs, bread", **Then** the task is stored with a unique ID, the provided title and description, default priority "Medium", status "Pending", and current timestamp
2. **Given** I have added 3 tasks, **When** I view the task list, **Then** all 3 tasks are displayed with their ID, title, status, and priority in the order they were created
3. **Given** an empty task list, **When** I view the task list, **Then** I see a message indicating no tasks exist

---

### User Story 2 - Update and Delete Tasks (Priority: P2)

As a user managing tasks, I need to update task details when plans change and delete tasks that are no longer relevant so my list stays accurate and current.

**Why this priority**: Once users can add tasks, they immediately need the ability to correct mistakes or change details. This makes the app truly usable for real-world scenarios.

**Independent Test**: Can be tested by creating 2 tasks, updating the title and description of the first task, deleting the second task, and verifying changes are reflected correctly in the task list.

**Acceptance Scenarios**:

1. **Given** a task exists with ID 1, **When** I update its title to "Buy organic groceries" and description to "Whole milk, free-range eggs, whole grain bread", **Then** the task's title and description are updated while preserving its ID, priority, status, and created timestamp
2. **Given** a task exists with ID 2, **When** I delete it, **Then** the task is removed from the list and subsequent view commands do not show it
3. **Given** I attempt to update a non-existent task ID, **When** I execute the update command, **Then** I receive a clear error message stating the task was not found
4. **Given** I attempt to delete a non-existent task ID, **When** I execute the delete command, **Then** I receive a clear error message stating the task was not found

---

### User Story 3 - Mark Tasks Complete (Priority: P3)

As a user completing work, I need to mark tasks as complete so I can track my progress and distinguish between pending and finished work.

**Why this priority**: Completion tracking is essential for productivity, but the app is still useful without it for simple list management. This adds significant value to task management.

**Independent Test**: Can be tested by creating 3 tasks, marking 2 as complete, viewing the list, and verifying the status is updated correctly and pending tasks remain unchanged.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 has status "Pending", **When** I mark it as complete, **Then** its status changes to "Completed" while all other attributes remain unchanged
2. **Given** a task with ID 2 is already "Completed", **When** I mark it as complete again, **Then** it remains "Completed" with no error
3. **Given** I have 5 tasks (3 pending, 2 completed), **When** I view the list, **Then** I can clearly distinguish which tasks are pending and which are completed

---

### User Story 4 - Filter Tasks by Priority (Priority: P4)

As a user managing multiple tasks with different urgency levels, I need to filter my task list by priority so I can focus on high-priority items first.

**Why this priority**: Priority filtering helps users manage workload effectively, but is not required for basic task management. This enhances productivity once the core features work.

**Independent Test**: Can be tested by creating 6 tasks with mixed priorities (2 High, 2 Medium, 2 Low), filtering by "High" priority, and verifying only High priority tasks are shown.

**Acceptance Scenarios**:

1. **Given** I have tasks with mixed priorities, **When** I filter by priority "High", **Then** only tasks with priority "High" are displayed
2. **Given** I have 10 tasks, **When** I filter by priority "Low", **Then** only tasks with priority "Low" are displayed, regardless of their status
3. **Given** no tasks match the priority filter, **When** I apply the filter, **Then** I see a message indicating no tasks match the filter criteria

---

### User Story 5 - Search Tasks by Keyword (Priority: P5)

As a user with many tasks, I need to search for tasks by keywords in their title or description so I can quickly find specific tasks without scrolling through the entire list.

**Why this priority**: Search is a convenience feature that becomes valuable as the task list grows, but is not essential for managing a small number of tasks.

**Independent Test**: Can be tested by creating 10 tasks with varied titles and descriptions, searching for keyword "meeting", and verifying only tasks containing "meeting" in title or description are shown.

**Acceptance Scenarios**:

1. **Given** I have tasks with various titles and descriptions, **When** I search for keyword "groceries", **Then** all tasks containing "groceries" in title OR description are displayed (case-insensitive)
2. **Given** I search for a keyword that doesn't exist in any task, **When** I execute the search, **Then** I see a message indicating no tasks match the search term
3. **Given** I search for keyword "project", **When** 5 tasks match in title and 3 match in description, **Then** all 8 unique tasks are displayed (no duplicates)

---

### Edge Cases

- What happens when a user attempts to add a task with an empty title? (TodoService validates and returns error tuple)
- What happens when a user attempts to add a task with a title exceeding 200 characters? (TodoService validates and returns error tuple)
- What happens when a user attempts to add a task with a description exceeding 1000 characters? (TodoService validates and returns error tuple)
- How does the system handle concurrent operations (not applicable for single-user CLI, but important for Phase II evolution)?
- What happens when filtering by an invalid priority value? (TodoService returns empty list or error tuple)
- What happens when the task list contains 1000+ tasks (performance consideration)?
- How does search handle special characters and punctuation? (Case-insensitive substring matching, special chars treated as literals)
- What happens if two tasks are created at the exact same timestamp? (Both valid, IDs remain unique)

## Clarifications

### Session 2025-01-01

- Q: How should users interact with the CLI application? → A: Single-command execution (argparse style) - Each operation is a separate command like `todo add "title"`, `todo list`, `todo delete 5` (similar to git, docker CLI). This aligns with Unix philosophy, supports scripting, and maps cleanly to Phase II API endpoints.
- Q: What data structure should represent the Todo entity in Phase I? → A: Python dataclass with type hints - Native Python 3.10+ feature providing automatic methods (__init__, __repr__, __eq__), full type safety, lightweight for in-memory use, and easy to extend for Phase II serialization.
- Q: Should TodoService methods be synchronous or asynchronous in Phase I? → A: Synchronous methods (no async/await) - Phase I has no I/O operations (in-memory only), so async adds unnecessary complexity. Phase II FastAPI handlers can easily wrap synchronous service methods in async endpoints.
- Q: How should TodoService communicate errors to the CLI layer? → A: Return type with Optional/Result pattern - Methods return `Optional[Todo]` or tuple `(success_data, error_msg)`. Explicit, type-safe error handling that forces CLI to handle error cases and maps cleanly to Phase II HTTP status codes.
- Q: How should TodoService store and manage the task collection internally? → A: Instance attribute (list of Todo objects) - `self._tasks: List[Todo] = []` managed by TodoService instance. Clean encapsulation, easy to test, and Phase II compatible with dependency injection.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to add a new task with a title (required) and description (optional)
- **FR-002**: System MUST automatically assign a unique integer ID to each task, starting from 1 and incrementing sequentially
- **FR-003**: System MUST automatically assign a default priority of "Medium" to new tasks unless specified otherwise
- **FR-004**: System MUST automatically assign a default status of "Pending" to new tasks
- **FR-005**: System MUST automatically capture the creation timestamp for each task using the system's current date and time
- **FR-006**: System MUST allow users to view all tasks with their ID, title, status, priority, and creation date
- **FR-007**: System MUST allow users to update a task's title and/or description by specifying the task ID
- **FR-008**: System MUST allow users to delete a task by specifying the task ID
- **FR-009**: System MUST allow users to mark a task as complete by specifying the task ID
- **FR-010**: System MUST allow users to set or change a task's priority to High, Medium, or Low when creating or updating
- **FR-011**: System MUST allow users to filter the task list by priority level (High, Medium, Low)
- **FR-012**: System MUST allow users to search for tasks by keyword, matching against title or description (case-insensitive)
- **FR-013**: System MUST validate that task titles are between 1 and 200 characters
- **FR-014**: System MUST validate that task descriptions do not exceed 1000 characters
- **FR-015**: System MUST display clear error messages when users attempt to update, delete, or mark complete a non-existent task ID (TodoService returns None or error tuple, CLI formats and displays message)
- **FR-016**: System MUST store all tasks in-memory using Python data structures (TodoService maintains `List[Todo]` as instance attribute)
- **FR-017**: System MUST provide a command-line interface (CLI) for all user interactions using single-command execution pattern (e.g., `todo add "title"`, `todo list`, `todo delete 5`)
- **FR-018**: System MUST separate business logic (TodoService) from CLI interface code using synchronous methods (in-memory operations only, no async required)

### Key Entities

- **Todo**: Represents a single task/item to be completed (implemented as Python dataclass with type hints)
  - Unique identifier (integer ID)
  - Title (string, 1-200 characters)
  - Description (string, 0-1000 characters, optional)
  - Priority level (enumeration: High, Medium, Low)
  - Status (enumeration: Pending, Completed)
  - Creation timestamp (datetime)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a new task in under 5 seconds from command execution to confirmation
- **SC-002**: Users can view their complete task list in under 2 seconds regardless of list size up to 100 tasks
- **SC-003**: Users can update or delete an existing task in under 5 seconds from command execution to confirmation
- **SC-004**: Users can mark a task as complete in under 3 seconds from command execution to confirmation
- **SC-005**: Users can filter tasks by priority and see results in under 2 seconds
- **SC-006**: Users can search for tasks by keyword and see results in under 2 seconds for lists up to 100 tasks
- **SC-007**: 100% of business logic functions can be tested independently of the CLI interface
- **SC-008**: The system maintains data integrity across all operations (no duplicate IDs, no lost data during updates/deletes)
- **SC-009**: Error messages are clear and actionable (e.g., "Task with ID 5 not found" instead of generic errors)
- **SC-010**: The core service logic can be imported and used by a web API without any modifications to the business logic

## Assumptions

- **Single User**: Phase I is designed for a single user running on their local machine. Multi-user support will be added in Phase II with authentication and database persistence.

- **Session-Based Storage**: All tasks are stored in-memory and will be lost when the application closes. This is acceptable for Phase I as persistence is planned for Phase II with Neon PostgreSQL.

- **Sequential ID Assignment**: Task IDs are assigned sequentially starting from 1. While this could theoretically lead to ID conflicts in a multi-user scenario, it's acceptable for Phase I's single-user context.

- **Priority Defaults**: When a user doesn't specify a priority, the system defaults to "Medium" as this represents the most common task urgency level.

- **UTF-8 Support**: The CLI will support UTF-8 characters in task titles and descriptions, allowing international characters and emojis.

- **Command-Line Interface**: Users are comfortable with command-line interfaces and can execute commands with arguments. No GUI is provided in Phase I.

- **Python Environment**: Users have Python 3.10+ installed with the ability to install dependencies via UV package manager.

- **No Undo/Redo**: Phase I does not include undo/redo functionality. Users must manually correct mistakes by updating or deleting tasks.

- **No Task History**: The system does not track change history for tasks. Only the current state is maintained.

- **No Reminders/Notifications**: Phase I focuses on task management only. Reminder and notification features are planned for Phase V with Kafka event streaming.

- **Linear Time Complexity Acceptable**: For Phase I's expected usage (< 100 tasks), linear search algorithms are acceptable. Performance optimization will be addressed if needed in later phases.

## Dependencies

- **Python 3.10+**: Required for modern type hints syntax including union types (PEP 604)
- **UV Package Manager**: Used for Python dependency management and virtual environment creation
- **Standard Library Only**: Phase I relies exclusively on Python's standard library (no external dependencies required)
  - `dataclasses` for Todo entity definition
  - `datetime` for timestamp management
  - `enum` for Priority and Status enumerations
  - `typing` for type hints
  - `argparse` for CLI parsing (single-command execution pattern)

## Out of Scope

- **Persistence**: No file or database storage in Phase I (planned for Phase II)
- **Multi-User Support**: No user authentication or data isolation (planned for Phase II)
- **Web Interface**: No REST API or web UI (planned for Phase II)
- **Natural Language Processing**: No AI chatbot integration (planned for Phase III)
- **Containerization**: No Docker or Kubernetes (planned for Phase IV)
- **Event Streaming**: No Kafka or Dapr (planned for Phase V)
- **Due Dates**: Task due dates and reminders (planned for Phase V)
- **Task Categories/Tags**: Grouping tasks by categories (planned for Phase V)
- **Recurring Tasks**: Automatic task repetition (planned for Phase V)
- **Task Priority Sorting**: Automatic sorting by priority (only filtering required)
- **Task Export/Import**: Exporting task list to external formats
- **Configuration File**: No persistent settings or user preferences
- **Task Archiving**: No separate archive for completed tasks
