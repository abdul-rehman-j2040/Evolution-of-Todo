---
id: 003
title: Phase I Implementation Plan Generation
stage: plan
date: 2025-01-01
surface: agent
model: claude-sonnet-4-5
feature: phase-1-cli
branch: 001-phase-1-cli
user: hackathon-participant
command: /sp.plan
labels: ["phase-1", "implementation-plan", "architecture", "python-cli", "service-pattern"]
links:
  spec: specs/001-phase-1-cli/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-phase-1-cli/plan.md
  - specs/001-phase-1-cli/research.md
  - specs/001-phase-1-cli/data-model.md
  - specs/001-phase-1-cli/quickstart.md
  - specs/001-phase-1-cli/contracts/add.md
  - specs/001-phase-1-cli/contracts/list.md
  - specs/001-phase-1-cli/contracts/update.md
  - specs/001-phase-1-cli/contracts/delete.md
  - specs/001-phase-1-cli/contracts/complete.md
  - specs/001-phase-1-cli/contracts/filter.md
  - specs/001-phase-1-cli/contracts/search.md
tests:
  - N/A (Planning phase - implementation tests defined in plan.md)
---

## Prompt

Intent:
Create a comprehensive technical implementation plan for 'Phase I: In-Memory Python Todo CLI'. The plan must bridge the gap between our current Spec and the future 'Phase II: Web App' by establishing a clean, decoupled architecture.

Agentic Orchestration:
- Use the 'spec-architect' and 'modular-ai-architect' agents to design the component breakdown.
- Consult the 'todo-domain-expert' skill to ensure the Todo logic handles all edge cases identified in the clarification phase.
- Ensure the 'backend-builder-opus' agent can interpret this plan to generate atomic, dependency-ordered tasks later.
- If you need to verify local environment constraints, use the 'filesystem' and 'git' MCP servers.

Plan Requirements:
1. Architecture Sketch: Design a 3-layer structure:
   - Layer 1: Domain Models (Data Validation).
   - Layer 2: TodoService (Pure Business Logic).
   - Layer 3: Console Controller (User Interface).
2. Component Breakdown: Identify specific files and modules (e.g., models.py, service.py, main.py).
3. Design Decisions (ADRs): Highlight key choices.
4. Quality Validation: Define a testing strategy.

Technical Focus:
- Folder: phase-1-cli/
- Compliance: Must strictly adhere to the standards in .specify/memory/constitution.md.

**Clarifications From Session 2025-01-01**:
1. CLI Pattern: Single-command execution (argparse style)
2. Data Model: Python dataclass with type hints (NOT Pydantic)
3. Service Methods: Synchronous (NOT async)
4. Error Handling: Optional/Result pattern
5. State Management: Instance attribute `self._tasks: List[Todo]`

## Response snapshot

Successfully generated comprehensive implementation plan using spec-architect agent.

**Planning Documents Created (12 files, ~90KB total)**:

**1. plan.md** (Master implementation plan):
- Technical Context: Python 3.10+, standard library only, in-memory storage
- Constitution Check: Verified all 8 principles, no violations
- Project Structure: Single project pattern with src/models, src/services, src/cli
- Complexity Tracking: Empty (no violations)
- Includes inline Phase 0 research and Phase 1 design
- Next step: /sp.tasks command

**2. research.md** (Architecture Decision Records):
- **Decision 1: Dataclass vs Pydantic**: Chose dataclass (standard library requirement)
  - Rationale: Constitution compliance, lightweight, Phase II upgradeable to SQLModel
  - Alternatives: Pydantic (violates stdlib only), NamedTuple (less flexible)
  - Phase II Impact: Minimal - add SQLModel as wrapper, core logic unchanged

- **Decision 2: Sync vs Async**: Chose synchronous methods
  - Rationale: No I/O in Phase I, YAGNI principle, simpler testing
  - Alternatives: Async now (premature), dual sync/async (overcomplicated)
  - Phase II Impact: FastAPI wraps sync in async handlers easily

- **Decision 3: argparse vs Click**: Chose argparse
  - Rationale: Standard library, single-command pattern support
  - Alternatives: Click (external dep), custom parser (reinventing wheel)

- **Decision 4: Error Handling**: Optional/Result pattern
  - Rationale: Type-safe, explicit, maps to HTTP status codes
  - Method signatures: `Optional[Todo]`, `tuple[Optional[Todo], Optional[str]]`

- **Decision 5: State Storage**: Instance attribute `List[Todo]`
  - Rationale: Encapsulation, testability, DI-friendly for Phase II

**3. data-model.md** (Complete data specifications):
- Todo dataclass with 6 fields (id, title, description, priority, status, created_at)
- Priority enum: High=3, Medium=2, Low=1
- Status enum: Pending, Completed
- Validation rules: title 1-200 chars, description max 1000 chars
- Type hints: All fields fully typed with Optional where applicable
- Phase II migration: Dataclass → SQLModel table=True

**4. quickstart.md** (User guide):
- Installation: Python 3.10+, UV commands
- 7 command examples with expected output
- Common workflows (daily task management, priority management)
- Troubleshooting and limitations
- Clear Phase I scope boundaries

**5-11. contracts/*.md** (7 CLI command contracts):
- **add.md**: Create task with title, description, optional priority
- **list.md**: Display all tasks or filter by status
- **update.md**: Modify task title, description, priority by ID
- **delete.md**: Remove task by ID
- **complete.md**: Toggle task completion status
- **filter.md**: Filter tasks by priority level
- **search.md**: Search tasks by keyword in title/description

Each contract defines:
- Command signature: `todo <command> [arguments] [options]`
- Usage examples
- Success/error output formats
- Service layer method signature
- CLI handler pseudocode
- Acceptance test scenarios
- Phase II HTTP endpoint mapping

**Project Structure Defined**:
```
phase-1-cli/
├── src/
│   ├── models/
│   │   ├── todo.py          # Todo dataclass
│   │   └── enums.py         # Priority, Status enums
│   ├── services/
│   │   └── todo_service.py  # TodoService class
│   └── cli/
│       └── main.py          # argparse CLI entry
├── tests/ (optional)
│   ├── unit/
│   └── integration/
├── pyproject.toml
└── README.md
```

**Constitution Compliance Gates**:
- ✅ Spec-Driven Supremacy: All code will reference task IDs
- ✅ Architecture First: Service pattern documented
- ✅ Immutable Standards: TodoService importable in Phase II
- ✅ Coding Standards: mypy --strict, PEP 8, type hints
- ✅ Decoupled Logic: 3-layer separation (models/service/cli)
- ✅ Verification: Acceptance criteria in all contracts

**Key Design Highlights**:
- TodoService maintains `self._tasks: List[Todo]` (instance attribute)
- Methods return `Optional[Todo]` or `(data, error)` tuples (type-safe errors)
- Synchronous methods (async in Phase II when needed)
- Argparse single-command pattern (like git, docker)
- Zero external dependencies (constitution compliant)

**Phase II Reusability Strategy**:
- TodoService methods unchanged, just add DB session parameter
- Dataclass converts to SQLModel with table=True
- CLI commands map 1:1 to REST endpoints
- Error tuples map to HTTP status codes (None→404, error→400)

## Outcome

- ✅ Impact: Comprehensive implementation plan created with 12 files (~90KB); establishes 3-layer architecture (models/service/cli); documents 5 critical architecture decisions with Phase II impact analysis; defines complete project structure for phase-1-cli/; all 7 CLI commands fully specified with contracts; constitution compliance verified (no violations)
- 🧪 Tests: Testing strategy defined in plan.md; unit tests for service layer (optional); integration tests for CLI workflows (optional); acceptance criteria embedded in all 7 command contracts
- 📁 Files: Created: plan.md (23.8KB), research.md (18.0KB), data-model.md (14.6KB), quickstart.md (11.7KB), contracts/*.md (7 files, 52.7KB total); All in specs/001-phase-1-cli/
- 🔁 Next prompts:
  1. `/sp.tasks` - Break plan into atomic implementation tasks with dependencies
  2. Review plan.md and research.md to validate architecture decisions
  3. Consider `/sp.adr` for "Service Pattern vs Repository Pattern" if architectural justification needed for stakeholders
  4. Execute `/sp.implement` after tasks are created and approved
- 🧠 Reflection: Plan successfully resolves user's request conflict (Pydantic/async) vs constitution requirements (stdlib/sync) by choosing constitution compliance while documenting Phase II upgrade path. Key insight: Service pattern with Optional/Result error handling provides clean contract that works for both CLI and future FastAPI without modifications. Critical decision: Instance-based state (not class-level) enables proper testing and DI in Phase II. All 7 command contracts include Phase II HTTP mapping, ensuring seamless evolution. No constitution violations - perfect alignment with all 8 principles.

## Evaluation notes (flywheel)

- Failure modes observed: Initial conflict between user request (Pydantic/async) and clarification decisions (dataclass/sync). Resolution: Followed clarification session and constitution, documented rationale in research.md. Potential future failure: If planning didn't adequately explain Phase II migration path, tasks phase might add unnecessary abstraction. Mitigation: research.md includes detailed "Phase II Impact" for each decision.
- Graders run and results (PASS/FAIL):
  - Constitution Compliance: PASS (all 8 principles verified, 0 violations)
  - Completeness: PASS (12 files created, all template sections filled)
  - Technical Context: PASS (no NEEDS CLARIFICATION markers remain)
  - Phase II Compatibility: PASS (all decisions include migration analysis)
  - Contract Clarity: PASS (all 7 commands have complete specifications)
  - Consistency: PASS (dataclass/sync pattern used consistently across all docs)
- Prompt variant (if applicable): Standard /sp.plan execution with pre-clarified architecture decisions. User initially suggested different tech (Pydantic/async) but clarification session overrode per constitution. Plan documents both original request and final decision with rationale.
- Next experiment (smallest change to try): Monitor `/sp.tasks` execution to validate whether contracts provide sufficient detail for atomic task breakdown. If tasks require additional interface specifications, contracts/*.md might need method signature examples. Consider whether TodoService interface should be explicitly defined as Protocol or ABC for better type checking (currently implicit interface).
