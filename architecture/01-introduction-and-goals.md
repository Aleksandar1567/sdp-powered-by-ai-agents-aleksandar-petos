# Chapter 1: Introduction and Goals

## 1.1 Purpose of This Document

This document describes the architecture of the **Social Network kata** — a
learning exercise in software architecture and test-driven development (TDD).
It is structured according to the [arc42 template](https://arc42.org) and uses
the [C4 model](https://c4model.com) for all architecture diagrams.

The goal is not to produce a production-ready system, but to practise
identifying bounded contexts, drawing clean module boundaries, and designing a
system that is easy to understand and test.

---

## 1.2 Requirements Overview

The system must support the following user-facing capabilities:

| ID  | Capability | Example |
|-----|-----------|---------|
| F-01 | **Post messages** — a user can publish a short text message. | Thomas posts "Hello, world!" |
| F-02 | **Read messages** — a user can view another user's message wall. | Alice reads Thomas's messages. |
| F-03 | **Follow users** — a user can follow one or more other users. | Charlie follows Thomas and Alice. |
| F-04 | **Aggregated timeline** — a user sees a merged feed of all messages from the users they follow, ordered by time. | Charlie views a timeline that interleaves Thomas's and Alice's posts. |
| F-05 | **Mention users** — a message may mention another user with `@username` syntax. Mentions are parsed and stored. | Thomas posts "Hey @alice, check this out!" |
| F-06 | **Share links** — a message may contain URLs. Links are extracted and stored alongside the message. | Thomas posts "Read this: https://example.com" |
| F-07 | **Private direct messages** — two users can exchange private messages that are not visible on any public wall or timeline. | Alice sends Thomas a private message. |

---

## 1.3 Quality Goals

The top quality goals for this kata (ordered by priority):

| Priority | Quality Goal | Motivation |
|----------|-------------|-----------|
| 1 | **Testability** | Every use case must be exercisable via pytest without external dependencies (no database, no network). This is a TDD exercise first and foremost. |
| 2 | **Modularity** | Each bounded context lives in its own Python module with an explicit public API. No cross-context internal coupling. |
| 3 | **Clarity** | The codebase should be a readable, teachable example of domain-driven design and clean architecture in Python. |
| 4 | **Simplicity** | Avoid over-engineering. In-memory repositories are intentional. No frameworks, no ORMs, no async unless needed. |

---

## 1.4 Stakeholders

| Role | Concern |
|------|---------|
| **Learner / Developer** (primary) | Understands how to decompose a system into bounded contexts and implement them with TDD. |
| **Code Reviewer / Mentor** | Can evaluate whether the kata correctly applies DDD, clean module boundaries, and arc42 documentation. |
| **Thomas** *(example actor)* | Can post messages that others read; his messages may contain links and mentions. |
| **Alice** *(example actor)* | Can read other users' walls, receive direct messages, and be mentioned. |
| **Charlie** *(example actor)* | Follows multiple users and consumes an aggregated timeline feed. |
