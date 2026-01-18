# Laravel Queue Worker systemdサービス化仕様

## 現状

### 実装済みジョブ
- ✅ `GeneratePdfJob`: PDF生成ジョブ（タイムアウト300秒、試行3回）
- ✅ `SendFormSubmissionNotificationJob`: フォーム送信通知ジョブ（タイムアウト300秒、試行3回）

### キュー設定
- **デフォルト接続**: `database`（`config/queue.php`）
- **キュー名**: `default`（環境変数`DB_QUEUE`で変更可能）
- **リトライ時間**: 90秒（環境変数`DB_QUEUE_RETRY_AFTER`で変更可能）
- **失敗ジョブ保存**: `database-uuids`（`failed_jobs`テーブル）

### 未実装
- ❌ systemdサービス化
- ❌ 本番環境でのワーカープロセス管理
- ❌ 複数キュー対応（優先度別キュー）

---

## systemdサービス化の仕様

### 1. 基本方針

- **ワーカー数**: 環境に応じて設定可能（デフォルト: 1ワーカー）
- **キュー分離**: 必要に応じて複数キューに対応（`default`, `notifications`, `pdfs`等）
- **自動再起動**: プロセスが異常終了した場合、自動的に再起動
- **ログ管理**: systemd journalとLaravelログの両方で管理

### 2. サービスファイル仕様

#### 2.1 基本サービス（単一ワーカー）

**ファイル**: `/etc/systemd/system/reforma-queue-worker.service`

```ini
[Unit]
Description=ReForma Laravel Queue Worker
After=network.target mysql.service
Requires=mysql.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/reforma/backend
ExecStart=/usr/bin/php artisan queue:work database --sleep=3 --tries=3 --max-time=3600 --timeout=300
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=reforma-queue-worker

# 環境変数（必要に応じて設定）
Environment="APP_ENV=production"
Environment="APP_DEBUG=false"
Environment="QUEUE_CONNECTION=database"
Environment="DB_QUEUE=default"
Environment="DB_QUEUE_RETRY_AFTER=90"

# リソース制限
LimitNOFILE=65535
MemoryMax=512M

[Install]
WantedBy=multi-user.target
```

#### 2.2 複数ワーカー対応（推奨）

**ファイル**: `/etc/systemd/system/reforma-queue-worker@.service`（テンプレートサービス）

```ini
[Unit]
Description=ReForma Laravel Queue Worker Instance %i
After=network.target mysql.service
Requires=mysql.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/reforma/backend
ExecStart=/usr/bin/php artisan queue:work database --sleep=3 --tries=3 --max-time=3600 --timeout=300 --queue=%i
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=reforma-queue-worker-%i

# 環境変数
Environment="APP_ENV=production"
Environment="APP_DEBUG=false"
Environment="QUEUE_CONNECTION=database"

# リソース制限
LimitNOFILE=65535
MemoryMax=512M

[Install]
WantedBy=multi-user.target
```

**起動例**:
```bash
# デフォルトキュー用ワーカー（2インスタンス）
systemctl enable reforma-queue-worker@default-1.service
systemctl enable reforma-queue-worker@default-2.service
systemctl start reforma-queue-worker@default-1.service
systemctl start reforma-queue-worker@default-2.service

# 通知専用キュー用ワーカー
systemctl enable reforma-queue-worker@notifications.service
systemctl start reforma-queue-worker@notifications.service

# PDF生成専用キュー用ワーカー
systemctl enable reforma-queue-worker@pdfs.service
systemctl start reforma-queue-worker@pdfs.service
```

### 3. パラメータ仕様

#### 3.1 queue:work コマンドオプション

| オプション | デフォルト値 | 説明 | 推奨値 |
|-----------|------------|------|--------|
| `--queue` | `default` | 処理するキュー名 | 用途別に分離（`default`, `notifications`, `pdfs`） |
| `--sleep` | `3` | ジョブがない場合の待機時間（秒） | `3`（短時間処理）または`5`（長時間処理） |
| `--tries` | `3` | ジョブの最大試行回数 | `3`（ジョブクラスで個別設定可能） |
| `--max-time` | `無制限` | ワーカーの最大実行時間（秒） | `3600`（1時間で再起動、メモリリーク対策） |
| `--timeout` | `60` | ジョブのタイムアウト時間（秒） | `300`（PDF生成など長時間処理に対応） |
| `--max-jobs` | `無制限` | ワーカーが処理する最大ジョブ数 | `1000`（メモリリーク対策） |
| `--max-time` | `無制限` | ワーカーの最大実行時間（秒） | `3600`（1時間で再起動） |
| `--stop-when-empty` | `false` | キューが空になったら停止 | 本番では`false`（常駐） |

#### 3.2 環境変数

| 変数名 | デフォルト値 | 説明 |
|--------|------------|------|
| `QUEUE_CONNECTION` | `database` | キュー接続ドライバー |
| `DB_QUEUE` | `default` | データベースキューのキュー名 |
| `DB_QUEUE_RETRY_AFTER` | `90` | リトライまでの待機時間（秒） |
| `DB_QUEUE_TABLE` | `jobs` | ジョブテーブル名 |

### 4. キュー分離戦略（推奨）

#### 4.1 キュー分離のメリット
- **優先度管理**: 重要度の高いジョブを優先処理
- **リソース管理**: 重い処理と軽い処理を分離
- **障害分離**: 一つのキューでエラーが発生しても他に影響しない

#### 4.2 推奨キュー構成

| キュー名 | 用途 | ワーカー数 | 優先度 |
|---------|------|-----------|--------|
| `default` | 汎用ジョブ | 1-2 | 中 |
| `notifications` | メール通知 | 1-2 | 高（即時性重視） |
| `pdfs` | PDF生成 | 1 | 低（重い処理） |

#### 4.3 ジョブのキュー指定

```php
// 通知ジョブを専用キューに投入
SendFormSubmissionNotificationJob::dispatch($formId, $submissionId)
    ->onQueue('notifications');

// PDF生成ジョブを専用キューに投入
GeneratePdfJob::dispatch($submissionId, $userId)
    ->onQueue('pdfs');
```

### 5. 監視・ログ

#### 5.1 systemd journal

```bash
# ワーカーの状態確認
systemctl status reforma-queue-worker@default-1

# ログ確認
journalctl -u reforma-queue-worker@default-1 -f

# エラーログのみ
journalctl -u reforma-queue-worker@default-1 -p err
```

#### 5.2 Laravelログ

- ジョブの実行ログ: `storage/logs/laravel.log`
- 失敗ジョブ: `failed_jobs`テーブル
- ジョブの実行状況: `jobs`テーブル

### 6. デプロイ時の対応

#### 6.1 デプロイスクリプト例

```bash
#!/bin/bash
# deploy-queue.sh

# 1. コードデプロイ
cd /var/www/reforma/backend
git pull origin main
composer install --no-dev --optimize-autoloader
php artisan migrate --force
php artisan config:cache
php artisan route:cache
php artisan view:cache

# 2. キューワーカーの再起動（グレースフル）
systemctl reload reforma-queue-worker@default-1
systemctl reload reforma-queue-worker@default-2
# または
php artisan queue:restart  # 全ワーカーに再起動シグナルを送信
```

#### 6.2 グレースフル再起動

```bash
# 方法1: systemctl reload（systemdがシグナルを送信）
systemctl reload reforma-queue-worker@default-1

# 方法2: artisan queue:restart（Laravelがシグナルを送信）
php artisan queue:restart
```

### 7. トラブルシューティング

#### 7.1 ワーカーが起動しない

```bash
# ログ確認
journalctl -u reforma-queue-worker@default-1 -n 50

# 権限確認
ls -la /var/www/reforma/backend
ls -la /var/www/reforma/backend/storage/logs

# データベース接続確認
php artisan tinker
>>> DB::connection()->getPdo();
```

#### 7.2 ジョブが処理されない

```bash
# キューにジョブがあるか確認
php artisan queue:work --once --verbose

# 失敗ジョブを確認
php artisan queue:failed

# 失敗ジョブを再試行
php artisan queue:retry all
```

#### 7.3 メモリリーク対策

- `--max-jobs=1000`: 1000ジョブ処理後に再起動
- `--max-time=3600`: 1時間実行後に再起動
- 定期的な再起動でメモリをクリア

### 8. 実装タスク

#### 8.1 バックエンド側

- [ ] systemdサービスファイルの作成
  - [ ] `/etc/systemd/system/reforma-queue-worker@.service`
  - [ ] 環境変数設定ファイル（`/etc/systemd/system/reforma-queue-worker@.service.d/override.conf`）
- [ ] デプロイスクリプトの更新
  - [ ] キューワーカーの再起動処理を追加
- [ ] ジョブクラスのキュー指定
  - [ ] `SendFormSubmissionNotificationJob` → `notifications`キュー
  - [ ] `GeneratePdfJob` → `pdfs`キュー
- [ ] ドキュメント更新
  - [ ] `README.md`にキューワーカー管理手順を追加
  - [ ] `CHANGELOG.md`にsystemdサービス化を記載

#### 8.2 運用側

- [ ] systemdサービスファイルの配置
- [ ] サービス有効化・起動
- [ ] 監視設定（必要に応じて）
- [ ] ログローテーション設定

---

## 参考

- [Laravel Queue Documentation](https://laravel.com/docs/12.x/queues)
- [systemd Service Unit](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
- [Laravel Queue Worker Options](https://laravel.com/docs/12.x/queues#queue-workers-and-deployment)
