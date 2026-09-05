# User Stories — Social Network Kata

## Bounded Contexts (Domains)

| Domain Token | Bounded Context | Architecture Reference |
|---|---|---|
| `POSTING` | Posting | `05-building-block-view.md §5.2` |
| `SOCIALGRAPH` | Social Graph | `05-building-block-view.md §5.3` |
| `TIMELINE` | Timeline/Feed | `05-building-block-view.md §5.4` |
| `MESSAGING` | Messaging | `05-building-block-view.md §5.5` |

---

## Story Inventory with Pareto Classification

> **Pareto note:** This is a 7-capability kata. A strict 20% would be 1–2 stories,
> which would leave core integration flows untested. The Core set is therefore
> 4 out of 11 stories (~36%) — the threshold where removing any one of them
> breaks at least one other story or eliminates a headline capability end-to-end.
> The remaining 7 stories are Supporting.

| # | Story ID | Title | Domain | Priority | Status |
|---|---|---|---|---|---|
| 1 | [POSTING-STORY-001](./POSTING.md#posting-story-001-post-a-message) | Post a Message | POSTING | **Core** | ✅ Written |
| 2 | [POSTING-STORY-002](./POSTING.md#posting-story-002-read-a-users-wall) | Read a User's Wall | POSTING | **Core** | ⬜ Pending |
| 3 | [SOCIALGRAPH-STORY-001](./SOCIALGRAPH.md#socialgraph-story-001-follow-a-user) | Follow a User | SOCIALGRAPH | **Core** | ⬜ Pending |
| 4 | [TIMELINE-STORY-001](./TIMELINE.md#timeline-story-001-view-aggregated-timeline) | View Aggregated Timeline | TIMELINE | **Core** | ⬜ Pending |
| 5 | [POSTING-STORY-003](./POSTING.md#posting-story-003-mention-a-user-in-a-post) | Mention a User in a Post | POSTING | Supporting | ⬜ Pending |
| 6 | [POSTING-STORY-004](./POSTING.md#posting-story-004-share-a-link-in-a-post) | Share a Link in a Post | POSTING | Supporting | ⬜ Pending |
| 7 | [SOCIALGRAPH-STORY-002](./SOCIALGRAPH.md#socialgraph-story-002-unfollow-a-user) | Unfollow a User | SOCIALGRAPH | Supporting | ⬜ Pending |
| 8 | [SOCIALGRAPH-STORY-003](./SOCIALGRAPH.md#socialgraph-story-003-list-followed-users) | List Followed Users | SOCIALGRAPH | Supporting | ⬜ Pending |
| 9 | [MESSAGING-STORY-001](./MESSAGING.md#messaging-story-001-send-a-private-direct-message) | Send a Private Direct Message | MESSAGING | Supporting | ⬜ Pending |
| 10 | [MESSAGING-STORY-002](./MESSAGING.md#messaging-story-002-read-a-conversation-thread) | Read a Conversation Thread | MESSAGING | Supporting | ⬜ Pending |
| 11 | [POSTING-STORY-005](./POSTING.md#posting-story-005-reject-empty-post) | Reject Empty Post | POSTING | Supporting | ⬜ Pending |

---

## Pareto Rationale

### Core stories (4 / 11 = 36%)

| Story | Pareto Rule Triggered |
|---|---|
| POSTING-STORY-001 | **Blocks all other stories** — every other story depends on posts existing in the repository. |
| POSTING-STORY-002 | **MVP-critical** — reading a wall is the primary consumption path for posts; without it F-02 is missing end-to-end. |
| SOCIALGRAPH-STORY-001 | **Blocks TIMELINE-STORY-001** — a timeline cannot be built without a follow relationship. |
| TIMELINE-STORY-001 | **Cross-component reach** — exercises Posting + Social Graph + Timeline together (F-04); validates the cross-context dependency-injection wiring. |

### Supporting stories (7 / 11 = 64%)

Mentions, links, unfollow, list-following, direct messages, conversation retrieval, and error guard-rails are all valuable but can be built and tested independently after the four Core stories are green.

---

## Progress Tracker

| Story ID | Bundle Written | Approved |
|---|---|---|
| POSTING-STORY-001 | ✅ | ✅ |
| POSTING-STORY-002 | ⬜ | ⬜ |
| SOCIALGRAPH-STORY-001 | ⬜ | ⬜ |
| TIMELINE-STORY-001 | ⬜ | ⬜ |
| POSTING-STORY-003 | ⬜ | ⬜ |
| POSTING-STORY-004 | ⬜ | ⬜ |
| SOCIALGRAPH-STORY-002 | ⬜ | ⬜ |
| SOCIALGRAPH-STORY-003 | ⬜ | ⬜ |
| MESSAGING-STORY-001 | ⬜ | ⬜ |
| MESSAGING-STORY-002 | ⬜ | ⬜ |
| POSTING-STORY-005 | ⬜ | ⬜ |
