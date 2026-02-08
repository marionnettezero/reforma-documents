# ReForma 正本仕様書 v1.5.4

**生成日時**: 2026-02-08T09:41:15.686326+00:00

このドキュメントは最新の分類別仕様書から自動生成された統合版です。

---

## コンポーネント・マニフェスト

| 分類 | バージョン | JSON | Markdown |
| --- | --- | --- | --- |
| backend | v0.1.1 | latest/classified/backend/reforma-backend-spec-v0.1.1.json | latest/classified/backend/reforma-backend-spec-v0.1.1.md |
| common | v1.5.1 | latest/classified/common/reforma-common-spec-v1.5.1.json | latest/classified/common/reforma-common-spec-v1.5.1.md |
| db | v0.1.2 | latest/classified/db/reforma-db-spec-v0.1.2.json | latest/classified/db/reforma-db-spec-v0.1.2.md |

---

# COMMON 仕様 (v1.5.1)


本書は **画面共通仕様 v1.5-updated** に、タイムゾーンと進捗表示の明確化、およびトーストメッセージ優先順位の実装メモを追記した改訂版です。

**注意**: このMarkdownファイルの変更は、対応するJSONファイル（reforma-common-spec-v1.5.1.json）にも反映してください。

## 追加説明

### 日時とタイムゾーン

- 日付・時刻は ISO 8601 形式で表記します。
- 原則として **Asia/Tokyo (UTC+09:00)** のタイムゾーンを用い、必要に応じて `+09:00` のオフセットを明示します。
- サーバー時間を UTC で扱う場合は `Z` 接尾辞を付け、タイムゾーン未指定の値は UTC と解釈します。

### 非同期処理の進捗表示

- `progress_endpoint` は `/v1/progress/{job_id}` のようなエンドポイントを実装し、非同期処理の進捗率や状態を JSON で返します。
- `indeterminate_progress` は progress_endpoint を実装できない場合のフォールバックであり、UI に indeterminate なプログレスインジケータを表示して、完了時にトースト通知を出します。

### Toast 表示文言の実装メモ

- トーストの文言は `message` → `errors.reason` → `code` の順に決定します。
- 同一エラーが 1 秒以内に連続発生した場合は重複表示を抑制し、最新のメッセージのみ表示します。
- トーストは画面の右上に固定表示し、複数メッセージはスタックして表示することを推奨します。

## Toast 表示文言の優先順位（確定）

Toast 表示は以下の優先順位で文言を決定します。

1. **`message`（最優先）**
2. **`errors.reason`（補助表示）**
3. **`code`（最終フォールバック）**

### 運用ルール

- `errors.reason` は機械判定が主用途であり、表示は ROOT_ONLY 等の限定ケースに留めます。
- 生のエラー（スタックトレース等）はトーストに表示せず、Debug UI (`VITE_DEBUG=true`) でのみ表示します。

### 擬似コード例

```ts
const toastText =
  error.message
  ?? mapReason(error.errors?.reason)
  ?? mapCode(error.code)
  ?? "処理に失敗しました";
```

## 画面タイトルとパンくずの表示仕様

### 画面タイトル
- 画面タイトルは**画面名のみ**を表示する（画面IDは含めない）
- 例: 「S-02 アカウント一覧」ではなく「アカウント一覧」を表示
- 画面タイトルは`ScreenHeader`コンポーネントの`h1`要素に表示される
- 画面タイトルは`screenLabel(spec)`関数で取得される（`spec.title`を返す）

### パンくず（Breadcrumbs）
- パンくずは画面タイトルと**同一の文言**を使用する
- パンくずの最後の項目（現在の画面）は画面名のみを表示する（画面IDは含めない）
- パンくずの構造: `ホーム > セクション名 > 画面名`
- 例: `ホーム > システム管理 > アカウント一覧`

### 実装ルール
- `screenLabel(spec)`関数は`spec.title`のみを返す（`${s.screen_no} ${s.title}`ではない）
- `Breadcrumbs`コンポーネントは`screenLabel(spec)`を使用して画面名を取得する
- 画面タイトルとパンくずは常に一致させる

## 変更履歴

- **v1.5.2 (2026-01-17)**: 画面タイトルとパンくずの表示仕様を追加。
- **v1.5.1 (2026-01-14)**: タイムゾーンおよび進捗エンドポイントの明確化、トースト表示実装メモを追記。
- **v1.5-updated (2026-01-14)**: トースト表示文言の優先順位を明記。


---

# BACKEND 仕様 (v0.1.1)

- version: v0.1.1
- generated_at: 2026-01-14T11:37:59.885164+00:00

**注意**: このMarkdownファイルの変更は、対応するJSONファイル（reforma-backend-spec-v0.1.1.json）にも反映してください。

## Sources
- latest/backend/reforma-backend-spec-v1.0.0-Backend-共有テンプレ-.json.json (v1.0.0)
- latest/backend/reforma-backend-spec-v1.0.0-backend-chat-init.json.json (v1.0.0)
- latest/backend/reforma-backend-spec-v1.0.0.json (v1.0.0)
- latest/backend/reforma-backend-spec-v0.1.1.json (v0.1.1)

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

## reforma-backend-spec-v0.1.1

_Source files:_ latest/backend/reforma-backend-spec-v0.1.1.json

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


---

# DB 仕様 (v0.1.2)

この文書は、実装されているマイグレーションファイルを基に最新のDB仕様をまとめたものです。

**注意**: このMarkdownファイルの変更は、対応するJSONファイル（reforma-db-spec-v0.1.2.json）にも反映してください。

## バージョンおよびメタ情報
- **バージョン**: v0.1.2
- **生成日時**: 2026-01-17T00:00:00Z
- **更新内容**: テーマ機能、表示モード機能、計算フィールド機能、マイクロ秒対応の追加

---

## テーブル一覧

### forms
フォーム定義のマスタテーブル

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---------|-----|------|-----------|------|
| id | bigint unsigned | NO | - | 主キー |
| code | varchar(255) | NO | - | フォーム識別子（form_key、ユニーク） |
| status | varchar(16) | NO | 'draft' | ステータス（draft/published/closed） |
| is_public | boolean | NO | false | 公開フラグ |
| public_period_start | timestamp | YES | NULL | 公開開始日時 |
| public_period_end | timestamp | YES | NULL | 公開終了日時 |
| answer_period_start | timestamp | YES | NULL | 回答開始日時 |
| answer_period_end | timestamp | YES | NULL | 回答終了日時 |
| attachment_enabled | boolean | NO | false | 添付ファイルの利用有無 |
| attachment_type | varchar(32) | YES | NULL | 添付ファイルの種類（pdf_template, uploaded_files） |
| pdf_template_path | varchar(512) | YES | NULL | PDFテンプレートのストレージパス（pdf_templateの場合のみ） |
| attachment_files_json | json | YES | NULL | アップロードしたファイルのパス配列（uploaded_filesの場合のみ） |
| notification_user_enabled | boolean | NO | false | ユーザー通知の有効/無効 |
| notification_user_email_template | text | YES | NULL | ユーザー宛メールテンプレート |
| notification_user_email_subject | varchar(255) | YES | NULL | ユーザー宛メールタイトル |
| notification_user_email_from | varchar(255) | YES | NULL | ユーザー宛メール送信元 |
| notification_user_email_reply_to | varchar(255) | YES | NULL | ユーザー宛メール返信先 |
| notification_user_email_cc | json | YES | NULL | ユーザー宛メールCC（JSON配列） |
| notification_user_email_bcc | json | YES | NULL | ユーザー宛メールBCC（JSON配列） |
| notification_admin_enabled | boolean | NO | false | 管理者通知の有効/無効 |
| notification_admin_user_ids | json | YES | NULL | 通知先管理者ID配列（JSON配列） |
| notification_admin_email_template | text | YES | NULL | 管理者宛メールテンプレート |
| notification_admin_email_subject | varchar(255) | YES | NULL | 管理者宛メールタイトル |
| notification_admin_email_from | varchar(255) | YES | NULL | 管理者宛メール送信元 |
| notification_admin_email_reply_to | varchar(255) | YES | NULL | 管理者宛メール返信先 |
| theme_id | bigint unsigned | YES | NULL | テーマID（themesテーブルへの外部キー） |
| theme_tokens | json | YES | NULL | テーマトークン（フォーム固有のカスタマイズ） |
| created_by | bigint unsigned | YES | NULL | 作成者ID |
| created_at | timestamp | YES | NULL | 作成日時 |
| updated_at | timestamp | YES | NULL | 更新日時 |
| deleted_at | timestamp | YES | NULL | 削除日時（論理削除） |

**インデックス**:
- `idx_forms_status_is_public`: (status, is_public)
- `idx_forms_code`: (code)
- `idx_forms_theme_id`: (theme_id)

**外部キー**:
- `fk_forms_created_by`: created_by → users.id (ON DELETE SET NULL)
- `fk_forms_theme_id`: theme_id → themes.id (ON DELETE SET NULL)

---

### form_fields
フォームの入力項目定義テーブル

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---------|-----|------|-----------|------|
| id | bigint unsigned | NO | - | 主キー |
| form_id | bigint unsigned | NO | - | フォームID |
| field_key | varchar(255) | NO | - | フィールド識別子 |
| type | varchar(64) | NO | - | input種別（text/email/select等） |
| sort_order | integer | NO | 0 | 表示順序 |
| is_required | boolean | NO | false | 固定必須フラグ |
| options_json | json | YES | NULL | 選択肢など（JSON） |
| visibility_rule | json | YES | NULL | 表示条件ルール（JSON） |
| required_rule | json | YES | NULL | 必須条件ルール（JSON） |
| step_transition_rule | json | YES | NULL | ステップ遷移ルール（JSON） |
| computed_rule | json | YES | NULL | 計算フィールドルール（JSON） |
| pdf_block_key | varchar(255) | YES | NULL | PDFテンプレート内のblock名 |
| pdf_page_number | integer | YES | NULL | PDFテンプレートのページ番号（1始まり、デフォルトは1） |
| created_at | timestamp | YES | NULL | 作成日時 |
| updated_at | timestamp | YES | NULL | 更新日時 |

**インデックス**:
- `idx_form_fields_form_id_sort_order`: (form_id, sort_order)
- `uk_form_fields_form_id_field_key`: (form_id, field_key) UNIQUE

**外部キー**:
- `fk_form_fields_form_id`: form_id → forms.id (ON DELETE CASCADE)

---

### submissions
フォーム送信データテーブル（responsesと同義）

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---------|-----|------|-----------|------|
| id | bigint unsigned | NO | - | 主キー |
| form_id | bigint unsigned | NO | - | フォームID |
| status | varchar(16) | NO | 'received' | ステータス（received/confirmed） |
| created_at | timestamp(6) | YES | NULL | 作成日時（マイクロ秒対応） |
| updated_at | timestamp(6) | YES | NULL | 更新日時（マイクロ秒対応） |

**インデックス**:
- `idx_submissions_form_id_created_at`: (form_id, created_at)
- `idx_submissions_status`: (status)

**外部キー**:
- `fk_submissions_form_id`: form_id → forms.id (ON DELETE CASCADE)

---

### submission_values
送信データの値テーブル

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---------|-----|------|-----------|------|
| id | bigint unsigned | NO | - | 主キー |
| submission_id | bigint unsigned | NO | - | 送信ID |
| field_key | varchar(255) | NO | - | フィールド識別子 |
| field_label_snapshot | varchar(255) | YES | NULL | フィールドラベルのスナップショット |
| value_json | json | NO | - | 回答値（JSON） |
| label_json | json | YES | NULL | ラベルスナップショット（JSON） |
| created_at | timestamp | YES | NULL | 作成日時 |
| updated_at | timestamp | YES | NULL | 更新日時 |

**インデックス**:
- `idx_submission_values_submission_id_field_key`: (submission_id, field_key)

**外部キー**:
- `fk_submission_values_submission_id`: submission_id → submissions.id (ON DELETE CASCADE)

---

### themes
テーマ定義のマスタテーブル

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---------|-----|------|-----------|------|
| id | bigint unsigned | NO | - | 主キー |
| code | varchar(255) | NO | - | テーマコード（ユニーク） |
| name | varchar(255) | NO | - | テーマ名（表示用） |
| description | text | YES | NULL | テーマの説明 |
| theme_tokens | json | NO | - | テーマトークン（CSS変数の値） |
| is_preset | boolean | NO | false | プリセットテーマかどうか |
| is_active | boolean | NO | true | 有効かどうか |
| created_by | bigint unsigned | YES | NULL | 作成者ID（プリセットテーマはNULL） |
| created_at | timestamp | NO | - | 作成日時 |
| updated_at | timestamp | NO | - | 更新日時 |
| deleted_at | timestamp | YES | NULL | 削除日時（論理削除） |

**インデックス**:
- `idx_themes_code`: (code) UNIQUE
- `idx_themes_is_active`: (is_active)
- `idx_themes_is_preset`: (is_preset)

**外部キー**:
- `fk_themes_created_by`: created_by → users.id (ON DELETE SET NULL)

---

## 変更履歴

### v0.1.2 (2026-01-17)
- テーマ機能の追加（themesテーブル、forms.theme_id, forms.theme_tokens）
- 表示モード機能の追加（submission_values.label_json, submission_values.field_label_snapshot）
- 計算フィールド機能の追加（form_fields.computed_rule）
- マイクロ秒対応（submissions.created_at, submissions.updated_atをtimestamp(6)に変更）

### v0.1.1 (2026-01-16)
- 添付ファイル機能の追加（forms.attachment_enabled, attachment_type, pdf_template_path, attachment_files_json）
- PDF生成機能の追加（form_fields.pdf_block_key, pdf_page_number）
- 期間チェック機能の追加（forms.public_period_start, public_period_end, answer_period_start, answer_period_end）
- 通知機能の追加（forms.notification_user_*, notification_admin_*）

### v0.1.0 (2026-01-14)
- 初版作成


---

