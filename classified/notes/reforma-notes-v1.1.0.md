# ReForma other specification (merged)
- version: v1.1.0
- generated_at: 2026-01-14T11:37:59.899600+00:00

## Sources
- latest/other/reforma-notes-v1.0.0-form-feature-attachments-.with-A06.json.json (v1.0.0)
- latest/other/reforma-notes-v1.0.0-form-feature-attachments-.with-samples.j.json (v1.0.0)
- latest/other/reforma-notes-v1.0.0-impl-handoff-init-pack.json.json (v1.0.0)
- latest/other/reforma-notes-v1.0.0-impl-handoff-init-pack.x-root.json.json (v1.0.0)
- latest/other/reforma-notes-v1.0.0-root-only-policy-.json.json (v1.0.0)
- latest/other/reforma-notes-v1.0.0-settings-key-catalog.json.json (v1.0.0)
- latest/other/reforma-notes-v1.0.0-条件分岐-実装整理パック-.json.json (v1.0.0)
- latest/other/reforma-notes-v1.0.0-条件分岐-評価結果IF-.json.json (v1.0.0)
- latest/other/reforma-notes-v1.0.0-追補パッチ-表示モード-テーマ-計算フィールド-.json.json (v1.0.0)
- latest/other/reforma-notes-v1.0.0.json (v1.0.0)
- latest/other/reforma-notes-v1.0.0.md (v1.0.0)
- latest/other/reforma-notes-v1.1.0.json (v1.1.0)
- latest/other/reforma-notes-v1.1.0.txt (v1.1.0)

---

## reforma-notes-v1.0.0-form-feature-attachments-.with-A06.json

_Source files:_ latest/other/reforma-notes-v1.0.0-form-feature-attachments-.with-A06.json.json

```json
{
  "meta": {
    "title": "フォーム機能別表（Attachments） v1.0",
    "version": "1.0",
    "generated_at": "2026-01-12T14:46:31.478591",
    "links": {
      "parent_spec": "フォーム機能詳細仕様書 v1.0"
    },
    "updated_at": "2026-01-12T14:59:41.882277"
  },
  "A-01_csv_column_definition": {
    "modes": [
      "value",
      "label",
      "both"
    ],
    "common_columns": [
      {
        "col_key": "submission_id",
        "label_ja": "受付ID",
        "type": "string",
        "modes": [
          "value",
          "label",
          "both"
        ],
        "notes": "submissions.id"
      },
      {
        "col_key": "submitted_at",
        "label_ja": "受付日時",
        "type": "datetime",
        "modes": [
          "value",
          "label",
          "both"
        ],
        "notes": "submissions.created_at"
      },
      {
        "col_key": "form_code",
        "label_ja": "フォーム識別子",
        "type": "string",
        "modes": [
          "value",
          "label",
          "both"
        ],
        "notes": "forms.code"
      },
      {
        "col_key": "status",
        "label_ja": "ステータス",
        "type": "string",
        "modes": [
          "value",
          "label",
          "both"
        ],
        "notes": "submissions.status"
      }
    ],
    "field_column_naming": {
      "value_or_label_mode": "f:{field_key}",
      "both_mode": {
        "value": "f:{field_key}",
        "label": "f:{field_key}__label"
      }
    },
    "type_rules": {
      "text": {
        "value": "string",
        "label": "string"
      },
      "textarea": {
        "value": "string",
        "label": "string"
      },
      "email": {
        "value": "string",
        "label": "string"
      },
      "tel": {
        "value": "string",
        "label": "string"
      },
      "number": {
        "value": "number",
        "label": "number"
      },
      "select": {
        "value": "value",
        "label": "option_label_snapshot_or_translate"
      },
      "radio": {
        "value": "value",
        "label": "option_label_snapshot_or_translate"
      },
      "checkbox": {
        "value": "join(values, delimiter)",
        "label": "join(labels, delimiter)",
        "delimiter_configurable": true
      },
      "date": {
        "value": "iso",
        "label": "iso"
      },
      "time": {
        "value": "iso",
        "label": "iso"
      },
      "datetime": {
        "value": "iso",
        "label": "iso"
      },
      "terms": {
        "value": "boolean",
        "label": "agree_or_disagree_label",
        "label_configurable": true
      },
      "file": {
        "value": "filename_or_url",
        "label": "filename_or_url",
        "depends_on_setting": true
      }
    },
    "csv_rules": {
      "delimiter_default": ",",
      "escape": "rfc4180_like",
      "utf8_bom": "configurable"
    },
    "sample_headers": {
      "form": "CONTACT_2026",
      "mode": "both",
      "csv_header": [
        "submission_id",
        "submitted_at",
        "form_code",
        "status",
        "f:name",
        "f:name__label",
        "f:email",
        "f:category",
        "f:category__label",
        "f:message"
      ],
      "sample_row": [
        "12345",
        "2026-01-12 20:15",
        "CONTACT_2026",
        "received",
        "ishida",
        "石田",
        "email@example.com",
        "inq",
        "お問い合わせ",
        "テストです"
      ]
    }
  },
  "A-02_search_rule_matrix": {
    "default_combine": "AND",
    "type_operators": [
      {
        "field_type": "text/textarea/email/tel",
        "operators": [
          "contains"
        ],
        "value_source": "submission_values.value",
        "index_hint": [
          "LIKE_now",
          "FULLTEXT_future"
        ]
      },
      {
        "field_type": "number",
        "operators": [
          "eq",
          "min",
          "max",
          "between"
        ],
        "value_source": "submission_values.value(normalized)",
        "index_hint": [
          "(field_id,value)"
        ]
      },
      {
        "field_type": "date/datetime",
        "operators": [
          "from",
          "to",
          "between"
        ],
        "value_source": "submission_values.value(iso)",
        "index_hint": [
          "(field_id,value)"
        ]
      },
      {
        "field_type": "select/radio",
        "operators": [
          "eq",
          "in"
        ],
        "value_source": "submission_values.value",
        "index_hint": [
          "(field_id,value)"
        ]
      },
      {
        "field_type": "checkbox",
        "operators": [
          "any_in(default)",
          "all_in(optional)"
        ],
        "value_source": "submission_values.value(array_or_joined)",
        "index_hint": [
          "consider_json_storage_future"
        ]
      },
      {
        "field_type": "terms",
        "operators": [
          "eq"
        ],
        "value_source": "submission_values.value(boolean)",
        "index_hint": [
          "(field_id,value)"
        ]
      }
    ],
    "checkbox_defaults": {
      "operator": "any_in",
      "all_in": "future_extension"
    }
  },
  "A-03_pdf_block_mapping": {
    "block_key_naming": {
      "field": "f:{field_key}",
      "system": [
        "sys:submitted_at",
        "sys:submission_id",
        "sys:form_code"
      ]
    },
    "mapping": [
      {
        "block_key": "sys:submitted_at",
        "source": "submissions.created_at",
        "fallback": null,
        "notes": "受付日時"
      },
      {
        "block_key": "sys:submission_id",
        "source": "submissions.id",
        "fallback": null,
        "notes": "受付ID"
      },
      {
        "block_key": "sys:form_code",
        "source": "forms.code",
        "fallback": null,
        "notes": "フォーム識別子"
      },
      {
        "block_key": "f:{field_key}",
        "source": "submission_values.value",
        "fallback": "empty",
        "notes": "型により整形"
      },
      {
        "block_key": "f:{field_key}__label",
        "source": "option_label_snapshot",
        "fallback": "translate",
        "notes": "選択系のみ"
      }
    ],
    "note": "Coordinates/fonts/layout are managed in template assets; this table defines data mapping only.",
    "sample_template_mapping": {
      "template": "contact_default_v1",
      "blocks": [
        {
          "block_key": "sys:submitted_at",
          "label": "受付日時",
          "note": "header"
        },
        {
          "block_key": "f:name__label",
          "label": "氏名",
          "note": "prefer label"
        },
        {
          "block_key": "f:email",
          "label": "メールアドレス"
        },
        {
          "block_key": "f:category__label",
          "label": "お問い合わせ種別"
        },
        {
          "block_key": "f:message",
          "label": "内容",
          "note": "multiline"
        }
      ]
    }
  },
  "A-04_notification_template_variables": {
    "rules": {
      "allowed_variables_only": true,
      "undefined_variable_behavior": "fail_and_audit_log"
    },
    "variables": [
      {
        "var": "{{form.code}}",
        "meaning": "フォーム識別子",
        "example": "CONTACT_2026"
      },
      {
        "var": "{{form.title}}",
        "meaning": "フォーム名（送信時表示言語）",
        "example": "お問い合わせ",
        "notes": "snapshot preferred"
      },
      {
        "var": "{{submission.id}}",
        "meaning": "受付ID",
        "example": "12345"
      },
      {
        "var": "{{submission.submitted_at}}",
        "meaning": "受付日時",
        "example": "2026-01-12 20:15",
        "notes": "server time"
      },
      {
        "var": "{{confirm_url.ack}}",
        "meaning": "ACK 再表示URL",
        "example": "https://..."
      },
      {
        "var": "{{confirm_url.pdf}}",
        "meaning": "PDF 閲覧URL",
        "example": "https://..."
      },
      {
        "var": "{{fields.summary}}",
        "meaning": "主要項目の抜粋",
        "example": "氏名:...",
        "notes": "form setting (future extension)"
      }
    ],
    "field_access": {
      "value": "{{field.<field_key>}}",
      "label": "{{field_label.<field_key>}}"
    },
    "sample_templates": {
      "user_ja": {
        "body": "{{form.title}} を受け付けました。\\n受付ID：{{submission.id}}\\n受付日時：{{submission.submitted_at}}\\n\\n{{fields.summary}}\\n\\n{{confirm_url.ack}}"
      }
    }
  },
  "A-05_examples": {
    "hidden_field_retention_example": {
      "scenario": "department was entered then hidden; still need to keep value",
      "approach": "configure retention exception rule for field_key=department"
    },
    "notification_resend_example": {
      "scenario": "user did not receive email; resend",
      "approach": "system_admin triggers resend; queued; audit logged"
    },
    "pdf_regeneration_example": {
      "policy": "default forbidden",
      "allowed_when": "defined operationally (e.g., wrong template)",
      "actor": "system_admin (or root when root-only configured)",
      "execution": "async with audit"
    }
  },
  "A-06_condition_branch_rules": {
    "source": "Basic Spec v1.0 Appendix D (reconstructed)",
    "applies_to": [
      "visibility_rule",
      "required_rule",
      "step_transition_rule"
    ],
    "conventions": {
      "explicit_logical_ops": true,
      "undefined_field_key": "configuration_error",
      "fallback_on_failure": [
        "hide",
        "not_required",
        "deny_transition"
      ]
    },
    "format": {
      "version": "1",
      "op": "and|or|not|comparison",
      "items": "required for and/or",
      "field": "target field_key",
      "value": "comparison value"
    },
    "operators": [
      "eq",
      "ne",
      "in",
      "contains",
      "gt",
      "gte",
      "lt",
      "lte",
      "between",
      "exists",
      "and",
      "or",
      "not"
    ],
    "examples": {
      "visibility_rule": {
        "version": "1",
        "op": "eq",
        "field": "category",
        "value": "inq"
      },
      "required_rule": {
        "version": "1",
        "op": "exists",
        "field": "company_name",
        "value": true
      },
      "step_transition_rule": {
        "version": "1",
        "op": "eq",
        "field": "terms",
        "value": true
      }
    },
    "apply": {
      "visibility_false": "hide_and_do_not_store",
      "required_false": "not_required",
      "transition_false": "deny_with_error"
    },
    "delegation": {
      "ui": "06.UI Spec",
      "api": "03.API Spec"
    }
  }
}
```

## reforma-notes-v1.0.0-form-feature-attachments-.with-samples.j

_Source files:_ latest/other/reforma-notes-v1.0.0-form-feature-attachments-.with-samples.j.json

```json
{
  "meta": {
    "title": "フォーム機能別表（Attachments） v1.0",
    "version": "1.0",
    "generated_at": "2026-01-12T14:46:31.478591",
    "links": {
      "parent_spec": "フォーム機能詳細仕様書 v1.0"
    },
    "updated_at": "2026-01-12T14:51:45.668980"
  },
  "A-01_csv_column_definition": {
    "modes": [
      "value",
      "label",
      "both"
    ],
    "common_columns": [
      {
        "col_key": "submission_id",
        "label_ja": "受付ID",
        "type": "string",
        "modes": [
          "value",
          "label",
          "both"
        ],
        "notes": "submissions.id"
      },
      {
        "col_key": "submitted_at",
        "label_ja": "受付日時",
        "type": "datetime",
        "modes": [
          "value",
          "label",
          "both"
        ],
        "notes": "submissions.created_at"
      },
      {
        "col_key": "form_code",
        "label_ja": "フォーム識別子",
        "type": "string",
        "modes": [
          "value",
          "label",
          "both"
        ],
        "notes": "forms.code"
      },
      {
        "col_key": "status",
        "label_ja": "ステータス",
        "type": "string",
        "modes": [
          "value",
          "label",
          "both"
        ],
        "notes": "submissions.status"
      }
    ],
    "field_column_naming": {
      "value_or_label_mode": "f:{field_key}",
      "both_mode": {
        "value": "f:{field_key}",
        "label": "f:{field_key}__label"
      }
    },
    "type_rules": {
      "text": {
        "value": "string",
        "label": "string"
      },
      "textarea": {
        "value": "string",
        "label": "string"
      },
      "email": {
        "value": "string",
        "label": "string"
      },
      "tel": {
        "value": "string",
        "label": "string"
      },
      "number": {
        "value": "number",
        "label": "number"
      },
      "select": {
        "value": "value",
        "label": "option_label_snapshot_or_translate"
      },
      "radio": {
        "value": "value",
        "label": "option_label_snapshot_or_translate"
      },
      "checkbox": {
        "value": "join(values, delimiter)",
        "label": "join(labels, delimiter)",
        "delimiter_configurable": true
      },
      "date": {
        "value": "iso",
        "label": "iso"
      },
      "time": {
        "value": "iso",
        "label": "iso"
      },
      "datetime": {
        "value": "iso",
        "label": "iso"
      },
      "terms": {
        "value": "boolean",
        "label": "agree_or_disagree_label",
        "label_configurable": true
      },
      "file": {
        "value": "filename_or_url",
        "label": "filename_or_url",
        "depends_on_setting": true
      }
    },
    "csv_rules": {
      "delimiter_default": ",",
      "escape": "rfc4180_like",
      "utf8_bom": "configurable"
    },
    "sample_headers": {
      "form": "CONTACT_2026",
      "mode": "both",
      "csv_header": [
        "submission_id",
        "submitted_at",
        "form_code",
        "status",
        "f:name",
        "f:name__label",
        "f:email",
        "f:category",
        "f:category__label",
        "f:message"
      ],
      "sample_row": [
        "12345",
        "2026-01-12 20:15",
        "CONTACT_2026",
        "received",
        "ishida",
        "石田",
        "email@example.com",
        "inq",
        "お問い合わせ",
        "テストです"
      ]
    }
  },
  "A-02_search_rule_matrix": {
    "default_combine": "AND",
    "type_operators": [
      {
        "field_type": "text/textarea/email/tel",
        "operators": [
          "contains"
        ],
        "value_source": "submission_values.value",
        "index_hint": [
          "LIKE_now",
          "FULLTEXT_future"
        ]
      },
      {
        "field_type": "number",
        "operators": [
          "eq",
          "min",
          "max",
          "between"
        ],
        "value_source": "submission_values.value(normalized)",
        "index_hint": [
          "(field_id,value)"
        ]
      },
      {
        "field_type": "date/datetime",
        "operators": [
          "from",
          "to",
          "between"
        ],
        "value_source": "submission_values.value(iso)",
        "index_hint": [
          "(field_id,value)"
        ]
      },
      {
        "field_type": "select/radio",
        "operators": [
          "eq",
          "in"
        ],
        "value_source": "submission_values.value",
        "index_hint": [
          "(field_id,value)"
        ]
      },
      {
        "field_type": "checkbox",
        "operators": [
          "any_in(default)",
          "all_in(optional)"
        ],
        "value_source": "submission_values.value(array_or_joined)",
        "index_hint": [
          "consider_json_storage_future"
        ]
      },
      {
        "field_type": "terms",
        "operators": [
          "eq"
        ],
        "value_source": "submission_values.value(boolean)",
        "index_hint": [
          "(field_id,value)"
        ]
      }
    ],
    "checkbox_defaults": {
      "operator": "any_in",
      "all_in": "future_extension"
    }
  },
  "A-03_pdf_block_mapping": {
    "block_key_naming": {
      "field": "f:{field_key}",
      "system": [
        "sys:submitted_at",
        "sys:submission_id",
        "sys:form_code"
      ]
    },
    "mapping": [
      {
        "block_key": "sys:submitted_at",
        "source": "submissions.created_at",
        "fallback": null,
        "notes": "受付日時"
      },
      {
        "block_key": "sys:submission_id",
        "source": "submissions.id",
        "fallback": null,
        "notes": "受付ID"
      },
      {
        "block_key": "sys:form_code",
        "source": "forms.code",
        "fallback": null,
        "notes": "フォーム識別子"
      },
      {
        "block_key": "f:{field_key}",
        "source": "submission_values.value",
        "fallback": "empty",
        "notes": "型により整形"
      },
      {
        "block_key": "f:{field_key}__label",
        "source": "option_label_snapshot",
        "fallback": "translate",
        "notes": "選択系のみ"
      }
    ],
    "note": "Coordinates/fonts/layout are managed in template assets; this table defines data mapping only.",
    "sample_template_mapping": {
      "template": "contact_default_v1",
      "blocks": [
        {
          "block_key": "sys:submitted_at",
          "label": "受付日時",
          "note": "header"
        },
        {
          "block_key": "f:name__label",
          "label": "氏名",
          "note": "prefer label"
        },
        {
          "block_key": "f:email",
          "label": "メールアドレス"
        },
        {
          "block_key": "f:category__label",
          "label": "お問い合わせ種別"
        },
        {
          "block_key": "f:message",
          "label": "内容",
          "note": "multiline"
        }
      ]
    }
  },
  "A-04_notification_template_variables": {
    "rules": {
      "allowed_variables_only": true,
      "undefined_variable_behavior": "fail_and_audit_log"
    },
    "variables": [
      {
        "var": "{{form.code}}",
        "meaning": "フォーム識別子",
        "example": "CONTACT_2026"
      },
      {
        "var": "{{form.title}}",
        "meaning": "フォーム名（送信時表示言語）",
        "example": "お問い合わせ",
        "notes": "snapshot preferred"
      },
      {
        "var": "{{submission.id}}",
        "meaning": "受付ID",
        "example": "12345"
      },
      {
        "var": "{{submission.submitted_at}}",
        "meaning": "受付日時",
        "example": "2026-01-12 20:15",
        "notes": "server time"
      },
      {
        "var": "{{confirm_url.ack}}",
        "meaning": "ACK 再表示URL",
        "example": "https://..."
      },
      {
        "var": "{{confirm_url.pdf}}",
        "meaning": "PDF 閲覧URL",
        "example": "https://..."
      },
      {
        "var": "{{fields.summary}}",
        "meaning": "主要項目の抜粋",
        "example": "氏名:...",
        "notes": "form setting (future extension)"
      }
    ],
    "field_access": {
      "value": "{{field.<field_key>}}",
      "label": "{{field_label.<field_key>}}"
    },
    "sample_templates": {
      "user_ja": {
        "body": "{{form.title}} を受け付けました。\\n受付ID：{{submission.id}}\\n受付日時：{{submission.submitted_at}}\\n\\n{{fields.summary}}\\n\\n{{confirm_url.ack}}"
      }
    }
  },
  "A-05_examples": {
    "hidden_field_retention_example": {
      "scenario": "department was entered then hidden; still need to keep value",
      "approach": "configure retention exception rule for field_key=department"
    },
    "notification_resend_example": {
      "scenario": "user did not receive email; resend",
      "approach": "system_admin triggers resend; queued; audit logged"
    },
    "pdf_regeneration_example": {
      "policy": "default forbidden",
      "allowed_when": "defined operationally (e.g., wrong template)",
      "actor": "system_admin (or root when root-only configured)",
      "execution": "async with audit"
    }
  }
}
```

## reforma-notes-v1.0.0-impl-handoff-init-pack.json

_Source files:_ latest/other/reforma-notes-v1.0.0-impl-handoff-init-pack.json.json

```json
{
  "meta": {
    "title": "ReForma 配布物③：実装引き継ぎ Init Pack（構造化JSON）",
    "generated_at": "2026-01-12T11:54:47.330137",
    "timezone": "Asia/Tokyo",
    "applies_to": {
      "spec_baseline": "v1.0 immutable",
      "extensions": [
        "v1.1 delta"
      ],
      "handoff": [
        "2026-01-12 backend->frontend",
        "SUP-FE latest"
      ]
    }
  },
  "priority_rule": [
    "backend-handoff-20260112",
    "sup-fe-latest",
    "extension-v1.1",
    "spec-v1.0"
  ],
  "mounting": {
    "spa_base": "/reforma/",
    "api_base": "/reforma/api/",
    "version_prefix": "/v1",
    "example": "/reforma/api/v1/auth/me",
    "no_api_double_prefix": true
  },
  "api_envelope": {
    "success": "boolean",
    "data": "any",
    "message": "string|null",
    "errors": "object|null",
    "error_extras": {
      "code": "string|null",
      "request_id": "string"
    }
  },
  "frontend_rules": {
    "session_invalid": {
      "trigger_statuses": [
        401,
        419
      ],
      "redirect": "/logout?reason=session_invalid",
      "invalidate_client_state": true
    },
    "theme": "ReForma background common",
    "debug_ui": {
      "modes": [
        "VITE_DEBUG",
        "VITE_DEBUG_UI",
        "?debug=1"
      ],
      "payload_transport": "navigate state.debugPayload"
    }
  },
  "backend_rules": {
    "auth_admin": {
      "method": "Sanctum PAT",
      "token_transport": "Authorization: Bearer <token>",
      "ttl_days_default": 30,
      "rolling_extension": {
        "enabled": true,
        "update_frequency": "once_per_day"
      },
      "expired_behavior": {
        "http_status": 401,
        "code": "TOKEN_EXPIRED"
      }
    },
    "respondent_auth": {
      "method": "session-based",
      "confirm_url_auth": "token-based is sufficient"
    }
  },
  "tokens": {
    "storage": "hash_only_in_db",
    "canonical_types": {
      "confirm_submission": {
        "ttl_hours": 24,
        "one_time": true
      },
      "ack_action": {
        "ttl_hours": 24,
        "one_time": true
      },
      "view_pdf": {
        "ttl_days": 7,
        "one_time": false,
        "one_time_configurable": true
      }
    }
  },
  "queue": {
    "driver": "database",
    "dlq": "failed_jobs",
    "retries": {
      "tries": 5,
      "backoff_seconds": [
        60,
        300,
        900
      ]
    },
    "queues_recommended": [
      "default",
      "notifications",
      "pdf"
    ],
    "async_targets": [
      "mail",
      "slack",
      "pdf_generate",
      "pdf_regenerate"
    ]
  },
  "pdf": {
    "types": [
      "submission",
      "ack"
    ],
    "storage_default": "s3",
    "storage_switchable": [
      "local"
    ],
    "regeneration_policy": {
      "source_of_truth": "submission-time snapshot",
      "default": "do not regenerate",
      "exception": "system_admin explicit action with audit log",
      "violation_http_status": 409
    }
  },
  "settings": {
    "table": "settings",
    "scope": "system",
    "initial_impl": "no UI; insert via seeder/SQL; app reads via cache",
    "schema_recommended": {
      "columns": [
        "id",
        "scope",
        "key",
        "type",
        "value_json",
        "description",
        "is_secret",
        "updated_by",
        "created_at",
        "updated_at"
      ],
      "unique": [
        "scope",
        "key"
      ]
    }
  },
  "deliverables": {
    "s02_implementation_pack": "s-02-implementation-pack.md",
    "settings_key_catalog": "settings-key-catalog.json"
  }
}
```

## reforma-notes-v1.0.0-impl-handoff-init-pack.x-root.json

_Source files:_ latest/other/reforma-notes-v1.0.0-impl-handoff-init-pack.x-root.json.json

```json
{
  "meta": {
    "title": "ReForma 配布物③：実装引き継ぎ Init Pack（構造化JSON）",
    "generated_at": "2026-01-12T12:23:22.721798",
    "timezone": "Asia/Tokyo",
    "applies_to": {
      "spec_baseline": "v1.0 immutable",
      "extensions": [
        "v1.1 delta"
      ],
      "handoff": [
        "2026-01-12 backend->frontend",
        "SUP-FE latest"
      ]
    },
    "version": "draft-2026-01-12+root-only"
  },
  "priority_rule": [
    "backend-handoff-20260112",
    "sup-fe-latest",
    "extension-v1.1",
    "spec-v1.0"
  ],
  "mounting": {
    "spa_base": "/reforma/",
    "api_base": "/reforma/api/",
    "version_prefix": "/v1",
    "example": "/reforma/api/v1/auth/me",
    "no_api_double_prefix": true
  },
  "api_envelope": {
    "success": "boolean",
    "data": "any",
    "message": "string|null",
    "errors": "object|null",
    "error_extras": {
      "code": "string|null",
      "request_id": "string"
    }
  },
  "frontend_rules": {
    "session_invalid": {
      "trigger_statuses": [
        401,
        419
      ],
      "redirect": "/logout?reason=session_invalid",
      "invalidate_client_state": true
    },
    "theme": "ReForma background common",
    "debug_ui": {
      "modes": [
        "VITE_DEBUG",
        "VITE_DEBUG_UI",
        "?debug=1"
      ],
      "payload_transport": "navigate state.debugPayload"
    }
  },
  "backend_rules": {
    "auth_admin": {
      "method": "Sanctum PAT",
      "token_transport": "Authorization: Bearer <token>",
      "ttl_days_default": 30,
      "rolling_extension": {
        "enabled": true,
        "update_frequency": "once_per_day"
      },
      "expired_behavior": {
        "http_status": 401,
        "code": "TOKEN_EXPIRED"
      }
    },
    "respondent_auth": {
      "method": "session-based",
      "confirm_url_auth": "token-based is sufficient"
    }
  },
  "tokens": {
    "storage": "hash_only_in_db",
    "canonical_types": {
      "confirm_submission": {
        "ttl_hours": 24,
        "one_time": true
      },
      "ack_action": {
        "ttl_hours": 24,
        "one_time": true
      },
      "view_pdf": {
        "ttl_days": 7,
        "one_time": false,
        "one_time_configurable": true
      }
    }
  },
  "queue": {
    "driver": "database",
    "dlq": "failed_jobs",
    "retries": {
      "tries": 5,
      "backoff_seconds": [
        60,
        300,
        900
      ]
    },
    "queues_recommended": [
      "default",
      "notifications",
      "pdf"
    ],
    "async_targets": [
      "mail",
      "slack",
      "pdf_generate",
      "pdf_regenerate"
    ]
  },
  "pdf": {
    "types": [
      "submission",
      "ack"
    ],
    "storage_default": "s3",
    "storage_switchable": [
      "local"
    ],
    "regeneration_policy": {
      "source_of_truth": "submission-time snapshot",
      "default": "do not regenerate",
      "exception": "system_admin explicit action with audit log",
      "violation_http_status": 409
    }
  },
  "settings": {
    "table": "settings",
    "scope": "system",
    "initial_impl": "no UI; insert via seeder/SQL; app reads via cache",
    "schema_recommended": {
      "columns": [
        "id",
        "scope",
        "key",
        "type",
        "value_json",
        "description",
        "is_secret",
        "updated_by",
        "created_at",
        "updated_at"
      ],
      "unique": [
        "scope",
        "key"
      ]
    }
  },
  "deliverables": {
    "s02_implementation_pack": "s-02-implementation-pack.md",
    "settings_key_catalog": "settings-key-catalog.json"
  },
  "root_admin": {
    "model": "attribute",
    "user_attribute": "is_root",
    "invariants": [
      "Root must be system_admin",
      "Root account cannot be disabled or deleted",
      "Root flag cannot be modified via UI/API (ops/seeder/SQL only)",
      "Root cannot grant Root to others (including self)"
    ],
    "future_policy": {
      "multiple_root_allowed": true,
      "grant_method": "ops_only"
    },
    "enforcement": {
      "screen_flag": "allow_root_only",
      "api_middleware": "RootOnly (system_admin && is_root)",
      "double_defense_required": true,
      "audit_log_required": true
    }
  },
  "rbac": {
    "root_only_screens": [
      {
        "screen_id": "S-XX",
        "name": "SYSTEM_SETTINGS",
        "route": "/system/settings",
        "status": "planned"
      },
      {
        "screen_id": "S-YY",
        "name": "ROLE_PERMISSION_ASSIGN",
        "route": "/system/roles/permissions",
        "status": "planned"
      }
    ],
    "root_only_apis": [
      {
        "api": "GET:/api/v1/system/settings",
        "status": "planned"
      },
      {
        "api": "PUT:/api/v1/system/settings",
        "status": "planned"
      },
      {
        "api": "GET:/api/v1/system/roles/permissions",
        "status": "planned"
      },
      {
        "api": "PUT:/api/v1/system/roles/permissions",
        "status": "planned"
      }
    ],
    "notes": [
      "Root-only features are not expressible via permission_assignment; require users.is_root=true in addition to system_admin role.",
      "Root-only must be enforced both at screen level (allow_root_only) and API level (RootOnly middleware)."
    ]
  }
}
```

## reforma-notes-v1.0.0-root-only-policy-.json

_Source files:_ latest/other/reforma-notes-v1.0.0-root-only-policy-.json.json

```json
{
  "schema_version": "1.0",
  "doc_type": "security_policy",
  "policy_key": "root_only",
  "version": "v1.0",
  "updated_at": "2026-01-13",
  "principles": [
    "root-only は権限構造や全体影響が極大の操作を is_root=true に限定する二重防御である",
    "UI ではなく API レベルで強制する",
    "拒否時は 403 / code=FORBIDDEN / errors.reason=ROOT_ONLY に統一する"
  ],
  "preconditions": {
    "auth": [
      "auth:sanctum",
      "abilities:admin",
      "reforma.admin_pat"
    ],
    "rbac": [
      "reforma.system_admin"
    ],
    "root_only": [
      "reforma.root_only"
    ]
  },
  "deny_response": {
    "http_status": 403,
    "code": "FORBIDDEN",
    "message": "Forbidden.",
    "errors": {
      "reason": "ROOT_ONLY"
    }
  },
  "targets": {
    "root_only_required": [
      {
        "key": "system_admin_promotion",
        "title": "system_admin 付与（昇格）",
        "rule": "target が system_admin へ昇格する場合のみ root-only 必須",
        "endpoints": [
          "PUT /v1/system/admin-users/{id}"
        ],
        "status": "implemented"
      },
      {
        "key": "root_grant_revoke",
        "title": "root 付与・剥奪（API を提供する場合）",
        "rule": "is_root の true/false 変更は root-only 必須",
        "constraints": [
          "root は必ず1人以上",
          "自己剥奪・自己降格は禁止"
        ],
        "status": "not_provided_v1"
      },
      {
        "key": "rbac_master_change",
        "title": "RBAC マスタ（roles）変更（API を提供する場合）",
        "rule": "roles の追加/削除/code変更は root-only 必須",
        "status": "not_provided_v1"
      }
    ],
    "system_admin_allowed": [
      {
        "key": "system_admin_demotion",
        "title": "system_admin 剥奪（降格）",
        "rule": "root-only は不要。ただし Phase A 制約（自己降格禁止/最後のsystem_admin禁止）は必須",
        "endpoints": [
          "PUT /v1/system/admin-users/{id}"
        ],
        "status": "implemented_with_phase_a_constraints"
      },
      {
        "key": "admin_profile_update",
        "title": "管理者の一般情報更新",
        "rule": "root-only は不要",
        "status": "allowed"
      }
    ],
    "forbidden_v1": [
      {
        "key": "roles_edit_api",
        "title": "roles の任意編集 API",
        "rule": "v1.0 では提供しない（Seeder による固定運用）"
      },
      {
        "key": "self_root_change",
        "title": "root の自己付与・自己剥奪",
        "rule": "抜け道になるため禁止"
      }
    ]
  },
  "sharing": {
    "audiences": [
      "backend",
      "frontend"
    ],
    "frontend_guidance": {
      "source_of_truth": "roles[] と is_root を用いて UI を制御する。root-only 対象操作は UI でも無効化するが、最終的には API で拒否される。",
      "deny_handling": "403 FORBIDDEN + errors.reason=ROOT_ONLY を受けたら『root 権限が必要です』を表示する"
    }
  }
}
```

## reforma-notes-v1.0.0-settings-key-catalog.json

_Source files:_ latest/other/reforma-notes-v1.0.0-settings-key-catalog.json.json

```json
{
  "meta": {
    "title": "ReForma 配布物②：Settings Key Catalog（v1.x）",
    "version": "1.0",
    "scope_policy": "system_fixed",
    "source_priority": [
      "backend-handoff-20260112",
      "backend-canvas-export-20260112",
      "sup-fe-latest",
      "spec-v1.1-delta",
      "spec-v1.0-immutable"
    ]
  },
  "keys": [
    {
      "key": "auth.admin.pat.ttl_days",
      "type": "int",
      "default": 30,
      "scope": "system",
      "is_secret": false,
      "description": "Admin PAT の既定TTL（日）。"
    },
    {
      "key": "auth.admin.pat.rolling_extension.enabled",
      "type": "bool",
      "default": true,
      "scope": "system",
      "is_secret": false,
      "description": "PAT ローリング延長の有効化。"
    },
    {
      "key": "auth.admin.pat.rolling_extension.update_frequency",
      "type": "string",
      "default": "once_per_day",
      "scope": "system",
      "is_secret": false,
      "description": "ローリング延長の更新頻度（確定：1日1回）。"
    },
    {
      "key": "auth.password_policy.min_length",
      "type": "int",
      "default": 8,
      "scope": "system",
      "is_secret": false,
      "description": "Admin/Respondent 共通の最小文字数（変更可）。"
    },
    {
      "key": "auth.password_policy.require.lowercase",
      "type": "bool",
      "default": true,
      "scope": "system",
      "is_secret": false,
      "description": "小文字必須。"
    },
    {
      "key": "auth.password_policy.require.uppercase",
      "type": "bool",
      "default": true,
      "scope": "system",
      "is_secret": false,
      "description": "大文字必須。"
    },
    {
      "key": "auth.password_policy.require.digit",
      "type": "bool",
      "default": true,
      "scope": "system",
      "is_secret": false,
      "description": "数字必須。"
    },
    {
      "key": "auth.password_policy.require.symbol",
      "type": "bool",
      "default": true,
      "scope": "system",
      "is_secret": false,
      "description": "記号必須。"
    },
    {
      "key": "auth.lock_policy.failures",
      "type": "int",
      "default": 3,
      "scope": "system",
      "is_secret": false,
      "description": "失敗回数でロック（変更可）。"
    },
    {
      "key": "auth.lock_policy.lock_minutes",
      "type": "int",
      "default": 15,
      "scope": "system",
      "is_secret": false,
      "description": "ロック時間（分）（変更可）。"
    },
    {
      "key": "auth.session.ttl_minutes",
      "type": "int",
      "default": null,
      "scope": "system",
      "is_secret": false,
      "description": "Admin/Respondent セッションTTL（分）。未設定ならアプリ既定。"
    },
    {
      "key": "token.ttl_hours.confirm_submission",
      "type": "int",
      "default": 24,
      "scope": "system",
      "is_secret": false,
      "description": "confirm_submission token の TTL（時間）。"
    },
    {
      "key": "token.one_time.confirm_submission",
      "type": "bool",
      "default": true,
      "scope": "system",
      "is_secret": false,
      "description": "confirm_submission token は one-time。"
    },
    {
      "key": "token.ttl_hours.ack_action",
      "type": "int",
      "default": 24,
      "scope": "system",
      "is_secret": false,
      "description": "ack_action token の TTL（時間）。"
    },
    {
      "key": "token.one_time.ack_action",
      "type": "bool",
      "default": true,
      "scope": "system",
      "is_secret": false,
      "description": "ack_action token は one-time。"
    },
    {
      "key": "token.ttl_days.view_pdf",
      "type": "int",
      "default": 7,
      "scope": "system",
      "is_secret": false,
      "description": "view_pdf token の TTL（日）。"
    },
    {
      "key": "token.one_time.view_pdf",
      "type": "bool",
      "default": false,
      "scope": "system",
      "is_secret": false,
      "description": "view_pdf token の one-time（既定false、変更可）。"
    },
    {
      "key": "admin_invite.ttl_hours",
      "type": "int",
      "default": 72,
      "scope": "system",
      "is_secret": false,
      "description": "管理アカウント招待 token TTL（時間）。"
    },
    {
      "key": "admin_invite.single_use",
      "type": "bool",
      "default": true,
      "scope": "system",
      "is_secret": false,
      "description": "管理アカウント招待 token は one-time。"
    },
    {
      "key": "admin_invite.rate_limit.min_interval_sec",
      "type": "int",
      "default": 60,
      "scope": "system",
      "is_secret": false,
      "description": "招待再送の最小間隔（秒）。"
    },
    {
      "key": "admin_invite.rate_limit.per_hour",
      "type": "int",
      "default": 5,
      "scope": "system",
      "is_secret": false,
      "description": "招待再送の上限（1時間）。"
    },
    {
      "key": "admin_invite.rate_limit.per_day",
      "type": "int",
      "default": 20,
      "scope": "system",
      "is_secret": false,
      "description": "招待再送の上限（1日）。"
    },
    {
      "key": "pdf.storage.driver",
      "type": "string",
      "default": "s3",
      "scope": "system",
      "is_secret": false,
      "description": "PDF 保存先の既定（s3 推奨 / local 切替可）。"
    },
    {
      "key": "pdf.regeneration.default_allowed",
      "type": "bool",
      "default": false,
      "scope": "system",
      "is_secret": false,
      "description": "PDF 再生成の既定（原則禁止）。"
    },
    {
      "key": "queue.driver",
      "type": "string",
      "default": "database",
      "scope": "system",
      "is_secret": false,
      "description": "Queue driver（確定：database）。"
    },
    {
      "key": "queue.retries.tries",
      "type": "int",
      "default": 5,
      "scope": "system",
      "is_secret": false,
      "description": "Job tries（確定：5）。"
    },
    {
      "key": "queue.retries.backoff_seconds",
      "type": "array<int>",
      "default": [
        60,
        300,
        900
      ],
      "scope": "system",
      "is_secret": false,
      "description": "Job backoff（確定：[60,300,900]）。"
    }
  ]
}
```

## A-06 条件分岐 JSON 契約

_Source files:_ latest/other/reforma-notes-v1.0.0-条件分岐-実装整理パック-.json.json

```json
{
  "id": "a06_contract",
  "title": "A-06 条件分岐 JSON 契約",
  "blocks": [
    {
      "type": "kv",
      "items": {
        "applies_to": [
          "visibility_rule",
          "required_rule",
          "step_transition_rule"
        ],
        "operators": [
          "eq",
          "ne",
          "in",
          "contains",
          "gt",
          "gte",
          "lt",
          "lte",
          "between",
          "exists",
          "and",
          "or",
          "not"
        ],
        "fallback_on_failure": [
          "hide",
          "not_required",
          "deny_transition"
        ],
        "explicit_logical_ops": true,
        "max_nesting_v1x": 1
      }
    },
    {
      "type": "object",
      "title": "format",
      "value": {
        "version": "1",
        "op": "and|or|not|comparison",
        "items": "required for and/or",
        "field": "target field_key",
        "value": "comparison value"
      }
    },
    {
      "type": "object",
      "title": "apply",
      "value": {
        "visibility_false": "hide_and_do_not_store",
        "required_false": "not_required",
        "transition_false": "deny_with_error"
      }
    },
    {
      "type": "object",
      "title": "examples",
      "value": {
        "visibility_rule": {
          "version": "1",
          "op": "eq",
          "field": "category",
          "value": "inq"
        },
        "required_rule": {
          "version": "1",
          "op": "exists",
          "field": "company_name",
          "value": true
        },
        "step_transition_rule": {
          "version": "1",
          "op": "eq",
          "field": "terms",
          "value": true
        }
      }
    }
  ]
}
```

## API 評価フロー

_Source files:_ latest/other/reforma-notes-v1.0.0-条件分岐-実装整理パック-.json.json

```json
{
  "id": "api_evaluation_flow",
  "title": "API 評価フロー",
  "blocks": [
    {
      "type": "list",
      "title": "responsibilities",
      "items": [
        "schema validation (rule JSON)",
        "field_key existence check",
        "type/operator/value compatibility",
        "answers normalization",
        "safe fallback on failure",
        "audit/processing logs (min PII)"
      ]
    },
    {
      "type": "list",
      "title": "apply_points",
      "items": [
        "public GET: return initial computed state",
        "step transition: re-evaluate on API (double defense)",
        "final submit: re-evaluate, finalize required/store targets"
      ]
    },
    {
      "type": "code",
      "language": "pseudo",
      "text": "入力: form_definition, answers_raw, current_step?\n(1) answers = normalize(answers_raw, form_definition)  // 型・配列・トリム等\n(2) validate_form_rules(form_definition)               // publish 時に実施が理想（実行時はキャッシュ）\n(3) visibility_map = eval_all_fields(visibility_rule, answers)\n(4) required_map   = eval_all_fields(required_rule, answers) with visibility_map gating\n(5) if step_mode:\n      can_transition = eval_step_transition(current_step.transition_rule, answers)\n(6) apply_policy:\n      - visibility=false -> hidden\n      - required=false   -> not required\n      - hidden field     -> (default) do_not_store\n(7) on submit:\n      - validate required visible fields\n      - persist snapshots for stored fields only\n      - dispatch async jobs (mail/slack/pdf) after commit (v1.1)"
    }
  ]
}
```

## エラー設計

_Source files:_ latest/other/reforma-notes-v1.0.0-条件分岐-実装整理パック-.json.json

```json
{
  "id": "error_response_design",
  "title": "エラー設計",
  "blocks": [
    {
      "type": "kv",
      "title": "envelope",
      "items": {
        "success": "boolean",
        "data": "object|null",
        "message": "string|null",
        "errors": "object|null"
      }
    },
    {
      "type": "table",
      "title": "status_codes",
      "columns": [
        "category",
        "http",
        "code",
        "errors_shape",
        "note"
      ],
      "rows": [
        [
          "config_validation",
          422,
          "CONDITION_RULE_INVALID",
          "errors.rule / errors.items[n]",
          "save/publish blocked"
        ],
        [
          "input_validation",
          422,
          "VALIDATION_ERROR",
          "errors.fields.{field_key}",
          "visible+required only"
        ],
        [
          "step_transition_denied",
          422,
          "STEP_TRANSITION_DENIED",
          "errors.step",
          "deny_with_error"
        ],
        [
          "runtime_eval_error",
          "200 or 422",
          "CONDITION_EVAL_ERROR",
          "errors.rule(optional)",
          "safe fallback; step->422"
        ]
      ]
    },
    {
      "type": "code",
      "language": "json",
      "text": "// STEP 次へ遷移が拒否された例（422）\n{\n  \"success\": false,\n  \"data\": null,\n  \"message\": \"次へ進む条件を満たしていません。\",\n  \"errors\": {\n    \"code\": \"STEP_TRANSITION_DENIED\",\n    \"step\": {\n      \"step_key\": \"step2\",\n      \"rule\": { \"...\": \"transition_rule(JSON)\" }\n    }\n  }\n}\n\n// ルールが不正で保存できない例（422）\n{\n  \"success\": false,\n  \"data\": null,\n  \"message\": \"条件分岐ルールに誤りがあります。\",\n  \"errors\": {\n    \"code\": \"CONDITION_RULE_INVALID\",\n    \"rule\": {\n      \"path\": \"fields[3].visibility_rule.items[1].field\",\n      \"reason\": \"unknown_field_key\"\n    }\n  }\n}"
    }
  ]
}
```

## React / E2E チェック

_Source files:_ latest/other/reforma-notes-v1.0.0-条件分岐-実装整理パック-.json.json

```json
{
  "id": "frontend_e2e",
  "title": "React / E2E チェック",
  "blocks": [
    {
      "type": "object",
      "title": "ui_builder_constraints",
      "value": {
        "max_conditions": 10,
        "max_nesting": 1
      }
    },
    {
      "type": "list",
      "title": "builder_checks",
      "items": [
        "explicit AND/OR shown",
        "max_nesting=1 enforced",
        "max_conditions=10 enforced",
        "no self reference",
        "operator filtered by field type",
        "value input UI per operator",
        "toggle off => store null/undefined"
      ]
    },
    {
      "type": "list",
      "title": "e2e_min",
      "items": [
        "E2E-01 builder save/reload JSON stable",
        "E2E-02 exclusive_with required",
        "E2E-03 nesting limit",
        "E2E-04 visibility apply",
        "E2E-05 required + 422",
        "E2E-06 step deny + 422",
        "E2E-07 invalid config => safe fallback"
      ]
    }
  ]
}
```

## reforma-notes-v1.0.0-条件分岐-評価結果IF-.json

_Source files:_ latest/other/reforma-notes-v1.0.0-条件分岐-評価結果IF-.json.json

```json
{
  "meta": {
    "title": "ReForma 条件分岐 評価結果I/F 定義（API→UI）",
    "version": "1.0",
    "generated_at": "2026-01-12T15:50:25.108877",
    "timezone": "Asia/Tokyo",
    "depends_on": {
      "A-06": "form-feature-attachments-v1.1.json#/A-06_condition_branch_rules",
      "UI_spec": "condition-ui-spec-v1.0.json"
    }
  },
  "schemas": {
    "FieldConditionState": {
      "visible": "boolean",
      "required": "boolean",
      "store": [
        "store",
        "do_not_store"
      ],
      "eval": [
        "ok",
        "fallback",
        "error"
      ],
      "reasons": {
        "optional": true,
        "item": {
          "kind": [
            "rule",
            "type",
            "missing_field",
            "unknown_operator"
          ],
          "path": "string?",
          "message": "string?"
        }
      }
    },
    "StepTransitionState": {
      "can_transition": "boolean",
      "eval": [
        "ok",
        "fallback",
        "error"
      ],
      "message": "string?",
      "reasons": "Reason[]?"
    },
    "ConditionState": {
      "version": "1",
      "evaluated_at": "ISO8601 string",
      "fields": "map(field_key -> FieldConditionState)",
      "step": "StepTransitionState?"
    }
  },
  "where_to_return": [
    {
      "api": "public form GET",
      "path": "data.condition_state",
      "purpose": "initial render"
    },
    {
      "api": "step transition",
      "path": "success: data.condition_state / fail: errors.step",
      "purpose": "double defense"
    },
    {
      "api": "final submit",
      "path": "optional: data.condition_state (debug)",
      "purpose": "audit/diagnostic"
    }
  ],
  "examples": {
    "public_get": "// 公開フォーム GET の例（抜粋）\n{\n  \"success\": true,\n  \"data\": {\n    \"form\": { \"...\": \"...\" },\n    \"condition_state\": {\n      \"version\": \"1\",\n      \"evaluated_at\": \"2026-01-13T00:00:00+09:00\",\n      \"fields\": {\n        \"company_name\": { \"visible\": true, \"required\": true, \"store\": \"store\", \"eval\": \"ok\" },\n        \"tel\": { \"visible\": false, \"required\": false, \"store\": \"do_not_store\", \"eval\": \"ok\" }\n      }\n    }\n  }\n}",
    "step_denied": "// STEP 次へ遷移 NG（422）の例\n{\n  \"success\": false,\n  \"data\": null,\n  \"message\": \"次へ進む条件を満たしていません。\",\n  \"errors\": {\n    \"code\": \"STEP_TRANSITION_DENIED\",\n    \"step\": {\n      \"can_transition\": false,\n      \"eval\": \"ok\",\n      \"message\": \"必須項目が未入力です。\",\n      \"reasons\": [{ \"kind\":\"rule\", \"path\":\"steps[1].transition_rule\", \"message\":\"rule evaluated false\" }]\n    }\n  }\n}",
    "fallback": "// 評価不能（参照 field_key 不正）→ 安全側フォールバック例（成功レスポンス内）\n{\n  \"condition_state\": {\n    \"version\": \"1\",\n    \"evaluated_at\": \"2026-01-13T00:00:00+09:00\",\n    \"fields\": {\n      \"advanced_section\": {\n        \"visible\": false,\n        \"required\": false,\n        \"store\": \"do_not_store\",\n        \"eval\": \"fallback\",\n        \"reasons\": [{ \"kind\":\"missing_field\", \"path\":\"fields[7].visibility_rule.items[0].field\", \"message\":\"unknown_field_key\" }]\n      }\n    }\n  }\n}"
  },
  "notes": [
    "UI は reasons/eval の有無に依存しない（任意項目）。",
    "評価不能時は A-06 conventions の安全側に倒す。",
    "v1.x は max_nesting=1 をUI/API双方で強制。"
  ],
  "raw_refs": {
    "a06_conventions": {
      "explicit_logical_ops": true,
      "undefined_field_key": "configuration_error",
      "fallback_on_failure": [
        "hide",
        "not_required",
        "deny_transition"
      ]
    },
    "ui_constraints": {
      "max_conditions": 10,
      "max_nesting": 1
    }
  }
}
```

## reforma-notes-v1.0.0-追補パッチ-表示モード-テーマ-計算フィールド-.json

_Source files:_ latest/other/reforma-notes-v1.0.0-追補パッチ-表示モード-テーマ-計算フィールド-.json.json

```json
{
  "meta": {
    "title": "ReForma 追補パッチ（表示モード / テーマ / 計算フィールド）",
    "version": "1.0",
    "generated_at": "2026-01-13T00:55:21.047728",
    "timezone": "Asia/Tokyo",
    "patch_type": "additive",
    "applies_to": [
      "form-feature-spec-v1.0.complete.json",
      "form-feature-attachments-v1.1.json",
      "03.ReForma-api-spec-v1.1-consolidated.json",
      "04.ReForma-db-spec-v1.1-consolidated.json"
    ]
  },
  "adds": [
    {
      "id": "SUPP-DISPLAY-MODE-001",
      "area": "display_mode",
      "recommended": {
        "name": "render_only + store_snapshot",
        "summary": "保存の正は value。UI表示は label/both を切替可能。保存時に label_snapshot を保持して再現性を担保。",
        "defaults": {
          "store_canonical": "value",
          "default_render_mode": "label",
          "allow_render_modes": [
            "label",
            "both",
            "value"
          ],
          "store_label_snapshot": true,
          "snapshot_locale_policy": "submission_locale_or_form_default"
        },
        "apply_points": {
          "render": [
            "公開フォーム: 選択肢表示（label/both/value）",
            "管理画面プレビュー: locale+mode切替",
            "ACK画面: labelを既定"
          ],
          "store": [
            "submit保存: canonical=valueを保存（value_json）",
            "label_snapshot: submission_values.label_json / field_label_snapshot に保存"
          ],
          "export": [
            "CSV: mode=both/value/label をパラメータ指定（既定both）",
            "PDF/ACK: 既定label（必要ならmode指定を追加可能）",
            "検索: canonical(value) と label_snapshot の両方に対応（A-02に委譲、既定はvalue優先）"
          ]
        }
      },
      "api_contract_additions": [
        {
          "endpoint": "POST /v1/forms/{form_key}/submit",
          "add_request_fields": {
            "locale": {
              "type": "string",
              "enum": [
                "ja",
                "en"
              ],
              "optional": true
            },
            "mode": {
              "type": "string",
              "enum": [
                "both",
                "value",
                "label"
              ],
              "optional": true,
              "note": "保存の正はvalue固定。modeはACK/出力の表示方針用に限定。"
            }
          },
          "add_response_fields": {
            "condition_state": {
              "ref": "ConditionState",
              "required": false
            }
          }
        }
      ],
      "data_model_additions": [
        {
          "table": "submission_values",
          "fields": {
            "value_json": "canonical value (already planned)",
            "label_json": "label snapshot (JSON, optional)",
            "field_label_snapshot": "field label snapshot (string, optional)"
          },
          "note": "既にDB仕様のスナップショット方針がある前提。無ければ追補で追加。"
        }
      ]
    },
    {
      "id": "SUPP-THEME-001",
      "area": "theming",
      "recommended": {
        "name": "theme_tokens_only + template_pack",
        "summary": "v1.xは安全にテーマトークン（CSS変数）とプリセットテーマ選択で提供。外部CSS URLはv2候補。",
        "defaults": {
          "theme_id": "default",
          "theme_tokens_schema": {
            "color_primary": "#xxxxxx",
            "color_secondary": "#xxxxxx",
            "color_bg": "#xxxxxx",
            "color_text": "#xxxxxx",
            "radius": "0|4|8|12",
            "spacing_scale": "sm|md|lg",
            "font_family": "system|noto_sans|custom (v2)",
            "button_style": "solid|outline",
            "input_style": "standard|filled"
          },
          "csp_policy": {
            "allow_external_css": false,
            "style_src": [
              "'self'"
            ],
            "font_src": [
              "'self'"
            ],
            "img_src": [
              "'self'",
              "data:"
            ]
          }
        },
        "ui_application": [
          "公開フォーム root に data-theme-id を付与",
          "theme_tokens を CSS variables に展開（:root ではなくフォームコンテナ配下）",
          "プリセットテーマはフロントに同梱（またはAPIから取得）"
        ]
      },
      "api_contract_additions": [
        {
          "endpoint": "GET /v1/forms/{id}",
          "add_response_fields": {
            "theme_id": {
              "type": "string",
              "required": false
            },
            "theme_tokens": {
              "type": "object",
              "required": false
            }
          }
        },
        {
          "endpoint": "PUT /v1/forms/{id}",
          "add_request_fields": {
            "theme_id": {
              "type": "string",
              "optional": true
            },
            "theme_tokens": {
              "type": "object",
              "optional": true
            }
          }
        }
      ],
      "data_model_additions": [
        {
          "table": "forms",
          "fields": {
            "theme_id": "string nullable",
            "theme_tokens": "json nullable"
          }
        }
      ],
      "out_of_scope_v1x": [
        "任意の外部CSS URL指定（安全/運用のため v2で検討）",
        "任意HTML埋め込み"
      ]
    },
    {
      "id": "SUPP-COMPUTED-001",
      "area": "computed_field",
      "recommended": {
        "name": "readonly_input + built_in_functions + store_snapshot + api_recompute",
        "summary": "v1.xは計算結果をreadonlyフィールドとして表示。式は関数プリセット。送信時にAPIが再計算して確定・保存。",
        "defaults": {
          "presentation": "readonly_input",
          "persistence": "store_snapshot",
          "engine": "built_in_functions",
          "max_dependency_depth": 1,
          "cycle_detection": true,
          "on_error_policy": {
            "display": "blank",
            "required": false,
            "store": "do_not_store"
          }
        },
        "built_in_functions": [
          {
            "fn": "sum",
            "args": "refs[]"
          },
          {
            "fn": "multiply",
            "args": "ref_a, ref_b"
          },
          {
            "fn": "tax",
            "args": "ref_amount, rate"
          },
          {
            "fn": "round",
            "args": "ref_value, digits"
          },
          {
            "fn": "min",
            "args": "refs[]"
          },
          {
            "fn": "max",
            "args": "refs[]"
          },
          {
            "fn": "if",
            "args": "condition, then, else"
          }
        ]
      },
      "form_definition_additions": [
        {
          "field_type": "computed",
          "schema": {
            "type": "computed",
            "field_key": "TOTAL",
            "label": {
              "ja": "合計",
              "en": "Total"
            },
            "result_type": "number|string",
            "format": "integer|decimal|currency",
            "computed_rule": {
              "engine": "built_in_functions",
              "fn": "sum",
              "args": [
                "ref:PRICE",
                "ref:TAX"
              ],
              "fallback": {
                "on_error": "blank",
                "store": "do_not_store"
              }
            },
            "is_required": false,
            "is_readonly": true
          }
        }
      ],
      "api_behavior": [
        "公開フォームUIでも即時計算して表示してよい（UX向上）",
        "submit時はAPIで再計算し、クライアント送信値は信用しない（上書き）",
        "保存は submission_values に value_json として保存（必要なら label_json も）"
      ],
      "validation_rules": [
        "computed_field はユーザ入力を受け取らない（payloadのanswersに含まれても無視/上書き）",
        "参照先 field_key の存在・型整合・循環を RuleValidator で検証（保存/Publish時）"
      ]
    }
  ]
}
```

## reforma-notes-v1.0.0

_Source files:_ latest/other/reforma-notes-v1.0.0.json

```json
{
  "title": "ReForma Frontend 補足仕様（SUP-FE）【統合・最新版】",
  "scope": "frontend-backend shared",
  "versioning_policy": "v1.0 specs immutable; extensions via SUP only",
  "sections": {
    "SUP-FE-001": {
      "title": "ZIP提供時のコマンド提示テンプレ",
      "commands": [
        "cd /var/www/reforma/frontend",
        "unzip -o reforma-react-vX.Y.Z-diff.zip -d .",
        "npm install  # or npm ci if lock updated",
        "npm run build:stg  # production: build:prd"
      ]
    },
    "SUP-FE-002": {
      "title": "リリース差分ZIP作成時のメタ情報更新",
      "checks": [
        "package.json version",
        "package-lock.json version (if exists)",
        "CHANGELOG.md latest on top",
        "verify build version output"
      ]
    },
    "SUP-FE-003": {
      "title": "E-01 エラー画面 クエリ拡張",
      "error_codes": [
        "FORBIDDEN",
        "AUTH_FAILED",
        "NOT_FOUND",
        "VALIDATION_ERROR",
        "UNKNOWN"
      ]
    },
    "SUP-FE-004": {
      "title": "E-01 Debug UI",
      "debug_modes": [
        "VITE_DEBUG",
        "VITE_DEBUG_UI",
        "?debug=1"
      ],
      "payload_transport": "navigate state.debugPayload"
    },
    "SUP-FE-005": {
      "title": "ReForma テーマ背景（全ページ共通）",
      "policy": "Use v0.4.11 Not Found gradient for all pages under ReForma theme"
    },
    "SUP-FE-006": {
      "title": "アカウント管理画面 追加方針",
      "screens": [
        "S-02",
        "S-03",
        "S-04",
        "S-05"
      ],
      "access": "System Admin only"
    },
    "SUP-FE-007": {
      "title": "管理アカウント管理（招待制）",
      "invite": {
        "ttl_hours": 72,
        "single_use": true,
        "resend_policy": "new token, invalidate old",
        "rate_limit": {
          "min_interval_sec": 60,
          "per_hour": 5,
          "per_day": 20
        }
      },
      "status": [
        "invited",
        "active",
        "disabled"
      ],
      "root_admin": {
        "seeded": true,
        "immutable": [
          "disable",
          "delete"
        ]
      },
      "safety_rules": [
        "cannot disable self",
        "cannot downgrade own role from system_admin",
        "system_admin count cannot be zero"
      ],
      "password_policy": {
        "min_length": 8,
        "require": [
          "lowercase",
          "uppercase",
          "digit",
          "symbol"
        ],
        "configurable": true,
        "lock": {
          "failures": 3,
          "lock_minutes": 15,
          "configurable": true
        }
      },
      "session": {
        "ttl": "configurable"
      },
      "csv_import": {
        "mode": "A",
        "columns": [
          "email",
          "name",
          "role",
          "status",
          "note"
        ],
        "duplicate_email": "error_and_rollback",
        "result_report": true,
        "bulk_invite_ui": true
      },
      "audit_log": "admin_audit_logs"
    },
    "SUP-FE-008": {
      "title": "Respondent 管理（ハイブリッド方式）",
      "model": [
        "respondent_profiles",
        "form_respondents"
      ],
      "profile": {
        "display_name": "required",
        "email": "nullable_unique",
        "external_ref": "unique"
      },
      "form_flow": [
        "login_or_register",
        "email_verify",
        "redirect_to_form"
      ],
      "auth": {
        "session_based": true,
        "policy_shared_with_admin": true
      }
    }
  }
}
```

## reforma-notes-v1.0.0

_Source files:_ latest/other/reforma-notes-v1.0.0.md

# ReForma 追補仕様まとめ（表示モード / テーマ / 計算フィールド）

_generated: 2026-01-13T00:55:21.047728 (Asia/Tokyo)_

## display_mode – render_only + store_snapshot

**概要**: 保存の正は value。UI表示は label/both を切替可能。保存時に label_snapshot を保持して再現性を担保。

### 推奨設定
```json

{
  "store_canonical": "value",
  "default_render_mode": "label",
  "allow_render_modes": [
    "label",
    "both",
    "value"
  ],
  "store_label_snapshot": true,
  "snapshot_locale_policy": "submission_locale_or_form_default"
}

```

## theming – theme_tokens_only + template_pack

**概要**: v1.xは安全にテーマトークン（CSS変数）とプリセットテーマ選択で提供。外部CSS URLはv2候補。

### 推奨設定
```json

{
  "theme_id": "default",
  "theme_tokens_schema": {
    "color_primary": "#xxxxxx",
    "color_secondary": "#xxxxxx",
    "color_bg": "#xxxxxx",
    "color_text": "#xxxxxx",
    "radius": "0|4|8|12",
    "spacing_scale": "sm|md|lg",
    "font_family": "system|noto_sans|custom (v2)",
    "button_style": "solid|outline",
    "input_style": "standard|filled"
  },
  "csp_policy": {
    "allow_external_css": false,
    "style_src": [
      "'self'"
    ],
    "font_src": [
      "'self'"
    ],
    "img_src": [
      "'self'",
      "data:"
    ]
  }
}

```

## computed_field – readonly_input + built_in_functions + store_snapshot + api_recompute

**概要**: v1.xは計算結果をreadonlyフィールドとして表示。式は関数プリセット。送信時にAPIが再計算して確定・保存。

### 推奨設定
```json

{
  "presentation": "readonly_input",
  "persistence": "store_snapshot",
  "engine": "built_in_functions",
  "max_dependency_depth": 1,
  "cycle_detection": true,
  "on_error_policy": {
    "display": "blank",
    "required": false,
    "store": "do_not_store"
  }
}

```

### フォーム定義追加例
```json

[
  {
    "field_type": "computed",
    "schema": {
      "type": "computed",
      "field_key": "TOTAL",
      "label": {
        "ja": "合計",
        "en": "Total"
      },
      "result_type": "number|string",
      "format": "integer|decimal|currency",
      "computed_rule": {
        "engine": "built_in_functions",
        "fn": "sum",
        "args": [
          "ref:PRICE",
          "ref:TAX"
        ],
        "fallback": {
          "on_error": "blank",
          "store": "do_not_store"
        }
      },
      "is_required": false,
      "is_readonly": true
    }
  }
]

```

### API挙動

- 公開フォームUIでも即時計算して表示してよい（UX向上）
- submit時はAPIで再計算し、クライアント送信値は信用しない（上書き）
- 保存は submission_values に value_json として保存（必要なら label_json も）


## reforma-notes-v1.1.0

_Source files:_ latest/other/reforma-notes-v1.1.0.json

```json
{
  "meta": {
    "title": "フォーム機能別表（Attachments） v1.0",
    "version": "1.1",
    "generated_at": "2026-01-12T14:46:31.478591",
    "links": {
      "parent_spec": "フォーム機能詳細仕様書 v1.0"
    },
    "updated_at": "2026-01-12T15:12:02.560114"
  },
  "A-01_csv_column_definition": {
    "modes": [
      "value",
      "label",
      "both"
    ],
    "common_columns": [
      {
        "col_key": "submission_id",
        "label_ja": "受付ID",
        "type": "string",
        "modes": [
          "value",
          "label",
          "both"
        ],
        "notes": "submissions.id"
      },
      {
        "col_key": "submitted_at",
        "label_ja": "受付日時",
        "type": "datetime",
        "modes": [
          "value",
          "label",
          "both"
        ],
        "notes": "submissions.created_at"
      },
      {
        "col_key": "form_code",
        "label_ja": "フォーム識別子",
        "type": "string",
        "modes": [
          "value",
          "label",
          "both"
        ],
        "notes": "forms.code"
      },
      {
        "col_key": "status",
        "label_ja": "ステータス",
        "type": "string",
        "modes": [
          "value",
          "label",
          "both"
        ],
        "notes": "submissions.status"
      }
    ],
    "field_column_naming": {
      "value_or_label_mode": "f:{field_key}",
      "both_mode": {
        "value": "f:{field_key}",
        "label": "f:{field_key}__label"
      }
    },
    "type_rules": {
      "text": {
        "value": "string",
        "label": "string"
      },
      "textarea": {
        "value": "string",
        "label": "string"
      },
      "email": {
        "value": "string",
        "label": "string"
      },
      "tel": {
        "value": "string",
        "label": "string"
      },
      "number": {
        "value": "number",
        "label": "number"
      },
      "select": {
        "value": "value",
        "label": "option_label_snapshot_or_translate"
      },
      "radio": {
        "value": "value",
        "label": "option_label_snapshot_or_translate"
      },
      "checkbox": {
        "value": "join(values, delimiter)",
        "label": "join(labels, delimiter)",
        "delimiter_configurable": true
      },
      "date": {
        "value": "iso",
        "label": "iso"
      },
      "time": {
        "value": "iso",
        "label": "iso"
      },
      "datetime": {
        "value": "iso",
        "label": "iso"
      },
      "terms": {
        "value": "boolean",
        "label": "agree_or_disagree_label",
        "label_configurable": true
      },
      "file": {
        "value": "filename_or_url",
        "label": "filename_or_url",
        "depends_on_setting": true
      }
    },
    "csv_rules": {
      "delimiter_default": ",",
      "escape": "rfc4180_like",
      "utf8_bom": "configurable"
    },
    "sample_headers": {
      "form": "CONTACT_2026",
      "mode": "both",
      "csv_header": [
        "submission_id",
        "submitted_at",
        "form_code",
        "status",
        "f:name",
        "f:name__label",
        "f:email",
        "f:category",
        "f:category__label",
        "f:message"
      ],
      "sample_row": [
        "12345",
        "2026-01-12 20:15",
        "CONTACT_2026",
        "received",
        "ishida",
        "石田",
        "email@example.com",
        "inq",
        "お問い合わせ",
        "テストです"
      ]
    }
  },
  "A-02_search_rule_matrix": {
    "default_combine": "AND",
    "type_operators": [
      {
        "field_type": "text/textarea/email/tel",
        "operators": [
          "contains"
        ],
        "value_source": "submission_values.value",
        "index_hint": [
          "LIKE_now",
          "FULLTEXT_future"
        ]
      },
      {
        "field_type": "number",
        "operators": [
          "eq",
          "min",
          "max",
          "between"
        ],
        "value_source": "submission_values.value(normalized)",
        "index_hint": [
          "(field_id,value)"
        ]
      },
      {
        "field_type": "date/datetime",
        "operators": [
          "from",
          "to",
          "between"
        ],
        "value_source": "submission_values.value(iso)",
        "index_hint": [
          "(field_id,value)"
        ]
      },
      {
        "field_type": "select/radio",
        "operators": [
          "eq",
          "in"
        ],
        "value_source": "submission_values.value",
        "index_hint": [
          "(field_id,value)"
        ]
      },
      {
        "field_type": "checkbox",
        "operators": [
          "any_in(default)",
          "all_in(optional)"
        ],
        "value_source": "submission_values.value(array_or_joined)",
        "index_hint": [
          "consider_json_storage_future"
        ]
      },
      {
        "field_type": "terms",
        "operators": [
          "eq"
        ],
        "value_source": "submission_values.value(boolean)",
        "index_hint": [
          "(field_id,value)"
        ]
      }
    ],
    "checkbox_defaults": {
      "operator": "any_in",
      "all_in": "future_extension"
    }
  },
  "A-03_pdf_block_mapping": {
    "block_key_naming": {
      "field": "f:{field_key}",
      "system": [
        "sys:submitted_at",
        "sys:submission_id",
        "sys:form_code"
      ]
    },
    "mapping": [
      {
        "block_key": "sys:submitted_at",
        "source": "submissions.created_at",
        "fallback": null,
        "notes": "受付日時"
      },
      {
        "block_key": "sys:submission_id",
        "source": "submissions.id",
        "fallback": null,
        "notes": "受付ID"
      },
      {
        "block_key": "sys:form_code",
        "source": "forms.code",
        "fallback": null,
        "notes": "フォーム識別子"
      },
      {
        "block_key": "f:{field_key}",
        "source": "submission_values.value",
        "fallback": "empty",
        "notes": "型により整形"
      },
      {
        "block_key": "f:{field_key}__label",
        "source": "option_label_snapshot",
        "fallback": "translate",
        "notes": "選択系のみ"
      }
    ],
    "note": "Coordinates/fonts/layout are managed in template assets; this table defines data mapping only.",
    "sample_template_mapping": {
      "template": "contact_default_v1",
      "blocks": [
        {
          "block_key": "sys:submitted_at",
          "label": "受付日時",
          "note": "header"
        },
        {
          "block_key": "f:name__label",
          "label": "氏名",
          "note": "prefer label"
        },
        {
          "block_key": "f:email",
          "label": "メールアドレス"
        },
        {
          "block_key": "f:category__label",
          "label": "お問い合わせ種別"
        },
        {
          "block_key": "f:message",
          "label": "内容",
          "note": "multiline"
        }
      ]
    }
  },
  "A-04_notification_template_variables": {
    "rules": {
      "allowed_variables_only": true,
      "undefined_variable_behavior": "fail_and_audit_log"
    },
    "variables": [
      {
        "var": "{{form.code}}",
        "meaning": "フォーム識別子",
        "example": "CONTACT_2026"
      },
      {
        "var": "{{form.title}}",
        "meaning": "フォーム名（送信時表示言語）",
        "example": "お問い合わせ",
        "notes": "snapshot preferred"
      },
      {
        "var": "{{submission.id}}",
        "meaning": "受付ID",
        "example": "12345"
      },
      {
        "var": "{{submission.submitted_at}}",
        "meaning": "受付日時",
        "example": "2026-01-12 20:15",
        "notes": "server time"
      },
      {
        "var": "{{confirm_url.ack}}",
        "meaning": "ACK 再表示URL",
        "example": "https://..."
      },
      {
        "var": "{{confirm_url.pdf}}",
        "meaning": "PDF 閲覧URL",
        "example": "https://..."
      },
      {
        "var": "{{fields.summary}}",
        "meaning": "主要項目の抜粋",
        "example": "氏名:...",
        "notes": "form setting (future extension)"
      }
    ],
    "field_access": {
      "value": "{{field.<field_key>}}",
      "label": "{{field_label.<field_key>}}"
    },
    "sample_templates": {
      "user_ja": {
        "body": "{{form.title}} を受け付けました。\\n受付ID：{{submission.id}}\\n受付日時：{{submission.submitted_at}}\\n\\n{{fields.summary}}\\n\\n{{confirm_url.ack}}"
      }
    }
  },
  "A-05_examples": {
    "hidden_field_retention_example": {
      "scenario": "department was entered then hidden; still need to keep value",
      "approach": "configure retention exception rule for field_key=department"
    },
    "notification_resend_example": {
      "scenario": "user did not receive email; resend",
      "approach": "system_admin triggers resend; queued; audit logged"
    },
    "pdf_regeneration_example": {
      "policy": "default forbidden",
      "allowed_when": "defined operationally (e.g., wrong template)",
      "actor": "system_admin (or root when root-only configured)",
      "execution": "async with audit"
    }
  },
  "A-06_condition_branch_rules": {
    "source": "Basic Spec v1.0 Appendix D (reconstructed)",
    "applies_to": [
      "visibility_rule",
      "required_rule",
      "step_transition_rule"
    ],
    "conventions": {
      "explicit_logical_ops": true,
      "undefined_field_key": "configuration_error",
      "fallback_on_failure": [
        "hide",
        "not_required",
        "deny_transition"
      ]
    },
    "format": {
      "version": "1",
      "op": "and|or|not|comparison",
      "items": "required for and/or",
      "field": "target field_key",
      "value": "comparison value"
    },
    "operators": [
      "eq",
      "ne",
      "in",
      "contains",
      "gt",
      "gte",
      "lt",
      "lte",
      "between",
      "exists",
      "and",
      "or",
      "not"
    ],
    "examples": {
      "visibility_rule": {
        "version": "1",
        "op": "eq",
        "field": "category",
        "value": "inq"
      },
      "required_rule": {
        "version": "1",
        "op": "exists",
        "field": "company_name",
        "value": true
      },
      "step_transition_rule": {
        "version": "1",
        "op": "eq",
        "field": "terms",
        "value": true
      }
    },
    "apply": {
      "visibility_false": "hide_and_do_not_store",
      "required_false": "not_required",
      "transition_false": "deny_with_error"
    },
    "delegation": {
      "ui": "06.UI Spec",
      "api": "03.API Spec"
    }
  },
  "revision": [
    {
      "version": "1.1",
      "date": "2026-01-13",
      "description": "Added A-06 (reconstructed from Basic Spec v1.0 Appendix D). Added practical samples to A-01/A-03/A-04."
    },
    {
      "version": "1.0",
      "date": "2026-01-12",
      "description": "Initial release."
    }
  ]
}
```

## reforma-notes-v1.1.0

_Source files:_ latest/other/reforma-notes-v1.1.0.txt

最初に、添付の「共通仕様 正本（v1.3）」と OpenAPI / root-only policy を必ず読み込んでください。
記載内容以外の前提を勝手に追加せず、共通仕様を最優先して実装・調整してください。

【必読（正本）】
1. reforma-frontend-common-ui-spec-v1.3.json（画面共通仕様・確定版/単一正本）
2. openapi-reforma-v1.1-full.updated.yaml（OpenAPI 正本）
3. reforma-root-only-policy-v1.0.json（root-only policy 正本）

【優先順位（矛盾が出た場合）】
共通画面仕様 v1.3 ＞ 画面仕様書 ＞ API仕様書
※ 画面要件を満たすために API 側を調整する方針

【フロント側の前提（共通仕様 v1.3 の要点）】
- 認証/権限の正本は /auth/me
  - RBAC：roles[]
  - root-only：is_root
- root-only の拒否は 403 + errors.reason=ROOT_ONLY を必須（通常403と区別表示する）
- APIエラー（非422）の正規化：
  - 基本エラーページ：/reforma/error
  - 400/403/409：トーストで表示する想定
  - 500/503：エラーページへ遷移する想定
  - raw error は Debug UI（VITE_DEBUG=true の時のみ）に出す。通常画面には出さない。
- 破壊的操作（削除等）は確認ダイアログ必須。
  - root権限のみ実行可能な削除は「対象ID入力（完全一致）」を必須とする。
- CSV/PDF/ファイル操作は進捗表示（プログレスバー）を前提とするため、可能なら進捗取得エンドポイント等を用意してほしい。
- 日時/数値/IDの扱い（宣言）：
  - 日時：APIはISO8601（UTCまたはTZ明示）、表示整形はフロント
  - 数値：APIは生値、表示整形はフロント
  - ID：表示は生値、比較は完全一致（root削除確認に利用）

【今回の依頼（バックエンド側と調整したいこと）】
1) S-02 アカウント一覧（/v1/system/admin-users）の完成に向けた最終すり合わせ
   - page/per_page 必須、sort enum、q/role/status 等（OpenAPI 正本準拠）
2) 進捗表示が必要な処理（CSV/PDF/ファイル）の進捗取得方式（推奨：progress endpoint）
3) エラー構造（errors.reason / code / message 等）の確定（/reforma/error とトースト表示の分岐に必要）

不明点・矛盾・調整が必要な点が出た場合は、必ず指摘し、仕様（v1.3）側へフィードバックしてください。
