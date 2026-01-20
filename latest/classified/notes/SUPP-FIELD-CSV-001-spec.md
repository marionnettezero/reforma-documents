# SUPP-FIELD-CSV-001: フォーム項目選択肢・項目全体 CSVインポート/エクスポート機能 実装仕様

**作成日**: 2026-01-22  
**最終更新日**: 2026-01-22  
**バージョン**: v1.0.0  
**実装完了日**: 2026-01-22

---

## 概要

フォーム項目の選択肢（select/radio/checkbox）をCSV形式でインポート/エクスポートする機能を実装する。また、項目全体のCSVインポート/エクスポート機能も提供する。すべて非同期処理（ジョブキュー）で実装し、進捗状況をリアルタイムで表示する。

### 機能概要

1. **特定フィールドの選択肢CSVインポート**
   - 項目詳細設定画面から、選択肢タイプのフィールドのみCSVインポート可能
   - 新規項目（未保存）の場合は、フロントエンドでCSVを解析し、保存時に選択肢を含めて保存

2. **特定フィールドの選択肢CSVエクスポート**
   - 項目詳細設定画面から、選択肢タイプのフィールドのみCSVエクスポート可能
   - エクスポートしたCSVは、インポートテンプレートとしても使用可能

3. **項目全体のCSVインポート**（既存機能の拡張）
   - 項目設定画面から、フォーム全体の項目をCSVで一括インポート

4. **項目全体のCSVエクスポート**（新規）
   - 項目設定画面から、フォーム全体の項目をCSVで一括エクスポート
   - エクスポートしたCSVは、インポートテンプレートとしても使用可能

---

## バックエンド実装状況

### 現在の実装状況

**既存実装**:
- ✅ `POST /v1/forms/{id}/fields/import/csv` - 選択肢/項目全体のCSVインポート（既存）
- ✅ `CsvImportService` - CSV解析・検証・インポート処理
- ✅ `ImportCsvJob` - CSVインポート非同期ジョブ
- ✅ `ProgressJob` - 進捗管理モデル
- ✅ `GET /v1/progress/{job_id}` - 進捗取得API

**実装済み**:
- ✅ `POST /v1/forms/{form_id}/fields/{field_key}/options/import/csv` - 特定フィールドの選択肢CSVインポート
- ✅ `POST /v1/forms/{form_id}/fields/{field_key}/options/export/csv` - 特定フィールドの選択肢CSVエクスポート
- ✅ `POST /v1/forms/{id}/fields/export/csv` - 項目全体のCSVエクスポート
- ✅ `CsvImportService::importSingleFieldOptions()` - 単一フィールドの選択肢インポート
- ✅ `CsvImportService::exportSingleFieldOptions()` - 単一フィールドの選択肢エクスポート
- ✅ `CsvImportService::exportFields()` - 項目全体のエクスポート
- ✅ `CsvImportService::validateSingleFieldOptions()` - 単一フィールドの選択肢CSV検証
- ✅ `ImportFieldOptionsJob` - 選択肢インポート非同期ジョブ（新規作成）
- ✅ `ExportFieldOptionsJob` - 選択肢エクスポート非同期ジョブ（新規作成）
- ✅ `ExportFieldsJob` - 項目全体エクスポート非同期ジョブ（新規作成）
- ✅ `FormsFieldsController::importFieldOptions()` - 特定フィールドの選択肢CSVインポート開始
- ✅ `FormsFieldsController::exportFieldOptions()` - 特定フィールドの選択肢CSVエクスポート開始
- ✅ `FormsFieldsController::exportFields()` - 項目全体のCSVエクスポート開始
- ✅ ルーティング追加（`routes/api.php`）
- ✅ 翻訳キー追加（`lang/ja/messages.php`, `lang/en/messages.php`）

---

## データモデル

### options_jsonの構造

**選択肢タイプ（select/radio/checkbox）のフィールド**:

```json
{
  "label": "選択肢のラベル（デフォルト）",
  "labels": {
    "ja": "日本語ラベル",
    "en": "English Label"
  },
  "options": [
    {
      "value": "option1",
      "label": "選択肢1（デフォルト）",
      "labels": {
        "ja": "選択肢1（日本語）",
        "en": "Option 1 (English)"
      }
    },
    {
      "value": "option2",
      "label": "選択肢2（デフォルト）",
      "labels": {
        "ja": "選択肢2（日本語）",
        "en": "Option 2 (English)"
      }
    }
  ]
}
```

---

## CSV形式

### 1. 特定フィールドの選択肢CSV（インポート/エクスポート）

**ヘッダー行**:
```
value,label,label_ja,label_en
```

**データ行の例**:
```csv
value,label,label_ja,label_en
option1,Option 1,選択肢1,Option 1
option2,Option 2,選択肢2,Option 2
option3,Option 3,選択肢3,Option 3
```

**注意事項**:
- `value`: 必須。選択肢の値（重複不可）
- `label`: 必須。デフォルトラベル（多言語未設定時のフォールバック）
- `label_ja`: オプション。日本語ラベル
- `label_en`: オプション。英語ラベル
- 項目値がない場合は、このCSV形式がインポートテンプレートとして使用可能

### 2. 項目全体のCSV（インポート/エクスポート）

**ヘッダー行**:
```
field_key,type,sort_order,is_required,options_json,visibility_rule,required_rule,step_transition_rule,computed_rule,pdf_block_key,pdf_page_number
```

**データ行の例**:
```csv
field_key,type,sort_order,is_required,options_json,visibility_rule,required_rule,step_transition_rule,computed_rule,pdf_block_key,pdf_page_number
email_field,email,1,true,"","","","","","",""
select_field,select,2,false,"{\"label\":\"選択してください\",\"options\":[{\"value\":\"opt1\",\"label\":\"選択肢1\"}]}","","","","","",""
```

**注意事項**:
- `field_key`: 必須。フィールドキー（重複不可）
- `type`: 必須。フィールドタイプ（text, email, select, radio, checkbox等）
- `sort_order`: オプション。並び順（数値、デフォルト: 0）
- `is_required`: オプション。必須フラグ（true/false、デフォルト: false）
- `options_json`: オプション。選択肢データ（JSON文字列）
- `visibility_rule`: オプション。表示条件ルール（JSON文字列）
- `required_rule`: オプション。必須条件ルール（JSON文字列）
- `step_transition_rule`: オプション。STEP遷移条件ルール（JSON文字列）
- `computed_rule`: オプション。計算ルール（JSON文字列）
- `pdf_block_key`: オプション。PDFブロックキー
- `pdf_page_number`: オプション。PDFページ番号（数値）

---

## API仕様

### 1. 特定フィールドの選択肢CSVインポート

**エンドポイント**: `POST /v1/forms/{form_id}/fields/{field_key}/options/import/csv`

**認証**: 必須（管理者権限）

**パラメータ**:
- `form_id` (path): フォームID
- `field_key` (path): フィールドキー

**リクエストボディ**:
- `file` (multipart/form-data): CSVファイル（必須）
  - ファイル形式: `.csv`, `.txt`
  - 最大サイズ: 10MB

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "job_id": "uuid-string"
  },
  "message": null,
  "errors": null
}
```

**エラーレスポンス**:
- `404`: フォームまたはフィールドが見つからない
- `422`: バリデーションエラー（ファイル形式、サイズ等）
- `403`: 権限不足

**処理フロー**:
1. リクエスト受信
2. フォーム・フィールドの存在確認
3. フィールドタイプが選択肢タイプ（select/radio/checkbox）か確認
4. CSVファイルを一時保存
5. 進捗ジョブを作成（`field_options_csv_import`）
6. `ImportFieldOptionsJob`をキューに投入
7. `job_id`を返却

### 2. 特定フィールドの選択肢CSVエクスポート

**エンドポイント**: `POST /v1/forms/{form_id}/fields/{field_key}/options/export/csv`

**認証**: 必須（管理者権限）

**パラメータ**:
- `form_id` (path): フォームID
- `field_key` (path): フィールドキー

**リクエストボディ**: なし

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "job_id": "uuid-string"
  },
  "message": null,
  "errors": null
}
```

**エラーレスポンス**:
- `404`: フォームまたはフィールドが見つからない
- `403`: 権限不足

**処理フロー**:
1. リクエスト受信
2. フォーム・フィールドの存在確認
3. フィールドタイプが選択肢タイプ（select/radio/checkbox）か確認
4. 進捗ジョブを作成（`field_options_csv_export`）
5. `ExportFieldOptionsJob`をキューに投入
6. `job_id`を返却

### 3. 項目全体のCSVインポート（既存）

**エンドポイント**: `POST /v1/forms/{id}/fields/import/csv`

**認証**: 必須（管理者権限）

**パラメータ**:
- `id` (path): フォームID

**リクエストボディ**:
- `file` (multipart/form-data): CSVファイル（必須）
- `type` (form-data): インポートタイプ（`options` または `fields`）（必須）

**レスポンス**: 既存実装を参照

### 4. 項目全体のCSVエクスポート（新規）

**エンドポイント**: `POST /v1/forms/{id}/fields/export/csv`

**認証**: 必須（管理者権限）

**パラメータ**:
- `id` (path): フォームID

**リクエストボディ**: なし

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "job_id": "uuid-string"
  },
  "message": null,
  "errors": null
}
```

**エラーレスポンス**:
- `404`: フォームが見つからない
- `403`: 権限不足

**処理フロー**:
1. リクエスト受信
2. フォームの存在確認
3. 進捗ジョブを作成（`fields_csv_export`）
4. `ExportFieldsJob`をキューに投入
5. `job_id`を返却

### 5. 進捗取得（既存）

**エンドポイント**: `GET /v1/progress/{job_id}`

**認証**: 必須（管理者権限）

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "job_id": "uuid-string",
    "type": "field_options_csv_import",
    "status": "running",
    "percent": 50,
    "message": "messages.csv_import_importing",
    "result_data": null,
    "result_path": null,
    "download_url": null,
    "download_expires_at": null,
    "expires_at": "2026-01-23T00:00:00Z"
  },
  "message": null,
  "errors": null
}
```

**ステータス**:
- `queued`: キュー待ち
- `running`: 実行中
- `succeeded`: 成功
- `failed`: 失敗

**ジョブタイプ**:
- `field_options_csv_import`: 特定フィールドの選択肢CSVインポート
- `field_options_csv_export`: 特定フィールドの選択肢CSVエクスポート
- `options_csv_import`: 選択肢CSVインポート（既存）
- `fields_csv_import`: 項目全体CSVインポート（既存）
- `fields_csv_export`: 項目全体CSVエクスポート（新規）

---

## バックエンド実装詳細

### 1. CsvImportServiceの拡張

#### importSingleFieldOptions()

```php
/**
 * 単一フィールドの選択肢をインポートする
 * 
 * @param array $validatedData 検証済みデータ
 * @param int $formId フォームID
 * @param string $fieldKey フィールドキー
 * @return array インポート結果（imported, failed, errors）
 */
public function importSingleFieldOptions(array $validatedData, int $formId, string $fieldKey): array
```

**処理内容**:
1. フォーム・フィールドの存在確認
2. フィールドタイプが選択肢タイプか確認
3. 既存の選択肢を取得
4. CSVデータを既存選択肢とマージ（valueで重複チェック）
5. フィールドを更新

#### exportSingleFieldOptions()

```php
/**
 * 単一フィールドの選択肢をCSV形式でエクスポートする
 * 
 * @param int $formId フォームID
 * @param string $fieldKey フィールドキー
 * @return string CSV文字列（UTF-8 BOM付き）
 */
public function exportSingleFieldOptions(int $formId, string $fieldKey): string
```

**処理内容**:
1. フォーム・フィールドの存在確認
2. フィールドタイプが選択肢タイプか確認
3. `options_json.options`から選択肢データを取得
4. CSV形式で生成（value, label, label_ja, label_en）
5. UTF-8 BOM付きで返却

#### exportFields()

```php
/**
 * フォーム項目全体をCSV形式でエクスポートする
 * 
 * @param int $formId フォームID
 * @return string CSV文字列（UTF-8 BOM付き）
 */
public function exportFields(int $formId): string
```

**処理内容**:
1. フォームの存在確認
2. フォームに紐づく全フィールドを取得（sort_order順）
3. 各フィールドのデータをCSV形式で生成
4. JSONフィールドはJSON文字列としてエスケープ
5. UTF-8 BOM付きで返却

### 2. ジョブクラスの実装

#### ImportFieldOptionsJob

**ファイル**: `app/Jobs/ImportFieldOptionsJob.php`

**責務**:
- 特定フィールドの選択肢CSVインポート処理（非同期）
- 進捗管理（0% → 20% → 40% → 80% → 100%）
- `imports`キューで処理

**処理フロー**:
1. 進捗更新: 準備中（0%）
2. CSVファイル読み込み（10%）
3. CSV解析（20%）
4. データ検証（40%）
5. データインポート（80%）
6. 完了（100%）

#### ExportFieldOptionsJob

**ファイル**: `app/Jobs/ExportFieldOptionsJob.php`

**責務**:
- 特定フィールドの選択肢CSVエクスポート処理（非同期）
- 進捗管理（0% → 50% → 100%）
- `exports`キューで処理

**処理フロー**:
1. 進捗更新: 準備中（0%）
2. データ取得・CSV生成（50%）
3. ファイル保存（80%）
4. 完了（100%）

#### ExportFieldsJob

**ファイル**: `app/Jobs/ExportFieldsJob.php`

**責務**:
- 項目全体のCSVエクスポート処理（非同期）
- 進捗管理（0% → 50% → 100%）
- `exports`キューで処理

**処理フロー**:
1. 進捗更新: 準備中（0%）
2. データ取得・CSV生成（50%）
3. ファイル保存（80%）
4. 完了（100%）

### 3. コントローラーの実装

#### FormsFieldsControllerの拡張

**追加メソッド**:

1. `importFieldOptions(Request $request, int $formId, string $fieldKey): JsonResponse`
   - 特定フィールドの選択肢CSVインポート開始

2. `exportFieldOptions(Request $request, int $formId, string $fieldKey): JsonResponse`
   - 特定フィールドの選択肢CSVエクスポート開始

3. `exportFields(Request $request, int $id): JsonResponse`
   - 項目全体のCSVエクスポート開始

---

## フロントエンド実装状況

### 現在の実装状況

**実装済み**:
- ✅ `src/utils/csvParser.ts` - CSV解析ユーティリティ（新規作成）
- ✅ `FieldDetailPanel` - CSVインポート/エクスポート機能追加
- ✅ `FormItemPage` - CSVエクスポート機能追加
- ✅ 翻訳キー追加（`src/ui/PreferencesContext.tsx`）

**実装詳細**:
- ✅ 選択肢タブにCSVインポート/エクスポートボタンを追加
- ✅ 新規項目の場合はフロントエンドでCSV解析
- ✅ 既存項目の場合は警告ダイアログ表示後にAPI呼び出し
- ✅ 進捗表示対応（`ProgressDisplay`コンポーネント使用）
- ✅ 項目全体のCSVエクスポート機能追加

---

## フロントエンド実装

### 1. 項目詳細設定画面（FieldDetailPanel）

#### 選択肢タブにCSVインポート/エクスポートボタンを追加

**実装場所**: `src/components/FieldDetailPanel.tsx`

**UI構成**:
- 選択肢タイプ（select/radio/checkbox）の場合のみ表示
- 「CSVインポート」ボタン
- 「CSVエクスポート」ボタン

**処理フロー（インポート）**:
1. ファイル選択ダイアログを表示
2. CSVファイルを選択
3. **既存項目（`field.id !== 0`）の場合、警告表示**:
   - 「既存の選択肢設定が上書きされます。続行しますか？」という警告メッセージを表示
   - 確認ダイアログでユーザーの承認を取得
4. 新規項目（`field.id === 0`）の場合:
   - フロントエンドでCSVを解析
   - 選択肢データを`editOptionsLabels`に設定
   - 保存時に`options_json`に含めて保存
5. 既存項目（`field.id !== 0`）の場合（警告承認後）:
   - `POST /v1/forms/{form_id}/fields/{field_key}/options/import/csv`を呼び出し
   - `job_id`を取得
   - 進捗表示を開始
   - 完了後、フィールドデータを再取得

**処理フロー（エクスポート）**:
1. `POST /v1/forms/{form_id}/fields/{field_key}/options/export/csv`を呼び出し
2. `job_id`を取得
3. 進捗表示を開始
4. 完了後、`download_url`からCSVファイルをダウンロード

### 2. 項目設定画面（FormItemPage）

#### 項目全体のCSVインポート/エクスポートUI

**実装場所**: `src/pages/forms/FormItemPage.tsx`

**UI構成**:
- 既存のCSVインポートモーダルを拡張
- 「CSVエクスポート」ボタンを追加

**処理フロー（インポート）**:
1. 「CSVインポート」ボタンをクリック
2. インポートモーダルを表示
3. インポートタイプを選択（選択肢のみ / 項目全体）
4. CSVファイルを選択
5. **既存設定がある場合、警告表示**:
   - 選択肢インポートの場合: 「既存の選択肢設定が上書きされます。続行しますか？」
   - 項目全体インポートの場合: 「既存の項目設定が上書きされます。続行しますか？」
   - 確認ダイアログでユーザーの承認を取得
6. 警告承認後、`POST /v1/forms/{id}/fields/import/csv`を呼び出し
7. `job_id`を取得
8. 進捗表示を開始
9. 完了後、フィールドデータを再取得

**処理フロー（エクスポート）**:
1. 「CSVエクスポート」ボタンをクリック
2. エクスポートタイプを選択（選択肢のみ / 項目全体）
3. `POST /v1/forms/{id}/fields/export/csv`を呼び出し（項目全体の場合）
4. `job_id`を取得
5. 進捗表示を開始
6. 完了後、`download_url`からCSVファイルをダウンロード

### 3. 進捗表示コンポーネント

**既存コンポーネント**: `src/components/ProgressDisplay.tsx`

**拡張内容**:
- 新しいジョブタイプに対応
- エラーメッセージの表示
- ダウンロードボタンの表示（完了時）

### 4. CSV解析ユーティリティ（フロントエンド）

**新規ファイル**: `src/utils/csvParser.ts` ✅ 実装済み

**機能**:
- CSV文字列を解析して配列に変換
- 選択肢CSV形式の検証
- エラーハンドリング

**実装内容**:
- `parseCsv()` - CSV文字列を解析して配列に変換（RFC4180準拠）
- `validateFieldOptionsCsv()` - 選択肢CSV形式の検証
- `FieldOptionRow`型定義

---

## UI仕様

### 1. 項目詳細設定画面（選択肢タブ）

**表示条件**:
- フィールドタイプが`select`、`radio`、`checkbox`の場合のみ表示

**UI要素**:
```
[選択肢タブ]
├─ 選択肢一覧（既存）
│   └─ 選択肢の追加・編集・削除
│
├─ CSV操作セクション
│   ├─ [CSVインポート] ボタン
│   │   └─ クリック → ファイル選択ダイアログ
│   │       └─ ファイル選択
│   │           └─ 既存項目の場合: 警告ダイアログ表示
│   │               └─ 「既存の選択肢設定が上書きされます。続行しますか？」
│   │                   └─ 承認 → インポート開始
│   │                       └─ 進捗表示（モーダルまたはトースト）
│   │
│   └─ [CSVエクスポート] ボタン
│       └─ クリック → エクスポート開始
│           └─ 進捗表示（モーダルまたはトースト）
│               └─ 完了後、ダウンロード開始
```

### 2. 項目設定画面（CSV操作）

**UI要素**:
```
[項目設定画面]
├─ [CSVインポート] ボタン（既存）
│   └─ クリック → インポートモーダル表示
│       ├─ インポートタイプ選択（選択肢のみ / 項目全体）
│       ├─ CSVファイル選択
│       ├─ 警告メッセージ表示（既存設定がある場合）
│       │   ├─ 選択肢インポート: 「既存の選択肢設定が上書きされます」
│       │   └─ 項目全体インポート: 「既存の項目設定が上書きされます」
│       └─ [インポート開始] ボタン
│           └─ クリック → 確認ダイアログ表示
│               └─ 承認 → インポート開始
│
└─ [CSVエクスポート] ボタン（新規）
    └─ クリック → エクスポートモーダル表示
        ├─ エクスポートタイプ選択（選択肢のみ / 項目全体）
        └─ [エクスポート開始] ボタン
            └─ 進捗表示
                └─ 完了後、ダウンロード開始
```

### 3. 進捗表示

**表示方法**:
- モーダルまたはトースト通知
- 進捗バー（0% → 100%）
- ステータスメッセージ（翻訳対応）

**完了時の表示**:
- 成功: ダウンロードボタンを表示
- 失敗: エラーメッセージを表示

---

## エラーハンドリング

### バックエンド

**検証エラー**:
- CSV形式の不正
- 必須カラムの欠如
- データ型の不一致
- フィールドの不存在
- フィールドタイプの不一致（選択肢タイプでない）

**処理エラー**:
- データベースエラー
- ファイルI/Oエラー
- メモリ不足

**エラーレスポンス**:
```json
{
  "success": false,
  "data": null,
  "message": "エラーメッセージ（翻訳対応）",
  "errors": {
    "field": ["エラーメッセージ1", "エラーメッセージ2"]
  }
}
```

### フロントエンド

**エラー表示**:
- バリデーションエラー: 入力フィールドの下に表示
- 処理エラー: トースト通知またはモーダルで表示
- 進捗エラー: 進捗表示コンポーネント内で表示

---

## 翻訳キー

### バックエンド（messages.php）

**既存キー**:
- `csv_import_queued`
- `csv_import_preparing`
- `csv_import_reading`
- `csv_import_validating`
- `csv_import_validating_rules`
- `csv_import_importing`
- `csv_import_completed`
- `csv_import_failed`

**新規キー**:
- `field_options_csv_import_queued`: "選択肢CSVインポートをキューに追加しました" / "Field options CSV import queued"
- `field_options_csv_export_queued`: "選択肢CSVエクスポートをキューに追加しました" / "Field options CSV export queued"
- `field_options_csv_export_generating`: "選択肢CSVを生成中..." / "Generating field options CSV..."
- `field_options_csv_export_completed`: "選択肢CSVエクスポートが完了しました" / "Field options CSV export completed"
- `field_options_csv_export_failed`: "選択肢CSVエクスポートに失敗しました" / "Field options CSV export failed"
- `fields_csv_export_queued`: "項目CSVエクスポートをキューに追加しました" / "Fields CSV export queued"
- `fields_csv_export_generating`: "項目CSVを生成中..." / "Generating fields CSV..."
- `fields_csv_export_completed`: "項目CSVエクスポートが完了しました" / "Fields CSV export completed"
- `fields_csv_export_failed`: "項目CSVエクスポートに失敗しました" / "Fields CSV export failed"
- `field_not_found`: "フィールドが見つかりません" / "Field not found"
- `field_type_invalid`: "このフィールドタイプではCSVインポート/エクスポートは使用できません" / "CSV import/export is not available for this field type"
- `csv_import_field_options_empty`: "CSVファイルが空です" / "CSV file is empty"
- `csv_import_field_options_invalid_format`: "CSV形式が不正です" / "Invalid CSV format"

### フロントエンド（翻訳コンテキスト）

**新規キー**:
- `field_options_csv_import`: "選択肢CSVインポート"
- `field_options_csv_export`: "選択肢CSVエクスポート"
- `fields_csv_export`: "項目CSVエクスポート"
- `csv_import_field_options`: "選択肢をCSVでインポート"
- `csv_export_field_options`: "選択肢をCSVでエクスポート"
- `csv_export_fields`: "項目をCSVでエクスポート"
- `csv_import_field_options_description`: "CSVファイルを選択して選択肢をインポートしてください"
- `csv_export_field_options_description`: "選択肢をCSVファイルとしてエクスポートします"
- `csv_export_fields_description`: "項目全体をCSVファイルとしてエクスポートします"
- `csv_import_field_options_help`: "選択肢を1行ずつ記載したCSVファイルを選択してください（value, label, label_ja, label_en）"
- `csv_export_field_options_template`: "エクスポートしたCSVは、インポートテンプレートとしても使用できます"
- `csv_export_fields_template`: "エクスポートしたCSVは、インポートテンプレートとしても使用できます"
- `csv_import_field_options_new_field_note`: "新規項目の場合、CSVを解析して選択肢を設定します。保存時に選択肢が反映されます。"
- `csv_import_field_options_existing_field_note`: "既存項目の場合、CSVをアップロードしてインポートを開始します。"
- `csv_import_field_options_overwrite_warning`: "既存の選択肢設定が上書きされます。続行しますか？"
- `csv_import_fields_overwrite_warning`: "既存の項目設定が上書きされます。続行しますか？"
- `csv_import_overwrite_confirm`: "上書きして続行"
- `csv_import_overwrite_cancel`: "キャンセル"

---

## テスト仕様

### バックエンドテスト

#### 1. 特定フィールドの選択肢CSVインポート

**テストケース**:
- 正常系: 選択肢タイプのフィールドにCSVをインポート
- 異常系: 存在しないフィールドキー
- 異常系: 選択肢タイプでないフィールド
- 異常系: CSV形式の不正
- 異常系: 必須カラムの欠如
- 異常系: ファイルサイズ超過

#### 2. 特定フィールドの選択肢CSVエクスポート

**テストケース**:
- 正常系: 選択肢タイプのフィールドからCSVをエクスポート
- 正常系: 選択肢がない場合の空CSV
- 異常系: 存在しないフィールドキー
- 異常系: 選択肢タイプでないフィールド

#### 3. 項目全体のCSVエクスポート

**テストケース**:
- 正常系: フォーム全体の項目をCSVでエクスポート
- 正常系: 項目がない場合の空CSV
- 異常系: 存在しないフォームID

### フロントエンドテスト

#### 1. 項目詳細設定画面

**テストケース**:
- 選択肢タイプのフィールドでCSVインポート/エクスポートボタンが表示される
- 選択肢タイプでないフィールドでボタンが表示されない
- 新規項目でのCSVインポート（フロントエンド解析）
- 既存項目でのCSVインポート（API呼び出し）
- 進捗表示の動作確認
- エラー表示の動作確認

#### 2. 項目設定画面

**テストケース**:
- CSVエクスポートボタンの表示
- エクスポートタイプの選択
- 進捗表示の動作確認
- ダウンロードの動作確認

---

## 後方互換性

### 既存機能への影響

**既存のCSVインポート機能**:
- `POST /v1/forms/{id}/fields/import/csv`は既存のまま維持
- 既存の`ImportCsvJob`は変更なし

**既存の進捗取得API**:
- `GET /v1/progress/{job_id}`は既存のまま維持
- 新しいジョブタイプに対応

---

## 注意事項

### バリデーション

1. **フィールドタイプチェック**:
   - 選択肢CSVインポート/エクスポートは、select/radio/checkboxタイプのみ許可
   - それ以外のタイプではエラーを返す

2. **新規項目の処理**:
   - 新規項目（`field.id === 0`）の場合は、フロントエンドでCSVを解析
   - 保存時に選択肢を含めて保存
   - バックエンドAPIは呼び出さない

3. **既存項目の処理**:
   - 既存項目（`field.id !== 0`）の場合は、バックエンドAPIを呼び出し
   - 非同期処理でインポート
   - 完了後、フィールドデータを再取得

### データ整合性

1. **選択肢のマージ**:
   - 既存の選択肢とCSVデータをマージ（valueで重複チェック）
   - 既存の選択肢は更新、新規の選択肢は追加

2. **多言語対応**:
   - CSV形式で多言語ラベル（label_ja, label_en）をサポート
   - フォームに追加されている言語のみ処理

### UI/UX

1. **進捗表示**:
   - モーダルまたはトースト通知で進捗を表示
   - 完了後、ダウンロードボタンを表示

2. **エラーハンドリング**:
   - エラー時は詳細なエラーメッセージを表示
   - バリデーションエラーは入力フィールドの下に表示

3. **ファイルサイズ制限**:
   - 10MB制限（既存のインポート機能と同じ）

4. **上書き警告表示**:
   - 既存項目の選択肢CSVインポート時: 「既存の選択肢設定が上書きされます。続行しますか？」という警告を表示
   - 項目全体のCSVインポート時: 「既存の項目設定が上書きされます。続行しますか？」という警告を表示
   - 確認ダイアログでユーザーの承認を取得してからインポートを開始
   - 警告メッセージは翻訳対応

---

## 実装ファイル一覧

### バックエンド

**新規作成**:
- `app/Jobs/ImportFieldOptionsJob.php` - 特定フィールドの選択肢CSVインポートジョブ
- `app/Jobs/ExportFieldOptionsJob.php` - 特定フィールドの選択肢CSVエクスポートジョブ
- `app/Jobs/ExportFieldsJob.php` - 項目全体のCSVエクスポートジョブ

**修正**:
- `app/Services/CsvImportService.php` - 新規メソッド追加（`importSingleFieldOptions`, `exportSingleFieldOptions`, `exportFields`, `validateSingleFieldOptions`）
- `app/Http/Controllers/Api/V1/FormsFieldsController.php` - 新規メソッド追加（`importFieldOptions`, `exportFieldOptions`, `exportFields`）
- `routes/api.php` - 新規ルーティング追加
- `lang/ja/messages.php` - 翻訳キー追加
- `lang/en/messages.php` - 翻訳キー追加

### フロントエンド

**新規作成**:
- `src/utils/csvParser.ts` - CSV解析ユーティリティ

**修正**:
- `src/components/FieldDetailPanel.tsx` - CSVインポート/エクスポート機能追加
- `src/pages/forms/FormItemPage.tsx` - CSVエクスポート機能追加
- `src/ui/PreferencesContext.tsx` - 翻訳キー追加

## 参照

- `app/Services/CsvImportService.php` - CSVインポートサービス
- `app/Services/CsvExportService.php` - CSVエクスポートサービス（回答データ用、参考）
- `app/Jobs/ImportCsvJob.php` - CSVインポートジョブ（既存）
- `app/Jobs/ImportFieldOptionsJob.php` - 特定フィールドの選択肢CSVインポートジョブ（新規）
- `app/Jobs/ExportFieldOptionsJob.php` - 特定フィールドの選択肢CSVエクスポートジョブ（新規）
- `app/Jobs/ExportFieldsJob.php` - 項目全体のCSVエクスポートジョブ（新規）
- `app/Jobs/ExportCsvJob.php` - CSVエクスポートジョブ（回答データ用、参考）
- `app/Models/FormField.php` - フォーム項目モデル
- `app/Models/ProgressJob.php` - 進捗ジョブモデル
- `src/components/FieldDetailPanel.tsx` - 項目詳細設定パネル
- `src/pages/forms/FormItemPage.tsx` - フォーム項目設定画面
- `src/components/ProgressDisplay.tsx` - 進捗表示コンポーネント
- `src/utils/csvParser.ts` - CSV解析ユーティリティ（新規）
- `src/ui/PreferencesContext.tsx` - 翻訳コンテキスト
