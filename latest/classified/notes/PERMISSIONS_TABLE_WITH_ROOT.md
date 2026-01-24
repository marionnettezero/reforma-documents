# システム権限表（root含む）

## 概要

本ドキュメントは、ReFormaシステムの権限管理について、rootユーザーを含めたすべてのロールとパーミッションの関係をまとめたものです。

## ロール定義

| ロールコード | ロール名 | 説明 |
|------------|---------|------|
| `root` | ルートユーザー | システム全体の完全な管理権限を持つ（`is_root=true`） |
| `system_admin` | システム管理者 | システム全体の管理権限を持つ |
| `form_admin` | フォーム管理者 | フォームと回答の管理権限を持つ |
| `operator` | オペレーター | 回答の閲覧・編集権限を持つ |
| `viewer` | 閲覧者 | フォームと回答の閲覧権限のみ |

## rootユーザーの権限

**rootユーザー（`is_root=true`）は、すべてのパーミッションとロールを超越した完全な権限を持ちます。**

### rootユーザーの特徴

1. **全パーミッション**: すべてのパーミッション（`forms.*`, `responses.*`, `users.*`, `logs.*`, `settings.*`, `permissions.*`, `themes.*`）を自動的に所有
2. **全フォームアクセス**: `form_access_restriction_enabled`の設定に関わらず、全フォームにアクセス可能
3. **root専用機能**: 以下の機能はrootユーザーのみが利用可能

## パーミッション定義

### フォーム関連
- `forms.read` - フォームの閲覧
- `forms.write` - フォームの作成・更新
- `forms.delete` - フォームの削除

### 回答関連
- `responses.read` - 回答の閲覧
- `responses.write` - 回答の編集・削除
- `responses.export` - 回答のCSVエクスポート
- `responses.pdf_regenerate` - 回答PDFの再生成
- `responses.notification_resend` - 回答通知の再送

### ユーザー管理関連
- `users.read` - ユーザーの閲覧
- `users.write` - ユーザーの作成・更新
- `users.delete` - ユーザーの削除

### ログ関連
- `logs.read` - ログの閲覧

### 設定関連
- `settings.read` - システム設定の閲覧
- `settings.write` - システム設定の更新

### 権限管理関連
- `permissions.read` - 権限定義の閲覧
- `permissions.write` - 権限定義の更新

### テーマ関連
- `themes.read` - テーマの閲覧
- `themes.write` - テーマの作成・更新
- `themes.delete` - テーマの削除

### フォームアクセス制限関連
- `form_access_restriction.write` - フォームアクセス制限の設定

## ロール別パーミッション一覧

### root（ルートユーザー）

**全パーミッションを自動的に所有**

| パーミッション | 説明 | 備考 |
|--------------|------|------|
| すべてのパーミッション | 全機能へのアクセス | 自動的に全権限を所有 |

**root専用機能**:
- システム設定の取得・更新
- ロール権限定義の取得・更新
- フォームアーカイブの削除
- ログアーカイブの削除
- プリセットテーマの更新
- ユーザーの`is_root`フラグの設定
- 新規ユーザーに`system_admin`ロールを付与（作成時）
- 既存ユーザーを`system_admin`ロールに昇格（更新時）

### system_admin（システム管理者）

| パーミッション | 説明 |
|--------------|------|
| `forms.read` | フォームの閲覧 |
| `forms.write` | フォームの作成・更新 |
| `forms.delete` | フォームの削除 |
| `responses.read` | 回答の閲覧 |
| `responses.write` | 回答の編集・削除 |
| `responses.export` | 回答のCSVエクスポート |
| `responses.pdf_regenerate` | 回答PDFの再生成 |
| `responses.notification_resend` | 回答通知の再送 |
| `users.read` | ユーザーの閲覧 |
| `users.write` | ユーザーの作成・更新 |
| `users.delete` | ユーザーの削除 |
| `logs.read` | ログの閲覧 |
| `settings.read` | システム設定の閲覧 |
| `settings.write` | システム設定の更新 |
| `permissions.read` | 権限定義の閲覧 |
| `permissions.write` | 権限定義の更新 |
| `themes.read` | テーマの閲覧 |
| `themes.write` | テーマの作成・更新 |
| `themes.delete` | テーマの削除 |
| `form_access_restriction.write` | フォームアクセス制限の設定 |

### form_admin（フォーム管理者）

| パーミッション | 説明 |
|--------------|------|
| `forms.read` | フォームの閲覧 |
| `forms.write` | フォームの作成・更新 |
| `forms.delete` | フォームの削除 |
| `responses.read` | 回答の閲覧 |
| `responses.write` | 回答の編集・削除 |
| `responses.export` | 回答のCSVエクスポート |
| `responses.pdf_regenerate` | 回答PDFの再生成 |
| `responses.notification_resend` | 回答通知の再送 |
| `themes.read` | テーマの閲覧 |
| `themes.write` | テーマの作成・更新 |
| `themes.delete` | テーマの削除 |
| `form_access_restriction.write` | フォームアクセス制限の設定 |

**注意**: form_adminは、自分が作成したフォーム、または`user_form_access`テーブルで許可されたフォームにのみアクセス可能です。

### operator（オペレーター）

| パーミッション | 説明 |
|--------------|------|
| `forms.read` | フォームの閲覧 |
| `responses.read` | 回答の閲覧 |
| `responses.write` | 回答の編集・削除 |
| `responses.export` | 回答のCSVエクスポート |
| `responses.pdf_regenerate` | 回答PDFの再生成 |
| `responses.notification_resend` | 回答通知の再送 |

### viewer（閲覧者）

| パーミッション | 説明 |
|--------------|------|
| `forms.read` | フォームの閲覧 |
| `responses.read` | 回答の閲覧 |

## APIエンドポイント別権限要件

### 認証関連

| エンドポイント | メソッド | 権限要件 | 備考 |
|--------------|---------|---------|------|
| `/v1/auth/me` | GET | 認証必須 | 全ロール（root含む） |
| `/v1/auth/logout` | POST | 認証必須 | 全ロール（root含む） |
| `/v1/auth/password` | PUT | 認証必須 | 全ロール（root含む） |

### フォーム管理

| エンドポイント | メソッド | 権限要件 | 備考 |
|--------------|---------|---------|------|
| `/v1/forms` | GET | `forms.read` | rootは全フォームにアクセス可能 |
| `/v1/forms` | POST | `forms.write` | rootは全権限 |
| `/v1/forms/{id}` | GET | `forms.read` | rootは全フォームにアクセス可能 |
| `/v1/forms/{id}` | PUT | `forms.write` | rootは全権限 |
| `/v1/forms/{id}` | DELETE | `forms.delete` | rootは全権限 |
| `/v1/forms/{id}/fields` | GET | `forms.read` | rootは全権限 |
| `/v1/forms/{id}/fields` | PUT | `forms.write` | rootは全権限 |
| `/v1/forms/{id}/fields/import/csv` | POST | `forms.write` | rootは全権限 |
| `/v1/forms/{id}/fields/export/csv` | POST | `forms.read` | rootは全権限 |
| `/v1/forms/{form_id}/fields/{field_key}/options/import/csv` | POST | `forms.write` | rootは全権限 |
| `/v1/forms/{form_id}/fields/{field_key}/options/export/csv` | POST | `forms.read` | rootは全権限 |
| `/v1/forms/{id}/attachment/pdf-template` | POST | `forms.write` | rootは全権限 |
| `/v1/forms/{id}/attachment/files` | POST | `forms.write` | rootは全権限 |
| `/v1/forms/{id}/attachment/files/{file_index}` | DELETE | `forms.write` | rootは全権限 |
| `/v1/forms/{id}/logo` | POST | `forms.write` | rootは全権限 |
| `/v1/forms/{id}/logo` | DELETE | `forms.write` | rootは全権限 |
| `/v1/forms/{id}/export` | POST | `forms.read` | rootは全権限 |
| `/v1/forms/import` | POST | `forms.write` | rootは全権限 |
| `/v1/forms/{id}/archive` | POST | `system_admin` ロール または root | rootは全権限 |
| `/v1/forms/archives/{archive_id}/restore` | POST | `system_admin` ロール または root | rootは全権限 |
| `/v1/forms/archives/{id}` | DELETE | **root のみ** | root専用 |

### 回答管理

| エンドポイント | メソッド | 権限要件 | 備考 |
|--------------|---------|---------|------|
| `/v1/responses` | GET | `responses.read` | rootは全フォームの回答にアクセス可能 |
| `/v1/responses/{id}` | GET | `responses.read` | rootは全権限 |
| `/v1/responses/{id}` | DELETE | `responses.write` | rootは全権限 |
| `/v1/responses/{id}/pdf` | GET | `responses.read` | rootは全権限 |
| `/v1/responses/export/csv` | POST | `responses.export` | rootは全権限 |
| `/v1/responses/{id}/notifications/resend` | POST | `system_admin` ロール または root | rootは全権限 |
| `/v1/responses/{id}/pdf/regenerate` | POST | `responses.pdf_regenerate` または root | rootは全権限 |

### ダッシュボード

| エンドポイント | メソッド | 権限要件 | 備考 |
|--------------|---------|---------|------|
| `/v1/dashboard/summary` | GET | 認証必須 | rootは全フォームの集計 |
| `/v1/dashboard/errors` | GET | 認証必須 | rootは全フォームのエラー |

### ジョブ進捗・エクスポート

| エンドポイント | メソッド | 権限要件 | 備考 |
|--------------|---------|---------|------|
| `/v1/progress/{job_id}` | GET | 認証必須 | rootは全権限 |
| `/v1/exports/{job_id}/download` | GET | 認証必須 | rootは全権限 |

### 検索・ログ

| エンドポイント | メソッド | 権限要件 | 備考 |
|--------------|---------|---------|------|
| `/v1/search` | GET | 認証必須 | rootは全権限 |
| `/v1/logs` | GET | 認証必須 | rootは全権限 |
| `/v1/logs/{id}` | GET | 認証必須 | rootは全権限 |
| `/v1/logs/export` | GET | `system_admin` ロール または root | rootは全権限 |
| `/v1/logs/archive` | POST | `system_admin` ロール または root | rootは全権限 |
| `/v1/logs/archives/{id}` | DELETE | **root のみ** | root専用 |

### システム管理

#### system_admin権限必須（rootもアクセス可能）

| エンドポイント | メソッド | 権限要件 | 備考 |
|--------------|---------|---------|------|
| `/v1/system/admin-users` | GET | `system_admin` ロール または root | rootは全権限 |
| `/v1/system/admin-users` | POST | `system_admin` ロール または root | rootは全権限（system_adminロールの付与・昇格はrootのみ） |
| `/v1/system/admin-users/{id}` | GET | `system_admin` ロール または root | rootは全権限 |
| `/v1/system/admin-users/{id}` | PUT | `system_admin` ロール または root | rootは全権限（system_admin昇格・is_root変更はrootのみ） |
| `/v1/system/admin-users/{id}` | DELETE | `system_admin` ロール または root | rootは全権限 |
| `/v1/system/admin-users/invites/resend` | POST | `system_admin` ロール または root | rootは全権限 |
| `/v1/system/admin-audit-logs` | GET | `system_admin` ロール または root | rootは全権限 |
| `/v1/system/roles` | GET | `system_admin` ロール または root | rootは全権限 |

#### root専用

| エンドポイント | メソッド | 権限要件 | 備考 |
|--------------|---------|---------|------|
| `/v1/system/root-only/ping` | GET | **root のみ** | root専用（動作確認用） |
| `/v1/system/roles/permissions` | GET | **root のみ** | root専用 |
| `/v1/system/roles/permissions` | PUT | **root のみ** | root専用 |
| `/v1/system/settings` | GET | **root のみ** | root専用 |
| `/v1/system/settings` | PUT | **root のみ** | root専用 |
| `/v1/forms/archives/{id}` | DELETE | **root のみ** | root専用 |
| `/v1/logs/archives/{id}` | DELETE | **root のみ** | root専用 |

### テーマ管理（パーミッションベース、rootもアクセス可能）

| エンドポイント | メソッド | 権限要件 | 備考 |
|--------------|---------|---------|------|
| `/v1/system/themes` | GET | `themes.read` または root | rootは全権限 |
| `/v1/system/themes` | POST | `themes.write` または root | rootは全権限 |
| `/v1/system/themes/{id}` | GET | `themes.read` または root | rootは全権限 |
| `/v1/system/themes/{id}` | PUT | `themes.write` または root | rootは全権限（プリセットテーマの更新はrootのみ） |
| `/v1/system/themes/{id}` | DELETE | `themes.delete` または root | rootは全権限 |
| `/v1/system/themes/{id}/usage` | GET | `themes.read` または root | rootは全権限 |
| `/v1/system/themes/{id}/copy` | POST | `themes.write` または root | rootは全権限 |

### その他

| エンドポイント | メソッド | 権限要件 | 備考 |
|--------------|---------|---------|------|
| `/v1/system/supported-languages` | GET | 認証必須 | 全ロール（root含む） |

## rootユーザーの特別な権限

### 1. 全パーミッションの自動所有

rootユーザーは、`User`モデルの`hasPermission()`メソッドで、すべてのパーミッションを自動的に所有していると判定されます。

```php
// User.php
public function hasPermission(string $permission): bool
{
    // rootユーザーは全権限
    if ($this->is_root) {
        return true;
    }
    // ... 通常のパーミッションチェック
}
```

### 2. 全フォームへのアクセス

rootユーザーは、`form_access_restriction_enabled`の設定に関わらず、すべてのフォームにアクセス可能です。

```php
// User.php
public function canAccessForm(int $formId): bool
{
    // rootユーザーは全フォームにアクセス可能
    if ($this->is_root) {
        return true;
    }
    // ... 通常のアクセスチェック
}
```

### 3. root専用機能

以下の機能は、rootユーザーのみが利用可能です：

- **システム設定の管理**: `/v1/system/settings` (GET, PUT)
- **ロール権限定義の管理**: `/v1/system/roles/permissions` (GET, PUT)
- **フォームアーカイブの削除**: `/v1/forms/archives/{id}` (DELETE)
- **ログアーカイブの削除**: `/v1/logs/archives/{id}` (DELETE)
- **プリセットテーマの更新**: `/v1/system/themes/{id}` (PUT) - プリセットテーマの場合
- **ユーザーの`is_root`フラグの設定**: `/v1/system/admin-users/{id}` (PUT)
- **新規ユーザーに`system_admin`ロールを付与**: `/v1/system/admin-users` (POST)
- **既存ユーザーを`system_admin`ロールに昇格**: `/v1/system/admin-users/{id}` (PUT)

### 4. rootユーザーの管理

- **rootユーザーの作成**: データベースで直接`is_root=true`を設定する必要があります
- **rootユーザーの削除**: 通常のユーザー削除と同じ手順ですが、最後のrootユーザーは削除できないように制限すべきです
- **rootユーザーの降格**: rootユーザー自身が`is_root=false`に変更することは可能ですが、最後のrootユーザーの場合は制限すべきです

## フォームアクセス制限

### form_access_restriction_enabled が有効な場合

- **root**: 全フォームにアクセス可能（制限無効）
- **system_admin**: 全フォームにアクセス可能（制限無効）
- **form_admin**: 自分が作成したフォーム、または`user_form_access`テーブルで許可されたフォームにのみアクセス可能
- **operator**, **viewer**: `user_form_access`テーブルで許可されたフォームにのみアクセス可能

### form_access_restriction_enabled が無効な場合

- 全ロールが全フォームにアクセス可能（ただし、`user_form_access`テーブルで明示的に拒否されている場合は除く）
- **root**: 常に全フォームにアクセス可能

## 特殊な権限チェック

### rootユーザーの特別な権限

1. **全パーミッション**: すべてのパーミッションを自動的に所有
2. **全フォームアクセス**: `form_access_restriction_enabled`の設定に関わらず、全フォームにアクセス可能
3. **root専用機能**: システム設定、権限定義、アーカイブ削除などのroot専用機能へのアクセス
4. **プリセットテーマ更新**: プリセットテーマの更新はrootのみ可能
5. **ユーザー管理の特別権限**: `is_root`フラグの設定、`system_admin`ロールの付与（新規作成・昇格）はrootのみ可能

### form_adminの特別な権限

- 自分が作成したフォーム（`created_by`が自分のID）には、`user_form_access`テーブルの設定に関わらずアクセス可能
- フォームの作成・更新・削除は、自分が作成したフォーム、または許可されたフォームに対してのみ可能

### system_adminの特別な権限

- 全フォームにアクセス可能（`form_access_restriction_enabled`の設定に関わらず）
- ユーザー管理機能へのアクセス
- ログアーカイブ機能へのアクセス
- フォームアーカイブ機能へのアクセス

## 注意事項

1. **rootユーザーの優先度**: rootユーザーは、すべてのパーミッションチェックとロールチェックを超越します
2. **パーミッションベースのチェック**: 多くのエンドポイントは`hasPermission()`メソッドでパーミッションベースのチェックを行いますが、rootユーザーは常に`true`を返します
3. **ロールベースのチェック**: 一部のエンドポイントは`hasRole()`メソッドでロールベースのチェックを行いますが、rootユーザーは全機能にアクセス可能です
4. **リソースパーミッション**: フォームや回答へのアクセスは、操作パーミッションに加えて、リソースパーミッション（`user_form_access`テーブル）もチェックされますが、rootユーザーは常にアクセス可能です
5. **root専用機能**: システム設定、権限定義、アーカイブ削除などの機能は、明示的に`is_root`をチェックしているため、rootユーザーのみが利用可能です
