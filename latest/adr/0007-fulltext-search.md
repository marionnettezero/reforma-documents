# ADR-0007: Full‑Text Search Index

**Status:** Proposed  
**Date:** 2026‑01‑14

## Context

The notes search specification hints at introducing a `FULLTEXT_future` index to enable comprehensive text search across notes【219090252433354†L245-L246】. Currently, search queries rely on simple filters and may not perform well for large text fields.

## Decision

We propose evaluating and adopting a full‑text search engine (e.g., PostgreSQL `tsvector`, ElasticSearch, or MeiliSearch) to index note content and support advanced search features. The chosen engine should integrate with existing persistence layers and permit queries such as phrase search, fuzzy matching, and ranking.

## Consequences

- **Improved UX:** Users will be able to search notes more intuitively and effectively.
- **Operational overhead:** Requires deploying and managing an additional service or enabling database features; may increase infrastructure cost.
- **Migration:** Existing data must be indexed; search API endpoints will need to support new query parameters and return ranked results.
