# ReForma frontend specification (merged)
- version: v0.9.0
- generated_at: 2026-01-19T00:00:00.000000+00:00
- updated_at: 2026-01-19T00:00:00.000000+00:00

**注意**: このMarkdownファイルの変更は、対応するJSONファイル（reforma-frontend-spec-v0.9.0.json）にも反映してください。

## 変更履歴

### v0.9.0 (2026-01-19)
- 条件分岐ビルダーUIの実装詳細を追加（F-03: フォーム項目設定）
- 表示モード機能の実装詳細を追加（公開フォーム画面、フォームプレビュー画面）
- 実装完了機能の反映

## Sources
- latest/frontend/reforma-frontend-spec-v0.3.0.json (v0.3.0)
- latest/frontend/reforma-frontend-spec-v0.5.8-frontend-handoff-.json.json (v0.5.8)
- latest/frontend/reforma-frontend-spec-v0.5.8.json (v0.5.8)
- latest/frontend/reforma-frontend-spec-v1.0.0-Frontend-共有テンプレ-.json.json (v1.0.0)
- latest/frontend/reforma-frontend-spec-v1.0.0-condition-operator-matrix-ui-.json.json (v1.0.0)
- latest/frontend/reforma-frontend-spec-v1.0.0-condition-ui-.json.json (v1.0.0)
- latest/frontend/reforma-frontend-spec-v1.0.0-condition-ui-examples-.json.json (v1.0.0)
- latest/frontend/reforma-frontend-spec-v1.0.0-frontend-chat-init.json.json (v1.0.0)
- latest/frontend/reforma-frontend-spec-v1.0.0-frontend-handoff-20260112.json.json (v1.0.0)
- latest/frontend/reforma-frontend-spec-v1.0.0.json (v1.0.0)
- latest/frontend/reforma-frontend-spec-v0.1.1.json (v0.1.1)

---

## メタデータ

_Source files:_ latest/frontend/reforma-frontend-spec-v0.3.0.json

```json
{
  "id": "meta",
  "title": "メタデータ",
  "blocks": [
    {
      "type": "kv",
      "items": {
        "document_name": "ReForma React 運用・画面UI仕様書",
        "target": "React（Vite/TS）フロントエンド（管理画面 + 公開フォーム関連）",
        "source_of_truth": "仕様書JSON（画面仕様書JSONの ui: fields/actions/columns 等）"
      }
    },
    {
      "type": "list",
      "title": "バージョン運用",
      "items": [
        "修正時はリビジョン（patch）のみインクリメント",
        "マイナー/メジャーはユーザー指示で変更",
        "例: v0.2.x 継続 → 次工程を v0.3.x"
      ]
    },
    {
      "type": "list",
      "title": "成果物提供方針",
      "items": [
        "git add / commit / push で提供",
        "変更/追加ファイルのみをコミット",
        "必要に応じてタグ付け"
      ]
    }
  ]
}
```

## 前提とスコープ

_Source files:_ latest/frontend/reforma-frontend-spec-v0.3.0.json

```json
{
  "id": "scope",
  "title": "前提とスコープ",
  "blocks": [
    {
      "type": "list",
      "title": "前提",
      "items": [
        "UI は Tailwind CSS を使用",
        "SPA（React Router）",
        "画面仕様書JSONを正として自動描画（共通レンダラ）",
        "Storybook 自動生成 + Playwright VRT（スナップショット比較）",
        "言語/テーマは cookie 優先（無ければブラウザ言語/OS設定）"
      ]
    },
    {
      "type": "list",
      "title": "スコープ",
      "items": [
        "管理画面（ログイン/ログアウト/ダッシュボード/一覧/詳細）",
        "公開フォーム（U-01）",
        "Debug UI（仕様書準拠の補足情報表示）"
      ]
    }
  ]
}
```

## 環境・デプロイ前提

_Source files:_ latest/frontend/reforma-frontend-spec-v0.3.0.json

```json
{
  "id": "env_deploy",
  "title": "環境・デプロイ前提",
  "blocks": [
    {
      "type": "kv",
      "title": "サーバ環境（参考）",
      "items": {
        "os": "Red Hat Enterprise Linux release 10.1 (Coughlan)",
        "httpd": "2.4.63-4",
        "php": "8.3.26-1",
        "mysql": "8.4.7-1",
        "aurora_mysql": "3.08.2"
      }
    },
    {
      "type": "list",
      "title": "Apache マウント構成",
      "items": [
        "React SPA: /reforma/ → /var/www/reforma/frontend/dist/",
        "Laravel API: /reforma/api/ → /var/www/reforma/backend/public/",
        "SPA fallback: /reforma/* は index.html に rewrite（/reforma/api/* は除外）"
      ]
    }
  ]
}
```

## 設定ファイル（.env）

_Source files:_ latest/frontend/reforma-frontend-spec-v0.3.0.json

```json
{
  "id": "dotenv",
  "title": "設定ファイル（.env）",
  "blocks": [
    {
      "type": "list",
      "title": "ファイル構成",
      "items": [
        ".env（デフォルト）",
        ".env.stg（staging: 3文字表記）",
        ".env.prd（production: 3文字表記）",
        ".env.example"
      ]
    },
    {
      "type": "kv",
      "title": "デフォルト値（例）",
      "items": {
        "VITE_ENV": "local",
        "VITE_BASE": "/reforma/",
        "VITE_API_BASE": "/reforma/api",
        "VITE_COPYRIGHT_OWNER": "ReForma",
        "VITE_COPYRIGHT_SINCE": "2026",
        "VITE_DEBUG": "true|false"
      }
    },
    {
      "type": "list",
      "title": "参照ルール",
      "items": [
        "vite build は mode に応じて .env.<mode> を参照",
        "STG ビルドは vite build --mode stg を使用"
      ]
    }
  ]
}
```

## 共通UI: 言語と表示モード

_Source files:_ latest/frontend/reforma-frontend-spec-v0.3.0.json

```json
{
  "id": "prefs",
  "title": "共通UI: 言語と表示モード",
  "blocks": [
    {
      "type": "object",
      "title": "言語",
      "value": {
        "supported": [
          "ja",
          "en"
        ],
        "toggle_label": {
          "ja_ui": "日 / 英",
          "en_ui": "JA / EN"
        },
        "priority": [
          "cookie",
          "browser_language"
        ]
      }
    },
    {
      "type": "object",
      "title": "表示モード（テーマ）",
      "value": {
        "modes": [
          "system",
          "light",
          "dark",
          "reforma"
        ],
        "behavior": {
          "system": "prefers-color-scheme に追従",
          "light": "Tailwind 公式配色準拠",
          "dark": "Tailwind 公式配色準拠",
          "reforma": "旧黒背景の ReForma テーマ"
        },
        "storage": "cookie",
        "ui": "segmented control（選択状態が明確）"
      }
    },
    {
      "type": "list",
      "title": "右上固定パネル",
      "items": [
        "言語/表示モード切替は右上固定パネル",
        "設定系ボタンは同パネルに追加",
        "全画面共通で利用"
      ]
    }
  ]
}
```

## ヘッダ / サイドバー / パンくず

_Source files:_ latest/frontend/reforma-frontend-spec-v0.3.0.json

```json
{
  "id": "layout",
  "title": "ヘッダ / サイドバー / パンくず",
  "blocks": [
    {
      "type": "list",
      "title": "ヘッダ",
      "items": [
        "ロゴ過多を避ける",
        "表示タイトルは title タグ文言を利用（言語切替に追従）"
      ]
    },
    {
      "type": "object",
      "title": "title タグ（全画面共通）",
      "value": {
        "ja": "ReForma（リフォルマ）- Flexible Form Management Platform",
        "other": "ReForma - Flexible Form Management Platform"
      }
    },
    {
      "type": "object",
      "title": "Breadcrumb（推奨）",
      "value": {
        "purpose": "現在地の把握",
        "pc": "ホーム / セクション / 画面名",
        "mobile": "省略（画面名中心）",
        "source": "画面仕様書の screen_id / label（定義は attachments 化可能）"
      }
    },
    {
      "type": "object",
      "title": "サイドバー",
      "value": {
        "pc": "常時表示",
        "mobile": "Drawer（ハンバーガーで開閉）",
        "copyright": "ログイン以外はサイドバー下部"
      }
    }
  ]
}
```

## 画面仕様（主要）

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0.json

```json
{
  "id": "screens",
  "title": "画面仕様（主要）",
  "blocks": [
    {
      "type": "object",
      "title": "A-01 ログイン画面",
      "value": {
        "top_right_panel": "言語/表示モード",
        "fields": [
          {
            "key": "login_id_email",
            "label": "ログイン ID（メールアドレス）"
          },
          {
            "key": "password",
            "label": "パスワード",
            "password_toggle": true
          }
        ],
        "layout": "縦並び（モバイル前提）",
        "validation": [
          "required",
          "email_format"
        ],
        "login_failed_message": "i18n 文言で表示",
        "from_ux": "state.from があれば戻り先案内（debugで詳細）",
        "footer": {
          "rule": "since〜現在年（同一年なら単年）",
          "owner_env": "VITE_COPYRIGHT_OWNER",
          "since_env": "VITE_COPYRIGHT_SINCE"
        }
      }
    },
    {
      "type": "object",
      "title": "A-02 ログアウト",
      "value": {
        "confirm_dialog": {
          "buttons": [
            "OK",
            "Cancel"
          ]
        }
      }
    },
    {
      "type": "object",
      "title": "ダッシュボード（ログイン後）",
      "value": {
        "id_rule": "screen_id ベース",
        "button_visibility": "light/dark/reforma で視認性確保",
        "layout": "メインはフル幅（右ペイン幅制限しない）"
      }
    },
    {
      "type": "object",
      "title": "一覧系（テーブル/カード）",
      "value": {
        "pc": "table",
        "mobile": "cards",
        "order": "actions は仕様書JSONの順序通り"
      }
    }
  ]
}
```

## Spec-driven 共通レンダラ

_Source files:_ latest/frontend/reforma-frontend-spec-v0.3.0.json

```json
{
  "id": "renderer",
  "title": "Spec-driven 共通レンダラ",
  "blocks": [
    {
      "type": "list",
      "title": "原則",
      "items": [
        "ui.fields / ui.actions / ui.columns を仕様書順で描画",
        "手書きUIを減らしデグレを防ぐ"
      ]
    },
    {
      "type": "list",
      "title": "レンダリング対象",
      "items": [
        "fields",
        "actions",
        "columns",
        "blocks（role別含む）"
      ]
    },
    {
      "type": "list",
      "title": "例外",
      "items": [
        "A-01 など UX が強い画面は spec を尊重しつつ手書き補強を許容"
      ]
    }
  ]
}
```

## Debug UI

_Source files:_ latest/frontend/reforma-frontend-spec-v0.3.0.json

```json
{
  "id": "debug_ui",
  "title": "Debug UI",
  "blocks": [
    {
      "type": "list",
      "title": "表示条件",
      "items": [
        "VITE_DEBUG=true で有効",
        "query(debug=1) は補助（最終判断は env）"
      ]
    },
    {
      "type": "list",
      "title": "表示内容",
      "items": [
        "screen_id / screen_key",
        "権限ロール/アクセス可否",
        "仕様書JSON抜粋（折り畳み + pre 整形）",
        "copy ボタン（JSON/画面情報）",
        "UI: Tailwind / Spec: JSON v1.0 は Debug UI に集約"
      ]
    },
    {
      "type": "list",
      "title": "見た目",
      "items": [
        "通常UIと区別できる枠/背景"
      ]
    }
  ]
}
```

## QA / 自動化

_Source files:_ latest/frontend/reforma-frontend-spec-v0.3.0.json

```json
{
  "id": "qa",
  "title": "QA / 自動化",
  "blocks": [
    {
      "type": "list",
      "title": "Spec Lint / Schema Validation",
      "items": [
        "npm run spec:lint で仕様書JSON検証",
        "スキーマは attachments 化可能（例: src/specs/schema.json）"
      ]
    },
    {
      "type": "list",
      "title": "Storybook 自動生成",
      "items": [
        "storybook:gen で仕様書更新→生成",
        "predev / prebuild で spec 変更時に自動生成（差分検知: SPEC_UNCHANGED 等）"
      ]
    },
    {
      "type": "list",
      "title": "Playwright VRT",
      "items": [
        "初回は --update-snapshots で snapshot 生成",
        "以降は差分検知"
      ]
    },
    {
      "type": "list",
      "title": "警告対応ポリシー",
      "items": [
        "重大（ビルド/実行阻害・セキュリティ）: 優先対応",
        "非重大（deprecation 等）: 影響評価の上、計画的に対応"
      ]
    }
  ]
}
```

## コマンド運用（ローカル/サーバ）

_Source files:_ latest/frontend/reforma-frontend-spec-v0.3.0.json

```json
{
  "id": "ops_commands",
  "title": "コマンド運用（ローカル/サーバ）",
  "blocks": [
    {
      "type": "list",
      "title": "展開〜反映（例）",
      "items": [
        "cd /var/www/reforma/frontend",
        "unzip -o <zip-file> -d ."
      ]
    },
    {
      "type": "list",
      "title": "クリーンインストール",
      "items": [
        "rm -rf node_modules dist .vite",
        "npm ci（lock あり） / npm install"
      ]
    },
    {
      "type": "list",
      "title": "ビルド（STG）",
      "items": [
        "npm run build:stg"
      ]
    },
    {
      "type": "list",
      "title": "Podman（Playwright）",
      "items": [
        "RHEL では apt-get が無いため Playwright の依存導入は Podman 前提",
        "コンテナ導入〜実行手順は運用手順として追記対象"
      ]
    }
  ]
}
```

## attachments（後で分離するもの）

_Source files:_ latest/frontend/reforma-frontend-spec-v0.3.0.json

```json
{
  "id": "attachments",
  "title": "attachments（後で分離するもの）",
  "blocks": [
    {
      "type": "attachments_index",
      "items": [
        {
          "key": "screen_spec_json",
          "description": "画面仕様書JSON（screen registry / ui schema）"
        },
        {
          "key": "json_schema",
          "description": "JSON Schema（Ajv 用）"
        },
        {
          "key": "breadcrumb_map",
          "description": "画面ID・パンくず階層定義"
        },
        {
          "key": "roles",
          "description": "role 定義（system_admin / form_admin / operator / viewer / public 等）"
        },
        {
          "key": "i18n_dict",
          "description": "i18n 文言辞書（ja/en）"
        },
        {
          "key": "supplement_spec_v1",
          "description": "補足仕様書 v1.0（パスワード表示ボタン必須、debug 表示仕様 等）"
        }
      ]
    }
  ]
}
```

## フォーム項目設定（F-03）

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0.json

```json
{
  "id": "section.screen.F-03.FORM_ITEM",
  "type": "screen",
  "screen_no": "F-03",
  "screen_id": "FORM_ITEM",
  "title": "フォーム項目設定",
  "role": "フォーム入力項目を定義する",
  "permissions": {
    "allow_roles": [
      "form_admin",
      "system_admin"
    ]
  },
  "route": {
    "path": "/forms/{form_id}/items"
  },
  "apis": [
    {
      "method": "GET",
      "path": "/api/v1/forms/{form_id}/items",
      "purpose": "項目一覧"
    },
    {
      "method": "POST",
      "path": "/api/v1/forms/{form_id}/items",
      "purpose": "項目作成"
    },
    {
      "method": "PUT",
      "path": "/api/v1/forms/{form_id}/items/{item_id}",
      "purpose": "項目更新"
    }
  ],
  "ui": {
    "item_fields": [
      {
        "key": "label_i18n",
        "required": true
      },
      {
        "key": "type",
        "required": true,
        "ref": "FORM_ITEM_TYPE_V1"
      },
      {
        "key": "required",
        "required": true
      },
      {
        "key": "options",
        "required_if": {
          "type_in": [
            "select",
            "radio",
            "checkbox"
          ]
        }
      }
    ],
    "conditional_display": {
      "rule_ref": "CONDITION_RULE_V1"
    },
    "condition_builder": {
      "component": "ConditionRuleBuilder",
      "features": [
        "複数条件の追加・削除（最大10個）",
        "AND/ORの論理結合を明示的に選択可能",
        "field type × operator 許可表の適用",
        "operator別 value_input UI",
        "バリデーション: 自己参照チェック、フィールド存在チェック"
      ],
      "rule_types": [
        "visibility_rule",
        "required_rule",
        "step_transition_rule"
      ],
      "implementation": {
        "file": "src/pages/forms/FormItemPage.tsx",
        "component_name": "ConditionRuleBuilder",
        "constraints": {
          "max_conditions": 10,
          "max_nesting": 1,
          "no_self_reference": true
        },
        "field_type_operators": {
          "text": ["eq", "ne", "contains", "exists", "not_empty", "empty"],
          "textarea": ["eq", "ne", "contains", "exists", "not_empty", "empty"],
          "email": ["eq", "ne", "contains", "exists", "not_empty", "empty"],
          "tel": ["eq", "ne", "contains", "exists", "not_empty", "empty"],
          "number": ["eq", "ne", "gt", "gte", "lt", "lte", "between", "exists", "not_empty", "empty"],
          "date": ["eq", "ne", "gt", "gte", "lt", "lte", "between", "exists", "not_empty", "empty"],
          "time": ["eq", "ne", "gt", "gte", "lt", "lte", "between", "exists", "not_empty", "empty"],
          "datetime": ["eq", "ne", "gt", "gte", "lt", "lte", "between", "exists", "not_empty", "empty"],
          "select": ["eq", "ne", "in", "exists", "not_empty", "empty"],
          "radio": ["eq", "ne", "in", "exists", "not_empty", "empty"],
          "checkbox": ["in", "exists", "not_empty", "empty"],
          "terms": ["eq", "ne", "exists", "not_empty", "empty"],
          "file": ["exists", "not_empty", "empty"],
          "hidden": ["eq", "ne", "exists", "not_empty", "empty"]
        },
        "operator_value_input": {
          "between": "最小値/最大値の2つの入力フィールド",
          "in": "カンマ区切りで複数値を入力可能",
          "exists/not_empty/empty": "値入力不要",
          "その他": "フィールドタイプに応じた入力タイプ（number, date, time, datetime-local, text）"
        }
      }
    }
  }
}
```

## フォームプレビュー（F-04）

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0.json

```json
{
  "id": "section.screen.F-04.FORM_PREVIEW",
  "type": "screen",
  "screen_no": "F-04",
  "screen_id": "FORM_PREVIEW",
  "title": "フォームプレビュー",
  "role": "公開前にフォームの表示・動作を確認する",
  "permissions": {
    "allow_roles": [
      "form_admin",
      "system_admin"
    ]
  },
  "route": {
    "path": "/forms/{form_id}/preview"
  },
  "apis": [
    {
      "method": "GET",
      "path": "/api/v1/forms/{form_id}/preview",
      "purpose": "プレビュー用データ"
    }
  ],
  "ui": {
    "behavior": [
      "read_only_preview"
    ],
    "display_mode": {
      "component": "DisplayModeSelector",
      "features": [
        "locale切替（利用可能な翻訳から選択）",
        "表示モード切替（label/both/value）",
        "選択肢フィールド（select/radio/checkbox）に適用"
      ],
      "implementation": {
        "file": "src/pages/forms/FormPreviewPage.tsx",
        "modes": [
          "label",
          "both",
          "value"
        ],
        "locale_source": "form.translations"
      }
    }
  }
}
```

## 公開フォーム画面（U-01）

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0.json

```json
{
  "id": "section.screen.U-01.FORM_VIEW",
  "type": "screen",
  "screen_no": "U-01",
  "screen_id": "FORM_VIEW",
  "title": "公開フォーム画面",
  "role": "一般利用者がフォーム入力を行う",
  "permissions": {
    "allow_roles": [
      "public"
    ]
  },
  "route": {
    "path": "/f/{form_key}"
  },
  "apis": [
    {
      "method": "GET",
      "path": "/api/v1/public/forms/{form_key}",
      "purpose": "公開フォーム定義取得"
    },
    {
      "method": "POST",
      "path": "/api/v1/public/forms/{form_key}/submit",
      "purpose": "回答送信"
    }
  ],
  "ui": {
    "fields_source": [
      {
        "ref": "FORM_ITEM_TYPE_V1"
      }
    ],
    "actions": [
      {
        "key": "submit"
      }
    ],
    "display_mode": {
      "component": "DisplayModeSelector",
      "features": [
        "表示モード切替（label/both/value）",
        "選択肢フィールド（select/radio/checkbox）に適用",
        "デフォルト: label"
      ],
      "implementation": {
        "file": "src/pages/public/PublicFormViewPage.tsx",
        "modes": [
          "label",
          "both",
          "value"
        ],
        "default_mode": "label",
        "note": "ACK画面での表示には、ACK APIのレスポンスに回答詳細を含める拡張が必要（将来の対応）"
      }
    }
  },
  "errors": [
    {
      "code": "VALIDATION_ERROR",
      "ref": "ERROR_CODES_V1"
    }
  ]
}
```
