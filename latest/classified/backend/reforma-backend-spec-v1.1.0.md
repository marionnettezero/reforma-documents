# ReForma backend specification (merged)
- version: v1.1.0
- generated_at: 2026-01-14T11:37:59.885164+00:00

## Sources
- latest/backend/reforma-backend-spec-v1.0.0-Backend-共有テンプレ-.json.json (v1.0.0)
- latest/backend/reforma-backend-spec-v1.0.0-backend-chat-init.json.json (v1.0.0)
- latest/backend/reforma-backend-spec-v1.0.0.json (v1.0.0)
- latest/backend/reforma-backend-spec-v1.1.0.json (v1.1.0)

---

## reforma-backend-spec-v1.0.0-Backend-共有テンプレ-.json

_Source files:_ latest/backend/reforma-backend-spec-v1.0.0-Backend-共有テンプレ-.json.json

```json
{
  "meta": {
    "title": "ReForma 開発チャット共有テンプレ（バックエンド）",
    "version": "1.0",
    "generated_at": "2026-01-12T16:56:01.989787",
    "timezone": "Asia/Tokyo",
    "target": "Laravel 12 Backend"
  },
  "versioning": {
    "rules": [
      "修正時はリビジョン（patch）のみインクリメント",
      "マイナー/メジャーはユーザー指示で変更",
      "例: v0.2.x 継続 → 次工程を v0.3.x"
    ]
  },
  "delivery_policy": {
    "method": "git add / commit / push",
    "rules": [
      "変更/追加ファイルのみをコミット",
      "必要に応じてタグ付け"
    ]
  },
  "paste_template": {
    "sections": [
      {
        "title": "前提",
        "body": [
          "本チャットは ReForma バックエンド（Laravel 12）実装フェーズの継続です。仕様の再検討はしません。",
          "正本仕様に従い「API実装」「条件分岐（A-06）評価」「ACK/PDF/通知/検索/権限」を実装に落とします。"
        ]
      },
      {
        "title": "正本仕様（必ず前提）",
        "body": [
          "01.ReForma-basic-spec-v1.1-consolidated.final.json",
          "02.ReForma-screen-spec-v1.1-consolidated.json",
          "03.ReForma-api-spec-v1.1-consolidated.json",
          "04.ReForma-db-spec-v1.1-consolidated.json",
          "05.ReForma-extension-spec-v1.1-consolidated.json",
          "condition-ui-spec-v1.0.json",
          "form-feature-attachments-v1.1.json（A-06が条件分岐の正本）",
          "form-feature-spec-v1.0.complete.json"
        ]
      },
      {
        "title": "重要な設計原則（厳守）",
        "body": [
          "条件分岐ルール正本は Attachments v1.1 / A-06",
          "UI は and/or を必ず明示（暗黙優先順位なし）",
          "評価不能時は安全側（非表示／必須解除／遷移不可）",
          "UIとAPIの二重防御（APIで最終確定）",
          "v1.x では条件ネスト 1段まで"
        ]
      },
      {
        "title": "今回の実装対象（APIカテゴリ）",
        "body": [
          "7.1 Auth",
          "7.2 Forms",
          "7.3 Submissions / Responses",
          "7.4 ACK / PDF",
          "7.7 Dashboard",
          "7.8 System Admin（SUP + root-only）"
        ]
      },
      {
        "title": "既に作成済みの成果物（このチャット生成物）",
        "body": [
          "openapi-reforma-v1.1-full.yaml / openapi-reforma-v1.1-full.json",
          "ReForma_Laravel12_最小実装設計_OpenAPIv1.1-full.json",
          "ReForma_条件分岐_評価結果IF_v1.0.json / .pdf"
        ]
      },
      {
        "title": "バックエンド側でまずやること（優先順）",
        "body": [
          "OpenAPI v1.1-full を source-of-truth として Laravel のルーティング/Controller/FormRequest/Service を起こす",
          "ConditionEvaluator（A-06）実装（安全側フォールバック、max_nesting=1）",
          "公開 submit / ack / 管理 responses / pdf を通す（E2E可能にする）",
          "RBAC（System Admin / Form Admin / Log Admin / root-only）を Gate/Policy で固定"
        ]
      },
      {
        "title": "出力してほしいもの",
        "body": [
          "実装雛形コード（Laravel 12）: routes/controllers/requests/services/policies/jobs/migrations",
          "APIのエラーレスポンス統一（envelope + code + fields/step/rule）",
          "ConditionState をレスポンスに載せる（公開submitなど）"
        ]
      }
    ]
  },
  "attachments_to_share": {
    "must_include": [
      {
        "file": "openapi-reforma-v1.1-full.yaml",
        "path": "sandbox:/mnt/data/openapi-reforma-v1.1-full.yaml",
        "purpose": "OpenAPI（実装可能な粒度）"
      },
      {
        "file": "openapi-reforma-v1.1-full.json",
        "path": "sandbox:/mnt/data/openapi-reforma-v1.1-full.json",
        "purpose": "OpenAPI（JSON版）"
      },
      {
        "file": "ReForma_Laravel12_最小実装設計_OpenAPIv1.1-full.json",
        "path": "sandbox:/mnt/data/ReForma_Laravel12_最小実装設計_OpenAPIv1.1-full.json",
        "purpose": "Laravel最小実装設計（routes/controllers/requests/services/policies/jobs）"
      },
      {
        "file": "ReForma_条件分岐_評価結果IF_v1.0.json",
        "path": "sandbox:/mnt/data/ReForma_条件分岐_評価結果IF_v1.0.json",
        "purpose": "ConditionState I/F（API→UI）"
      },
      {
        "file": "ReForma_条件分岐_評価結果IF_v1.0.pdf",
        "path": "sandbox:/mnt/data/ReForma_条件分岐_評価結果IF_v1.0.pdf",
        "purpose": "ConditionState I/F（PDF）"
      }
    ],
    "reference_specs": [
      "03.ReForma-api-spec-v1.1-consolidated.json（カテゴリ一覧）",
      "04.ReForma-db-spec-v1.1-consolidated.json（テーブル/関係/スナップショット）",
      "form-feature-attachments-v1.1.json（A-06 条件分岐）"
    ]
  }
}
```

## reforma-backend-spec-v1.0.0-backend-chat-init.json

_Source files:_ latest/backend/reforma-backend-spec-v1.0.0-backend-chat-init.json.json

```json
{
  "purpose": "ReForma Backend 開発チャット初期共有テンプレ",
  "role": "Backend single source of truth",
  "references": {
    "specs": [
      "01.ReForma 基本仕様書 v1.0",
      "02.ReForma 画面仕様書 v1.0",
      "03.ReForma API 仕様書 v1.0",
      "04.ReForma DB 仕様書 v1.0",
      "05.ReForma 拡張仕様書 v1.0 (+v1.1)",
      "06.ReForma React 運用・画面UI仕様書 v0.3"
    ],
    "sup": "ReForma Frontend 補足仕様（SUP-FE）【統合・最新版】"
  },
  "admin_users": {
    "invite": {
      "token": {
        "ttl_hours": 72,
        "single_use": true,
        "resend_new_token": true
      },
      "status": [
        "invited",
        "active",
        "disabled"
      ]
    },
    "security": {
      "password_policy": "admin/respondent 共通・設定変更可",
      "lock_policy": "失敗回数・ロック時間とも設定変更可",
      "session_ttl": "設定変更可"
    },
    "root_admin": {
      "seeded": true,
      "immutable": [
        "disable",
        "delete"
      ]
    }
  },
  "respondent": {
    "model": "hybrid",
    "profile": {
      "email": "nullable unique",
      "external_ref": "unique"
    },
    "flow": "login or register -> email verify -> redirect to form"
  }
}
```

## 補足仕様: API パス構成の正規化（/api 重複排除）

_Source files:_ latest/backend/reforma-backend-spec-v1.0.0.json

```json
{
  "rule": "External base /reforma/api/ + Laravel prefix /v1 => /reforma/api/v1/...",
  "implementation": {
    "laravel_routes_prefix": "/v1 (no /api prefix)",
    "apache_alias": "/reforma/api/ -> backend/public/"
  }
}
```

## 補足仕様: httpd（Apache）既存マウント構成への準拠

_Source files:_ latest/backend/reforma-backend-spec-v1.0.0.json

```json
{
  "react_mount": "/reforma/ -> frontend/dist/",
  "api_mount": "/reforma/api/ -> backend/public/",
  "app_url_recommended": "https://<host>/reforma/api",
  "notes": [
    "Keep Laravel standard .htaccess rewrite",
    "Avoid trailing slash mismatches in APP_URL"
  ]
}
```

## 補足仕様: セッション無効（401/419）扱い

_Source files:_ latest/backend/reforma-backend-spec-v1.0.0.json

```json
{
  "frontend": "401/419 => /logout?reason=session_invalid, invalidate state",
  "backend": [
    "401 for unauth",
    "419 may occur for CSRF/session; normalize to envelope"
  ]
}
```

## 推奨案（初期実装のベースライン提案）

_Source files:_ latest/backend/reforma-backend-spec-v1.0.0.json

```json
{
  "auth_admin": {
    "method": "Sanctum PAT",
    "ttl_days": 30,
    "rolling_extension": "once_per_day",
    "expired_code": "TOKEN_EXPIRED"
  },
  "auth_respondent": {
    "method": "session-based",
    "confirm_url_auth": "token-based"
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
    }
  },
  "pdf": {
    "storage": {
      "default": "s3",
      "fallback": "local"
    },
    "regeneration": "snapshot source, default no-regenerate, admin explicit regenerate with audit"
  },
  "confirm_url": {
    "types": {
      "confirm_submission": {
        "ttl": "24h",
        "one_time": true
      },
      "ack_action": {
        "ttl": "24h",
        "one_time": true
      },
      "view_pdf": {
        "ttl": "7d",
        "one_time": false
      }
    },
    "token_storage": "hash only in DB"
  },
  "settings": {
    "store": "DB settings table",
    "scope": "system",
    "ui": "future"
  }
}
```

## 確定事項（Backend 追加前提・2026-01-12）

_Source files:_ latest/backend/reforma-backend-spec-v1.0.0.json

```json
{
  "settings_scope": "system fixed",
  "pdf_storage": "S3 default, switchable to local",
  "respondent_scope": "browser may cross forms",
  "confirm_url_view_pdf_one_time": "default false, configurable"
}
```

## reforma-backend-spec-v1.1.0

_Source files:_ latest/backend/reforma-backend-spec-v1.1.0.json

```json
{
  "meta": {
    "title": "ReForma Backend 共有テンプレ（追補反映）",
    "version": "1.1",
    "generated_at": "2026-01-13T01:08:32.431777",
    "timezone": "Asia/Tokyo"
  },
  "paste_template": {
    "sections": [
      {
        "title": "前提",
        "body": [
          "本チャットは ReForma バックエンド（Laravel 12）実装フェーズの継続。仕様の再検討はしない。",
          "正本仕様＋追補パッチに従い API/条件分岐/表示モード/テーマ/計算フィールド を実装に落とす。"
        ]
      },
      {
        "title": "正本仕様（必ず前提）",
        "body": [
          "01.ReForma-basic-spec-v1.1-consolidated.final.json",
          "03.ReForma-api-spec-v1.1-consolidated.json",
          "04.ReForma-db-spec-v1.1-consolidated.json",
          "form-feature-attachments-v1.1.json（A-06 条件分岐 正本）",
          "form-feature-spec-v1.0.complete.json"
        ]
      },
      {
        "title": "追補（本チャットで追加：必ず反映）",
        "body": [
          "ReForma_追補パッチ_表示モード_テーマ_計算フィールド_v1.0.1.json（表示モード/テーマ/計算フィールド）",
          "テーマ分離: 公開フォームテーマは管理画面テーマに追従しない（フォーム設定 theme_id/theme_tokens のみ適用）"
        ]
      },
      {
        "title": "実装原則",
        "body": [
          "UIとAPIの二重防御（最終確定はAPI）",
          "評価不能時は安全側（非表示／必須解除／遷移不可／計算は空・保存しない等）",
          "v1.x：条件ネスト1段、計算依存も循環禁止・深い依存グラフ禁止",
          "保存の正は value、label はスナップショット（表示モード追補）"
        ]
      },
      {
        "title": "今回の実装対象（APIカテゴリ）",
        "body": [
          "7.1 Auth / 7.2 Forms / 7.3 Responses / 7.4 ACK/PDF / 7.7 Dashboard / 7.8 System Admin（SUP + root-only）"
        ]
      },
      {
        "title": "出力してほしいもの",
        "body": [
          "Laravel 12 雛形コード（routes/controllers/requests/services/policies/jobs/migrations）",
          "RuleValidator: A-06 + computed_rule の妥当性検証（参照存在/型/循環/制限）",
          "Submit: ConditionEvaluator + ComputedEvaluator を実行して確定値を保存（クライアント計算値は信用しない）"
        ]
      }
    ]
  },
  "attachments_to_share": {
    "must_include": [
      {
        "file": "openapi-reforma-v1.1-full.yaml",
        "path": "sandbox:/mnt/data/openapi-reforma-v1.1-full.yaml",
        "purpose": "OpenAPI（実装参照）"
      },
      {
        "file": "ReForma_Laravel12_最小実装設計_OpenAPIv1.1-full.json",
        "path": "sandbox:/mnt/data/ReForma_Laravel12_最小実装設計_OpenAPIv1.1-full.json",
        "purpose": "Laravel最小設計"
      },
      {
        "file": "ReForma_条件分岐_評価結果IF_v1.0.json",
        "path": "sandbox:/mnt/data/ReForma_条件分岐_評価結果IF_v1.0.json",
        "purpose": "ConditionState I/F"
      },
      {
        "file": "ReForma_追補パッチ_表示モード_テーマ_計算フィールド_v1.0.1.json",
        "path": "sandbox:/mnt/data/ReForma_追補パッチ_表示モード_テーマ_計算フィールド_v1.0.1.json",
        "purpose": "追補パッチ（テーマ分離含む）"
      }
    ]
  }
}
```
