# Chapter 9: Architecture Decisions

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
- Matches existing repo tooling (`pyproject.toml` already configured for Python 3.12, black, isort, ruff)
- In-memory storage keeps the kata focused on domain logic, not infrastructure
- Modular boundaries let each bounded context evolve independently and map cleanly to future C4 Container/Component diagrams
- No external dependencies needed to run or test the kata
- Fast to iterate on with pytest for TDD

**Consequences:**
- Data is not persisted between runs (acceptable for a kata, not for production)
- If the kata later needs to demonstrate EDA/microservices concepts, the modules must be refactored to communicate via events instead of direct in-process calls
- Team must be disciplined about not leaking one module's internals into another (e.g. Timeline must not reach directly into Social Graph's data structures)

---

## ADR-002: Use the Repository Pattern with In-Memory Implementations

**Status:** Accepted

**Context:**
Domain services (e.g. `TimelineService`) need to retrieve data from other
bounded contexts. We need to decide how services access data: shared global
state, direct dict access, or an abstraction layer.

**Decision:**
Each bounded context exposes its data through a repository class
(`InMemory*Repository`). Services receive repository instances via constructor
injection (dependency injection). No service accesses another context's
internal data structures directly.

**Rationale:**
- The repository pattern decouples domain logic from storage implementation
- Constructor injection makes dependencies explicit and testable (repositories can be pre-populated in tests)
- Enables future swap to a real database without changing service logic
- Prevents implicit coupling between contexts through shared global state

**Consequences:**
- Slightly more boilerplate than direct dict access
- Tests must construct and wire up repository instances manually (acceptable — this is standard pytest practice)
- If a real persistence layer is added later, only the repository implementation changes, not the service

---

## ADR-003: TimelineService Depends Directly on PostRepository and FollowRepository (No Events)

**Status:** Accepted

**Context:**
`TimelineService` needs data from two other bounded contexts: the Social Graph
(to know who a user follows) and Posting (to fetch those users' posts). Options
are: (a) direct in-process calls to the other contexts' repositories, (b) an
in-process event bus, or (c) copying/denormalising data into a dedicated
timeline store.

**Decision:**
`TimelineService` receives `InMemoryFollowRepository` and `InMemoryPostRepository`
as constructor arguments and calls them directly. No event bus is used.

**Rationale:**
- For a kata, synchronous in-process calls are the simplest correct approach
- An event bus would add complexity (event registration, dispatch, ordering) that is not justified at this scale
- The repository interfaces are the stable API boundary; the service does not depend on internal details of the other modules
- A real production system would likely use a pre-computed timeline updated by domain events (`MessagePosted`, `UserFollowed`), but that pattern adds complexity inappropriate for a learning exercise

**Consequences:**
- Timeline reads are O(n) in number of followees — not an issue for a kata
- A future event-driven refactor would introduce `MessagePosted` and `UserFollowed` events and a separate timeline projection store
- Cross-context repository injection must be wired up in the application composition root (or test fixtures)

---

## ADR-004: Use Frozen Dataclasses for Domain Models

**Status:** Accepted

**Context:**
Domain models (`Post`, `DirectMessage`) are value objects created once and
never mutated. We need to decide whether to use plain classes, dicts, named
tuples, or dataclasses.

**Decision:**
Use `@dataclass(frozen=True)` for all domain model classes.

**Rationale:**
- `frozen=True` enforces immutability — stored objects cannot be accidentally mutated by a caller that holds a reference
- Dataclasses provide `__eq__` and `__repr__` for free, which are essential for clean pytest assertions
- More readable than named tuples; no boilerplate like plain classes
- Pythonic and well-understood by Python developers

**Consequences:**
- Objects cannot be updated in place; any "change" requires creating a new instance (intentional for value objects)
- `frozen=True` dataclasses are hashable if all fields are hashable — useful if posts ever need to be stored in sets
