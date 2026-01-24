# システム権限表（root除く）

## 概要

本ドキュメントは、ReFormaシステムの権限管理について、rootユーザーを除いた通常のロールとパーミッションの関係をまとめたものです。

## ロール定義

| ロールコード | ロール名 | 説明 |
|------------|---------|------|
| `system_admin` | システム管理者 | システム全体の管理権限を持つ |
| `form_admin` | フォーム管理者 | フォームと回答の管理権限を持つ |
| `operator` | オペレーター | 回答の閲覧・編集権限を持つ |
| `viewer` | 閲覧者 | フォームと回答の閲覧権限のみ |

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
| `/v1/auth/me` | GET | 認証必須 | 全ロール |
| `/v1/auth/logout` | POST | 認証必須 | 全ロール |
| `/v1/auth/password` | PUT | 認証必須 | 全ロール |

### フォーム管理

| エンドポイント | メソッド | 権限要件 | 備考 |
|--------------|---------|---------|------|
| `/v1/forms` | GET | `forms.read` | アクセス可能なフォームのみ |
| `/v1/forms` | POST | `forms.write` | - |
| `/v1/forms/{id}` | GET | `forms.read` | アクセス可能なフォームのみ |
| `/v1/forms/{id}` | PUT | `forms.write` | アクセス可能なフォームのみ |
| `/v1/forms/{id}` | DELETE | `forms.delete` | アクセス可能なフォームのみ |
| `/v1/forms/{id}/fields` | GET | `forms.read` | アクセス可能なフォームのみ |
| `/v1/forms/{id}/fields` | PUT | `forms.write` | アクセス可能なフォームのみ |
| `/v1/forms/{id}/fields/import/csv` | POST | `forms.write` | アクセス可能なフォームのみ |
| `/v1/forms/{id}/fields/export/csv` | POST | `forms.read` | アクセス可能なフォームのみ |
| `/v1/forms/{form_id}/fields/{field_key}/options/import/csv` | POST | `forms.write` | アクセス可能なフォームのみ |
| `/v1/forms/{form_id}/fields/{field_key}/options/export/csv` | POST | `forms.read` | アクセス可能なフォームのみ |
| `/v1/forms/{id}/attachment/pdf-template` | POST | `forms.write` | アクセス可能なフォームのみ |
| `/v1/forms/{id}/attachment/files` | POST | `forms.write` | アクセス可能なフォームのみ |
| `/v1/forms/{id}/attachment/files/{file_index}` | DELETE | `forms.write` | アクセス可能なフォームのみ |
| `/v1/forms/{id}/logo` | POST | `forms.write` | アクセス可能なフォームのみ |
| `/v1/forms/{id}/logo` | DELETE | `forms.write` | アクセス可能なフォームのみ |
| `/v1/forms/{id}/export` | POST | `forms.read` | アクセス可能なフォームのみ |
| `/v1/forms/import` | POST | `forms.write` | form_admin または system_admin |
| `/v1/forms/{id}/archive` | POST | `system_admin` ロール | system_adminのみ |
| `/v1/forms/archives/{archive_id}/restore` | POST | `system_admin` ロール | system_adminのみ |
| `/v1/forms/archives/{id}` | DELETE | `root` のみ | root専用（別表参照） |

### 回答管理

| エンドポイント | メソッド | 権限要件 | 備考 |
|--------------|---------|---------|------|
| `/v1/responses` | GET | `responses.read` | アクセス可能なフォームの回答のみ |
| `/v1/responses/{id}` | GET | `responses.read` | アクセス可能なフォームの回答のみ |
| `/v1/responses/{id}` | DELETE | `responses.write` | アクセス可能なフォームの回答のみ |
| `/v1/responses/{id}/pdf` | GET | `responses.read` | アクセス可能なフォームの回答のみ |
| `/v1/responses/export/csv` | POST | `responses.export` | アクセス可能なフォームの回答のみ |
| `/v1/responses/{id}/notifications/resend` | POST | `system_admin` ロール | system_adminのみ |
| `/v1/responses/{id}/pdf/regenerate` | POST | `responses.pdf_regenerate` | system_adminまたはroot |

### ダッシュボード

| エンドポイント | メソッド | 権限要件 | 備考 |
|--------------|---------|---------|------|
| `/v1/dashboard/summary` | GET | 認証必須 | アクセス可能なフォームの集計のみ |
| `/v1/dashboard/errors` | GET | 認証必須 | アクセス可能なフォームのエラーのみ |

### ジョブ進捗・エクスポート

| エンドポイント | メソッド | 権限要件 | 備考 |
|--------------|---------|---------|------|
| `/v1/progress/{job_id}` | GET | 認証必須 | 自分のジョブのみ |
| `/v1/exports/{job_id}/download` | GET | 認証必須 | 自分のジョブのみ |

### 検索・ログ

| エンドポイント | メソッド | 権限要件 | 備考 |
|--------------|---------|---------|------|
| `/v1/search` | GET | 認証必須 | 全ロール |
| `/v1/logs` | GET | 認証必須 | 全ロール |
| `/v1/logs/{id}` | GET | 認証必須 | 全ロール |
| `/v1/logs/export` | GET | `system_admin` ロール | system_adminのみ |
| `/v1/logs/archive` | POST | `system_admin` ロール | system_adminのみ |
| `/v1/logs/archives/{id}` | DELETE | `root` のみ | root専用（別表参照） |

### システム管理（system_admin権限必須）

| エンドポイント | メソッド | 権限要件 | 備考 |
|--------------|---------|---------|------|
| `/v1/system/admin-users` | GET | `system_admin` ロール | system_adminのみ |
| `/v1/system/admin-users` | POST | `system_admin` ロール | system_adminのみ（system_adminロールの付与はrootのみ） |
| `/v1/system/admin-users/{id}` | GET | `system_admin` ロール | system_adminのみ |
| `/v1/system/admin-users/{id}` | PUT | `system_admin` ロール | system_adminのみ（system_adminロールの昇格・is_root変更はrootのみ） |
| `/v1/system/admin-users/{id}` | DELETE | `system_admin` ロール | system_adminのみ |
| `/v1/system/admin-users/invites/resend` | POST | `system_admin` ロール | system_adminのみ |
| `/v1/system/admin-audit-logs` | GET | `system_admin` ロール | system_adminのみ |
| `/v1/system/roles` | GET | `system_admin` ロール | system_admin以上 |

### テーマ管理（パーミッションベース）

| エンドポイント | メソッド | 権限要件 | 備考 |
|--------------|---------|---------|------|
| `/v1/system/themes` | GET | `themes.read` | form_admin以上 |
| `/v1/system/themes` | POST | `themes.write` | form_admin以上 |
| `/v1/system/themes/{id}` | GET | `themes.read` | form_admin以上 |
| `/v1/system/themes/{id}` | PUT | `themes.write` | form_admin以上（プリセットテーマはrootのみ） |
| `/v1/system/themes/{id}` | DELETE | `themes.delete` | form_admin以上 |
| `/v1/system/themes/{id}/usage` | GET | `themes.read` | form_admin以上 |
| `/v1/system/themes/{id}/copy` | POST | `themes.write` | form_admin以上 |

### その他

| エンドポイント | メソッド | 権限要件 | 備考 |
|--------------|---------|---------|------|
| `/v1/system/supported-languages` | GET | 認証必須 | 全ロール |

## フォームアクセス制限

### form_access_restriction_enabled が有効な場合

- `form_admin`: 自分が作成したフォーム、または`user_form_access`テーブルで許可されたフォームにのみアクセス可能
- `system_admin`: 全フォームにアクセス可能（制限無効）
- `operator`, `viewer`: `user_form_access`テーブルで許可されたフォームにのみアクセス可能

### form_access_restriction_enabled が無効な場合

- 全ロールが全フォームにアクセス可能（ただし、`user_form_access`テーブルで明示的に拒否されている場合は除く）

## 特殊な権限チェック

### form_adminの特別な権限

- 自分が作成したフォーム（`created_by`が自分のID）には、`user_form_access`テーブルの設定に関わらずアクセス可能
- フォームの作成・更新・削除は、自分が作成したフォーム、または許可されたフォームに対してのみ可能

### system_adminの特別な権限

- 全フォームにアクセス可能（`form_access_restriction_enabled`の設定に関わらず）
- ユーザー管理機能へのアクセス
- ログアーカイブ機能へのアクセス
- フォームアーカイブ機能へのアクセス

## 注意事項

1. **パーミッションベースのチェック**: 多くのエンドポイントは`hasPermission()`メソッドでパーミッションベースのチェックを行います
2. **ロールベースのチェック**: 一部のエンドポイントは`hasRole()`メソッドでロールベースのチェックを行います
3. **リソースパーミッション**: フォームや回答へのアクセスは、操作パーミッションに加えて、リソースパーミッション（`user_form_access`テーブル）もチェックされます
4. **rootユーザー**: rootユーザー（`is_root=true`）は全権限を持ちますが、本表では除外しています（別表参照）
