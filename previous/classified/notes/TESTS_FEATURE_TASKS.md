# tests/Feature テスト改修・追加タスク一覧

## 現状サマリ

| 区分 | 対象 | 内容 | 状態 |
|------|------|------|------|
| 古い仕様 | ResponsesCsvExportTest | CSV ヘッダー・フィールド名のアサーションが実装と不一致 | 要改修 |
| 新規 | AdminUsersControllerTest | show() の created_by / updated_by 返却に対するテストなし | 要追加 |
| 新規 | LogsApiTest | GET /v1/logs/archives のルーティング・archives() のテストなし | 要追加 |
| 済 | ResponsesExportFlowTest | response_id → UTF-8 BOM アサーションに変更済み | 対応済 |

---

## A. ResponsesCsvExportTest（古い仕様の改修）

### 実装の前提（CsvExportService）

- **システムカラム**  
  - ヘッダーには**キー名**（`submission_id` 等）ではなく、`getSystemColumnLabel()` の**ラベル**を出力。  
  - デフォルト locale=ja: `回答ID`, `送信日時`, `フォームコード`, `ステータス`。
- **フィールドカラム**  
  - `getFieldCsvLabel()` の結果（`csv_label_json` → `options_json` → **`field_key`** の順でフォールバック）。  
  - **`f:` プレフィックスは使っていない**。  
  - 例: `field_key` が `name` → ヘッダー `name`、`category` の __label → `category__label`。

### タスク

| # | メソッド | 変更前（古い仕様） | 変更後（現行仕様） | 備考 |
|---|----------|-------------------|---------------------|------|
| A.1 | test_csv_export_value_mode | `submission_id` | `回答ID` | システム第1列。locale=ja 想定。 |
| A.2 | test_csv_export_value_mode | `submitted_at` | `送信日時` | 同上。 |
| A.3 | test_csv_export_value_mode | `form_code` | `フォームコード` | 同上。 |
| A.4 | test_csv_export_value_mode | `status` | `ステータス` | 同上。 |
| A.5 | test_csv_export_value_mode | `f:name` | `name` | フィールドは `field_key` またはそのラベル、`f:` なし。 |
| A.6 | test_csv_export_value_mode | `f:age` | `age` | 同上。 |
| A.7 | test_csv_export_label_mode | `f:category__label` | `category__label` | `f:` を削除。 |
| A.8 | test_csv_export_both_mode | `f:category` | `category` | 同上。 |
| A.9 | test_csv_export_both_mode | `f:category__label` | `category__label` | 同上。 |

**触らないもの**

- `test_csv_export_queues_job` … ヘッダー内容に依存していない。
- `test_csv_export_escapes_special_characters` … ヘッダー名のアサーションなし、エスケープ結果のみ。
- `test_csv_export_filters_by_form_id` … ヘッダー名に依存しない。
- データの存在確認（`(string) $submission->id`, `Test User`, `25`, `ビジネス`, `business` 等）は現状のままでよい。

---

## B. AdminUsersControllerTest（新規テスト）

### 背景

- `AdminUsersController::show()` の返却に `created_by`, `updated_by` を追加済み。
- `AdminUsersControllerTest` に `show()` のテストは存在しない。

### タスク

| # | 内容 | 対象 |
|---|------|------|
| B.1 | `test_show_returns_user_with_created_by_and_updated_by` を追加 | `AdminUsersControllerTest.php` |

**想定内容**

1. system_admin ユーザーを作成し、PAT を発行。
2. 別ユーザー（`created_by` / `updated_by` は null で可）を作成。
3. `GET /v1/system/admin-users/{id}` を実行。
4. `assertStatus(200)`。
5. `assertJsonStructure` で `data.user` に `created_by`, `updated_by` のキーが含まれることを確認。
   - 値は `null` でもよい（既存ユーザーやシーダー由来で未設定の想定）。

**参考**: 既存の `createSystemAdmin()`, `issueAdminPat()` を流用。Role の firstOrCreate は `setUp` で実施済み。

---

## C. LogsApiTest（新規テスト）

### 背景

- `GET /v1/logs/archives` が `/logs/{id}` にマッチして `show(int $id)` に `id="archives"` が渡り Type Error になっていた問題を、ルート順の変更で解消済み。
- `LogsApiTest` は `/v1/logs`, `/v1/logs/{id}` のみで、`/v1/logs/archives` のテストがない。

### タスク

| # | 内容 | 対象 |
|---|------|------|
| C.1 | `test_logs_archives_returns_200_and_archives_structure` を追加 | `LogsApiTest.php` |

**想定内容**

1. system_admin ロールをもつユーザーを作成（`archives()` 内で `requireSystemAdmin()` が呼ばれるため）。
2. PAT を発行。
3. `GET /v1/logs/archives?page=1&per_page=50` を実行。
4. `assertStatus(200)`。
5. `assertJsonStructure` で `data.archives` に `items`, `total`, `page`, `per_page` が含まれることを確認。
   - `items` が空配列でもよい（LogArchive が 0 件の想定）。

**補足**

- `LogsController::archives()` の返却形:  
  `['archives' => ['items' => ..., 'total' => ..., 'page' => ..., 'per_page' => ...]]`
- `LogsApiTest` に Role の付与や system_admin の作成がない場合は、`AdminUsersControllerTest::createSystemAdmin()` と同様のヘルパーを追加するか、`LogsApiTest` 内で Role を firstOrCreate してユーザーに attach する。

---

## D. 対応不要

| テスト | 理由 |
|--------|------|
| ResponsesExportFlowTest | `response_id` のアサーションを UTF-8 BOM に変更済み。 |
| その他 Feature テスト | `response_id`／`f:` プレフィックス／`submission_id` 等のキー名に依存しているのは `ResponsesCsvExportTest` のみ。 |

---

## 実施順の提案

1. **A** … ResponsesCsvExportTest のアサーション修正（既存失敗解消）。
2. **B** … AdminUsersControllerTest に show の created_by/updated_by テストを追加。
3. **C** … LogsApiTest に /logs/archives のテストを追加。

---

## 改修後の確認

- `php vendor/bin/phpunit tests/Feature/ResponsesCsvExportTest.php`
- `php vendor/bin/phpunit tests/Feature/System/AdminUsersControllerTest.php`
- `php vendor/bin/phpunit tests/Feature/LogsApiTest.php`

上記がすべて成功することを確認。
