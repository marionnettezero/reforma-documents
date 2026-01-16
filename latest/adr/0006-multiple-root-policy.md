# ADR-0006: Multiple Root User Policy

**Status:** Proposed  
**Date:** 2026‑01‑14

## Context

Within the notes specification, the `root_admin` section outlines a future policy that allows multiple root users and indicates that grants should occur only via operational tooling【219090252433354†L1274-L1277】. Today, the system supports a single root user.

## Decision

We propose to support multiple root accounts in order to reduce operational bottlenecks and single points of failure. Root accounts will be granted or revoked exclusively through a secured operational CLI or administration API; there will be no UI for self‑provisioning. Audit logs must record all root grants and revocations. Documentation must be updated to reflect the implications of multiple root users.

## Consequences

- **Security:** Increases the risk of privilege misuse if not tightly controlled; strict audit and periodic review of root accounts will be required.
- **Redundancy:** Removes dependence on a single root user, improving resilience.
- **Implementation:** Requires schema changes to support multiple root flags and updates to RBAC checks across the application.
