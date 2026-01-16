# ADR-0005: Role Permission Assignment UI and API

**Status:** Proposed  
**Date:** 2026‑01‑14

## Context

The notes specification also describes a root‑only `ROLE_PERMISSION_ASSIGN` screen and corresponding API endpoints for assigning permissions to roles【219090252433354†L1286-L1316】. Currently, there is no UI or API implementation.

## Decision

We propose to build a role‑permission assignment interface where root administrators can view existing roles, assign or revoke permissions, and create new roles. The backend will expose `GET /v1/system/roles/permissions` and `PUT /v1/system/roles/permissions` endpoints guarded by root authentication. Changes will update the underlying RBAC policy store.

## Consequences

- **RBAC clarity:** Centralizing role management simplifies administration and reduces misconfiguration.
- **Complexity:** Requires careful validation to avoid privilege escalation and consistency with existing authorization logic.
- **Testing:** Comprehensive integration tests will be necessary to ensure roles map correctly to permissions.
