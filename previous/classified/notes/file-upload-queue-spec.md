# ファイルアップロード・CSVインポートのジョブキュー対応仕様

## 現状

### 実装済み（ファイルアップロード）
- ✅ `POST /v1/forms/{id}/attachment/pdf-template`: PDFテンプレートアップロード
- ✅ `POST /v1/forms/{id}/attachment/files`: 添付ファイルアップロード
- ❌ **現在は同期処理**（コントローラー内で直接処理）

### 未実装（CSVインポート）
- ❌ CSVインポート機能は未実装

---

## ジョブキュー対応の必要性

### ファイルアップロード

#### 対応が有効なケース
1. **大量ファイルの一括アップロード**
   - 複数ファイルを同時にアップロード
   - ファイル数が多い場合、処理に時間がかかる

2. **ファイル処理が必要な場合**
   - 画像リサイズ
   - ウイルススキャン
   - ファイル形式変換
   - メタデータ抽出

3. **ユーザー体験の向上**
   - 非同期処理でリクエストを即座に返却
   - 進捗表示が可能

#### 対応が不要なケース
- 単一ファイルのアップロード（軽量）
- 即座に結果が必要な場合
- ファイル処理が不要な場合

### CSVインポート

#### 対応が必須なケース
1. **大量データのインポート**
   - 数千件以上のデータをインポート
   - 処理に時間がかかる

2. **データ検証・変換処理**
   - CSVデータのバリデーション
   - データ形式の変換
   - 既存データとの整合性チェック

3. **エラーハンドリング**
   - 部分的な失敗の処理
   - エラーレポートの生成

---

## 実装方針

### 1. ファイルアップロードのジョブキュー対応（オプション）

#### 1.1 基本方針
- **軽量なアップロード**: 同期処理のまま（現在の実装）
- **大量ファイル・処理が必要**: ジョブキュー対応

#### 1.2 ジョブクラスの作成（将来実装）

**ファイル**: `app/Jobs/ProcessFileUploadJob.php`

```php
<?php

namespace App\Jobs;

use App\Models\ProgressJob;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Storage;

class ProcessFileUploadJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $timeout = 300;
    public int $tries = 2;
    public string $queue = 'uploads'; // または 'default'

    public function __construct(
        private string $jobId,
        private int $formId,
        private array $filePaths, // 一時保存されたファイルパス
        private string $uploadType // 'pdf_template' or 'attachments'
    ) {
    }

    public function handle(): void
    {
        $job = ProgressJob::query()->find($this->jobId);
        
        if (!$job) {
            \Log::error('ProgressJob not found', ['job_id' => $this->jobId]);
            return;
        }

        try {
            $job->status = 'running';
            $job->percent = 0;
            $job->message = 'messages.file_upload_processing';
            $job->save();

            $processedFiles = [];
            
            foreach ($this->filePaths as $index => $tempPath) {
                // ファイル処理（リサイズ、バリデーション等）
                // ...
                
                // 最終保存先に移動
                $finalPath = $this->moveToFinalLocation($tempPath, $this->formId);
                $processedFiles[] = $finalPath;

                // 進捗更新
                $job->percent = (int) (($index + 1) / count($this->filePaths) * 100);
                $job->save();
            }

            // フォームにファイル情報を保存
            $this->updateFormFiles($this->formId, $processedFiles, $this->uploadType);

            $job->status = 'succeeded';
            $job->percent = 100;
            $job->message = 'messages.file_upload_completed';
            $job->save();
        } catch (\Exception $e) {
            $job->status = 'failed';
            $job->message = 'messages.file_upload_failed';
            $job->save();
            throw $e;
        }
    }
}
```

#### 1.3 コントローラーの修正（将来実装）

```php
public function uploadAttachments(Request $request, int $id): JsonResponse
{
    // バリデーション
    $validated = $request->validate([
        'files' => ['required', 'array', 'min:1', 'max:10'],
        'files.*' => ['required', 'file', 'max:10240'],
        'async' => ['nullable', 'boolean'], // 非同期処理フラグ
    ]);

    $form = Form::findOrFail($id);

    // 非同期処理が有効な場合
    if ($validated['async'] ?? false) {
        $jobId = (string) Str::uuid();
        
        // 一時保存
        $tempPaths = [];
        foreach ($validated['files'] as $file) {
            $tempPath = Storage::disk('local')->putFile('temp', $file);
            $tempPaths[] = $tempPath;
        }

        // 進捗ジョブを作成
        $job = ProgressJob::query()->create([
            'job_id' => $jobId,
            'type' => 'file_upload',
            'status' => 'queued',
            'percent' => 0,
            'message' => 'messages.file_upload_queued'
        ]);

        // ジョブをキューに投入
        ProcessFileUploadJob::dispatch($jobId, $form->id, $tempPaths, 'attachments');

        return ApiResponse::success($request, [
            'job' => ['job_id' => $jobId],
        ], null);
    }

    // 同期処理（現在の実装）
    // ...
}
```

### 2. CSVインポートのジョブキュー対応（将来実装）

#### 2.1 ジョブクラスの作成

**ファイル**: `app/Jobs/ImportCsvJob.php`

```php
<?php

namespace App\Jobs;

use App\Models\ProgressJob;
use App\Services\CsvImportService;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Storage;

class ImportCsvJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $timeout = 1800; // 30分（大量データに対応）
    public int $tries = 1; // CSVインポートは再試行不要
    public string $queue = 'imports'; // または 'default'

    public function __construct(
        private string $jobId,
        private string $csvPath, // アップロードされたCSVファイルのパス
        private int $formId,
        private array $options = [] // インポートオプション
    ) {
    }

    public function handle(CsvImportService $csvImportService): void
    {
        $job = ProgressJob::query()->find($this->jobId);
        
        if (!$job) {
            \Log::error('ProgressJob not found', ['job_id' => $this->jobId]);
            return;
        }

        try {
            // 進捗更新: 準備中
            $job->status = 'running';
            $job->percent = 0;
            $job->message = 'messages.csv_import_preparing';
            $job->save();

            // CSVファイルを読み込み
            $csvContent = Storage::disk('local')->get($this->csvPath);
            
            // 進捗更新: データ読み込み完了
            $job->percent = 10;
            $job->message = 'messages.csv_import_reading';
            $job->save();

            // CSV解析
            $rows = $csvImportService->parse($csvContent);
            
            // 進捗更新: 解析完了
            $job->percent = 20;
            $job->message = 'messages.csv_import_validating';
            $job->save();

            // データ検証・変換
            $validatedData = $csvImportService->validate($rows, $this->formId);
            
            // 進捗更新: 検証完了
            $job->percent = 50;
            $job->message = 'messages.csv_import_importing';
            $job->save();

            // データインポート（チャンク処理）
            $totalRows = count($validatedData);
            $imported = 0;
            $errors = [];

            foreach ($validatedData as $index => $row) {
                try {
                    $csvImportService->importRow($row, $this->formId);
                    $imported++;
                } catch (\Exception $e) {
                    $errors[] = [
                        'row' => $index + 1,
                        'error' => $e->getMessage(),
                    ];
                }

                // 進捗更新（100行ごと）
                if (($index + 1) % 100 === 0) {
                    $job->percent = 50 + (int) (($index + 1) / $totalRows * 50);
                    $job->save();
                }
            }

            // 進捗更新: 完了
            $job->status = 'succeeded';
            $job->percent = 100;
            $job->message = 'messages.csv_import_completed';
            $job->result_data = [
                'imported' => $imported,
                'failed' => count($errors),
                'errors' => $errors,
            ];
            $job->save();
        } catch (\Exception $e) {
            $job->status = 'failed';
            $job->message = 'messages.csv_import_failed';
            $job->save();
            throw $e;
        }
    }
}
```

#### 2.2 コントローラーの作成（将来実装）

**ファイル**: `app/Http/Controllers/Api/V1/ResponsesImportController.php`

```php
<?php

namespace App\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use App\Models\Form;
use App\Models\ProgressJob;
use App\Support\ApiResponse;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;

class ResponsesImportController extends Controller
{
    public function startCsv(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'form_id' => ['required', 'integer', 'exists:forms,id'],
            'file' => ['required', 'file', 'mimes:csv,txt', 'max:10240'], // 10MB制限
        ]);

        $form = Form::findOrFail($validated['form_id']);

        // CSVファイルを一時保存
        $file = $validated['file'];
        $csvPath = Storage::disk('local')->putFile('imports', $file);

        $jobId = (string) Str::uuid();

        // 進捗ジョブを作成
        $job = ProgressJob::query()->create([
            'job_id' => $jobId,
            'type' => 'responses_csv_import',
            'status' => 'queued',
            'percent' => 0,
            'message' => 'messages.csv_import_queued'
        ]);

        // ジョブをキューに投入
        \App\Jobs\ImportCsvJob::dispatch($jobId, $csvPath, $form->id);

        return ApiResponse::success($request, [
            'job' => ['job_id' => $jobId],
        ], null);
    }
}
```

---

## キュー構成の更新

| キュー名 | 用途 | ワーカー数 | 優先度 |
|---------|------|-----------|--------|
| `default` | 汎用ジョブ | 1-2 | 中 |
| `notifications` | メール通知 | 1-2 | 高（即時性重視） |
| `pdfs` | PDF生成 | 1 | 低（重い処理） |
| `exports` | CSVエクスポート | 1 | 低（重い処理） |
| `imports` | CSVインポート | 1 | 低（重い処理、将来実装） |
| `uploads` | ファイルアップロード処理 | 1 | 低（オプション、将来実装） |

---

## 実装タスク

### ファイルアップロード（オプション）
- [ ] `ProcessFileUploadJob`ジョブクラスの作成（将来実装）
- [ ] コントローラーに非同期処理フラグを追加（将来実装）
- [ ] 進捗表示対応（将来実装）

### CSVインポート（将来実装）
- [ ] `CsvImportService`の作成
- [ ] `ImportCsvJob`ジョブクラスの作成
- [ ] `ResponsesImportController`の作成
- [ ] ルーティング追加（`POST /v1/responses/import/csv`）
- [ ] 翻訳メッセージの追加
- [ ] エラーレポート機能
- [ ] テスト実装

---

## まとめ

### ファイルアップロード
- **現状**: 同期処理で問題なし（軽量）
- **将来**: 大量ファイル・処理が必要な場合はジョブキュー対応を検討
- **優先度**: 低（オプション）

### CSVインポート
- **現状**: 未実装
- **将来**: 実装時はジョブキュー対応が必須
- **優先度**: 中（機能実装時に合わせて対応）

---

## 参考

- `csv-export-queue-spec.md`（CSVエクスポートのジョブキュー対応仕様）
- `queue-worker-systemd-spec.md`（キューワーカー管理仕様）
