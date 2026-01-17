# ReForma API仕様書 (v0.1.4 統合版)
この文書は、OpenAPI仕様を元に最新のAPI仕様をまとめたものです。以前のAPI仕様からの差分ではなく、**全文を日本語で記載**しており、最新版のみを参照すれば十分です。v1.3.3 をベースに、添付ファイル機能、通知機能、期間チェック機能を追加しています。

**注意**: このMarkdownファイルの変更は、対応するJSONファイル（reforma-api-spec-v0.1.4.json）にも反映してください。

## バージョンおよびメタ情報
- **バージョン**: v0.1.7
- **生成日時**: 2026-01-17T00:00:00Z
- **OpenAPI バージョン**: 3.0.3
- **更新内容**: ファイルアップロード・CSVインポートのジョブキュー対応、進捗表示機能の追加

### 変更履歴

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
