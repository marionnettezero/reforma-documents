# ADR-0013: PDF Template Management and Block Mapping

**Status:** Proposed  
**Date:** 2026‑01‑14

## Context

The notes specification includes `A-03_pdf_block_mapping` and mentions a series of PDF patch files (e.g., `ReForma_追補パッチ_表示モード_テーマ_計算フィールド_v1.0.1.json`) for managing PDF templates and calculation fields【343970276494006†L875-L941】. Current handling of PDF generation and template updates is manual and error‑prone.

## Decision

We propose to introduce a formal PDF template management system. Templates and block mappings will be stored in a version‑controlled repository with metadata (version, effective date, change summary). A management API will allow administrators to upload new templates, map fields, and apply patches. The PDF generation service will reference the latest approved template matching the document type.

## Consequences

- **Consistency:** Centralizes management of PDF templates, reducing inconsistencies across documents.
- **Governance:** Enables clear version history and audit trails for template changes.
- **Implementation effort:** Requires building an upload mechanism, storage for templates, and integration with the existing PDF generation pipeline.
