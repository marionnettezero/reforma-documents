# テーマ・カスタムスタイルとグローバルCSS

フォーム設定のテーマで「カスタム」を選んだときに利用できる、**要素ごとのスタイル指定**と**グローバルCSS**の仕様・記述方法をまとめる。

---

## 1. フォーム設定で指定できる要素

フォーム編集画面の **フォーム設定 > テーマ設定 > カスタム** の **詳細カスタマイズ** で、次の要素にクラス名・インラインスタイルを指定できる。

| 画面表示名     | 要素キー（内部） | 対象・補足 |
|----------------|------------------|------------|
| ルート要素     | `root`           | アプリ全体のルート `<div id="root">`。背景などに使用。 |
| コンテナ       | `container`      | フォーム全体のラッパー（`data-form-container` が付いた要素）。 |
| コンテンツ領域 | `content`        | フィールド表示エリア（`data-custom-style="content"`）。 |
| ヘッダ領域     | `header`         | 上部のヘッダ（`data-custom-style="header"`）。 |
| フッタ領域     | `footer`         | 下部のフッタ（`data-custom-style="footer"`）。 |
| カード         | `card`           | フォームの各カード（`data-custom-style="card"`）。 |
| プライマリボタン | `buttonPrimary`  | 送信・「次へ」等（`data-custom-style="buttonPrimary"`）。 |
| セカンダリボタン | `buttonSecondary`| 「戻る」等（`data-custom-style="buttonSecondary"`）。 |
| 入力フィールド | `input`          | テキスト・テキストエリア・セレクト等。 |
| タイトル       | `title`          | フォームタイトル（h1）。 |
| 説明文         | `description`    | フォーム説明（p）。 |
| フィールドラベル | `fieldLabel`     | 各項目のラベル。 |

各要素には次の形式でスタイルを指定する。

- **クラス名**: スペース区切りで複数指定可能。
- **インラインスタイル**: `property: value;` を1行1つで記述（例: `background-color: #ffffff;`）。
- **条件付きスタイル**（該当する要素のみ）: hover / focus / disabled / error ごとに上記を別途指定可能。

これらは「要素スタイル」としてテーマに保存され、プレビュー・公開フォームで適用される。  
一方、**グローバルCSS** は別枠で、自由なCSSを追加するために使う。

---

## 2. グローバルCSSの記述の仕方

テーマ設定の **グローバルCSS** 欄には、**任意のCSS** をそのまま書ける。

- プレビュー・リアルタイムプレビュー・公開フォームの `data-form-container` 内に、`<style id="custom-style-global">` として挿入され、その内容がそのまま解釈される。
- コメント、セレクタ、@ルール（`@media` 等）も利用可能。制限はとくにない。

### 2.1 セレクタの例（要素・ID・クラス・属性）

装飾したい対象に応じて、次のようなセレクタが使える。

| 目的                 | セレクタ例 |
|----------------------|------------|
| ルート要素           | `#root` |
| フォームコンテナ     | `[data-form-container]` |
| ヘッダ               | `[data-custom-style="header"]` |
| コンテンツ領域       | `[data-custom-style="content"]` |
| フッタ               | `[data-custom-style="footer"]` |
| カード               | `[data-custom-style="card"]` |
| プライマリボタン     | `[data-custom-style="buttonPrimary"]` |
| セカンダリボタン     | `[data-custom-style="buttonSecondary"]` |
| 特定フィールド（ID） | `#フィールドキー`（例: `#email`） |
| 特定フィールド（クラス） | `.form-field-フィールドキー`（例: `.form-field-email`） |
| 特定フィールド（属性） | `[data-field-key="フィールドキー"]`（例: `[data-field-key="email"]`） |
| 全フィールドのラッパー | `.form-field` |

「フィールドキー」は項目詳細で設定する英数字・アンダースコアのみのキー（例: `email`, `name_1`）。  
各フィールドのラッパーには次の属性・クラスが付与されている。

- `id` = フィールドキー（空でないときのみ）
- `class` = `space-y-1 form-field form-field-{フィールドキー}`
- `data-field-key` = フィールドキー（空でないときのみ）

---

## 3. グローバルCSSの記述例

```css
/* ルートの背景 */
#root {
  background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
}

/* ヘッダだけ下線を太く */
[data-custom-style="header"] {
  border-bottom-width: 2px;
}

/* メール欄のラッパーを目立たせる */
.form-field-email {
  background: #f0f9ff;
  padding: 0.5rem;
  border-radius: 0.5rem;
}

/* 同じことを id で指定する例（フォーム内で一意なとき） */
#email {
  max-width: 24rem;
}

/* 属性セレクタでフォントサイズ */
[data-field-key="tel"] {
  font-size: 1.125rem;
}

/* 全フィールドに共通の余白 */
.form-field {
  margin-bottom: 1rem;
}
```

---

## 4. 適用範囲の整理

- **要素スタイル（詳細カスタマイズ）**: フォーム設定の「詳細カスタマイズ」で要素キーごとに指定したクラス・インラインスタイル。対象は上記「指定できる要素」のとおり。
- **グローバルCSS**: 同じテーマ設定内の「グローバルCSS」に書いたCSSがそのまま実行される。上記のセレクタや例のように、`#root`・`[data-form-container]`・`[data-custom-style="…"]`・`.form-field` / `.form-field-{キー}` / `#フィールドキー` / `[data-field-key="…"]` を組み合わせて、レイアウト・装飾を拡張できる。

両方とも、**プレビュー・リアルタイムプレビュー・公開フォーム** に共通で効く。

---

## 5. 参照している実装

- カスタムスタイル型: `reforma-frontend-react/src/types/customStyle.ts`（`CustomStyleConfig`, `ElementStyleConfig`）
- 適用ロジック: `reforma-frontend-react/src/utils/customStyle.ts`（`applyGlobalCss`, `applyCustomStyleConfig`）
- フィールドラッパーの id / class / data-field-key: `reforma-frontend-react/src/components/forms/PublicFormField.tsx` のルート要素
- `data-custom-style` の付与: `PublicFormViewPage`, `FormRealtimePreview`, `FormPreviewPage`, `Card` など

---

## 6. ヘッダ・フッタのHTML（カスタムスタイル）のバリデーション

カスタムスタイル設定では、**ヘッダ**・**フッタ**に **HTML をそのまま記述**できる（`headerHtml` / `footerHtml`）。タグを使ってレイアウトやリンクを入れられるが、**XSS 対策のためフロントでサニタイズ**がかかる。

### 6.1 フロントエンドでのサニタイズ（あり）

- **実装**: `reforma-frontend-react/src/utils/htmlSanitizer.ts` の `sanitizeHtml()`
- **利用箇所**:
  - **表示時**: プレビュー・公開フォームで `dangerouslySetInnerHTML` に渡す直前に `sanitizeHtml(...)` を実行
  - **保存時**: フォーム保存時に `headerHtml` / `footerHtml` をサニタイズしてから API に送信

**許可されるタグ**（ホワイトリスト）:  
`div`, `span`, `p`, `a`, `img`, `h1`～`h6`, `ul`, `ol`, `li`, `strong`, `em`, `b`, `i`, `u`, `br`, `hr`, `table` 系, `blockquote`, `pre`, `code`

**禁止タグ**:  
`script`, `iframe`, `object`, `embed`, `form`, `input`, `button`（`FORBID_TAGS` で明示的に除去）

**禁止属性**:  
`onerror`, `onload`, `onclick`, `onmouseover`, `onfocus`, `onblur` など（`FORBID_ATTR`）

**許可属性**:  
`href`, `src`, `alt`, `title`, `class`, `id`, `style`, `width`, `height`, `target`, `rel`

そのため、**`<script>` タグは保存前・表示前の両方で除去され、実行されない**。通常の編集経路（管理画面でヘッダ／フッタを編集して保存し、プレビュー・公開で表示）では、スクリプトによる XSS は抑止される。

### 6.2 バックエンドでのバリデーション（なし）

- **FormsController** / **ThemesController** では、`custom_style_config` に `'custom_style_config' => ['nullable', 'array']` のルールのみ。
- **`headerHtml` / `footerHtml` の文字列内容**（タグの禁止・許可など）を検証する処理は**ない**。

API を直接叩いて未サニタイズの HTML（`<script>` 含む）を渡した場合は、そのまま DB に保存される可能性がある。一方、**表示時は常にフロントで `sanitizeHtml()` を通す**ため、プレビュー・公開フォームでの表示時点での XSS は防がれている。厳密にする場合は、バックエンドでも受信時に HTML サニタイズ（または許可タグの検証）を入れる拡張が考えられる。
