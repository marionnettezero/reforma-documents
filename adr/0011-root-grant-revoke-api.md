# ADR-0011: Root Grant/Revoke API Endpoints

**Status:** Proposed  
**Date:** 2026‑01‑14

## Context

The notes specification lists `root_grant_revoke` and `rbac_master_change` API endpoints as `not_provided_v1`【219090252433354†L1389-L1394】. As multiple root accounts are considered (see ADR‑0006), an API for granting and revoking root privileges will eventually be required.

## Decision

We propose to design and implement RESTful endpoints (`POST /v1/system/root/grant` and `POST /v1/system/root/revoke`) that allow an existing root administrator to grant or revoke root status to another user. Access to these endpoints will be protected by an out‑of‑band authentication mechanism and audited. The API will validate that the requesting user is root and that the target account exists.

## Consequences

- **Auditability:** All root privilege changes will be logged for compliance.
- **Risk management:** Improper use could lead to privilege escalation; therefore, strict policies and periodic reviews are essential.
- **Dependency:** Requires the multiple root policy (ADR‑0006) to be adopted first.
