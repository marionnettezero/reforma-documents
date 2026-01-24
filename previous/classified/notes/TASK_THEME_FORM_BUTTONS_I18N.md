# タスク: テーマ一覧・フォーム一覧のボタン文言・ヒント・レイアウト

## 現状サマリ

### テーマ一覧（ThemeListPage.tsx）

| 項目 | 現状 |
|------|------|
| Import ボタン | `t("import")` → 「インポート」/ "Import"（汎用キー） |
| Export ボタン | `t("export")` → 「エクスポート」/ "Export"（汎用キー） |
| UTF-8 ヒント | **なし**（HelpText 未設置） |
| ボタン配置 | 新規作成 → スペーサー `w-24` → Import → Export（既に 1 ボタン幅の間隔あり） |
| HelpText コンポーネント | **import 済み** |

- 翻訳: `theme_import` / `theme_export` は PreferencesContext に**既存**（ja/en 両方）。

### フォーム一覧（FormListPage.tsx）

| 項目 | 現状 |
|------|------|
| Import ボタン | `t("form_import") \|\| "インポート"` → キー未登録のためフォールバック「インポート」 |
| UTF-8 ヒント | **なし**（HelpText 未設置・import もなし） |
| 新規作成〜Import の間隔 | **なし**（`gap-3` のみ、1 ボタン幅のスペーサーなし） |
| Archive ボタン | `t("archive") \|\| "アーカイブ"` → キー `archive` は**未登録**、フォールバック「アーカイブ」 |
| Archive ダイアログ | 下記の翻訳キーで t() 使用、PreferencesContext には**未登録**（すべてフォールバック依存） |

- Import モーダル: `form_import` をタイトルに使用（キー未登録）。`form_import_description` 等も未登録。

### 共通・項目詳細（参考）

| 項目 | 現状 |
|------|------|
| UTF-8 ヒント文言 | `csv_import_export_utf8_only`: 「文字コードは UTF-8 のみに対応しています」/ "Only UTF-8 character encoding is supported"（**PreferencesContext に既存**） |
| 表示方法 | `HelpText` 内で `t("csv_import_export_utf8_only")`（FieldDetailPanel.tsx で使用） |

---

## タスク一覧

### 1. テーマ一覧: Import / Export ボタン文言の変更（多言語対応）

**ファイル:** `reforma-frontend-react/src/pages/system/ThemeListPage.tsx`

| 箇所 | 現状 | 変更後 |
|------|------|--------|
| Import ボタン（L725） | `{t("import")}` | `{t("theme_import")}` |
| Export ボタン（L733） | `{t("export")}` | `{t("theme_export")}` |

- `theme_import` / `theme_export` は既に PreferencesContext に定義済み（「テーマインポート」「テーマエクスポート」/ "Theme Import", "Theme Export"）。他言語は必要に応じてキー追加。

---

### 2. テーマ一覧: Import / Export ボタン下部に UTF-8 ヒント（共通・項目詳細と同様）

**ファイル:** `reforma-frontend-react/src/pages/system/ThemeListPage.tsx`

- **文言:** `t("csv_import_export_utf8_only")`（項目詳細と同一。既存キー）
- **コンポーネント:** 共通の `HelpText`（既に import 済み）
- **配置:** Import / Export ボタンを含む左側ブロックの**直下**
- **レイアウト案:**
  - 左ブロックを `flex-col` でラップ
  - 1 行目: 既存の `create_new` → スペーサー → Import → Export
  - 2 行目: `<HelpText>{t("csv_import_export_utf8_only") || "文字コードは UTF-8 のみに対応しています"}</HelpText>`

※ `justify-between` の「左ブロック」を、`[ボタン行, HelpText]` の `flex-col` にして、その親を従来の「左」として使う。

---

### 3. フォーム一覧: Import ボタン文言を「フォームインポート」に（多言語対応）

**ファイル:**  
- `reforma-frontend-react/src/pages/forms/FormListPage.tsx`  
- `reforma-frontend-react/src/ui/PreferencesContext.tsx`

**3a) PreferencesContext に `form_import` を追加**

- `form_import`:  
  - ja: `"フォームインポート"`  
  - en: `"Form Import"`  
- フォーム Import モーダルの `title` でも `t("form_import")` を使用しているため、モーダルもこのキーで統一可能。

**3b) FormListPage の Import ボタン**

| 箇所 | 現状 | 変更後 |
|------|------|--------|
| Import ボタン（L547） | `{t("form_import") \|\| "インポート"}` | `{t("form_import")}`（フォールバックは `"フォームインポート"` を Preferences 側に持たせるか、`\|\| "フォームインポート"` のどちらか。キー登録後は `t("form_import")` のみで可） |

- モーダル `title`（L1009）は現状 `t("form_import") || "フォームインポート"` → キー追加後に `t("form_import")` で統一。

---

### 4. フォーム一覧: Import ボタン下部に UTF-8 ヒント（共通・項目詳細と同様）

**ファイル:** `reforma-frontend-react/src/pages/forms/FormListPage.tsx`

- **文言:** `t("csv_import_export_utf8_only")`（項目詳細・テーマ一覧と同一）
- **コンポーネント:** `HelpText` を **import 追加**
- **配置:** 新規作成・Import ボタン行の**直下**（Import ボタン下部として解釈）
- **レイアウト案:**
  - 左ブロックを `flex-col` でラップ
  - 1 行目: 新規作成 → （後述のスペーサー）→ Import
  - 2 行目: `<HelpText>{t("csv_import_export_utf8_only") || "文字コードは UTF-8 のみに対応しています"}</HelpText>`

---

### 5. フォーム一覧: Import ボタンの位置（新規作成から 1 ボタン幅の間隔）

**ファイル:** `reforma-frontend-react/src/pages/forms/FormListPage.tsx`

- **現状:** `Link(create_new)` の直後に `button(Import)`。`gap-3` のみで、テーマ一覧のような「1 ボタン幅」のスペースはなし。
- **変更:** 新規作成と Import の間に、テーマ一覧と同様のスペーサーを挿入  
  - `<span className="w-24 flex-shrink-0" aria-hidden="true" />`
- **位置:** `Link(create_new)` の直後、`button(Import)` の直前。

---

### 6. フォーム一覧: Archive ボタン文言を「アーカイブ」に（多言語対応）

**ファイル:**  
- `reforma-frontend-react/src/pages/forms/FormListPage.tsx`  
- `reforma-frontend-react/src/ui/PreferencesContext.tsx`

**6a) PreferencesContext に `archive` を追加**

- `archive`:  
  - ja: `"アーカイブ"`  
  - en: `"Archive"`
- 汎用の `import` / `export` の近く（Common UI あたり）に置く想定。

**6b) FormListPage の Archive ボタン**

| 箇所 | 現状 | 変更後 |
|------|------|--------|
| 一覧の Archive ボタン（L742） | `{t("archive") \|\| "アーカイブ"}` | `{t("archive")}`（キー追加後） |
| アーカイブ確認ダイアログの実行ボタン（L1109） | `{t("archive") \|\| "アーカイブ"}` | `{t("archive")}` |

- 文言自体は「アーカイブ」のまま。キーを登録して多言語化するのが目的。

---

### 7. フォーム一覧: Archive ダイアログの翻訳キー確認

**ファイル:** `reforma-frontend-react/src/pages/forms/FormListPage.tsx`（L1069–1112 付近）

| 用途 | 翻訳キー | 日本語フォールバック | PreferencesContext 登録 |
|------|----------|----------------------|---------------------------|
| ダイアログタイトル | `form_archive_confirm_title` | フォームアーカイブ | **未登録** |
| 説明文 | `form_archive_confirm_description` | フォームと回答データをアーカイブします。アーカイブされたデータは物理削除されます。この操作は取り消せません。 | **未登録** |
| 対象フォーム見出し | `form_archive_confirm_form_info` | アーカイブ対象のフォーム | **未登録** |
| 実行ボタン | `archive` | アーカイブ | **未登録**（タスク 6 で追加） |

**推奨:**

- 上記 4 つを **PreferencesContext に追加** する。
- 既存の `archive_download_completed` の近く、もしくは「Form 関連」のブロックに、  
  `form_archive_confirm_title`, `form_archive_confirm_description`, `form_archive_confirm_form_info` を ja/en で定義。
- 実行ボタンはタスク 6 の `archive` をそのまま利用。

**英語例（参考）:**

- `form_archive_confirm_title`: "Form Archive"
- `form_archive_confirm_description`: "The form and response data will be archived. Archived data will be permanently deleted. This action cannot be undone."
- `form_archive_confirm_form_info`: "Form to be archived"

---

## 実装時の依存関係

1. **PreferencesContext のキー追加**（3, 6, 7）  
   → FormListPage / ThemeListPage の `t(...)` の前提になる。

2. **ThemeListPage**  
   - タスク 1: ボタン文言（既存キー利用）  
   - タスク 2: HelpText と `csv_import_export_utf8_only`（既存キー・既存 import 利用）

3. **FormListPage**  
   - タスク 3: `form_import` キー追加 + ボタン・モーダルで使用  
   - タスク 4: HelpText の import 追加 + `csv_import_export_utf8_only`  
   - タスク 5: スペーサー `w-24` 追加  
   - タスク 6: `archive` キー追加 + 一覧・ダイアログの実行ボタン  
   - タスク 7: `form_archive_confirm_*` のキー追加 + ダイアログで使用

---

## 変更ファイル一覧（予定）

| ファイル | タスク |
|----------|--------|
| `src/ui/PreferencesContext.tsx` | 3, 6, 7（`form_import`, `archive`, `form_archive_confirm_title`, `form_archive_confirm_description`, `form_archive_confirm_form_info`） |
| `src/pages/system/ThemeListPage.tsx` | 1, 2 |
| `src/pages/forms/FormListPage.tsx` | 3, 4, 5, 6, 7（Import/Archive 文言、HelpText、スペーサー、ダイアログ文言） |

---

## 補足

- **csv_import_export_utf8_only**  
  - 項目詳細・テーマ一覧・フォーム一覧で共通利用。  
  - 文言を変える場合は PreferencesContext の当該キーのみ変更。
- **HelpText**  
  - 項目詳細（FieldDetailPanel）と同様のスタイルで、UTF-8 ヒントを表示する。
- **テーマ一覧の「1 ボタン幅」**  
  - 既に `w-24` のスペーサーがあるため、テーマ一覧側の追加対応は不要。
