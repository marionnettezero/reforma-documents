# ADR-0004: System Settings UI and API

**Status:** Proposed  
**Date:** 2026‑01‑14

## Context

The `notes` specification describes a root‑only system settings interface (`SYSTEM_SETTINGS`) and corresponding GET/PUT API endpoints under `/v1/system/settings`【219090252433354†L1286-L1316】. At present, there is no user interface or API implementation; only placeholders exist in the backend spec (`settings.ui: future`)【775654022417029†L315-L318】. A decision is needed on whether and how to implement this feature.

## Decision

We propose to implement a dedicated system‑settings page accessible only to root administrators. This page will allow viewing and editing of global configuration values (e.g., system email templates, feature flags). The corresponding API endpoints (`GET /v1/system/settings` and `PUT /v1/system/settings`) will enforce root authorization and perform validation. RBAC definitions will include a `root` role with exclusive access to these endpoints.

## Consequences

- **Security:** Restricting access to root users reduces the attack surface but requires careful audit logging for changes.
- **UX:** A dedicated UI centralizes configuration management and improves discoverability.
- **Implementation effort:** Requires backend controller, service logic, and a frontend screen; existing specs must be updated to mark this feature as implemented.
