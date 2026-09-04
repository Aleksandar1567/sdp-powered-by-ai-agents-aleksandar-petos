# Chapter 8: Cross-cutting Concepts

## 8.1 Authentication and Authorisation

**Not applicable for this kata.**

Usernames are plain strings passed as function arguments. There is no login,
no session, no token, and no access control. Any caller can read any user's
wall or send a message as any user. This is intentional — the kata focuses on
domain logic, not security infrastructure.

> If this kata were extended to a real system, authentication would sit at the
> boundary of the system (e.g. an API Gateway + JWT) and would not need to
> penetrate into the domain modules.

---

## 8.2 Error Handling

Errors are raised as plain Python exceptions. Each service raises domain-specific
exceptions for invalid operations:

| Exception | Raised by | Condition |
|-----------|-----------|-----------|
| `ValueError` | `PostService` | Empty message text |
| `ValueError` | `FollowService` | A user attempts to follow themselves |
| `ValueError` | `DirectMessageService` | Empty message text or sender equals recipient |

There is no global exception handler. Tests assert that the correct exception
type and message are raised.

---

## 8.3 Logging

No logging framework is used in the kata. Output, if any, goes to `stdout` via
`print()` during manual exploration. Tests produce no output on success.

> In a production extension, structured logging (e.g. `structlog`) would be
> injected into services as a dependency, keeping the domain models free of
> logging concerns.

---

## 8.4 Identifiers

Every `Post` and `DirectMessage` is assigned a unique `id` on creation using
`uuid.uuid4()` (converted to string). This keeps IDs unique across a process
lifetime without requiring a database sequence.

---

## 8.5 Timestamps

`datetime.utcnow()` (or `datetime.now(UTC)` for Python 3.11+) is used to stamp
`Post` and `DirectMessage` objects at creation time. The `TimelineService` sorts
by timestamp descending. Tests that care about ordering should create messages
with explicit timestamps rather than relying on wall-clock timing.

---

## 8.6 Domain Model Immutability

`Post` and `DirectMessage` are `@dataclass(frozen=True)`. Once created, they
cannot be mutated. This simplifies reasoning in tests and prevents accidental
in-place modification of stored objects.
