# FormsApiTest / FormsNotificationApiTest 残存不具合タスク

## 概要

TESTS_ALIGNMENT_TASKS（A〜C, B）対応後も、FormsApiTest と FormsNotificationApiTest に Failure が残る。本タスクで切り出して対応する。

---

## 現状（抜粋）

| テスト | 件数 | 主な要因 |
|--------|------|----------|
| FormsApiTest | 6 Failure | `ApiErrorCode::VALIDATION_ERROR` 未定義（→ 500） |
| FormsNotificationApiTest | 5 Failure | 上記に加え、`notification_user_email_subject` 等の JSON キー不整合 |

---

## A. ApiErrorCode::VALIDATION_ERROR の誤記（実装バグ）

### 背景

- `App\Support\ApiErrorCode` は `VALIDATION_FAILED` を定義しており、**`VALIDATION_ERROR` は存在しない**。
- `FormsController::update()` 内で `ApiErrorCode::VALIDATION_ERROR` を参照しており、該当パスで 500 が返る。

### タスク

| # | 対象 | 内容 |
|---|------|------|
| A.1 | `FormsController.php` 行 524 | `ApiErrorCode::VALIDATION_ERROR` を `ApiErrorCode::VALIDATION_FAILED` に修正。 |
| A.2 | `FormsController.php` 行 571 | 同上。 |

**備考**: `->withErrors(...)` の呼び出しは `ApiResponse::error()` の戻り値に対して行われている。`ApiResponse::error` が JsonResponse を返すか、withErrors を持つかは実装次第。修正は enum の差し替えのみとする。

---

## B. FormsController のフォーム取得レスポンス構造とテストのアサーション

### 背景

- `test_get_form_includes_notification_settings` が `data.form` に `notification_user_email_subject` のキーがあることを期待。
- 実装の `show()` / `update()` の返却が、通知まわりを `form` 直下ではなく `form.translations[].notification_*` や別構造で返している可能性。

### タスク

| # | 内容 |
|---|------|
| B.1 | `FormsController::show()` の返却 JSON 構造を確認し、`data.form` または `data.form.translations[].*` に `notification_user_email_subject` 等が含まれるか確認。 |
| B.2 | 実装に合わせて、`FormsNotificationApiTest::test_get_form_includes_notification_settings` の `assertJsonStructure` を修正する。キーが `translations[].notification_user_email_subject` の場合はそのパスでアサート。 |

---

## 実施順

1. **A** … `VALIDATION_ERROR` → `VALIDATION_FAILED` の修正（A.1, A.2）。
2. **B** … show の返却構造を確認のうえ、テストの assertJsonStructure を実装に合わせる（B.1, B.2）。

---

## 改修後の確認

```bash
php vendor/bin/phpunit tests/Feature/FormsApiTest.php
php vendor/bin/phpunit tests/Feature/FormsNotificationApiTest.php
```

---

## 実施メモ（B およびテスト整合）

### B 実施結果

- **B.1**: `show()` の返却では `notification_user_email_subject` / `notification_admin_email_subject` は **`data.form` 直下になく、`data.translations[].*` にある** ことを確認。
- **B.2**: `test_get_form_includes_notification_settings` の `assertJsonStructure` を `data.form` から subject を外し、`data.translations.*.notification_user_email_subject` と `assertJsonPath('data.translations.0.notification_user_email_subject', ...)` に合わせて修正。あわせて `FormTranslation` を事前作成。

### 追加で実施したテスト修正（実装との整合）

| 要因 | 対応 |
|------|------|
| **`is_public`** | `forms` テーブルにカラムなし。`test_forms_store` / `test_forms_show` / `test_forms_update` から送信・assert・`assertDatabaseHas` の `is_public` を削除。 |
| **`notification_user_email_subject` / `*_template`** | Form ではなく **FormTranslation** の属性。`test_forms_update_notification_settings` で `translations` 経由で送信し、事前に `FormTranslation` を作成。`test_update_notification_user_settings_success` では form 直下の subject/template の送信・assert を削除。 |
| **`notification_admin_email_subject` / `*_template`** | 同上。`test_update_notification_admin_settings_success` から form 直下の送信・assert を削除。 |
| **`notification_user_enabled: true` 時の必須** | `notification_user_email_from` と `notification_user_email_reply_to` が必須。`test_forms_update_notification_enables_email_fields_auto_creation` / `test_forms_update_notification_does_not_create_duplicate_email_fields` / `test_auto_add_email_fields_*` / `test_do_not_add_email_fields_*` の put にこれらを追加。 |
