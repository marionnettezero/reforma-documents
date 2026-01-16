# ADR-0010: Customizable Notification Summary (fields.summary)

**Status:** Proposed  
**Date:** 2026‑01‑14

## Context

In the notification template specification, the `fields.summary` field notes that customizing summary content via form settings is a future extension【219090252433354†L421-L425】. The current implementation auto‑selects major fields.

## Decision

We propose to make the summary section of notifications configurable. Form designers will be able to specify which fields or computed expressions should appear in the notification summary. The rendering engine will fallback to the default behavior if no configuration is provided.

## Consequences

- **Flexibility:** Administrators can tailor notifications to highlight the most relevant information.
- **Complexity:** Requires a schema to store summary configuration and logic to resolve expressions securely.
- **Backward compatibility:** Existing forms without custom configuration should continue to function as before.
