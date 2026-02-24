<!--
Sync Impact Report (Constitution Update)
=====================================
Version Change: None → 1.0.0
Modified Principles: N/A (Initial creation)
Added Sections: All (Initial constitution)
Removed Sections: None

Templates Status:
✅ plan-template.md - Reviewed, aligned with constitution principles
✅ spec-template.md - Reviewed, aligned with constitution principles
✅ tasks-template.md - Reviewed, aligned with constitution principles

Follow-up TODOs:
- None - All placeholders filled with project-specific values

Rationale for v1.0.0:
- Initial constitution for Evolution of Todo project
- Establishes fundamental principles for 5-phase hackathon
- Defines spec-driven development workflow
- Sets quality standards for all phases
-->

# Evolution of Todo Ecosystem Constitution

## Core Principles

### I. Spec-Driven Supremacy

**Rule**: No code is to be generated or modified without an approved specification and task ID.

**Rationale**: This hackathon tests mastery of Spec-Driven Development. Every line of code MUST trace back to:
- A specification document (spec.md)
- An implementation plan (plan.md)
- A specific task ID (tasks.md)

This ensures predictable, auditable development where Claude Code acts as an executor of well-defined requirements, not a "vibe coder."

**Enforcement**:
- Code files MUST include comments referencing Task IDs
- PRs rejected if task reference missing
- No "quick fixes" or "just this once" exceptions
- Spec updates trigger version control and re-planning

### II. Architecture First

**Rule**: Prioritize system architecture over implementation speed; every change must map back to speckit.plan.

**Rationale**: The Evolution of Todo project progresses through 5 phases (CLI → Web → AI Chatbot → K8s → Cloud). Each phase builds on the previous, making architectural continuity critical. Rushing to code without planning breaks the evolution path.

**Enforcement**:
- Architecture decisions documented in plan.md before implementation
- Cross-phase changes require constitution amendment
- Technology stack locked per phase (Python → Next.js/FastAPI → Agents SDK → K8s → Kafka/Dapr)
- Architectural Decision Records (ADRs) required for significant choices

**Architecture Evolution Path**:
- **Phase I**: Python CLI with in-memory storage, core CRUD logic
- **Phase II**: Next.js frontend + FastAPI backend + Neon DB, JWT authentication
- **Phase III**: OpenAI Agents SDK + MCP Server, stateless AI chatbot
- **Phase IV**: Docker containerization, Minikube deployment, Helm charts
- **Phase V**: Kafka event streaming, Dapr runtime, cloud deployment (DigitalOcean/Azure/GCP)

### III. Immutable Standards (Reusable Intelligence)

**Rule**: Every phase must inherit and respect the quality gates and logic established in previous phases.

**Rationale**: The project simulates real-world software evolution where you cannot "start over" each phase. Logic from Phase I must be reusable in Phase II; Phase II APIs must support Phase III chatbot; Phase III services must containerize for Phase IV.

**Enforcement**:
- Core business logic (Task CRUD) written once in Phase I, imported thereafter
- Phase II backend wraps Phase I logic, not rewrites it
- Phase III MCP tools call Phase II APIs, not duplicate logic
- Phase IV containers package Phase III app unchanged
- Phase V event-driven layer extends, not replaces, Phase IV

**Reuse Checklist**:
- [ ] Task model definition reused from Phase I
- [ ] CRUD operations inherited from previous phase
- [ ] Validation rules consistent across phases
- [ ] Test coverage maintained or expanded

### IV. Traceability

**Rule**: Maintain a strict Prompt History Record (PHR) for every significant architectural decision.

**Rationale**: Judges evaluate not just the final product but the **process**. PHRs provide evidence of spec-driven workflow, iterations with Claude Code, and decision-making rationale.

**Enforcement**:
- Every `/sp.specify`, `/sp.plan`, `/sp.tasks`, `/sp.implement` command generates a PHR
- PHRs stored in `history/prompts/` with routing:
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`
- PHR format includes: prompt text (verbatim), response text, task links, artifacts modified

**PHR Required For**:
- New feature specifications
- Architectural decisions (plan.md updates)
- Task breakdowns
- Constitution amendments
- Integration with new technologies (MCP, Dapr, Kafka)

### V. Coding Standards

**Rule**: Use strictly typed Python (Type Hints/PEP 8) for backend and strictly typed TypeScript for frontend.

**Rationale**: Type safety reduces bugs, improves IDE support, and makes code self-documenting. Critical for multi-phase projects where code evolves over months.

**Python Standards**:
- All function signatures include type hints
- `mypy --strict` passes without errors
- PEP 8 compliance enforced by Black formatter
- Dataclasses or Pydantic models for data structures

**TypeScript Standards**:
- `"strict": true` in tsconfig.json
- No `any` types without explicit justification
- Interface definitions for all API contracts
- ESLint + Prettier for consistency

### VI. Decoupled Logic

**Rule**: Use Repository or Service pattern to ensure business logic is decoupled from UI/interface.

**Rationale**: This enables the CLI → Web → Chatbot evolution. The same task logic must work via command line (Phase I), REST API (Phase II), and natural language (Phase III).

**Enforcement**:
- **Phase I**: Core logic in `src/services/task_service.py`, CLI in `src/cli/`
- **Phase II**: Backend calls `task_service.py`, frontend calls REST API
- **Phase III**: MCP tools call `task_service.py`, Agents SDK handles NLP

**Anti-patterns to Avoid**:
- Database queries in API route handlers
- Business validation in React components
- Tight coupling between UI framework and logic

### VII. Security

**Rule**: JWT-based authentication is mandatory for all multi-user phases, ensuring total user data isolation.

**Rationale**: Phase II introduces multi-user support. Without proper auth, users could access each other's tasks. This is a non-negotiable security requirement.

**Enforcement**:
- **Phase II+**: Better Auth configured to issue JWT tokens
- Frontend includes `Authorization: Bearer <token>` in all API requests
- Backend middleware validates JWT and extracts `user_id`
- All database queries filtered by authenticated `user_id`
- Endpoints without valid token return `401 Unauthorized`

**Security Checklist**:
- [ ] JWT secret shared between frontend and backend via `.env`
- [ ] Token expiry configured (e.g., 7 days)
- [ ] User ID extracted from token, not trusted from request body
- [ ] Database foreign keys enforce user ownership

### VIII. Verification

**Rule**: All features must have acceptance criteria defined during planning and verified before marking complete.

**Rationale**: Spec-driven development requires measurable success criteria. "Done" means acceptance scenarios pass, not just "code compiles."

**Enforcement**:
- Every spec.md includes Given-When-Then acceptance scenarios
- Tasks marked complete only when acceptance tests pass
- Manual verification required if automated tests not implemented
- PHR documents verification evidence (screenshots, logs, test output)

**Acceptance Example** (Phase I: Add Task):
```
Given: User starts the CLI app
When: User runs `add "Buy groceries" "Milk, eggs, bread"`
Then: Task appears in task list with ID, title, description, status "pending"
```

## Technology Stack

### Phase I: In-Memory Python Console App
- **Language**: Python 3.10+
- **Package Manager**: UV
- **Storage**: In-memory data structures (dict, list)
- **CLI Framework**: argparse or Click
- **Testing**: pytest (optional for Phase I)

### Phase II: Full-Stack Web Application
- **Frontend**: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- **Backend**: Python FastAPI, uvicorn
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT plugin
- **Hosting**: Vercel (frontend), any Python host (backend)

### Phase III: AI-Powered Chatbot
- **Chat UI**: OpenAI ChatKit
- **AI Framework**: OpenAI Agents SDK
- **MCP Server**: Official MCP SDK (Python)
- **Backend**: Same as Phase II + MCP server
- **Database**: Same as Phase II + conversation/message tables

### Phase IV: Local Kubernetes Deployment
- **Containerization**: Docker, Docker Desktop
- **Orchestration**: Kubernetes (Minikube)
- **Package Manager**: Helm Charts
- **AI DevOps**: kubectl-ai, kagent
- **Optional**: Docker AI Agent (Gordon) for intelligent Docker operations

### Phase V: Advanced Cloud Deployment
- **Event Streaming**: Kafka (Strimzi on K8s or Redpanda Cloud)
- **Distributed Runtime**: Dapr (Pub/Sub, State, Bindings, Secrets, Service Invocation)
- **Cloud Provider**: DigitalOcean Kubernetes (DOKS), Azure AKS, or Google GKE
- **CI/CD**: GitHub Actions
- **Monitoring**: (Optional) Prometheus, Grafana

## Operational Constraints

### Tooling

**Rule**: Use Claude Code for all generation; manual coding is strictly prohibited.

**Rationale**: This hackathon evaluates your ability to **architect with AI**, not write syntax. You are the Product Architect; Claude Code is the Builder.

**Allowed**:
- Writing specifications in natural language
- Refining prompts to Claude Code
- Reviewing generated code
- Testing and validation
- Debugging by providing error logs to Claude

**Prohibited**:
- Manually writing implementation code
- Editing generated code outside of Claude Code workflow
- "Quick fixes" that bypass spec-driven process

**Process**:
1. Write spec → `/sp.specify`
2. Claude asks clarifying questions → `/sp.clarify`
3. Generate plan → `/sp.plan`
4. Break into tasks → `/sp.tasks`
5. Implement → `/sp.implement`
6. Verify → Mark task complete in tasks.md

### Structure

**Rule**: Maintain a Monorepo structure with a central `specs/` directory serving as the single source of truth for all phases.

**Rationale**: Multiple repos complicate Claude Code's ability to maintain context across frontend/backend/infrastructure. Monorepo enables atomic commits and easier cross-layer changes.

**Repository Structure**:
```
hackathon-todo/
├── .specify/                    # Spec-Kit configuration & templates
│   ├── memory/
│   │   └── constitution.md      # This file
│   ├── templates/
│   │   ├── spec-template.md
│   │   ├── plan-template.md
│   │   └── tasks-template.md
│   └── scripts/
├── specs/                       # All feature specifications
│   ├── overview.md
│   ├── architecture.md
│   ├── features/
│   │   ├── task-crud.md
│   │   ├── authentication.md
│   │   └── chatbot.md
│   └── api/
│       ├── rest-endpoints.md
│       └── mcp-tools.md
├── history/                     # Prompt History Records
│   ├── prompts/
│   │   ├── constitution/
│   │   ├── phase-1/
│   │   ├── phase-2/
│   │   └── general/
│   └── adr/                     # Architecture Decision Records
├── phase-1-cli/                 # Phase I: Python CLI app
│   ├── src/
│   ├── tests/
│   └── README.md
├── phase-2-web/                 # Phase II onwards
│   ├── frontend/
│   ├── backend/
│   ├── docker-compose.yml
│   └── README.md
├── CLAUDE.md                    # Root Claude Code instructions
└── README.md                    # Project documentation
```

### Workflow

**Rule**: Strictly follow the SDD lifecycle: Specify → Plan → Tasks → Implement.

**Enforcement**:
- No tasks created without a plan
- No plan created without a spec
- No implementation without a task ID
- All stages versioned in git

**SDD Commands**:
- `/sp.constitution` - Create/update project constitution
- `/sp.specify` - Write feature specification (WHAT)
- `/sp.clarify` - Ask clarifying questions on spec
- `/sp.plan` - Generate implementation plan (HOW)
- `/sp.tasks` - Break plan into atomic tasks
- `/sp.implement` - Execute task(s)
- `/sp.phr` - Generate Prompt History Record
- `/sp.adr` - Document architectural decision

### Evolutionary Path

**Rule**: Strictly adhere to the technology stack progression defined in the Architecture First principle.

**Phase Gate Requirements**:

**Phase I → Phase II**:
- [ ] Core CRUD logic extracted to reusable module
- [ ] Task data model defined with types
- [ ] Basic validation rules documented

**Phase II → Phase III**:
- [ ] REST API endpoints documented with OpenAPI
- [ ] JWT authentication working
- [ ] Database schema stable
- [ ] API client library available

**Phase III → Phase IV**:
- [ ] MCP tools defined and tested
- [ ] Stateless server architecture verified
- [ ] Conversation state persisted to DB
- [ ] Health check endpoints available

**Phase IV → Phase V**:
- [ ] All services containerized
- [ ] Helm charts working on Minikube
- [ ] Resource limits defined
- [ ] Zero-downtime deployment strategy

## Success Criteria

### Logic Continuity

**Requirement**: Code from Phase I must be imported or adapted into Phase II without complete logic rewrites.

**Verification**:
- Phase II `backend/src/services/task_service.py` imports from Phase I `src/services/task_service.py`
- Task model (`Task` class) identical or extended, not redefined
- CRUD operations call Phase I functions with persistence layer added

### Spec-Code Alignment

**Requirement**: 100% of implemented code must reference specific Task IDs and Spec sections.

**Verification**:
- Every code file includes header comment:
  ```python
  # Task: T-042
  # Spec: specs/features/task-crud.md §2.3
  # Plan: specs/features/task-crud/plan.md §4.1
  ```
- Git commits reference task IDs: `feat(T-042): Add task creation endpoint`

### Deployment Integrity

**Requirement**: All cloud-native components (Kafka, Dapr, K8s) must pass health checks and run without errors.

**Verification**:
- `kubectl get pods --all-namespaces` shows all pods `Running`
- Health endpoints return `200 OK`
- Kafka topics created and accepting messages
- Dapr sidecars initialized successfully
- Application accessible via ingress/load balancer

### Feature Completeness

**Phase I** (100 points):
- [ ] Add Task
- [ ] Delete Task
- [ ] Update Task
- [ ] View Task List
- [ ] Mark Task Complete

**Phase II** (150 points):
- [ ] All Phase I features via web UI
- [ ] User authentication (signup/signin)
- [ ] Multi-user data isolation
- [ ] RESTful API endpoints
- [ ] Persistent database storage

**Phase III** (200 points):
- [ ] Natural language task management
- [ ] Stateless chat endpoint
- [ ] MCP server with 5 tools (add/list/complete/delete/update)
- [ ] Conversation persistence
- [ ] AI agent with OpenAI Agents SDK

**Phase IV** (250 points):
- [ ] Dockerfiles for frontend/backend
- [ ] Helm charts for deployment
- [ ] Local deployment on Minikube
- [ ] Health checks and readiness probes
- [ ] Resource limits configured

**Phase V** (300 points):
- [ ] Kafka event streaming for task operations
- [ ] Dapr integration (Pub/Sub, State, Secrets)
- [ ] Cloud deployment (DOKS/AKS/GKE)
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Advanced features (priorities, tags, search, recurring tasks, reminders)

**Bonus Points** (up to 600):
- [ ] Reusable Intelligence (custom subagents/skills) +200
- [ ] Cloud-Native Blueprints (Agent Skills) +200
- [ ] Multi-language support (Urdu) +100
- [ ] Voice commands +200

## Governance

### Amendment Process

1. **Proposal**: Create `history/adr/YYYY-MM-DD-constitution-amendment.md` with rationale
2. **Review**: Discuss with stakeholders (team, mentors)
3. **Approval**: Document approval in ADR
4. **Implementation**: Update `constitution.md` with version bump
5. **Migration**: Update all dependent specs, plans, tasks
6. **PHR**: Generate Prompt History Record for amendment

### Version Policy

This constitution follows semantic versioning:
- **MAJOR**: Backward-incompatible principle removals or redefinitions
- **MINOR**: New principle/section added or materially expanded guidance
- **PATCH**: Clarifications, wording, typo fixes

### Compliance Review

- All PRs must verify constitution compliance
- Claude Code must reference constitution in planning phase
- Spec templates must include "Constitution Check" section
- Violations require justification in ADR or rejection

### Hierarchy

When conflicts arise, precedence order:
1. **Constitution** (this file) - Project-wide non-negotiables
2. **Spec** (spec.md) - Feature requirements
3. **Plan** (plan.md) - Implementation architecture
4. **Tasks** (tasks.md) - Execution breakdown

### Living Document

This constitution is a **living document**. As the project evolves through 5 phases, expect amendments to:
- Add phase-specific principles (e.g., "Kafka Event Schema Stability" in Phase V)
- Refine tooling constraints (e.g., "Gordon usage optional" after Phase IV)
- Document learned best practices

**Expectation**: Constitution reviewed and potentially amended between each phase.

---

**Version**: 1.0.0 | **Ratified**: 2025-12-31 | **Last Amended**: 2025-12-31
