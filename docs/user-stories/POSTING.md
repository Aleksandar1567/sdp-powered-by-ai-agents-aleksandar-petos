# POSTING Domain — User Story Bundles

---

## POSTING-STORY-001: Post a Message

**AS A** registered user
**I WANT** to publish a short text message under my username
**SO THAT** my message is stored and can be read by other users on my wall

**Priority:** Core (Pareto 20%)

**Architecture Reference:** `05-building-block-view.md §5.2` · `06-runtime-view.md §6.1`

---

### Scenarios

#### POSTING-STORY-001-S1: Successfully post a plain-text message

**GIVEN**
- A `PostService` instance wired with a fresh `InMemoryPostRepository`
- A user identified by the username `"thomas"`
- A non-empty text `"Hello, world!"`

**WHEN**
- `PostService.post("thomas", "Hello, world!")` is called

**THEN**
- A `Post` object is returned
- `post.author == "thomas"`
- `post.text == "Hello, world!"`
- `post.id` is a non-empty string (UUID)
- `post.timestamp` is set to a recent UTC datetime
- `post.mentions == []`
- `post.links == []`
- The repository contains exactly one post for `"thomas"`

#### POSTING-STORY-001-S2: Post is immutable after creation

**GIVEN**
- A `Post` returned by `PostService.post("thomas", "Hello")`

**WHEN**
- An attempt is made to mutate any field (e.g. `post.text = "changed"`)

**THEN**
- A `FrozenInstanceError` (or equivalent `dataclasses` exception) is raised
- The stored post in the repository is unchanged

#### POSTING-STORY-001-S3: Multiple posts by the same user are all stored

**GIVEN**
- A `PostService` instance with a fresh repository
- User `"thomas"` has already posted `"First post"`

**WHEN**
- `PostService.post("thomas", "Second post")` is called

**THEN**
- The repository contains two posts for `"thomas"`
- Both posts are retrievable and have distinct `id` values

---

## Backend Sub-Stories

### POSTING-BE-001.1: Implement `PostService.post()` with `MessageParser` and `InMemoryPostRepository`

**AS A** backend developer
**I WANT** `PostService.post(author, text)` to parse the text, create a frozen `Post` dataclass, persist it, and return it
**SO THAT** domain logic, parsing, and storage are each in a single, independently testable unit

**Architecture Reference:** `05-building-block-view.md §5.2` · `06-runtime-view.md §6.1`

#### POSTING-BE-001.1-S1: `PostService.post()` delegates parsing to `MessageParser`

**GIVEN**
- `MessageParser` is a pure utility (no state)
- `PostService` is constructed with an `InMemoryPostRepository`

**WHEN**
- `PostService.post("thomas", "Hey @alice see https://example.com")` is called

**THEN**
- `MessageParser.parse()` is invoked exactly once with `"Hey @alice see https://example.com"`
- The returned `Post.mentions` equals `["alice"]`
- The returned `Post.links` equals `["https://example.com"]`

#### POSTING-BE-001.1-S2: `Post` is assigned a unique UUID on each call

**GIVEN**
- A `PostService` with a fresh repository

**WHEN**
- `PostService.post("thomas", "A")` is called twice

**THEN**
- The two returned `Post` objects have different `id` values
- Both IDs are valid UUID strings (`uuid.UUID(post.id)` does not raise)

#### POSTING-BE-001.1-S3: `PostService.post()` saves the post to the repository

**GIVEN**
- A `PostService` with a fresh `InMemoryPostRepository`

**WHEN**
- `PostService.post("thomas", "Hello")` is called

**THEN**
- `InMemoryPostRepository.find_by_author("thomas")` returns a list containing exactly the returned post

---

### POSTING-BE-001.2: Implement `InMemoryPostRepository` with keyed storage

**AS A** backend developer
**I WANT** `InMemoryPostRepository` to store `Post` objects in a `dict[str, list[Post]]` keyed by author
**SO THAT** posts can be retrieved efficiently by author without a database

**Architecture Reference:** `05-building-block-view.md §5.2`

#### POSTING-BE-001.2-S1: `save()` appends to the author's list

**GIVEN**
- A fresh `InMemoryPostRepository`
- A `Post` with `author="thomas"`

**WHEN**
- `repository.save(post)` is called

**THEN**
- `repository.find_by_author("thomas")` returns `[post]`

#### POSTING-BE-001.2-S2: `find_by_author()` returns empty list for unknown author

**GIVEN**
- A fresh `InMemoryPostRepository` with no saved posts

**WHEN**
- `repository.find_by_author("nobody")` is called

**THEN**
- An empty list `[]` is returned (no `KeyError` raised)

#### POSTING-BE-001.2-S3: Repositories are independent between test instances

**GIVEN**
- Two separately constructed `InMemoryPostRepository` instances

**WHEN**
- A post is saved in the first instance

**THEN**
- The second instance's `find_by_author()` returns `[]` — no shared state

---

### POSTING-BE-001.3: Implement `MessageParser` for mentions and URLs

**AS A** backend developer
**I WANT** `MessageParser.parse(text)` to return all `@mention` usernames and all URLs found in the text
**SO THAT** post enrichment (mentions, links) is handled by a single, pure, unit-testable function

**Architecture Reference:** `05-building-block-view.md §5.2`

#### POSTING-BE-001.3-S1: Parser extracts `@mention` usernames

**GIVEN**
- Raw text `"Hey @alice and @bob!"`

**WHEN**
- `MessageParser.parse("Hey @alice and @bob!")` is called

**THEN**
- `result.mentions == ["alice", "bob"]` (in order of appearance)
- `result.links == []`

#### POSTING-BE-001.3-S2: Parser extracts URLs

**GIVEN**
- Raw text `"Read this: https://example.com and http://foo.org"`

**WHEN**
- `MessageParser.parse(...)` is called

**THEN**
- `result.links == ["https://example.com", "http://foo.org"]`
- `result.mentions == []`

#### POSTING-BE-001.3-S3: Parser is pure — same input always produces same output

**GIVEN**
- The same text `"Hello @alice https://x.com"` is passed twice

**WHEN**
- `MessageParser.parse()` is called twice

**THEN**
- Both calls return identical `mentions` and `links` lists
- No internal state changes between calls

---

## Frontend Sub-Stories

> Not applicable. The architecture defines no UI or HTTP API surface — the system
> is a single-process Python kata consumed directly via Python function calls in
> tests and a REPL (`03-context-and-scope.md §3.3`).

---

## Infrastructure Sub-Stories

### POSTING-INFRA-001.1: Module and package structure for the Posting bounded context

**AS A** developer setting up the project
**I WANT** the `posting/` package to contain `models.py`, `parser.py`, `repository.py`, and `service.py` with correct `__init__.py` exports
**SO THAT** the public API (`PostService`, `InMemoryPostRepository`, `Post`) is importable from `social_network.posting` without exposing internals

**Architecture Reference:** `04-solution-strategy.md §4.3` · `07-deployment-view.md §7.1`

#### POSTING-INFRA-001.1-S1: Package is importable as `social_network.posting`

**GIVEN**
- The repository is checked out and `pre-commit install` has been run

**WHEN**
- A Python interpreter runs `from social_network.posting import PostService, InMemoryPostRepository, Post`

**THEN**
- No `ImportError` or `ModuleNotFoundError` is raised
- All three names are bound to their respective classes

#### POSTING-INFRA-001.1-S2: Posting internals are not reachable from sibling modules

**GIVEN**
- The `social_graph/`, `timeline/`, and `messaging/` packages exist

**WHEN**
- `ruff` import-order checks run (or a manual import audit is performed)

**THEN**
- No file under `social_graph/`, `timeline/`, or `messaging/` imports from `social_network.posting` internal modules (only the public API imports are allowed in `timeline/`)
- Consistent with `10-quality-requirements.md §10.1` modularity criterion

---

### POSTING-INFRA-001.2: In-memory repository wiring via dependency injection in test fixtures

**AS A** developer writing tests
**I WANT** each test to construct its own `InMemoryPostRepository` and inject it into `PostService`
**SO THAT** tests are fully isolated — no shared global state between test runs

**Architecture Reference:** `04-solution-strategy.md §4.1` · `09-architecture-decisions.md §ADR-002` · `11-risks-and-technical-debts.md §11.1 R-02`

#### POSTING-INFRA-001.2-S1: Fresh repository per test

**GIVEN**
- A pytest test function that constructs `repo = InMemoryPostRepository()` and `service = PostService(repo)`

**WHEN**
- The test runs `service.post("thomas", "Hello")` and a second test runs independently

**THEN**
- Each test starts with zero posts in its repository
- Running `pytest` repeatedly produces the same results regardless of execution order

#### POSTING-INFRA-001.2-S2: pytest fixture provides pre-wired `PostService`

**GIVEN**
- A shared `@pytest.fixture` named `post_service` in `conftest.py` that returns `PostService(InMemoryPostRepository())`

**WHEN**
- Multiple test functions declare `post_service` as a parameter

**THEN**
- Each invocation receives a separate instance (fixture scope is `"function"`, the pytest default)
- No post created in one test is visible in another

---

### POSTING-INFRA-001.3: Observability — logging and test output for the Posting module

**AS A** developer debugging a failing test or exploring the kata
**I WANT** key operations (post creation) to emit a structured log record (or at minimum a `print` statement) with `author`, `post_id`, and `timestamp`
**SO THAT** I can trace the flow during manual REPL exploration without a debugger

**Architecture Reference:** `08-cross-cutting-concepts.md §8.3`

> **Events sub-story:** Not applicable. The architecture explicitly uses synchronous
> in-process calls with no event bus (`04-solution-strategy.md §4.1`,
> `09-architecture-decisions.md §ADR-003`). There are no asynchronous events to
> produce or consume in the Posting bounded context.

#### POSTING-INFRA-001.3-S1: Post creation is traceable via stdout during REPL use

**GIVEN**
- `PostService` is instantiated and used from a Python REPL or `python -m social_network` script

**WHEN**
- `PostService.post("thomas", "Hello")` is called

**THEN**
- A line is printed to `stdout` containing at minimum the `author` and `post_id`
- When the same call is made inside a `pytest` test, no output appears on success (consistent with `08-cross-cutting-concepts.md §8.3`: "Tests produce no output on success")

---

## Traceability Verification

| Scenario ID | Architecture Reference | Parent Story | Testable Assertion (THEN) |
|---|---|---|---|
| POSTING-STORY-001-S1 | `05-building-block-view.md §5.2`, `06-runtime-view.md §6.1` | POSTING-STORY-001 | `PostService.post()` returns a `Post` with correct author, text, empty mentions/links, non-empty id and timestamp |
| POSTING-STORY-001-S2 | `05-building-block-view.md §5.2`, `09-architecture-decisions.md §ADR-004` | POSTING-STORY-001 | Mutating a field on a returned `Post` raises `FrozenInstanceError` |
| POSTING-STORY-001-S3 | `05-building-block-view.md §5.2` | POSTING-STORY-001 | Repository holds two posts with distinct IDs after two `post()` calls |
| POSTING-BE-001.1-S1 | `05-building-block-view.md §5.2`, `06-runtime-view.md §6.1` | POSTING-STORY-001 | `MessageParser.parse()` called once; returned `Post` has correct `mentions` and `links` |
| POSTING-BE-001.1-S2 | `05-building-block-view.md §5.2`, `08-cross-cutting-concepts.md §8.4` | POSTING-STORY-001 | Two posts have different UUIDs, both valid |
| POSTING-BE-001.1-S3 | `05-building-block-view.md §5.2`, `09-architecture-decisions.md §ADR-002` | POSTING-STORY-001 | `find_by_author("thomas")` returns the saved post after `post()` |
| POSTING-BE-001.2-S1 | `05-building-block-view.md §5.2` | POSTING-STORY-001 | `find_by_author()` returns `[post]` after `save(post)` |
| POSTING-BE-001.2-S2 | `05-building-block-view.md §5.2` | POSTING-STORY-001 | `find_by_author("nobody")` returns `[]` with no exception |
| POSTING-BE-001.2-S3 | `09-architecture-decisions.md §ADR-002`, `11-risks-and-technical-debts.md §11.1 R-02` | POSTING-STORY-001 | Two repository instances have independent state |
| POSTING-BE-001.3-S1 | `05-building-block-view.md §5.2` | POSTING-STORY-001 | `parse("Hey @alice and @bob!")` returns `mentions=["alice","bob"]`, `links=[]` |
| POSTING-BE-001.3-S2 | `05-building-block-view.md §5.2` | POSTING-STORY-001 | `parse("Read this: https://example.com …")` returns correct `links` list |
| POSTING-BE-001.3-S3 | `05-building-block-view.md §5.2` | POSTING-STORY-001 | Two calls with identical input produce identical output |
| POSTING-INFRA-001.1-S1 | `04-solution-strategy.md §4.3`, `07-deployment-view.md §7.1` | POSTING-STORY-001 | `from social_network.posting import PostService` succeeds |
| POSTING-INFRA-001.1-S2 | `10-quality-requirements.md §10.1` | POSTING-STORY-001 | No cross-context internal import found by lint/audit |
| POSTING-INFRA-001.2-S1 | `09-architecture-decisions.md §ADR-002`, `11-risks-and-technical-debts.md §11.1 R-02` | POSTING-STORY-001 | Test isolation verified by running in reverse order |
| POSTING-INFRA-001.2-S2 | `09-architecture-decisions.md §ADR-002` | POSTING-STORY-001 | Each test invocation of the `post_service` fixture gets a separate instance |
| POSTING-INFRA-001.3-S1 | `08-cross-cutting-concepts.md §8.3` | POSTING-STORY-001 | `stdout` contains `author` and `post_id` after `post()` call in REPL; pytest produces no output on success |
