# Apache BASIC認証設定

## 設定例

### 1. パスワードファイルの作成

```bash
# .htpasswdファイルを作成（初回）
htpasswd -c /var/www/.htpasswd reforma_user

# 追加ユーザー（2人目以降）
htpasswd /var/www/.htpasswd reforma_user2
```

**注意**: `/var/www/.htpasswd`のパーミッションは適切に設定済みです。

### 2. Apache設定（BASIC認証追加版）

```apache
# ------------------------------------------------------------
# ReForma mount (no DocumentRoot / no VirtualHost)
# URL: https://stg.apps.jesa.or.jp/reforma/
# React SPA  : /reforma/
# Laravel API: /reforma/api/
# ------------------------------------------------------------

# Laravel public mounted under /reforma/api  ※先に書く
Alias /reforma/api/ "/var/www/reforma/backend/public/"
<Directory "/var/www/reforma/backend/public">
    AllowOverride All
    Require all granted
    
    # BASIC認証を追加
    AuthType Basic
    AuthName "ReForma API - Restricted Access"
    AuthUserFile /var/www/.htpasswd
    Require valid-user
</Directory>

# React (build output) mounted under /reforma  ※後に書く
Alias /reforma/ "/var/www/reforma/frontend/dist/"
<Directory "/var/www/reforma/frontend/dist">
    AllowOverride None
    Require all granted
    FallbackResource /reforma/index.html
</Directory>

<IfModule mod_headers.c>
  # SPA の入口は常に最新確認
  <Files "index.html">
    Header set Cache-Control "no-cache, must-revalidate"
  </Files>

  # ハッシュ付き静的資産は長期キャッシュ
  <FilesMatch "\.(js|css|png|jpg|jpeg|gif|svg|webp|woff2?)$">
    Header set Cache-Control "public, max-age=31536000, immutable"
  </FilesMatch>
</IfModule>
```

## フロントエンド側の対応

### 環境変数の設定

`.env.production`または`.env.staging`に追加：

```bash
# BASIC認証情報（ステージング環境など）
VITE_API_BASIC_AUTH_USER=reforma_user
VITE_API_BASIC_AUTH_PASS=your_password_here
```

### apiFetch.tsの修正

```typescript
// src/utils/apiFetch.ts に追加

import { envString } from "./env";

/**
 * BASIC認証ヘッダーを生成
 */
function getBasicAuthHeader(): string | null {
  const user = envString("VITE_API_BASIC_AUTH_USER", "");
  const pass = envString("VITE_API_BASIC_AUTH_PASS", "");
  
  if (!user || !pass) {
    return null; // BASIC認証が設定されていない場合はnull
  }
  
  const credentials = btoa(`${user}:${pass}`);
  return `Basic ${credentials}`;
}

export async function apiFetch(input: string, init?: RequestInit): Promise<Response> {
  const url = normalizeApiUrl(input);
  
  // BASIC認証ヘッダーを追加
  const basicAuth = getBasicAuthHeader();
  const headers: HeadersInit = {
    ...(init?.headers ?? {}),
  };
  
  if (basicAuth) {
    headers["Authorization"] = basicAuth;
  }

  const res = await fetch(url, {
    credentials: "include",
    ...init,
    headers,
  });
  
  // ... 既存の処理 ...
}
```

## 注意事項

### 1. セキュリティ
- `/var/www/.htpasswd`ファイルのパーミッションは適切に設定済み
- パスワードは環境変数で管理し、リポジトリにコミットしない
- 本番環境ではHTTPS必須

### 2. フロントエンドからのアクセス
- `apiFetch.ts`でBASIC認証ヘッダーを自動追加すれば問題なし
- ブラウザの自動BASIC認証ダイアログは表示されない（ヘッダーで送信するため）

### 3. 環境別の設定
- 開発環境: BASIC認証なし
- ステージング環境: BASIC認証あり
- 本番環境: BASIC認証なし（または別の認証方式）

### 4. CORSとの関係
- BASIC認証はCORSとは独立して動作
- `credentials: "include"`は既に設定済みなので問題なし

## 代替案：特定IPのみ許可

BASIC認証の代わりに、特定IPからのみアクセスを許可する方法：

```apache
<Directory "/var/www/reforma/backend/public">
    AllowOverride All
    # 特定IPのみ許可
    Require ip 192.168.1.0/24
    Require ip 10.0.0.0/8
    # または特定ホストのみ
    # Require host example.com
</Directory>
```
