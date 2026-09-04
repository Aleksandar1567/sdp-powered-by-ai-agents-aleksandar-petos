# Chapter 2: Architecture Constraints

## 2.1 Technical Constraints

| ID   | Constraint | Rationale |
|------|-----------|-----------|
| TC-01 | **Python 3.12** | The kata is implemented in Python 3.12. No other language may be used. |
| TC-02 | **Single-process modular monolith** | All bounded contexts run in the same Python process. No separate services, containers, or processes. |
| TC-03 | **In-memory repositories only** | No external database, no file persistence, no network I/O. All data lives in plain Python data structures (dicts, lists) within the process lifetime. |
| TC-04 | **One module per bounded context** | The four bounded contexts (Posting, Social Graph, Timeline/Feed, Messaging) map 1:1 to Python packages/modules. |
| TC-05 | **pytest for all tests** | The test framework is pytest. No unittest, no other runners. |
| TC-06 | **No external frameworks** | No Django, FastAPI, SQLAlchemy, or similar. Only the Python standard library plus pytest and linting tools (`black`, `isort`, `ruff`). |
| TC-07 | **Pre-commit hooks must pass** | All commits must pass the configured pre-commit hooks (`black`, `isort`, `ruff`, PlantUML validation, commit message format). `--no-verify` must never be used. |

## 2.2 Organisational Constraints

| ID   | Constraint | Rationale |
|------|-----------|-----------|
| OC-01 | **Kata scope** | This is a learning exercise, not a production system. Features are limited to those listed in Chapter 1. No authentication, no authorisation, no rate limiting. |
| OC-02 | **Documentation-first** | Architecture documentation (arc42 + C4) must be produced and reviewed before implementation. |
| OC-03 | **Branch strategy** | Work happens on feature branches. Direct commits to `main`/`master` are not permitted. PRs must close the relevant GitHub issue. |
| OC-04 | **Reviewer** | The instructor (`momokrunic`) must be added as a reviewer on the PR before merging. |

## 2.3 Conventions

| ID   | Constraint | Rationale |
|------|-----------|-----------|
| CV-01 | **arc42 chapter structure** | Documentation follows the arc42 template, one file per chapter, under `architecture/`. |
| CV-02 | **C4 diagrams in PlantUML** | All architecture diagrams use the C4-PlantUML standard library. Diagrams are stored as `.puml` and rendered as `.svg`; markdown files reference only `.svg`. |
| CV-03 | **ADR format** | Every significant architectural decision gets an ADR in `architecture/09-architecture-decisions.md`, numbered sequentially. Old ADRs are never deleted — they are marked Superseded. |
| CV-04 | **Conventional Commits** | Commit messages follow the Conventional Commits specification enforced by the `check-commit-msg` hook. |
