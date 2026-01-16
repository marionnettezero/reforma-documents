# ADR-0012: Finalization of OpenAPI v1.1 Specification

**Status:** Proposed  
**Date:** 2026‑01‑14

## Context

The API section notes that the current OpenAPI v1.1 draft lacks certain parameters and that these will be supplemented in the final specification【343970276494006†L6482-L6484】. Without a finalized specification, API consumers cannot fully rely on the contract.

## Decision

We propose to audit all existing endpoints against the implementation, identify missing request and response parameters, and update the OpenAPI v1.1 specification accordingly. The finalized document will be versioned and published alongside the canonical spec. Any breaking changes will be communicated via a deprecation policy.

## Consequences

- **Clarity:** API consumers will have a complete and accurate contract, reducing integration errors.
- **Maintenance:** Requires ongoing synchronization between code and specification; a linting step should be added to CI.
- **Backward compatibility:** Newly added parameters may require clients to update; a migration plan should be provided.
