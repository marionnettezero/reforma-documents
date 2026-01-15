# ADR-0008: JSON Field Storage for Multi‑Value Attributes

**Status:** Proposed  
**Date:** 2026‑01‑14

## Context

The notes specification suggests using `consider_json_storage_future` for fields that store multiple values, such as checkbox selections【219090252433354†L290-L293】. At present, such values are stored in normalized relational tables, which complicates queries like “all values present”.

## Decision

We propose to store multi‑value attributes in JSON or array columns (depending on the underlying database) to simplify storage and retrieval. Query operators (`any_in`, `all_in`) will operate directly on these JSON fields. The API layer will abstract the storage mechanism from clients.

## Consequences

- **Simpler schema:** Reduces join complexity and improves read performance for multi‑value fields.
- **Query complexity:** Requires careful indexing and operator support to maintain performance, especially for `all_in` queries.
- **Migration:** Existing data must be migrated to the new format without data loss.
