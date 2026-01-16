# ReForma API仕様書 (v1.3.2 統合版)
この文書は、OpenAPI仕様 (v1.3.0) を元に最新のAPI仕様をまとめたものです。以前のAPI仕様からの差分ではなく、**全文を日本語で記載**しており、最新版のみを参照すれば十分です。また、旧バージョン v1.3.0 に存在していたが v1.3.1 では記載されていなかったエンドポイントやパラメータを統合しています。

## バージョンおよびメタ情報
- **バージョン**: v1.3.2
- **生成日時**: 2026-01-15T02:36:47.355902Z
- **OpenAPI バージョン**: 3.0.3

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
- **パラメータ**:
  - `form_key` (パス, 必須, 型: string): 
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
- **説明**: Respondent 用フォーム表示（/f/{form_key}）。条件分岐がある場合は condition_state を返す。
- **パラメータ**:
  - `form_key` (パス, 必須, 型: string): 
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopePublicFormView
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

