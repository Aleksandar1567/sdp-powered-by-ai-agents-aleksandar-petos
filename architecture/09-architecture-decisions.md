# Architecture Decisions

## ADR-001: Use Python with In-Memory Modular Monolith for the Social Network Kata

**Status:** Accepted

**Context:**
The Social Network kata (Posting, Reading, Following, Mentions, Links, Direct
Messages) needs to be implemented as a small, testable exercise, not a
production system. We need fast development iteration, easy TDD, and a clear
separation between bounded contexts (Posting, Social Graph, Timeline/Feed,
Messaging) without the overhead of real infrastructure.

**Decision:**
Implement the kata in Python as a single-process modular monolith. Each
bounded context (Posting, Social Graph, Timeline/Feed, Messaging) is a
separate module with its own in-memory repository (plain Python data
structures), communicating through explicit module boundaries rather than a
shared database.

**Rationale:**
- Matches existing repo tooling (pyproject.toml already configured for
  Python 3.12, black, isort, ruff)
- In-memory storage keeps the kata focused on domain logic, not
  infrastructure
- Modular boundaries let each bounded context evolve independently and map
  cleanly to future C4 Container/Component diagrams
- No external dependencies needed to run or test the kata
- Fast to iterate on with pytest for TDD in later modules

**Consequences:**
- Data is not persisted between runs (acceptable for a kata, not for
  production)
- If the kata later needs to demonstrate EDA/microservices concepts, the
  modules must be refactored to communicate via events instead of direct
  in-process calls
- Team must be disciplined about not leaking one module's internals into
  another (e.g. Timeline must not reach directly into Social Graph's data
  structures)
