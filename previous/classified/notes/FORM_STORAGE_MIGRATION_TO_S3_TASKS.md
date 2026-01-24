# フォームストレージS3移行・非同期処理対応 実装タスク

## 概要

本ドキュメントは、以下の機能を実装するためのタスクを整理したものです：

1. **フォームロゴのS3移行**: フォームのロゴ画像をローカルディスクからS3に移行
2. **公開フォームファイルアップロードのS3対応**: 公開フォームでのファイルアップロードをS3に保存
3. **全処理の非同期化**: エクスポート/インポート/アーカイブ処理をジョブキューで非同期処理

---

## 現状確認

### フォームロゴの保存

#### 現在の実装
- **コントローラ**: `app/Http/Controllers/Api/V1/FormsController.php`
- **メソッド**: `uploadLogo()`, `deleteLogo()`
- **ストレージ**: `Storage::disk('public')` を使用
- **保存パス**: `forms/logos/{form_id}/logo.{ext}`
- **処理方式**: 同期処理（即座に保存）

#### コード箇所
```php
// FormsController@uploadLogo (line 752-802)
$logoPath = $file->storeAs(
    "forms/logos/{$form->id}",
    'logo.' . $file->getClientOriginalExtension(),
    'public'
);
$logoUrl = Storage::disk('public')->url($logoPath);
```

### 公開フォームでのファイルアップロード

#### 現在の実装
- **コントローラ**: `app/Http/Controllers/Api/V1/PublicFormsController.php`
- **メソッド**: `submit()`
- **処理**: 回答データの保存のみ（ファイルアップロードフィールドの処理は未確認）
- **推測**: ファイルアップロードフィールド（`type: 'file'`）の場合、ローカルディスクに保存されている可能性

#### 確認が必要な点
- ファイルアップロードフィールドの処理ロジック
- ファイルの保存先（ローカルディスク or S3）
- ファイルの保存方法（同期 or 非同期）

### 既存の非同期処理

#### ProcessFileUploadJob
- **用途**: PDFテンプレートと添付ファイルのアップロード
- **進捗管理**: `ProgressJob` を使用
- **ストレージ**: `PdfStorageService` を使用（S3対応済み）
- **キュー**: `uploads` キュー

#### 既存のジョブパターン
```php
// ジョブのディスパッチ
ProcessFileUploadJob::dispatch($jobId, $formId, $tempPaths, $uploadType, $originalFilenames, $locale);

// 進捗確認
ProgressJob::find($jobId);
```

### 既存のストレージサービス

#### PdfStorageService
- **用途**: PDFテンプレートと生成PDFのストレージ管理
- **対応**: S3とローカルストレージの切り替え対応
- **設定**: `config/reforma.php` の `pdf.storage_disk`（local or s3）
- **メソッド**: `disk()`, `storeTemplate()`, `storeAttachment()`, `url()`, `delete()`

#### ストレージ設定
- **設定ファイル**: `config/filesystems.php`
- **ディスク**: `public`（ローカル）、`s3`（S3）

---

## タスク1: フォームロゴのS3移行 ✅ 実装完了

### 1.1 ストレージサービスの拡張 ✅

#### 1.1.1 LogoStorageServiceの作成 ✅
- **ファイル**: `app/Services/LogoStorageService.php`（新規作成）
- **責務**: フォームロゴのストレージ管理（S3対応）
- **機能**:
  - S3とローカルストレージの切り替え対応
  - ロゴの保存、取得、削除、URL生成

#### 1.1.2 設定の追加 ✅
- **ファイル**: `config/reforma.php`
- **追加項目**:
  ```php
  'logo' => [
      'storage_disk' => env('REFORMA_LOGO_STORAGE_DISK', 's3'), // 'local' or 's3'
      'path' => env('REFORMA_LOGO_PATH', 'forms/logos'),
  ],
  ```

### 1.2 非同期処理の実装 ✅

#### 1.2.1 ロゴアップロードジョブの作成 ✅
- **ファイル**: `app/Jobs/ProcessLogoUploadJob.php`（新規作成）
- **責務**: ロゴアップロードの非同期処理
- **進捗管理**: `ProgressJob` を使用
- **処理フロー**:
  1. 一時ファイルの存在確認
  2. ファイル内容の読み込み
  3. S3へのアップロード（`LogoStorageService`を使用）
  4. 古いロゴの削除（存在する場合）
  5. フォームの`logo_path`を更新
  6. 進捗更新

#### 1.2.2 ロゴ削除ジョブの作成 ✅
- **ファイル**: `app/Jobs/ProcessLogoDeleteJob.php`（新規作成）
- **責務**: ロゴ削除の非同期処理
- **処理フロー**:
  1. S3からロゴファイルを削除
  2. フォームの`logo_path`をクリア
  3. 進捗更新

### 1.3 コントローラの修正 ✅

#### 1.3.1 FormsController@uploadLogoの修正 ✅
- **変更内容**:
  1. ファイルを一時保存（`Storage::disk('local')->putFile('temp', $file)`）
  2. `ProgressJob`を作成
  3. `ProcessLogoUploadJob`をディスパッチ
  4. ジョブIDを返却

#### 1.3.2 FormsController@deleteLogoの修正 ✅
- **変更内容**:
  1. `ProgressJob`を作成
  2. `ProcessLogoDeleteJob`をディスパッチ
  3. ジョブIDを返却

### 1.4 フロントエンドの修正 ✅

#### 1.4.1 ロゴアップロードUIの修正 ✅
- **ファイル**: `src/pages/forms/FormEditIntegratedPage.tsx`
- **変更内容**:
  1. アップロード後にジョブIDを取得
  2. 進捗ポーリングを開始
  3. 完了時にロゴURLを更新
  4. エラーハンドリング

---

## タスク2: 公開フォームファイルアップロードのS3対応 ✅ 実装完了

### 2.1 ファイルアップロード処理の確認 ✅

#### 2.1.1 現状調査 ✅
- **確認項目**:
  1. ファイルアップロードフィールド（`type: 'file'`）の処理ロジック
  2. ファイルの保存先（ローカルディスク or データベース）
  3. ファイルの保存方法（同期 or 非同期）

#### 2.1.2 調査対象
- `PublicFormsController@submit`
- `AnswerNormalizerService`（回答値の正規化）
- `FieldValidationService`（フィールドバリデーション）

### 2.2 ストレージサービスの拡張 ✅

#### 2.2.1 FormFileStorageServiceの作成 ✅
- **ファイル**: `app/Services/FormFileStorageService.php`（新規作成）
- **責務**: 公開フォームでのファイルアップロードのストレージ管理（S3対応）
- **機能**:
  - S3とローカルストレージの切り替え対応
  - ファイルの保存、取得、削除、URL生成
  - 一時ファイルの管理

#### 2.2.2 設定の追加 ✅
- **ファイル**: `config/reforma.php`
- **追加項目**:
  ```php
  'form_files' => [
      'storage_disk' => env('REFORMA_FORM_FILES_STORAGE_DISK', 's3'), // 'local' or 's3'
      'path' => env('REFORMA_FORM_FILES_PATH', 'form-files'),
      'temp_path' => env('REFORMA_FORM_FILES_TEMP_PATH', 'temp/form-files'),
  ],
  ```

### 2.3 非同期処理の実装

#### 2.3.1 ファイルアップロードジョブの作成
- **ファイル**: `app/Jobs/ProcessFormFileUploadJob.php`（新規作成）
- **責務**: 公開フォームでのファイルアップロードの非同期処理
- **進捗管理**: `ProgressJob` を使用（オプション、必要に応じて）
- **処理フロー**:
  1. 一時ファイルの存在確認
  2. ファイル内容の読み込み
  3. ファイルバリデーション（サイズ、形式等）
  4. S3へのアップロード（`FormFileStorageService`を使用）
  5. 一時ファイルの削除
  6. ファイルパスを返却

### 2.4 コントローラの修正 ✅

#### 2.4.1 PublicFormsController@submitの修正 ✅
- **変更内容**:
  1. ファイルアップロードフィールドの検出
  2. ファイルを一時保存
  3. `ProcessFormFileUploadJob`をディスパッチ（各ファイルごと）
  4. ジョブ完了を待機（または非同期で処理）
  5. ファイルパスを回答値に設定
  6. 回答データを保存

#### 2.4.2 注意事項
- ファイルアップロードが完了するまで回答データの保存を待機する必要がある場合、同期処理が必要
- または、ファイルアップロード完了後に回答データを更新する仕組みが必要

---

## タスク3: エクスポート/インポート/アーカイブ処理の非同期化

### 3.1 フォームエクスポートの非同期化

#### 3.1.1 エクスポートジョブの作成
- **ファイル**: `app/Jobs/FormExportJob.php`（新規作成）
- **責務**: フォームエクスポートの非同期処理
- **進捗管理**: `ProgressJob` を使用
- **処理フロー**:
  1. フォーム基本情報の取得
  2. 翻訳データの取得
  3. 項目データの取得
  4. 添付ファイルの取得
  5. JSON形式でデータを構築
  6. ZIPファイルとして圧縮（ファイルがある場合）
  7. S3またはローカルストレージに保存
  8. ダウンロードURLを生成
  9. 進捗更新

#### 3.1.2 コントローラの修正
- **ファイル**: `app/Http/Controllers/Api/V1/FormsController.php`
- **変更内容**:
  1. `export`メソッドで`ProgressJob`を作成
  2. `FormExportJob`をディスパッチ
  3. ジョブIDを返却

### 3.2 フォームインポートの非同期化

#### 3.2.1 インポートジョブの作成
- **ファイル**: `app/Jobs/FormImportJob.php`（新規作成）
- **責務**: フォームインポートの非同期処理
- **進捗管理**: `ProgressJob` を使用
- **処理フロー**:
  1. アップロードされたファイルの検証
  2. ZIPファイルの展開（ZIPファイルの場合）
  3. JSONデータの検証
  4. フォームコードの重複チェック
  5. テーマIDの存在チェック
  6. フォーム基本情報の作成
  7. 翻訳データの作成
  8. 項目データの作成
  9. 添付ファイルのコピー
  10. 進捗更新
  11. 作成されたフォームIDを返却

#### 3.2.2 コントローラの修正
- **ファイル**: `app/Http/Controllers/Api/V1/FormsController.php`
- **変更内容**:
  1. `import`メソッドでファイルを一時保存
  2. `ProgressJob`を作成
  3. `FormImportJob`をディスパッチ
  4. ジョブIDを返却

### 3.3 フォームアーカイブの非同期化

#### 3.3.1 アーカイブジョブの作成
- **ファイル**: `app/Jobs/FormArchiveJob.php`（新規作成）
- **責務**: フォームアーカイブの非同期処理
- **進捗管理**: `ProgressJob` を使用
- **処理フロー**:
  1. フォーム基本情報の取得
  2. 翻訳データの取得
  3. 項目データの取得
  4. 送信データの取得
  5. 送信値データの取得
  6. 添付ファイルの取得
  7. メタデータの作成
  8. ZIPファイルとして圧縮
  9. S3にアップロード
  10. 関連データの物理削除（トランザクション内で実行）
  11. テーブルのフラグメント解消
  12. アーカイブ情報をデータベースに記録
  13. 進捗更新

#### 3.3.2 コントローラの修正
- **ファイル**: `app/Http/Controllers/Api/V1/FormsController.php`
- **変更内容**:
  1. `archive`メソッドで`ProgressJob`を作成
  2. `FormArchiveJob`をディスパッチ
  3. ジョブIDを返却

### 3.4 アーカイブ復元の非同期化

#### 3.4.1 アーカイブ復元ジョブの作成
- **ファイル**: `app/Jobs/FormArchiveRestoreJob.php`（新規作成）
- **責務**: アーカイブ復元の非同期処理
- **進捗管理**: `ProgressJob` を使用
- **処理フロー**:
  1. アーカイブ情報の取得
  2. S3からアーカイブファイルをダウンロード
  3. ZIPファイルを展開
  4. JSONデータの検証
  5. フォームコードの重複チェック
  6. テーマIDの存在チェック
  7. フォーム基本情報の作成
  8. 翻訳データの作成
  9. 項目データの作成
  10. 送信データの作成
  11. 送信値データの作成
  12. 添付ファイルのコピー
  13. 進捗更新
  14. 復元されたフォームIDを返却

#### 3.4.2 コントローラの修正
- **ファイル**: `app/Http/Controllers/Api/V1/FormsController.php`
- **変更内容**:
  1. `restoreArchive`メソッドで`ProgressJob`を作成
  2. `FormArchiveRestoreJob`をディスパッチ
  3. ジョブIDを返却

---

## 実装順序の推奨

### Phase 1: フォームロゴのS3移行 ✅ 完了
1. ✅ 設定の追加（1.1.2）
2. ✅ LogoStorageServiceの作成（1.1.1）
3. ✅ ProcessLogoUploadJobの作成（1.2.1）
4. ✅ ProcessLogoDeleteJobの作成（1.2.2）
5. ✅ FormsControllerの修正（1.3）
6. ✅ フロントエンドの修正（1.4）

### Phase 2: 公開フォームファイルアップロードのS3対応 ✅ 完了
1. ✅ 現状調査（2.1）
2. ✅ 設定の追加（2.2.2）
3. ✅ FormFileStorageServiceの作成（2.2.1）
4. ✅ ProcessFormFileUploadJobの作成（2.3.1）
5. ✅ PublicFormsControllerの修正（2.4）
6. ✅ AnswerNormalizerServiceの修正（fileタイプの正規化）
7. ✅ FieldValidationServiceの修正（fileタイプのバリデーション）
8. ✅ PublicFormFieldコンポーネントの修正（fileタイプのUI実装）
9. ✅ PublicFormViewPageの修正（FormDataを使用したファイル送信）

### Phase 3: エクスポート/インポート/アーカイブ処理の非同期化 ✅ 完了
1. ✅ FormExportJobの作成（3.1.1）
2. ✅ FormsController@exportの修正（3.1.2）
3. ✅ FormImportJobの作成（3.2.1）
4. ✅ FormsController@importの修正（3.2.2）
5. ✅ FormArchiveJobの作成（3.3.1）
6. ✅ FormsController@archiveの修正（3.3.2）
7. ✅ FormArchiveRestoreJobの作成（3.4.1）
8. ✅ FormsController@restoreArchiveの修正（3.4.2）
9. ✅ form_archivesテーブルのマイグレーション作成
10. ✅ FormArchiveモデルの作成

---

## 技術的な考慮事項

### ファイルサイズ
- 大きなファイル（ロゴ、アップロードファイル）の場合、メモリ使用量に注意
- ストリーミング処理の検討

### パフォーマンス
- 非同期処理により、APIレスポンス時間が短縮される
- 進捗ポーリングの頻度を適切に設定（過度なポーリングを避ける）

### エラーハンドリング
- ジョブ失敗時のロールバック処理
- 一時ファイルのクリーンアップ
- 進捗ジョブの状態管理

### セキュリティ
- 一時ファイルへのアクセス制御
- S3の署名付きURLの有効期限設定
- ファイルアップロードのバリデーション強化

### データ整合性
- ファイルアップロード完了前の回答データ保存の制御
- トランザクション管理（アーカイブ処理等）

### 既存データの移行
- 既存のローカルディスクに保存されているロゴファイルのS3移行
- 既存のローカルディスクに保存されているアップロードファイルのS3移行
- 移行スクリプトの作成

---

## 関連ファイル一覧

### バックエンド（新規作成）
- ✅ `app/Services/LogoStorageService.php`
- ✅ `app/Services/FormFileStorageService.php`
- ✅ `app/Jobs/ProcessLogoUploadJob.php`
- ✅ `app/Jobs/ProcessLogoDeleteJob.php`
- ✅ `app/Jobs/ProcessFormFileUploadJob.php`
- ✅ `app/Jobs/FormExportJob.php`
- ✅ `app/Jobs/FormImportJob.php`
- ✅ `app/Jobs/FormArchiveJob.php`
- ✅ `app/Jobs/FormArchiveRestoreJob.php`
- ✅ `app/Models/FormArchive.php`
- ✅ `database/migrations/2026_01_23_100000_create_form_archives_table.php`

### バックエンド（修正）
- ✅ `app/Http/Controllers/Api/V1/FormsController.php`（ロゴアップロード/削除、エクスポート/インポート/アーカイブ/復元）
- ✅ `app/Http/Controllers/Api/V1/PublicFormsController.php`（ファイルアップロード処理）
- ✅ `app/Services/AnswerNormalizerService.php`（fileタイプの正規化）
- ✅ `app/Services/FieldValidationService.php`（fileタイプのバリデーション）
- ✅ `config/reforma.php`（logo, form_files設定）
- `config/filesystems.php`（必要に応じて）

### フロントエンド（修正）
- ✅ `src/pages/forms/FormEditIntegratedPage.tsx`（ロゴアップロードUI）
- ✅ `src/components/forms/PublicFormField.tsx`（fileタイプのUI実装）
- ✅ `src/pages/public/PublicFormViewPage.tsx`（FormDataを使用したファイル送信）
- `src/pages/forms/FormListPage.tsx`（エクスポート/インポート/アーカイブUI、未実装）

---

## テスト項目

### フォームロゴのS3移行
- [ ] ロゴアップロード（S3保存）
- [ ] ロゴ削除（S3削除）
- [ ] ロゴURL生成（署名付きURL）
- [ ] 非同期処理の進捗管理
- [ ] エラーハンドリング（アップロード失敗、削除失敗等）
- [ ] 既存ロゴのS3移行

### 公開フォームファイルアップロードのS3対応
- [ ] ファイルアップロード（S3保存）
- [ ] ファイルバリデーション
- [ ] ファイルURL生成（署名付きURL）
- [ ] 非同期処理の進捗管理
- [ ] エラーハンドリング（アップロード失敗等）
- [ ] 既存ファイルのS3移行

### エクスポート/インポート/アーカイブ処理の非同期化
- [ ] エクスポート処理の非同期化
- [ ] インポート処理の非同期化
- [ ] アーカイブ処理の非同期化
- [ ] アーカイブ復元処理の非同期化
- [ ] 進捗管理（ProgressJob）
- [ ] エラーハンドリング（ジョブ失敗等）

---

## 参考情報

### 既存の類似機能
- **ProcessFileUploadJob**: PDFテンプレートと添付ファイルのアップロード（非同期処理）
- **PdfStorageService**: PDFストレージ管理（S3対応）
- **ProgressJob**: 進捗管理

### 関連ドキュメント
- `FORM_EXPORT_IMPORT_ARCHIVE_TASKS.md`: エクスポート/インポート/アーカイブ機能の実装タスク
