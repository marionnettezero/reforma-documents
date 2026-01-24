# tests/ テストコード 現行ソース同期タスク一覧

## 現状サマリ（全テスト実行結果ベース）

| 結果 | 件数 | 主な要因 |
|------|------|----------|
| 成功 | 159 | - |
| エラー | 27 | Role 不在（ModelNotFoundException）、ファイルアップロードまわり |
| 失敗 | 6 | アサーション不一致（期待 400 で 200、例外メッセージ不一致など） |

**対象テストクラス（不具合あり）**

- `FormsApiTest` … 12 件（すべて Role 由来）
- `FormsAttachmentApiTest` … 10 件（Role + アップロード・実装の差異）
- `FormsNotificationApiTest` … 8 件（すべて Role 由来）
- `PdfGenerationServiceTest` … 4 件（例外メッセージ）
- その他 1 件（`test_upload_attachments_fails_when_attachment_type_not_uploaded_files` の期待 400 / 実 200）

---

## A. Role の事前作成（ModelNotFoundException 解消）

### 背景

- `RolePermissionsSeeder` は `Setting::set('roles.permissions', ...)` のみで、**Role レコードは作らない**。
- `Role::where('code', 'form_admin')->firstOrFail()` を使用しているテストで `ModelNotFoundException` が発生。
- `RoleSeeder` または `Role::firstOrCreate` で `form_admin` 等のロールを作成する必要がある。

### タスク

| # | 内容 | 対象 |
|---|------|------|
| A.1 | `prepare()` の**先頭**で `RoleSeeder` を実行する | `FormsApiTest` |
| A.2 | `prepare()` の**先頭**で `RoleSeeder` を実行する | `FormsAttachmentApiTest` |
| A.3 | `prepare()` の**先頭**で `RoleSeeder` を実行する | `FormsNotificationApiTest` |

**実装例**

```php
private function prepare(): void
{
    (new \Database\Seeders\RoleSeeder())->run();  // 追加: Role が firstOrFail より先に存在するようする
    config(['sanctum.expiration' => null]);
    // … 以下既存
}
```

**注意**

- `RoleSeeder` は `RoleCode` を使う。`RoleCode` がない、または `form_admin` 等と一致しない場合は、`AdminUsersControllerTest::setUp` と同様に `Role::firstOrCreate(['code' => 'form_admin', 'name' => 'フォーム管理者'])` を並べる方式でも可。
- `RolePermissionsSeeder` は `Setting` 用のため、`RoleSeeder` の有無に影響されない。既存の `(new RolePermissionsSeeder())->run()` はそのままでよい。

---

## B. FormsAttachmentApiTest（ファイルアップロード・実装との整合）

### 背景

1. **`postJson` とファイル**
   - `uploadPdfTemplate` / `uploadAttachments` は `multipart/form-data` 想定。`postJson` では `file` が正しく送れず、バリデーション 422 や、ジョブ内の「Temporary file has invalid size」に至る。

2. **`uploadPdfTemplate` と `form.attachment_type`**
   - 現状、`form.attachment_type !== 'pdf_template'` のときの 400 返却がない。バリデーション通過後にジョブを投入し、ジョブで失敗すると 500 になる。
   - テスト `test_upload_pdf_template_fails_when_attachment_type_not_pdf_template` は 400 を期待。

3. **`uploadAttachments` と `form.attachment_type`**
   - 現状、`form.attachment_type !== 'uploaded_files'` のときの 400 返却がない。`translation.attachment_type` を `uploaded_files` に上書きして処理しており、200 が返る。
   - テスト `test_upload_attachments_fails_when_attachment_type_not_uploaded_files` は 400 を期待。

### タスク（テスト側）

| # | メソッド | 内容 |
|---|----------|------|
| B.1 | `test_upload_pdf_template_success` | `postJson` をやめ、`post()` で `['file' => $file, 'locale' => 'ja']` を送る（multipart）。`Storage::fake` 時の ProcessFileUploadJob の実行結果が 0 バイト等で失敗する場合は、ジョブ投入と `job_id` のアサーションに留め、ジョブ内の process は別テスト or モックで検証する方針でも可。 |
| B.2 | `test_upload_pdf_template_fails_when_attachment_type_not_pdf_template` | `postJson` を `post()` に変更。`['file' => UploadedFile::fake()->create('template.pdf', 100, 'application/pdf'), 'locale' => 'ja']` で送る。**実装で `form.attachment_type` チェックを入れた場合** は 400 のまま。実装を入れない場合は、期待を 200 に変更するか、本タスクでは「実装に合わせて 400 を返す」前提で記載。 |
| B.3 | `test_upload_pdf_template_fails_when_file_not_pdf` | ファイルだけ変え、`post()` で送る。422 のアサーションはそのままでよい。 |
| B.4 | `test_upload_attachments_success` | `postJson` を `post()` に変更。`['files' => [$file1, $file2], 'locale' => 'ja']` で送る。ジョブが同期的に失敗する場合の扱いは B.1 と同様。 |
| B.5 | `test_upload_attachments_fails_when_attachment_type_not_uploaded_files` | 期待を **実装に合わせる**。実装に `form.attachment_type === 'uploaded_files'` チェックを入れるなら 400 のまま。**入れない場合は** `assertStatus(200)` に変更し、`code` のアサーションを外す。 |
| B.6 | `test_upload_attachments_fails_when_too_many_files` | ファイル数以外は `post()` に統一する程度で可。422 はそのまま。 |

**触らないもの**

- `test_delete_attachment_*` の URL や `attachment_files` の構造は、現行 `deleteAttachment` の実装に合わせる（`Form` / `FormTranslation` の差も実装準拠）。
- `test_update_form_with_attachment_settings` / `test_update_form_clears_files_when_switching_attachment_type` は CRUD のみ。Role 解消後は Role まわり以外の変更は最小限でよい。

### タスク（実装側・推奨）

| # | 対象 | 内容 |
|---|------|------|
| B.7 | `FormsController::uploadPdfTemplate` | `Form::findOrFail($id)` の直後、`$form->attachment_type !== 'pdf_template'` のとき `ApiResponse::error(..., 400, ApiErrorCode::VALIDATION_FAILED, ...)` を返す。`form.attachment_enabled` が false のときも 400 にするかは仕様次第（必要なら同様に追加）。 |
| B.8 | `FormsController::uploadAttachments` | `Form::findOrFail($id)` の直後、`$form->attachment_type !== 'uploaded_files'` のとき上記と同様に 400 を返す。`form.attachment_enabled` も同様に検討。 |

---

## C. PdfGenerationServiceTest（例外メッセージ）

### 背景

- `PdfGenerationService::generate()` の先頭で `extension_loaded('pdflib')` をチェックし、未ロードのとき `'PDFLib extension is not loaded'` を投げる。
- そのため、`attachment_enabled` / `attachment_type` / `pdf_template_path` / テンプレート存在のチェックより**先に**例外になり、以下の 4 テストで `expectExceptionMessage` が失敗する。
  - `test_generate_throws_exception_when_attachment_not_enabled`
  - `test_generate_throws_exception_when_attachment_type_not_pdf_template`
  - `test_generate_throws_exception_when_template_path_not_set`
  - `test_generate_throws_exception_when_template_not_exists`

### タスク

| # | 方針 | 内容 |
|---|------|------|
| C.1 | **実装の順序変更（推奨）** | `PdfGenerationService::generate()` 内で、`extension_loaded('pdflib')` のチェックを、`attachment_enabled` / `attachment_type` / `pdf_template_path` / テンプレート存在の**後**に移動する（例: `generatePdf()` を呼ぶ直前）。これで PDFLib 未ロード環境でも、上記 4 テストは期望するメッセージで例外を検証できる。 |
| C.2 | **テスト側で吸収する場合** | 実装を変えない場合は、`extension_loaded('pdflib')` が true のときのみ上記 4 テストを実行し、false のときは `$this->markTestSkipped('PDFLib extension is not loaded');` とする。 |

---

## D. その他・確認のみ

| テスト / 現象 | 対応 |
|--------------|------|
| `test_upload_pdf_template_success` 等でジョブ同期実行時に「Temporary file has invalid size」 | `Storage::fake` + `UploadedFile::fake` の組み合わせで、ProcessFileUploadJob が参照するパスに 0 バイトになることがある。`post()` 化しても続く場合は、当該テストはジョブ投入と `job_id` までに絞る、または `FileUploadQueueTest` 側でジョブ実処理を検証する。 |
| `test_upload_attachments_fails_when_attachment_type_not_uploaded_files` で 200 が返る | 実装に B.8 の `form.attachment_type` チェックを入れず、テストを現行実装に合わせる場合は、B.5 のとおり期待を 200 に変更。 |
| `ResponsesExportFlowTest` 等で「ProgressJob not found」ログ | 環境や実行順で job_id の解決が遅れる可能性。再現しなければ、ログのみの事象として一旦保留。 |

---

## E. 実施順の提案

1. **A** … Role 作成（A.1〜A.3）。FormsApi / FormsAttachment / FormsNotification の ModelNotFoundException 解消。
2. **C** … PdfGenerationService のチェック順序変更（C.1）またはスキップ（C.2）。PdfGenerationServiceTest の 4 失敗解消。
3. **B（実装）** … B.7, B.8 の `form.attachment_type` チェック追加。未実装なら B.5 は「期待 200」に変更。
4. **B（テスト）** … B.1〜B.6 の `postJson` → `post()` 化および期待値の調整。

---

## F. 改修後の確認

以下がすべて成功することを確認。

```bash
php vendor/bin/phpunit tests/Feature/FormsApiTest.php
php vendor/bin/phpunit tests/Feature/FormsAttachmentApiTest.php
php vendor/bin/phpunit tests/Feature/FormsNotificationApiTest.php
php vendor/bin/phpunit tests/Unit/PdfGenerationServiceTest.php
```

必要に応じて:

```bash
php vendor/bin/phpunit
```

---

## G. 参考

- **Role 作成**  
  - `database/seeders/RoleSeeder.php`（RoleCode 使用）  
  - `tests/Feature/System/AdminUsersControllerTest.php` の `setUp`（`Role::firstOrCreate`）
- **添付まわり実装**  
  - `app/Http/Controllers/Api/V1/FormsController.php` の `uploadPdfTemplate`, `uploadAttachments`
- **PDF 生成**  
  - `app/Services/PdfGenerationService.php` の `generate()` 先頭のチェック順
