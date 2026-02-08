# フォーム複製・エクスポート／インポートのデータ欠損確認

フォームの**複製**（copy-with-new-code）と**エクスポート→インポート**において、データ損失が発生しないかを実装対比で確認した結果をまとめる。

---

## 1. エクスポート→インポート

### 1.1 確認方法

- **エクスポート**: `FormExportJob::buildExportData()` が `form.toArray()` / `translations.toArray()` / `fields.toArray()` から id・form_id・日付のみ除外して出力。ファイルは PDF テンプレート・添付（フォーム／翻訳別）・ロゴを実体ごと ZIP に含める。
- **インポート**: `FormImportJob` の `createForm` / `createTranslations` / `createFields` / `copyFiles` が、エクスポート JSON の `form` / `translations` / `fields` / `files` を新規 form_id で再作成。

### 1.2 結果：データ損失なし

| 対象 | エクスポート | インポート | 備考 |
|------|--------------|------------|------|
| Form | toArray() 全項目（id/日付除く） | createForm で全項目を設定。pdf_template_path / attachment_files_json / logo_path は copyFiles で新パスに差し替え | 問題なし |
| FormTranslation | toArray() 全項目（id/form_id/日付除く） | createTranslations で全項目を設定。attachment_files_json は copyFiles で翻訳別に更新 | 問題なし |
| FormField | toArray() 全項目（id/form_id/日付除く） | createFields で field_key, type, step_key, group_key, sort_order, is_required, options_json, visibility_rule, required_rule, step_transition_rule, **pdf_block_key, pdf_page_number, computed_rule, csv_export_enabled, csv_label_json** をすべて反映 | 問題なし |
| ファイル | form の pdf_template_path、attachment_files_json、各翻訳の attachment_files_json、logo_path の実体を ZIP に格納 | copyFiles で `PdfStorageService::storeTemplate/storeAttachment`・`LogoStorageService::store` により**新 form_id 基準のパス**に保存し、form / 翻訳の該当カラムを更新 | 新 id・新パスで考慮済み |

エクスポート／インポート間で、フォーム・翻訳・項目・ファイルとも欠落はなく、インポート後は新しい form_id に合わせたパスになっている。

---

## 2. フォーム複製（copy-with-new-code）

### 2.1 挙動の整理

- **フォーム／翻訳**: 既存フォームの属性をそのまま新フォームにコピー。`pdf_template_path`・`attachment_files_json`・`logo_path` は**パスをそのまま**引き継ぐ（ファイル実体の再コピーはしない）。＝ 複製フォームは元フォームと同じストレージパスを参照する。
- **項目**: リクエストの `fields` をそのまま新フォームの FormField として保存。  
  `GET /v1/forms/{id}/fields?include_rules=true` で取得した内容をそのまま送る前提。

### 2.2 修正前のデータ損失（項目）

複製時、バックエンドは `fields` のうち次の項目を**バリデーションにも create にも含めておらず**、フロントから送られても捨てられていた。

- `pdf_block_key`
- `pdf_page_number`
- `computed_rule`
- `csv_export_enabled`
- `csv_label_json`

### 2.3 実施した修正（対応済み）

`FormsController::copyWithNewCode` に以下を反映済み。

1. **バリデーション**に追加  
   `fields.*.pdf_block_key` / `fields.*.pdf_page_number` / `fields.*.computed_rule` / `fields.*.csv_export_enabled` / `fields.*.csv_label_json` を nullable 等で許可。
2. **FormField::create** に渡す配列に上記 5 項目を追加。  
   `csv_export_enabled` は未送信時に `true` でフォールバック。

これにより、`include_rules=true` 付きフィールド一覧をそのまま複製に渡した場合、項目まわりのデータ損失は発生しない。

### 2.4 複製時のファイルまわり（仕様としての注意）

複製では、PDF テンプレート・添付・ロゴの**ストレージパスをそのまま**新フォームに設定している。ファイルの実体は複製せず、元フォームと同一パスを共有する。

- 元フォームを削除したり、ストレージを整理したりすると、複製フォーム側の表示・ダウンロードが壊れる可能性がある。
- 「完全に独立した複製」が必要な場合は、一度エクスポートしてから別フォームコードでインポートする運用にすると、必ず新 form_id 配下のファイルとして復元される。

---

## 3. テーブル定義との照合

マイグレーション（`create_forms_table`, `create_form_translations_table`, `create_form_fields_table`, `add_ack_view_json_to_forms_table`）のカラムと、エクスポート・インポート・複製で扱う項目を照合した。

### 3.1 forms テーブル

| カラム（id/timestamps/deleted_at 除く） | エクスポート | インポート | 複製 |
|----------------------------------------|--------------|------------|------|
| code | ✓ toArray | ✓ formCode として適用 | ✓ new_code |
| status, public_period_*, answer_period_* | ✓ | ✓ | ✓ |
| attachment_enabled, attachment_type, pdf_template_path, attachment_files_json | ✓ | ✓（パスは copyFiles で上書き） | ✓（パスそのまま） |
| theme_id, theme_tokens, custom_style_config | ✓ | ✓ | ✓ |
| logo_path, logo_json | ✓ | ✓（パスは copyFiles で上書き） | ✓（パスそのまま） |
| layout_width_json, ack_view_json | ✓ | ✓ | ✓ |
| step_group_structure, csv_system_columns_json | ✓ | ✓ | ✓（step_group_structure はリクエストから） |
| notification_user_*, notification_admin_* | ✓ | ✓ | ✓ |
| created_by, updated_by | ✓ | ✓ ともに userId | ✓ **updated_by を追加済み**（従来抜け） |
| deleted_by | ✓ | 新規のため未設定（null） | 新規のため未設定（null） |

### 3.2 form_translations テーブル

| カラム（id/form_id/timestamps 除く） | エクスポート | インポート | 複製 |
|--------------------------------------|--------------|------------|------|
| locale, title, description | ✓ | ✓ | ✓ |
| notification_user_email_*, notification_admin_email_* | ✓ | ✓ | ✓ |
| attachment_description, attachment_type, attachment_files_json | ✓ | ✓（attachment_files_json は copyFiles で上書き） | ✓ |

### 3.3 form_fields テーブル

| カラム（id/form_id/timestamps 除く） | エクスポート | インポート | 複製 |
|--------------------------------------|--------------|------------|------|
| field_key, type, step_key, group_key, sort_order, is_required | ✓ | ✓ | ✓ |
| options_json, visibility_rule, required_rule, step_transition_rule | ✓ | ✓ | ✓ |
| computed_rule, pdf_block_key, pdf_page_number | ✓ | ✓ | ✓ |
| csv_export_enabled, csv_label_json | ✓ | ✓（未指定時 **true** に統一済み。テーブル default と一致） | ✓ |

### 3.4 今回の修正（テーブル照合で判明した抜け）

- **複製時の `forms.updated_by`**: 新規作成時に `created_by` のみ設定し `updated_by` が未設定で null になっていた。`'updated_by' => $user->id` を追加済み。
- **インポート時の `form_fields.csv_export_enabled` デフォルト**: 未指定時に `false` になっており、テーブル定義・他API（フォールバック `true`）と不一致だった。`?? true` に統一済み。

---

## 4. 参照した実装

| 処理 | ファイル・メソッド |
|------|--------------------|
| エクスポート | `FormExportJob::buildExportData()` |
| インポート | `FormImportJob::createForm`, `createTranslations`, `createFields`, `copyFiles` |
| 複製 | `FormsController::copyWithNewCode()` |
| フィールド一覧（複製用） | `FormsFieldsController::index()`（`include_rules=true` 時に pdf_block_key, pdf_page_number, computed_rule, csv_export_enabled, csv_label_json を返却） |
| テーブル定義 | `database/migrations/2026_01_01_000003_create_forms_table.php`, `000004_create_form_translations_table.php`, `000005_create_form_fields_table.php`, `2026_01_24_000001_add_ack_view_json_to_forms_table.php` |

---

## 5. 結論

- **エクスポート→インポート**: フォーム・翻訳・項目・ファイルのいずれもテーブル定義と照合して欠損はなく、インポート時は新しい form_id に合わせたパスで保存されている。`csv_export_enabled` の未指定時デフォルトをテーブルどおり `true` に統一済み。
- **フォーム複製**: 項目の `pdf_block_key` / `pdf_page_number` / `computed_rule` / `csv_export_enabled` / `csv_label_json` が保存されない不具合を修正済み。フォームの `updated_by` が未設定だった抜けを修正済み。ファイルは従来どおり「参照の引き継ぎ」のため、完全な独立複製が必要な場合はエクスポート→インポートを利用すること。
