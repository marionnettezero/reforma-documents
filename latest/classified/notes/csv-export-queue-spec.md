# CSVエクスポートのジョブキュー対応仕様

## 現状

### 実装状況
- ✅ `ResponsesExportController::startCsv()`: CSVエクスポート開始API
- ✅ `CsvExportService::generate()`: CSV生成ロジック
- ✅ `ProgressJob`モデル: 進捗管理
- ❌ **現在は同期処理**（コントローラー内で直接CSV生成）

### 問題点
- 大量データのエクスポート時にリクエストタイムアウトの可能性
- 長時間処理でWebサーバーのリソースを占有
- ユーザーは処理完了まで待機する必要がある

---

## ジョブキュー対応のメリット

### 1. 非同期処理
- リクエストは即座に返却（`job_id`を返す）
- バックグラウンドでCSV生成を実行
- タイムアウトの心配がない

### 2. リソース管理
- Webサーバーのリソースを占有しない
- 専用ワーカーで処理（`exports`キュー）
- メモリリーク対策（`--max-jobs`, `--max-time`）

### 3. スケーラビリティ
- 複数のワーカーで並行処理可能
- 大量のエクスポートリクエストに対応

---

## 実装方針

### 1. ジョブクラスの作成

**ファイル**: `app/Jobs/ExportCsvJob.php`

```php
<?php

namespace App\Jobs;

use App\Models\ProgressJob;
use App\Services\CsvExportService;
use App\Services\SettingsService;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Storage;
use Carbon\CarbonImmutable;

class ExportCsvJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    /**
     * ジョブのタイムアウト時間（秒）
     */
    public int $timeout = 600; // 10分（大量データに対応）

    /**
     * ジョブの試行回数
     */
    public int $tries = 2; // CSVエクスポートは再試行不要（失敗時は手動再実行）

    /**
     * 処理するキュー名
     */
    public string $queue = 'exports';

    /**
     * @param string $jobId 進捗ジョブID
     * @param string $mode エクスポートモード（value/label/both）
     * @param int|null $formId フォームID（nullの場合は全フォーム）
     */
    public function __construct(
        private string $jobId,
        private string $mode,
        private ?int $formId = null
    ) {
    }

    public function handle(
        CsvExportService $csvExportService,
        SettingsService $settingsService
    ): void {
        $job = ProgressJob::query()->find($this->jobId);
        
        if (!$job) {
            \Log::error('ProgressJob not found', ['job_id' => $this->jobId]);
            return;
        }

        try {
            // 進捗更新: キューに投入された状態（コントローラーで設定済み）
            // status: queued, percent: 0

            // 進捗更新: 準備中
            $job->status = 'running';
            $job->percent = 0;
            $job->message = 'messages.csv_export_preparing';
            $job->save();

            // 送信データを取得
            $query = \App\Models\Submission::with(['form.fields', 'values']);
            if ($this->formId) {
                $query->where('form_id', $this->formId);
            }
            $submissions = $query->orderBy('created_at', 'desc')->get();

            // 進捗更新: データ取得完了
            $job->percent = 30;
            $job->message = 'messages.csv_export_data_loaded';
            $job->save();

            // CSV生成
            $job->percent = 50;
            $job->message = 'messages.csv_export_generating';
            $job->save();

            $csv = $csvExportService->generate($submissions, $this->mode);
            
            // 進捗更新: CSV生成完了
            $job->percent = 80;
            $job->message = 'messages.csv_export_saving';
            $job->save();

            // ファイル保存
            $path = sprintf('exports/%s_responses.csv', $this->jobId);
            Storage::disk('local')->put($path, $csv);

            // 進捗更新: 完了
            $jobTtl = (int) $settingsService->getInt('progress.job_ttl_seconds', 86400);
            $downloadTtl = (int) $settingsService->getInt('export.download_url_ttl_seconds', 3600);

            $job->status = 'succeeded';
            $job->percent = 100;
            $job->message = 'messages.csv_export_completed';
            $job->result_path = $path;
            $job->download_expires_at = CarbonImmutable::now()->addSeconds($downloadTtl);
            $job->expires_at = CarbonImmutable::now()->addSeconds($jobTtl);
            $job->save();
        } catch (\Exception $e) {
            \Log::error('CSV export job failed', [
                'job_id' => $this->jobId,
                'error' => $e->getMessage(),
                'trace' => $e->getTraceAsString(),
            ]);

            $job->status = 'failed';
            $job->message = 'messages.csv_export_failed';
            $job->save();
            
            throw $e; // ジョブを失敗としてマーク
        }
    }
}
```

### 2. コントローラーの修正

**ファイル**: `app/Http/Controllers/Api/V1/ResponsesExportController.php`

```php
public function startCsv(Request $request): JsonResponse
{
    // バリデーション
    $validated = $request->validate([
        'mode' => ['nullable', 'string', 'in:value,label,both'],
        'form_id' => ['nullable', 'integer', 'exists:forms,id'],
    ]);

    $mode = $validated['mode'] ?? 'value';
    $formId = $validated['form_id'] ?? null;

    $jobId = (string) Str::uuid();

    // 進捗ジョブを作成（queued状態）
    $job = ProgressJob::query()->create([
        'job_id' => $jobId,
        'type' => 'responses_csv_export',
        'status' => 'queued', // キューに投入された状態
        'percent' => 0,
        'message' => 'messages.csv_export_queued'
    ]);

    // ジョブをキューに投入
    \App\Jobs\ExportCsvJob::dispatch($jobId, $mode, $formId);

    return ApiResponse::success($request, [
        'job' => [
            'job_id' => $jobId,
        ],
    ], null);
}
```

### 3. キュー構成の更新

| キュー名 | 用途 | ワーカー数 | 優先度 |
|---------|------|-----------|--------|
| `default` | 汎用ジョブ | 1-2 | 中 |
| `notifications` | メール通知 | 1-2 | 高（即時性重視） |
| `pdfs` | PDF生成 | 1 | 低（重い処理） |
| `exports` | CSVエクスポート | 1 | 低（重い処理） |

### 4. systemdサービスの追加

```bash
# CSVエクスポートキュー用ワーカー
sudo systemctl enable reforma-queue-worker@exports.service
sudo systemctl start reforma-queue-worker@exports.service
```

---

## 処理フロー

### 修正前（同期処理）

```
1. ユーザーがCSVエクスポートをリクエスト
   ↓
2. ResponsesExportController::startCsv() が実行
   ↓
3. データ取得 + CSV生成（同期処理、時間がかかる）
   ↓
4. ファイル保存
   ↓
5. レスポンス返却（完了まで待機）
```

### 修正後（非同期処理）

```
1. ユーザーがCSVエクスポートをリクエスト
   ↓
2. ResponsesExportController::startCsv() が実行
   ↓
3. ProgressJobを作成（status: queued）
   ↓
4. ExportCsvJobをキューに投入
   ↓
5. 即座にレスポンス返却（job_idを含む）
   ↓
6. reforma-queue-worker@exports がジョブを処理
   ↓
7. CSV生成 + ファイル保存
   ↓
8. ProgressJobを更新（status: succeeded）
   ↓
9. ユーザーは GET /v1/progress/{job_id} で進捗確認
   ↓
10. 完了後、GET /v1/exports/{job_id}/download でダウンロード
```

---

## 実装タスク

### バックエンド側
- [ ] `ExportCsvJob`ジョブクラスの作成
- [ ] `ResponsesExportController::startCsv()`の修正（ジョブ投入に変更）
- [ ] 翻訳メッセージの追加:
  - `csv_export_queued`: キューに投入されました
  - `csv_export_preparing`: 準備中...
  - `csv_export_data_loaded`: データ取得完了
  - `csv_export_generating`: CSV生成中...
  - `csv_export_saving`: ファイル保存中...
  - `csv_export_completed`: エクスポート完了
  - `csv_export_failed`: エクスポート失敗
- [ ] systemdサービスファイルの更新（`exports`キュー対応）
- [ ] README.mdの更新（exportsキュー用ワーカーの起動方法）
- [ ] CHANGELOG.mdの更新

### テスト
- [ ] CSVエクスポートジョブのテスト
- [ ] 進捗管理のテスト
- [ ] エラーハンドリングのテスト

---

## 注意事項

### 1. タイムアウト設定
- ジョブのタイムアウト: 600秒（10分）
- 大量データの場合は、必要に応じて調整

### 2. 再試行ポリシー
- 試行回数: 2回（失敗時は手動再実行を推奨）
- CSVエクスポートは再試行しても同じ結果になる可能性が高い

### 3. メモリ使用量
- 大量データの場合は、チャンク処理を検討
- 現在の実装は全データをメモリに読み込むため、メモリ不足に注意

### 4. 進捗管理
- `status`: `queued` → `running` → `succeeded` / `failed`
- `percent`: 0 → 30 → 50 → 80 → 100（段階的に更新）
- ユーザーは `GET /v1/progress/{job_id}` で進捗を確認可能
- フロントエンドは定期的にポーリングして進捗を表示

**進捗の段階**:
1. `queued` (0%): キューに投入された状態
2. `running` (0%): 準備中
3. `running` (30%): データ取得完了
4. `running` (50%): CSV生成中
5. `running` (80%): ファイル保存中
6. `succeeded` (100%): 完了（ダウンロードURLが利用可能）
7. `failed` (0%): 失敗

---

## 参考

- [Laravel Queue Documentation](https://laravel.com/docs/12.x/queues)
- `queue-worker-systemd-spec.md`（キューワーカー管理仕様）
- `queue-worker-operation-flow.md`（動作イメージ）
