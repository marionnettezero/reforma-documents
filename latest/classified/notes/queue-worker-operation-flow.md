# キューワーカーの動作イメージ

## 概要

Laravelのキュー処理では、**ジョブをキューに投入**し、**ワーカープロセスがキューから取り出して処理**します。

## キュー分離の理由

### 1. 優先度管理
- **通知ジョブ**: 即座に処理したい（ユーザーへの即時通知）
- **PDF生成ジョブ**: 時間がかかるが、すぐに完了する必要はない

### 2. リソース管理
- **通知ジョブ**: 軽量（メール送信のみ）
- **PDF生成ジョブ**: 重い処理（PDF生成、メモリ消費大）

### 3. 障害分離
- 一つのキューでエラーが発生しても、他のキューには影響しない
- PDF生成が失敗しても、通知は正常に送信される

---

## 動作フロー

### シナリオ1: フォーム送信時の処理

```
1. ユーザーがフォームを送信
   ↓
2. PublicFormsController::submit() が実行
   ↓
3. SendFormSubmissionNotificationJob::dispatch() が呼ばれる
   ↓
4. ジョブが "notifications" キューに投入される
   (jobsテーブルにレコードが作成される)
   ↓
5. reforma-queue-worker@notifications サービスが
   キューからジョブを取り出して処理
   ↓
6. メール通知が送信される
```

### シナリオ2: PDF再生成時の処理

```
1. 管理者がPDF再生成を実行
   ↓
2. ResponsesPdfRegenerateController::regenerate() が実行
   ↓
3. GeneratePdfJob::dispatch() が呼ばれる
   ↓
4. ジョブが "pdfs" キューに投入される
   (jobsテーブルにレコードが作成される)
   ↓
5. reforma-queue-worker@pdfs サービスが
   キューからジョブを取り出して処理
   ↓
6. PDFが生成される
```

### シナリオ3: 同時に複数のジョブが発生した場合

```
時刻: 10:00:00
- フォーム送信1 → notificationsキューに投入
- フォーム送信2 → notificationsキューに投入
- PDF再生成1 → pdfsキューに投入

時刻: 10:00:01
- reforma-queue-worker@notifications が
  フォーム送信1の通知を処理開始
- reforma-queue-worker@pdfs が
  PDF再生成1を処理開始

時刻: 10:00:05
- フォーム送信1の通知完了
- reforma-queue-worker@notifications が
  フォーム送信2の通知を処理開始

時刻: 10:00:30
- PDF再生成1完了（重い処理なので時間がかかる）
- フォーム送信2の通知完了
```

**ポイント**: 通知とPDF生成は**並行して処理**されます。

---

## サービス登録のイメージ

### 登録されるサービス

```bash
# 通知専用ワーカー（1インスタンス）
reforma-queue-worker@notifications.service

# PDF生成専用ワーカー（1インスタンス）
reforma-queue-worker@pdfs.service
```

### 各サービスの動作

```
┌─────────────────────────────────────┐
│ reforma-queue-worker@notifications │
│ (通知専用ワーカー)                  │
├─────────────────────────────────────┤
│ 1. notificationsキューを監視         │
│ 2. ジョブがあれば取り出し            │
│ 3. SendFormSubmissionNotificationJob │
│    を実行                            │
│ 4. 完了後、次のジョブを待機          │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ reforma-queue-worker@pdfs           │
│ (PDF生成専用ワーカー)                │
├─────────────────────────────────────┤
│ 1. pdfsキューを監視                   │
│ 2. ジョブがあれば取り出し              │
│ 3. GeneratePdfJobを実行             │
│ 4. 完了後、次のジョブを待機            │
└─────────────────────────────────────┘
```

### データベースの状態

#### jobsテーブル（キューに投入されたジョブ）

| id | queue | payload | attempts | created_at |
|----|-------|---------|----------|------------|
| 1 | notifications | {...} | 0 | 2026-01-17 10:00:00 |
| 2 | notifications | {...} | 0 | 2026-01-17 10:00:01 |
| 3 | pdfs | {...} | 0 | 2026-01-17 10:00:02 |

#### ワーカーの処理

1. **reforma-queue-worker@notifications** が `queue='notifications'` のジョブを処理
2. **reforma-queue-worker@pdfs** が `queue='pdfs'` のジョブを処理
3. 処理が完了すると、jobsテーブルから削除される

---

## 実際のコマンド例

### サービスの状態確認

```bash
# 通知ワーカーの状態
$ sudo systemctl status reforma-queue-worker@notifications
● reforma-queue-worker@notifications.service - ReForma Laravel Queue Worker Instance notifications
   Loaded: loaded (/etc/systemd/system/reforma-queue-worker@notifications.service)
   Active: active (running) since Wed 2026-01-17 10:00:00 JST
   Main PID: 12345 (php)
   Tasks: 1
   Memory: 50.0M
   CGroup: /system.slice/system-reforma\x2dqueue\x2dworker.slice/reforma-queue-worker@notifications.service
           └─12345 /usr/bin/php artisan queue:work database --queue=notifications ...

# PDF生成ワーカーの状態
$ sudo systemctl status reforma-queue-worker@pdfs
● reforma-queue-worker@pdfs.service - ReForma Laravel Queue Worker Instance pdfs
   Loaded: loaded (/etc/systemd/system/reforma-queue-worker@pdfs.service)
   Active: active (running) since Wed 2026-01-17 10:00:00 JST
   Main PID: 12346 (php)
   Tasks: 1
   Memory: 200.0M  ← PDF生成はメモリを多く使用
   CGroup: /system.slice/system-reforma\x2dqueue\x2dworker.slice/reforma-queue-worker@pdfs.service
           └─12346 /usr/bin/php artisan queue:work database --queue=pdfs ...
```

### ログの確認

```bash
# 通知ワーカーのログ
$ sudo journalctl -u reforma-queue-worker@notifications -f
Jan 17 10:00:01 server reforma-queue-worker-notifications[12345]: Processing: App\Jobs\SendFormSubmissionNotificationJob
Jan 17 10:00:05 server reforma-queue-worker-notifications[12345]: Processed: App\Jobs\SendFormSubmissionNotificationJob

# PDF生成ワーカーのログ
$ sudo journalctl -u reforma-queue-worker@pdfs -f
Jan 17 10:00:02 server reforma-queue-worker-pdfs[12346]: Processing: App\Jobs\GeneratePdfJob
Jan 17 10:00:30 server reforma-queue-worker-pdfs[12346]: Processed: App\Jobs\GeneratePdfJob
```

---

## キューを分離しない場合との比較

### キューを分離しない場合（すべてdefaultキュー）

```
┌─────────────────────────────────────┐
│ reforma-queue-worker@default        │
├─────────────────────────────────────┤
│ 1. defaultキューを監視               │
│ 2. ジョブを順番に処理                 │
│    - 通知ジョブ1 (5秒)               │
│    - 通知ジョブ2 (5秒)               │
│    - PDF生成ジョブ1 (30秒) ← 待たされる│
│    - 通知ジョブ3 (5秒)               │
└─────────────────────────────────────┘

問題点:
- PDF生成が重いと、通知が遅れる
- 1つのワーカーが詰まると、すべてのジョブが遅れる
```

### キューを分離した場合（推奨）

```
┌─────────────────────────────────────┐
│ reforma-queue-worker@notifications  │
├─────────────────────────────────────┤
│ 1. notificationsキューを監視          │
│ 2. 通知ジョブのみを処理               │
│    - 通知ジョブ1 (5秒)               │
│    - 通知ジョブ2 (5秒)               │
│    - 通知ジョブ3 (5秒)               │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ reforma-queue-worker@pdfs          │
├─────────────────────────────────────┤
│ 1. pdfsキューを監視                  │
│ 2. PDF生成ジョブのみを処理            │
│    - PDF生成ジョブ1 (30秒)           │
└─────────────────────────────────────┘

メリット:
- 通知は即座に処理される（PDF生成の影響を受けない）
- PDF生成が重くても、通知は正常に動作
- 障害が分離される（PDF生成が失敗しても通知は送信される）
```

---

## まとめ

1. **通知とPDF生成は別々のサービスとして登録**します
2. **各サービスは独立して動作**し、それぞれのキューを監視します
3. **並行処理が可能**で、通知とPDF生成が同時に実行されます
4. **障害が分離**され、一つのキューでエラーが発生しても他に影響しません
