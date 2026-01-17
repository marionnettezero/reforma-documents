# ReForma システム全体構成

**作成日**: 2026-01-17  
**対象バージョン**: v0.5.9以降

---

## 目次

1. [システム全体概要](#システム全体概要)
2. [アーキテクチャ図](#アーキテクチャ図)
3. [コンポーネント詳細](#コンポーネント詳細)
4. [データフロー](#データフロー)
5. [ジョブキューシステム](#ジョブキューシステム)
6. [認証・認可フロー](#認証認可フロー)
7. [デプロイ構成](#デプロイ構成)

---

## システム全体概要

ReFormaは、**フォーム作成・回答管理システム**として、以下のコンポーネントで構成されています：

- **フロントエンド**: React SPA（Single Page Application）
- **バックエンド**: Laravel 12 API
- **データベース**: MySQL（RDS等）
- **ストレージ**: S3 / Local（PDF、添付ファイル）
- **メール送信**: SMTP
- **ジョブキュー**: Laravel Queue（Database Driver）+ systemd Workers

---

## アーキテクチャ図

```
┌─────────────────────────────────────────────────────────────────┐
│                        ユーザー（ブラウザ）                        │
└────────────────────────────┬────────────────────────────────────┘
                              │
                              │ HTTPS
                              │
┌─────────────────────────────▼────────────────────────────────────┐
│                        Apache Web Server                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  /reforma/          → React SPA (dist/)                   │   │
│  │  /reforma/api/      → Laravel API (public/)               │   │
│  │  BASIC認証: .htpasswd                                      │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────┬────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
        ┌───────────▼──────┐  ┌─────────▼──────────┐
        │  React SPA       │  │  Laravel API       │
        │  (Frontend)     │  │  (Backend)         │
        │                  │  │                    │
        │  - Vite          │  │  - REST API        │
        │  - React 18      │  │  - Sanctum PAT    │
        │  - Tailwind CSS  │  │  - RBAC           │
        │  - JSON Schema   │  │  - Queue Jobs      │
        └──────────────────┘  └─────────┬──────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
        ┌───────────▼──────┐  ┌─────────▼──────────┐  ┌─────▼──────┐
        │   MySQL          │  │  Laravel Queue      │  │   S3 /     │
        │   (Database)     │  │  (Database)         │  │   Local    │
        │                  │  │                     │  │  Storage   │
        │  - users         │  │  - jobs             │  │            │
        │  - forms         │  │  - failed_jobs      │  │  - PDFs    │
        │  - submissions   │  │  - progress_jobs   │  │  - Files   │
        │  - themes        │  │                     │  │            │
        │  - settings      │  │                     │  │            │
        └──────────────────┘  └─────────┬──────────┘  └─────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
        ┌───────────▼──────┐  ┌─────────▼──────────┐  ┌─────▼──────┐
        │  Queue Workers   │  │  Queue Workers     │  │  SMTP      │
        │  (systemd)       │  │  (systemd)         │  │  Server    │
        │                  │  │                    │  │            │
        │  notifications   │  │  pdfs              │  │  - Mail    │
        │  exports         │  │  imports           │  │            │
        │  uploads         │  │  (default)         │  │            │
        └──────────────────┘  └────────────────────┘  └─────────────┘
```

---

## コンポーネント詳細

### 1. フロントエンド（React SPA）

**技術スタック**:
- React 18
- Vite（ビルドツール）
- Tailwind CSS（スタイリング）
- TypeScript
- JSON Schema（UI定義）

**主な機能**:
- フォーム作成・編集UI
- フォーム項目設定UI
- 回答一覧・詳細表示
- CSVエクスポート・インポート
- テーマ管理
- システム設定
- 認証・認可（Sanctum PAT）

**デプロイ**:
- ビルド成果物（`dist/`）をApacheの`/reforma/`配下に配置
- SPAルーティング対応（`FallbackResource`）

**環境変数**:
- `VITE_API_BASE`: APIベースURL（例: `/reforma/api`）
- `VITE_API_VERSION`: APIバージョン（例: `v1`）
- `VITE_API_BASIC_AUTH_USER`: BASIC認証ユーザー名（オプション）
- `VITE_API_BASIC_AUTH_PASS`: BASIC認証パスワード（オプション）

### 2. バックエンド（Laravel API）

**技術スタック**:
- Laravel 12
- PHP 8.2+
- Sanctum（PAT認証）
- RBAC（Role-Based Access Control）

**主な機能**:
- RESTful API（`/v1/*`）
- 認証・認可（Sanctum PAT、RBAC）
- フォーム管理（CRUD）
- 回答管理（送信、確認応答、CSVエクスポート）
- PDF生成（テンプレートベース）
- メール通知
- テーマ管理
- システム設定
- ジョブキュー（非同期処理）

**APIエンドポイント例**:
- `GET /v1/health`: ヘルスチェック
- `POST /v1/auth/login`: ログイン
- `GET /v1/forms`: フォーム一覧
- `POST /v1/public/forms/{form_key}/submit`: 公開フォーム送信
- `GET /v1/progress/{job_id}`: 進捗確認

**デプロイ**:
- Laravelの`public/`ディレクトリをApacheの`/reforma/api/`配下に配置
- `.env`ファイルで環境変数を設定

### 3. データベース（MySQL）

**主なテーブル**:
- `users`: ユーザー情報（`is_root`フラグ含む）
- `roles`: ロール定義（system_admin, form_admin, operator, viewer）
- `user_roles`: ユーザー-ロール関連
- `forms`: フォーム定義
- `form_fields`: フォーム項目定義
- `submissions`: 回答データ
- `submission_values`: 回答値（JSON形式）
- `themes`: テーマ定義
- `settings`: システム設定
- `jobs`: キュージョブ（Laravel Queue）
- `failed_jobs`: 失敗したジョブ
- `progress_jobs`: 進捗追跡用ジョブ

**特徴**:
- マイクロ秒対応（`submissions.created_at`等）
- JSONカラム（`theme_tokens`, `options_json`, `value_json`等）
- Soft Deletes（論理削除）

### 4. ストレージ（S3 / Local）

**保存対象**:
- PDFテンプレート（フォームごと）
- 添付ファイル（フォームごと）
- 生成されたPDF（回答ごと）
- CSVエクスポートファイル（一時）

**設定**:
- デフォルト: S3（`pdf.storage.driver=s3`）
- 開発環境: Local（`pdf.storage.driver=local`）

### 5. メール送信（SMTP）

**用途**:
- フォーム送信通知（ユーザー・管理者）
- 管理アカウント招待
- 通知再送

**設定**:
- `.env`でSMTP設定（`MAIL_*`）

---

## データフロー

### 1. フォーム送信フロー

```
ユーザー（ブラウザ）
  ↓
React SPA (/reforma/)
  ↓ POST /v1/public/forms/{form_key}/submit
Laravel API
  ↓
1. 回答データをDBに保存（submissions, submission_values）
2. 通知ジョブをキューに投入（notificationsキュー）
  ↓
Queue Worker (notifications)
  ↓
メール送信（SMTP）
```

### 2. PDF生成フロー

```
管理者（ブラウザ）
  ↓
React SPA (/reforma/)
  ↓ POST /v1/responses/{id}/pdf/regenerate
Laravel API
  ↓
PDF生成ジョブをキューに投入（pdfsキュー）
  ↓
Queue Worker (pdfs)
  ↓
1. PDFテンプレートを読み込み
2. 回答データを埋め込み
3. PDFを生成
4. S3 / Localに保存
```

### 3. CSVエクスポートフロー

```
管理者（ブラウザ）
  ↓
React SPA (/reforma/)
  ↓ POST /v1/responses/export/csv
Laravel API
  ↓
1. 進捗ジョブを作成（progress_jobs）
2. CSVエクスポートジョブをキューに投入（exportsキュー）
  ↓ レスポンス: { job_id }
React SPA
  ↓ ポーリング: GET /v1/progress/{job_id}
Laravel API
  ↓
Queue Worker (exports)
  ↓
1. 回答データを取得
2. CSVを生成
3. 一時ファイルに保存
4. 進捗ジョブを更新（status, percent, result_path）
  ↓
React SPA
  ↓ ダウンロード: GET /v1/exports/{job_id}/download
Laravel API
  ↓
CSVファイルを返却
```

### 4. ファイルアップロードフロー

```
管理者（ブラウザ）
  ↓
React SPA (/reforma/)
  ↓ POST /v1/forms/{id}/attachment/pdf-template
Laravel API
  ↓
1. ファイルを一時保存
2. 進捗ジョブを作成（progress_jobs）
3. ファイルアップロードジョブをキューに投入（uploadsキュー）
  ↓ レスポンス: { job_id }
React SPA
  ↓ ポーリング: GET /v1/progress/{job_id}
Laravel API
  ↓
Queue Worker (uploads)
  ↓
1. 一時ファイルを読み込み
2. S3 / Localに保存
3. フォームのpdf_template_pathを更新
4. 進捗ジョブを更新（status, percent）
```

---

## ジョブキューシステム

### 概要

Laravel Queueを使用して、**重い処理や非同期処理をバックグラウンドで実行**します。

**キュードライバ**: Database（`QUEUE_CONNECTION=database`）

**キュー分離**:
- `notifications`: メール通知（即時処理が必要）
- `pdfs`: PDF生成（重い処理）
- `exports`: CSVエクスポート（大量データ処理）
- `imports`: CSVインポート（大量データ処理）
- `uploads`: ファイルアップロード（重いファイル処理）

### ワーカー管理（systemd）

**構成A: 全キュー分離（推奨）**

各キューに専用ワーカーを割り当て：

```bash
# サービスファイルを配置
sudo cp scripts/reforma-queue-worker@.service /etc/systemd/system/
sudo systemctl daemon-reload

# 各キューのワーカーを起動
sudo systemctl enable reforma-queue-worker@notifications.service
sudo systemctl start reforma-queue-worker@notifications.service
sudo systemctl enable reforma-queue-worker@pdfs.service
sudo systemctl start reforma-queue-worker@pdfs.service
sudo systemctl enable reforma-queue-worker@exports.service
sudo systemctl start reforma-queue-worker@exports.service
sudo systemctl enable reforma-queue-worker@imports.service
sudo systemctl start reforma-queue-worker@imports.service
sudo systemctl enable reforma-queue-worker@uploads.service
sudo systemctl start reforma-queue-worker@uploads.service
```

**構成B: 最小構成**

`notifications`と`pdfs`のみ専用ワーカー、他は`default`ワーカーで統合：

```bash
# 専用ワーカー
sudo systemctl enable reforma-queue-worker@notifications.service
sudo systemctl start reforma-queue-worker@notifications.service
sudo systemctl enable reforma-queue-worker@pdfs.service
sudo systemctl start reforma-queue-worker@pdfs.service

# defaultワーカー（複数キューを処理）
# /etc/systemd/system/reforma-queue-worker-default.service を作成
# ExecStart=/usr/bin/php artisan queue:work database --queue=exports,imports,uploads ...
sudo systemctl enable reforma-queue-worker-default.service
sudo systemctl start reforma-queue-worker-default.service
```

### ジョブの種類

| ジョブクラス | キュー | 用途 | タイムアウト | 試行回数 |
|------------|--------|------|-------------|---------|
| `SendFormSubmissionNotificationJob` | `notifications` | メール通知 | 300秒 | 3回 |
| `GeneratePdfJob` | `pdfs` | PDF生成 | 300秒 | 3回 |
| `ExportCsvJob` | `exports` | CSVエクスポート | 600秒 | 2回 |
| `ImportCsvJob` | `imports` | CSVインポート | 1800秒 | 1回 |
| `ProcessFileUploadJob` | `uploads` | ファイルアップロード | 300秒 | 2回 |

### 進捗追跡

**`progress_jobs`テーブル**:
- `job_id`: ジョブID（UUID）
- `type`: ジョブタイプ（`csv_export`, `csv_import`, `file_upload`等）
- `status`: ステータス（`queued`, `running`, `succeeded`, `failed`）
- `percent`: 進捗（0-100）
- `message`: メッセージ（翻訳キー）
- `result_path`: 結果ファイルパス（CSVエクスポート等）
- `result_data`: 結果データ（JSON、エラーレポート等）
- `expires_at`: 有効期限
- `download_expires_at`: ダウンロード有効期限

**フロントエンドでの進捗表示**:
1. ジョブ投入後、`job_id`を取得
2. `GET /v1/progress/{job_id}`をポーリング（2秒間隔）
3. `status`が`succeeded`または`failed`になったら停止
4. `succeeded`の場合、`download_url`を表示

---

## 認証・認可フロー

### 認証方式

**Sanctum PAT（Personal Access Token）**:
- 管理者向けの認証方式
- トークンは`personal_access_tokens`テーブルに保存
- 有効期限（TTL）は設定可能（デフォルト: 30日）
- ローリング延長対応

**フロー**:
```
1. POST /v1/auth/login
   { email, password }
   ↓
2. レスポンス: { token, user }
   ↓
3. 以降のリクエスト: Authorization: Bearer {token}
```

### 認可方式

**RBAC（Role-Based Access Control）**:

| ロール | 権限 |
|--------|------|
| `system_admin` | システム設定、テーマ管理、ユーザー管理 |
| `form_admin` | フォーム管理、回答管理、テーマ適用 |
| `operator` | 回答閲覧、CSVエクスポート |
| `viewer` | 回答閲覧のみ |

**特殊権限**:
- `root`（`is_root=true`）: プリセットテーマの変更、システム設定の変更等

**ミドルウェア**:
- `reforma.system_admin`: System Admin以上
- `reforma.form_admin`: Form Admin以上
- `reforma.root_only`: rootのみ

---

## デプロイ構成

### 本番環境（STG/本番）

**Apache設定**:
```apache
# React SPA
Alias /reforma/ "/var/www/reforma/frontend/dist/"
<Directory "/var/www/reforma/frontend/dist">
    FallbackResource /reforma/index.html
    # BASIC認証（オプション）
    AuthType Basic
    AuthName "ReForma - Restricted Access"
    AuthUserFile /var/www/.htpasswd
    Require valid-user
</Directory>

# Laravel API
Alias /reforma/api/ "/var/www/reforma/backend/public/"
<Directory "/var/www/reforma/backend/public">
    AllowOverride All
    Require all granted
    # BASIC認証（オプション）
    AuthType Basic
    AuthName "ReForma API - Restricted Access"
    AuthUserFile /var/www/.htpasswd
    Require valid-user
</Directory>
```

**ディレクトリ構成**:
```
/var/www/reforma/
├── frontend/
│   └── dist/          # React SPA ビルド成果物
├── backend/
│   ├── app/           # Laravel アプリケーション
│   ├── public/         # Apache から公開
│   ├── storage/       # ログ、一時ファイル
│   └── .env           # 環境変数
└── .htpasswd          # BASIC認証（オプション）
```

**キューワーカー**:
- systemdサービスとして起動
- 自動再起動設定（`Restart=always`）
- ログは`journalctl`で確認

### 開発環境

**フロントエンド**:
```bash
cd reforma-frontend-react
npm run dev
# http://localhost:5173/reforma/
```

**バックエンド**:
```bash
cd reforma-backend-laravel
php artisan serve
# http://localhost:8000
```

**キューワーカー**:
```bash
# 開発環境では手動で起動
php artisan queue:work --queue=notifications
php artisan queue:work --queue=pdfs
# または
php artisan queue:work --queue=exports,imports,uploads
```

---

## 関連ドキュメント

- [queue-worker-operation-flow.md](./queue-worker-operation-flow.md) - キューワーカーの動作フロー
- [queue-worker-systemd-spec.md](./queue-worker-systemd-spec.md) - キューワーカーのsystemd設定
- [apache-basic-auth-config.md](./apache-basic-auth-config.md) - Apache BASIC認証設定
- [OPERATION_MANUAL.md](../../reforma-backend-laravel/docs/OPERATION_MANUAL.md) - 運用マニュアル
