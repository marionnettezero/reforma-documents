# バックエンド共通化リファクタリング タスク

## 概要

本ドキュメントは、バックエンド側で共通化できそうな処理を整理し、リファクタリングタスクを提示したものです。

**目的**: コードの重複を削減し、保守性と再利用性を向上させる

---

## 現状確認

### 1. アーカイブダウンロード処理の重複

#### 現状
- `FormsController@downloadArchive` と `LogsController@downloadArchive` でほぼ同一の処理が重複
- 権限チェック、S3署名付きURL生成、エラーハンドリングが同じパターン

#### 重複箇所
- 権限チェック（system_admin以上）
- S3ディスク取得
- ファイル存在確認
- 署名付きURL生成（60分有効）
- エラーレスポンス

---

### 2. CSVエクスポート処理の重複

#### 現状
- `LogExportJob` と `ThemeExportJob` でCSV生成処理が重複
- `LogExportJob` はインライン実装、`ThemeExportJob` は `escapeCsvLine` メソッドを使用
- CSVエスケープ処理の実装が異なる

#### 重複箇所
- CSV行のエスケープ処理（RFC4180準拠）
- UTF-8 BOMの付与（ThemeExportJobのみ）
- ファイル保存処理
- ダウンロードURL生成
- 進捗ジョブの完了処理

#### 既存サービス
- `CsvExportService` が存在するが、主に回答データのCSVエクスポート用

---

### 3. CSVインポート処理の重複

#### 現状
- `ThemeImportJob` でCSV解析処理が実装されている
- 他のCSVインポート処理（`CsvImportService`）との共通化可能性

#### 重複箇所
- CSV解析処理
- UTF-8 BOM除去
- 行データのパース

#### 既存サービス
- `CsvImportService` が存在するが、主にフォーム項目のCSVインポート用

---

### 4. エクスポートジョブの共通パターン

#### 現状
- `FormExportJob`, `LogExportJob`, `ThemeExportJob` で共通パターンが存在
- 進捗管理、ファイル保存、ダウンロードURL生成が同じパターン

#### 共通パターン
- ProgressJobの取得・検証
- 進捗更新（0% → 30% → 80% → 100%）
- ファイル保存（`exports/{job_id}_{type}.csv`）
- ダウンロードURL生成
- TTL設定（`progress.job_ttl_seconds`, `export.download_url_ttl_seconds`）
- エラーハンドリング

---

### 5. インポートジョブの共通パターン

#### 現状
- `FormImportJob`, `ThemeImportJob` で共通パターンが存在
- 進捗管理、ファイル検証、トランザクション処理が同じパターン

#### 共通パターン
- ProgressJobの取得・検証
- 一時ファイルの存在確認
- 進捗更新（0% → 20% → 40% → 60% → 80% → 100%）
- ファイル読み込み・解析
- データ検証
- トランザクション管理
- エラーハンドリング

---

### 6. 権限チェック処理の重複

#### 現状
- 複数のコントローラーで同じ権限チェックパターンが繰り返されている
- `system_admin以上` のチェックが多数箇所で重複

#### 重複パターン
```php
$user = auth()->user();
if (!$user) {
    throw new AuthorizationException('認証が必要です');
}
if (!$user->hasRole(RoleCode::SYSTEM_ADMIN) && !$user->is_root) {
    throw new AuthorizationException('この操作を実行する権限がありません（system_admin以上）');
}
```

#### 重複箇所
- `FormsController@downloadArchive`
- `LogsController@downloadArchive`
- `FormsController@archives`
- `LogsController@archives`
- その他多数

---

### 7. ProgressJob作成処理の重複

#### 現状
- 複数のコントローラーで `ProgressJob::create` が同じパターンで使用されている

#### 共通パターン
```php
$jobId = Str::uuid()->toString();
$progressJob = ProgressJob::create([
    'job_id' => $jobId,
    'type' => 'xxx_export', // または 'xxx_import'
    'status' => 'pending',
    'percent' => 0,
    'message' => 'messages.xxx_started',
]);
```

#### 重複箇所
- `FormsController` (複数箇所)
- `LogsController` (複数箇所)
- `ThemesController` (複数箇所)

---

## タスク1: アーカイブダウンロード処理の共通化

### 1.1 サービスクラスの作成

#### 1.1.1 ファイル作成
- **ファイル**: `app/Services/ArchiveDownloadService.php`（新規作成）
- **責務**: アーカイブファイルのダウンロードURL生成

#### 1.1.2 実装内容
- `downloadUrl(string $archivePath, int $expirationMinutes = 60): string` メソッド
- S3ディスク取得
- ファイル存在確認
- 署名付きURL生成
- エラーハンドリング

#### 1.1.3 実装ファイル
- `app/Services/ArchiveDownloadService.php`（新規作成）

---

### 1.2 コントローラーのリファクタリング

#### 1.2.1 FormsController@downloadArchive
- `ArchiveDownloadService` を使用するように変更
- 権限チェックはトレイトまたはミドルウェアで共通化（タスク6参照）

#### 1.2.2 LogsController@downloadArchive
- `ArchiveDownloadService` を使用するように変更
- 権限チェックはトレイトまたはミドルウェアで共通化（タスク6参照）

#### 1.2.3 実装ファイル
- `app/Http/Controllers/Api/V1/FormsController.php`（修正）
- `app/Http/Controllers/Api/V1/LogsController.php`（修正）

---

## タスク2: CSVエクスポート処理の共通化

### 2.1 CSVエスケープ処理の共通化

#### 2.1.1 サービスクラスの拡張または新規作成
- **オプション1**: `CsvExportService` を拡張
- **オプション2**: `app/Services/CsvHelperService.php`（新規作成）

#### 2.1.2 実装内容
- `escapeCsvLine(array $row, bool $includeBom = false): string` メソッド
- RFC4180準拠のエスケープ処理
- UTF-8 BOM付与オプション

#### 2.1.3 実装ファイル
- `app/Services/CsvExportService.php`（拡張）または `app/Services/CsvHelperService.php`（新規作成）

---

### 2.2 エクスポートジョブの基底クラス作成

#### 2.2.1 基底クラス作成
- **ファイル**: `app/Jobs/BaseExportJob.php`（新規作成、抽象クラス）
- **責務**: エクスポートジョブの共通処理

#### 2.2.2 共通メソッド
- `updateProgress(int $percent, string $message): void` - 進捗更新
- `saveExportFile(string $content, string $filename): string` - ファイル保存
- `completeJob(string $path): void` - ジョブ完了処理
- `failJob(string $message): void` - ジョブ失敗処理

#### 2.2.3 抽象メソッド
- `abstract protected function export(): string` - エクスポート処理（各ジョブで実装）

#### 2.2.4 実装ファイル
- `app/Jobs/BaseExportJob.php`（新規作成）
- `app/Jobs/LogExportJob.php`（修正）
- `app/Jobs/ThemeExportJob.php`（修正）

---

## タスク3: CSVインポート処理の共通化

### 3.1 CSV解析処理の共通化

#### 3.1.1 サービスクラスの拡張または新規作成
- **オプション1**: `CsvImportService` を拡張
- **オプション2**: `app/Services/CsvHelperService.php`（新規作成）

#### 3.1.2 実装内容
- `parseCsv(string $csvContent, bool $removeBom = true): array` メソッド
- UTF-8 BOM除去
- CSV行のパース
- エラーハンドリング

#### 3.1.3 実装ファイル
- `app/Services/CsvImportService.php`（拡張）または `app/Services/CsvHelperService.php`（新規作成）

---

### 3.2 インポートジョブの基底クラス作成

#### 3.2.1 基底クラス作成
- **ファイル**: `app/Jobs/BaseImportJob.php`（新規作成、抽象クラス）
- **責務**: インポートジョブの共通処理

#### 3.2.2 共通メソッド
- `updateProgress(int $percent, string $message): void` - 進捗更新
- `validateTempFile(string $tempPath): void` - 一時ファイル検証
- `readTempFile(string $tempPath): string` - 一時ファイル読み込み
- `completeJob(array $resultData): void` - ジョブ完了処理
- `failJob(string $message, array $errors = []): void` - ジョブ失敗処理

#### 3.2.3 抽象メソッド
- `abstract protected function import(string $fileContent): array` - インポート処理（各ジョブで実装）

#### 3.2.4 実装ファイル
- `app/Jobs/BaseImportJob.php`（新規作成）
- `app/Jobs/ThemeImportJob.php`（修正）

---

## タスク4: 権限チェック処理の共通化

### 4.1 トレイトまたはミドルウェアの作成

#### 4.1.1 オプション1: トレイト作成
- **ファイル**: `app/Http/Controllers/Concerns/RequiresSystemAdmin.php`（新規作成）
- **責務**: system_admin以上の権限チェック

#### 4.1.2 オプション2: ミドルウェア作成
- **ファイル**: `app/Http/Middleware/RequireSystemAdmin.php`（新規作成）
- **責務**: system_admin以上の権限チェック

#### 4.1.3 実装内容
- 認証チェック
- system_adminまたはis_rootチェック
- エラーレスポンス

#### 4.1.4 推奨
- **トレイト**: コントローラーメソッド単位で柔軟に適用可能
- **ミドルウェア**: ルート単位で一括適用可能

#### 4.1.5 実装ファイル
- `app/Http/Controllers/Concerns/RequiresSystemAdmin.php`（新規作成、推奨）
- または `app/Http/Middleware/RequireSystemAdmin.php`（新規作成）

---

### 4.2 コントローラーのリファクタリング

#### 4.2.1 適用対象
- `FormsController@downloadArchive`
- `FormsController@archives`
- `LogsController@downloadArchive`
- `LogsController@archives`
- `LogsController@archive`
- その他該当箇所

#### 4.2.2 実装ファイル
- 各コントローラーファイル（修正）

---

## タスク5: ProgressJob作成処理の共通化

### 5.1 ヘルパーメソッドまたはサービスの作成

#### 5.1.1 オプション1: コントローラーベースクラスの拡張
- **ファイル**: `app/Http/Controllers/Controller.php`（既存ファイルに追加）
- **メソッド**: `createProgressJob(string $type, string $startMessage): string`

#### 5.1.2 オプション2: サービスクラスの作成
- **ファイル**: `app/Services/ProgressJobService.php`（新規作成）
- **メソッド**: `create(string $type, string $startMessage): string`

#### 5.1.3 実装内容
- UUID生成
- ProgressJob作成
- job_id返却

#### 5.1.4 実装ファイル
- `app/Http/Controllers/Controller.php`（拡張）または `app/Services/ProgressJobService.php`（新規作成）

---

### 5.2 コントローラーのリファクタリング

#### 5.2.1 適用対象
- `FormsController` (複数箇所)
- `LogsController` (複数箇所)
- `ThemesController` (複数箇所)

#### 5.2.2 実装ファイル
- 各コントローラーファイル（修正）

---

## タスク6: エラーハンドリングの共通化

### 6.1 ジョブエラーハンドリングの共通化

#### 6.1.1 基底クラスでの実装
- `BaseExportJob` と `BaseImportJob` で共通のエラーハンドリング
- try-catchブロックの共通化
- ログ出力の統一

#### 6.1.2 実装ファイル
- `app/Jobs/BaseExportJob.php`（新規作成）
- `app/Jobs/BaseImportJob.php`（新規作成）

---

## 実装順序の推奨

### Phase 1: 低リスク・高効果
1. **タスク1**: アーカイブダウンロード処理の共通化（影響範囲が限定的）
2. **タスク4**: 権限チェック処理の共通化（多数箇所で使用、影響大）

### Phase 2: 中リスク・中効果
3. **タスク5**: ProgressJob作成処理の共通化（影響範囲が限定的）
4. **タスク2**: CSVエクスポート処理の共通化（既存サービス拡張）

### Phase 3: 高リスク・高効果
5. **タスク3**: CSVインポート処理の共通化（既存サービス拡張）
6. **タスク2.2**: エクスポートジョブの基底クラス作成（大規模リファクタリング）
7. **タスク3.2**: インポートジョブの基底クラス作成（大規模リファクタリング）

---

## 技術的な考慮事項

### 後方互換性
- 既存のAPIエンドポイントの動作は変更しない
- 既存のジョブ処理の動作は変更しない
- 段階的なリファクタリングを推奨

### テスト
- 各リファクタリング後に既存のテストが通ることを確認
- 新規作成するサービスクラスのユニットテストを追加

### パフォーマンス
- 共通化によるオーバーヘッドは最小限に
- 既存のパフォーマンス特性を維持

---

## 関連ファイル一覧

### 新規作成
- `app/Services/ArchiveDownloadService.php`
- `app/Http/Controllers/Concerns/RequiresSystemAdmin.php`（またはミドルウェア）
- `app/Services/CsvHelperService.php`（または既存サービスの拡張）
- `app/Jobs/BaseExportJob.php`
- `app/Jobs/BaseImportJob.php`
- `app/Services/ProgressJobService.php`（オプション）

### 修正
- `app/Http/Controllers/Api/V1/FormsController.php`
- `app/Http/Controllers/Api/V1/LogsController.php`
- `app/Jobs/LogExportJob.php`
- `app/Jobs/ThemeExportJob.php`
- `app/Jobs/ThemeImportJob.php`
- `app/Services/CsvExportService.php`（拡張の場合）
- `app/Services/CsvImportService.php`（拡張の場合）

---

## 実装状況

### Phase 1: 低リスク・高効果 ✅ 完了
- ✅ **タスク1**: アーカイブダウンロード処理の共通化
  - `ArchiveDownloadService` 作成済み
  - `FormsController`, `LogsController` で使用中
- ✅ **タスク4**: 権限チェック処理の共通化
  - `RequiresSystemAdmin` トレイト作成済み
  - 各コントローラーで使用中

### Phase 2: 中リスク・中効果 ✅ 完了
- ✅ **タスク5**: ProgressJob作成処理の共通化
  - `Controller::createProgressJob()` メソッド追加済み
  - 各コントローラーで使用中
- ✅ **タスク2**: CSVエクスポート処理の共通化
  - `CsvExportService::escapeCsvLine()` 拡張済み
  - `BaseExportJob` 基底クラス作成済み
  - `LogExportJob`, `ThemeExportJob` で使用中

### Phase 3: 高リスク・高効果 ✅ 完了
- ✅ **タスク3**: CSVインポート処理の共通化
  - `CsvImportService::parseCsv()` 拡張済み
  - `BaseImportJob` 基底クラス作成済み
  - `ThemeImportJob` で使用中
- ✅ **タスク2.2**: エクスポートジョブの基底クラス作成
  - `BaseExportJob` 作成済み
- ✅ **タスク3.2**: インポートジョブの基底クラス作成
  - `BaseImportJob` 作成済み

**すべてのタスクが完了しました。**

---

## 参考情報

### 既存のサービス
- `CsvExportService`: 回答データのCSVエクスポート用
- `CsvImportService`: フォーム項目のCSVインポート用
- `PdfStorageService`: PDFファイルのストレージ管理
- `LogoStorageService`: ロゴファイルのストレージ管理

### 既存のパターン
- トレイト: `app/Http/Controllers/Concerns/` ディレクトリに既存のトレイトがあるか確認
- ミドルウェア: `app/Http/Middleware/` ディレクトリに既存のミドルウェアがあるか確認
