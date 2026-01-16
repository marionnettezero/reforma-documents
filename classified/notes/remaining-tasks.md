# ReForma Remaining Tasks List

**Created**: 2026-01-31  
**Base**: Comparison of reforma-notes-v1.1.0.md content with implementation status

---

## Implemented Features

✅ **Attachment Features**
- PDF template upload and management
- Uploaded file management
- PDF generation (pdf_block_key, pdf_page_number support, multi-page support)

✅ **Notification Features**
- User notifications (email sending, CC/BCC support)
- Admin notifications (multiple admin selection)
- Email template variable expansion
- Asynchronous sending via queue processing

✅ **Period Check Features**
- Public period check (public_period_start, public_period_end)
- Answer period check (answer_period_start, answer_period_end)

✅ **Settings Management**
- Settings table and model implementation
- SettingsService implementation
- Settings API (GET/PUT /v1/system/settings)

✅ **Root-only Features**
- Root-only middleware implementation
- Root-only API protection

✅ **CSV Export Base**
- CSV export job start API
- Progress management functionality

✅ **Search Base**
- Cross-cutting search API (users, logs)

---

## Unimplemented / Required Tasks

### 1. A-01: Complete CSV Export Implementation
**Current Status**: Only empty CSV generation  
**Required Implementation**:
- value/label/both mode support
- Common column definitions (submission_id, submitted_at, form_code, status)
- Field column naming rules (f:{field_key}, f:{field_key}__label)
- Value/label conversion rules by field type
- UTF-8 BOM support (already implemented)
- RFC4180-compliant escape processing

**Reference**: reforma-notes-v1.1.0.md A-01_csv_column_definition

---

### 2. A-02: Complete Search Implementation (Submissions Search)
**Current Status**: Only cross-cutting search (admin_user, log)  
**Required Implementation**:
- Submissions/Responses search functionality
- Search operators by field type:
  - text/textarea/email/tel: contains
  - number: eq, min, max, between
  - date/datetime: from, to, between
  - select/radio: eq, in
  - checkbox: any_in (default), all_in (optional)
  - terms: eq
- AND combination of search conditions (default)
- Index optimization (field_id, value)

**Reference**: reforma-notes-v1.1.0.md A-02_search_rule_matrix

---

### 3. A-05: Notification Resend Feature
**Current Status**: Not implemented  
**Required Implementation**:
- Notification resend API triggerable by system_admin
- Asynchronous sending via queue processing
- Audit log recording (admin_audit_logs)

**Reference**: reforma-notes-v1.1.0.md A-05_examples.notification_resend_example

---

### 4. A-05: PDF Regeneration Feature
**Current Status**: Not implemented  
**Required Implementation**:
- Default regeneration forbidden (409 error)
- Explicit operation only allowed by system_admin or root-only
- Audit log recording
- Asynchronous processing (queue)

**Reference**: reforma-notes-v1.1.0.md A-05_examples.pdf_regeneration_example

---

### 5. A-06: Condition Branch Evaluation Feature
**Current Status**: Not implemented  
**Required Implementation**:
- ConditionEvaluator service implementation
- Evaluation of visibility_rule, required_rule, step_transition_rule
- ConditionState response generation (FieldConditionState, StepTransitionState)
- Safe-side fallback (hide/not_required/deny_transition on evaluation failure)
- Maximum nesting limit of 1 level
- Evaluation on public form GET, submit, step transition

**Reference**: 
- reforma-notes-v1.1.0.md A-06_condition_branch_rules
- reforma-notes-v1.1.0.md API 評価フロー
- reforma-notes-v1.1.0.md reforma-notes-v1.0.0-条件分岐-評価結果IF-.json

---

### 6. SUPP-DISPLAY-MODE-001: Display Mode Feature
**Current Status**: Not implemented  
**Required Implementation**:
- Add label_json, field_label_snapshot columns to submission_values table
- Add locale, mode parameters to POST /v1/forms/{form_key}/submit
- Support for label/both/value modes
- Canonical storage is value, label is snapshot
- Mode specification support for CSV export

**Reference**: reforma-notes-v1.1.0.md reforma-notes-v1.0.0-追補パッチ-表示モード-テーマ-計算フィールド-.json SUPP-DISPLAY-MODE-001

---

### 7. SUPP-THEME-001: Theme Feature
**Current Status**: Not implemented  
**Required Implementation**:
- Add theme_id, theme_tokens columns to forms table
- Add theme_id, theme_tokens to GET /v1/forms/{id} response
- Add theme_id, theme_tokens to PUT /v1/forms/{id} request
- Theme token schema definition (color_primary, color_secondary, etc.)
- External CSS URL to be considered in v2 (not provided in v1.x)

**Reference**: reforma-notes-v1.1.0.md reforma-notes-v1.0.0-追補パッチ-表示モード-テーマ-計算フィールド-.json SUPP-THEME-001

---

### 8. SUPP-COMPUTED-001: Computed Field Feature
**Current Status**: Not implemented  
**Required Implementation**:
- Add computed_rule column (JSON) to form_fields table
- Definition of computed type fields
- built_in_functions implementation (sum, multiply, tax, round, min, max, if)
- ComputedEvaluator service implementation
- Cycle detection (max_dependency_depth=1)
- API recomputation on submit (do not trust client-sent values)
- Blank display and do_not_store on error

**Reference**: reforma-notes-v1.1.0.md reforma-notes-v1.0.0-追補パッチ-表示モード-テーマ-計算フィールド-.json SUPP-COMPUTED-001

---

### 9. Settings Key Catalog: Initial Data Seeding
**Current Status**: Settings table and API implemented, initial data not seeded  
**Required Implementation**:
- Create seeder for all keys defined in settings-key-catalog.json
- Authentication-related settings (PAT TTL, rolling extension, password policy, lock policy, session TTL)
- Token-related settings (confirm_submission, ack_action, view_pdf)
- Admin account invitation settings (TTL, rate limits)
- PDF-related settings (storage driver, regeneration permission)
- Queue-related settings (driver, retry settings)

**Reference**: reforma-notes-v1.1.0.md reforma-notes-v1.0.0-settings-key-catalog.json

---

### 10. Frontend Adjustment: Complete S-02 Account List
**Current Status**: Implementation status unknown  
**Required Implementation**:
- Adjust GET /v1/system/admin-users parameters:
  - page, per_page: required
  - sort: enum definition (created_at_desc, etc.)
  - q: keyword search
  - role: role filter
  - status: status filter
- OpenAPI canonical compliance

**Reference**: reforma-notes-v1.1.0.md reforma-notes-v1.1.0.txt

---

### 11. Frontend Adjustment: Extend Progress Display Feature
**Current Status**: progress endpoint implemented  
**Required Implementation**:
- Determine progress acquisition method for CSV/PDF/file operations
- Provide information needed for progress bar display
- Recommended: extend progress endpoint

**Reference**: reforma-notes-v1.1.0.md reforma-notes-v1.1.0.txt

---

### 12. Frontend Adjustment: Unify Error Structure
**Current Status**: Implementation status unknown  
**Required Implementation**:
- Unify errors.reason / code / message, etc.
- Branching logic for /reforma/error and toast display
- Clarify error code definitions

**Reference**: 
- reforma-notes-v1.1.0.md reforma-notes-v1.1.0.txt
- reforma-notes-v1.1.0.md エラー設計

---

## Recommended Priority

### High Priority
1. A-06: Condition branch evaluation feature (core feature)
2. A-01: Complete CSV export implementation (extension of existing base)
3. Settings Key Catalog: Initial data seeding (required for operation)

### Medium Priority
4. A-02: Complete search implementation
5. A-05: Notification resend feature
6. A-05: PDF regeneration feature
7. Frontend adjustment items (3 items)

### Low Priority (v2 candidates)
8. SUPP-DISPLAY-MODE-001: Display mode feature
9. SUPP-THEME-001: Theme feature
10. SUPP-COMPUTED-001: Computed field feature

---

## Notes

- Refer to `reforma-notes-v1.1.0.md` for detailed specifications of each task
- When implementing, also update the OpenAPI definition (reforma-openapi-v0.1.4.yaml)
- Don't forget to reflect changes in the specification documents
