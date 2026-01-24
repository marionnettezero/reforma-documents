# Phase 2: 修正タスク

## 概要

Phase 2実装後の修正タスクです。

## 修正点

### 修正1: ヘッダ領域 / コンテンツ領域 / フッタ領域 の親要素の padding 削除
- **目的**: フル領域を子要素に使わせる
- **対象**: `data-form-container`要素のpadding

### 修正2: custom_style_config がフォームにある場合は theme_tokens を適用しない
- **目的**: custom_style_config のスタイルを優先する
- **対象**: theme_tokens の適用ロジック

### 修正3: プリセットテーマの選択色の調整
- **目的**: 白背景で白文字が見えない問題を解決
- **対象**: プリセットテーマ選択UIのスタイル

### 修正4: プリセットテーマを 2 カラムから 3 カラムに変更
- **目的**: UIの改善
- **対象**: プリセットテーマ選択のグリッドレイアウト

## タスクリスト

### 修正1: padding削除

#### タスク1-1: PublicFormViewPage - data-form-containerのpadding削除
- **ファイル**: `src/pages/public/PublicFormViewPage.tsx`
- **内容**: 
  - `data-form-container`要素の`px-6 py-10`クラスを削除
  - ヘッダ領域、コンテンツ領域、フッタ領域がフル幅で表示されるようにする
- **注意**: 
  - ヘッダ内の`px-6 py-4`は子要素なので残す
  - フッタの`py-6 px-6`も子要素なので残す

#### タスク1-2: FormRealtimePreview - data-form-containerのpadding削除
- **ファイル**: `src/components/forms/FormRealtimePreview.tsx`
- **内容**: 
  - `data-form-container`要素の`px-6 py-10`クラスを削除
  - ヘッダ領域、コンテンツ領域、フッタ領域がフル幅で表示されるようにする
- **注意**: 
  - ヘッダ内の`px-6 py-4`は子要素なので残す
  - フッタの`py-6 px-6`も子要素なので残す

### 修正2: theme_tokens適用の条件分岐

#### タスク2-1: PublicFormViewPage - theme_tokens適用の条件分岐
- **ファイル**: `src/pages/public/PublicFormViewPage.tsx`
- **内容**: 
  - `customStyleConfig`が存在する場合は`theme_tokens`を適用しない
  - `useEffect`で`theme_tokens`を適用している箇所（784-809行目）を修正
  - 条件: `if (!form || !form.theme_tokens || customStyleConfig) return;`
- **対象箇所**:
  - `applyThemeTokensToElementWithInlineStyles`の呼び出し
  - `convertThemeTokensToCssVars`の呼び出し
  - `applyCssVarsToElement`の呼び出し

#### タスク2-2: PublicFormViewPage - インラインスタイルでのtheme_tokens使用を条件分岐
- **ファイル**: `src/pages/public/PublicFormViewPage.tsx`
- **内容**: 
  - インラインスタイルで`form?.theme_tokens`を使用している箇所を修正
  - `customStyleConfig`が存在する場合は`theme_tokens`を使用しない
  - 三項演算子を使用: `customStyleConfig ? undefined : form?.theme_tokens?.color_xxx`
- **対象箇所**（約84箇所）:
  - ヘッダーカードのstyle（1291-1293行目）
  - メインカードのstyle（1332-1334行目）
  - FieldComponent内のインラインスタイル（複数箇所）
  - その他のインラインスタイルで`theme_tokens`を使用している箇所
- **注意**: 
  - `customStyleConfig`が存在する場合は`undefined`を設定
  - `customStyleConfig`が存在しない場合のみ`theme_tokens`を使用
  - すべての箇所で一貫して条件分岐を適用

#### タスク2-3: FormRealtimePreview - theme_tokens適用の条件分岐
- **ファイル**: `src/components/forms/FormRealtimePreview.tsx`
- **内容**: 
  - `customStyleConfig`が存在する場合は`themeTokens`を適用しない
  - `useEffect`で`themeTokens`を適用している箇所（327-348行目）を修正
  - 条件: `if (!themeTokens || !containerRef.current || !formThemeRef.current || customStyleConfig) return;`
- **対象箇所**:
  - `applyThemeTokensToElementWithInlineStyles`の呼び出し
  - `convertThemeTokensToCssVars`の呼び出し
  - `applyCssVarsToElement`の呼び出し

#### タスク2-4: FormRealtimePreview - インラインスタイルでのthemeTokens使用を条件分岐
- **ファイル**: `src/components/forms/FormRealtimePreview.tsx`
- **内容**: 
  - インラインスタイルで`themeTokens`を使用している箇所を修正
  - `customStyleConfig`が存在する場合は`themeTokens`を使用しない
  - 三項演算子を使用: `customStyleConfig ? undefined : themeTokens?.color_xxx`
- **対象箇所**（約49箇所）:
  - ヘッダーカードのstyle（523-525行目）
  - メインカードのstyle
  - PreviewFieldComponent内のインラインスタイル（複数箇所）
  - その他のインラインスタイルで`themeTokens`を使用している箇所
- **注意**: 
  - `customStyleConfig`が存在する場合は`undefined`を設定
  - `customStyleConfig`が存在しない場合のみ`themeTokens`を使用
  - すべての箇所で一貫して条件分岐を適用

### 修正3: プリセットテーマ選択色の調整

#### タスク3-1: FormEditIntegratedPage - プリセットテーマ選択色の調整
- **ファイル**: `src/pages/forms/FormEditIntegratedPage.tsx`
- **内容**: 
  - 選択時のスタイルを調整
  - 現在: `border-blue-500 bg-blue-50`（白背景で白文字が見えない問題）
  - 修正案1: `border-blue-600 bg-blue-100 text-blue-900`（より濃い背景色と文字色）
  - 修正案2: `border-blue-500 bg-blue-50 text-blue-900`（文字色を明示的に指定）
  - グローバルテーマが白文字の場合でも見えるようにする
- **対象箇所**:
  - プリセットテーマ選択のラベル（2736-2740行目、2763-2767行目、3769-3773行目、3796-3800行目）
  - 4箇所のプリセットテーマ選択UI（2箇所の通常表示 + 2箇所の条件付き表示）
- **注意**: 
  - 選択時の文字色を明示的に指定する（`text-blue-900`など）
  - 未選択時も視認性を確保

### 修正4: プリセットテーマを3カラムに変更

#### タスク4-1: FormEditIntegratedPage - プリセットテーマを3カラムに変更
- **ファイル**: `src/pages/forms/FormEditIntegratedPage.tsx`
- **内容**: 
  - `grid-cols-2`を`grid-cols-3`に変更
  - 2箇所のプリセットテーマ選択UIを修正
- **対象箇所**:
  - 2984行目: `grid grid-cols-3 gap-3` ✅ 完了
  - 4012行目: `grid grid-cols-3 gap-3` ✅ 完了
- **実装状況**（2026-01-23確認）:
  - ✅ 2箇所完了（2984行目、4012行目）

## 実装順序の推奨

1. **修正1: padding削除**（タスク1-1, 1-2）
   - ヘッダ/コンテンツ/フッタ領域の親要素のpaddingを削除

2. **修正2: theme_tokens適用の条件分岐**（タスク2-1〜2-4）
   - custom_style_configがある場合はtheme_tokensを適用しない

3. **修正3: プリセットテーマ選択色の調整**（タスク3-1）
   - 選択時の色を調整

4. **修正4: プリセットテーマを3カラムに変更**（タスク4-1）
   - グリッドレイアウトを3カラムに変更

## 注意点

1. **padding削除**
   - 親要素（`data-form-container`）のpaddingのみ削除
   - 子要素（ヘッダ内、フッタ内）のpaddingは維持

2. **theme_tokens適用の条件分岐**
   - `customStyleConfig`が存在する場合（nullでない場合）は`theme_tokens`を適用しない
   - `customStyleConfig`がnullまたはundefinedの場合のみ`theme_tokens`を適用
   - インラインスタイルでも同様の条件分岐が必要

3. **プリセットテーマ選択色**
   - グローバルテーマが白文字の場合でも見えるようにする
   - 選択時の背景色と文字色のコントラストを確保

4. **3カラムレイアウト**
   - プリセットテーマが4つ（dark, light, reforma, classic）+ カスタム = 5つ
   - 3カラムにすると、2行目に2つ表示される

## 進捗状況

- **全体進捗**: 4/4 修正タスク完了（100%）
- **最終更新**: 2026-01-23
- **完了タスク**: 
  - ✅ 修正1: padding削除（タスク1-1, 1-2）
  - ✅ 修正2: theme_tokens適用の条件分岐（タスク2-1〜2-4）
  - ✅ 修正3: プリセットテーマ選択色の調整（タスク3-1）
  - ✅ 修正4: プリセットテーマを3カラムに変更（タスク4-1）
- **進行中タスク**: なし
- **未着手タスク**: なし

## 実装完了内容（2026-01-23）

### ✅ 修正4: プリセットテーマを3カラムに変更
- 4012行目の`grid-cols-2`を`grid-cols-3`に変更完了
- 2箇所すべてのプリセットテーマ選択UIが3カラムレイアウトに統一
