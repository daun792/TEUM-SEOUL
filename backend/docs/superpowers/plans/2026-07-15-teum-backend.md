# TEUM SEOUL Backend Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the WBS backend scope for TourAPI data, festival APIs, nearby-place distance queries, and anonymous board CRUD.

**Architecture:** FastAPI routers use SQLAlchemy sessions and SQLite models. Pydantic validates TourAPI files before idempotent upsert. Passwords are stored as PBKDF2-SHA256 hashes.

**Tech Stack:** Python 3.12, FastAPI, SQLAlchemy 2, Pydantic 2, SQLite, pytest

## Global Constraints

- Backend only; no Vue or chatbot implementation.
- Preserve frontend-compatible festival aliases such as `id`, `name`, `lat`, `lng`, and `period`.
- Import 서울 data by `contentid` without duplicate rows.

---

### Task 1: TourAPI validation and import
- [x] Write failing coordinate/date validation tests.
- [x] Implement Pydantic source models and directory discovery.
- [x] Implement idempotent SQLAlchemy upsert.
- [x] Verify 6,518 서울 rows import and second import updates without duplicates.

### Task 2: Festival and nearby APIs
- [x] Write failing list/detail/nearby tests.
- [x] Implement date/keyword pagination filters.
- [x] Implement bounding-box candidate query and Haversine distance sorting.
- [x] Verify against imported 서울 dataset.

### Task 3: Anonymous post APIs
- [x] Write failing CRUD/password/search/pagination tests.
- [x] Implement PBKDF2-SHA256 password hashing.
- [x] Implement list/detail/create/update/delete/password verification endpoints.
- [x] Verify all tests pass.

### Task 4: Operations and documentation
- [x] Add `.env.example`, requirements, Render blueprint, health endpoint, README, API contract.
- [x] Generate OpenAPI document.
- [x] Run compile and test verification.
