# テーマエクスポート/インポート機能 実装タスク

## 概要

本ドキュメントは、テーマデータをCSV形式でエクスポート/インポートする機能を実装するためのタスクを整理したものです。

**目的**: テーマデータを本番サーバに持っていく等の需要に対応

**要件**:
1. **テーマエクスポート**: テーマデータをCSV形式でダウンロード可能（非同期/進捗表示あり）
2. **テーマインポート**: エクスポートされたテーマCSVをインポート可能（非同期/進捗表示あり、テーマコード指定、同一テーマコードはエラー）

---

## 現状確認

### テーマデータ構造

#### Themeモデル
- **テーブル**: `themes`
- **主要カラム**:
  - `id`: 主キー
  - `code`: テーマコード（ユニーク、string, 255）
  - `name`: テーマ名（string, 255）
  - `description`: 説明（text, nullable）
  - `theme_tokens`: テーマトークン（JSON）
  - `custom_style_config`: カスタムスタイル設定（JSON, nullable）
  - `is_preset`: プリセットテーマかどうか（boolean）
  - `is_active`: 有効かどうか（boolean）
  - `created_by`: 作成者ID（integer, nullable）
  - `created_at`, `updated_at`: タイムスタンプ
  - `deleted_at`: 論理削除（SoftDeletes）

#### テーマトークン構造
```json
{
  "color_primary": "#0f172a",
  "color_secondary": "#6c757d",
  "color_bg": "#ffffff",
  "color_text": "#0f172a",
  "radius": "8",
  "spacing_scale": "md",
  "font_family": "system",
  "button_style": "solid",
  "input_style": "standard"
}
```

#### カスタムスタイル設定構造
```json
{
  "presetTheme": "light",
  "headerEnabled": true,
  "footerEnabled": true,
  "globalCss": ":root { --spacing-scale: 1rem; }",
  "elements": {
    "container": { "style": { ... } },
    "card": { "className": "...", "style": { ... } },
    "buttonPrimary": { "className": "...", "style": { ... } },
    "buttonSecondary": { "className": "...", "style": { ... } },
    "input": { "className": "...", "style": { ... } },
    "header": { "style": { ... } },
    "footer": { "style": { ... } }
  }
}
```

### 既存の実装パターン

#### フォームエクスポート/インポート
- **エクスポート**: `FormExportJob`（非同期、進捗表示、ZIP形式）
- **インポート**: `FormImportJob`（非同期、進捗表示、JSON/ZIP形式）
- **API**: `FormsController@export`, `FormsController@import`

#### CSVエクスポート/インポート
- **CSVエクスポート**: `ExportCsvJob`（非同期、進捗表示、CSV形式）
- **CSVインポート**: `CsvImportService`（同期処理）
- **進捗管理**: `ProgressJob`モデルを使用

#### 既存のテーマAPI
- `GET /v1/system/themes`: テーマ一覧
- `POST /v1/system/themes`: テーマ作成
- `GET /v1/system/themes/{id}`: テーマ詳細
- `PUT /v1/system/themes/{id}`: テーマ更新
- `DELETE /v1/system/themes/{id}`: テーマ削除
- `GET /v1/system/themes/{id}/usage`: テーマ使用状況
- `POST /v1/system/themes/{id}/copy`: テーマコピー

#### 権限管理
- **テーマ管理**: `themes.read`, `themes.write`, `themes.delete`パーミッション
- **system_admin以上**: テーマの作成・更新・削除が可能
- **プリセットテーマ更新**: root-only

---

## タスク1: テーマエクスポート機能

### 1.1 バックエンド: テーマエクスポートジョブ実装

#### 1.1.1 ジョブ作成
- **ファイル**: `app/Jobs/ThemeExportJob.php`（新規作成）
- **責務**: テーマデータのCSVエクスポート処理（非同期）
- **進捗管理**: `ProgressJob`を使用
- **キュー**: `exports`キュー

#### 1.1.2 処理フロー
1. 進捗ジョブの取得・検証
2. テーマデータの取得（`Theme`モデルから取得、論理削除済みは除外）
3. 進捗更新（0% → 30%）
4. CSV形式でデータを構築
5. 進捗更新（30% → 80%）
6. CSVファイルを保存（`exports/{job_id}_themes.csv`）
7. 進捗更新（80% → 100%）
8. ダウンロードURLを生成
9. 進捗ジョブを完了状態に更新

#### 1.1.3 CSV形式
```csv
code,name,description,theme_tokens,custom_style_config,is_preset,is_active,created_by,created_at,updated_at
dark,ダークテーマ,暗い背景のダークテーマ,"{""color_primary"":""#ffffff"",...}","{""presetTheme"":""dark"",...}",true,true,,2024-01-01T00:00:00Z,2024-01-01T00:00:00Z
light,ライトテーマ,明るい背景のライトテーマ,"{""color_primary"":""#0f172a"",...}","{""presetTheme"":""light"",...}",true,true,,2024-01-01T00:00:00Z,2024-01-01T00:00:00Z
```

**CSVカラム**:
- `code`: テーマコード（必須）
- `name`: テーマ名（必須）
- `description`: 説明（nullable）
- `theme_tokens`: テーマトークン（JSON文字列）
- `custom_style_config`: カスタムスタイル設定（JSON文字列、nullable）
- `is_preset`: プリセットテーマかどうか（boolean: true/false）
- `is_active`: 有効かどうか（boolean: true/false）
- `created_by`: 作成者ID（integer、nullable）
- `created_at`: 作成日時（ISO8601形式）
- `updated_at`: 更新日時（ISO8601形式）

**注意事項**:
- JSONフィールド（`theme_tokens`, `custom_style_config`）はJSON文字列としてエスケープして出力
- フォームとテーマの関連データ（`forms.theme_id`）は含めない
- 論理削除済みテーマ（`deleted_at IS NOT NULL`）は除外

#### 1.1.4 実装ファイル
- `app/Jobs/ThemeExportJob.php`（新規作成）

---

### 1.2 バックエンド: テーマエクスポートAPI実装

#### 1.2.1 エンドポイント追加
- **パス**: `POST /v1/system/themes/export`
- **権限**: `themes.read`パーミッション（system_admin以上）
- **リクエスト**: なし（全テーマをエクスポート）
- **レスポンス**: 
  ```json
  {
    "success": true,
    "data": {
      "job": {
        "job_id": "uuid-string"
      }
    },
    "message": "messages.theme_export_started"
  }
  ```

#### 1.2.2 実装内容
- **ファイル**: `app/Http/Controllers/Api/V1/System/ThemesController.php`（既存ファイルに追加）
- **メソッド**: `export`
- **処理フロー**:
  1. 権限チェック（`themes.read`パーミッション）
  2. `ProgressJob`を作成（`type: 'theme_export'`, `status: 'pending'`）
  3. `ThemeExportJob`をディスパッチ
  4. ジョブIDを返却

#### 1.2.3 実装ファイル
- `app/Http/Controllers/Api/V1/System/ThemesController.php`（exportメソッド追加）
- `routes/api.php`（ルーティング追加）

---

### 1.3 フロントエンド: テーマエクスポートUI実装

#### 1.3.1 テーマ一覧画面への追加
- **場所**: `src/pages/system/ThemeListPage.tsx`
- **機能**: テーマ一覧画面の上部に「エクスポート」ボタンを追加
- **権限**: `themes.read`パーミッション（system_admin以上）の場合のみ表示

#### 1.3.2 実装内容
1. エクスポートボタンの追加
2. クリック時に`POST /v1/system/themes/export`を呼び出し
3. ジョブIDを取得して`exportJobId`ステートに保存
4. `ProgressDisplay`コンポーネントで進捗表示
5. 完了時に自動ダウンロード（`downloadFile`を使用）
6. エラーハンドリング

#### 1.3.3 実装ファイル
- `src/pages/system/ThemeListPage.tsx`（既存ファイルに追加）

---

## タスク2: テーマインポート機能

### 2.1 バックエンド: テーマインポートジョブ実装

#### 2.1.1 ジョブ作成
- **ファイル**: `app/Jobs/ThemeImportJob.php`（新規作成）
- **責務**: テーマデータのCSVインポート処理（非同期）
- **進捗管理**: `ProgressJob`を使用
- **キュー**: `imports`キュー

#### 2.1.2 処理フロー
1. 進捗ジョブの取得・検証
2. 一時ファイルの存在確認
3. 進捗更新（0% → 20%）
4. CSVファイルの読み込み・解析
5. 進捗更新（20% → 40%）
6. CSVデータの検証（必須カラム、データ形式、テーマコードの重複チェック）
7. 進捗更新（40% → 60%）
8. テーマデータの作成（トランザクション内で実行）
9. 進捗更新（60% → 80%）
10. 検証エラーの集計
11. 進捗更新（80% → 100%）
12. 進捗ジョブを完了状態に更新（成功/失敗情報を含む）

#### 2.1.3 CSV検証ルール
- **必須カラム**: `code`, `name`
- **テーマコードの重複チェック**: 既存のテーマコードと重複する場合はエラー
- **データ形式検証**:
  - `theme_tokens`: 有効なJSON形式か確認
  - `custom_style_config`: 有効なJSON形式か確認（nullable）
  - `is_preset`: `true`または`false`の文字列
  - `is_active`: `true`または`false`の文字列
  - `created_by`: 整数または空文字（nullable）

#### 2.1.4 エラーハンドリング
- CSV解析エラー: 行番号とエラー内容を記録
- バリデーションエラー: 行番号とエラー内容を記録
- テーマコード重複エラー: 行番号と重複しているテーマコードを記録
- トランザクションエラー: ロールバックしてエラーを記録

#### 2.1.5 実装ファイル
- `app/Jobs/ThemeImportJob.php`（新規作成）

---

### 2.2 バックエンド: テーマインポートAPI実装

#### 2.2.1 エンドポイント追加
- **パス**: `POST /v1/system/themes/import`
- **権限**: `themes.write`パーミッション（system_admin以上）
- **リクエスト**: `multipart/form-data`
  - `file`: CSVファイル（必須）
  - `theme_code`: テーマコード（オプション、指定時は全行に適用）
- **レスポンス**: 
  ```json
  {
    "success": true,
    "data": {
      "job": {
        "job_id": "uuid-string"
      }
    },
    "message": "messages.theme_import_started"
  }
  ```

#### 2.2.2 実装内容
- **ファイル**: `app/Http/Controllers/Api/V1/System/ThemesController.php`（既存ファイルに追加）
- **メソッド**: `import`
- **処理フロー**:
  1. 権限チェック（`themes.write`パーミッション）
  2. リクエストバリデーション（ファイル、テーマコード）
  3. アップロードされたファイルを一時保存
  4. `ProgressJob`を作成（`type: 'theme_import'`, `status: 'pending'`）
  5. `ThemeImportJob`をディスパッチ（一時ファイルパス、テーマコード、ユーザーIDを渡す）
  6. ジョブIDを返却

#### 2.2.3 テーマコードの指定方法
- **リクエストパラメータで指定**: `theme_code`パラメータで指定した場合、CSV内の`code`カラムを無視して、指定されたテーマコードを使用
- **CSV内で指定**: `theme_code`パラメータが未指定の場合、CSV内の`code`カラムを使用
- **重複チェック**: 指定されたテーマコード（またはCSV内のテーマコード）が既存のテーマコードと重複する場合はエラー

#### 2.2.4 実装ファイル
- `app/Http/Controllers/Api/V1/System/ThemesController.php`（importメソッド追加）
- `routes/api.php`（ルーティング追加）

---

### 2.3 フロントエンド: テーマインポートUI実装

#### 2.3.1 テーマ一覧画面への追加
- **場所**: `src/pages/system/ThemeListPage.tsx`
- **機能**: テーマ一覧画面の上部に「インポート」ボタンを追加
- **権限**: `themes.write`パーミッション（system_admin以上）の場合のみ表示

#### 2.3.2 実装内容
1. インポートボタンの追加
2. クリック時にファイル選択ダイアログを表示
3. CSVファイルを選択
4. テーマコード指定オプション（オプション入力フィールド）
5. `POST /v1/system/themes/import`を呼び出し（`FormData`を使用）
6. ジョブIDを取得して`importJobId`ステートに保存
7. `ProgressDisplay`コンポーネントで進捗表示
8. 完了時に成功メッセージを表示
9. エラーハンドリング（バリデーションエラー、重複エラー等）

#### 2.3.3 実装ファイル
- `src/pages/system/ThemeListPage.tsx`（既存ファイルに追加）

---

## 実装順序の推奨

### Phase 1: バックエンド実装
1. `ThemeExportJob`の実装（CSV生成、進捗管理）
2. `ThemesController@export`の実装（APIエンドポイント、ジョブディスパッチ）
3. `routes/api.php`にエクスポートルーティング追加
4. `ThemeImportJob`の実装（CSV解析、検証、インポート処理、進捗管理）
5. `ThemesController@import`の実装（APIエンドポイント、ファイルアップロード、ジョブディスパッチ）
6. `routes/api.php`にインポートルーティング追加

### Phase 2: フロントエンド実装
1. `ThemeListPage`にエクスポートボタン追加（進捗表示対応）
2. `ThemeListPage`にインポートボタン追加（ファイル選択、テーマコード指定、進捗表示対応）

---

## 技術的な考慮事項

### CSV形式
- **エンコーディング**: UTF-8 BOM付き（Excel互換性のため）
- **エスケープ**: RFC4180準拠（カンマ、改行、ダブルクォートをエスケープ）
- **JSONフィールド**: `theme_tokens`と`custom_style_config`はJSON文字列として出力（改行を含む可能性があるため、適切にエスケープ）

### パフォーマンス
- **非同期処理**: 大量のテーマデータに対応するため、ジョブキューで非同期処理
- **進捗管理**: `ProgressJob`を使用して進捗状況を返却
- **タイムアウト**: ジョブのタイムアウト時間を適切に設定（デフォルト: 600秒）

### エラーハンドリング
- **CSV解析エラー**: 行番号とエラー内容を記録
- **バリデーションエラー**: 行番号とエラー内容を記録
- **テーマコード重複エラー**: 行番号と重複しているテーマコードを記録
- **トランザクションエラー**: ロールバックしてエラーを記録
- **部分的な失敗**: 複数行のCSVで一部が失敗した場合、成功した行数と失敗した行数を記録

### セキュリティ
- **権限チェック**: `themes.read`（エクスポート）、`themes.write`（インポート）
- **ファイル検証**: アップロードされたファイルがCSV形式であることを確認
- **データ検証**: インポート時のデータ検証（不正なデータの注入防止）

### データ整合性
- **トランザクション管理**: インポート処理はトランザクション内で実行
- **テーマコードのユニーク性**: インポート時に既存のテーマコードと重複チェック
- **JSON形式の検証**: `theme_tokens`と`custom_style_config`が有効なJSON形式であることを確認

---

## 関連ファイル一覧

### バックエンド（新規作成）
- `app/Jobs/ThemeExportJob.php`（新規作成）
- `app/Jobs/ThemeImportJob.php`（新規作成）

### バックエンド（修正）
- `app/Http/Controllers/Api/V1/System/ThemesController.php`（export, importメソッド追加）
- `routes/api.php`（ルーティング追加）

### フロントエンド（修正）
- `src/pages/system/ThemeListPage.tsx`（エクスポート/インポートボタン追加、進捗表示対応）

### 言語ファイル（追加）
- `lang/ja/messages.php`（テーマエクスポート/インポート関連メッセージ）
- `lang/en/messages.php`（テーマエクスポート/インポート関連メッセージ）

---

## 実装状況

### バックエンド
- ✅ テーマエクスポートジョブの実装（`ThemeExportJob.php`）
- ✅ CSV形式でのエクスポート（全カラム）
- ✅ JSONフィールドの適切なエスケープ
- ✅ 進捗管理（0% → 30% → 80% → 100%）
- ✅ ダウンロードURLの生成
- ✅ テーマインポートジョブの実装（`ThemeImportJob.php`）
- ✅ CSV解析処理
- ✅ バリデーション処理（必須カラム、データ形式）
- ✅ テーマコード重複チェック
- ✅ トランザクション管理
- ✅ エラーハンドリング（CSV解析エラー、バリデーションエラー、重複エラー）
- ✅ 権限チェック（themes.read, themes.write）
- ✅ APIエンドポイント実装（`ThemesController@export`, `ThemesController@import`）
- ✅ ルーティング追加（`routes/api.php`）
- ✅ 多言語対応（`lang/ja/messages.php`, `lang/en/messages.php`）

### フロントエンド
- ✅ エクスポートボタンの表示（themes.read権限がある場合のみ）
- ✅ エクスポート処理の実行
- ✅ 進捗表示（ProgressDisplay）
- ✅ 完了時の自動ダウンロード
- ✅ インポートボタンの表示（themes.write権限がある場合のみ）
- ✅ ファイル選択ダイアログ
- ✅ テーマコード指定オプション
- ✅ インポート処理の実行
- ✅ 進捗表示（ProgressDisplay）
- ✅ 完了時の成功メッセージ表示
- ✅ エラーハンドリング（バリデーションエラー、重複エラー等）
- ✅ 多言語対応（`PreferencesContext.tsx`）

**実装完了日**: 2026-01-23

---

## 参考情報

### 既存の類似機能
- **フォームエクスポート/インポート**: `FormExportJob`, `FormImportJob`（JSON/ZIP形式）
- **CSVエクスポート**: `ExportCsvJob`（回答データのCSVエクスポート）
- **CSVインポート**: `CsvImportService`（フォーム項目のCSVインポート）
- **進捗管理**: `ProgressJob`モデル、`ProgressController`

### 関連ドキュメント
- `FORM_EXPORT_IMPORT_ARCHIVE_TASKS.md`: フォームエクスポート/インポート機能の実装タスク
- `CSV_FIELDS_STEP_GROUP_FORMAT.md`: CSV形式の仕様
