# フォームアーカイブ修正・ログアーカイブ機能 実装タスク

## 概要

本ドキュメントは、以下の機能を実装するためのタスクを整理したものです：

1. **フォームアーカイブ機能の修正**: 生成PDFとユーザアップロードファイルを含める
2. **アーカイブ削除機能**: アーカイブの削除機能（rootのみ、id確認）
3. **ログ一覧エクスポート機能**: CSV形式でログデータをエクスポート
4. **ログ一覧アーカイブ機能**: ログデータをzip圧縮してS3に保存、物理削除

---

## 現状確認

### フォームアーカイブ機能

#### 現在の実装
- **ジョブ**: `app/Jobs/FormArchiveJob.php`
- **含まれるファイル**:
  - ✅ ロゴファイル（LogoStorageService経由）
  - ✅ PDFテンプレート（PdfStorageService経由）
  - ✅ 添付ファイル（PdfStorageService経由、フォームと翻訳データの両方）
  - ❌ **生成されたPDF（submissionごとに生成されるPDF）が含まれていない**
  - ❌ **ユーザがアップロードしたファイル（FormFileStorageServiceで保存されるファイル）が含まれていない**

#### 不足している点
1. **生成されたPDF**: `pdf-outputs/{submission_id}/submission_{submission_id}.pdf`
2. **ユーザアップロードファイル**: `form-files/{form_id}/{submission_id}/{field_key}/{filename}`

### アーカイブ削除機能

#### 現在の実装
- ❌ **未実装**

#### 必要な機能
- アーカイブの削除（S3から削除、データベースから削除）
- id値の確認（アカウント削除と同様）
- rootのみ削除可能
- 既にS3から削除されている場合のエラーハンドリング

### ログ一覧機能

#### 現在の実装
- **コントローラ**: `app/Http/Controllers/Api/V1/LogsController.php`
- **エンドポイント**: 
  - `GET /v1/logs` - ログ一覧
  - `GET /v1/logs/{id}` - ログ詳細
- **モデル**: `app/Models/AdminLog.php`
- **テーブル**: `admin_logs`
- **カラム**: `id`, `level`, `category`, `message`, `request_id`, `endpoint`, `reason`, `user_id`, `created_at`, `updated_at`

#### 不足している機能
- ❌ **エクスポート機能（CSV）**: 未実装
- ❌ **アーカイブ機能**: 未実装

### 権限管理

#### rootユーザーの確認方法
- `$user->is_root` で確認
- 例: `AdminUsersController@destroy`で使用

#### system_adminの確認方法
- `$user->hasRole(RoleCode::SYSTEM_ADMIN)` で確認

---

## タスク1: フォームアーカイブ機能の修正

### 1.1 FormArchiveJobの修正

#### 1.1.1 生成PDFの取得とアーカイブへの追加
- **ファイル**: `app/Jobs/FormArchiveJob.php`
- **修正箇所**: `buildArchiveData`メソッド
- **処理内容**:
  1. 各submissionごとに`PdfStorageService::outputPath($submissionId)`でPDFパスを取得
  2. `PdfStorageService::exists($pdfPath)`でPDFの存在確認
  3. PDFが存在する場合は`PdfStorageService::get($pdfPath)`で取得
  4. 一時ディレクトリに保存（`files/generated-pdfs/{submission_id}/submission_{submission_id}.pdf`）
  5. ファイル情報を`$files`配列に追加（`type: 'generated_pdf'`）

#### 1.1.2 ユーザアップロードファイルの取得とアーカイブへの追加
- **ファイル**: `app/Jobs/FormArchiveJob.php`
- **修正箇所**: `buildArchiveData`メソッド
- **処理内容**:
  1. `submission_values`から`type: 'file'`のフィールドを検出
  2. `value_json`からファイルパスを取得
  3. `FormFileStorageService::exists($filePath)`でファイルの存在確認
  4. ファイルが存在する場合は`FormFileStorageService::get($filePath)`で取得
  5. 一時ディレクトリに保存（`files/user-uploads/{submission_id}/{field_key}/{filename}`）
  6. ファイル情報を`$files`配列に追加（`type: 'user_uploaded_file'`）

#### 1.1.3 注意事項
- ファイルが存在しない場合のエラーハンドリング（警告ログを出力して続行）
- 大量のsubmissionがある場合のパフォーマンス考慮
- 進捗更新の適切なタイミング

---

## タスク2: アーカイブ削除機能

### 2.1 バックエンド: アーカイブ削除API実装

#### 2.1.1 エンドポイント追加
- **パス**: `DELETE /v1/forms/archives/{id}`
- **権限**: rootのみ（`$user->is_root`でチェック）
- **リクエスト**: 
  ```json
  {
    "id": 123  // アーカイブID（確認用）
  }
  ```

#### 2.1.2 実装内容
- **ファイル**: `app/Http/Controllers/Api/V1/FormsController.php`
- **メソッド**: `deleteArchive`
- **処理フロー**:
  1. root権限チェック（`$user->is_root`）
  2. リクエストから`id`を取得してバリデーション
  3. パスパラメータの`id`とリクエストボディの`id`が一致することを確認
  4. `FormArchive`を取得
  5. S3からアーカイブファイルを削除（既に削除されている場合は警告ログを出力して続行）
  6. データベースから`FormArchive`レコードを削除
  7. 成功レスポンスを返却

#### 2.1.3 エラーハンドリング
- S3から既に削除されている場合: 警告ログを出力してデータベースからは削除
- アーカイブが見つからない場合: 404エラー
- idが一致しない場合: 400エラー
- root権限がない場合: 403エラー

#### 2.1.4 実装ファイル
- `app/Http/Controllers/Api/V1/FormsController.php`に`deleteArchive`メソッドを追加

---

## タスク3: ログ一覧エクスポート機能

### 3.1 バックエンド: ログエクスポートAPI実装

#### 3.1.1 エンドポイント追加
- **パス**: `GET /v1/logs/export`
- **権限**: system_admin以上（`$user->hasRole(RoleCode::SYSTEM_ADMIN)`または`$user->is_root`）
- **クエリパラメータ**: 
  - `level` (optional): レベル（info/warn/error）
  - `q` (optional): キーワード検索
  - `date_from` (optional): 開始日
  - `date_to` (optional): 終了日

#### 3.1.2 実装内容
- **ファイル**: `app/Http/Controllers/Api/V1/LogsController.php`
- **メソッド**: `export`
- **処理フロー**:
  1. 権限チェック（system_admin以上）
  2. クエリパラメータでログをフィルタリング（既存の`index`メソッドと同様）
  3. CSV形式でデータを構築
  4. CSVファイルを生成
  5. レスポンスとして返却（Content-Type: text/csv）

#### 3.1.3 CSV形式
```csv
id,level,category,message,request_id,endpoint,reason,user_id,created_at
1,error,form,エラーが発生しました,xxx-xxx-xxx,/v1/forms,VALIDATION_FAILED,1,2024-01-01T00:00:00Z
```

#### 3.1.4 実装ファイル
- `app/Http/Controllers/Api/V1/LogsController.php`に`export`メソッドを追加

---

## タスク4: ログ一覧アーカイブ機能

### 4.1 バックエンド: ログアーカイブAPI実装

#### 4.1.1 エンドポイント追加
- **パス**: `POST /v1/logs/archive`
- **権限**: system_admin以上（`$user->hasRole(RoleCode::SYSTEM_ADMIN)`または`$user->is_root`）
- **リクエスト**: 
  ```json
  {
    "level": "error",  // optional
    "date_from": "2024-01-01",  // optional
    "date_to": "2024-12-31"  // optional
  }
  ```

#### 4.1.2 アーカイブジョブの作成
- **ファイル**: `app/Jobs/LogArchiveJob.php`（新規作成）
- **責務**: ログデータのアーカイブ処理
- **進捗管理**: `ProgressJob` を使用
- **処理フロー**:
  1. フィルタ条件でログデータを取得
  2. CSV形式でデータを構築
  3. メタデータの作成（アーカイブ日時、実行ユーザー情報、フィルタ条件等）
  4. ZIPファイルとして圧縮
  5. S3にアップロード（`archives/logs/archive-{timestamp}.zip`）
  6. ログデータの物理削除（トランザクション内で実行）
  7. テーブルのフラグメント解消（`OPTIMIZE TABLE admin_logs`）
  8. アーカイブ情報をデータベースに記録（`log_archives`テーブルに新規作成）
  9. 進捗更新

#### 4.1.3 データベーステーブル追加
- **テーブル**: `log_archives`
- **カラム**:
  - `id`: 主キー
  - `archive_path`: S3のアーカイブパス
  - `archive_size`: アーカイブファイルサイズ（バイト）
  - `archived_at`: アーカイブ日時
  - `archived_by`: アーカイブ実行ユーザーID
  - `filter_level`: フィルタ条件（レベル）
  - `filter_date_from`: フィルタ条件（開始日）
  - `filter_date_to`: フィルタ条件（終了日）
  - `log_count`: アーカイブされたログ数
  - `metadata_json`: メタデータ（JSON）
  - `created_at`, `updated_at`: タイムスタンプ

#### 4.1.4 マイグレーション
- **ファイル**: `database/migrations/YYYY_MM_DD_HHMMSS_create_log_archives_table.php`

#### 4.1.5 モデル作成
- **ファイル**: `app/Models/LogArchive.php`（新規作成）

#### 4.1.6 コントローラの修正
- **ファイル**: `app/Http/Controllers/Api/V1/LogsController.php`
- **メソッド**: `archive`
- **処理内容**:
  1. 権限チェック（system_admin以上）
  2. リクエストバリデーション
  3. `ProgressJob`を作成
  4. `LogArchiveJob`をディスパッチ
  5. ジョブIDを返却

### 4.2 バックエンド: ログアーカイブ削除API実装

#### 4.2.1 エンドポイント追加
- **パス**: `DELETE /v1/logs/archives/{id}`
- **権限**: rootのみ（`$user->is_root`でチェック）
- **リクエスト**: 
  ```json
  {
    "id": 123  // アーカイブID（確認用）
  }
  ```

#### 4.2.2 実装内容
- **ファイル**: `app/Http/Controllers/Api/V1/LogsController.php`
- **メソッド**: `deleteArchive`
- **処理フロー**:
  1. root権限チェック（`$user->is_root`）
  2. リクエストから`id`を取得してバリデーション
  3. パスパラメータの`id`とリクエストボディの`id`が一致することを確認
  4. `LogArchive`を取得
  5. S3からアーカイブファイルを削除（既に削除されている場合は警告ログを出力して続行）
  6. データベースから`LogArchive`レコードを削除
  7. 成功レスポンスを返却

#### 4.2.3 エラーハンドリング
- S3から既に削除されている場合: 警告ログを出力してデータベースからは削除
- アーカイブが見つからない場合: 404エラー
- idが一致しない場合: 400エラー
- root権限がない場合: 403エラー

---

## 実装順序の推奨

### Phase 1: フォームアーカイブ機能の修正
1. FormArchiveJobの修正（生成PDFの取得と追加）
2. FormArchiveJobの修正（ユーザアップロードファイルの取得と追加）

### Phase 2: アーカイブ削除機能
1. FormsController@deleteArchiveの実装
2. エラーハンドリングの実装

### Phase 3: ログ一覧エクスポート機能
1. LogsController@exportの実装
2. CSV生成処理の実装

### Phase 4: ログ一覧アーカイブ機能
1. log_archivesテーブルのマイグレーション作成
2. LogArchiveモデルの作成
3. LogArchiveJobの作成
4. LogsController@archiveの実装
5. LogsController@deleteArchiveの実装

---

## 技術的な考慮事項

### ファイルサイズ
- 大量のログデータの場合、CSVファイルのサイズが大きくなる可能性
- メモリ使用量に注意

### パフォーマンス
- 大量のログデータのアーカイブ処理は時間がかかる可能性
- 非同期処理（ジョブキュー）を使用
- 進捗管理（ProgressJob）を使用

### エラーハンドリング
- S3から既に削除されている場合の処理
- ジョブ失敗時のロールバック処理
- 一時ファイルのクリーンアップ

### セキュリティ
- root権限のチェック
- id値の確認（誤削除防止）

### データ整合性
- トランザクション管理（アーカイブ処理等）
- 物理削除後のテーブルフラグメント解消

---

## 関連ファイル一覧

### バックエンド（修正）
- `app/Jobs/FormArchiveJob.php`（生成PDFとユーザアップロードファイルの追加）
- `app/Http/Controllers/Api/V1/FormsController.php`（deleteArchiveメソッド追加）
- `app/Http/Controllers/Api/V1/LogsController.php`（export, archive, deleteArchiveメソッド追加）

### バックエンド（新規作成）
- `app/Jobs/LogArchiveJob.php`
- `app/Models/LogArchive.php`
- `database/migrations/YYYY_MM_DD_HHMMSS_create_log_archives_table.php`

---

## 実装状況（2026-01-23確認）

### ✅ バックエンド: 実装済み

#### タスク1: フォームアーカイブ機能の修正
- ✅ FormArchiveJob: 生成PDFとユーザアップロードファイルの処理が実装済み
  - `buildArchiveData`メソッドで生成PDF（`generated_pdf`）とユーザアップロードファイル（`user_uploaded_file`）を取得してアーカイブに含める処理が実装済み

#### タスク2: アーカイブ削除機能
- ✅ FormsController@deleteArchive: 実装済み
  - root権限チェック、id値の確認、S3からの削除、データベースからの削除が実装済み

#### タスク3: ログ一覧エクスポート機能
- ✅ LogsController@export: 実装済み
  - CSV形式でエクスポート、フィルタ条件の適用、権限チェックが実装済み

#### タスク4: ログ一覧アーカイブ機能
- ✅ LogArchiveJob: 実装済み
- ✅ LogArchiveモデル: 実装済み
- ✅ log_archivesテーブル: マイグレーション実装済み
- ✅ LogsController@archive: 実装済み
- ✅ LogsController@deleteArchive: 実装済み

### ✅ フロントエンド: 実装済み

#### フォーム関連UI
- ✅ FormListPage: エクスポート/インポート/アーカイブのボタンが実装済み
- ✅ FormArchiveListPage: アーカイブ一覧画面が実装済み（2026-01-23実装）
- ✅ サイドメニュー: フォームアーカイブ一覧をフォーム一覧の下に追加（2026-01-23実装）

#### ログ関連UI
- ✅ LogListPage: エクスポート/アーカイブのボタンが実装済み
- ✅ LogArchiveListPage: ログアーカイブ一覧画面が実装済み
- ✅ サイドメニュー: ログアーカイブ一覧をログ一覧の下に追加（2026-01-23実装）

#### バックエンドAPI
- ✅ LogsController@archives: ログアーカイブ一覧取得APIが実装済み
- ✅ FormsController@archives: フォームアーカイブ一覧取得APIが実装済み（2026-01-23実装）

## 実装完了項目（2026-01-23）

### バックエンド実装完了

1. ✅ **LogsController@archivesメソッドの実装**:
   - `GET /v1/logs/archives`エンドポイント
   - ページネーション対応
   - 日付範囲フィルタリング
   - 権限チェック（system_admin以上）

2. ✅ **FormsController@archivesメソッドの実装**:
   - `GET /v1/forms/archives`エンドポイント
   - ページネーション対応
   - 日付範囲フィルタリング
   - 権限チェック（system_admin以上）

### フロントエンドUI実装完了

1. ✅ **FormListPageへの追加**:
   - エクスポートボタン（form_admin / system_admin のみ表示）
   - インポートボタン（form_admin / system_admin のみ表示）
   - アーカイブボタン（system_admin のみ表示）

2. ✅ **FormArchiveListPageの作成**:
   - アーカイブ一覧の表示
   - 復元ボタン（system_admin のみ表示）
   - 削除ボタン（root のみ表示）
   - 日付範囲フィルタリング
   - ページネーション対応

3. ✅ **LogListPageへの追加**:
   - エクスポートボタン（system_admin のみ表示）
   - アーカイブボタン（system_admin のみ表示）

4. ✅ **LogArchiveListPageの作成**:
   - ログアーカイブ一覧の表示
   - 削除ボタン（root のみ表示）
   - 日付範囲フィルタリング
   - ページネーション対応

5. ✅ **ルーティング・画面仕様書の追加**:
   - `LOG_ARCHIVE_LIST`画面のルーティング追加
   - `FORM_ARCHIVE_LIST`画面のルーティング追加
   - 画面仕様書への追加

6. ✅ **サイドメニューへの追加**:
   - フォームアーカイブ一覧をフォーム一覧の下に追加
   - ログアーカイブ一覧をログ一覧の下に追加
   - system_admin以上のみ表示

## テスト項目

### フォームアーカイブ機能の修正
- [x] 生成PDFがアーカイブに含まれる（バックエンド実装済み）
- [x] ユーザアップロードファイルがアーカイブに含まれる（バックエンド実装済み）
- [x] ファイルが存在しない場合のエラーハンドリング（バックエンド実装済み）
- [x] 大量のsubmissionがある場合のパフォーマンス（バックエンド実装済み）

### アーカイブ削除機能
- [x] root権限チェック（バックエンド実装済み）
- [x] id値の確認（バックエンド実装済み）
- [x] S3からアーカイブファイルの削除（バックエンド実装済み）
- [x] データベースからアーカイブレコードの削除（バックエンド実装済み）
- [x] 既にS3から削除されている場合のエラーハンドリング（バックエンド実装済み）

### ログ一覧エクスポート機能
- [x] CSV形式でエクスポート（バックエンド実装済み）
- [x] フィルタ条件の適用（バックエンド実装済み）
- [x] 権限チェック（system_admin以上）（バックエンド実装済み）
- [x] エラーハンドリング（バックエンド実装済み）

### ログ一覧アーカイブ機能
- [x] ログデータのアーカイブ化（バックエンド実装済み）
- [x] S3へのアップロード（バックエンド実装済み）
- [x] 物理削除の実行（バックエンド実装済み）
- [x] テーブルのフラグメント解消（バックエンド実装済み）
- [x] アーカイブ情報の記録（バックエンド実装済み）
- [x] 権限チェック（system_admin以上）（バックエンド実装済み）
- [x] エラーハンドリング（バックエンド実装済み）

### ログアーカイブ削除機能
- [x] root権限チェック（バックエンド実装済み）
- [x] id値の確認（バックエンド実装済み）
- [x] S3からアーカイブファイルの削除（バックエンド実装済み）
- [x] データベースからアーカイブレコードの削除（バックエンド実装済み）
- [x] 既にS3から削除されている場合のエラーハンドリング（バックエンド実装済み）
