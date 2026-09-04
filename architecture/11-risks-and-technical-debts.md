# Chapter 11: Risks and Technical Debts

## 11.1 Risks

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|-----------|--------|------------|
| R-01 | **Bounded context leakage** — a developer imports an internal model from another module directly instead of going through the service API | Medium | Medium | Code review; `ruff` import rules can be configured to flag cross-context imports |
| R-02 | **Global repository state in tests** — a repository instance is accidentally shared between tests, causing test ordering dependencies | Low | High | Each test (or fixture) constructs fresh repository instances; no module-level singletons |
| R-03 | **Timeline correctness under concurrent writes** — in a real system, two posts arriving simultaneously could produce a non-deterministic order | N/A for kata | High for production | Timestamps + tie-breaking by ID; not relevant while single-threaded |

## 11.2 Technical Debts

| ID | Debt | Impact | Suggested Resolution |
|----|------|--------|---------------------|
| TD-01 | **In-memory storage** — all data is lost when the process exits | Acceptable for kata | Add a `SqlitePostRepository` / `SqliteFollowRepository` implementing the same interface |
| TD-02 | **No input validation on usernames** — any string is accepted as a username, including empty strings | Low for kata | Add a `Username` value object with validation in each context |
| TD-03 | **O(n) timeline reads** — `TimelineService` fetches posts for each followee separately | Acceptable for kata | In production, maintain a pre-computed timeline projection updated by domain events |
| TD-04 | **No pagination** — `wall()` and `timeline()` return all messages | Acceptable for kata | Add `limit`/`offset` parameters to repository `find_by_author` |
| TD-05 | **Direct cross-context repository injection in Timeline** — `TimelineService` holds references to repositories from two other contexts | Acceptable for kata | In a microservices evolution, Timeline would subscribe to `MessagePosted` and `UserFollowed` events and maintain its own projection |
