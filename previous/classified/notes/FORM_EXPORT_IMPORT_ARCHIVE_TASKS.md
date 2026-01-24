# フォームエクスポート/インポート・アーカイブ機能 実装タスク

## 概要

本ドキュメントは、以下の機能を実装するためのタスクを整理したものです：

1. **フォームエクスポート/インポート機能**: staging環境で作成したフォームの構成を本番環境に移行するための機能
2. **フォームアーカイブ機能**: 古いフォームと回答データをS3にアーカイブ化し、物理削除する機能

---

## 現状確認

### データモデル構造

#### Form（フォーム）
- **テーブル**: `forms`
- **論理削除**: `SoftDeletes`使用（`deleted_at`カラム）
- **主要カラム**:
  - `code`: フォームコード（一意）
  - `status`: ステータス（draft/published/closed）
  - `public_period_start`, `public_period_end`: 公開期間
  - `attachment_enabled`, `attachment_type`, `pdf_template_path`, `attachment_files_json`: 添付ファイル設定
  - `notification_user_enabled`, `notification_user_email_*`: ユーザー通知設定
  - `notification_admin_enabled`, `notification_admin_*`: 管理者通知設定
  - `theme_id`, `theme_tokens`, `custom_style_config`: テーマ設定
  - `logo_path`, `logo_json`: ロゴ設定
  - `layout_width_json`: レイアウト設定
  - `step_group_structure`: STEP/GROUP構造（JSON）
  - `csv_system_columns_json`: CSV出力設定
  - `created_by`, `updated_by`, `deleted_by`: 作成者/更新者/削除者

#### FormTranslation（フォーム翻訳）
- **テーブル**: `form_translations`
- **リレーション**: `Form` に `hasMany`
- **主要カラム**:
  - `form_id`: フォームID
  - `locale`: ロケール（ja/en等）
  - `title`: タイトル
  - `description`: 説明

#### FormField（フォーム項目）
- **テーブル**: `form_fields`
- **リレーション**: `Form` に `hasMany`
- **主要カラム**:
  - `form_id`: フォームID
  - `field_key`: フィールドキー
  - `type`: フィールドタイプ
  - `step_key`, `group_key`: STEP/GROUPキー
  - `sort_order`: 並び順
  - `is_required`: 必須フラグ
  - `options_json`: オプション設定（JSON）
  - `visibility_rule`, `required_rule`, `step_transition_rule`, `computed_rule`: ルール設定（JSON）

#### Submission（送信データ）
- **テーブル**: `submissions`
- **物理削除**: `SoftDeletes`なし
- **主要カラム**:
  - `form_id`: フォームID
  - `status`: ステータス
  - `confirm_token`, `confirm_token_expires_at`: 確認トークン

#### SubmissionValue（送信値）
- **テーブル**: `submission_values`
- **リレーション**: `Submission` に `hasMany`
- **主要カラム**:
  - `submission_id`: 送信ID
  - `field_key`: フィールドキー
  - `field_label_snapshot`: フィールドラベルのスナップショット
  - `value_json`: 値（JSON）
  - `label_json`: ラベル（JSON）

### 既存の権限管理

#### バックエンド
- **ミドルウェア**: `reforma.system_admin`（`EnsureSystemAdmin`）
- **ロールチェック**: `$user->hasRole(RoleCode::FORM_ADMIN)` / `$user->hasRole(RoleCode::SYSTEM_ADMIN)`
- **パーミッションチェック**: `$user->hasPermission('forms.read')` / `$user->hasPermission('forms.write')` / `$user->hasPermission('forms.delete')`

#### フロントエンド
- **フック**: `useHasRole(["form_admin", "system_admin"])`
- **関数**: `hasAnyUiRole(user, ["form_admin", "system_admin"])`

### 既存のストレージ機能

- **PdfStorageService**: S3とローカルストレージの切り替え対応
- **設定**: `config/reforma.php` の `pdf.storage_disk`（local or s3）
- **Storage**: Laravelの`Storage`ファサードを使用

### 既存のAPIエンドポイント

- `GET /v1/forms`: フォーム一覧
- `POST /v1/forms`: フォーム作成
- `GET /v1/forms/{id}`: フォーム取得
- `PUT /v1/forms/{id}`: フォーム更新
- `DELETE /v1/forms/{id}`: フォーム削除（論理削除）
- `GET /v1/forms/{id}/fields`: フォーム項目一覧
- `PUT /v1/forms/{id}/fields`: フォーム項目一括更新

---

## タスク1: フォームエクスポート/インポート機能

### 1.1 バックエンド: エクスポートAPI実装

#### 1.1.1 エンドポイント追加
- **パス**: `GET /v1/forms/{id}/export`
- **権限**: `form_admin` または `system_admin`
- **レスポンス**: JSON形式のフォームデータ（ZIPファイルとしてダウンロード可能）

#### 1.1.2 エクスポートデータ構造
```json
{
  "version": "1.0.0",
  "exported_at": "2024-01-01T00:00:00Z",
  "form": {
    "code": "form_001",
    "status": "draft",
    "public_period_start": null,
    "public_period_end": null,
    "answer_period_start": null,
    "answer_period_end": null,
    "attachment_enabled": false,
    "attachment_type": null,
    "pdf_template_path": null,
    "attachment_files_json": null,
    "notification_user_enabled": false,
    "notification_user_email_from": null,
    "notification_user_email_reply_to": null,
    "notification_user_email_cc": null,
    "notification_user_email_bcc": null,
    "notification_admin_enabled": false,
    "notification_admin_user_ids": null,
    "notification_admin_email_from": null,
    "notification_admin_email_reply_to": null,
    "theme_id": null,
    "theme_tokens": null,
    "custom_style_config": null,
    "logo_path": null,
    "logo_json": null,
    "layout_width_json": null,
    "step_group_structure": {},
    "csv_system_columns_json": null
  },
  "translations": [
    {
      "locale": "ja",
      "title": "フォームタイトル",
      "description": "フォーム説明",
      "notification_user_email_template": null,
      "notification_user_email_subject": null,
      "notification_admin_email_template": null,
      "notification_admin_email_subject": null,
      "attachment_description": null,
      "attachment_type": null,
      "attachment_files_json": null
    }
  ],
  "fields": [
    {
      "field_key": "field_001",
      "type": "text",
      "step_key": "step_1",
      "group_key": "default",
      "sort_order": 0,
      "is_required": true,
      "options_json": {},
      "visibility_rule": null,
      "required_rule": null,
      "step_transition_rule": null,
      "computed_rule": null,
      "pdf_block_key": null,
      "pdf_page_number": null,
      "csv_export_enabled": false,
      "csv_label_json": null
    }
  ],
  "files": {
    "logo": null,
    "pdf_template": null,
    "attachments": []
  }
}
```

#### 1.1.3 実装ファイル
- **コントローラ**: `app/Http/Controllers/Api/V1/FormsController.php` に `export` メソッド追加
- **サービス**: `app/Services/FormExportService.php`（新規作成）
- **リクエスト**: `app/Http/Requests/FormExportRequest.php`（新規作成、バリデーション用）

#### 1.1.4 実装内容
1. フォーム基本情報の取得
2. 翻訳データの取得
3. 項目データの取得
4. 添付ファイル（ロゴ、PDFテンプレート、添付ファイル）の取得
5. JSON形式でデータを構築
6. ファイルがある場合はZIPファイルとして圧縮
7. レスポンスとして返却（Content-Type: application/json または application/zip）

### 1.2 バックエンド: インポートAPI実装

#### 1.2.1 エンドポイント追加
- **パス**: `POST /v1/forms/import`
- **権限**: `form_admin` または `system_admin`
- **リクエスト**: multipart/form-data（JSONファイルまたはZIPファイル）

#### 1.2.2 インポート処理フロー
1. アップロードされたファイルの検証（JSON形式またはZIP形式）
2. ZIPファイルの場合は展開
3. JSONデータの検証（必須フィールド、データ形式）
4. フォームコードの重複チェック（既存のフォームコードと重複する場合はエラー、または新規コードを生成）
5. テーマIDの存在チェック（存在しない場合はnullに設定）
6. フォーム基本情報の作成
7. 翻訳データの作成
8. 項目データの作成
9. 添付ファイルのコピー（ロゴ、PDFテンプレート、添付ファイル）
10. 作成されたフォームIDを返却

#### 1.2.3 実装ファイル
- **コントローラ**: `app/Http/Controllers/Api/V1/FormsController.php` に `import` メソッド追加
- **サービス**: `app/Services/FormImportService.php`（新規作成）
- **リクエスト**: `app/Http/Requests/FormImportRequest.php`（新規作成、バリデーション用）

#### 1.2.4 注意事項
- フォームコードの重複処理: オプションで「既存コードを上書き」または「新規コードを生成」を選択可能
- テーマIDのマッピング: 異なる環境間でテーマIDが異なる場合の対応（テーマコードでマッピング）
- ファイルパスの調整: ストレージパスの環境依存性を考慮

### 1.3 フロントエンド: エクスポートUI実装

#### 1.3.1 フォーム一覧画面への追加
- **場所**: `FormListPage.tsx`
- **機能**: 各フォームの操作ボタンに「エクスポート」ボタンを追加
- **権限**: `canManageForms`（form_admin / system_admin）の場合のみ表示

#### 1.3.2 実装内容
1. エクスポートボタンの追加
2. クリック時にAPIを呼び出し
3. レスポンスをZIPファイルまたはJSONファイルとしてダウンロード
4. ローディング状態の表示
5. エラーハンドリング

### 1.4 フロントエンド: インポートUI実装

#### 1.4.1 フォーム一覧画面への追加
- **場所**: `FormListPage.tsx`
- **機能**: フォーム作成ボタンの近くに「インポート」ボタンを追加
- **権限**: `canManageForms`（form_admin / system_admin）の場合のみ表示

#### 1.4.2 実装内容
1. インポートボタンの追加
2. ファイル選択ダイアログの表示
3. ファイルアップロード処理
4. インポートオプションの選択（フォームコードの重複処理方法）
5. インポート実行
6. 成功時はフォーム編集画面に遷移
7. エラーハンドリング（バリデーションエラー、重複エラー等）

---

## タスク2: フォームアーカイブ機能

### 2.1 バックエンド: アーカイブAPI実装

#### 2.1.1 エンドポイント追加
- **パス**: `POST /v1/forms/{id}/archive`
- **権限**: `system_admin` のみ
- **処理**: フォームと回答データをS3にアーカイブ化し、物理削除

#### 2.1.2 アーカイブデータ構造
```
archive-{form_id}-{timestamp}.zip
├── form.json              # フォーム基本情報
├── translations.json      # 翻訳データ
├── fields.json            # 項目データ
├── submissions.json       # 送信データ
├── submission_values.json # 送信値データ（value_json, label_jsonを含む）
├── files/                 # 添付ファイル
│   ├── logo/
│   ├── pdf_template/
│   └── attachments/
└── metadata.json          # アーカイブメタデータ（アーカイブ日時、ユーザー情報等）
```

#### 2.1.3 実装ファイル
- **コントローラ**: `app/Http/Controllers/Api/V1/FormsController.php` に `archive` メソッド追加
- **サービス**: `app/Services/FormArchiveService.php`（新規作成）
- **リクエスト**: `app/Http/Requests/FormArchiveRequest.php`（新規作成、バリデーション用）

#### 2.1.4 実装内容
1. フォーム基本情報の取得
2. 翻訳データの取得
3. 項目データの取得
4. 送信データの取得（`submissions`テーブル）
5. 送信値データの取得（`submission_values`テーブル）
6. 添付ファイルの取得（ロゴ、PDFテンプレート、添付ファイル、生成されたPDF）
7. メタデータの作成（アーカイブ日時、実行ユーザー情報等）
8. ZIPファイルとして圧縮
9. S3にアップロード（バケット: `reforma-archives`、パス: `forms/{form_id}/archive-{timestamp}.zip`）
10. 関連データの物理削除（トランザクション内で実行）
    - `submission_values` の削除
    - `submissions` の削除
    - `form_fields` の削除
    - `form_translations` の削除
    - `forms` の物理削除（`forceDelete()`）
13. テーブルのフラグメント解消（`OPTIMIZE TABLE` を実行）
14. アーカイブ情報をデータベースに記録（`form_archives`テーブルに新規作成）

#### 2.1.5 データベーステーブル追加
- **テーブル**: `form_archives`
- **カラム**:
  - `id`: 主キー
  - `form_id`: 元のフォームID（削除済みのため参照不可だが、記録用）
  - `form_code`: フォームコード（記録用）
  - `archive_path`: S3のアーカイブパス
  - `archive_size`: アーカイブファイルサイズ（バイト）
  - `archived_at`: アーカイブ日時
  - `archived_by`: アーカイブ実行ユーザーID
  - `metadata_json`: メタデータ（JSON）
  - `created_at`, `updated_at`: タイムスタンプ

#### 2.1.6 マイグレーション
- **ファイル**: `database/migrations/YYYY_MM_DD_HHMMSS_create_form_archives_table.php`

### 2.2 バックエンド: アーカイブ復元API実装

#### 2.2.1 エンドポイント追加
- **パス**: `POST /v1/forms/archive/{archive_id}/restore`
- **権限**: `system_admin` のみ
- **処理**: S3からアーカイブを取得し、新しいフォームとして復元

#### 2.2.2 復元処理フロー
1. アーカイブ情報の取得（`form_archives`テーブル）
2. S3からアーカイブファイルをダウンロード
3. ZIPファイルを展開
4. JSONデータの検証
5. フォームコードの重複チェック（既存のフォームコードと重複する場合は新規コードを生成）
6. テーマIDの存在チェック（存在しない場合はnullに設定）
7. フォーム基本情報の作成（新しいIDで作成）
8. 翻訳データの作成
9. 項目データの作成
10. 送信データの作成（`submissions`テーブル）
11. 送信値データの作成（`submission_values`テーブル）
12. 添付ファイルのコピー（ロゴ、PDFテンプレート、添付ファイル、生成されたPDF）
13. 復元されたフォームIDを返却

#### 2.2.3 実装ファイル
- **コントローラ**: `app/Http/Controllers/Api/V1/FormsController.php` に `restoreArchive` メソッド追加
- **サービス**: `app/Services/FormArchiveService.php` に `restore` メソッド追加
- **リクエスト**: `app/Http/Requests/FormRestoreArchiveRequest.php`（新規作成、バリデーション用）

### 2.3 バックエンド: アーカイブ一覧API実装

#### 2.3.1 エンドポイント追加
- **パス**: `GET /v1/forms/archives`
- **権限**: `system_admin` のみ
- **レスポンス**: アーカイブ一覧（ページネーション対応）

#### 2.3.2 実装ファイル
- **コントローラ**: `app/Http/Controllers/Api/V1/FormsController.php` に `archives` メソッド追加

### 2.4 フロントエンド: アーカイブUI実装

#### 2.4.1 フォーム一覧画面への追加
- **場所**: `FormListPage.tsx`
- **機能**: 各フォームの操作ボタンに「アーカイブ」ボタンを追加
- **権限**: `system_admin` の場合のみ表示

#### 2.4.2 実装内容
1. アーカイブボタンの追加
2. 確認ダイアログの表示（物理削除の警告）
3. クリック時にAPIを呼び出し
4. ローディング状態の表示
5. 成功時はフォーム一覧から削除
6. エラーハンドリング

### 2.5 フロントエンド: アーカイブ一覧・復元UI実装

#### 2.5.1 アーカイブ一覧画面の作成
- **場所**: `src/pages/forms/FormArchiveListPage.tsx`（新規作成）
- **機能**: アーカイブ一覧の表示、復元機能

#### 2.5.2 実装内容
1. アーカイブ一覧の表示（ページネーション対応）
2. 各アーカイブの情報表示（フォームコード、アーカイブ日時、サイズ等）
3. 復元ボタンの追加
4. 復元確認ダイアログの表示
5. 復元処理の実行
6. 成功時はフォーム編集画面に遷移
7. エラーハンドリング

#### 2.5.3 ルーティング追加
- **パス**: `/forms/archives`
- **画面ID**: `FORM_ARCHIVE_LIST`
- **権限**: `system_admin` のみ

---

## 実装順序の推奨

### Phase 1: フォームエクスポート/インポート機能
1. バックエンド: エクスポートジョブ実装（非同期処理、`FORM_STORAGE_MIGRATION_TO_S3_TASKS.md`のタスク3.1を参照）
2. バックエンド: エクスポートAPI実装（1.1、ジョブディスパッチ）
3. バックエンド: インポートジョブ実装（非同期処理、`FORM_STORAGE_MIGRATION_TO_S3_TASKS.md`のタスク3.2を参照）
4. バックエンド: インポートAPI実装（1.2、ジョブディスパッチ）
5. フロントエンド: エクスポートUI実装（1.3、進捗管理対応）
6. フロントエンド: インポートUI実装（1.4、進捗管理対応）

### Phase 2: フォームアーカイブ機能
1. データベース: `form_archives`テーブルの作成（2.1.5）
2. バックエンド: アーカイブジョブ実装（非同期処理、`FORM_STORAGE_MIGRATION_TO_S3_TASKS.md`のタスク3.3を参照）
3. バックエンド: アーカイブAPI実装（2.1、ジョブディスパッチ）
4. バックエンド: アーカイブ一覧API実装（2.3）
5. バックエンド: アーカイブ復元ジョブ実装（非同期処理、`FORM_STORAGE_MIGRATION_TO_S3_TASKS.md`のタスク3.4を参照）
6. バックエンド: アーカイブ復元API実装（2.2、ジョブディスパッチ）
7. フロントエンド: アーカイブUI実装（2.4、進捗管理対応）
8. フロントエンド: アーカイブ一覧・復元UI実装（2.5、進捗管理対応）

---

## 技術的な考慮事項

### ファイルサイズ
- 大きなフォーム（多数の回答データを含む）の場合、ZIPファイルのサイズが大きくなる可能性
- ストリーミング処理や非同期処理（ジョブキュー）の検討

### パフォーマンス
- **全処理を非同期化**: エクスポート/インポート/アーカイブ処理は全てジョブキューで非同期処理とする
- `ProgressJob`を使用して進捗状況を返却
- 詳細は `FORM_STORAGE_MIGRATION_TO_S3_TASKS.md` の「タスク3: エクスポート/インポート/アーカイブ処理の非同期化」を参照

### エラーハンドリング
- アーカイブ処理中のエラー（S3アップロード失敗、データベース削除失敗等）のロールバック処理
- 部分的な失敗時の対応（トランザクション管理）

### セキュリティ
- アーカイブファイルへのアクセス制御（S3の署名付きURL、有効期限設定）
- インポート時のデータ検証（不正なデータの注入防止）

### データ整合性
- アーカイブ処理中のフォームへのアクセス制御（ロック機構）
- 復元時の外部キー制約の考慮（テーマID等）

---

## 関連ファイル一覧

### バックエンド（新規作成）
- `app/Http/Controllers/Api/V1/FormsController.php`（既存ファイルに追加）
- `app/Services/FormExportService.php`
- `app/Services/FormImportService.php`
- `app/Services/FormArchiveService.php`
- `app/Http/Requests/FormExportRequest.php`
- `app/Http/Requests/FormImportRequest.php`
- `app/Http/Requests/FormArchiveRequest.php`
- `app/Http/Requests/FormRestoreArchiveRequest.php`
- `app/Models/FormArchive.php`
- `database/migrations/YYYY_MM_DD_HHMMSS_create_form_archives_table.php`
- `app/Jobs/FormExportJob.php`（非同期処理用）
- `app/Jobs/FormImportJob.php`（非同期処理用）
- `app/Jobs/FormArchiveJob.php`（非同期処理用）
- `app/Jobs/FormArchiveRestoreJob.php`（非同期処理用）

### フロントエンド（新規作成・修正）
- ✅ `src/pages/forms/FormListPage.tsx`（既存ファイルに追加） - **実装済み**: エクスポート/インポート/アーカイブボタン（2026-01-23実装完了）
- ✅ `src/pages/forms/FormArchiveListPage.tsx`（新規作成） - **実装済み**: アーカイブ一覧画面（2026-01-23実装完了）
- ✅ `src/routePaths.ts`（既存ファイルに追加） - **実装済み**: アーカイブ一覧画面のルーティング（2026-01-23実装完了）
- ✅ `src/specs/screen.v1.0.json`（既存ファイルに追加、アーカイブ一覧画面の定義） - **実装済み**: アーカイブ一覧画面の定義（2026-01-23実装完了）
- ✅ `src/layout/AppLayout.tsx`（既存ファイルに追加） - **実装済み**: サイドメニューへの追加（2026-01-23実装完了）
- ✅ `src/App.tsx`（既存ファイルに追加） - **実装済み**: ルーティング追加（2026-01-23実装完了）

---

## 実装状況（2026-01-23確認）

### ✅ バックエンド: 実装済み

#### エクスポート機能
- [x] フォーム基本情報のエクスポート（バックエンド実装済み）
- [x] 翻訳データのエクスポート（バックエンド実装済み）
- [x] 項目データのエクスポート（バックエンド実装済み）
- [x] 添付ファイルのエクスポート（バックエンド実装済み）
- [x] 権限チェック（form_admin / system_admin）（バックエンド実装済み）
- [x] エラーハンドリング（存在しないフォームID等）（バックエンド実装済み）

#### インポート機能
- [x] JSONファイルのインポート（バックエンド実装済み）
- [x] ZIPファイルのインポート（バックエンド実装済み）
- [x] フォームコードの重複処理（バックエンド実装済み）
- [x] テーマIDのマッピング（バックエンド実装済み）
- [x] 添付ファイルの復元（バックエンド実装済み）
- [x] 権限チェック（form_admin / system_admin）（バックエンド実装済み）
- [x] エラーハンドリング（不正なデータ形式等）（バックエンド実装済み）

#### アーカイブ機能
- [x] フォームと回答データのアーカイブ化（バックエンド実装済み）
- [x] S3へのアップロード（バックエンド実装済み）
- [x] 物理削除の実行（バックエンド実装済み）
- [x] テーブルのフラグメント解消（バックエンド実装済み）
- [x] アーカイブ情報の記録（バックエンド実装済み）
- [x] 権限チェック（system_adminのみ）（バックエンド実装済み）
- [x] エラーハンドリング（S3アップロード失敗、データベース削除失敗等）（バックエンド実装済み）
- [x] 生成PDFのアーカイブ（バックエンド実装済み）
- [x] ユーザアップロードファイルのアーカイブ（バックエンド実装済み）

#### アーカイブ復元機能
- [x] S3からのアーカイブ取得（バックエンド実装済み）
- [x] フォームと回答データの復元（バックエンド実装済み）
- [x] 添付ファイルの復元（バックエンド実装済み）
- [x] フォームコードの重複処理（バックエンド実装済み）
- [x] 権限チェック（system_adminのみ）（バックエンド実装済み）
- [x] エラーハンドリング（存在しないアーカイブID、不正なデータ形式等）（バックエンド実装済み）

### ✅ フロントエンド: 実装済み（2026-01-23実装完了）

#### エクスポート/インポート/アーカイブUI
- [x] FormListPage: エクスポートボタン（実装済み、非同期処理・進捗表示対応）
- [x] FormListPage: インポートボタン（実装済み、非同期処理・進捗表示対応）
- [x] FormListPage: アーカイブボタン（実装済み、非同期処理・進捗表示対応）
- [x] FormArchiveListPage: アーカイブ一覧画面（実装済み）
- [x] FormArchiveListPage: 復元ボタン（実装済み、非同期処理・進捗表示対応）
- [x] FormArchiveListPage: 削除ボタン（実装済み、rootのみ表示、ID確認付き）
- [x] サイドメニュー: フォームアーカイブ一覧をフォーム一覧の下に追加（実装済み）
- [x] ルーティング・画面仕様書: FORM_ARCHIVE_LIST画面の定義が追加済み

---

## 参考情報

### 既存の類似機能
- **CSVエクスポート/インポート**: `FormsFieldsController@exportFields`, `FormsFieldsController@importCsv`
- **PDFストレージ**: `PdfStorageService`（S3対応）
- **ジョブキュー**: `ProgressJob`（非同期処理）

### 関連ドキュメント
- `SUPP-FORM-STEP-001-spec.md`: フォームSTEP構造の仕様
- `VALIDATION_RULES_STATUS.md`: バリデーションルールの仕様
- `FORM_STORAGE_MIGRATION_TO_S3_TASKS.md`: ストレージS3移行・非同期処理対応の実装タスク
