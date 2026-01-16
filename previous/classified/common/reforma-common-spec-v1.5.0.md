# ReForma common specification (merged)
- version: v1.5.0
- generated_at: 2026-01-14T11:37:59.905852+00:00

## Sources
- latest/common/reforma-common-spec-v1.2.0.json (v1.2.0)
- latest/common/reforma-common-spec-v1.3.0.json (v1.3.0)
- latest/common/reforma-common-spec-v1.3.0.md (v1.3.0)
- latest/common/reforma-common-spec-v1.5.0.json (v1.5.0)
- latest/common/reforma-common-spec-v1.5.0.md (v1.5.0)

---

## reforma-common-spec-v1.2.0

_Source files:_ latest/common/reforma-common-spec-v1.2.0.json

```json
{
  "handoff_type": "frontend_to_backend",
  "project": "ReForma",
  "scope": "common_ui_and_behavior",
  "frontend_common_spec_version": "1.2",
  "mandatory_read": [
    "reforma-frontend-common-ui-spec-v1.2.json"
  ],
  "priority_rules": {
    "screen_common_spec": "highest",
    "screen_spec": "second",
    "api_spec": "third"
  },
  "key_frontend_expectations": {
    "auth_source": "/auth/me",
    "rbac": "roles[]",
    "root_only": "is_root",
    "root_only_error": {
      "status": 403,
      "errors.reason": "ROOT_ONLY"
    }
  },
  "error_handling_contract": {
    "base_error_page": "/reforma/error",
    "toast_errors": [
      400,
      403,
      409
    ],
    "page_errors": [
      500,
      503
    ],
    "debug_raw_error": "only_when_VITE_DEBUG_true"
  },
  "destructive_action_policy": {
    "confirmation_required": true,
    "root_only_additional_rule": {
      "id_input_required": true,
      "exact_match": true
    }
  },
  "file_and_async_operations": {
    "progress_required": true,
    "preferred": "progress_endpoint",
    "fallback": "indeterminate_progress"
  },
  "date_number_format_policy": {
    "api": "raw_value",
    "frontend": "format_by_locale"
  },
  "notes": [
    "Do not introduce UI-side assumptions not described in common spec.",
    "Any deviation must be discussed and reflected back into the common spec."
  ]
}
```

## reforma-common-spec-v1.3.0

_Source files:_ latest/common/reforma-common-spec-v1.3.0.json

{
  "meta": {
    "name": "ReForma Frontend Common UI Specification",
    "version": "1.3",
    "status": "final",
    "scope": "all_screens",
    "purpose": "machine_share_single_source_of_truth",
    "notes": "This file consolidates v1.1, v1.2 and v1.3 into a single definitive common UI spec."
  },

  "priority_rules": {
    "order": [
      "frontend_common_ui_spec",
      "screen_spec",
      "api_spec"
    ],
    "note": "If inconsistencies occur, frontend common UI spec has highest priority."
  },

  "i18n": {
    "policy": "All user-facing texts must be multilingual (ja/en).",
    "exception": {
      "debug_ui": "Japanese only"
    },
    "resource_path": "src/i18n/"
  },

  "display_format_rules": {
    "datetime": {
      "api": "ISO8601",
      "timezone": "explicit_or_utc",
      "frontend_display": "format_by_locale"
    },
    "number": {
      "api": "raw_value",
      "frontend_display": "locale_format_with_separators"
    },
    "id": {
      "display": "raw_value",
      "comparison": "strict_match",
      "use_case": "root_destructive_confirmation"
    }
  },

  "breadcrumbs": {
    "enabled": true,
    "label_source": "screen_name",
    "use_screen_id": false,
    "i18n": true,
    "rule": "Breadcrumb label must be identical to screen title"
  },

  "screen_title": {
    "enabled": true,
    "label_source": "screen_name",
    "i18n": true,
    "display_name_override": {
      "allowed": true,
      "key": "display_screen_name"
    },
    "layout": {
      "separator_line_required": true,
      "description_area_optional": true
    }
  },

  "layout_common": {
    "sidebar": {
      "state_persistence": "localStorage",
      "storage_key": "reforma_sidebar_collapsed",
      "collapsed_style": "icon_only",
      "motif_icon_used": true,
      "file": "src/layout/AppLayout.tsx"
    },
    "top_controls": {
      "items": ["language", "theme"],
      "collapsible": true,
      "state_persistence": "localStorage",
      "mobile_behavior": "always_collapsed",
      "file": "src/components/TopControls.tsx"
    }
  },

  "theme": {
    "modes": ["system", "light", "dark", "reforma"],
    "reforma_icon": "motif_icon",
    "tooltip_policy": "operation_based",
    "persistence": "localStorage"
  },

  "language_switch": {
    "supported_locales": ["ja", "en"],
    "display_rule": {
      "ja": "日本語 / 英語",
      "en": "JA / EN"
    },
    "icon": {
      "type": "svg_tile",
      "path": "src/assets/lang-*-tile.svg"
    }
  },

  "list_screen_common": {
    "features": [
      "search(q)",
      "pagination(page, per_page)",
      "sort(enum, default_fixed)",
      "per_page_selector"
    ],
    "url_state_sync": true,
    "api_policy": "OpenAPI v1.1 list_policy"
  },

  "empty_state": {
    "enabled": true,
    "use_case": ["initial_empty", "search_no_result"],
    "ui_policy": {
      "icon": "common",
      "message": "i18n_required",
      "action_button": "optional"
    },
    "shared_component": {
      "name": "EmptyState",
      "file": "src/components/EmptyState.tsx"
    }
  },

  "loading_indicator": {
    "enabled": true,
    "policy": {
      "initial_load": "full_screen",
      "partial_load": "inline_or_overlay"
    },
    "shared_component": {
      "name": "LoadingOverlay",
      "file": "src/components/LoadingOverlay.tsx"
    }
  },

  "screen_guard": {
    "enabled": true,
    "auth_source": "/auth/me",
    "rbac_key": "roles[]",
    "root_only_key": "is_root",
    "guards": {
      "role": {
        "component": "RequireRole",
        "file": "src/guards/RequireRole.tsx"
      },
      "root_only": {
        "component": "RequireRoot",
        "file": "src/guards/RequireRoot.tsx"
      }
    },
    "policy": "Guard must be evaluated before API call and rendering"
  },

  "form_validation_error": {
    "enabled": true,
    "policy": {
      "display_position": "field_bottom",
      "one_message_per_field": true,
      "i18n_required": true,
      "api_422_mapping": true
    },
    "shared_component": {
      "name": "FormError",
      "file": "src/components/FormError.tsx"
    }
  },

  "api_error_handling": {
    "enabled": true,
    "base_error_page": "/reforma/error",
    "display_policy": {
      "toast": ["400", "403", "409"],
      "error_page": ["500", "503"],
      "root_only": {
        "condition": "errors.reason=ROOT_ONLY",
        "message_type": "dedicated"
      }
    },
    "debug_policy": {
      "when_debug": "show_raw_error_in_debug_ui",
      "otherwise": "hide_raw_error"
    },
    "shared_handler": {
      "name": "apiErrorHandler",
      "file": "src/utils/apiErrorHandler.ts"
    }
  },

  "success_notification": {
    "enabled": true,
    "policy": {
      "display_type": "toast",
      "frequency": "once_per_action",
      "message_style": "short_operation_form",
      "i18n_required": true
    },
    "shared_component": {
      "name": "ToastProvider",
      "file": "src/components/ToastProvider.tsx"
    }
  },

  "destructive_action_confirmation": {
    "enabled": true,
    "base_policy": {
      "dialog_required": true,
      "danger_style": true,
      "default_text": {
        "title": "confirm_delete",
        "description": "irreversible_operation"
      }
    },
    "root_only_additional_policy": {
      "id_input_required": true,
      "input_match_rule": "target_id_exact_match"
    },
    "shared_component": {
      "name": "ConfirmDialog",
      "file": "src/components/ConfirmDialog.tsx"
    }
  },

  "file_operation_progress": {
    "enabled": true,
    "target_operations": ["csv_export", "csv_import", "pdf_generate", "file_upload"],
    "display_policy": {
      "on_start": "loading_overlay",
      "progress_type": "progress_bar",
      "completion": {
        "success": "toast",
        "failure": "api_error_handling"
      }
    },
    "progress_source": {
      "preferred": "api_progress_endpoint",
      "fallback": "indeterminate_progress"
    },
    "shared_component": {
      "name": "ProgressOverlay",
      "file": "src/components/ProgressOverlay.tsx"
    }
  },

  "inline_help_text": {
    "enabled": true,
    "display_position": "below_screen_title",
    "style_policy": {
      "font_size": "small",
      "color": "muted",
      "icon_optional": true
    },
    "i18n_required": true
  },

  "tooltip_policy": {
    "style": "operation_based",
    "i18n_required": true
  },

## reforma-common-spec-v1.3.0

_Source files:_ latest/common/reforma-common-spec-v1.3.0.md

# ReForma フロントエンド 共通画面仕様 v1.3（確定版）

本書は ReForma フロントエンドにおける **全画面共通仕様の最終確定版** である。
v1.1 / v1.2 の内容をすべて統合している。

---

## 優先順位
画面挙動の優先順位は以下とする。

1. 共通画面仕様（本書 v1.3）
2. 画面仕様書
3. API仕様書

---

## 表示フォーマットの前提（宣言）

### 日時
- API：ISO8601（UTC または明示TZ）
- 表示：フロントエンドで locale に応じて整形

### 数値
- API：生値
- 表示：桁区切り等はフロントエンドで付与

### ID
- 表示：そのまま表示
- 比較：完全一致
- root 削除確認時の入力比較に使用

---

## 多言語化
- 全文言は多言語対応（ja/en）
- デバッグUIのみ日本語固定

---

## パンくず・画面タイトル
- 画面名を表示（画面IDは使用しない）
- パンくずと画面タイトルは同一文言
- 多言語対応
- タイトル下に区切り線、補足情報を表示可能

---

## レイアウト共通
### 左サイドバー
- 開閉状態は localStorage に保存
- 折りたたみ時はアイコン中心
- ReForma モチーフアイコンを使用

### 右上パネル（言語 / テーマ）
- 折りたたみ可能
- モバイルでは常時折りたたみ
- 言語表示：
  - 日本語UI：日本語 / 英語
  - 英語UI：JA / EN

---

## 一覧画面
- 検索 / ページング / 並び順 / 表示件数
- URL と状態同期
- OpenAPI v1.1 list_policy 準拠

---

## 空状態（Empty State）
- データ0件時は必ず表示
- 初期状態と検索結果なしを区別

---

## ローディング・進捗
- 初回ロード：全体ローディング
- 再取得：部分ローディング
- CSV / PDF 等はプログレスバーで進捗表示

---

## フォームエラー
- フィールド直下に表示
- API 422 と統合

---

## APIエラー（非422）
- 基本エラーページ：`/reforma/error`
- 400/403/409：トースト
- 500/503：エラーページ
- ROOT_ONLY：専用文言

---

## 成功通知
- トースト1回
- 短い操作形文言

---

## 破壊的操作（削除等）
- 確認ダイアログ必須
- root 権限操作では **対象IDの入力必須**

---

## 画面ガード
- 描画・API前に権限制御
- `/auth/me` を正本とする

---

## デバッグUI
- `VITE_DEBUG=true` のとき表示
- 画面下部に集約
- 文言は日本語のみ

---

以上。

## reforma-common-spec-v1.5.0

_Source files:_ latest/common/reforma-common-spec-v1.5.0.json

```json
{
  "meta": {
    "name": "ReForma Frontend Common UI Specification",
    "version": "1.5-updated",
    "status": "final",
    "generated_at": "2026-01-14T07:02:22Z",
    "supersedes": "1.5",
    "single_source_of_truth": true,
    "precedence": [
      "common_ui_spec_v1.5",
      "screen_spec",
      "api_spec"
    ],
    "policy": {
      "no_unwritten_assumptions": true,
      "api_adjustment_allowed_for_ui": true
    }
  },
  "auth_and_authorization": {
    "source_of_truth_endpoint": "/v1/auth/me",
    "fields": {
      "rbac_roles": "roles[]",
      "root_only_flag": "is_root"
    },
    "ui_decision_rules": [
      "UIは roles[] を正本として機能の表示/活性/操作可否を決定する",
      "UIは is_root を正本として root-only 操作の表示/活性/操作可否を決定する（最終防御はAPI）"
    ]
  },
  "api_base_configuration": {
    "env": {
      "VITE_API_BASE": "/reforma/api/",
      "VITE_API_VERSION": "v1"
    },
    "rule": "API URL は VITE_API_BASE + VITE_API_VERSION を結合したものを正とする"
  },
  "error_handling": {
    "normalized_envelope": {
      "authoritative_keys": {
        "classification": "code",
        "machine_reason": "errors.reason",
        "display_message": "message",
        "deprecated": [
          "errors.code"
        ]
      },
      "root_only_contract": {
        "http_status": 403,
        "errors_reason": "ROOT_ONLY",
        "must_distinguish_from_generic_403": true
      }
    },
    "navigation_policy": {
      "by_http_status": {
        "401": "redirect:/login",
        "404": "page:/reforma/not-found",
        "422": "inline-validation",
        "400": "toast",
        "403": "toast",
        "409": "toast",
        "429": "toast",
        "500": "page:/reforma/error",
        "503": "page:/reforma/error"
      },
      "rule": "画面遷移の正本は HTTP ステータス。code / errors.reason は補助判断に用いる"
    },
    "debug_ui": {
      "enabled_when": "VITE_DEBUG=true",
      "visible_fields_minimum": [
        "request_id",
        "endpoint",
        "errors.reason"
      ],
      "optional_fields": [
        "http_status",
        "code",
        "method",
        "timestamp"
      ],
      "raw_error_hidden_in_normal_ui": true
    }
  },
  "destructive_actions": {
    "confirm_dialog_required": true,
    "root_only_delete": {
      "frontend_id_confirmation": {
        "required": true,
        "match_rule": "完全一致（ID生値同士で比較）"
      },
      "backend_requirement": {
        "authorization": "root-only を必須（policyで担保）",
        "id_confirmation": "必須ではない（UI安全装置として扱う）"
      }
    }
  },
  "progress_and_exports": {
    "progress": {
      "endpoint": "/v1/progress/{job_id}",
      "expired_behavior": {
        "http_status": 404,
        "ui": "期限切れ表示（Not Found 画面内で説明）",
        "retry": "再実行導線を表示してよい"
      }
    },
    "exports": {
      "allow_resign_after_url_expired": true,
      "pdf_regeneration_policy": {
        "separate_regenerate_api": false,
        "regenerate_method": "元の生成開始APIを再実行（新job）",
        "note": "再署名(resign)と再生成(regenerate)を区別する"
      }
    }
  },
  "data_format_rules": {
    "datetime": {
      "api": "ISO8601（UTCまたはTZ明示）",
      "ui": "表示整形はフロント"
    },
    "number": {
      "api": "生値",
      "ui": "表示整形はフロント"
    },
    "id": {
      "display": "生値",
      "comparison": "完全一致"
    }
  },
  "user_attributes": {
    "exposed_in": [
      "/v1/auth/me",
      "/v1/system/admin-users (list)",
      "/v1/system/admin-users/{id} (detail)"
    ],
    "fields": {
      "is_root": "boolean",
      "form_create_limit_enabled": "boolean",
      "form_create_limit": {
        "type": "integer|null",
        "constraint": "enabled=true の場合 min=1（0は禁止）"
      }
    },
    "edit_location": "S-02 アカウント編集UI"
  },
  "change_log": [
    {
      "version": "1.5",
      "date": "2026-01-14",
      "changes": [
        "progress job TTL 超過時の UI 挙動（期限切れ表示）を明記",
        "PDF 再生成は当面別APIを作らない方針を明記",
        "画面遷移の正本を HTTP ステータスに統一",
        "Debug UI の最小表示項目を確定",
        "root-only 削除の ID 入力はフロント強制・認可は backend に限定"
      ]
    },
    {
      "version": "1.5-updated",
      "date": "2026-01-14",
      "changes": [
        "toast 表示文言の優先順位（message > errors.reason > code）を明記"
      ]
    }
  ],
  "ui_requirements": {
    "toast_message_priority": {
      "priority": [
        "message",
        "errors.reason",
        "code"
      ],
      "rule": "Toast 表示は message を最優先。message が無い場合に errors.reason を補助表示し、それも無い場合は code をフォールバックとして使用する。",
      "notes": [
        "errors.reason は機械判定が主用途。表示は ROOT_ONLY 等の限定ケースに留める。",
        "raw error（stack 等）は toast に表示しない。Debug UI のみで表示する。"
      ]
    }
  }
}
```

## reforma-common-spec-v1.5.0

_Source files:_ latest/common/reforma-common-spec-v1.5.0.md

# ReForma 画面共通仕様 v1.5-updated

本書は **画面共通仕様 v1.5** に、toast 表示文言の優先順位を明記した更新版です。

## Toast 表示文言の優先順位（確定）

Toast 表示は以下の優先順位で文言を決定する。

1. **`message`（最優先）**
2. **`errors.reason`（補助表示）**
3. **`code`（最終フォールバック）**

### 運用ルール
- `errors.reason` は機械判定が主用途。表示は ROOT_ONLY 等の限定ケースに留める。
- raw error（stack trace 等）は toast に表示しない。
- raw error の表示は Debug UI（`VITE_DEBUG=true`）に限定する。

### 擬似コード例

```ts
const toastText =
  error.message
  ?? mapReason(error.errors?.reason)
  ?? mapCode(error.code)
  ?? "処理に失敗しました";
```

## 変更履歴
- v1.5-updated (2026-01-14): toast 表示文言の優先順位を明記
