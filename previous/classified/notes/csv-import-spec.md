# CSVインポート機能仕様

## 概要

フォームの項目管理を効率化するため、CSVインポート機能を提供します。
2種類のインポートタイプをサポートします：

1. **選択肢インポート**（`options`）
   - 既存のフィールドに対して選択肢（options_json）を追加・更新
   - 選択肢タイプのフィールド（select, radio, checkbox）のみ対応

2. **項目全体インポート**（`fields`）
   - フォームの項目全体をインポート
   - フィールドの定義を含む（field_key, type, sort_order, is_required, options_json等）
   - フォームの項目で指定可能なものは全て網羅

## 1. 選択肢インポート（`options`）

### CSV形式

**ヘッダー行**:
```
field_key,value,label,label_ja,label_en
```

**データ行例**:
```
select_field,option1,Option 1,オプション1,Option 1
select_field,option2,Option 2,オプション2,Option 2
radio_field,value1,Value 1,値1,Value 1
```

### カラム説明

| カラム名 | 必須 | 説明 |
|---------|------|------|
| `field_key` | ✓ | フィールドキー（既存のフィールド） |
| `value` | ✓ | 選択肢の値 |
| `label` | - | 選択肢のラベル（デフォルト） |
| `label_ja` | - | 選択肢のラベル（日本語） |
| `label_en` | - | 選択肢のラベル（英語） |

### 動作

- 既存のフィールドに対して選択肢を追加・更新
- `value`で重複チェック（既存の場合は更新、新規の場合は追加）
- 選択肢タイプのフィールド（select, radio, checkbox）のみ対応

### エンドポイント

```
POST /v1/forms/{id}/fields/import/csv
Content-Type: multipart/form-data

Parameters:
- file: CSVファイル（必須）
- type: "options"（必須）
```

## 2. 項目全体インポート（`fields`）

### CSV形式

**ヘッダー行**:
```
field_key,type,sort_order,is_required,options_json,visibility_rule,required_rule,step_transition_rule,pdf_block_key,pdf_page_number,computed_rule
```

**データ行例**:
```
name,text,1,true,,"","","",,,
email,email,2,true,,"","","",,,
age,number,3,false,,"","","",,,
gender,select,4,true,"{""options"":[{""value"":""male"",""label"":""Male"",""labels"":{""ja"":""男性"",""en"":""Male""}}]}","","","",,,
```

### カラム説明

| カラム名 | 必須 | 説明 |
|---------|------|------|
| `field_key` | ✓ | フィールドキー（一意） |
| `type` | ✓ | フィールドタイプ（text, email, number, select, radio, checkbox等） |
| `sort_order` | - | 並び順（整数、デフォルト: 0） |
| `is_required` | - | 必須フラグ（true/false、デフォルト: false） |
| `options_json` | - | 選択肢定義（JSON文字列、選択肢タイプの場合） |
| `visibility_rule` | - | 表示ルール（JSON文字列） |
| `required_rule` | - | 必須ルール（JSON文字列） |
| `step_transition_rule` | - | ステップ遷移ルール（JSON文字列） |
| `pdf_block_key` | - | PDFブロックキー |
| `pdf_page_number` | - | PDFページ番号（整数） |
| `computed_rule` | - | 計算ルール（JSON文字列） |

### JSON形式のフィールド

以下のフィールドはJSON文字列として扱います：
- `options_json`: 選択肢定義
  ```json
  {
    "options": [
      {
        "value": "option1",
        "label": "Option 1",
        "labels": {
          "ja": "オプション1",
          "en": "Option 1"
        }
      }
    ]
  }
  ```
- `visibility_rule`: 表示ルール
- `required_rule`: 必須ルール
- `step_transition_rule`: ステップ遷移ルール
- `computed_rule`: 計算ルール

### 動作

- フォームの項目全体を一括置き換え（差分更新ではない）
- 既存のフィールドを削除し、CSVの内容で新規作成
- ルールバリデーションを実行（条件分岐ルールの整合性チェック）
- トランザクション処理（エラー時はロールバック）

### エンドポイント

```
POST /v1/forms/{id}/fields/import/csv
Content-Type: multipart/form-data

Parameters:
- file: CSVファイル（必須）
- type: "fields"（必須）
```

## 3. 共通仕様

### 進捗管理

両方のインポートタイプで進捗管理をサポート：

- **選択肢インポート**:
  - 0%: キューに追加
  - 10%: CSVファイル読み込み完了
  - 20%: データ解析完了
  - 40%: データ検証完了
  - 100%: インポート完了

- **項目全体インポート**:
  - 0%: キューに追加
  - 10%: CSVファイル読み込み完了
  - 20%: データ解析完了
  - 40%: データ検証完了
  - 60%: ルールバリデーション完了
  - 80%: データインポート中
  - 100%: インポート完了

### エラーハンドリング

- CSV解析エラー: 行番号とエラー内容を返却
- データ検証エラー: 検証失敗した行の情報を返却
- ルールバリデーションエラー: 条件分岐ルールの整合性エラーを返却
- インポートエラー: 失敗したフィールドの情報を返却

### レスポンス

**進捗確認**:
```
GET /v1/progress/{job_id}

Response:
{
  "success": true,
  "data": {
    "job": {
      "job_id": "...",
      "type": "options_csv_import" | "fields_csv_import",
      "status": "queued" | "running" | "succeeded" | "failed",
      "percent": 0-100,
      "message": "messages.csv_import_...",
      "result_data": {
        "imported": 10,
        "failed": 0,
        "errors": []
      }
    }
  }
}
```

## 4. 実装方針

### 4.1 CsvImportServiceの拡張

- `importOptions()`: 選択肢インポート（既存）
- `importFields()`: 項目全体インポート（新規）
- `validateFields()`: 項目全体の検証（新規）

### 4.2 ImportCsvJobの拡張

- インポートタイプ（`options` or `fields`）をパラメータに追加
- タイプに応じて適切なメソッドを呼び出し

### 4.3 エンドポイントの拡張

- `POST /v1/forms/{id}/fields/import/csv`に`type`パラメータを追加
- `type`が`options`の場合は選択肢インポート、`fields`の場合は項目全体インポート

## 5. 使用例

### 選択肢インポート

```bash
curl -X POST "https://api.example.com/v1/forms/1/fields/import/csv" \
  -H "Authorization: Bearer {token}" \
  -F "file=@options.csv" \
  -F "type=options"
```

### 項目全体インポート

```bash
curl -X POST "https://api.example.com/v1/forms/1/fields/import/csv" \
  -H "Authorization: Bearer {token}" \
  -F "file=@fields.csv" \
  -F "type=fields"
```
