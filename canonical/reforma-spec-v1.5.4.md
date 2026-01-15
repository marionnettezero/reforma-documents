# ReForma 正本仕様書 v1.5.4

**生成日時**: 2026-01-15T16:56:35.352571+00:00

このドキュメントは最新の分類別仕様書から自動生成された統合版です。

---

## コンポーネント・マニフェスト

| 分類 | バージョン | JSON | Markdown |
| --- | --- | --- | --- |
| api | v1.3.3 | classified\api\reforma-api-spec-v1.3.3.json | classified\api\reforma-api-spec-v1.3.3.md |
| backend | v1.1.0 | classified\backend\reforma-backend-spec-v1.1.0.json | classified\backend\reforma-backend-spec-v1.1.0.md |
| common | v1.5.1 | classified\common\reforma-common-spec-v1.5.1.json | classified\common\reforma-common-spec-v1.5.1.md |
| db | v1.0.0 | classified\db\reforma-db-spec-v1.0.0.json | classified\db\reforma-db-spec-v1.0.0.md |
| frontend | v1.1.0 | classified\frontend\reforma-frontend-spec-v1.1.0.json | classified\frontend\reforma-frontend-spec-v1.1.0.md |

---

# COMMON 仕様 (v1.5.1)


本書は **画面共通仕様 v1.5-updated** に、タイムゾーンと進捗表示の明確化、およびトーストメッセージ優先順位の実装メモを追記した改訂版です。

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

## 変更履歴

- **v1.5.1 (2026-01-14)**: タイムゾーンおよび進捗エンドポイントの明確化、トースト表示実装メモを追記。
- **v1.5-updated (2026-01-14)**: トースト表示文言の優先順位を明記。


---

# API 仕様 (v1.3.3)

この文書は、OpenAPI仕様 (v1.3.0) を元に最新のAPI仕様をまとめたものです。以前のAPI仕様からの差分ではなく、**全文を日本語で記載**しており、最新版のみを参照すれば十分です。v1.3.2 をベースに、v1.3.0 で定義されていた条件分岐（ConditionState）関連のスキーマ定義とエラーコードを統合しています。

## バージョンおよびメタ情報
- **バージョン**: v1.3.3
- **生成日時**: 2026-01-16T10:00:00Z
- **OpenAPI バージョン**: 3.0.3

---

## 条件分岐スキーマ定義（ConditionState）

条件分岐機能で使用するスキーマ定義です。公開フォーム取得（GET /v1/public/forms/{form_key}）や submit 時のレスポンスに含まれます。

### Reason
評価エラーや警告の理由を表すオブジェクト。

```json
{
  "type": "object",
  "properties": {
    "kind": {
      "type": "string",
      "enum": ["rule", "type", "missing_field", "unknown_operator"]
    },
    "path": {
      "type": "string"
    },
    "message": {
      "type": "string"
    }
  },
  "required": ["kind"]
}
```

### FieldConditionState
各フィールドの条件分岐評価結果。

```json
{
  "type": "object",
  "properties": {
    "visible": {
      "type": "boolean",
      "description": "フィールドを表示するか"
    },
    "required": {
      "type": "boolean",
      "description": "フィールドが必須か"
    },
    "store": {
      "type": "string",
      "enum": ["store", "do_not_store"],
      "description": "値を保存するか"
    },
    "eval": {
      "type": "string",
      "enum": ["ok", "fallback", "error"],
      "description": "評価結果ステータス"
    },
    "reasons": {
      "type": "array",
      "items": { "$ref": "#/components/schemas/Reason" },
      "description": "評価エラー/警告の理由（eval が fallback/error の場合）"
    }
  },
  "required": ["visible", "required", "store", "eval"]
}
```

### StepTransitionState
STEP 遷移の評価結果。

```json
{
  "type": "object",
  "properties": {
    "can_transition": {
      "type": "boolean",
      "description": "次の STEP に遷移可能か"
    },
    "eval": {
      "type": "string",
      "enum": ["ok", "fallback", "error"],
      "description": "評価結果ステータス"
    },
    "message": {
      "type": "string",
      "description": "遷移不可時のメッセージ"
    },
    "reasons": {
      "type": "array",
      "items": { "$ref": "#/components/schemas/Reason" },
      "description": "評価エラー/警告の理由"
    }
  },
  "required": ["can_transition", "eval"]
}
```

### ConditionState
条件分岐の全体評価結果。公開フォーム GET や submit レスポンスの `data.condition_state` に含まれる。

```json
{
  "type": "object",
  "properties": {
    "version": {
      "type": "string",
      "enum": ["1"],
      "description": "ConditionState のスキーマバージョン"
    },
    "evaluated_at": {
      "type": "string",
      "format": "date-time",
      "description": "評価日時（ISO8601）"
    },
    "fields": {
      "type": "object",
      "additionalProperties": { "$ref": "#/components/schemas/FieldConditionState" },
      "description": "field_key をキーとした各フィールドの評価結果"
    },
    "step": {
      "$ref": "#/components/schemas/StepTransitionState",
      "description": "STEP 遷移の評価結果（STEP 遷移時のみ）"
    }
  },
  "required": ["version", "evaluated_at", "fields"]
}
```

---

## 条件分岐関連エラーコード

| コード | HTTP | 発生条件 |
|--------|------|----------|
| `STEP_TRANSITION_DENIED` | 422 | STEP 遷移条件が false と評価された場合 |
| `CONDITION_EVAL_ERROR` | 200/422 | 条件評価時にランタイムエラーが発生（安全側フォールバック適用） |
| `CONDITION_RULE_INVALID` | 422 | 管理画面でルール保存/公開時にルールが不正な場合 |

---

## 条件分岐の適用箇所

| エンドポイント | 用途 | condition_state の位置 |
|---------------|------|------------------------|
| GET /v1/public/forms/{form_key} | 公開フォーム初期描画 | `data.condition_state` |
| POST /v1/forms/{form_key}/submit | フォーム送信 | `data.condition_state`（成功時）、`errors.step`（422 STEP_TRANSITION_DENIED 時） |

---

## エンドポイント一覧

### POST /v1/auth/login
- **概要**: ログイン
- **リクエストボディ**:
  - コンテンツタイプ: application/json
    - スキーマ型: object
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 422: 422 Validation Error
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### POST /v1/auth/logout
- **概要**: ログアウト
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### GET /v1/auth/me
- **概要**: 自分自身の情報
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### GET /v1/forms
- **概要**: フォーム一覧
- **パラメータ**:
  - `page` (クエリ, 必須, 型: integer): 
  - `per_page` (クエリ, 必須, 型: integer): 
  - `sort` (クエリ, 任意, 型: None): 
  - `status` (クエリ, 任意, 型: string): 
  - `q` (クエリ, 任意, 型: string): 
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### POST /v1/forms
- **概要**: フォーム作成
- **リクエストボディ**:
  - コンテンツタイプ: application/json
    - スキーマ型: object
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 201: Created
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 422: 422 Validation Error
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### GET /v1/forms/{id}
- **概要**: フォーム取得
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): 
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### PUT /v1/forms/{id}
- **概要**: フォーム更新
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): 
- **リクエストボディ**:
  - コンテンツタイプ: application/json
    - スキーマ型: object
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 422: 422 Validation Error
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### DELETE /v1/forms/{id}
- **概要**: フォーム削除（論理）
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): 
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### GET /v1/forms/{id}/fields
- **概要**: フォーム項目一覧
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): 
  - `include_rules` (クエリ, 任意, 型: boolean): 
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### PUT /v1/forms/{id}/fields
- **概要**: フォーム項目一括更新
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): 
- **リクエストボディ**:
  - コンテンツタイプ: application/json
    - スキーマ型: object
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 422: 422 Validation Error
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### GET /v1/responses
- **概要**: 送信一覧（Responses）
- **パラメータ**:
  - `page` (クエリ, 必須, 型: integer): 
  - `per_page` (クエリ, 必須, 型: integer): 
  - `sort` (クエリ, 任意, 型: None): 
  - `form_id` (クエリ, 任意, 型: integer): 
  - `status` (クエリ, 任意, 型: string): 
  - `q` (クエリ, 任意, 型: string): 
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### GET /v1/responses/{id}
- **概要**: 送信詳細
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): 
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### POST /v1/forms/{form_key}/submit
- **概要**: 公開 submit
- **説明**: フォーム送信。条件分岐がある場合、成功時は `data.condition_state` を返す。STEP 遷移が拒否された場合は 422 で `errors.step` を返す。
- **パラメータ**:
  - `form_key` (パス, 必須, 型: string): 
- **リクエストボディ**:
  - コンテンツタイプ: application/json
    - スキーマ型: object
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
      - 追加フィールド: `data.condition_state` (#/components/schemas/ConditionState)
  - 422: 422 Validation Error
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
      - 追加フィールド: `errors.step` (#/components/schemas/StepTransitionState) - STEP_TRANSITION_DENIED 時

### GET /v1/forms/{form_key}/ack
- **概要**: ACK 表示
- **パラメータ**:
  - `form_key` (パス, 必須, 型: string): 
  - `token` (クエリ, 任意, 型: string): 
  - `submission_id` (クエリ, 任意, 型: integer): 
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object

### GET /v1/responses/{id}/pdf
- **概要**: PDF 取得（管理側）
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): 
  - `pdf_type` (クエリ, 任意, 型: string): 
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/pdf
      - スキーマ型: string
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### GET /v1/dashboard/summary
- **概要**: ダッシュボード集計
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### GET /v1/dashboard/errors
- **概要**: ダッシュボード（エラー/失敗一覧）
- **パラメータ**:
  - `page` (クエリ, 必須, 型: integer): 
  - `per_page` (クエリ, 必須, 型: integer): 
  - `sort` (クエリ, 任意, 型: None): 
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### GET /v1/system/admin-users
- **概要**: 管理者ユーザ一覧
- **説明**: - 返却の正本ロールは `roles[]`。
- `role` は互換のための deprecated フィールド（将来削除予定）。
- **パラメータ**:
  - `page` (クエリ, 必須, 型: integer): 
  - `per_page` (クエリ, 必須, 型: integer): 
  - `sort` (クエリ, 任意, 型: None): 
  - `role` (クエリ, 任意, 型: string): 
  - `status` (クエリ, 任意, 型: string): 
  - `q` (クエリ, 任意, 型: string): 
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### POST /v1/system/admin-users
- **概要**: 管理者ユーザ作成（招待）
- **リクエストボディ**:
  - コンテンツタイプ: application/json
    - スキーマ型: object
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 201: Created
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 422: 422 Validation Error
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### PUT /v1/system/admin-users/{id}
- **概要**: 管理者ユーザ更新
- **説明**: ### RBAC
- 必須: system_admin
- **system_admin 付与（昇格）**は root-only（is_root=true 必須）
- system_admin 剥奪（降格）は system_admin で可（ただし自己降格禁止・最後の system_admin 禁止）

- `roles` は現状単一ロール運用（要素数1）
- `is_root` 変更は root 権限が必要
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): 
- **リクエストボディ**:
  - コンテンツタイプ: application/json
    - スキーマ型: #/components/schemas/AdminUserUpdateRequest
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 422: 422 Validation Error
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### GET /v1/system/admin-users/{id}
- **概要**: 管理者アカウント詳細取得
- **説明**: S-03 アカウント詳細/編集用。返却ロールは roles[] が正本。role は返さない。
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): 
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 404: Not Found
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### POST /v1/system/admin-users/invites/resend
- **概要**: 招待再送
- **リクエストボディ**:
  - コンテンツタイプ: application/json
    - スキーマ型: object
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 422: 422 Validation Error
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### GET /v1/system/admin-audit-logs
- **概要**: 監査ログ一覧
- **パラメータ**:
  - `page` (クエリ, 必須, 型: integer): 
  - `per_page` (クエリ, 必須, 型: integer): 
  - `sort` (クエリ, 任意, 型: None): 
  - `user_id` (クエリ, 任意, 型: integer): 
  - `action` (クエリ, 任意, 型: string): 
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### GET /v1/system/roles/permissions
- **概要**: ロール権限定義取得
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### PUT /v1/system/roles/permissions
- **概要**: ロール権限定義更新
- **リクエストボディ**:
  - コンテンツタイプ: application/json
    - スキーマ型: object
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 422: 422 Validation Error
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### GET /v1/system/settings
- **概要**: システム設定取得
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### PUT /v1/system/settings
- **概要**: システム設定更新
- **リクエストボディ**:
  - コンテンツタイプ: application/json
    - スキーマ型: object
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 422: 422 Validation Error
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### GET /v1/system/root-only/ping
- **概要**: root-only 動作確認（ping）
- **説明**: root-only ミドルウェア動作確認用。system_admin を満たした上で is_root=true の場合のみ成功。
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### GET /v1/progress/{job_id}
- **概要**: 進捗取得
- **説明**: CSV/PDF/ファイル操作等の進捗を取得する。
- **パラメータ**:
  - `job_id` (パス, 必須, 型: string): 
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeProgress
  - 404: Not Found / expired
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 500: Server Error
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### GET /v1/search
- **概要**: 横断検索
- **説明**: フォーム/回答/監査ログ/アカウント等を横断検索する（S-06）。
- **パラメータ**:
  - `q` (クエリ, 必須, 型: string): 
  - `types` (クエリ, 任意, 型: array): 
  - `page` (クエリ, 必須, 型: integer): 
  - `per_page` (クエリ, 必須, 型: integer): 
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeSearch
  - 401: Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 422: Validation Error
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### GET /v1/logs
- **概要**: ログ一覧
- **説明**: L-01 ログ一覧。
- **パラメータ**:
  - `page` (クエリ, 必須, 型: integer): 
  - `per_page` (クエリ, 必須, 型: integer): 
  - `level` (クエリ, 任意, 型: string): 
  - `q` (クエリ, 任意, 型: string): 
  - `date_from` (クエリ, 任意, 型: string): 
  - `date_to` (クエリ, 任意, 型: string): 
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeLogsList
  - 401: Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 422: Validation Error
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### GET /v1/logs/{id}
- **概要**: ログ詳細
- **説明**: L-02 ログ詳細。
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): 
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeLogDetail
  - 401: Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 404: Not Found
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### GET /v1/public/forms/{form_key}
- **概要**: 公開フォーム表示取得
- **説明**: Respondent 用フォーム表示（/f/{form_key}）。条件分岐がある場合は `data.condition_state` を返す。
- **パラメータ**:
  - `form_key` (パス, 必須, 型: string): 
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopePublicFormView
      - 追加フィールド: `data.condition_state` (#/components/schemas/ConditionState)
  - 404: Not Found
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### POST /v1/responses/export/csv
- **概要**: 回答CSVエクスポート（ジョブ開始）
- **説明**: 回答一覧のCSVエクスポートを非同期ジョブとして開始し、job_id を返す。
- **リクエストボディ**:
  - コンテンツタイプ: application/json
    - スキーマ型: #/components/schemas/ResponsesCsvExportRequest
- **レスポンス**:
  - 202: Accepted
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeJobAccepted
  - 401: Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 422: Validation Error
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 500: Server Error
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### GET /v1/exports/{job_id}/download
- **概要**: 成果物ダウンロード
- **説明**: エクスポート成果物のダウンロード。URL期限切れ時は再署名（settings に依存）。
- **パラメータ**:
  - `job_id` (パス, 必須, 型: string): 
- **レスポンス**:
  - 302: Redirect to signed download URL
  - 401: Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 404: Not Found / expired
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError


---

# BACKEND 仕様 (v1.1.0)

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


---

# FRONTEND 仕様 (v1.1.0)

- version: v1.1.0
- generated_at: 2026-01-14T11:37:59.767769+00:00

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
- latest/frontend/reforma-frontend-spec-v1.1.0.json (v1.1.0)

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
        "通常: diff zip（変更/追加ファイルのみ）",
        "指定時: フル zip"
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

_Source files:_ latest/frontend/reforma-frontend-spec-v0.3.0.json

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

## reforma-frontend-spec-v0.5.8-frontend-handoff-.json

_Source files:_ latest/frontend/reforma-frontend-spec-v0.5.8-frontend-handoff-.json.json

```json
{
  "metadata": {
    "project": "ReForma",
    "component": "frontend-react",
    "handoff_title": "ReForma React 引き継ぎパック（v0.5.8 時点）",
    "generated_at": "2026-01-14T00:19:22.141465+09:00",
    "timezone": "Asia/Tokyo",
    "language": "ja",
    "status": "active",
    "notes": [
      "このJSONは新しいChatGPTチャットに貼り付け・添付して使う機械共有用。",
      "フルZIPがダウンロード不可になる事象が発生したため、以後は差分ZIP運用を基本とし、フルZIPはユーザー側でバックアップ生成する方針も併記。"
    ]
  },
  "baseline": {
    "source_of_truth_version": "0.5.8",
    "baseline_source": "ユーザー環境に適用済みの v0.5.8 相当（v0.4.12.3 + v0.5.x 差分適用）",
    "previous_baseline_zip": "reforma-react-v0.4.12.3.zip",
    "package_version_required": true,
    "build_log_expected_prefix": "reforma-react@0.5.8",
    "zip_distribution_constraints": {
      "default": "diff_zip_only",
      "full_zip": "依頼時のみ（ただしダウンロード制限が起きる可能性あり）",
      "diff_zip_structure_rule": "トップディレクトリを含めず、プロジェクト直下に上書き展開できる構造（例: src/, package.json 等が直に入る）"
    }
  },
  "delivery_rules": {
    "versioning": {
      "must_update_package_json_version_each_release": true,
      "must_match_build_output": true
    },
    "zip_apply_commands": {
      "no_path_prefix_rule": "コマンド例で /path/to/ は付けない（zipは作業ディレクトリに置く前提）",
      "diff_apply": [
        "cd /var/www/reforma/frontend",
        "unzip -o reforma-react-vX.Y.Z-diff.zip -d ."
      ],
      "full_apply": [
        "cd /var/www/reforma/frontend",
        "unzip -o reforma-react-vX.Y.Z.zip -d .",
        "npm install"
      ]
    },
    "cache_clear_required": {
      "reason": "適用したはずなのに修正が見えない場合が多発するため",
      "commands": [
        "cd /var/www/reforma/frontend",
        "rm -rf dist",
        "rm -rf node_modules/.vite"
      ],
      "browser": [
        "Chrome/Edge: Ctrl+Shift+R（強制再読み込み）",
        "DevTools > Network > Disable cache を有効化して再読込"
      ]
    }
  },
  "specs_and_artifacts": {
    "core_specs_in_project_files": [
      "01.ReForma 基本仕様書 v1.0.json",
      "02.ReForma 画面仕様書 v1.0.json",
      "03.ReForma API 仕様書 v1.0.json",
      "04.ReForma DB 仕様書 v1.0.json",
      "05.ReForma 拡張仕様書 v1.0.json",
      "06.ReForma React 運用・画面ui仕様書 V0.3.json"
    ],
    "latest_consolidated_specs_shared": [
      "01.ReForma-basic-spec-v1.1-consolidated.final.json",
      "02.ReForma-screen-spec-v1.1-consolidated.json",
      "form-feature-spec-v1.0.complete.json",
      "form-feature-attachments-v1.1.json",
      "condition-ui-spec-v1.0.json",
      "ReForma_条件分岐_実装整理パック_v1.0.json",
      "ReForma_条件分岐_評価結果IF_v1.0.json",
      "ReForma_API_条件分岐_追補_適用ガイド_OperationIdマッピング_v1.0.json",
      "ReForma_API_条件分岐評価結果IF_追補_v1.0.patch.json",
      "ReForma_追補パッチ_表示モード_テーマ_計算フィールド_v1.0.1.json",
      "reforma-root-only-policy-v1.0.json"
    ],
    "openapi": {
      "use_as_source_of_truth": true,
      "latest": [
        "openapi-reforma-v1.1-full.updated.yaml",
        "openapi-reforma-v1.1-full.updated.json"
      ],
      "supplements_variants": [
        "openapi-reforma-v1.1-full+supplements.yaml",
        "openapi-reforma-v1.1-full+supplements.json",
        "ReForma_OpenAPI_追補反映_patch_v1.0.json"
      ]
    },
    "generated_by_chatgpt": [
      "condition-operator-matrix-ui-v1.0.json (attachments化前提の field type × operator 許可表 + operator別 value_input UI 推奨)"
    ]
  },
  "auth_and_rbac": {
    "api_auth": "auth:sanctum + abilities:admin + reforma.admin_pat",
    "rbac_role_key": "roles[] in /auth/me",
    "root_flag_key": "is_root in /auth/me",
    "rbac_roles_known": [
      "reforma.system_admin"
    ],
    "root_only": {
      "enforced_at_api": "reforma.root_only (APIレベル強制)",
      "ui_source_of_truth": [
        "/auth/me roles[]",
        "/auth/me is_root"
      ],
      "error_handling": {
        "http_status": 403,
        "code": "FORBIDDEN",
        "errors.reason": "ROOT_ONLY",
        "ui_message_ja": "root 権限が必要です（この操作は root-only です）",
        "must_be_distinct_from_generic_forbidden": true
      }
    }
  },
  "ui_completed_work_v0_5_x": {
    "sidebar": {
      "pc_collapsible": true,
      "collapsed_behavior": [
        "モチーフロゴ(SVG)クリックで開閉トグル",
        "メニューはアイコン化",
        "ログアウトはロゴ直下に配置",
        "ボタンサイズ/中央寄せ/幅を統一（開閉両方）"
      ],
      "tooltips_i18n": "折りたたみ/展開のツールチップは言語に応じて切替（ja/en/zh 想定）"
    },
    "logo_glow": {
      "login_logo": "ロゴ領域hover/focusのみでグロー（画面hoverでは発火しない）",
      "app_logo": "左上ロゴも同様"
    },
    "logout_dialog": {
      "positioning": "PCは上寄り（タイトルパネル下あたり）、モバイルは中央",
      "status": "OK"
    }
  },
  "known_constraints_and_caveats": {
    "file_download_instability": [
      "長いチャットではZIPがダウンロード不能になる場合がある（特にフルZIP）",
      "可能ならユーザー環境で Git もしくは自前ZIPで v0.5.8 正本を保存しておく"
    ],
    "api_not_connected_yet": "現時点ではAPI未接続で進行（Authはスタブ/未接続想定）"
  },
  "next_recommended_tasks": [
    {
      "id": "NEXT-A",
      "title": "Auth/me 接続（最小）",
      "why": "roles[]/is_root を正本として UI 制御・root-only 判定を実データに移行するため",
      "scope": [
        "GET /v1/auth/me の接続",
        "401/419 -> /logout?reason=session_invalid",
        "403 reason(ROOT_ONLY) の共通処理の再確認"
      ]
    },
    {
      "id": "NEXT-B",
      "title": "S-02 アカウント一覧（System Admin）着手",
      "scope": [
        "一覧/検索/ソート/ページング",
        "root-only 操作（system_admin昇格）UI制御"
      ]
    }
  ],
  "files_to_attach_in_new_chat": {
    "must_attach": [
      "このJSON（reforma-frontend-handoff-v0.5.8.json）",
      "reforma-root-only-policy-v1.0.json",
      "openapi-reforma-v1.1-full.updated.yaml（または .json）",
      "ReForma_追補パッチ_表示モード_テーマ_計算フィールド_v1.0.1.json",
      "condition-operator-matrix-ui-v1.0.json"
    ],
    "recommended_attach": [
      "02.ReForma-screen-spec-v1.1-consolidated.json（画面/パンくず/タイトル準拠の確認用）",
      "06.ReForma React 運用・画面ui仕様書 V0.3.json（デバッグUI/共通UIルール）",
      "ReForma_Frontend_共有テンプレ_v1.1_追補反映.json（開発開始テンプレ）"
    ],
    "if_possible_best": [
      "ユーザー環境の v0.5.8 正本ソース（Git repo かユーザーが生成したフルZIP）",
      "直近のスクリーンショット（サイドバー開/閉）"
    ]
  }
}
```

## reforma-frontend-spec-v0.5.8

_Source files:_ latest/frontend/reforma-frontend-spec-v0.5.8.json

```json
{
  "metadata": {
    "project": "ReForma",
    "component": "frontend-react",
    "handoff_title": "ReForma React 引き継ぎパック（v0.5.8 時点・テンプレ埋め込み版）",
    "generated_at": "2026-01-14T00:19:22.141465+09:00",
    "timezone": "Asia/Tokyo",
    "language": "ja",
    "status": "active",
    "notes": [
      "このJSONは新しいChatGPTチャットに貼り付け・添付して使う機械共有用。",
      "フルZIPがダウンロード不可になる事象が発生したため、以後は差分ZIP運用を基本とし、フルZIPはユーザー側でバックアップ生成する方針も併記。"
    ],
    "updated_at": "2026-01-14T00:47:07.802954+09:00",
    "version": "1.1.0"
  },
  "baseline": {
    "source_of_truth_version": "0.5.8",
    "baseline_source": "ユーザー環境に適用済みの v0.5.8 相当（v0.4.12.3 + v0.5.x 差分適用）",
    "previous_baseline_zip": "reforma-react-v0.4.12.3.zip",
    "package_version_required": true,
    "build_log_expected_prefix": "reforma-react@0.5.8",
    "zip_distribution_constraints": {
      "default": "diff_zip_only",
      "full_zip": "依頼時のみ（ただしダウンロード制限が起きる可能性あり）",
      "diff_zip_structure_rule": "トップディレクトリを含めず、プロジェクト直下に上書き展開できる構造（例: src/, package.json 等が直に入る）"
    }
  },
  "delivery_rules": {
    "versioning": {
      "must_update_package_json_version_each_release": true,
      "must_match_build_output": true
    },
    "zip_apply_commands": {
      "no_path_prefix_rule": "コマンド例で /path/to/ は付けない（zipは作業ディレクトリに置く前提）",
      "diff_apply": [
        "cd /var/www/reforma/frontend",
        "unzip -o reforma-react-vX.Y.Z-diff.zip -d ."
      ],
      "full_apply": [
        "cd /var/www/reforma/frontend",
        "unzip -o reforma-react-vX.Y.Z.zip -d .",
        "npm install"
      ]
    },
    "cache_clear_required": {
      "reason": "適用したはずなのに修正が見えない場合が多発するため",
      "commands": [
        "cd /var/www/reforma/frontend",
        "rm -rf dist",
        "rm -rf node_modules/.vite"
      ],
      "browser": [
        "Chrome/Edge: Ctrl+Shift+R（強制再読み込み）",
        "DevTools > Network > Disable cache を有効化して再読込"
      ]
    }
  },
  "specs_and_artifacts": {
    "core_specs_in_project_files": [
      "01.ReForma 基本仕様書 v1.0.json",
      "02.ReForma 画面仕様書 v1.0.json",
      "03.ReForma API 仕様書 v1.0.json",
      "04.ReForma DB 仕様書 v1.0.json",
      "05.ReForma 拡張仕様書 v1.0.json",
      "06.ReForma React 運用・画面ui仕様書 V0.3.json"
    ],
    "latest_consolidated_specs_shared": [
      "01.ReForma-basic-spec-v1.1-consolidated.final.json",
      "02.ReForma-screen-spec-v1.1-consolidated.json",
      "form-feature-spec-v1.0.complete.json",
      "form-feature-attachments-v1.1.json",
      "condition-ui-spec-v1.0.json",
      "ReForma_条件分岐_実装整理パック_v1.0.json",
      "ReForma_条件分岐_評価結果IF_v1.0.json",
      "ReForma_API_条件分岐_追補_適用ガイド_OperationIdマッピング_v1.0.json",
      "ReForma_API_条件分岐評価結果IF_追補_v1.0.patch.json",
      "ReForma_追補パッチ_表示モード_テーマ_計算フィールド_v1.0.1.json",
      "reforma-root-only-policy-v1.0.json"
    ],
    "openapi": {
      "use_as_source_of_truth": true,
      "latest": [
        "openapi-reforma-v1.1-full.updated.yaml",
        "openapi-reforma-v1.1-full.updated.json"
      ],
      "supplements_variants": [
        "openapi-reforma-v1.1-full+supplements.yaml",
        "openapi-reforma-v1.1-full+supplements.json",
        "ReForma_OpenAPI_追補反映_patch_v1.0.json"
      ]
    },
    "generated_by_chatgpt": [
      "condition-operator-matrix-ui-v1.0.json (attachments化前提の field type × operator 許可表 + operator別 value_input UI 推奨)"
    ]
  },
  "auth_and_rbac": {
    "api_auth": "auth:sanctum + abilities:admin + reforma.admin_pat",
    "rbac_role_key": "roles[] in /auth/me",
    "root_flag_key": "is_root in /auth/me",
    "rbac_roles_known": [
      "reforma.system_admin"
    ],
    "root_only": {
      "enforced_at_api": "reforma.root_only (APIレベル強制)",
      "ui_source_of_truth": [
        "/auth/me roles[]",
        "/auth/me is_root"
      ],
      "error_handling": {
        "http_status": 403,
        "code": "FORBIDDEN",
        "errors.reason": "ROOT_ONLY",
        "ui_message_ja": "root 権限が必要です（この操作は root-only です）",
        "must_be_distinct_from_generic_forbidden": true
      }
    }
  },
  "ui_completed_work_v0_5_x": {
    "sidebar": {
      "pc_collapsible": true,
      "collapsed_behavior": [
        "モチーフロゴ(SVG)クリックで開閉トグル",
        "メニューはアイコン化",
        "ログアウトはロゴ直下に配置",
        "ボタンサイズ/中央寄せ/幅を統一（開閉両方）"
      ],
      "tooltips_i18n": "折りたたみ/展開のツールチップは言語に応じて切替（ja/en/zh 想定）"
    },
    "logo_glow": {
      "login_logo": "ロゴ領域hover/focusのみでグロー（画面hoverでは発火しない）",
      "app_logo": "左上ロゴも同様"
    },
    "logout_dialog": {
      "positioning": "PCは上寄り（タイトルパネル下あたり）、モバイルは中央",
      "status": "OK"
    }
  },
  "known_constraints_and_caveats": {
    "file_download_instability": [
      "長いチャットではZIPがダウンロード不能になる場合がある（特にフルZIP）",
      "可能ならユーザー環境で Git もしくは自前ZIPで v0.5.8 正本を保存しておく"
    ],
    "api_not_connected_yet": "現時点ではAPI未接続で進行（Authはスタブ/未接続想定）"
  },
  "next_recommended_tasks": [
    {
      "id": "NEXT-A",
      "title": "Auth/me 接続（最小）",
      "why": "roles[]/is_root を正本として UI 制御・root-only 判定を実データに移行するため",
      "scope": [
        "GET /v1/auth/me の接続",
        "401/419 -> /logout?reason=session_invalid",
        "403 reason(ROOT_ONLY) の共通処理の再確認"
      ]
    },
    {
      "id": "NEXT-B",
      "title": "S-02 アカウント一覧（System Admin）着手",
      "scope": [
        "一覧/検索/ソート/ページング",
        "root-only 操作（system_admin昇格）UI制御"
      ]
    }
  ],
  "files_to_attach_in_new_chat": {
    "must_attach": [
      "このJSON（reforma-frontend-handoff-v0.5.8.json）",
      "reforma-root-only-policy-v1.0.json",
      "openapi-reforma-v1.1-full.updated.yaml（または .json）",
      "ReForma_追補パッチ_表示モード_テーマ_計算フィールド_v1.0.1.json",
      "condition-operator-matrix-ui-v1.0.json"
    ],
    "recommended_attach": [
      "02.ReForma-screen-spec-v1.1-consolidated.json（画面/パンくず/タイトル準拠の確認用）",
      "06.ReForma React 運用・画面ui仕様書 V0.3.json（デバッグUI/共通UIルール）",
      "ReForma_Frontend_共有テンプレ_v1.1_追補反映.json（開発開始テンプレ）"
    ],
    "if_possible_best": [
      "ユーザー環境の v0.5.8 正本ソース（Git repo かユーザーが生成したフルZIP）",
      "直近のスクリーンショット（サイドバー開/閉）"
    ]
  },
  "templates": {
    "new_chat_initial_post": "ReForma React 開発の続き（新チャット）です。\n\n0. 前提（正本）\n- 正本ソース：ユーザー環境の v0.5.8（/var/www/reforma/frontend に適用済み）\n- 今後の配布：差分ZIPのみが基本（フルZIPは依頼時のみ。ただしダウンロード不能になる可能性あり）\n- API は現状未接続（Auth/me は将来的に接続）\n\n1. 提供ルール（必須）\n- 差分ZIPはトップディレクトリを含めず、プロジェクト直下に上書き展開できる構造（例：src/, package.json が直に入る）\n- 各リリース毎に package.json の version を必ず更新し、buildログ表示（reforma-react@X.Y.Z）も追従させる\n- コマンド例に /path/to/ は付けない（zipは作業ディレクトリに置く前提）\n- 提供手順にはキャッシュクリア手順を必ず含める（dist と node_modules/.vite 削除、ブラウザ強制再読み込み）\n\n2. 差分ZIP適用手順\n```bash\ncd /var/www/reforma/frontend\nunzip -o reforma-react-vX.Y.Z-diff.zip -d .\n# 必要なら npm install\n```\n\n3. キャッシュクリア & ビルド（反映確認）\n```bash\ncd /var/www/reforma/frontend\nrm -rf dist\nrm -rf node_modules/.vite\nnpm run build:stg\n```\nブラウザ：Ctrl+Shift+R（強制再読み込み）／DevTools > Network > Disable cache\n\n4. ローカルGit運用（正本固定＋差分管理）\n初回のみ（v0.5.8 固定）\n```bash\ncd /var/www/reforma/frontend\ngit init\ngit branch -M main\ncat > .gitignore <<'EOF'\nnode_modules/\ndist/\n.vite/\nnode_modules/.vite/\n.env\n.env.*\n.DS_Store\n*.log\nEOF\ngit add .\ngit commit -m \"chore: baseline v0.5.8 (local canonical snapshot)\"\ngit tag -a v0.5.8 -m \"ReForma React canonical baseline v0.5.8\"\n```\n\n開発時（推奨）\n```bash\ngit checkout -b feature/<task-name>\n# 作業\ngit add .\ngit commit -m \"feat: <summary>\"\n```\n\n手元フルZIP生成（保険）\n```bash\ngit archive --format=zip --output=reforma-react-v0.5.8.zip v0.5.8\n```\n\n5. 仕様・参照ファイル（添付推奨）\n必須：reforma-root-only-policy-v1.0.json / openapi-reforma-v1.1-full.updated.yaml / ReForma_追補パッチ_表示モード_テーマ_計算フィールド_v1.0.1.json / condition-operator-matrix-ui-v1.0.json / reforma-frontend-handoff-v0.5.8.json\n推奨：02.ReForma-screen-spec-v1.1-consolidated.json / 06.ReForma React 運用・画面ui仕様書 V0.3.json / ReForma_Frontend_共有テンプレ_v1.1_追補反映.json\n\n6. 現状の実装済み（v0.5.8）\n- サイドバー：PC折りたたみ、モチーフロゴ(SVG)クリックで開閉、メニューアイコン化、ログアウト位置（ロゴ直下）、ボタン幅/サイズ/中央寄せ統一\n- ロゴグロー：ロゴ領域 hover/focus のみで発火（画面hoverでは発火しない）\n- ログアウトダイアログ：PC上寄り、モバイル中央\n- root-only：/auth/me の roles[] と is_root を正本にUI制御、403 reason=ROOT_ONLY を専用表示\n\n7. 次にやりたい作業\n- （ここに今回進めたい作業を記載）\n"
  }
}
```

## reforma-frontend-spec-v1.0.0-Frontend-共有テンプレ-.json

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0-Frontend-共有テンプレ-.json.json

```json
{
  "meta": {
    "title": "ReForma 開発チャット共有テンプレ（フロントエンド）",
    "version": "1.0",
    "generated_at": "2026-01-12T16:56:01.989787",
    "timezone": "Asia/Tokyo",
    "target": "React Frontend"
  },
  "paste_template": {
    "sections": [
      {
        "title": "前提",
        "body": [
          "本チャットは ReForma フロントエンド（React）実装フェーズの継続です。仕様の再検討はしません。",
          "フォーム機能・条件分岐UI（ビルダー＋公開フォーム）の実装、E2E整理を進めます。"
        ]
      },
      {
        "title": "正本仕様（必ず前提）",
        "body": [
          "01.ReForma-basic-spec-v1.1-consolidated.final.json",
          "02.ReForma-screen-spec-v1.1-consolidated.json",
          "condition-ui-spec-v1.0.json（F-03/F-05配置・保存先JSON・権限/文言/v1.x制約）",
          "form-feature-attachments-v1.1.json（A-06が条件分岐の正本）",
          "form-feature-spec-v1.0.complete.json",
          "06.ReForma React 運用・画面ui仕様書 V0.3.json",
          "フロントソース: reforma-react-v0.4.12.3.zip（次の開発は v0.5.0 から）"
        ]
      },
      {
        "title": "重要な設計原則（厳守）",
        "body": [
          "and/or は必ず明示（暗黙優先順位なし）",
          "v1.x では条件ネストは 1段まで",
          "評価不能時は安全側（非表示／必須解除／遷移不可）",
          "UIとAPIの二重防御（UI即時評価＋API最終確定）"
        ]
      },
      {
        "title": "フロントで扱う条件分岐I/F（ConditionState）",
        "body": [
          "API が返す ConditionState をそのまま UI に適用（fields.visible/required/store）",
          "reasons/eval は任意（UIは presence 依存しない）"
        ]
      },
      {
        "title": "既に作成済みの成果物（参照/生成）",
        "body": [
          "ReForma_条件分岐_評価結果IF_v1.0.json（ConditionState I/F）",
          "openapi-reforma-v1.1-full.yaml（APIクライアント生成/参照用）"
        ]
      },
      {
        "title": "今回のフロント実装対象（優先）",
        "body": [
          "F-03/F-05: 条件分岐ビルダーUI（1段ネスト制限、AND/OR明示、field type別 operator/value UI、保存JSONは condition-ui-spec に準拠）",
          "公開フォーム（/f/{form_key}）: ConditionState適用（非表示/必須解除/遷移不可）、submit 422 errors 表示",
          "E2E（Playwright等）: ビルダー保存→再読込再現、公開フォーム表示/必須/遷移、異常系フォールバック"
        ]
      },
      {
        "title": "出力してほしいもの",
        "body": [
          "実装チェックリスト / E2Eシナリオ（最小セット）",
          "ConditionState 適用の状態管理方針（Renderer/Builderの責務分離）"
        ]
      }
    ]
  },
  "attachments_to_share": {
    "must_include": [
      {
        "file": "ReForma_条件分岐_評価結果IF_v1.0.json",
        "path": "sandbox:/mnt/data/ReForma_条件分岐_評価結果IF_v1.0.json",
        "purpose": "ConditionState I/F（API→UI）"
      },
      {
        "file": "openapi-reforma-v1.1-full.yaml",
        "path": "sandbox:/mnt/data/openapi-reforma-v1.1-full.yaml",
        "purpose": "OpenAPI（API参照/クライアント生成）"
      },
      {
        "file": "condition-ui-spec-v1.0.json",
        "path": "sandbox:/mnt/data/condition-ui-spec-v1.0.json",
        "purpose": "条件分岐UI仕様（保存先JSON/配置/権限/文言）"
      },
      {
        "file": "form-feature-attachments-v1.1.json",
        "path": "sandbox:/mnt/data/form-feature-attachments-v1.1.json",
        "purpose": "Attachments（A-06 条件分岐 正本）"
      },
      {
        "file": "reforma-react-v0.4.12.3.zip",
        "path": "sandbox:/mnt/data/reforma-react-v0.4.12.3.zip",
        "purpose": "既存フロントソース（v0.5.0から開始）"
      }
    ],
    "reference_specs": [
      "02.ReForma-screen-spec-v1.1-consolidated.json（画面遷移/配置）",
      "06.ReForma React 運用・画面ui仕様書 V0.3.json（UI規約）"
    ]
  }
}
```

## reforma-frontend-spec-v1.0.0-condition-operator-matrix-ui-.json

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0-condition-operator-matrix-ui-.json.json

```json
{
  "metadata": {
    "document_id": "reforma-condition-operator-matrix",
    "title": "ReForma 条件分岐: field type × operator 許可表 + operator別 value_input UI（v1.x 推奨）",
    "version": "1.0.0",
    "status": "proposed",
    "timezone": "Asia/Tokyo",
    "generated_at": "2026-01-13T02:32:54.632904+09:00",
    "compatibility": {
      "condition_spec": "ReForma_条件分岐_実装整理パック_v1.0 (A-06 contract)",
      "constraints": {
        "max_nesting": 1,
        "max_conditions": 10,
        "logic_ops": [
          "and",
          "or",
          "not"
        ],
        "comparison_ops": [
          "eq",
          "ne",
          "in",
          "contains",
          "gt",
          "gte",
          "lt",
          "lte",
          "between",
          "exists"
        ]
      }
    },
    "notes": [
      "本JSONは attachments 化を前提に、仕様書/実装で共通利用できるように正規化している。",
      "UIは『row = field_selector / operator_selector / value_input』を前提とする。",
      "logic_ops(and/or/not) は型依存しない（グループ構築用）。本表は comparison_ops の許可を中心に定義する。"
    ]
  },
  "attachments": {
    "index": [
      {
        "attachment_id": "ATTACHMENT_CONDITION_FIELD_TYPE_GROUPS_V1",
        "title": "フィールド型グルーピング（条件分岐用）",
        "kind": "mapping"
      },
      {
        "attachment_id": "ATTACHMENT_CONDITION_OPERATOR_CATALOG_V1",
        "title": "演算子カタログ（logic/comparison）",
        "kind": "catalog"
      },
      {
        "attachment_id": "ATTACHMENT_CONDITION_OPERATOR_MATRIX_V1",
        "title": "field type group × operator 許可表（comparison）",
        "kind": "matrix"
      },
      {
        "attachment_id": "ATTACHMENT_CONDITION_VALUE_INPUT_UI_V1",
        "title": "operator別 value_input UI 推奨",
        "kind": "ui_spec"
      }
    ],
    "items": [
      {
        "attachment_id": "ATTACHMENT_CONDITION_FIELD_TYPE_GROUPS_V1",
        "kind": "mapping",
        "field_type_groups": [
          {
            "group_id": "text_like",
            "label": {
              "ja": "テキスト系",
              "en": "Text-like",
              "zh": "文本类"
            },
            "field_types": [
              "text",
              "textarea",
              "email",
              "tel"
            ],
            "value_shape": "string"
          },
          {
            "group_id": "number",
            "label": {
              "ja": "数値",
              "en": "Number",
              "zh": "数值"
            },
            "field_types": [
              "number"
            ],
            "value_shape": "number"
          },
          {
            "group_id": "date_like",
            "label": {
              "ja": "日付/日時",
              "en": "Date/Datetime",
              "zh": "日期/日期时间"
            },
            "field_types": [
              "date",
              "datetime"
            ],
            "value_shape": "date_or_datetime"
          },
          {
            "group_id": "choice_single",
            "label": {
              "ja": "選択（単一）",
              "en": "Single choice",
              "zh": "单选"
            },
            "field_types": [
              "select",
              "radio"
            ],
            "value_shape": "string"
          },
          {
            "group_id": "choice_multi",
            "label": {
              "ja": "選択（複数）",
              "en": "Multi choice",
              "zh": "多选"
            },
            "field_types": [
              "checkbox"
            ],
            "value_shape": "array<string>"
          },
          {
            "group_id": "boolean",
            "label": {
              "ja": "真偽（同意）",
              "en": "Boolean (agree)",
              "zh": "布尔（同意）"
            },
            "field_types": [
              "agree"
            ],
            "value_shape": "boolean"
          },
          {
            "group_id": "file",
            "label": {
              "ja": "ファイル",
              "en": "File",
              "zh": "文件"
            },
            "field_types": [
              "file"
            ],
            "value_shape": "file_state"
          },
          {
            "group_id": "display_only",
            "label": {
              "ja": "表示のみ（値なし）",
              "en": "Display-only",
              "zh": "仅展示"
            },
            "field_types": [
              "section",
              "paragraph"
            ],
            "value_shape": "none"
          }
        ],
        "resolution_rules": [
          "未知の field_type は display_only と同等に扱い（comparison禁止）、exists のみ許可するか、UIから除外する。",
          "複数の field_type が同一 group に属する場合は group の許可表を適用する。"
        ]
      },
      {
        "attachment_id": "ATTACHMENT_CONDITION_OPERATOR_CATALOG_V1",
        "kind": "catalog",
        "operators": [
          {
            "op": "and",
            "kind": "logic",
            "label": {
              "ja": "AND（すべて満たす）",
              "en": "AND (all)",
              "zh": "且（全部满足）"
            },
            "description": {
              "ja": "子条件をすべて満たす",
              "en": "All child conditions must match",
              "zh": "所有子条件都需满足"
            }
          },
          {
            "op": "or",
            "kind": "logic",
            "label": {
              "ja": "OR（いずれか満たす）",
              "en": "OR (any)",
              "zh": "或（任一满足）"
            },
            "description": {
              "ja": "子条件のいずれかを満たす",
              "en": "Any child condition matches",
              "zh": "任一子条件满足即可"
            }
          },
          {
            "op": "not",
            "kind": "logic",
            "label": {
              "ja": "NOT（否定）",
              "en": "NOT",
              "zh": "非"
            },
            "description": {
              "ja": "子条件を否定する（v1.xはネスト1まで）",
              "en": "Negates a child condition (max nesting 1)",
              "zh": "对子条件取反（v1.x最多1层嵌套）"
            }
          },
          {
            "op": "eq",
            "kind": "comparison",
            "label": {
              "ja": "＝（一致）",
              "en": "Equals",
              "zh": "等于"
            },
            "value_shape": "scalar"
          },
          {
            "op": "ne",
            "kind": "comparison",
            "label": {
              "ja": "≠（不一致）",
              "en": "Not equals",
              "zh": "不等于"
            },
            "value_shape": "scalar"
          },
          {
            "op": "in",
            "kind": "comparison",
            "label": {
              "ja": "含む（いずれか一致）",
              "en": "In (any of)",
              "zh": "包含（任一匹配）"
            },
            "value_shape": "array"
          },
          {
            "op": "contains",
            "kind": "comparison",
            "label": {
              "ja": "部分一致（含む）",
              "en": "Contains",
              "zh": "包含（子串）"
            },
            "value_shape": "string"
          },
          {
            "op": "gt",
            "kind": "comparison",
            "label": {
              "ja": "＞",
              "en": "Greater than",
              "zh": "大于"
            },
            "value_shape": "scalar"
          },
          {
            "op": "gte",
            "kind": "comparison",
            "label": {
              "ja": "≧",
              "en": "Greater or equal",
              "zh": "大于等于"
            },
            "value_shape": "scalar"
          },
          {
            "op": "lt",
            "kind": "comparison",
            "label": {
              "ja": "＜",
              "en": "Less than",
              "zh": "小于"
            },
            "value_shape": "scalar"
          },
          {
            "op": "lte",
            "kind": "comparison",
            "label": {
              "ja": "≦",
              "en": "Less or equal",
              "zh": "小于等于"
            },
            "value_shape": "scalar"
          },
          {
            "op": "between",
            "kind": "comparison",
            "label": {
              "ja": "範囲（between）",
              "en": "Between",
              "zh": "区间"
            },
            "value_shape": "range"
          },
          {
            "op": "exists",
            "kind": "comparison",
            "label": {
              "ja": "値がある/ない",
              "en": "Exists",
              "zh": "有值/无值"
            },
            "value_shape": "boolean"
          }
        ],
        "ui_grouping_recommendation": [
          {
            "group": "basic",
            "ops": [
              "eq",
              "ne",
              "in",
              "contains"
            ]
          },
          {
            "group": "numeric_date",
            "ops": [
              "gt",
              "gte",
              "lt",
              "lte",
              "between"
            ]
          },
          {
            "group": "presence",
            "ops": [
              "exists"
            ]
          }
        ]
      },
      {
        "attachment_id": "ATTACHMENT_CONDITION_OPERATOR_MATRIX_V1",
        "kind": "matrix",
        "matrix_type": "group_x_operator",
        "applies_to": {
          "dimension_x": "field_type_group_id",
          "dimension_y": "comparison_operator"
        },
        "allow": {
          "text_like": [
            "eq",
            "ne",
            "in",
            "contains",
            "exists"
          ],
          "number": [
            "eq",
            "ne",
            "in",
            "gt",
            "gte",
            "lt",
            "lte",
            "between",
            "exists"
          ],
          "date_like": [
            "eq",
            "ne",
            "in",
            "gt",
            "gte",
            "lt",
            "lte",
            "between",
            "exists"
          ],
          "choice_single": [
            "eq",
            "ne",
            "in",
            "exists"
          ],
          "choice_multi": [
            "in",
            "exists"
          ],
          "boolean": [
            "eq",
            "ne",
            "exists"
          ],
          "file": [
            "exists"
          ],
          "display_only": []
        },
        "policy_notes": [
          "logic_ops(and/or/not) は型依存しないため本matrix対象外。",
          "choice_multi(checkbox) の eq/ne は意味がぶれやすいため v1.x 推奨では許可しない（any-of は in を使用）。",
          "file は v1.x 推奨では exists のみに限定（アップロード有無の判定）。"
        ],
        "frontend_behavior": {
          "operator_selector_filtering": "フィールド選択後、matrix.allow[group] に含まれる op のみ表示する。",
          "invalid_operator_on_load": "既存ルールが matrix 外の場合は、UI上で警告表示し、保存時にバリデーションエラーとする（もしくは自動変換せず保持する）。"
        }
      },
      {
        "attachment_id": "ATTACHMENT_CONDITION_VALUE_INPUT_UI_V1",
        "kind": "ui_spec",
        "row_model": {
          "fields": [
            "field_selector",
            "operator_selector",
            "value_input"
          ],
          "notes": [
            "value_input は operator と field_type_group により型/部品が決定される。",
            "exists は value を boolean 固定（true/false）として扱い、入力はトグル/セグメントで提供する。"
          ]
        },
        "operator_ui": [
          {
            "operator": "eq",
            "value_shape": "scalar",
            "ui": {
              "component_by_group": {
                "text_like": "TextInput",
                "number": "NumberInput",
                "date_like": "DateOrDatetimePicker",
                "choice_single": "SingleSelect",
                "choice_multi": "N/A (use 'in')",
                "boolean": "BooleanSegment",
                "file": "N/A (use 'exists')"
              }
            },
            "validation": {
              "required": true
            }
          },
          {
            "operator": "ne",
            "value_shape": "scalar",
            "ui": {
              "component_by_group": {
                "text_like": "TextInput",
                "number": "NumberInput",
                "date_like": "DateOrDatetimePicker",
                "choice_single": "SingleSelect",
                "choice_multi": "N/A (use 'in')",
                "boolean": "BooleanSegment",
                "file": "N/A (use 'exists')"
              }
            },
            "validation": {
              "required": true
            }
          },
          {
            "operator": "in",
            "value_shape": "array",
            "ui": {
              "component_by_group": {
                "text_like": "TagInput (Enter to add)",
                "number": "TagInputNumeric (Enter to add)",
                "date_like": "MultiDatePicker (or TagInputDate)",
                "choice_single": "MultiSelect",
                "choice_multi": "MultiSelect (options)",
                "boolean": "N/A",
                "file": "N/A"
              },
              "display_hint": {
                "choice_multi": {
                  "ja": "含む（いずれか一致）",
                  "en": "Includes any of",
                  "zh": "包含任一"
                }
              }
            },
            "validation": {
              "min_items": 1
            }
          },
          {
            "operator": "contains",
            "value_shape": "string",
            "ui": {
              "component": "TextInput",
              "placeholder_i18n_key": "condition.value.contains.placeholder"
            },
            "validation": {
              "required": true
            }
          },
          {
            "operator": "gt",
            "value_shape": "scalar",
            "ui": {
              "component_by_group": {
                "number": "NumberInput",
                "date_like": "DateOrDatetimePicker"
              }
            },
            "validation": {
              "required": true
            }
          },
          {
            "operator": "gte",
            "value_shape": "scalar",
            "ui": {
              "component_by_group": {
                "number": "NumberInput",
                "date_like": "DateOrDatetimePicker"
              }
            },
            "validation": {
              "required": true
            }
          },
          {
            "operator": "lt",
            "value_shape": "scalar",
            "ui": {
              "component_by_group": {
                "number": "NumberInput",
                "date_like": "DateOrDatetimePicker"
              }
            },
            "validation": {
              "required": true
            }
          },
          {
            "operator": "lte",
            "value_shape": "scalar",
            "ui": {
              "component_by_group": {
                "number": "NumberInput",
                "date_like": "DateOrDatetimePicker"
              }
            },
            "validation": {
              "required": true
            }
          },
          {
            "operator": "between",
            "value_shape": "range",
            "ui": {
              "component_by_group": {
                "number": "RangeNumber (from/to)",
                "date_like": "RangeDateOrDatetime (from/to)"
              },
              "labels_i18n": {
                "from": "condition.value.between.from",
                "to": "condition.value.between.to"
              }
            },
            "validation": {
              "required": true,
              "both_required": true,
              "from_lte_to": true
            }
          },
          {
            "operator": "exists",
            "value_shape": "boolean",
            "ui": {
              "component": "BooleanSegment",
              "options": [
                {
                  "value": true,
                  "label_i18n_key": "condition.value.exists.true"
                },
                {
                  "value": false,
                  "label_i18n_key": "condition.value.exists.false"
                }
              ]
            },
            "validation": {
              "required": true
            }
          }
        ],
        "i18n_keys_minimum_set": [
          "condition.operator.eq",
          "condition.operator.ne",
          "condition.operator.in",
          "condition.operator.contains",
          "condition.operator.gt",
          "condition.operator.gte",
          "condition.operator.lt",
          "condition.operator.lte",
          "condition.operator.between",
          "condition.operator.exists",
          "condition.value.contains.placeholder",
          "condition.value.between.from",
          "condition.value.between.to",
          "condition.value.exists.true",
          "condition.value.exists.false"
        ]
      }
    ]
  }
}
```

## reforma-frontend-spec-v1.0.0-condition-ui-.json

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0-condition-ui-.json.json

```json
{
  "meta": {
    "title": "条件分岐 UI 仕様（06.UI 連携）",
    "version": "1.0",
    "generated_at": "2026-01-12T15:23:57.297125",
    "depends_on": [
      "フォーム機能別表（Attachments） v1.1 / A-06",
      "条件分岐 UI 操作例 v1.0",
      "06.ReForma React 運用・画面ui仕様書"
    ]
  },
  "screens": {
    "F-03_field_edit": {
      "visibility_rule": {
        "label": "次の条件を満たすとき表示",
        "toggle": true,
        "save_as": "field.visibility_rule"
      },
      "required_rule": {
        "label": "次の条件を満たすとき必須",
        "toggle": true,
        "exclusive_with": "is_required",
        "save_as": "field.required_rule"
      }
    },
    "F-05_step_edit": {
      "transition_rule": {
        "label": "次へ進む条件",
        "toggle": true,
        "save_as": "step.transition_rule"
      }
    }
  },
  "builder": {
    "row": [
      "field_selector",
      "operator_selector",
      "value_input"
    ],
    "logic": {
      "group": [
        "AND",
        "OR"
      ],
      "nesting": "max_1_level_v1"
    },
    "validation": [
      "field_required",
      "type_match",
      "no_self_reference"
    ]
  },
  "permissions": {
    "edit": [
      "form_admin",
      "system_admin",
      "root"
    ],
    "view": [
      "viewer",
      "operator"
    ]
  },
  "storage": {
    "field": {
      "visibility_rule": "form_definition.fields[].visibility_rule",
      "required_rule": "form_definition.fields[].required_rule"
    },
    "step": {
      "transition_rule": "form_definition.steps[].transition_rule"
    }
  },
  "constraints": {
    "max_conditions": 10,
    "max_nesting": 1
  }
}
```

## reforma-frontend-spec-v1.0.0-condition-ui-examples-.json

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0-condition-ui-examples-.json.json

```json
{
  "meta": {
    "title": "条件分岐 UI 操作例 v1.0",
    "version": "1.0",
    "generated_at": "2026-01-12T15:17:18.777520",
    "positioning": {
      "canonical_rules": "フォーム機能別表（Attachments） v1.1 / A-06",
      "this_doc": "UI creation examples + saved JSON examples"
    }
  },
  "assumptions": {
    "form_code": "CONTACT_2026",
    "fields": [
      {
        "field_key": "category",
        "type": "select",
        "label": "お問い合わせ種別"
      },
      {
        "field_key": "company_name",
        "type": "text",
        "label": "会社名"
      },
      {
        "field_key": "department",
        "type": "text",
        "label": "部署"
      },
      {
        "field_key": "email",
        "type": "email",
        "label": "メール"
      },
      {
        "field_key": "terms",
        "type": "terms",
        "label": "同意"
      }
    ],
    "steps": [
      {
        "step": "STEP1",
        "fields": [
          "category",
          "company_name",
          "department",
          "email"
        ]
      },
      {
        "step": "STEP2",
        "fields": [
          "terms"
        ]
      }
    ]
  },
  "examples": [
    {
      "id": "ex1_visibility_department_by_category",
      "target": {
        "kind": "field",
        "field_key": "department"
      },
      "rule_type": "visibility_rule",
      "ui_steps": [
        "フォーム編集→項目→department",
        "表示条件(Visibility) ON",
        "条件: category == business",
        "プレビュー確認→保存"
      ],
      "saved_rule": {
        "version": "1",
        "op": "eq",
        "field": "category",
        "value": "business"
      },
      "expected_behavior": [
        "category=business → department表示",
        "otherwise → 非表示（値は保存しない）"
      ]
    },
    {
      "id": "ex2_required_department_when_company_name_exists",
      "target": {
        "kind": "field",
        "field_key": "department"
      },
      "rule_type": "required_rule",
      "ui_steps": [
        "department を選択",
        "固定必須はOFF",
        "必須条件(Required condition) ON",
        "条件: company_name exists",
        "保存"
      ],
      "saved_rule": {
        "version": "1",
        "op": "exists",
        "field": "company_name",
        "value": true
      },
      "expected_behavior": [
        "company_name empty → department任意",
        "company_name filled → department必須"
      ]
    },
    {
      "id": "ex3_visibility_or_group",
      "target": {
        "kind": "field",
        "field_key": "department"
      },
      "rule_type": "visibility_rule",
      "ui_steps": [
        "department → 表示条件",
        "論理結合を OR に設定",
        "条件1: category == business",
        "条件2: company_name exists",
        "保存"
      ],
      "saved_rule": {
        "version": "1",
        "op": "or",
        "items": [
          {
            "op": "eq",
            "field": "category",
            "value": "business"
          },
          {
            "op": "exists",
            "field": "company_name",
            "value": true
          }
        ]
      },
      "expected_behavior": [
        "category=business または company_name 入力済み → 表示",
        "それ以外 → 非表示"
      ]
    },
    {
      "id": "ex4_step_transition_terms_required",
      "target": {
        "kind": "step",
        "step": "STEP2"
      },
      "rule_type": "step_transition_rule",
      "ui_steps": [
        "STEP設定→STEP2",
        "次へ進む条件(Transition) ON",
        "条件: terms == true",
        "保存"
      ],
      "saved_rule": {
        "version": "1",
        "op": "eq",
        "field": "terms",
        "value": true
      },
      "expected_behavior": [
        "terms未同意 → 遷移不可＋エラー",
        "terms同意 → 遷移可"
      ]
    }
  ],
  "implementation_notes": [
    "and/or を必ず明示して保存する（暗黙優先順位なし）",
    "UIはfield_keyを選択式にして未定義参照を防ぐ",
    "評価不能時は安全側（非表示／必須解除／遷移不可）"
  ]
}
```

## reforma-frontend-spec-v1.0.0-frontend-chat-init.json

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0-frontend-chat-init.json.json

```json
{
  "purpose": "ReForma Frontend 新規チャット初期共有テンプレ",
  "role": "Frontend single source of truth",
  "baseline": {
    "version": "v0.4.12.3",
    "type": "full zip"
  },
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
  "current_target": {
    "screen": "S-02 アカウント一覧",
    "role": "System Admin",
    "features": [
      "list",
      "search",
      "filter",
      "sort",
      "pagination",
      "bulk invite resend"
    ]
  },
  "rules": {
    "routing": "401/419 -> /logout?reason=session_invalid",
    "title": "breadcrumb と一致",
    "theme": "ReForma 背景共通",
    "diff_policy": "diff zip 管理"
  }
}
```

## reforma-frontend-spec-v1.0.0-frontend-handoff-20260112.json

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0-frontend-handoff-20260112.json.json

```json
{
  "meta": {
    "project": "ReForma",
    "channel": "Frontend handoff from Backend chat",
    "date": "2026-01-12",
    "timezone": "Asia/Tokyo",
    "version": "backend-handoff-20260112-01"
  },
  "api": {
    "mount": {
      "spa_base": "/reforma/",
      "api_base": "/reforma/api/",
      "version_prefix": "/v1",
      "example": "/reforma/api/v1/auth/me"
    },
    "routing_rule": {
      "no_api_double_prefix": true,
      "note": "Laravel側では /api プレフィックスを使わず、/v1 を先頭にする。Apache Alias が /reforma/api/ を担当。"
    },
    "response_envelope": {
      "shape": {
        "success": "boolean",
        "data": "any",
        "message": "string|null",
        "errors": "object|null"
      },
      "error_extras": {
        "code": "string|null",
        "request_id": "string"
      }
    },
    "list_policy": {
      "page_required": true,
      "per_page_required": true,
      "sort_optional": true,
      "sort_enum": [
        "created_at_desc",
        "created_at_asc"
      ],
      "default_sort": "created_at_desc",
      "response_fields_required": [
        "items",
        "total",
        "page",
        "per_page"
      ]
    }
  },
  "auth": {
    "frontend_behavior_already_confirmed": {
      "session_invalid_handling": {
        "trigger_statuses": [
          401,
          419
        ],
        "redirect": "/logout?reason=session_invalid",
        "logout_page_public": true,
        "client_state": "front invalidates logged-in state"
      }
    },
    "admin_auth": {
      "method": "Sanctum Personal Access Token (PAT)",
      "token_transport": "Authorization: Bearer <token>",
      "token_ttl_days_default": 30,
      "token_ttl_configurable": true,
      "rolling_extension": {
        "enabled": true,
        "update_frequency": "once_per_day",
        "expired_behavior": {
          "http_status": 401,
          "code": "TOKEN_EXPIRED"
        }
      }
    },
    "respondent_auth": {
      "method": "session-based per SUP spec",
      "authorization_for_confirm_url": "token-based (confirm_url token) is sufficient",
      "respondent_session_scope": "same browser may cross multiple forms (state may persist), but authorization remains token-based"
    }
  },
  "roles": {
    "system_admin": {
      "fixed": true,
      "constraints": [
        "system_admin must never become 0",
        "cannot revoke own system_admin",
        "cannot disable self"
      ]
    },
    "others": {
      "modifiable": true,
      "recommended_immutables": [
        "slug"
      ],
      "modifiable_fields": [
        "display_name",
        "permission_assignment"
      ]
    }
  },
  "confirm_url": {
    "token_storage": "store only token_hash in DB; raw token appears only in URL",
    "token_types": {
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
    "ttl_configurable_via_settings": true,
    "one_time_configurable": {
      "view_pdf": true
    }
  },
  "pdf": {
    "storage": {
      "default": "S3",
      "switchable": [
        "local"
      ],
      "reason": "production has 2 web servers; avoid local divergence"
    },
    "regeneration_policy": {
      "source_of_truth": "submission-time snapshot",
      "default": "do not regenerate",
      "exception": "system_admin explicit action with audit log"
    }
  },
  "queue": {
    "driver": "database",
    "dlq_equivalent": "failed_jobs",
    "worker": "systemd (recommended)",
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
    ]
  },
  "settings": {
    "storage": "DB table: settings",
    "scope": "system (fixed for now)",
    "initial_impl": "no UI; initial values inserted manually or via seeder/SQL; app reads via cache",
    "recommended_schema": {
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
  }
}
```

## 共通レイアウト

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0.json

```json
{
  "id": "section.common.layout",
  "type": "common",
  "title": "共通レイアウト",
  "layout": {
    "header": {
      "elements": [
        "system_name",
        "user_info",
        "logout_action"
      ]
    },
    "sidebar": {
      "behavior": "role_based_menu"
    },
    "content": {
      "behavior": "screen_specific"
    }
  }
}
```

## 権限制御

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0.json

```json
{
  "id": "section.common.authorization",
  "type": "common",
  "title": "権限制御",
  "authorization": {
    "model": "role_based",
    "roles": {
      "viewer": {
        "description": "参照権限（閲覧可能範囲内）"
      },
      "operator": {
        "description": "運用権限（回答・検索の運用）"
      },
      "form_admin": {
        "description": "フォーム管理権限（フォーム作成・編集・項目設定）"
      },
      "system_admin": {
        "description": "システム管理権限（全機能・ログ閲覧）"
      }
    },
    "enforcement": [
      "screen_level",
      "field_level"
    ],
    "rules": [
      "user は自身の権限範囲を超える情報を閲覧できない"
    ]
  }
}
```

## 多言語対応

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0.json

```json
{
  "id": "section.common.i18n",
  "type": "common",
  "title": "多言語対応",
  "i18n": {
    "languages": [
      "ja",
      "en",
      "zh"
    ],
    "strategy": "i18n_dictionary",
    "requirements": [
      "画面文言はすべて i18n キーで管理する"
    ]
  }
}
```

## バリデーション・エラー表示

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0.json

```json
{
  "id": "section.common.validation_and_errors",
  "type": "common",
  "title": "バリデーション・エラー表示",
  "validation": {
    "ui": {
      "on_field": "immediate",
      "on_submit": "full"
    }
  },
  "errors": {
    "ui": {
      "api_error_display": [
        "toast",
        "error_screen"
      ]
    },
    "references": {
      "error_code_ref": "ERROR_CODES_V1"
    }
  }
}
```

## ログイン画面

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0.json

```json
{
  "id": "section.screen.A-01.LOGIN",
  "type": "screen",
  "screen_no": "A-01",
  "screen_id": "LOGIN",
  "title": "ログイン画面",
  "role": "ReForma 管理画面への認証を行う",
  "permissions": {
    "allow_roles": [
      "viewer",
      "operator",
      "form_admin",
      "system_admin"
    ]
  },
  "route": {
    "path": "/login"
  },
  "apis": [
    {
      "method": "POST",
      "path": "/api/v1/auth/login",
      "purpose": "認証"
    },
    {
      "method": "GET",
      "path": "/api/v1/auth/me",
      "purpose": "ログインユーザー取得"
    }
  ],
  "ui": {
    "fields": [
      {
        "key": "email",
        "required": true
      },
      {
        "key": "password",
        "required": true
      }
    ],
    "actions": [
      {
        "key": "submit_login"
      }
    ]
  },
  "errors": [
    {
      "code": "AUTH_FAILED",
      "ref": "ERROR_CODES_V1"
    }
  ]
}
```

## ログアウト

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0.json

```json
{
  "id": "section.screen.A-02.LOGOUT",
  "type": "screen",
  "screen_no": "A-02",
  "screen_id": "LOGOUT",
  "title": "ログアウト",
  "role": "ログアウト処理を行いログイン画面へ遷移する",
  "permissions": {
    "allow_roles": [
      "viewer",
      "operator",
      "form_admin",
      "system_admin"
    ]
  },
  "route": {
    "path": "/logout"
  },
  "apis": [
    {
      "method": "POST",
      "path": "/api/v1/auth/logout",
      "purpose": "セッション破棄"
    }
  ],
  "ui": {
    "actions": [
      {
        "key": "execute_logout"
      }
    ]
  }
}
```

## システム管理ダッシュボード

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0.json

```json
{
  "id": "section.screen.S-01.SYS_DASH",
  "type": "screen",
  "screen_no": "S-01",
  "screen_id": "SYS_DASH",
  "title": "システム管理ダッシュボード",
  "role": "ログインユーザーが自身の権限範囲内で閲覧可能な情報を俯瞰する",
  "permissions": {
    "allow_roles": [
      "viewer",
      "operator",
      "form_admin",
      "system_admin"
    ]
  },
  "route": {
    "path": "/dashboard"
  },
  "apis": [
    {
      "method": "GET",
      "path": "/api/v1/dashboard/summary",
      "purpose": "サマリー"
    },
    {
      "method": "GET",
      "path": "/api/v1/dashboard/forms",
      "purpose": "閲覧可能フォーム情報"
    },
    {
      "method": "GET",
      "path": "/api/v1/dashboard/responses",
      "purpose": "閲覧可能回答サマリー"
    },
    {
      "method": "GET",
      "path": "/api/v1/dashboard/errors",
      "purpose": "エラーサマリー（system_adminのみ）",
      "constraints": {
        "allow_roles": [
          "system_admin"
        ]
      }
    }
  ],
  "ui": {
    "blocks_by_role": {
      "viewer": {
        "blocks": [
          {
            "key": "accessible_form_count"
          },
          {
            "key": "accessible_response_count"
          },
          {
            "key": "recent_responses_readonly"
          },
          {
            "key": "notices"
          }
        ]
      },
      "operator": {
        "blocks": [
          {
            "key": "unprocessed_response_count"
          },
          {
            "key": "responses_by_period"
          },
          {
            "key": "notification_status_summary"
          },
          {
            "key": "minor_error_warnings"
          }
        ]
      },
      "form_admin": {
        "blocks": [
          {
            "key": "form_level_aggregations"
          },
          {
            "key": "ack_pdf_setting_status"
          },
          {
            "key": "recent_form_setting_changes"
          }
        ]
      },
      "system_admin": {
        "blocks": [
          {
            "key": "system_error_summary"
          },
          {
            "key": "processing_failure_summary"
          },
          {
            "key": "link_to_logs"
          },
          {
            "key": "system_info"
          }
        ]
      }
    }
  }
}
```

## フォーム一覧

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0.json

```json
{
  "id": "section.screen.F-01.FORM_LIST",
  "type": "screen",
  "screen_no": "F-01",
  "screen_id": "FORM_LIST",
  "title": "フォーム一覧",
  "role": "フォームの作成・管理の起点",
  "permissions": {
    "allow_roles": [
      "form_admin",
      "system_admin"
    ]
  },
  "route": {
    "path": "/forms"
  },
  "apis": [
    {
      "method": "GET",
      "path": "/api/v1/forms",
      "purpose": "フォーム一覧"
    },
    {
      "method": "POST",
      "path": "/api/v1/forms",
      "purpose": "フォーム作成"
    }
  ],
  "ui": {
    "list": {
      "columns": [
        "form_name",
        "status",
        "languages",
        "response_count"
      ],
      "actions": [
        {
          "key": "open_form_edit"
        },
        {
          "key": "open_form_preview"
        }
      ]
    }
  }
}
```

## フォーム編集

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0.json

```json
{
  "id": "section.screen.F-02.FORM_EDIT",
  "type": "screen",
  "screen_no": "F-02",
  "screen_id": "FORM_EDIT",
  "title": "フォーム編集",
  "role": "フォーム基本情報の設定",
  "permissions": {
    "allow_roles": [
      "form_admin",
      "system_admin"
    ]
  },
  "route": {
    "path": "/forms/{form_id}/edit"
  },
  "apis": [
    {
      "method": "GET",
      "path": "/api/v1/forms/{form_id}",
      "purpose": "フォーム取得"
    },
    {
      "method": "PUT",
      "path": "/api/v1/forms/{form_id}",
      "purpose": "フォーム更新"
    }
  ],
  "ui": {
    "fields": [
      {
        "key": "form_name_i18n",
        "required": true
      },
      {
        "key": "description_i18n",
        "required": false
      },
      {
        "key": "publish_status",
        "required": true
      },
      {
        "key": "post_submit_behavior",
        "required": true,
        "values": [
          "ack",
          "redirect"
        ]
      }
    ],
    "actions": [
      {
        "key": "save"
      }
    ]
  }
}
```

## フォーム項目設定

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
    }
  }
}
```

## フォームプレビュー

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
    ]
  }
}
```

## 公開フォーム画面

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
    ]
  },
  "errors": [
    {
      "code": "VALIDATION_ERROR",
      "ref": "ERROR_CODES_V1"
    }
  ]
}
```

## ACK（受付完了）画面

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0.json

```json
{
  "id": "section.screen.A-03.ACK_VIEW",
  "type": "screen",
  "screen_no": "A-03",
  "screen_id": "ACK_VIEW",
  "title": "ACK（受付完了）画面",
  "role": "フォーム送信完了を通知する",
  "permissions": {
    "allow_roles": [
      "public"
    ]
  },
  "route": {
    "path": "/f/{form_key}/ack"
  },
  "apis": [
    {
      "method": "GET",
      "path": "/api/v1/public/forms/{form_key}/ack",
      "purpose": "ACK 表示情報"
    }
  ],
  "ui": {
    "blocks": [
      {
        "key": "completion_message_i18n"
      },
      {
        "key": "receipt_number",
        "optional": true
      },
      {
        "key": "notes_i18n",
        "optional": true
      }
    ]
  }
}
```

## 回答一覧

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0.json

```json
{
  "id": "section.screen.R-01.RESPONSE_LIST",
  "type": "screen",
  "screen_no": "R-01",
  "screen_id": "RESPONSE_LIST",
  "title": "回答一覧",
  "role": "フォーム回答の一覧・検索を行う",
  "permissions": {
    "allow_roles": [
      "operator",
      "form_admin",
      "system_admin"
    ]
  },
  "route": {
    "path": "/responses"
  },
  "apis": [
    {
      "method": "GET",
      "path": "/api/v1/responses",
      "purpose": "回答一覧"
    }
  ],
  "ui": {
    "list": {
      "columns": [
        "received_at",
        "form_name",
        "status"
      ],
      "actions": [
        {
          "key": "open_response_detail"
        }
      ]
    }
  }
}
```

## 回答詳細

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0.json

```json
{
  "id": "section.screen.R-02.RESPONSE_DETAIL",
  "type": "screen",
  "screen_no": "R-02",
  "screen_id": "RESPONSE_DETAIL",
  "title": "回答詳細",
  "role": "個別の回答内容を確認する",
  "permissions": {
    "allow_roles": [
      "operator",
      "form_admin",
      "system_admin"
    ]
  },
  "route": {
    "path": "/responses/{response_id}"
  },
  "apis": [
    {
      "method": "GET",
      "path": "/api/v1/responses/{response_id}",
      "purpose": "回答詳細"
    }
  ],
  "ui": {
    "blocks": [
      {
        "key": "response_header"
      },
      {
        "key": "answers"
      },
      {
        "key": "status_and_actions"
      }
    ]
  }
}
```

## 処理ログ一覧

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0.json

```json
{
  "id": "section.screen.L-01.LOG_LIST",
  "type": "screen",
  "screen_no": "L-01",
  "screen_id": "LOG_LIST",
  "title": "処理ログ一覧",
  "role": "API・通知・PDF 処理ログを確認する",
  "permissions": {
    "allow_roles": [
      "system_admin"
    ]
  },
  "route": {
    "path": "/logs"
  },
  "apis": [
    {
      "method": "GET",
      "path": "/api/v1/logs",
      "purpose": "ログ一覧"
    }
  ],
  "ui": {
    "list": {
      "columns": [
        "created_at",
        "category",
        "status",
        "message"
      ],
      "actions": [
        {
          "key": "open_log_detail"
        }
      ]
    }
  }
}
```

## 処理ログ詳細

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0.json

```json
{
  "id": "section.screen.L-02.LOG_DETAIL",
  "type": "screen",
  "screen_no": "L-02",
  "screen_id": "LOG_DETAIL",
  "title": "処理ログ詳細",
  "role": "処理ログの詳細を確認する",
  "permissions": {
    "allow_roles": [
      "system_admin"
    ]
  },
  "route": {
    "path": "/logs/{log_id}"
  },
  "apis": [
    {
      "method": "GET",
      "path": "/api/v1/logs/{log_id}",
      "purpose": "ログ詳細"
    }
  ],
  "ui": {
    "blocks": [
      {
        "key": "log_header"
      },
      {
        "key": "payload_excerpt",
        "note": "実体スキーマは attachments に分離"
      },
      {
        "key": "error_details"
      }
    ]
  }
}
```

## 横断検索画面

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0.json

```json
{
  "id": "section.screen.C-01.SEARCH",
  "type": "screen",
  "screen_no": "C-01",
  "screen_id": "SEARCH",
  "title": "横断検索画面",
  "role": "フォーム・回答・ログを横断的に検索する",
  "permissions": {
    "allow_roles": [
      "operator",
      "form_admin",
      "system_admin"
    ]
  },
  "route": {
    "path": "/search"
  },
  "apis": [
    {
      "method": "GET",
      "path": "/api/v1/search",
      "purpose": "横断検索"
    }
  ],
  "ui": {
    "query": {
      "fields": [
        "keyword",
        "from_date",
        "to_date",
        "category"
      ]
    },
    "results": {
      "sections": [
        "forms",
        "responses",
        "logs"
      ]
    }
  }
}
```

## エラー画面

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0.json

```json
{
  "id": "section.screen.E-01.ERROR",
  "type": "screen",
  "screen_no": "E-01",
  "screen_id": "ERROR",
  "title": "エラー画面",
  "role": "権限エラー等の共通エラー表示",
  "permissions": {
    "allow_roles": [
      "viewer",
      "operator",
      "form_admin",
      "system_admin",
      "public"
    ]
  },
  "route": {
    "path": "/error"
  },
  "ui": {
    "blocks": [
      {
        "key": "error_title"
      },
      {
        "key": "error_message"
      },
      {
        "key": "guidance"
      }
    ]
  },
  "references": {
    "error_code_ref": "ERROR_CODES_V1"
  }
}
```

## Not Found（404）画面

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0.json

```json
{
  "id": "section.screen.N-01.NOT_FOUND",
  "type": "screen",
  "screen_no": "N-01",
  "screen_id": "NOT_FOUND",
  "title": "Not Found（404）画面",
  "role": "存在しないページへのアクセス時に表示",
  "permissions": {
    "allow_roles": [
      "viewer",
      "operator",
      "form_admin",
      "system_admin",
      "public"
    ]
  },
  "route": {
    "path": "*"
  },
  "ui": {
    "blocks": [
      {
        "key": "not_found_title"
      },
      {
        "key": "not_found_message"
      },
      {
        "key": "link_to_home"
      }
    ]
  }
}
```

## 画面遷移（概要）

_Source files:_ latest/frontend/reforma-frontend-spec-v1.0.0.json

```json
{
  "id": "section.navigation.flows",
  "type": "navigation",
  "title": "画面遷移（概要）",
  "flows": [
    {
      "name": "admin_login",
      "steps": [
        {
          "from": "/login",
          "to": "/dashboard"
        }
      ]
    },
    {
      "name": "form_management",
      "steps": [
        {
          "from": "/dashboard",
          "to": "/forms"
        },
        {
          "from": "/forms",
          "to": "/forms/{form_id}/edit"
        },
        {
          "from": "/forms/{form_id}/edit",
          "to": "/forms/{form_id}/items"
        },
        {
          "from": "/forms/{form_id}/items",
          "to": "/forms/{form_id}/preview"
        }
      ]
    },
    {
      "name": "response_management",
      "steps": [
        {
          "from": "/dashboard",
          "to": "/responses"
        },
        {
          "from": "/responses",
          "to": "/responses/{response_id}"
        }
      ]
    },
    {
      "name": "system_logs",
      "constraints": {
        "allow_roles": [
          "system_admin"
        ]
      },
      "steps": [
        {
          "from": "/dashboard",
          "to": "/logs"
        },
        {
          "from": "/logs",
          "to": "/logs/{log_id}"
        }
      ]
    },
    {
      "name": "public_submit",
      "steps": [
        {
          "from": "/f/{form_key}",
          "to": "/f/{form_key}/ack"
        }
      ]
    }
  ]
}
```

## reforma-frontend-spec-v1.1.0

_Source files:_ latest/frontend/reforma-frontend-spec-v1.1.0.json

```json
{
  "meta": {
    "title": "ReForma Frontend 共有テンプレ（追補反映）",
    "version": "1.1",
    "generated_at": "2026-01-13T01:08:32.431777",
    "timezone": "Asia/Tokyo"
  },
  "paste_template": {
    "sections": [
      {
        "title": "前提",
        "body": [
          "本チャットは ReForma フロントエンド（React）実装フェーズの継続。仕様の再検討はしない。",
          "正本仕様＋追補パッチに従い 条件分岐UI/表示モード/テーマ/計算フィールド を実装する。"
        ]
      },
      {
        "title": "正本仕様（必ず前提）",
        "body": [
          "02.ReForma-screen-spec-v1.1-consolidated.json",
          "condition-ui-spec-v1.0.json（条件分岐UI・保存JSON）",
          "form-feature-attachments-v1.1.json（A-06 条件分岐 正本）",
          "06.ReForma React 運用・画面ui仕様書 V0.3.json",
          "reforma-react-v0.4.12.3.zip（v0.5.0から開始）"
        ]
      },
      {
        "title": "追補（本チャットで追加：必ず反映）",
        "body": [
          "ReForma_追補パッチ_表示モード_テーマ_計算フィールド_v1.0.1.json",
          "テーマ分離: 公開フォームテーマは管理画面テーマに追従しない（フォーム theme_id/theme_tokens のみ）",
          "計算フィールド: readonly + built-in 関数（UI計算はUX、submit時はAPI再計算で確定）"
        ]
      },
      {
        "title": "実装ポイント",
        "body": [
          "公開フォーム: theme_tokens をフォームコンテナに CSS variables として適用（:root/bodyには当てない、.rf-form 名前空間で完結）",
          "表示モード: 保存の正は value。表示は label/ both / value を切替可。label_snapshot がある場合はそれを優先表示可能。",
          "計算フィールド: 依存フィールド変更で再計算、readonly表示。循環/深い依存は扱わない（v1.x制限）",
          "条件分岐: and/or 明示、評価不能は安全側。ConditionStateを適用。"
        ]
      }
    ]
  },
  "attachments_to_share": {
    "must_include": [
      {
        "file": "ReForma_追補パッチ_表示モード_テーマ_計算フィールド_v1.0.1.json",
        "path": "sandbox:/mnt/data/ReForma_追補パッチ_表示モード_テーマ_計算フィールド_v1.0.1.json",
        "purpose": "追補パッチ（テーマ分離含む）"
      },
      {
        "file": "ReForma_条件分岐_評価結果IF_v1.0.json",
        "path": "sandbox:/mnt/data/ReForma_条件分岐_評価結果IF_v1.0.json",
        "purpose": "ConditionState I/F"
      },
      {
        "file": "openapi-reforma-v1.1-full.yaml",
        "path": "sandbox:/mnt/data/openapi-reforma-v1.1-full.yaml",
        "purpose": "API参照"
      },
      {
        "file": "condition-ui-spec-v1.0.json",
        "path": "sandbox:/mnt/data/condition-ui-spec-v1.0.json",
        "purpose": "条件分岐UI仕様"
      },
      {
        "file": "form-feature-attachments-v1.1.json",
        "path": "sandbox:/mnt/data/form-feature-attachments-v1.1.json",
        "purpose": "Attachments（A-06）"
      }
    ]
  }
}
```


---

# DB 仕様 (v1.0.0)

- version: v1.0.0
- generated_at: 2026-01-14T11:37:59.882283+00:00

## Sources
- latest/db/reforma-db-spec-v1.0.0.json (v1.0.0)

---

## reforma-db-spec-v1.0.0

_Source files:_ latest/db/reforma-db-spec-v1.0.0.json

<FULL_JSON_REPLACED_IN_RUNTIME>


---

