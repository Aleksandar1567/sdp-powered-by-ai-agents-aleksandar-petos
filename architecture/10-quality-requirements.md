# Chapter 10: Quality Requirements

## 10.1 Quality Tree

The quality goals from Chapter 1 are expanded here into concrete, testable criteria.

| Quality Goal | Scenario | Criterion |
|-------------|----------|-----------|
| **Testability** | Run the full test suite | `pytest` completes with no external services running (no DB, no network). All tests pass in an isolated environment. |
| **Testability** | Test a service in isolation | Each service can be instantiated with a fresh in-memory repository in a single line of test setup. No global state between tests. |
| **Modularity** | Cross-context import check | No module under `posting/` imports from `social_graph/`, `timeline/`, or `messaging/` internals (and vice versa). Only `timeline/` may import repository interfaces from other contexts. |
| **Modularity** | Bounded context independence | Deleting or replacing the `messaging/` module does not require changes in any other module. |
| **Clarity** | Code readability | A developer unfamiliar with the kata can understand the purpose of any module, class, and method without reading tests. Docstrings or clear naming is sufficient. |
| **Simplicity** | Dependency count | Zero runtime dependencies beyond the Python standard library. Dev/test dependencies limited to `pytest`, `black`, `isort`, `ruff`, `pre-commit`. |

## 10.2 Quality Scenarios

### QS-01: Full test suite runs offline
**Stimulus:** Developer runs `pytest` on a machine with no network access.
**Response:** All tests pass. No import errors, no network timeouts.

### QS-02: New bounded context can be added without touching existing modules
**Stimulus:** A new `notifications/` context is added to notify mentioned users.
**Response:** The `notifications/` package is created. The only required change to an existing module is an optional hook in `PostService` (e.g. calling a registered observer), not a structural change to any existing module.

### QS-03: Timeline returns posts in correct chronological order
**Stimulus:** Alice posts at T1, Thomas posts at T2 > T1. Charlie follows both.
**Response:** `TimelineService.timeline("charlie")` returns Thomas's post before Alice's post.
