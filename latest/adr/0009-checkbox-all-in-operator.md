# ADR-0009: "all_in" Operator for Checkbox Filters

**Status:** Proposed  
**Date:** 2026‑01‑14

## Context

Checkbox filters currently support an `any_in` operator, but the `all_in` operator is marked as a future extension【219090252433354†L305-L309】. Users sometimes need to filter records that match all selected values.

## Decision

We propose to implement an `all_in` operator for checkbox filters. When specified, the backend will return records whose associated array field contains all selected options. This feature should be opt‑in per endpoint and documented in the API specification.

## Consequences

- **Enhanced filtering:** Allows more precise queries, improving user productivity.
- **Complex queries:** May require advanced indexing (e.g., GIN indexes in PostgreSQL) to maintain performance.
- **UI updates:** The frontend must allow users to choose between `any` and `all` selection modes where applicable.
