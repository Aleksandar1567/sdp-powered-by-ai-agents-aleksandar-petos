# Chapter 4: Solution Strategy

## 4.1 Fundamental Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Architecture style** | Modular monolith | Single Python process. Each bounded context is a package with a clear public API. No distributed system complexity needed for a kata. |
| **Decomposition strategy** | Domain-Driven Design — bounded contexts | The four domains (Posting, Social Graph, Timeline/Feed, Messaging) have distinct responsibilities and distinct models. They communicate through explicit service interfaces, not shared data structures. |
| **Persistence** | In-memory repositories | Data structures are plain Python dicts/lists inside repository classes. The repository pattern is used so the storage strategy could be swapped later without touching domain logic. |
| **Inter-context communication** | Direct in-process calls via injected dependencies | `TimelineService` receives `FollowRepository` and `PostRepository` as constructor arguments. No events, no shared globals. This is the simplest correct approach for a kata. |
| **Testing** | Pytest, test-first (TDD) | Tests are written before production code. Each bounded context has its own test module. No mocking frameworks — in-memory repositories serve as test doubles. |

## 4.2 Achieving the Quality Goals

| Quality Goal | Strategy |
|-------------|----------|
| **Testability** | Repository pattern with in-memory implementations means tests never need a database or network. Dependency injection allows testing services in isolation. |
| **Modularity** | Each bounded context is a Python package (`posting/`, `social_graph/`, `timeline/`, `messaging/`). Cross-context access is only permitted through the other module's public service class or repository interface — never by importing internal models directly. |
| **Clarity** | Dataclasses for domain models, plain classes for services and repositories. No magic, no metaclasses, no decorators beyond `@dataclass`. |
| **Simplicity** | No framework. No async. No events for a kata of this scale. The simplest solution that fulfils the functional requirements and quality goals is preferred. |

## 4.3 Module Responsibilities

```
social_network/
├── posting/          # F-01, F-02, F-05, F-06
│   ├── models.py     # Post dataclass
│   ├── parser.py     # MessageParser (regex for mentions + URLs)
│   ├── repository.py # InMemoryPostRepository
│   └── service.py    # PostService
├── social_graph/     # F-03
│   ├── repository.py # InMemoryFollowRepository
│   └── service.py    # FollowService
├── timeline/         # F-04
│   └── service.py    # TimelineService (depends on PostRepo + FollowRepo)
└── messaging/        # F-07
    ├── models.py     # DirectMessage dataclass
    ├── repository.py # InMemoryDirectMessageRepository
    └── service.py    # DirectMessageService
```
