# 添付設定フィールドのフロントエンドでの参照元

**作成日**: 2026-01-26  
**対象**: `attachment_enabled` / `attachment_type` / `pdf_template_path` / `attachment_files_json` がフロントのフォーム編集画面でどこから復元・表示されているかの整理。「テーブルにデータがみあたらないが画面では復元されている」事象の原因を明確にする。

---

## 1. どのテーブルにどのカラムがあるか（バックエンド）

| カラム | テーブル | 備考 |
|--------|----------|------|
| `attachment_enabled` | **forms** のみ | 添付の有効/無効 |
| `attachment_type` | **forms** と **form_translations** | 種別（`pdf_template` / `uploaded_files`） |
| `pdf_template_path` | **forms** のみ | PDFテンプレートのストレージパス |
| `attachment_files_json` | **forms** と **form_translations** | ファイルパス配列（forms は uploaded_files 用など） |

通知ジョブや PDF 生成は **forms** の `attachment_enabled` / `attachment_type` / `pdf_template_path` を参照する。  
フロントの「添付」UI は **form_translations** の `attachment_type` / `attachment_files_json` を主に使っている。

---

## 2. フロントでどこから読み出しているか

### 2.1 フォーム編集画面（FormEditIntegratedPage）

**初回ロード時（API 取得後）**

- 取得先: `GET /v1/forms/{id}` の `res.data.form` と `res.data.translations`
- 設定箇所:
  - **attachment_enabled**  
    → `res.data.form.attachment_enabled`  
    → `setFormAttachmentEnabled(formData.attachment_enabled)`  
    （2961–2990 行付近、2846 行）
  - **attachment_type / attachment_files_json**  
    → `res.data.translations[].attachment_type` / `res.data.translations[].attachment_files_json`  
    → `translationsMap` 経由で `setTranslations(translationsMap)`  
    （2961–2990 行、2974–2984 行）

**表示で参照している state**

- 添付の「有効にする」チェック: `formAttachmentEnabled`（form の `attachment_enabled` に対応）
- 添付タイプ（PDFテンプレート / アップロードファイル）:  
  `translations[activeAttachmentLanguageTab].attachment_type`
- アップロード済みファイル一覧:  
  `translations[activeAttachmentLanguageTab].attachment_files_json`

**結論**:  
フォーム編集の「添付」セクションで表示しているのは、

- **有効/無効** → **forms.attachment_enabled**（API の `form`）
- **タイプ・ファイル一覧** → **form_translations.attachment_type / attachment_files_json**（API の `translations`）

`form.attachment_type` や `form.pdf_template_path` は、この画面の添付セクション表示には使っていない。

### 2.2 フォーム一覧の詳細（FormListPage）

- `selectedForm.attachment_enabled`
- `selectedForm.attachment_type`
- `selectedForm.pdf_template_path` は型・表示用に参照あり（45–46 行付近）

一覧詳細は「フォーム」単位なので、API の `form`（forms テーブル由来）をそのまま表示している。

### 2.3 一時保存（ローカル）からの復元

- `saveTemporaryData` で `formAttachmentEnabled` を `formBasic.formAttachmentEnabled` として保存し、`translations` をそのまま保存（2495 行: `translations` に `attachment_type` / `attachment_files_json` を含む）。
- `applyTemporaryData` で
  - `formBasic.formAttachmentEnabled` → `setFormAttachmentEnabled`
  - `savedData.translations` → `setTranslations`（2390–2391 行）
- 復元は「フォーム詳細の再取得より先」に走る可能性があるが、その後の `fetchFormDetail` で API の `form` / `translations` で上書きする。  
  そのため、**最終的に画面上に出ている値は API レスポンスどおり**であり、
  - 添付タイプ・ファイル一覧が「復元されて見える」＝ **API の `translations`（＝ form_translations）に値が入っている**、
  - 有効/無効が「復元されて見える」＝ **API の `form.attachment_enabled`（＝ forms）に値が入っている**、
という対応になる。

---

## 3. 「テーブルにみあたらないが画面では復元されている」となりうる理由

- **forms だけを SQL で見ている場合**  
  - `attachment_type` / `pdf_template_path` / `attachment_files_json` が forms では null でも、  
    **form_translations** の同じ form_id の行に `attachment_type` や `attachment_files_json` が入っていれば、  
    フロントは `res.data.translations` からそれを読み、添付タイプ・ファイル一覧としては「復元されている」ように表示する。
- 逆に、**form_translations には入っているが forms には反映されていない**場合、
  - 一覧詳細や通知・PDF 生成は forms を見るため、そちらと「ずれ」が生じる。
  - バックエンド側のジョブで、`form.attachment_type` が空のときは `form_translations.attachment_type` をフォールバックする対応を既に入れている。

---

## 4. 保存時のフロント → バックエンド

保存時（1795–1856 行付近）:

- **form として送るもの**  
  - `attachment_enabled` のみ（1828 行: `formAttachmentEnabled`）
- **translations として送るもの**  
  - 各 locale の `attachment_type`（1811 行）  
  - 各 locale の `attachment_files_json`（1812 行）

`attachment_type` / `attachment_files_json` は **翻訳単位**で送っている。  
バックエンドの update では、受け取った `translations.*.attachment_type` / `attachment_files_json` を form_translations に保存し、**forms 側の `attachment_type` は** request に `attachment_type` が含まれる場合だけ更新している（FormsController 670–676 行など）。  
フロントの保存ペイロードには **トップレベルの `attachment_type` が含まれていない**ため、forms.attachment_type / forms.pdf_template_path は「フォーム更新 API の body では更新されず、PDF アップロード時にだけ更新される」形になっている。

---

## 5. 参照コード位置（フロント）

- **フォーム取得直後の state 設定**  
  - `FormEditIntegratedPage.tsx` 2835–2990 行（formData / res.data.translations → setForm* / setTranslations）
- **添付セクションの表示**  
  - 3184 行: `formAttachmentEnabled`（有効チェック）
  - 3215–3222 行: `translations[activeAttachmentLanguageTab].attachment_type`
  - 3297 / 3313–3314 / 3385 / 3389 行: `translations[activeAttachmentLanguageTab].attachment_files_json`
- **保存ペイロード**  
  - 1811–1812 行: translations の `attachment_type` / `attachment_files_json`
  - 1828 行: `attachment_enabled`
- **一時保存の保存・復元**  
  - 2465–2510 行: `saveTemporaryData`（formBasic.formAttachmentEnabled, translations）
  - 2359–2430 行: `applyTemporaryData`（formBasic, translations）

---

## 6. まとめ

- 画面上で「添付を有効」「PDFテンプレート」「ファイル一覧」が復元されて見えるとき、
  - **有効/無効** → **forms.attachment_enabled**（API の `form`）
  - **タイプ・ファイル一覧** → **form_translations.attachment_type / attachment_files_json**（API の `translations`）
  がそれぞれ参照元。
- 「テーブルにデータがみあたらない」が **forms だけを見ている**場合、form_translations を同じ form_id で確認すると、タイプ・ファイル一覧の出所が説明できる。
- 保存時、フロントは `attachment_type` / `attachment_files_json` を **translations だけ**で送っており、forms の `attachment_type` / `pdf_template_path` はフォーム更新 API のリクエストでは更新されない。  
  そのため、PDF テンプレート利用や通知時の添付判定では、バックエンド側で「form_translations の attachment_type をフォールバックする」などの対応が必要になる（既存対応ではジョブ内でフォールバックを実装済み）。
