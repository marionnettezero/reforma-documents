# CSVエクスポートのプログレス表示フロー

## 概要

CSVエクスポートをジョブキュー対応にすることで、**リアルタイムのプログレス表示**が可能になります。

## 処理フローと進捗更新

### 1. エクスポート開始

```
ユーザー: POST /v1/responses/export/csv
         ↓
コントローラー: ProgressJobを作成（status: queued, percent: 0）
         ↓
コントローラー: ExportCsvJobをキューに投入
         ↓
レスポンス: { "job_id": "xxx-xxx-xxx" }
```

**フロントエンド**: `job_id`を受け取り、進捗表示を開始

### 2. 進捗更新の段階

#### 段階1: キューに投入（0%）
```json
{
  "status": "queued",
  "percent": 0,
  "message": "messages.csv_export_queued"
}
```

#### 段階2: 準備中（0%）
```json
{
  "status": "running",
  "percent": 0,
  "message": "messages.csv_export_preparing"
}
```

#### 段階3: データ取得完了（30%）
```json
{
  "status": "running",
  "percent": 30,
  "message": "messages.csv_export_data_loaded"
}
```

#### 段階4: CSV生成中（50%）
```json
{
  "status": "running",
  "percent": 50,
  "message": "messages.csv_export_generating"
}
```

#### 段階5: ファイル保存中（80%）
```json
{
  "status": "running",
  "percent": 80,
  "message": "messages.csv_export_saving"
}
```

#### 段階6: 完了（100%）
```json
{
  "status": "succeeded",
  "percent": 100,
  "message": "messages.csv_export_completed",
  "download_url": "/v1/exports/xxx-xxx-xxx/download",
  "download_expires_at": "2026-01-17T10:30:00Z"
}
```

#### 段階7: 失敗（0%）
```json
{
  "status": "failed",
  "percent": 0,
  "message": "messages.csv_export_failed"
}
```

## フロントエンドの実装例

### 進捗表示コンポーネント

```typescript
import { useEffect, useState } from 'react';
import { apiGetJson } from '../utils/apiFetch';

interface ProgressJob {
  job_id: string;
  status: 'queued' | 'running' | 'succeeded' | 'failed';
  percent: number;
  message: string;
  download_url?: string;
  download_expires_at?: string;
}

export function CsvExportProgress({ jobId }: { jobId: string }) {
  const [progress, setProgress] = useState<ProgressJob | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!jobId) return;

    // 進捗をポーリング（2秒間隔）
    const interval = setInterval(async () => {
      try {
        const data = await apiGetJson<{ job: ProgressJob }>(`/v1/progress/${jobId}`);
        setProgress(data.job);

        // 完了または失敗したらポーリングを停止
        if (data.job.status === 'succeeded' || data.job.status === 'failed') {
          clearInterval(interval);
        }
      } catch (err) {
        setError('進捗の取得に失敗しました');
        clearInterval(interval);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [jobId]);

  if (!progress) {
    return <div>読み込み中...</div>;
  }

  if (progress.status === 'failed') {
    return (
      <div className="error">
        <p>エクスポートに失敗しました</p>
        <p>{progress.message}</p>
      </div>
    );
  }

  if (progress.status === 'succeeded') {
    return (
      <div className="success">
        <p>エクスポートが完了しました</p>
        <a href={progress.download_url} download>
          CSVをダウンロード
        </a>
        {progress.download_expires_at && (
          <p>有効期限: {new Date(progress.download_expires_at).toLocaleString()}</p>
        )}
      </div>
    );
  }

  return (
    <div className="progress">
      <div className="progress-bar">
        <div 
          className="progress-bar-fill" 
          style={{ width: `${progress.percent}%` }}
        />
      </div>
      <p>{progress.message}</p>
      <p>{progress.percent}%</p>
    </div>
  );
}
```

### 使用例

```typescript
function ExportButton() {
  const [jobId, setJobId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleExport = async () => {
    setLoading(true);
    try {
      const response = await apiPostJson<{ job: { job_id: string } }>(
        '/v1/responses/export/csv',
        { mode: 'both', form_id: 1 }
      );
      setJobId(response.job.job_id);
    } catch (err) {
      console.error('Export failed', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <button onClick={handleExport} disabled={loading}>
        CSVエクスポート
      </button>
      {jobId && <CsvExportProgress jobId={jobId} />}
    </div>
  );
}
```

## 進捗表示のUI例

### プログレスバー

```
[████████████░░░░░░░░] 60%
CSV生成中...
```

### ステータス表示

```
状態: 実行中
進捗: 60%
メッセージ: CSV生成中...
```

### 完了時の表示

```
✅ エクスポートが完了しました

[CSVをダウンロード] ボタン

有効期限: 2026-01-17 10:30:00
```

## ポーリング間隔の推奨値

- **実行中**: 2秒間隔（リアルタイム感を出す）
- **完了/失敗**: ポーリング停止
- **タイムアウト**: 30秒以上応答がない場合はエラー表示

## 注意事項

### 1. 大量データの場合
- CSV生成に時間がかかる場合、進捗が50%で長時間止まる可能性がある
- 将来的には、行ごとの進捗更新を検討（`CsvExportService`の修正が必要）

### 2. エラーハンドリング
- ジョブが失敗した場合、`status: failed`で返却される
- フロントエンドは適切なエラーメッセージを表示

### 3. タイムアウト
- ジョブのタイムアウト: 600秒（10分）
- フロントエンドのポーリングタイムアウト: 30秒（応答がない場合）

### 4. ダウンロードURLの有効期限
- デフォルト: 3600秒（1時間）
- 有効期限が切れた場合は、再度エクスポートが必要

## まとめ

ジョブキュー対応により、以下の機能が実現できます：

1. ✅ **リアルタイムの進捗表示**: フロントエンドが定期的に進捗を確認
2. ✅ **段階的な進捗更新**: 0% → 30% → 50% → 80% → 100%
3. ✅ **完了通知**: ダウンロードURLが利用可能になったことを通知
4. ✅ **エラーハンドリング**: 失敗時の適切な表示

これにより、ユーザーはエクスポートの進行状況を把握でき、完了を待つ必要がなくなります。
