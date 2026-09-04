# Chapter 12: Glossary

| Term | Definition |
|------|-----------|
| **arc42** | A template for software architecture documentation with 12 standardised chapters. Used as the structure for this document. |
| **Bounded Context** | A DDD concept: a cohesive part of the domain with its own ubiquitous language and model. The four bounded contexts here are Posting, Social Graph, Timeline/Feed, and Messaging. |
| **C4 Model** | A set of four hierarchical diagram types (Context, Container, Component, Code) for visualising software architecture. |
| **Conventional Commits** | A commit message specification: `<type>(<scope>): <description>`. Enforced by the `check-commit-msg` pre-commit hook. |
| **Direct Message (DM)** | A private message visible only to the sender and recipient. Handled by the Messaging bounded context. |
| **Dependency Injection** | A pattern where a class receives its dependencies (e.g. repository instances) via constructor arguments rather than creating them internally. Used in all service classes. |
| **Frozen Dataclass** | A Python `@dataclass(frozen=True)` whose fields cannot be mutated after construction. Used for `Post` and `DirectMessage`. |
| **In-memory Repository** | A repository implementation that stores data in Python data structures (dicts/lists) within the process. No persistence beyond process lifetime. |
| **Kata** | A coding exercise practised repeatedly to build skill. This system is a Social Network kata for learning architecture and TDD. |
| **Mention** | A reference to another user in a message using `@username` syntax. Parsed by `MessageParser` and stored in `Post.mentions`. |
| **Modular Monolith** | An application that runs as a single process but is internally divided into distinct modules with explicit boundaries, as opposed to a single-layer monolith or a distributed system. |
| **PlantUML** | A text-based diagramming tool. Architecture diagrams are stored as `.puml` files and rendered to `.svg`. |
| **Repository Pattern** | A design pattern that mediates between the domain and data mapping layers using a collection-like interface. |
| **Timeline / Feed** | An aggregated, chronologically sorted list of posts from all users that a given user follows. |
| **TDD** | Test-Driven Development — a practice of writing failing tests before writing production code. |
| **Wall** | A user's personal list of their own posts, visible to any other user. |
