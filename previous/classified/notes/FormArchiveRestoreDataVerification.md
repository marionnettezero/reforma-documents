# フォームアーカイブ・復元のデータ欠損確認

フォーム一覧の**アーカイブ**と、フォームアーカイブ一覧からの**復元**において、データ損失が発生しないかをテーブル定義と実装の照合で確認した結果をまとめる。

---

## 1. アーカイブの仕様

- **FormArchiveJob**: フォームと回答データを JSON（form.json, translations.json, fields.json, submissions.json, submission_values.json）および metadata.json（ファイル一覧含む）として一時ディレクトリに書き出し、ZIP 化して S3 に保存。その後、DB のフォーム・翻訳・項目・送信・送信値を物理削除し、`form_archives` に記録する。
- **アーカイブに含まれるファイル**: PDF テンプレート、添付ファイル（フォーム／翻訳別）、ロゴ、生成済みPDF（各 submission）、ユーザアップロードファイル（file フィールド）。

---

## 2. 復元の仕様

- **FormArchiveRestoreJob**: S3 から ZIP を取得して展開し、上記 JSON を読み、新規 form_id で forms / form_translations / form_fields / submissions / submission_values を再作成。metadata.files に基づき pdf_template / attachment / logo / **generated_pdf** / **user_uploaded_file** を新パスにコピーする。ユーザアップロードファイルは FormFileStorageService で新 form_id・新 submission_id 配下に保存し、submission_values の value_json.path を新パスに差し替える。

---

## 3. テーブル定義との照合と今回の修正

### 3.1 forms / form_translations / form_fields

アーカイブは `form.toArray()` / `translations.toArray()` / `fields.toArray()` から id・form_id・日付のみ除外して出力。復元の createForm / createTranslations / createFields は FormImportJob と同様に全項目を設定。

- **form_fields.csv_export_enabled**: 復元時の未指定デフォルトが `false` になっており、テーブル default・FormImportJob と不一致だった。**`?? true` に統一済み。**

### 3.2 submissions テーブル

| カラム（id/form_id/timestamps 除く） | アーカイブ | 復元 |
|--------------------------------------|------------|------|
| status | ✓ toArray | ✓ |
| locale | ✓ toArray | ✓ **追加済み**（従来抜け） |
| confirm_token, confirm_token_expires_at | ✓ | ✓ |

- **アーカイブでの submission.id**: 復元時に「旧 submission_id → 新 submission_id」のマッピングに必要なため、**id を消さずに保存するよう修正済み。**（従来は unset していたため、復元で submission_values をどの submission に紐づけるか判定できなかった。）
- **submission.locale**: 復元の createSubmissions で **`locale` を設定するよう追加済み。**

### 3.3 submission_values テーブル

| カラム（id/submission_id/timestamps 除く） | アーカイブ | 復元 |
|-------------------------------------------|------------|------|
| field_key, field_label_snapshot, value_json, label_json | ✓ | ✓ |

- **アーカイブでの submission_id**: 復元時に submissionIdMap で新 id に差し替えるため、**submission_id を消さずに保存するよう修正済み。**（従来は unset していた。）

### 3.4 フォームコード重複時の上書き

- **handleFormCode**: 重複かつ「上書き」時に論理削除だけでは code が解放されず、後の create でユニーク違反になっていた。**`Form::withTrashed()->where('code', $code)->forceDelete()` で物理削除するよう修正済み。**

### 3.5 復元で扱うファイル種別

| type | アーカイブ | 復元 |
|------|------------|------|
| pdf_template | ✓ 実体をZIPに含める | ✓ 新 form_id のパスに保存 |
| attachment（form/翻訳別） | ✓ | ✓ |
| logo | ✓ | ✓ |
| generated_pdf | ✓ 実体をZIPに含める | ✓ **対応済み**（copyFiles で PdfStorageService::storeOutput により新 submission_id で保存） |
| user_uploaded_file | ✓ 実体をZIPに含める | ✓ **対応済み**（copyFiles で FormFileStorageService::store により新 form_id/submission_id で保存。復元後に updateSubmissionValuePaths で value_json.path を新パスに差し替え） |

---

## 4. form_archives テーブル（メタデータ用）

アーカイブ一覧・復元トリガー用。カラムは form_id, form_code, archive_path, archive_size, archived_at, archived_by, metadata_json, timestamps。  
FormArchiveJob の `FormArchive::create` では上記をすべて設定しているため、抜けはない。

---

## 5. 今回の修正まとめ

| 対象 | 内容 |
|------|------|
| FormArchiveJob | submission から id を unset しない。submission_value から submission_id を unset しない。 |
| FormArchiveRestoreJob handleFormCode | 重複かつ上書き時は `forceDelete` で code を解放。 |
| FormArchiveRestoreJob createFields | csv_export_enabled の未指定時を `?? true` に統一。 |
| FormArchiveRestoreJob createSubmissions | `locale` を設定するよう追加。 |
| FormArchiveRestoreJob copyFiles | generated_pdf を PdfStorageService::storeOutput で新 submission_id に保存。user_uploaded_file を FormFileStorageService::store で新 form_id/submission_id に保存し、旧path→新path のマッピングを返す。 |
| FormArchiveRestoreJob updateSubmissionValuePaths | copyFiles 後に呼び出し、復元した submission_values の value_json.path をユーザアップロードの新パスに差し替え。 |

---

## 6. 参照した実装

| 処理 | ファイル・メソッド |
|------|--------------------|
| アーカイブ | `FormArchiveJob::buildArchiveData()`, `createZipFile()`, `uploadToS3()` |
| 復元 | `FormArchiveRestoreJob::createForm`, `createTranslations`, `createFields`, `createSubmissions`, `createSubmissionValues`, `copyFiles()`, `updateSubmissionValuePaths()`, `handleFormCode()` |
| 復元時のファイル保存 | `PdfStorageService::storeOutput`（generated_pdf）, `FormFileStorageService::store`（user_uploaded_file） |
| テーブル定義 | `create_forms_table`, `create_form_translations_table`, `create_form_fields_table`, `add_ack_view_json_to_forms_table`, `create_submissions_tables`, `add_locale_to_submissions_table`, `create_other_tables`（form_archives） |

---

## 7. 結論

- **アーカイブ**: forms / form_translations / form_fields は toArray ベースで全データを出力。submissions は **id を残す**、submission_values は **submission_id を残す** ように変更済み。PDF テンプレート・添付・ロゴ・生成済みPDF・ユーザアップロードは実体を ZIP に含める。
- **復元**: フォーム・翻訳・項目はテーブルどおり復元。送信は **locale** を追加済み。送信値は submission_id マッピングにより正しい submission に紐づく（アーカイブで submission_id を残す修正により解消）。フォームコード重複かつ上書き時は **forceDelete** で code を解放。csv_export_enabled のデフォルトは **true** に統一。
- **ファイル復元**: pdf_template / attachment / logo に加え、**generated_pdf**（PdfStorageService::storeOutput で新 submission_id に保存）と **user_uploaded_file**（FormFileStorageService::store で新 form_id/submission_id に保存し、updateSubmissionValuePaths で value_json.path を新パスに差し替え）も復元対象として対応済み。
