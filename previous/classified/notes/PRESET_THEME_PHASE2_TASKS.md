# Phase 2: ヘッダ/フッタ領域のON/OFF機能とHTML入力

## 概要

Phase 2では、カスタムスタイル設定のヘッダ/フッタ領域のON/OFF機能とHTML入力機能を実装します。

## 現状確認

### 実装済み
- ✅ 型定義: `CustomStyleConfig`に`headerEnabled`, `footerEnabled`, `headerHtml`, `footerHtml`が定義済み
- ✅ プリセットテーマ: 各テーマに`headerEnabled: true`, `footerEnabled: true`が設定済み
- ✅ バックエンド: `custom_style_config`の保存・取得機能は実装済み

### 実装済み（2026-01-23確認）
- ✅ フォーム編集画面: ヘッダ/フッタのON/OFFとHTML入力UI（FormEditIntegratedPage.tsxで実装済み）
- ✅ 公開フォーム画面: ヘッダ/フッタ領域の表示ロジック（PublicFormViewPage.tsxで実装済み）
- ✅ リアルタイムプレビュー: ヘッダ/フッタ領域の表示ロジック（FormRealtimePreview.tsxで実装済み）
- ✅ デフォルト表示: ヘッダ（ロゴ・タイトル）、フッタ（AppCopyrightコンポーネント）のデフォルト表示（実装済み）
- ✅ HTMLサニタイズ: ヘッダ/フッタHTMLのサニタイズ処理（sanitizeHtml関数を使用）

## 要件

### ヘッダ領域の仕様
- **デフォルト表示**: ロゴとフォーム名（現在の実装と同じ）
- **カスタマイズ時**: `headerHtml` にHTMLコードを設定すると、その内容を表示
- **タグ**: `<header>` タグで囲む
- **固定表示**: `position: sticky; top: 0;` でスクロール時にTOPに残る
- **スタイル**: `elements.header` でカスタマイズ可能
- **ON/OFF**: `headerEnabled` が `false` の場合は非表示

### フッタ領域の仕様
- **デフォルト表示**: `AppCopyright`コンポーネントを使用（サイドメニュー下部と同じ実装）
  - 環境変数`VITE_COPYRIGHT_OWNER`（デフォルト: "ReForma"）と`VITE_COPYRIGHT_SINCE`で設定可能
  - 例: "© 2024 ReForma" または "© 2020-2024 ReForma"
- **カスタマイズ時**: `footerHtml` にHTMLコードを設定すると、その内容を表示
- **タグ**: `<footer>` タグで囲む
- **スタイル**: `elements.footer` でカスタマイズ可能
- **ON/OFF**: `footerEnabled` が `false` の場合は非表示

## タスクリスト

### フロントエンド側

#### タスク1: HTMLサニタイズユーティリティの作成
- **ファイル**: `src/utils/htmlSanitizer.ts`（新規作成）
- **内容**: 
  - `sanitizeHtml`関数を実装
  - 危険なタグ（`<script>`, `<iframe>`, `<object>`等）を除去
  - 基本的なHTMLタグは許可（`<div>`, `<span>`, `<p>`, `<a>`, `<img>`, `<h1>`-`<h6>`, `<ul>`, `<ol>`, `<li>`等）
  - XSS対策を実装
- **注意**: 
  - DOMPurifyなどのライブラリを使用するか、簡易的な実装を検討
  - セキュリティを最優先に考慮

#### タスク2: FormEditIntegratedPage - ヘッダ/フッタ設定UIの追加
- **ファイル**: `src/pages/forms/FormEditIntegratedPage.tsx`
- **内容**: 
  - テーマ設定セクション内にヘッダ/フッタ設定を追加
  - ヘッダON/OFFトグルスイッチ
  - ヘッダHTML入力エリア（textarea、プレースホルダー付き）
  - フッタON/OFFトグルスイッチ
  - フッタHTML入力エリア（textarea、プレースホルダー付き）
  - プレビューリンク（リアルタイムプレビューで確認可能）
- **UI配置**: 
  - プリセットテーマ選択の下に配置
  - アコーディオン内のセクションとして追加

#### タスク3: FormEditIntegratedPage - ヘッダ/フッタ設定の保存・読み込み
- **ファイル**: `src/pages/forms/FormEditIntegratedPage.tsx`
- **内容**: 
  - `formCustomStyleConfig`の`headerEnabled`, `footerEnabled`, `headerHtml`, `footerHtml`を管理
  - フォーム取得時に設定を読み込み
  - フォーム保存時に設定を送信
  - HTML入力時にサニタイズ処理を実行（保存時または入力時）

#### タスク4: PublicFormViewPage - ヘッダ領域の表示ロジック実装
- **ファイル**: `src/pages/public/PublicFormViewPage.tsx`
- **内容**: 
  - `customStyleConfig.headerEnabled`をチェック
  - `headerEnabled === true`の場合のみヘッダを表示
  - `headerHtml`が設定されている場合はそのHTMLを表示（サニタイズ済み）
  - `headerHtml`が未設定の場合はデフォルト表示（ロゴ・タイトル）
  - `<header>`タグで囲み、`position: sticky; top: 0;`を適用
  - `elements.header`のスタイルを適用
  - `data-custom-style="header"`属性を追加

#### タスク5: PublicFormViewPage - フッタ領域の表示ロジック実装
- **ファイル**: `src/pages/public/PublicFormViewPage.tsx`
- **内容**: 
  - `customStyleConfig.footerEnabled`をチェック
  - `footerEnabled === true`の場合のみフッタを表示
  - `footerHtml`が設定されている場合はそのHTMLを表示（サニタイズ済み）
  - `footerHtml`が未設定の場合は`AppCopyright`コンポーネントを使用（デフォルト表示）
  - `<footer>`タグで囲む
  - `text-center`クラスを追加して中央揃えにする（ログイン画面と同じスタイル）
  - `elements.footer`のスタイルを適用
  - `data-custom-style="footer"`属性を追加
  - `AppCopyright`コンポーネントをインポートして使用

#### タスク6: PublicFormViewPage - コンテンツ領域のラッピング
- **ファイル**: `src/pages/public/PublicFormViewPage.tsx`
- **内容**: 
  - 既存のフォームコンテンツ（Card、フィールド等）を`<div data-custom-style="content">`で囲む
  - `elements.content`のスタイルを適用
  - ヘッダとフッタの間に配置

#### タスク7: FormRealtimePreview - ヘッダ領域の表示ロジック実装
- **ファイル**: `src/components/forms/FormRealtimePreview.tsx`
- **内容**: 
  - `customStyleConfig.headerEnabled`をチェック
  - `headerEnabled === true`の場合のみヘッダを表示
  - `headerHtml`が設定されている場合はそのHTMLを表示（サニタイズ済み）
  - `headerHtml`が未設定の場合はデフォルト表示（ロゴ・タイトル）
  - `<header>`タグで囲み、`position: sticky; top: 0;`を適用
  - `elements.header`のスタイルを適用
  - `data-custom-style="header"`属性を追加

#### タスク8: FormRealtimePreview - フッタ領域の表示ロジック実装
- **ファイル**: `src/components/forms/FormRealtimePreview.tsx`
- **内容**: 
  - `customStyleConfig.footerEnabled`をチェック
  - `footerEnabled === true`の場合のみフッタを表示
  - `footerHtml`が設定されている場合はそのHTMLを表示（サニタイズ済み）
  - `footerHtml`が未設定の場合は`AppCopyright`コンポーネントを使用（デフォルト表示）
  - `<footer>`タグで囲む
  - `text-center`クラスを追加して中央揃えにする（ログイン画面と同じスタイル）
  - `elements.footer`のスタイルを適用
  - `data-custom-style="footer"`属性を追加
  - `AppCopyright`コンポーネントをインポートして使用

#### タスク9: FormRealtimePreview - コンテンツ領域のラッピング
- **ファイル**: `src/components/forms/FormRealtimePreview.tsx`
- **内容**: 
  - 既存のフォームコンテンツ（Card、フィールド等）を`<div data-custom-style="content">`で囲む
  - `elements.content`のスタイルを適用
  - ヘッダとフッタの間に配置

#### タスク10: customStyle.ts - ヘッダ/フッタ/コンテンツ領域のスタイル適用
- **ファイル**: `src/utils/customStyle.ts`
- **内容**: 
  - `applyCustomStyleConfig`関数を拡張
  - `elements.header`, `elements.footer`, `elements.content`のスタイルを適用
  - `data-custom-style`属性を持つ要素を検索してスタイルを適用

## 実装順序の推奨

1. **基盤構築**（タスク1）
   - HTMLサニタイズユーティリティの作成

2. **フォーム編集画面の実装**（タスク2-3）
   - UI追加（タスク2）
   - 保存・読み込みロジック（タスク3）

3. **公開フォーム画面の実装**（タスク4-6）
   - ヘッダ領域（タスク4）
   - フッタ領域（タスク5）
   - コンテンツ領域のラッピング（タスク6）

4. **リアルタイムプレビューの実装**（タスク7-9）
   - ヘッダ領域（タスク7）
   - フッタ領域（タスク8）
   - コンテンツ領域のラッピング（タスク9）

5. **スタイル適用の拡張**（タスク10）
   - customStyle.tsの拡張

## 注意点

1. **セキュリティ**
   - HTML入力は必ずサニタイズ処理を実行
   - 危険なタグやスクリプトを除去
   - XSS対策を最優先に考慮

2. **デフォルト表示**
   - ヘッダ: ロゴとフォーム名（既存の実装を再利用）
   - フッタ: `AppCopyright`コンポーネントを使用（ログイン画面と同じ実装）
     - 環境変数で設定可能（`VITE_COPYRIGHT_OWNER`, `VITE_COPYRIGHT_SINCE`）
     - `text-center`クラスで中央揃えにする（ログイン画面と同じスタイル）
     - 既存のコンポーネントを再利用するため、追加実装不要
     - **注意**: `AppCopyright`コンポーネント自体は配置スタイルを持たず、親要素のクラスで制御
       - ログイン画面: `text-center`（中央揃え）
       - サイドメニュー: `text-center`なし（左揃え）
       - フッタ領域: `text-center`（中央揃え）で統一

3. **スタイル適用**
   - ヘッダは`position: sticky; top: 0;`で固定表示
   - フッタは通常のフローで表示
   - `data-custom-style`属性で要素を識別

4. **後方互換性**
   - `headerEnabled`が未設定の場合は`true`として扱う（デフォルト表示）
   - `footerEnabled`が未設定の場合は`true`として扱う（デフォルト表示）
   - `headerHtml`/`footerHtml`が未設定の場合はデフォルト表示

5. **プレビュー**
   - リアルタイムプレビューで即座に反映されるようにする
   - HTML入力の変更がリアルタイムで反映される

## デフォルト表示の実装例

### ヘッダ（デフォルト）
```tsx
<header data-custom-style="header" className="sticky top-0 z-50 ...">
  <div className="flex items-center gap-3">
    {logoPath && (
      <img src={logoPath} alt="Form Logo" className="w-[100px] h-[100px]" />
    )}
    <h1>{formTitle}</h1>
  </div>
</header>
```

### フッタ（デフォルト）
```tsx
import { AppCopyright } from "../../components/AppCopyright";

<footer data-custom-style="footer" className="text-center ...">
  <AppCopyright />
</footer>
```
- **注意**: `text-center`クラスを追加して中央揃えにする（ログイン画面と同じスタイル）
- `AppCopyright`コンポーネント自体は配置スタイルを持たず、親要素で制御

## テスト項目

1. **ヘッダON/OFF**
   - `headerEnabled: true`でヘッダが表示される
   - `headerEnabled: false`でヘッダが非表示になる

2. **フッタON/OFF**
   - `footerEnabled: true`でフッタが表示される
   - `footerEnabled: false`でフッタが非表示になる

3. **HTML入力**
   - `headerHtml`が設定されている場合、そのHTMLが表示される
   - `footerHtml`が設定されている場合、そのHTMLが表示される
   - 危険なタグがサニタイズされる

4. **デフォルト表示**
   - `headerHtml`が未設定の場合、デフォルトのロゴ・タイトルが表示される
   - `footerHtml`が未設定の場合、`AppCopyright`コンポーネントが表示される（サイドメニューと同じ）

5. **スタイル適用**
   - `elements.header`のスタイルが適用される
   - `elements.footer`のスタイルが適用される
   - `elements.content`のスタイルが適用される

6. **リアルタイムプレビュー**
   - 設定変更が即座にプレビューに反映される
