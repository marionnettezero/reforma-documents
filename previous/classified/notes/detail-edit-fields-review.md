# 各画面詳細/編集項目の確認結果

**作成日**: 2026-01-17  
**目的**: 各画面の詳細表示・編集機能で、API仕様書と実装を照合し、不足項目を洗い出す

---

## S-02: アカウント一覧（AccountListPage）

### API仕様（GET /v1/system/admin-users/{id}）
**返却フィールド**:
- `id` (integer)
- `name` (string)
- `email` (string)
- `status` (string: active, suspended, invited, deleted)
- `roles` (array: SYSTEM_ADMIN, FORM_ADMIN, LOG_ADMIN)
- `is_root` (boolean) - root権限フラグ
- `form_create_limit_enabled` (boolean) - フォーム作成制限有効化フラグ
- `form_create_limit` (integer|null) - フォーム作成制限数
- `created_at` (string, ISO8601)
- `updated_at` (string, ISO8601)

### 現在の実装状況

#### 詳細表示（showDetailModal）
**表示項目**:
- ✅ ID
- ✅ 名前
- ✅ メールアドレス
- ✅ ステータス
- ✅ ロール
- ✅ 作成日時
- ✅ 招待日時（invited_atがある場合）

**不足項目**:
- ❌ `updated_at` - 更新日時
- ❌ `is_root` - root権限フラグ（root-only表示推奨）
- ❌ `form_create_limit_enabled` - フォーム作成制限有効化フラグ
- ❌ `form_create_limit` - フォーム作成制限数

#### 編集（showEditModal）
**編集項目**:
- ✅ 名前
- ✅ メールアドレス
- ✅ ステータス（active, suspended）
- ✅ ロール

**不足項目**:
- ❌ `is_root` - root権限フラグ（root-only編集、root権限が必要）
- ❌ `form_create_limit_enabled` - フォーム作成制限有効化フラグ
- ❌ `form_create_limit` - フォーム作成制限数

### API仕様（PUT /v1/system/admin-users/{id}）
**更新可能フィールド**:
- `name` (nullable, string, max:255)
- `status` (nullable, in:active,suspended)
- `roles` (required, array, min:1, max:1)
- `is_root` (nullable, boolean) - root権限が必要
- `form_create_limit_enabled` (nullable, boolean)
- `form_create_limit` (nullable, integer, min:1)

**注意事項**:
- `is_root`の変更はroot権限が必要
- `email`は更新不可（API仕様に含まれていない）

---

## S-03: テーマ一覧（ThemeListPage）

### API仕様（GET /v1/system/themes/{id}）
**返却フィールド**:
- `id` (integer)
- `code` (string) - テーマコード（編集不可）
- `name` (string) - テーマ名
- `description` (string|null) - 説明
- `theme_tokens` (object) - テーマトークン（CSS変数）
- `is_preset` (boolean) - プリセットフラグ（編集不可）
- `is_active` (boolean) - 有効フラグ
- `created_by` (integer|null) - 作成者ID
- `created_at` (string, ISO8601)
- `updated_at` (string, ISO8601)

### 現在の実装状況
**詳細・編集機能は未実装**

### 実装すべき項目

#### 詳細表示
**表示項目**:
- `id` - テーマID
- `code` - テーマコード（読み取り専用）
- `name` - テーマ名
- `description` - 説明
- `theme_tokens` - テーマトークン（JSON表示または視覚化）
- `is_preset` - プリセットフラグ（Badge表示）
- `is_active` - 有効フラグ（Badge表示）
- `created_by` - 作成者（ユーザー名表示）
- `created_at` - 作成日時
- `updated_at` - 更新日時
- `usage_count` - 使用状況（GET /v1/system/themes/{id}/usageから取得）

#### 編集
**編集項目**:
- `name` - テーマ名（必須）
- `description` - 説明（任意）
- `theme_tokens` - テーマトークン（JSONエディタまたは視覚的エディタ）
- `is_active` - 有効フラグ（チェックボックス）

**注意事項**:
- `code`は編集不可（一意制約のため）
- `is_preset`は編集不可（プリセットテーマはroot-onlyで更新可能だが、フラグ自体は変更不可）
- プリセットテーマの更新はroot-only権限が必要

### API仕様（PUT /v1/system/themes/{id}）
**更新可能フィールド**:
- `name` (nullable, string, max:255)
- `description` (nullable, string)
- `theme_tokens` (nullable, object) - スキーマ準拠
- `is_active` (nullable, boolean)

---

## F-01: フォーム一覧（FormListPage）

### API仕様（GET /v1/forms/{id}）
**返却フィールド**:
- `id` (integer)
- `code` (string) - フォームコード（編集不可）
- `status` (string: draft, published, closed)
- `is_public` (boolean) - 公開フラグ
- `attachment_enabled` (boolean) - 添付ファイル有効化
- `attachment_type` (string|null: pdf_template, uploaded_files)
- `pdf_template_path` (string|null) - PDFテンプレートパス
- `attachment_files` (array|null) - 添付ファイル一覧
- `notification_user_enabled` (boolean) - ユーザー通知有効化
- `notification_user_email_template` (string|null) - ユーザー通知テンプレート
- `notification_user_email_subject` (string|null) - ユーザー通知件名
- `notification_user_email_from` (string|null) - ユーザー通知送信元
- `notification_user_email_reply_to` (string|null) - ユーザー通知返信先
- `notification_user_email_cc` (array|null) - ユーザー通知CC
- `notification_user_email_bcc` (array|null) - ユーザー通知BCC
- `notification_admin_enabled` (boolean) - 管理者通知有効化
- `notification_admin_user_ids` (array|null) - 管理者通知送信先ユーザーID一覧
- `notification_admin_email_template` (string|null) - 管理者通知テンプレート
- `notification_admin_email_subject` (string|null) - 管理者通知件名
- `notification_admin_email_from` (string|null) - 管理者通知送信元
- `notification_admin_email_reply_to` (string|null) - 管理者通知返信先
- `theme_id` (integer|null) - テーマID
- `theme` (object|null) - テーマ情報（theme_idが指定されている場合）
- `theme_tokens` (object|null) - テーマトークン（解決済み）
- `created_by` (integer|null) - 作成者ID
- `created_at` (string, ISO8601)
- `updated_at` (string, ISO8601)
- `translations` (array) - 多言語翻訳情報
  - `id` (integer)
  - `form_id` (integer)
  - `locale` (string: ja, en)
  - `title` (string)
  - `description` (string|null)

### 現在の実装状況
**詳細・編集機能は未実装**

### 実装すべき項目

#### 詳細表示
**表示項目**:
- `id` - フォームID
- `code` - フォームコード（読み取り専用）
- `status` - ステータス（Badge表示）
- `is_public` - 公開フラグ（Badge表示）
- `translations` - 多言語翻訳情報（locale別表示）
- `attachment_enabled` - 添付ファイル有効化
- `attachment_type` - 添付ファイルタイプ
- `notification_user_enabled` - ユーザー通知有効化
- `notification_admin_enabled` - 管理者通知有効化
- `theme_id` / `theme` - テーマ情報
- `created_by` - 作成者（ユーザー名表示）
- `created_at` - 作成日時
- `updated_at` - 更新日時
- `response_count` - 回答数（一覧から取得可能）

#### 編集
**編集項目**:
- `status` - ステータス（draft, published, closed）
- `is_public` - 公開フラグ（チェックボックス）
- `translations` - 多言語翻訳情報（locale別編集）
  - `title` (必須)
  - `description` (任意)
- `attachment_enabled` - 添付ファイル有効化（チェックボックス）
- `attachment_type` - 添付ファイルタイプ（選択）
- `notification_user_enabled` - ユーザー通知有効化（チェックボックス）
- `notification_user_email_template` - ユーザー通知テンプレート（テキストエリア）
- `notification_user_email_subject` - ユーザー通知件名（テキスト入力）
- `notification_user_email_from` - ユーザー通知送信元（メールアドレス入力）
- `notification_user_email_reply_to` - ユーザー通知返信先（メールアドレス入力）
- `notification_user_email_cc` - ユーザー通知CC（配列入力）
- `notification_user_email_bcc` - ユーザー通知BCC（配列入力）
- `notification_admin_enabled` - 管理者通知有効化（チェックボックス）
- `notification_admin_user_ids` - 管理者通知送信先ユーザーID一覧（ユーザー選択）
- `notification_admin_email_template` - 管理者通知テンプレート（テキストエリア）
- `notification_admin_email_subject` - 管理者通知件名（テキスト入力）
- `notification_admin_email_from` - 管理者通知送信元（メールアドレス入力）
- `notification_admin_email_reply_to` - 管理者通知返信先（メールアドレス入力）
- `theme_id` - テーマID（テーマ選択）
- `theme_tokens` - テーマトークン（フォーム固有のカスタマイズ）

**注意事項**:
- `code`は編集不可（一意制約のため）
- `created_by`は編集不可
- ファイルアップロード（PDFテンプレート、添付ファイル）は別API（POST /v1/forms/{id}/attachment/*）

### API仕様（PUT /v1/forms/{id}）
**更新可能フィールド**:
- `status` (nullable, in:draft,published,closed)
- `is_public` (nullable, boolean)
- `attachment_enabled` (nullable, boolean)
- `attachment_type` (nullable, in:pdf_template,uploaded_files)
- `notification_user_enabled` (nullable, boolean)
- `notification_user_email_template` (nullable, string)
- `notification_user_email_subject` (nullable, string, max:255)
- `notification_user_email_from` (nullable, email, max:255)
- `notification_user_email_reply_to` (nullable, email, max:255)
- `notification_user_email_cc` (nullable, array)
- `notification_user_email_cc.*` (email, max:255)
- `notification_user_email_bcc` (nullable, array)
- `notification_user_email_bcc.*` (email, max:255)
- `notification_admin_enabled` (nullable, boolean)
- `notification_admin_user_ids` (nullable, array)
- `notification_admin_user_ids.*` (integer, exists:users,id)
- `notification_admin_email_template` (nullable, string)
- `notification_admin_email_subject` (nullable, string, max:255)
- `notification_admin_email_from` (nullable, email, max:255)
- `notification_admin_email_reply_to` (nullable, email, max:255)
- `translations` (nullable, array)
- `translations.*.locale` (required_with:translations, string, in:ja,en)
- `translations.*.title` (required_with:translations, string, max:255)
- `translations.*.description` (nullable, string)
- `theme_id` (nullable, integer, exists:themes,id,where:is_active,true)
- `theme_tokens` (nullable, object)

---

## まとめ

### S-02: アカウント一覧（実装済み、不足項目あり）
**不足項目**:
1. 詳細表示: `updated_at`, `is_root`, `form_create_limit_enabled`, `form_create_limit`
2. 編集: `is_root`（root-only）, `form_create_limit_enabled`, `form_create_limit`

### S-03: テーマ一覧（未実装）
**実装が必要**: 詳細表示・編集機能全体

### F-01: フォーム一覧（未実装）
**実装が必要**: 詳細表示・編集機能全体（多数のフィールド）

---

## 優先度

### 高優先度
1. **S-02: アカウント一覧の不足項目追加**（既存機能の完成）
   - `form_create_limit_enabled`, `form_create_limit`の表示・編集
   - `updated_at`の表示
   - `is_root`の表示（root-only表示推奨）

### 中優先度
2. **S-03: テーマ一覧の詳細・編集機能実装**
3. **F-01: フォーム一覧の詳細・編集機能実装**（多数のフィールドがあるため、段階的実装推奨）
