# タスク: UTF-8 ヒント配置・アーカイブ文言／スタイル・フォームエクスポート Toast

## 現状サマリ

### 1. テーマ一覧の UTF-8 ヒントの配置

| 項目 | 現状 |
|------|------|
| 配置 | ボタン行（新規作成・スペーサー・テーマインポート・テーマエクスポート）の**直下**に `HelpText` を `flex-col` の 2 行目として配置 |
| 左端 | HelpText は親の幅いっぱいに表示され、**テーマインポートの左端とは揃っていない**（テーマインポートは「新規作成 + gap + w-24 + gap」の右側から開始） |

- **揃えたい位置:** テーマインポートの左端 = 新規作成の幅 + `gap-3`(12px) + `w-24`(96px) + `gap-3`(12px) の右端。

---

### 2. フォーム一覧の UTF-8 ヒントの配置

| 項目 | 現状 |
|------|------|
| 配置 | ボタン行（新規作成・スペーサー・フォームインポート）の**直下**に `HelpText` を配置 |
| 左端 | 同様に、**フォームインポートの左端とは揃っていない** |

- **揃えたい位置:** フォームインポートの左端 = 新規作成の幅 + `gap-3` + `w-24` + `gap-3` の右端（テーマ一覧と同じ構造）。

---

### 3. フォームアーカイブ関連の form_list_column_form_name / form_list_column_response_count

| 項目 | 現状 |
|------|------|
| 使用箇所 | **FormListPage** の「フォームアーカイブ」確認ダイアログ（`form_archive_confirm_title` など）内。アーカイブ対象フォームの表示で使用 |
| コード | `t("form_list_column_form_name") \|\| "フォーム名"`、`t("form_list_column_response_count") \|\| "回答数"` |
| PreferencesContext | **form_list_column_form_name** と **form_list_column_response_count** は**未登録**。`form_list_column_code` は登録済み |
| 結果 | `t()` がキー文字列を返すか、フォールバックの日本語のみ表示され、**多言語で翻訳されていない** |

- **補足:** 「フォームアーカイブ**画面**」の文言は、FormArchiveListPage（F-05）ではなく、**FormListPage のアーカイブ確認ダイアログ**で使われている `form_list_column_*` を指していると解釈。

---

### 4. アーカイブボタンの警告風スタイル

| 項目 | 現状 |
|------|------|
| 対象 | **FormListPage** の一覧各行にあるアーカイブボタン（`t("archive")`） |
| スタイル | `border-orange-300 bg-white text-orange-700 hover:bg-orange-50`、`dark:border-orange-500/30 dark:bg-slate-900/40 dark:text-orange-400 dark:hover:bg-orange-950/20` |
| 解釈 | 背景は `bg-white`（ライト）／`dark:bg-slate-900/40`（ダーク）。オレンジの枠・文字はあるが、**背景が白のため、やや警告感が弱い** |

- **要望:** 「警告風」「一覧のオレンジ文字色とあう背景」→ オレンジ系の背景を足して、警告らしさを強める。
- **補足:** FormArchiveListPage（F-05）には「アーカイブ」ラベルのボタンはなく、「ダウンロード」「復元」「削除」のみ。ここでは **FormListPage のアーカイブボタン**を対象とする。

---

### 5. フォームエクスポート時の Toast 文言

| 項目 | 現状 |
|------|------|
| 使用箇所 | **FormListPage** の `handleExport` / `handleExportComplete` / `handleExportError` |
| 使用キー | `form_export_started`、`form_export_completed`、`form_export_failed`、`download_failed`（完了時のダウンロード失敗用） |
| PreferencesContext | **form_export_started / form_export_completed / form_export_failed / download_failed は未登録** |
| 結果 | フォールバックの日本語のみ表示され、**多言語で翻訳されていない** |

---

## タスク一覧

### タスク 1. テーマ一覧: UTF-8 ヒントの左端をテーマインポート左端に揃える

**ファイル:** `reforma-frontend-react/src/pages/system/ThemeListPage.tsx`

- **変更内容:** HelpText の 2 行目で、「テーマインポート」の左端と開始位置を揃える。
- **レイアウト案:**
  - 2 行目を `flex` にして、左に「見えぬスペーサー」を置き、その右に `HelpText` を配置。
  - スペーサー幅: テーマインポートの左端 = 新規作成ボタン幅 + `gap-3` + `w-24` + `gap-3`。  
    - 新規作成を約 `7rem`（112px）と仮定すると、`7rem + 0.75rem + 6rem + 0.75rem = 14.5rem`（約 232px）。  
  - 例: `<span className="w-[14.5rem] flex-shrink-0" aria-hidden="true" />` を HelpText の左に配置し、`flex` で横並びにする。
- **構造例:**
  ```tsx
  {canManageThemes && (
    <div className="flex gap-3 items-start">
      <span className="w-[14.5rem] flex-shrink-0" aria-hidden="true" />
      <HelpText>{t("csv_import_export_utf8_only") || "文字コードは UTF-8 のみに対応しています"}</HelpText>
    </div>
  )}
  ```

---

### タスク 2. フォーム一覧: UTF-8 ヒントの左端をフォームインポート左端に揃える

**ファイル:** `reforma-frontend-react/src/pages/forms/FormListPage.tsx`

- **変更内容:** テーマ一覧と同様に、HelpText の左端を「フォームインポート」の左端に揃える。
- **レイアウト:** タスク 1 と同一。ボタン構成は「新規作成 + スペーサー + フォームインポート」のため、同じ `w-[14.5rem]` のスペーサーで揃えられる。
- **構造例:** タスク 1 と同様の `flex` + スペーサー + `HelpText`。

---

### タスク 3. form_list_column_form_name / form_list_column_response_count の翻訳追加

**ファイル:**  
- `reforma-frontend-react/src/ui/PreferencesContext.tsx`  
- 利用箇所: `reforma-frontend-react/src/pages/forms/FormListPage.tsx`（アーカイブ確認ダイアログ）

**3a) PreferencesContext にキーを追加（ja / en）**

- `form_list_column_form_name`  
  - ja: `"フォーム名"`  
  - en: `"Form Name"`
- `form_list_column_response_count`  
  - ja: `"回答数"`  
  - en: `"Response Count"`

**3b) 追加位置**

- `form_list_column_code` の近く（Form List 関連）に追加。

**3c) FormListPage**

- 既に `t("form_list_column_form_name")` / `t("form_list_column_response_count")` を使用しているため、キー追加後にそのまま翻訳が適用される。フォールバック `|| "フォーム名"` / `|| "回答数"` は、キーがあれば不要になるが、残しても可。

---

### タスク 4. フォーム一覧のアーカイブボタンを警告風にする

**ファイル:** `reforma-frontend-react/src/pages/forms/FormListPage.tsx`

- **対象:** 一覧の「アーカイブ」ボタン（`onClick={() => handleArchiveClick(form)}`）。
- **現状:** `border-orange-300 bg-white text-orange-700 hover:bg-orange-50`、ダーク時は `dark:border-orange-500/30 dark:bg-slate-900/40 dark:text-orange-400 dark:hover:bg-orange-950/20`。
- **変更案:** オレンジ文字に合わせた「警告風」の背景とする。
  - ライト: `bg-white` → `bg-orange-50` など、薄いオレンジ背景。
  - ダーク: 現状の `dark:bg-slate-900/40` のまま、または `dark:bg-orange-950/20` などでオレンジ寄りにする（デザインに合わせて調整）。
- **例（ライトのみ変更）:**  
  `bg-orange-50`、`hover:bg-orange-100` など。`border` と `text-orange-700` は維持。

---

### タスク 5. フォームエクスポート時の Toast 文言を翻訳可能にする

**ファイル:**  
- `reforma-frontend-react/src/ui/PreferencesContext.tsx`  
- `reforma-frontend-react/src/pages/forms/FormListPage.tsx`

**5a) PreferencesContext にキーを追加（ja / en）**

- `form_export_started`  
  - ja: `"フォームエクスポートを開始しました"`  
  - en: `"Form export started"`
- `form_export_completed`  
  - ja: `"フォームエクスポートが完了しました"`  
  - en: `"Form export completed"`
- `form_export_failed`  
  - ja: `"フォームエクスポートに失敗しました"`  
  - en: `"Form export failed"`
- `download_failed`  
  - ja: `"ダウンロードに失敗しました"`  
  - en: `"Download failed"`  
  - （`handleExportComplete` 内の `showError(t("download_failed") \|\| "ダウンロードに失敗しました")` 用。他画面でも使う場合は共通化）

**5b) 追加位置**

- フォーム関連または既存の `form_import` などエクスポート／インポート周りの近く。

**5c) FormListPage**

- `form_export_started` / `form_export_completed` / `form_export_failed` / `download_failed` は既に `t()` 使用のため、キー追加後は翻訳が効く。フォールバックは任意。

---

## 変更ファイル一覧（予定）

| ファイル | タスク |
|----------|--------|
| `src/pages/system/ThemeListPage.tsx` | 1 |
| `src/pages/forms/FormListPage.tsx` | 2, 4 |
| `src/ui/PreferencesContext.tsx` | 3, 5 |

---

## 補足

- **UTF-8 ヒントのスペーサー幅:** `14.5rem` は目安。実機で「新規作成」の実際の幅を確認し、`14rem`〜`15rem` の範囲で微調整するとよい。
- **タスク 4 の対象:** FormArchiveListPage に「アーカイブ」ボタンはないため、**FormListPage のアーカイブボタン**を対象とした。FormArchiveListPage の「復元」を警告風にしたい場合は、別タスクとして扱う。
