# キューワーカー systemd サービス ユーザー設定トラブルシューティング

## エラーメッセージ

```
Failed to determine user credentials: No such process
Failed at step USER spawning /usr/bin/php: No such process
```

## 原因

systemdサービスファイル（`reforma-queue-worker@.service`）で指定されている`User=www-data`が、実際のサーバー環境に存在しない、またはsystemdが認識できない状態です。

### 考えられる原因

1. **ユーザーが存在しない**
   - デフォルトのサービスファイルでは`User=www-data`を指定
   - 環境によっては`www-data`ユーザーが存在しない場合がある
   - Amazon Linux 2 / CentOS / RHEL: `apache`ユーザー
   - 一部の環境: `nginx`ユーザー
   - EC2インスタンス: `ec2-user`など

2. **ユーザーID/グループIDの問題**
   - ユーザーは存在するが、systemdが正しく認識できない

3. **権限の問題**
   - ユーザーが存在するが、必要な権限がない

## 対処方法

### 1. 現在のWebサーバーユーザーを確認

```bash
# Apacheの場合
ps aux | grep apache | head -1
# または
ps aux | grep httpd | head -1

# Nginxの場合
ps aux | grep nginx | head -1

# 一般的な確認方法
id www-data
id apache
id nginx
```

### 2. サービスファイルのユーザーを修正

#### 方法A: サービスファイルを直接編集（推奨）

```bash
# サービスファイルを編集
sudo nano /etc/systemd/system/reforma-queue-worker@.service
```

以下の行を修正：

```ini
# 修正前
User=www-data
Group=www-data

# 修正後（例：Apacheの場合）
User=apache
Group=apache

# または（例：Nginxの場合）
User=nginx
Group=nginx

# または（例：EC2の場合）
User=ec2-user
Group=ec2-user
```

#### 方法B: systemd override設定を使用（推奨）

サービスファイルを直接編集せず、override設定を使用する方法：

```bash
# override設定ディレクトリを作成
sudo mkdir -p /etc/systemd/system/reforma-queue-worker@.service.d/

# override設定ファイルを作成
sudo nano /etc/systemd/system/reforma-queue-worker@.service.d/override.conf
```

以下の内容を記述：

```ini
[Service]
User=apache
Group=apache
```

### 3. systemd設定を再読み込み

```bash
# systemd設定を再読み込み
sudo systemctl daemon-reload

# サービスを再起動
sudo systemctl restart reforma-queue-worker@default.service

# ステータスを確認
sudo systemctl status reforma-queue-worker@default.service
```

### 4. ユーザーが存在しない場合の対処

#### 4.1 ユーザーを作成する（推奨）

```bash
# www-dataユーザーとグループを作成
sudo groupadd www-data
sudo useradd -g www-data www-data

# または、既存のWebサーバーユーザーを使用
# （Apacheの場合）
sudo groupadd apache
sudo useradd -g apache apache
```

#### 4.2 既存のWebサーバーユーザーを使用する

```bash
# Apacheの場合
User=apache
Group=apache

# Nginxの場合
User=nginx
Group=nginx
```

### 5. 一時的な対処（非推奨）

**注意**: セキュリティ上の理由から、本番環境では推奨されません。

```ini
# UserとGroupの行を削除またはコメントアウト
# User=www-data
# Group=www-data
```

この場合、サービスはrootユーザーで実行されます。

## 確認手順

### 1. ユーザーの存在確認

```bash
# ユーザーが存在するか確認
id www-data
id apache
id nginx

# 存在するユーザーの一覧を確認
cat /etc/passwd | grep -E "(www-data|apache|nginx)"
```

### 2. サービスファイルの確認

```bash
# サービスファイルの内容を確認
cat /etc/systemd/system/reforma-queue-worker@.service

# override設定がある場合
cat /etc/systemd/system/reforma-queue-worker@.service.d/override.conf
```

### 3. サービスステータスの確認

```bash
# サービスのステータスを確認
sudo systemctl status reforma-queue-worker@default.service

# 詳細なログを確認
sudo journalctl -u reforma-queue-worker@default.service -n 50 --no-pager
```

### 4. 権限の確認

```bash
# 作業ディレクトリの権限を確認
ls -la /var/www/reforma/backend

# ストレージディレクトリの権限を確認
ls -la /var/www/reforma/backend/storage
ls -la /var/www/reforma/backend/storage/logs
```

## 推奨設定

### Amazon Linux 2 / CentOS / RHEL の場合

```ini
[Service]
User=apache
Group=apache
WorkingDirectory=/var/www/reforma/backend
```

### Ubuntu / Debian の場合

```ini
[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/reforma/backend
```

### Nginx を使用している場合

```ini
[Service]
User=nginx
Group=nginx
WorkingDirectory=/var/www/reforma/backend
```

## 注意事項

1. **セキュリティ**: サービスは最小権限の原則に従い、Webサーバーユーザーで実行することを推奨
2. **ファイル権限**: 作業ディレクトリとストレージディレクトリが、指定したユーザーで読み書き可能であることを確認
3. **ログディレクトリ**: `storage/logs`ディレクトリが書き込み可能であることを確認

## ファイル権限の設定例

```bash
# 作業ディレクトリの所有者を変更
sudo chown -R apache:apache /var/www/reforma/backend

# ストレージディレクトリの権限を設定
sudo chmod -R 775 /var/www/reforma/backend/storage
sudo chmod -R 775 /var/www/reforma/backend/bootstrap/cache
```

## 参考

- [systemd.service - systemd service unit configuration](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
- [Laravel Queue Workers](https://laravel.com/docs/queues#running-queue-workers)
