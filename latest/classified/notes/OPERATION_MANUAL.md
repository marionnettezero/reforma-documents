# ReForma Backend 運用マニュアル

**作成日**: 2026-01-17  
**対象バージョン**: v0.5.4以降

---

## 目次

1. [初期セットアップ](#初期セットアップ)
2. [初期ユーザーの作成](#初期ユーザーの作成)
3. [ジョブキューワーカーの設定](#ジョブキューワーカーの設定)
4. [運用時の対応方法](#運用時の対応方法)
5. [トラブルシューティング](#トラブルシューティング)

---

## 初期セットアップ

### 1. データベースの初期化

データベースの初期化から初期データの投入までの手順を説明します。

#### 1-1. 新規セットアップ（初回インストール時）

**手順1: データベースの作成**

MySQLを使用する場合：

```bash
# MySQLに接続
mysql -u root -p

# データベースを作成
CREATE DATABASE reforma CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# ユーザーを作成（必要に応じて）
CREATE USER 'reforma_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON reforma.* TO 'reforma_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

**手順2: 環境変数の設定**

`.env`ファイルでデータベース接続情報を設定：

```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=reforma
DB_USERNAME=reforma_user
DB_PASSWORD=your_password
```

**手順3: マイグレーションの実行（テーブル作成）**

```bash
# すべてのマイグレーションを実行してテーブルを作成
php artisan migrate
```

このコマンドで以下のテーブルが作成されます：

**Laravel標準テーブル（重要・最初に作成される）：**
- `users` - ユーザー情報（`sessions`テーブルも同時に作成される）
- `sessions` - セッション情報（`SESSION_DRIVER=database`の場合に必須）
- `cache` - キャッシュ情報（`CACHE_STORE=database`の場合に必須）
- `cache_locks` - キャッシュロック（`CACHE_STORE=database`の場合に必須）
- `jobs` - ジョブキュー（`QUEUE_CONNECTION=database`の場合に必須）
- `job_batches` - ジョブバッチ（`QUEUE_CONNECTION=database`の場合に必須）
- `failed_jobs` - 失敗したジョブ（`QUEUE_CONNECTION=database`の場合に必須）
- `personal_access_tokens` - Sanctum認証トークン

**ReForma固有テーブル：**
- `roles` - ロール情報
- `user_roles` - ユーザーとロールの関連
- `forms` - フォーム情報
- `form_translations` - フォームの翻訳情報
- `form_fields` - フォームフィールド情報
- `submissions` - フォーム送信データ
- `submission_values` - 送信データの値
- `settings` - システム設定
- `themes` - テーマ情報
- `admin_logs` - 管理ログ
- `progress_jobs` - 進捗ジョブ情報
- `notification_sent_logs` - 通知送信ログ

**重要**: 
- `php artisan migrate`を実行すると、上記のすべてのテーブルが作成されます
- 特に`sessions`、`cache`、`jobs`テーブルは、Laravelの標準マイグレーションファイル（`0001_01_01_000000_create_users_table.php`、`0001_01_01_000001_create_cache_table.php`、`0001_01_01_000002_create_jobs_table.php`）で作成されます
- データベースリセット後、これらのテーブルが存在しないと、APIアクセス時に500エラーが発生する可能性があります
- 必ず`php artisan migrate`を実行してすべてのテーブルを作成してください

**マイグレーションの確認：**

```bash
# マイグレーションの状態を確認
php artisan migrate:status

# 未実行のマイグレーションがある場合は実行
php artisan migrate

# データベースのテーブル一覧を確認（MySQLの場合）
mysql -u reforma_user -p reforma -e "SHOW TABLES;"
```

**注意**: もし`php artisan migrate`を実行しても`sessions`、`cache`、`jobs`テーブルが作成されない場合は、以下のコマンドで個別に作成できます：

```bash
# セッションテーブルを作成（通常は不要、create_users_table.phpに含まれている）
php artisan session:table
php artisan migrate

# キャッシュテーブルを作成（通常は不要、0001_01_01_000001_create_cache_table.phpに含まれている）
php artisan cache:table
php artisan migrate

# ジョブテーブルを作成（通常は不要、0001_01_01_000002_create_jobs_table.phpに含まれている）
php artisan queue:table
php artisan migrate
```

**手順4: 初期データの投入**

```bash
# すべてのシーダーを実行（推奨）
php artisan db:seed

# または、個別に実行する場合
php artisan db:seed --class=RoleSeeder        # デフォルトロールの作成
php artisan db:seed --class=SettingsSeeder    # システム設定の投入
php artisan db:seed --class=ThemeSeeder       # プリセットテーマの投入
php artisan db:seed --class=RootUserSeeder    # 初期rootユーザーの作成（環境変数設定が必要）
```

**実行されるシーダーの内容：**

1. **RoleSeeder**: デフォルトロールの作成
   - System Admin（システム管理者）
   - Form Admin（フォーム管理者）
   - Operator（オペレーター）
   - Viewer（閲覧者）
   - 既存のロールがある場合は更新されない（idempotent）

2. **SettingsSeeder**: システム設定の初期値を投入
   - 各種システム設定のデフォルト値
   - 既存の設定がある場合は更新されない（idempotent）

3. **ThemeSeeder**: プリセットテーマの投入
   - デフォルトテーマの作成
   - 既存のテーマがある場合は更新されない（idempotent）

4. **RootUserSeeder**: 初期rootユーザーの作成
   - 環境変数`CREATE_ROOT_USER=true`または本番環境の場合のみ実行
   - 既にrootユーザーが存在する場合はスキップ
   - 環境変数でメールアドレス、パスワード、名前を設定可能
   - System Adminロールが自動的に付与される

**手順5: 確認**

```bash
# データベースの状態を確認
php artisan migrate:status

# テーブル一覧を確認（MySQLの場合）
mysql -u reforma_user -p reforma -e "SHOW TABLES;"
```

#### 1-2. 確認作業用のデータベースリセット

**注意**: 以下の操作は**すべてのデータを削除**します。本番環境では絶対に実行しないでください。

**方法1: マイグレーションのロールバックと再実行（推奨）**

```bash
# すべてのマイグレーションをロールバック（全テーブル削除）
php artisan migrate:reset

# マイグレーションを再実行
php artisan migrate

# 初期データを再投入
php artisan db:seed
```

**方法2: データベースの再作成**

```bash
# データベースを削除して再作成（MySQLの場合）
mysql -u root -p -e "DROP DATABASE IF EXISTS reforma;"
mysql -u root -p -e "CREATE DATABASE reforma CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# マイグレーションを実行
php artisan migrate

# 初期データを投入
php artisan db:seed
```

**方法3: Freshコマンド（開発環境のみ）**

```bash
# すべてのテーブルを削除して再作成し、シーダーも実行
php artisan migrate:fresh --seed
```

**注意事項：**

- データベースリセットは**開発環境や確認作業時のみ**使用してください
- 本番環境では絶対に実行しないでください
- リセット前に重要なデータがある場合は必ずバックアップを取得してください
- S3に保存されているファイル（PDFテンプレート、添付ファイルなど）は削除されません

#### 1-3. 特定のマイグレーションのみ実行

```bash
# 最新のマイグレーションまで実行
php artisan migrate

# 特定のマイグレーションファイルまで実行
php artisan migrate --path=/database/migrations/2026_01_17_085523_create_notification_sent_logs_table.php

# マイグレーションの状態を確認
php artisan migrate:status
```

#### 1-4. マイグレーションのロールバック

```bash
# 最後に実行したマイグレーションをロールバック
php artisan migrate:rollback

# 最後の3つのマイグレーションをロールバック
php artisan migrate:rollback --step=3

# すべてのマイグレーションをロールバック
php artisan migrate:reset
```

### 2. 環境変数の設定

`.env`ファイルに以下を設定：

```env
# ============================================================
# ReForma Backend (Laravel 12) - Environment Config
# 作用先:
# - Laravel: app/config/*.php, bootstrap/app.php
# - Queue/Session/Cache: database driver を使用
# - Storage: S3 (署名URL発行/保存)
# ============================================================

# ------------------------------------------------------------
# [1] Laravel 基本（アプリ/URL/タイムゾーン/ロケール）
# 作用: config/app.php, URL生成, 日時処理, 翻訳(Validation等)
# ------------------------------------------------------------
APP_NAME=ReForma
APP_ENV=production
APP_KEY=base64:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
APP_DEBUG=false
APP_URL=https://your-domain.com/reforma/api
APP_TIMEZONE=Asia/Tokyo

APP_LOCALE=ja
APP_FALLBACK_LOCALE=en
APP_FAKER_LOCALE=ja_JP

# ------------------------------------------------------------
# [1-1] ビルド / デプロイ識別情報
# 作用:
# - /v1/health API のレスポンスに含める
# - フロントエンド管理画面での環境表示・デプロイ判別用
# - 障害調査時に「どのビルドが動いているか」を即座に把握するため
#
# 運用:
# - 手動デプロイ時は手動で更新
# - CI/CD 導入時はデプロイ時に自動注入するのが理想
# ------------------------------------------------------------
# APP_BUILD_VERSION=backend-v0.5.9
# APP_BUILD_SHA=abc1234
# APP_BUILD_TIMESTAMP=2026-01-17T12:00:00+09:00

# ------------------------------------------------------------
# [2] メンテナンスモード（複数Webサーバ対応）
# 作用: php artisan down/up の状態管理
# - driver=cache：メンテ状態を「キャッシュ」に保存する
# - store=database：キャッシュの保存先をDBにする（Redis不要／複数Webで同期）
# ------------------------------------------------------------
APP_MAINTENANCE_DRIVER=cache
APP_MAINTENANCE_STORE=database
# 参考:
# APP_MAINTENANCE_DRIVER=file

# ------------------------------------------------------------
# [3] セキュリティ/ハッシュ
# 作用: config/hashing.php（password hashコスト）
# ------------------------------------------------------------
BCRYPT_ROUNDS=12

# ------------------------------------------------------------
# [4] ログ
# 作用: config/logging.php
# ------------------------------------------------------------
LOG_CHANNEL=stack
LOG_STACK=single
# LOG_STACK=daily
LOG_DEPRECATIONS_CHANNEL=null
LOG_LEVEL=info

# ------------------------------------------------------------
# [5] DB（MySQL/Aurora）
# 作用: config/database.php
# ------------------------------------------------------------
DB_CONNECTION=mysql
DB_HOST=your-db-host.example.com
DB_PORT=3306
DB_DATABASE=reforma
DB_USERNAME=reforma
DB_PASSWORD=your_secure_password

# ------------------------------------------------------------
# [6] セッション（Respondent用・将来拡張）
# 作用: config/session.php
# - database driver の場合 sessions テーブルが必要
# ------------------------------------------------------------
SESSION_DRIVER=database
SESSION_LIFETIME=120
SESSION_ENCRYPT=false
SESSION_PATH=/
SESSION_DOMAIN=null

# ------------------------------------------------------------
# [7] キュー（非同期: PDF/通知など）
# 作用: config/queue.php
# - database driver の場合 jobs / failed_jobs テーブルが必要
# ------------------------------------------------------------
QUEUE_CONNECTION=database

# ------------------------------------------------------------
# [8] キャッシュ（settingsキャッシュ等）
# 作用: config/cache.php
# - database driver の場合 cache テーブルが必要
# ------------------------------------------------------------
CACHE_STORE=database
# CACHE_PREFIX=

# ------------------------------------------------------------
# [9] ブロードキャスト（未使用ならlogでOK）
# 作用: config/broadcasting.php
# ------------------------------------------------------------
BROADCAST_CONNECTION=log

# ------------------------------------------------------------
# [10] ストレージ（S3）
# 作用: config/filesystems.php
# - PDF保存/署名URL発行に利用
# ------------------------------------------------------------
FILESYSTEM_DISK=s3

AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_DEFAULT_REGION=ap-northeast-1
AWS_BUCKET=reforma-bucket
AWS_USE_PATH_STYLE_ENDPOINT=false

# 開発環境でLocalストレージを使用する場合:
# FILESYSTEM_DISK=local

# ------------------------------------------------------------
# [11] Mail（本番環境はSMTP推奨）
# 作用: config/mail.php
# ------------------------------------------------------------
MAIL_MAILER=smtp
MAIL_SCHEME=null
MAIL_HOST=smtp.example.com
MAIL_PORT=587
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
MAIL_ENCRYPTION=tls
MAIL_FROM_ADDRESS=noreply@example.com
MAIL_FROM_NAME="${APP_NAME}"

# 開発環境でログ出力する場合:
# MAIL_MAILER=log
# MAIL_SCHEME=null
# MAIL_HOST=127.0.0.1
# MAIL_PORT=2525
# MAIL_USERNAME=null
# MAIL_PASSWORD=null

# ------------------------------------------------------------
# [12] Sanctum（AdminはPAT/Bearer運用）
# 作用: Sanctum SPA Cookie認証用の判定（今回空でOK）
# - Bearer(PAT)には基本影響なし
# ------------------------------------------------------------
SANCTUM_STATEFUL_DOMAINS=

# ------------------------------------------------------------
# [13] BASIC認証（staging環境用）
# 作用: EC2のstaging環境でApache/NginxレベルでBASIC認証が設定されている場合、
# バックエンドAPIが自分自身を呼び出す際にBASIC認証を自動送信する
# 
# 使用方法:
# - 環境変数 APP_BASIC_AUTH_USER と APP_BASIC_AUTH_PASSWORD を設定
# - HTTPクライアントを使用する際に Http::withStagingAuth() を使用
#   例: Http::withStagingAuth()->get('https://example.com/api/endpoint')
# ------------------------------------------------------------
APP_BASIC_AUTH_USER=
APP_BASIC_AUTH_PASSWORD=

# ------------------------------------------------------------
# [13] Front build（Vite）
# 作用: フロントビルド時の参照（Backend単体では影響ほぼ無し）
# ------------------------------------------------------------
VITE_APP_NAME="${APP_NAME}"

# ------------------------------------------------------------
# [14] ReForma 独自設定
# 作用: ReForma側の SettingsService（実装で参照）
# 注意: 初期fallback。将来 settings テーブルが正
# ------------------------------------------------------------

# API設定
REFORMA_API_BASE=/reforma/api
REFORMA_API_VERSION_PATH=v1
REFORMA_OPENAPI_VERSION=1.3.0

# PDFストレージ設定
REFORMA_PDF_STORAGE_DISK=s3
# REFORMA_PDF_STORAGE_DISK=local
REFORMA_PDF_TEMPLATE_PATH=pdf-templates
REFORMA_PDF_ATTACHMENT_PATH=attachments
REFORMA_PDF_OUTPUT_PATH=pdf-outputs

# 通知設定
REFORMA_NOTIFICATION_DEFAULT_EMAILS=admin@example.com

# 認証設定（初期fallback）
REFORMA_AUTH_PAT_TTL_DAYS=30
REFORMA_PDF_SIGNED_URL_TTL_SECONDS=120

# S3 暗号化（将来 settings で切替。初期はSSE-S3）
REFORMA_S3_ENCRYPTION=AES256
# REFORMA_S3_ENCRYPTION=aws:kms
REFORMA_S3_KMS_KEY_ID=

# ------------------------------------------------------------
# [15] Rootユーザー作成（初回セットアップ時のみ）
# 作用: RootUserSeeder で使用
# ------------------------------------------------------------
# 初回セットアップ時にのみ設定（本番環境では自動的に有効）
# CREATE_ROOT_USER=true
ROOT_USER_INITIAL_EMAIL=root@example.com
ROOT_USER_INITIAL_PASSWORD=your_secure_password
ROOT_USER_INITIAL_NAME=Root User
```

**重要**: 
- `APP_KEY`は`php artisan key:generate`で生成してください
- パスワードやシークレットキーは必ず強力な値に変更してください
- 本番環境では`APP_DEBUG=false`を必ず設定してください

### 3. S3バケットのCORS設定

フォームアーカイブ・ログアーカイブのダウンロードや、生成PDF・CSVエクスポートの署名URLダウンロードでは、ブラウザが**管理画面のオリジン**からS3の署名付きURLへ直接リクエストします。S3バケットにCORSを設定していないと、**CORS Missing Allow Origin** が発生し、ダウンロードに失敗します。

**手順（AWS マネジメントコンソール）**

1. [S3](https://console.aws.amazon.com/s3/) で対象バケットを開く
2. **アクセス許可** タブ → **CORS (Cross-origin resource sharing)** → **編集**
3. 以下を参考にCORS設定を追加（`AllowedOrigins` は運用する管理画面のオリジンに置き換える）

```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["GET", "HEAD"],
    "AllowedOrigins": [
      "https://your-admin-domain.com",
      "https://stg.your-admin-domain.com",
      "http://localhost:5173"
    ],
    "ExposeHeaders": ["Content-Length", "Content-Disposition"]
  }
]
```

**設定の説明**

| 項目 | 説明 |
|------|------|
| `AllowedOrigins` | 管理画面（ReForma フロントエンド）のオリジン。本番・ステージング・ローカル開発のURLを列挙。末尾に `/` を付けない。 |
| `AllowedMethods` | ダウンロードは `GET`。`HEAD` も含めておく。 |
| `AllowedHeaders` | プリフライト等で送るヘッダ。`["*"]` で可。 |
| `ExposeHeaders` | ブラウザに渡すヘッダ。`Content-Disposition` でファイル名付きダウンロード、`Content-Length` でサイズ取得がしやすくなる。 |

**注意**

- `AllowedOrigins` に載っていないオリジンからのアクセスは、CORSでブロックされます。デプロイ先や `APP_URL` を増やした場合は、ここにオリジンを追加してください。
- ローカル開発（例: `http://localhost:5173`）でもS3の署名URLを開く場合は、`AllowedOrigins` に含めておきます。

トラブル時に「CORS Missing Allow Origin」と出た場合は、[アーカイブ・PDFのダウンロードで CORS Missing Allow Origin が発生する](#6-アーカイブpdfのダウンロードで-cors-missing-allow-origin-が発生する) を参照してください。

---

## 初期ユーザーの作成

### 方法1: Seederを使用（推奨）

#### 1. 環境変数の設定

`.env`ファイルに以下を設定：

```env
# Rootユーザーの初期設定
ROOT_USER_INITIAL_EMAIL=root@example.com
ROOT_USER_INITIAL_PASSWORD=your_secure_password
ROOT_USER_INITIAL_NAME=Root User

# Rootユーザー作成を有効化（本番環境では自動的に有効）
CREATE_ROOT_USER=true
```

**重要**: 初期パスワードは必ず強力なパスワードを設定してください。

#### 2. Seederの実行

```bash
# Rootユーザーを作成
php artisan db:seed --class=RootUserSeeder
```

#### 3. ログイン確認

作成されたrootユーザーでログインし、パスワードを変更してください。

```bash
# API経由でログイン
curl -X POST https://your-domain.com/reforma/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "root@example.com",
    "password": "your_secure_password"
  }'
```

### 方法2: 手動で作成

Seederを使用できない場合は、以下のSQLを実行：

**注意**: 以下のSQLはMySQL用です。SQLiteを使用している場合は、`ON DUPLICATE KEY UPDATE`の代わりに適切な構文を使用してください。

```sql
-- System Adminロールを取得または作成
INSERT INTO roles (code, name, created_at, updated_at)
VALUES ('system_admin', 'System Admin', NOW(), NOW())
ON DUPLICATE KEY UPDATE name = 'System Admin';

-- Rootユーザーを作成
-- 注意: パスワードハッシュは実際のパスワードに合わせて変更してください
-- パスワードハッシュの生成方法: php artisan tinker で Hash::make('your_password') を実行
INSERT INTO users (name, email, password, status, is_root, form_create_limit_enabled, form_create_limit, created_at, updated_at)
VALUES (
  'Root User',
  'root@example.com',
  '$2y$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJqZ5Z5Z5', -- 'password' のハッシュ（必ず変更すること）
  'active',
  true,
  false,
  NULL,
  NOW(),
  NOW()
);

-- ユーザーにSystem Adminロールを付与
INSERT INTO user_roles (user_id, role_id)
SELECT u.id, r.id
FROM users u, roles r
WHERE u.email = 'root@example.com' AND r.code = 'system_admin'
ON DUPLICATE KEY UPDATE user_id = u.id;
```

**重要**: 
- パスワードハッシュは、実際に使用するパスワードを`Hash::make()`で生成したものに置き換えてください
- ログイン後、必ずパスワードを変更してください

### 方法3: Tinkerを使用

```bash
php artisan tinker
```

```php
use App\Models\User;
use App\Models\Role;
use App\Enums\RoleCode;
use Illuminate\Support\Facades\Hash;

// System Adminロールを取得または作成
$role = Role::firstOrCreate(
    ['code' => RoleCode::SYSTEM_ADMIN->value],
    ['name' => 'System Admin']
);

// Rootユーザーを作成
$user = User::create([
    'name' => 'Root User',
    'email' => 'root@example.com',
    'password' => Hash::make('your_secure_password'),
    'status' => 'active',
    'is_root' => true,
    'form_create_limit_enabled' => false,
    'form_create_limit' => null,
]);

// ロールを付与（既に付与されている場合はスキップ）
if (!$user->roles()->where('code', RoleCode::SYSTEM_ADMIN->value)->exists()) {
    $user->roles()->attach($role->id);
}
```

---

## ジョブキューワーカーの設定

### 1. サービスファイルの配置

```bash
# サービスファイルをコピー
sudo cp scripts/reforma-queue-worker@.service /etc/systemd/system/

# systemdをリロード
sudo systemctl daemon-reload
```

### 2. サービスの起動

#### 構成A: 推奨構成（本番環境・全キュー分離）

以下のキュー用ワーカーを起動：

```bash
# 通知キュー用ワーカー
sudo systemctl enable reforma-queue-worker@notifications.service
sudo systemctl start reforma-queue-worker@notifications.service

# PDF生成キュー用ワーカー
sudo systemctl enable reforma-queue-worker@pdfs.service
sudo systemctl start reforma-queue-worker@pdfs.service

# CSVエクスポートキュー用ワーカー
sudo systemctl enable reforma-queue-worker@exports.service
sudo systemctl start reforma-queue-worker@exports.service

# CSVインポートキュー用ワーカー
sudo systemctl enable reforma-queue-worker@imports.service
sudo systemctl start reforma-queue-worker@imports.service

# ファイルアップロードキュー用ワーカー
sudo systemctl enable reforma-queue-worker@uploads.service
sudo systemctl start reforma-queue-worker@uploads.service

# アーカイブキュー用ワーカー（フォーム／ログアーカイブ・復元）
sudo systemctl enable reforma-queue-worker@archives.service
sudo systemctl start reforma-queue-worker@archives.service
```

**動作イメージ**:
- **通知ジョブ**: `notifications`キューに投入 → `reforma-queue-worker@notifications`が処理
- **PDF生成ジョブ**: `pdfs`キューに投入 → `reforma-queue-worker@pdfs`が処理
- **CSVエクスポートジョブ**: `exports`キューに投入 → `reforma-queue-worker@exports`が処理
- **CSVインポートジョブ**: `imports`キューに投入 → `reforma-queue-worker@imports`が処理
- **ファイルアップロードジョブ**: `uploads`キューに投入 → `reforma-queue-worker@uploads`が処理
- **アーカイブジョブ**（フォーム／ログアーカイブ・フォーム復元）: `archives`キューに投入 → `reforma-queue-worker@archives`が処理

各サービスは独立して動作し、並行処理が可能です。

#### 構成B: 最小構成（notifications/pdf専用 + default統合）

`notifications`と`pdfs`のみ専用ワーカーを使用し、他のキュー（`exports`, `imports`, `uploads`）は`default`ワーカーで処理する場合：

**1. 専用ワーカーの起動**

```bash
# 通知キュー用ワーカー
sudo systemctl enable reforma-queue-worker@notifications.service
sudo systemctl start reforma-queue-worker@notifications.service

# PDF生成キュー用ワーカー
sudo systemctl enable reforma-queue-worker@pdfs.service
sudo systemctl start reforma-queue-worker@pdfs.service
```

**2. defaultワーカーの設定**

`default`ワーカーで複数のキューを処理するため、専用のサービスファイルを作成します：

```bash
# サービスファイルを作成
sudo nano /etc/systemd/system/reforma-queue-worker-default.service
```

以下の内容を記述：

```ini
[Unit]
Description=ReForma Laravel Queue Worker (default - exports,imports,uploads,archives)
After=network.target mysql.service
Requires=mysql.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/reforma/backend
ExecStart=/usr/bin/php artisan queue:work database --sleep=3 --tries=3 --max-time=3600 --timeout=300 --max-jobs=1000 --queue=exports,imports,uploads,archives
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=reforma-queue-worker-default

# 環境変数（必要に応じて設定）
Environment="APP_ENV=production"
Environment="APP_DEBUG=false"
Environment="QUEUE_CONNECTION=database"

# リソース制限
LimitNOFILE=65535
MemoryLimit=512M

[Install]
WantedBy=multi-user.target
```

**3. defaultワーカーの起動**

```bash
# systemdをリロード
sudo systemctl daemon-reload

# defaultワーカーを起動
sudo systemctl enable reforma-queue-worker-default.service
sudo systemctl start reforma-queue-worker-default.service
```

**動作イメージ**:
- **通知ジョブ**: `notifications`キューに投入 → `reforma-queue-worker@notifications`が処理
- **PDF生成ジョブ**: `pdfs`キューに投入 → `reforma-queue-worker@pdfs`が処理
- **CSVエクスポートジョブ**: `exports`キューに投入 → `reforma-queue-worker-default`が処理
- **CSVインポートジョブ**: `imports`キューに投入 → `reforma-queue-worker-default`が処理
- **ファイルアップロードジョブ**: `uploads`キューに投入 → `reforma-queue-worker-default`が処理
- **アーカイブジョブ**（フォーム／ログアーカイブ・フォーム復元）: `archives`キューに投入 → `reforma-queue-worker-default`が処理

**注意**: `default`ワーカーは複数のキューを順次処理するため、大量のジョブが投入される場合は、専用ワーカーを追加することを推奨します。

### 3. サービスの状態確認

#### 構成A（全キュー分離）の場合

```bash
# 全ワーカーの状態確認
sudo systemctl status reforma-queue-worker@notifications.service
sudo systemctl status reforma-queue-worker@pdfs.service
sudo systemctl status reforma-queue-worker@exports.service
sudo systemctl status reforma-queue-worker@imports.service
sudo systemctl status reforma-queue-worker@uploads.service
sudo systemctl status reforma-queue-worker@archives.service

# ログ確認
sudo journalctl -u reforma-queue-worker@notifications.service -f
sudo journalctl -u reforma-queue-worker@pdfs.service -f
sudo journalctl -u reforma-queue-worker@exports.service -f
sudo journalctl -u reforma-queue-worker@imports.service -f
sudo journalctl -u reforma-queue-worker@uploads.service -f
sudo journalctl -u reforma-queue-worker@archives.service -f
```

#### 構成B（最小構成）の場合

```bash
# 全ワーカーの状態確認
sudo systemctl status reforma-queue-worker@notifications.service
sudo systemctl status reforma-queue-worker@pdfs.service
sudo systemctl status reforma-queue-worker-default.service

# ログ確認
sudo journalctl -u reforma-queue-worker@notifications.service -f
sudo journalctl -u reforma-queue-worker@pdfs.service -f
sudo journalctl -u reforma-queue-worker-default.service -f
```

### 4. サービスの停止・再起動

#### 構成A（全キュー分離）の場合

```bash
# 停止
sudo systemctl stop reforma-queue-worker@notifications.service

# 再起動
sudo systemctl restart reforma-queue-worker@notifications.service

# 無効化（自動起動を無効化）
sudo systemctl disable reforma-queue-worker@notifications.service
```

#### 構成B（最小構成）の場合

```bash
# defaultワーカーの停止
sudo systemctl stop reforma-queue-worker-default.service

# defaultワーカーの再起動
sudo systemctl restart reforma-queue-worker-default.service

# defaultワーカーの無効化（自動起動を無効化）
sudo systemctl disable reforma-queue-worker-default.service
```

---

## 運用時の対応方法

### 1. コード更新後の対応（git pull後）

コードを更新（`git pull`）した後は、以下のコマンドを実行してください：

#### 1-1. 依存関係の更新

```bash
# Composerの依存関係を更新
composer install --no-dev --optimize-autoloader
```

**注意**: 
- `--no-dev`は本番環境で使用（開発用パッケージをインストールしない）
- `--optimize-autoloader`はオートローダーを最適化

#### 1-2. マイグレーションの実行

```bash
# 新しいマイグレーションがある場合に実行
php artisan migrate
```

**注意**: 
- 本番環境では、事前にマイグレーションの内容を確認してください
- バックアップを取得してから実行することを推奨します

#### 1-3. キャッシュのクリアと再生成（本番環境）

```bash
# 設定キャッシュのクリアと再生成
php artisan config:clear
php artisan config:cache

# ルートキャッシュのクリアと再生成
php artisan route:clear
php artisan route:cache

# ビューキャッシュのクリアと再生成
php artisan view:clear
php artisan view:cache

# アプリケーションキャッシュのクリア
php artisan cache:clear
```

**注意**: 
- 開発環境では、キャッシュをクリアするだけで十分です（`php artisan config:clear`など）
- 本番環境では、パフォーマンス向上のためキャッシュを再生成することを推奨します

#### 1-4. キューワーカーの再起動

コード変更後は、キューワーカーを再起動してください：

```bash
# 方法1: Laravelのコマンド（推奨・グレースフル再起動）
php artisan queue:restart

# 方法2: systemctl reload（グレースフル再起動）
sudo systemctl reload reforma-queue-worker@notifications.service
sudo systemctl reload reforma-queue-worker@pdfs.service
sudo systemctl reload reforma-queue-worker@exports.service
sudo systemctl reload reforma-queue-worker@imports.service
sudo systemctl reload reforma-queue-worker@uploads.service
sudo systemctl reload reforma-queue-worker@archives.service

# または、defaultワーカーを使用している場合
sudo systemctl reload reforma-queue-worker-default.service
```

**重要**: 
- `php artisan queue:restart`は、すべてのキューワーカーに再起動シグナルを送信します
- 実行中のジョブは完了まで待機してから再起動されます（グレースフル再起動）

#### 1-5. 確認

```bash
# アプリケーションの状態確認
php artisan about

# マイグレーションの状態確認
php artisan migrate:status

# キューワーカーの状態確認
sudo systemctl status reforma-queue-worker@notifications.service
```

#### 1-6. 完全な更新手順（まとめ）

```bash
# 1. コードを更新
git pull origin main

# 2. 依存関係を更新
composer install --no-dev --optimize-autoloader

# 3. マイグレーションを実行（新しいマイグレーションがある場合）
php artisan migrate

# 4. キャッシュをクリアして再生成（本番環境）
php artisan config:clear && php artisan config:cache
php artisan route:clear && php artisan route:cache
php artisan view:clear && php artisan view:cache
php artisan cache:clear

# 5. キューワーカーを再起動
php artisan queue:restart

# 6. 状態確認
php artisan about
sudo systemctl status reforma-queue-worker@notifications.service
```

### 2. ジョブキューの監視

#### キューの状態確認

```bash
# キューに残っているジョブ数を確認
php artisan queue:monitor

# 失敗したジョブの確認
php artisan queue:failed

# 失敗したジョブの詳細確認
php artisan queue:failed:show {job_id}
```

#### ログの確認

```bash
# Laravelログ
tail -f storage/logs/laravel.log

# systemdログ（各ワーカー）
sudo journalctl -u reforma-queue-worker@notifications.service -f
sudo journalctl -u reforma-queue-worker@pdfs.service -f
```

### 2. 失敗したジョブの再試行

```bash
# 失敗したジョブを再試行
php artisan queue:retry {job_id}

# 全ての失敗したジョブを再試行
php artisan queue:retry all

# 失敗したジョブを削除
php artisan queue:forget {job_id}

# 全ての失敗したジョブを削除
php artisan queue:flush
```

### 3. ワーカーの再起動

コード変更後や設定変更後は、ワーカーを再起動してください：

```bash
# 全ワーカーを再起動
sudo systemctl restart reforma-queue-worker@notifications.service
sudo systemctl restart reforma-queue-worker@pdfs.service
sudo systemctl restart reforma-queue-worker@exports.service
sudo systemctl restart reforma-queue-worker@imports.service
sudo systemctl restart reforma-queue-worker@uploads.service
sudo systemctl restart reforma-queue-worker@archives.service
```

### 4. キューのクリア

緊急時やメンテナンス時に、キューをクリアする場合：

```bash
# 特定のキューのジョブをクリア
php artisan queue:clear notifications
php artisan queue:clear pdfs
php artisan queue:clear exports
php artisan queue:clear imports
php artisan queue:clear uploads

# 全キューのジョブをクリア
php artisan queue:clear
```

**注意**: 実行中のジョブは停止されません。実行中のジョブを停止する場合は、ワーカーを停止してください。

### 5. 進捗ジョブの確認

進捗ジョブの状態は、API経由で確認できます：

```bash
# 進捗確認
curl -X GET https://your-domain.com/reforma/api/v1/progress/{job_id} \
  -H "Authorization: Bearer {token}"
```

レスポンス例：

```json
{
  "success": true,
  "data": {
    "job": {
      "job_id": "uuid",
      "type": "csv_export",
      "status": "running",
      "percent": 50,
      "message": "messages.csv_export_generating",
      "download_url": null,
      "result_data": null,
      "expires_at": "2026-01-18T12:00:00Z",
      "download_expires_at": null
    }
  }
}
```

### 6. 定期メンテナンス

#### 失敗したジョブの定期クリーンアップ

```bash
# 30日以上前の失敗したジョブを削除
php artisan queue:prune-failed --hours=720
```

#### 進捗ジョブの定期クリーンアップ

`expires_at`が過ぎた進捗ジョブは、定期的に削除することを推奨します。

```bash
# 有効期限切れの進捗ジョブを削除（カスタムコマンドが必要な場合は実装）
php artisan tinker
```

```php
use App\Models\ProgressJob;
use Illuminate\Support\Carbon;

// 有効期限切れの進捗ジョブを削除
ProgressJob::where('expires_at', '<', Carbon::now())->delete();
```

---

## トラブルシューティング

### 1. ワーカーが起動しない

#### 確認事項

```bash
# サービスファイルの構文確認
sudo systemctl status reforma-queue-worker@notifications.service

# ログ確認
sudo journalctl -u reforma-queue-worker@notifications.service -n 50

# パーミッション確認
ls -la /var/www/reforma/backend
```

#### よくある原因

- サービスファイルのパスが間違っている
- ユーザー/グループのパーミッション不足
- データベース接続エラー
- 環境変数が設定されていない

### 2. ジョブが処理されない

#### 確認事項

```bash
# キューにジョブが存在するか確認
php artisan queue:monitor

# ワーカーが動作しているか確認
sudo systemctl status reforma-queue-worker@notifications.service

# ワーカーのログ確認
sudo journalctl -u reforma-queue-worker@notifications.service -f
```

#### 対処方法

1. ワーカーを再起動
2. キューをクリアして再投入
3. データベース接続を確認

### 3. ジョブが失敗する

#### 確認事項

```bash
# 失敗したジョブの一覧
php artisan queue:failed

# 失敗したジョブの詳細
php artisan queue:failed:show {job_id}
```

#### よくある原因

- ファイルパスの問題（PDFテンプレート、添付ファイル）
- メール送信エラー（SMTP設定）
- データベース接続エラー
- タイムアウト（大量データ処理時）

#### 対処方法

1. エラーログを確認
2. 設定を確認（メール、ストレージ等）
3. タイムアウト時間を調整（サービスファイルの`--timeout`オプション）

### 4. 進捗ジョブが表示されない

#### 確認事項

```bash
# データベースで進捗ジョブを確認
php artisan tinker
```

```php
use App\Models\ProgressJob;

// 最新の進捗ジョブを確認
ProgressJob::orderBy('created_at', 'desc')->limit(10)->get();
```

#### 対処方法

1. データベース接続を確認
2. `progress_jobs`テーブルが存在するか確認
3. マイグレーションを再実行

### 5. パフォーマンスの問題

#### 確認事項

```bash
# ワーカーのリソース使用状況
sudo systemctl status reforma-queue-worker@notifications.service
top -p $(pgrep -f "queue:work")
```

#### 対処方法

1. ワーカーの数を増やす（複数のワーカーを起動）
2. タイムアウト時間を調整
3. メモリ制限を調整（サービスファイルの`MemoryLimit`）

### 6. アーカイブ・PDFのダウンロードで CORS Missing Allow Origin が発生する

#### 現象

- フォームアーカイブ・ログアーカイブのダウンロード、または生成PDF・CSVエクスポートの署名URLをブラウザで開いたときに、**CORS Missing Allow Origin** が表示され、ファイルが取得できない。

#### 原因

- 管理画面のオリジン（例: `https://admin.example.com`）から、S3の署名付きURLへ直接 `GET` している。
- 対象のS3バケットに、そのオリジンを許可する **CORS設定** がないと、S3が `Access-Control-Allow-Origin` を返さず、ブラウザがレスポンスをブロックする。

#### 対処方法

1. 使用しているS3バケットの **CORS設定** を行う。手順と設定例は [3. S3バケットのCORS設定](#3-s3バケットのcors設定) を参照。
2. `AllowedOrigins` に、**実際に利用している管理画面のオリジン**（スキーム＋ホスト＋ポート。末尾の `/` は含めない）を必ず含める。
   - 例: `https://reforma-jesa-stg.example.com`、`https://reforma.example.com`、`http://localhost:5173` など。
3. 設定を保存後、ブラウザのキャッシュを消すか、シークレットウィンドウで再度ダウンロードを試す。

### 7. アーカイブ・PDFのS3署名付きURLで「Only one auth mechanism allowed」になる

#### 現象

- フォームアーカイブ・ログアーカイブや生成PDFの **S3署名付きURL** をブラウザで開いたときに、S3から次のようなエラーが返る。

```xml
<Error>
  <Code>InvalidArgument</Code>
  <Message>Only one auth mechanism allowed; only the X-Amz-Algorithm query parameter, Signature query string parameter or the Authorization header should be specified</Message>
  <ArgumentName>Authorization</ArgumentName>
  <ArgumentValue>Bearer 77|...</ArgumentValue>
</Error>
```

#### 原因

- S3の署名付きURLは、クエリ文字列に `X-Amz-Algorithm`、`X-Amz-Signature` などで認証情報を持っている。
- S3は **認証手段は1種類だけ** とみなし、クエリの認証と `Authorization` ヘッダーの **両方** が付いていると `InvalidArgument` を返す。
- 管理画面の `downloadFile` が、**すべてのリクエスト** に `Authorization: Bearer <token>` を付与していたため、S3の署名付きURLへアクセスする際にもBearerが付き、二重認証と判断されていた。

#### 対処方法

1. **ReForma フロントエンド** を、`downloadFile` を修正したバージョンに更新する。  
   修正内容: **外部オリジン**（S3の署名付きURLなど、`new URL(fullUrl).origin !== window.location.origin`）へのリクエストでは `Authorization` ヘッダーを付けない。自オリジン（自API経由のダウンロード）のときのみ Bearer/Basic を付与する。
2. カスタムクライアントや curl 等で署名付きURLを叩く場合も、**`Authorization` ヘッダーは付けない**。署名付きURLのクエリパラメータだけが認証に使われる。

---

## 補足

### 環境変数の一覧

#### Rootユーザー作成関連

| 変数名 | 説明 | デフォルト値 |
|--------|------|-------------|
| `ROOT_USER_INITIAL_EMAIL` | Rootユーザーの初期メールアドレス | `root@example.com` |
| `ROOT_USER_INITIAL_PASSWORD` | Rootユーザーの初期パスワード | `root` |
| `ROOT_USER_INITIAL_NAME` | Rootユーザーの初期ユーザー名 | `Root User` |
| `CREATE_ROOT_USER` | Rootユーザー作成を有効化 | `false`（本番環境では自動的に有効） |

#### ReForma独自設定

| 変数名 | 説明 | デフォルト値 |
|--------|------|-------------|
| `REFORMA_API_BASE` | APIベースパス | `/reforma/api` |
| `REFORMA_API_VERSION_PATH` | APIバージョンパス | `v1` |
| `REFORMA_OPENAPI_VERSION` | OpenAPI仕様バージョン | `1.3.0` |
| `REFORMA_PDF_STORAGE_DISK` | PDFストレージディスク | `local` |
| `REFORMA_PDF_TEMPLATE_PATH` | PDFテンプレートパス | `pdf-templates` |
| `REFORMA_PDF_ATTACHMENT_PATH` | 添付ファイルパス | `attachments` |
| `REFORMA_PDF_OUTPUT_PATH` | 生成PDF出力パス | `pdf-outputs` |
| `REFORMA_NOTIFICATION_DEFAULT_EMAILS` | デフォルト通知メールアドレス（カンマ区切り） | 空文字列 |
| `REFORMA_AUTH_PAT_TTL_DAYS` | PAT有効期限（日） | `30` |
| `REFORMA_PDF_SIGNED_URL_TTL_SECONDS` | PDF署名URL有効期限（秒） | `120` |
| `REFORMA_S3_ENCRYPTION` | S3暗号化方式 | `AES256` |
| `REFORMA_S3_KMS_KEY_ID` | S3 KMSキーID（aws:kms使用時） | 空文字列 |

#### ビルド情報（オプション）

| 変数名 | 説明 | デフォルト値 |
|--------|------|-------------|
| `APP_BUILD_VERSION` | ビルドバージョン | `VERSION`ファイルから取得 |
| `APP_BUILD_SHA` | Git SHA | Gitから取得 |
| `APP_BUILD_TIMESTAMP` | ビルドタイムスタンプ | Gitから取得 |

### キューの種類

| キュー名 | 用途 | タイムアウト | 試行回数 | 推奨構成 |
|---------|------|-------------|---------|---------|
| `notifications` | メール通知 | 300秒 | 3回 | 専用ワーカー（推奨） |
| `pdfs` | PDF生成 | 300秒 | 3回 | 専用ワーカー（推奨） |
| `exports` | CSVエクスポート | 600秒 | 2回 | 専用ワーカー or default統合 |
| `imports` | CSVインポート | 1800秒 | 1回 | 専用ワーカー or default統合 |
| `uploads` | ファイルアップロード | 300秒 | 2回 | 専用ワーカー or default統合 |

**構成の選択**:
- **構成A（全キュー分離）**: 各キューに専用ワーカーを割り当て。大量のジョブが投入される場合や、キューごとにリソースを分離したい場合に推奨。
- **構成B（最小構成）**: `notifications`と`pdfs`のみ専用ワーカー、他は`default`ワーカーで統合。リソースが限られている場合や、ジョブの投入頻度が低い場合に推奨。

### セキュリティ注意事項

1. **Rootユーザーのパスワード**: 初期パスワードは必ず変更してください
2. **環境変数**: `.env`ファイルは適切なパーミッション（600）を設定してください
3. **ログ**: ログファイルに機密情報が含まれないように注意してください
4. **BASIC認証**: ステージング環境等でBASIC認証を設定する場合は、`.htpasswd`ファイルのパーミッションを適切に設定してください

---

## 関連ドキュメント

- README.md (reforma-backend-laravel リポジトリ) - プロジェクト概要
- CHANGELOG.md (reforma-backend-laravel リポジトリ) - 変更履歴
- [queue-worker-systemd-spec.md](./queue-worker-systemd-spec.md) - キューワーカー詳細仕様
- [queue-worker-operation-flow.md](./queue-worker-operation-flow.md) - キューワーカー動作フロー
