# ReForma API仕様書 (v0.9.1 統合版)
この文書は、OpenAPI仕様を元に最新のAPI仕様をまとめたものです。以前のAPI仕様からの差分ではなく、**全文を日本語で記載**しており、最新版のみを参照すれば十分です。v1.3.3 をベースに、添付ファイル機能、通知機能、期間チェック機能を追加しています。

**注意**: このMarkdownファイルの変更は、対応するJSONファイル（reforma-api-spec-v0.9.1.json）にも反映してください。

## バージョンおよびメタ情報
- **バージョン**: v0.9.1
- **生成日時**: 2026-01-19T00:00:00Z
- **OpenAPI バージョン**: 3.0.3
- **更新内容**: 実装コードとの整合性を確保するため、不足していたエンドポイントを追加

### 変更履歴

#### v0.9.1 (2026-01-19)
- 実装コードとの整合性を確保するため、不足していたエンドポイントを追加
  - GET /v1/health - ヘルスチェック（認証不要）
  - POST /v1/forms/{form_key}/step-transition - STEP遷移評価（認証不要）
  - POST /v1/responses/{id}/notifications/resend - 通知再送（system_admin権限必須）
  - POST /v1/responses/{id}/pdf/regenerate - PDF再生成（system_adminまたはroot-only権限必須）
  - GET /v1/system/themes - テーマ一覧（system_admin権限必須）
  - POST /v1/system/themes - テーマ作成（system_admin権限必須）
  - GET /v1/system/themes/{id} - テーマ詳細（system_admin権限必須）
  - PUT /v1/system/themes/{id} - テーマ更新（system_admin権限必須、プリセットテーマはroot-only）
  - DELETE /v1/system/themes/{id} - テーマ削除（system_admin権限必須）
  - GET /v1/system/themes/{id}/usage - テーマ使用状況（system_admin権限必須）
  - POST /v1/system/themes/{id}/copy - テーマコピー（system_admin権限必須）
  - GET /v1/system/roles - ロール一覧（system_admin権限必須）

#### v0.9.0 (2026-01-19)
- 条件分岐ビルダーUI（フロントエンド実装）に関する記載を追加
  - フロントエンド側で実装された`ConditionRuleBuilder`コンポーネントの概要を追加
  - 条件分岐ルールの保存形式（JSON）について記載
  - 詳細はフロントエンド仕様書（reforma-frontend-spec-v0.9.0.md）を参照

#### v0.1.8 (2026-01-17)
- フォーム一覧API（GET /v1/forms）のレスポンスに`translations`と`response_count`フィールドを追加
  - `translations`: 多言語翻訳情報の配列（一覧取得時のみ含まれる）
  - `response_count`: 回答数（一覧取得時のみ含まれる）

#### v0.1.7 (2026-01-17)
- ファイルアップロードのジョブキュー対応
  - `POST /v1/forms/{id}/attachment/pdf-template`: 非同期処理に変更、進捗表示対応
  - `POST /v1/forms/{id}/attachment/files`: 非同期処理に変更、進捗表示対応
  - レスポンス: `data.job.job_id`を返却（進捗確認用）
- CSVインポート機能の追加
  - `POST /v1/forms/{id}/fields/import/csv`: CSVインポート開始（`type`パラメータ: `options` or `fields`）
  - 選択肢インポート（`options`）: 既存フィールドの選択肢を追加・更新
  - 項目全体インポート（`fields`）: フォーム項目全体を一括置き換え
  - 進捗表示対応（`GET /v1/progress/{job_id}`）
  - エラーレポート機能（`result_data`に詳細情報を保存）
- 進捗管理の拡張
  - `progress_jobs`テーブルに`result_data`カラム追加（JSON形式）
  - `GET /v1/progress/{job_id}`に`result_data`フィールドを追加

#### v0.1.6 (2026-01-17)
- エラーメッセージの多言語対応機能を追加
  - ロケール取得の優先順位: リクエストパラメータ`locale` > `Accept-Language`ヘッダー > デフォルト（日本語）
  - サポート言語: `ja`（日本語）、`en`（英語）
  - すべてのエラーメッセージと成功メッセージが自動翻訳される

#### v0.1.5 (2026-01-17)
- テーマ機能の追加
- 表示モード機能（locale/modeパラメータ）の追加

---

## 多言語対応（Internationalization）

ReForma APIは、エラーメッセージとレスポンスメッセージの多言語対応をサポートしています。

### ロケール取得の優先順位

APIレスポンスのメッセージは、以下の優先順位でロケールを決定します：

1. **リクエストパラメータの`locale`**（最優先）
   - クエリパラメータまたはリクエストボディに`locale`パラメータが含まれている場合、その値を使用
   - 有効な値: `"ja"`（日本語）、`"en"`（英語）

2. **`Accept-Language`ヘッダー**
   - HTTPリクエストヘッダーの`Accept-Language`から言語を取得
   - 例: `Accept-Language: en-US,en;q=0.9,ja;q=0.8`
   - サポートされる言語コード: `ja`, `en`

3. **デフォルト（日本語）**
   - 上記のいずれも指定されていない場合、デフォルトで日本語（`ja`）を使用

### サポート言語

- `ja`: 日本語（デフォルト）
- `en`: 英語

### エラーメッセージの翻訳

すべてのエラーメッセージと成功メッセージは、取得されたロケールに応じて自動的に翻訳されます。

- 翻訳キー形式: `messages.xxx`（例: `messages.form_not_found`）
- 置換パラメータ対応: `:count`, `:error`, `:fields`など
- 翻訳が見つからない場合: フォールバックとして日本語を試行し、それでも見つからない場合は翻訳キーをそのまま返す

### 使用例

#### リクエストパラメータでロケールを指定
```
GET /v1/forms/123?locale=en
```

#### Accept-Languageヘッダーでロケールを指定
```
GET /v1/forms/123
Accept-Language: en
```

#### リクエストボディでロケールを指定（POST/PUT）
```json
{
  "locale": "en",
  "answers": { ... }
}
```

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

## 条件分岐ビルダーUI（フロントエンド実装）

フロントエンド側で実装された条件分岐ビルダーUI（`ConditionRuleBuilder`コンポーネント）についての概要です。詳細な実装仕様は、フロントエンド仕様書（`reforma-frontend-spec-v0.9.0.md`）の「F-03: フォーム項目設定」セクションを参照してください。

### 概要

条件分岐ビルダーUIは、フォーム項目設定画面（F-03）で条件分岐ルールを視覚的に構築するためのUIコンポーネントです。以下の機能を提供します：

- **複数条件の追加・削除**: 最大10個の条件を追加可能
- **AND/ORの論理結合**: 論理演算子（AND/OR）を明示的に選択可能
- **field type × operator 許可表の適用**: フィールドタイプに応じて使用可能な演算子を自動フィルタリング
- **operator別 value_input UI**: 演算子に応じた適切な値入力UI（例: `between`は範囲入力、`in`はカンマ区切り入力）
- **バリデーション**: 自己参照チェック、フィールド存在チェック

### ルールタイプ

以下の3種類のルールタイプに対応しています：

1. **visibility_rule**: フィールドの表示/非表示を制御
2. **required_rule**: フィールドの必須/任意を制御
3. **step_transition_rule**: STEP遷移の可否を制御

### 保存形式（JSON）

条件分岐ビルダーUIで構築されたルールは、以下のJSON形式で保存されます：

#### 単一条件の例

```json
{
  "version": "1",
  "op": "eq",
  "field": "category",
  "value": "business"
}
```

#### 複数条件（AND結合）の例

```json
{
  "version": "1",
  "op": "and",
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
}
```

#### 複数条件（OR結合）の例

```json
{
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
}
```

### 制約

- **最大条件数**: 10個
- **最大ネスト深度**: 1段（v1.x制限）
- **自己参照禁止**: フィールドが自身を参照する条件は設定不可

### 実装ファイル

- **コンポーネント**: `src/pages/forms/FormItemPage.tsx`内の`ConditionRuleBuilder`
- **詳細仕様**: `reforma-frontend-spec-v0.9.0.md`の「F-03: フォーム項目設定」セクション

---

## エンドポイント一覧

### GET /v1/health
- **概要**: ヘルスチェック
- **説明**: APIの稼働状況とビルド情報を返却する。認証不要。
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
      - フィールド:
        - `data.status` (string) - 稼働状態（"ok"）
        - `data.app` (object) - アプリケーション情報
          - `name` (string) - アプリケーション名
          - `env` (string) - 環境（local, staging, production等）
          - `laravel_version` (string) - Laravelバージョン
        - `data.api` (object) - API情報
          - `base` (string) - APIベースパス
          - `version_path` (string) - バージョンパス（"v1"）
          - `openapi_version` (string) - OpenAPIバージョン
        - `data.build` (object) - ビルド情報
          - `version` (string) - ビルドバージョン
          - `sha` (string) - Git SHA
          - `timestamp` (string) - ビルドタイムスタンプ

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
  - `page` (クエリ, 必須, 型: integer): ページ番号（1以上）
  - `per_page` (クエリ, 必須, 型: integer): 1ページあたりの件数（1-200）
  - `sort` (クエリ, 任意, 型: string): ソート順（`created_at_desc`, `created_at_asc`, `updated_at_desc`, `updated_at_asc`）
  - `status` (クエリ, 任意, 型: string): ステータスで絞り込み（`draft`, `published`, `closed`）
  - `q` (クエリ, 任意, 型: string): キーワード検索（code、翻訳のtitle/descriptionで部分一致）
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
      - レスポンス構造:
        ```json
        {
          "success": true,
          "data": {
            "forms": {
              "items": [
                {
                  "id": 1,
                  "code": "FORM_001",
                  "status": "published",
                  "is_public": true,
                  "attachment_enabled": false,
                  "attachment_type": null,
                  "pdf_template_path": null,
                  "attachment_files": null,
                  "notification_user_enabled": false,
                  "notification_admin_enabled": false,
                  "created_by": 1,
                  "created_at": "2026-01-17T00:00:00Z",
                  "updated_at": "2026-01-17T00:00:00Z",
                  "translations": [
                    {
                      "id": 1,
                      "form_id": 1,
                      "locale": "ja",
                      "title": "フォーム名",
                      "description": "説明"
                    }
                  ],
                  "response_count": 10
                }
              ],
              "total": 1,
              "page": 1,
              "per_page": 20,
              "sort": "created_at_desc"
            }
          },
          "message": null,
          "errors": null,
          "code": "OK",
          "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        }
        ```
      - フィールド説明:
        - `data.forms.items[].translations`: 多言語翻訳情報の配列（一覧取得時のみ含まれる）
        - `data.forms.items[].response_count`: 回答数（一覧取得時のみ含まれる）
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
      - 追加フィールド:
        - `data.form.theme_id` (型: integer, 任意): テーマID
        - `data.form.theme` (型: object, 任意): テーマ情報（theme_idが指定されている場合）
        - `data.form.theme_tokens` (型: object, 任意): テーマトークン（解決済み）
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### PUT /v1/forms/{id}
- **概要**: フォーム更新
- **権限**: Form Admin以上
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): 
- **リクエストボディ**:
  - コンテンツタイプ: application/json
    - スキーマ型: object
    - 追加フィールド:
      - `theme_id` (任意, 型: integer, exists:themes,id,where:is_active,true): テーマID（is_active=trueのテーマのみ）
      - `theme_tokens` (任意, 型: object): テーマトークン（フォーム固有のカスタマイズ）
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
  - `id` (パス, 必須, 型: integer): フォームID
- **リクエストボディ**:
  - コンテンツタイプ: application/json
    - スキーマ型: object
    - フィールド: `fields` (array) - フォーム項目配列
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
      - フィールド: `data.fields` (array) - 更新されたフォーム項目配列
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 422: 422 Validation Error
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### POST /v1/forms/{id}/fields/import/csv
- **概要**: CSVインポート開始（非同期処理）
- **説明**: フォームの選択肢または項目全体をCSVファイルから一括インポートする。インポート処理は非同期で実行され、進捗は`GET /v1/progress/{job_id}`で確認できる。
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): フォームID
- **リクエストボディ**:
  - コンテンツタイプ: multipart/form-data
    - `file` (必須, 型: file): CSVファイル（最大10MB）
    - `type` (必須, 型: string): インポートタイプ（`options` or `fields`）
      - `options`: 選択肢インポート（既存フィールドの選択肢を追加・更新）
      - `fields`: 項目全体インポート（フォーム項目全体を一括置き換え）
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
      - フィールド: `data.job.job_id` (string) - 進捗確認用のジョブID
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 422: 422 Validation Error
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

**CSV形式（選択肢インポート）**:
- ヘッダー行: `field_key,value,label,label_ja,label_en`
- データ行: 選択肢のデータ（1行1選択肢）

**CSV形式（項目全体インポート）**:
- ヘッダー行: `field_key,type,sort_order,is_required,options_json,visibility_rule,required_rule,step_transition_rule,pdf_block_key,pdf_page_number,computed_rule`
- データ行: フォーム項目のデータ（1行1項目）
- JSON形式のフィールド（`options_json`, `visibility_rule`等）はJSON文字列として記述

**参照**: 
- `csv-import-spec.md`（詳細仕様）

### POST /v1/forms/{id}/attachment/pdf-template
- **概要**: PDFテンプレートアップロード（非同期処理）
- **説明**: フォームのPDFテンプレートをアップロードする。PDFテンプレートは、フォーム送信時に回答データを埋め込んでPDFを生成するために使用される。アップロード処理は非同期で実行され、進捗は`GET /v1/progress/{job_id}`で確認できる。
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): フォームID
- **リクエストボディ**:
  - コンテンツタイプ: multipart/form-data
    - `file` (必須, 型: file): PDFテンプレートファイル（最大10MB）
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
      - フィールド: `data.job.job_id` (string) - 進捗確認用のジョブID
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 422: 422 Validation Error
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### POST /v1/forms/{id}/attachment/files
- **概要**: 添付ファイルアップロード（非同期処理）
- **説明**: フォームの添付ファイルをアップロードする（複数ファイル対応、最大10ファイル、各ファイル最大10MB）。アップロードされたファイルは、フォーム送信時にメール通知に添付される。アップロード処理は非同期で実行され、進捗は`GET /v1/progress/{job_id}`で確認できる。
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): フォームID
- **リクエストボディ**:
  - コンテンツタイプ: multipart/form-data
    - `files` (必須, 型: array[file]): アップロードするファイル（複数可、最大10ファイル、各ファイル最大10MB）
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
      - フィールド: `data.job.job_id` (string) - 進捗確認用のジョブID
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 422: 422 Validation Error
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### DELETE /v1/forms/{id}/attachment/files/{file_index}
- **概要**: 添付ファイル削除
- **説明**: フォームの添付ファイルを削除する。
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): フォームID
  - `file_index` (パス, 必須, 型: integer): 削除するファイルのインデックス（0始まり）
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
      - フィールド: `data.deleted` (boolean) - 削除成功フラグ
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 404: 404 Not Found
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
    - 追加フィールド:
      - `locale` (任意, 型: string, enum: ["ja", "en"]): ロケール（デフォルト: "ja"）
      - `mode` (任意, 型: string, enum: ["both", "value", "label"]): 表示モード（保存の正はvalue固定、modeはACK/出力の表示方針用）
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
      - 追加フィールド: `data.condition_state` (#/components/schemas/ConditionState)
  - 422: 422 Validation Error
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
      - 追加フィールド: `errors.step` (#/components/schemas/StepTransitionState) - STEP_TRANSITION_DENIED 時

### GET /v1/public/forms/{form_key}
- **概要**: 公開フォーム表示取得
- **説明**: 一般ユーザー向けの公開フォーム取得。公開期間のチェックが行われ、期間外の場合はエラーを返す。
- **パラメータ**:
  - `form_key` (パス, 必須, 型: string): フォーム識別子
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
      - 追加フィールド: 
        - `data.condition_state` (#/components/schemas/ConditionState)
        - `data.form.theme_id` (型: integer, 任意): テーマID
        - `data.form.theme_code` (型: string, 任意): テーマコード
        - `data.form.theme_tokens` (型: object, 任意): テーマトークン（CSS変数の値）
  - 404: 404 Not Found
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### POST /v1/forms/{form_key}/step-transition
- **概要**: STEP遷移評価
- **説明**: 現在のSTEPから次のSTEPへの遷移が可能かどうかを評価する。認証不要。
- **パラメータ**:
  - `form_key` (パス, 必須, 型: string): フォーム識別子
- **リクエストボディ**:
  - コンテンツタイプ: application/json
    - スキーマ型: object
    - 必須フィールド:
      - `current_step_key` (string) - 現在のSTEPキー
      - `answers` (object) - 回答値
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
      - フィールド:
        - `data.condition_state` (#/components/schemas/ConditionState) - 条件分岐評価結果
  - 403: 403 Forbidden（公開期間外）
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 422: 422 Validation Error（STEP遷移拒否またはバリデーションエラー）
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
      - エラーコード: `STEP_TRANSITION_DENIED`（STEP遷移が拒否された場合）
  - 404: Not Found
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

### POST /v1/responses/{id}/notifications/resend
- **概要**: 通知再送
- **説明**: 指定された送信データの通知を再送する。system_admin権限が必要。
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): 送信ID
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
      - フィールド:
        - `data.submission_id` (integer) - 送信ID
        - `data.form_id` (integer) - フォームID
        - `data.form_code` (string) - フォームコード
  - 400: 400 Bad Request（通知が有効でない）
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden（system_admin権限が必要）
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 404: Not Found
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 500: Server Error
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError

### POST /v1/responses/{id}/pdf/regenerate
- **概要**: PDF再生成
- **説明**: 指定された送信データのPDFを再生成する。system_adminまたはroot-only権限が必要。デフォルトでは再生成禁止（409エラー）。
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): 送信ID
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
      - フィールド:
        - `data.submission_id` (integer) - 送信ID
        - `data.form_id` (integer) - フォームID
        - `data.form_code` (string) - フォームコード
  - 400: 400 Bad Request（PDF生成が利用できない）
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 401: 401 Unauthorized
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 403: 403 Forbidden
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 404: Not Found
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 409: 409 Conflict（再生成が許可されていない）
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
  - 500: Server Error
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

### GET /v1/system/themes
- **概要**: テーマ一覧取得
- **権限**: System Admin以上
- **パラメータ**:
  - `page` (クエリ, 必須, 型: integer): ページ番号
  - `per_page` (クエリ, 必須, 型: integer): 1ページあたりの件数（1-200）
  - `sort` (クエリ, 任意, 型: string, enum: ["created_at_desc", "created_at_asc", "name_asc", "name_desc"]): ソート順
  - `is_preset` (クエリ, 任意, 型: boolean): プリセットテーマのみ取得
  - `is_active` (クエリ, 任意, 型: boolean): 有効なテーマのみ取得（デフォルト: true）
  - `q` (クエリ, 任意, 型: string): キーワード検索（code, name）
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
      - フィールド:
        - `data.themes` (型: array): テーマ一覧
        - `data.pagination` (型: object): ページネーション情報
  - 401: 401 Unauthorized
  - 403: 403 Forbidden

### POST /v1/system/themes
- **概要**: テーマ作成
- **権限**: System Admin以上
- **リクエストボディ**:
  - コンテンツタイプ: application/json
    - スキーマ型: object
    - 必須フィールド:
      - `code` (型: string, max:255, unique:themes,code): テーマコード
      - `name` (型: string, max:255): テーマ名
      - `theme_tokens` (型: object): テーマトークン（スキーマ準拠）
    - 任意フィールド:
      - `description` (型: string): テーマの説明
      - `is_active` (型: boolean, デフォルト: true): 有効かどうか
- **レスポンス**:
  - 201: Created
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
  - 403: 403 Forbidden
  - 422: 422 Validation Error

### GET /v1/system/themes/{id}
- **概要**: テーマ詳細取得
- **権限**: System Admin以上
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): テーマID
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
  - 403: 403 Forbidden
  - 404: 404 Not Found

### PUT /v1/system/themes/{id}
- **概要**: テーマ更新
- **権限**: 
  - 通常テーマ: System Admin以上
  - プリセットテーマ: root-only（is_root=true必須）
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): テーマID
- **リクエストボディ**:
  - コンテンツタイプ: application/json
    - スキーマ型: object
    - 任意フィールド:
      - `name` (型: string, max:255): テーマ名
      - `description` (型: string): テーマの説明
      - `theme_tokens` (型: object): テーマトークン（スキーマ準拠）
      - `is_active` (型: boolean): 有効かどうか
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
  - 403: 403 Forbidden（プリセットテーマ更新時はroot-only）
  - 404: 404 Not Found
  - 422: 422 Validation Error

### DELETE /v1/system/themes/{id}
- **概要**: テーマ削除（論理削除）
- **権限**: System Admin以上
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): テーマID
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
  - 403: 403 Forbidden（プリセットテーマは削除不可）
  - 404: 404 Not Found
  - 409: 409 Conflict（使用中のテーマは削除不可）

### GET /v1/system/themes/{id}/usage
- **概要**: テーマ使用状況確認
- **権限**: System Admin以上
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): テーマID
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
      - フィールド:
        - `data.theme` (型: object): テーマ情報
        - `data.usage.form_count` (型: integer): 使用中のフォーム数
        - `data.usage.forms` (型: array): 使用中のフォーム一覧
  - 401: 401 Unauthorized
  - 403: 403 Forbidden
  - 404: 404 Not Found

### POST /v1/system/themes/{id}/copy
- **概要**: テーマコピー
- **権限**: System Admin以上
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): コピー元テーマID
- **リクエストボディ**:
  - コンテンツタイプ: application/json
    - スキーマ型: object
    - 必須フィールド:
      - `code` (型: string, max:255, unique:themes,code): 新しいテーマコード
      - `name` (型: string, max:255): 新しいテーマ名
    - 任意フィールド:
      - `description` (型: string): テーマの説明
- **レスポンス**:
  - 201: Created
    - コンテンツタイプ: application/json
      - スキーマ型: object
  - 401: 401 Unauthorized
  - 403: 403 Forbidden
  - 404: 404 Not Found
  - 422: 422 Validation Error

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

### GET /v1/system/themes
- **概要**: テーマ一覧取得
- **説明**: テーマ一覧を取得する。system_admin権限が必要。
- **パラメータ**:
  - `page` (クエリ, 必須, 型: integer): ページ番号（1以上）
  - `per_page` (クエリ, 必須, 型: integer): 1ページあたりの件数（1-200）
  - `sort` (クエリ, 任意, 型: string, enum: ["created_at_desc", "created_at_asc", "name_asc", "name_desc"]): ソート順
  - `is_preset` (クエリ, 任意, 型: boolean): プリセットテーマのみ取得
  - `is_active` (クエリ, 任意, 型: boolean): 有効なテーマのみ取得（デフォルト: true）
  - `q` (クエリ, 任意, 型: string): キーワード検索（code, name）
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
      - フィールド:
        - `data.themes` (array) - テーマ一覧
        - `data.pagination` (object) - ページネーション情報
  - 401: 401 Unauthorized
  - 403: 403 Forbidden

### POST /v1/system/themes
- **概要**: テーマ作成
- **説明**: テーマを作成する。system_admin権限が必要。
- **リクエストボディ**:
  - コンテンツタイプ: application/json
    - スキーマ型: object
    - 必須フィールド:
      - `code` (string, max:255, unique:themes,code) - テーマコード
      - `name` (string, max:255) - テーマ名
      - `theme_tokens` (object) - テーマトークン（スキーマ準拠）
    - 任意フィールド:
      - `description` (string) - テーマの説明
      - `is_active` (boolean, デフォルト: true) - 有効かどうか
- **レスポンス**:
  - 201: Created
  - 401: 401 Unauthorized
  - 403: 403 Forbidden
  - 422: 422 Validation Error

### GET /v1/system/themes/{id}
- **概要**: テーマ詳細取得
- **説明**: テーマ詳細を取得する。system_admin権限が必要。
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): テーマID
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
      - フィールド:
        - `data.theme` (object) - テーマ情報
  - 401: 401 Unauthorized
  - 403: 403 Forbidden
  - 404: Not Found

### PUT /v1/system/themes/{id}
- **概要**: テーマ更新
- **説明**: テーマを更新する。system_admin権限が必要。プリセットテーマの更新はroot-only権限が必要。
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): テーマID
- **リクエストボディ**:
  - コンテンツタイプ: application/json
    - スキーマ型: object
    - 任意フィールド:
      - `name` (string, max:255) - テーマ名
      - `description` (string) - テーマの説明
      - `theme_tokens` (object) - テーマトークン
      - `is_active` (boolean) - 有効かどうか
- **レスポンス**:
  - 200: OK
  - 401: 401 Unauthorized
  - 403: 403 Forbidden（プリセットテーマ更新にはroot-only権限が必要）
  - 404: Not Found
  - 422: 422 Validation Error

### DELETE /v1/system/themes/{id}
- **概要**: テーマ削除
- **説明**: テーマを削除する（論理削除）。system_admin権限が必要。プリセットテーマは削除不可。使用中のテーマは削除不可。
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): テーマID
- **レスポンス**:
  - 200: OK
  - 401: 401 Unauthorized
  - 403: 403 Forbidden（プリセットテーマは削除不可）
  - 404: Not Found
  - 409: 409 Conflict（使用中のテーマは削除不可）

### GET /v1/system/themes/{id}/usage
- **概要**: テーマ使用状況確認
- **説明**: テーマの使用状況を確認する。system_admin権限が必要。
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): テーマID
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
      - フィールド:
        - `data.theme` (object) - テーマ情報
        - `data.usage` (object) - 使用状況
          - `form_count` (integer) - 使用中のフォーム数
          - `forms` (array) - 使用中のフォーム一覧
  - 401: 401 Unauthorized
  - 403: 403 Forbidden
  - 404: Not Found

### POST /v1/system/themes/{id}/copy
- **概要**: テーマコピー
- **説明**: テーマをコピーして新規テーマを作成する。system_admin権限が必要。
- **パラメータ**:
  - `id` (パス, 必須, 型: integer): テーマID
- **リクエストボディ**:
  - コンテンツタイプ: application/json
    - スキーマ型: object
    - 必須フィールド:
      - `code` (string, max:255, unique:themes,code) - 新しいテーマコード
      - `name` (string, max:255) - 新しいテーマ名
    - 任意フィールド:
      - `description` (string) - 新しいテーマの説明
- **レスポンス**:
  - 201: Created
    - コンテンツタイプ: application/json
      - スキーマ型: object
      - フィールド:
        - `data.theme` (object) - 作成されたテーマ情報
  - 401: 401 Unauthorized
  - 403: 403 Forbidden
  - 404: Not Found
  - 422: 422 Validation Error

### GET /v1/system/roles
- **概要**: ロール一覧取得
- **説明**: 管理者ユーザー用のロール一覧を取得する。検索条件や編集画面の選択肢として使用する。system_admin権限が必要。
- **注意**: 多言語対応はフロントエンド側で行う。APIは`name`カラム（日本語）のみを返却する。
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
      - フィールド:
        - `data.roles` (array) - ロール一覧
          - `code` (string) - ロールコード（SYSTEM_ADMIN, FORM_ADMIN, LOG_ADMIN）
          - `name` (string) - ロール名（rolesテーブルのnameカラムの値、日本語）
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
- **概要**: 進捗状況取得
- **説明**: バックグラウンドジョブの進捗状況を取得する。ファイルアップロード、CSVインポート、CSVエクスポート等の非同期処理の進捗を確認できる。
- **パラメータ**:
  - `job_id` (パス, 必須, 型: string): ジョブID（UUID形式）
- **レスポンス**:
  - 200: OK
    - コンテンツタイプ: application/json
      - スキーマ型: object
      - フィールド:
        - `data.job.job_id` (string) - ジョブID
        - `data.job.type` (string) - ジョブタイプ（`file_upload`, `options_csv_import`, `fields_csv_import`, `csv_export`等）
        - `data.job.status` (string) - ステータス（`queued`, `running`, `succeeded`, `failed`）
        - `data.job.percent` (integer) - 進捗率（0-100）
        - `data.job.message` (string) - 進捗メッセージ（翻訳キー形式）
        - `data.job.download_url` (string, nullable) - ダウンロードURL（CSVエクスポートの場合）
        - `data.job.result_data` (object, nullable) - 結果データ（CSVインポートの場合、`imported`, `failed`, `errors`を含む）
        - `data.job.expires_at` (string, nullable) - ジョブの有効期限（ISO 8601形式）
        - `data.job.download_expires_at` (string, nullable) - ダウンロードURLの有効期限（ISO 8601形式）
  - 404: Not Found
    - コンテンツタイプ: application/json
      - スキーマ型: #/components/schemas/EnvelopeError
      - 説明: ジョブが見つからない、または有効期限が切れている場合
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
