# テーマトークン適用改善仕様書

## 概要

フォーム設定で指定したテーマトークンが公開フォーム画面とプレビュー画面で正しく適用されない問題を解決する。

## 問題の現状

### 現在の実装
- テーマトークンはCSS変数（`--color-bg`, `--color-text`など）として`data-form-theme`属性を持つ要素に設定されている
- しかし、実際のスタイルはTailwindクラス（`bg-white`, `text-slate-900`など）で指定されている
- TailwindクラスはCSS変数を使用していないため、CSS変数を設定しても反映されない

### 問題の原因
1. `<html class="group">`でTailwindの`group-data-[theme=reforma]:`が適用されている
2. `Card`コンポーネントは`uiTokens.card`を使用（Tailwindクラス: `bg-white`, `text-slate-900`など）
3. フォーム表示部分の要素（`Card`, `input`, `button`など）はすべてTailwindクラスでスタイリングされている
4. TailwindクラスはCSS変数を使用していないため、CSS変数を設定しても反映されない

### 現在のコード例
```tsx
// PublicFormViewPage.tsx
<div className="min-h-screen px-6 py-10">
  <div className="mx-auto max-w-3xl space-y-4" data-form-theme>
    <Card>  {/* uiTokens.card = "bg-white text-slate-900 ..." */}
      ...
    </Card>
  </div>
</div>
```

```tsx
// themeTokens.ts
// CSS変数を設定しているが、Tailwindクラスが優先される
cssVars["--color-bg"] = tokens.color_bg;  // 使用されない
cssVars["--color-text"] = tokens.color_text;  // 使用されない
```

## 解決策

### 方法: インラインスタイルで直接適用

Tailwindクラスと競合しないように、インラインスタイル（`style`属性）で直接背景色・文字色を適用する。

### 実装方針

1. **上位div（`min-h-screen`）への背景色・文字色の適用**
   - テーマトークンの`color_bg`と`color_text`をインラインスタイルで直接適用
   - これにより、フォーム全体の背景色と文字色が変更される

2. **フォーム表示部分の要素への適用**
   - `Card`コンポーネント: 背景色と文字色をインラインスタイルで適用
   - `input`要素: 背景色、文字色、ボーダー色をインラインスタイルで適用
   - `button`要素: 背景色、文字色をインラインスタイルで適用
   - その他の要素: 必要に応じてインラインスタイルを適用

3. **CSS変数との併用**
   - 角丸、スペーシング、フォントファミリーなどはCSS変数として保持
   - カラー系のみインラインスタイルで直接適用

## 詳細仕様

### 1. themeTokens.ts の拡張

#### 1.1 背景色・文字色をインラインスタイルで適用する関数を追加

```typescript
/**
 * テーマトークンの背景色と文字色を要素に直接適用（インラインスタイル）
 * 
 * @param element 適用先のHTMLElement
 * @param tokens テーマトークンオブジェクト
 * @returns 適用したスタイルのRecord（クリーンアップ用）
 */
export function applyThemeColorsToElement(
  element: HTMLElement,
  tokens: ThemeTokens
): Record<string, string> {
  const appliedStyles: Record<string, string> = {};
  
  // 背景色
  if (tokens.color_bg) {
    element.style.backgroundColor = tokens.color_bg;
    appliedStyles.backgroundColor = tokens.color_bg;
  }
  
  // 文字色
  if (tokens.color_text) {
    element.style.color = tokens.color_text;
    appliedStyles.color = tokens.color_text;
  }
  
  return appliedStyles;
}

/**
 * 要素から適用したスタイルを削除
 * 
 * @param element 対象のHTMLElement
 * @param styles 削除するスタイルのRecord
 */
export function removeThemeColorsFromElement(
  element: HTMLElement,
  styles: Record<string, string>
): void {
  Object.keys(styles).forEach((key) => {
    element.style.removeProperty(key);
  });
}

/**
 * テーマトークンを要素に適用（背景色・文字色をインラインスタイル、その他をCSS変数）
 * 
 * @param element 適用先のHTMLElement
 * @param tokens テーマトークンオブジェクト
 * @returns クリーンアップ関数
 */
export function applyThemeTokensToElementWithInlineStyles(
  element: HTMLElement,
  tokens: ThemeTokens
): () => void {
  // 背景色・文字色をインラインスタイルで適用
  const appliedColors = applyThemeColorsToElement(element, tokens);
  
  // その他のトークンをCSS変数として適用
  const cssVars = convertThemeTokensToCssVars(tokens);
  // カラー系は除外（インラインスタイルで適用済み）
  delete cssVars["--color-bg"];
  delete cssVars["--color-text"];
  applyCssVarsToElement(element, cssVars);
  
  // クリーンアップ関数を返す
  return () => {
    removeThemeColorsFromElement(element, appliedColors);
    removeCssVarsFromElement(element, cssVars);
  };
}
```

#### 1.2 フォーム要素用のスタイル適用関数を追加

```typescript
/**
 * フォーム要素（Card, input, button等）にテーマトークンを適用
 * 
 * @param element 適用先のHTMLElement
 * @param tokens テーマトークンオブジェクト
 * @param elementType 要素タイプ（'card' | 'input' | 'button' | 'text'）
 * @returns 適用したスタイルのRecord（クリーンアップ用）
 */
export function applyThemeToFormElement(
  element: HTMLElement,
  tokens: ThemeTokens,
  elementType: 'card' | 'input' | 'button' | 'text'
): Record<string, string> {
  const appliedStyles: Record<string, string> = {};
  
  switch (elementType) {
    case 'card':
      // Card要素: 背景色、文字色、ボーダー色
      if (tokens.color_bg) {
        element.style.backgroundColor = tokens.color_bg;
        appliedStyles.backgroundColor = tokens.color_bg;
      }
      if (tokens.color_text) {
        element.style.color = tokens.color_text;
        appliedStyles.color = tokens.color_text;
      }
      if (tokens.color_primary) {
        element.style.borderColor = tokens.color_primary;
        appliedStyles.borderColor = tokens.color_primary;
      }
      break;
      
    case 'input':
      // Input要素: 背景色、文字色、ボーダー色、フォーカス時の色
      if (tokens.color_bg) {
        element.style.backgroundColor = tokens.color_bg;
        appliedStyles.backgroundColor = tokens.color_bg;
      }
      if (tokens.color_text) {
        element.style.color = tokens.color_text;
        appliedStyles.color = tokens.color_text;
      }
      if (tokens.color_primary) {
        element.style.borderColor = tokens.color_primary;
        appliedStyles.borderColor = tokens.color_primary;
      }
      break;
      
    case 'button':
      // Button要素: 背景色、文字色
      if (tokens.color_primary) {
        element.style.backgroundColor = tokens.color_primary;
        appliedStyles.backgroundColor = tokens.color_primary;
      }
      if (tokens.color_text) {
        element.style.color = tokens.color_text;
        appliedStyles.color = tokens.color_text;
      }
      break;
      
    case 'text':
      // テキスト要素: 文字色のみ
      if (tokens.color_text) {
        element.style.color = tokens.color_text;
        appliedStyles.color = tokens.color_text;
      }
      break;
  }
  
  // 角丸
  if (tokens.radius !== undefined) {
    element.style.borderRadius = `${tokens.radius}px`;
    appliedStyles.borderRadius = `${tokens.radius}px`;
  }
  
  return appliedStyles;
}
```

### 2. PublicFormViewPage の変更

#### 2.1 上位divへの背景色・文字色の適用

```tsx
// useEffectでテーマトークンを適用
useEffect(() => {
  if (!form || !form.theme_tokens) return;
  
  // 上位div（min-h-screen）に背景色・文字色を適用
  const container = document.querySelector(`[data-form-container]`) as HTMLElement;
  if (container) {
    const cleanup = applyThemeTokensToElementWithInlineStyles(container, form.theme_tokens);
    return cleanup;
  }
}, [form]);

// JSX
return (
  <div 
    className="min-h-screen px-6 py-10"
    data-form-container
  >
    <div className="mx-auto max-w-3xl space-y-4" data-form-theme>
      ...
    </div>
  </div>
);
```

#### 2.2 Cardコンポーネントへの適用

```tsx
// Cardコンポーネントをラップしてテーマトークンを適用
<Card
  style={{
    backgroundColor: form?.theme_tokens?.color_bg || undefined,
    color: form?.theme_tokens?.color_text || undefined,
    borderColor: form?.theme_tokens?.color_primary || undefined,
  }}
>
  ...
</Card>
```

#### 2.3 入力フィールドへの適用

```tsx
// FieldComponent内でインラインスタイルを適用
<input
  type="text"
  style={{
    backgroundColor: form?.theme_tokens?.color_bg || undefined,
    color: form?.theme_tokens?.color_text || undefined,
    borderColor: form?.theme_tokens?.color_primary || undefined,
  }}
  className="w-full rounded-xl border px-3 py-2 text-sm outline-none focus:ring-4 focus:ring-brand-gold/30 focus:border-brand-gold/40 disabled:opacity-50"
  ...
/>
```

### 3. FormPreviewPage の変更

PublicFormViewPageと同様の変更を適用する。

### 4. 適用対象要素

以下の要素にテーマトークンを適用する：

1. **上位div（`min-h-screen`）**
   - `backgroundColor`: `color_bg`
   - `color`: `color_text`

2. **Cardコンポーネント**
   - `backgroundColor`: `color_bg`
   - `color`: `color_text`
   - `borderColor`: `color_primary`

3. **入力フィールド（input, textarea, select）**
   - `backgroundColor`: `color_bg`
   - `color`: `color_text`
   - `borderColor`: `color_primary`

4. **ボタン要素**
   - `backgroundColor`: `color_primary`
   - `color`: `color_text`（または`color_secondary`）

5. **テキスト要素（h1, h2, h3, p, label等）**
   - `color`: `color_text`

### 5. 優先順位

インラインスタイルはTailwindクラスより優先されるため、以下の優先順位で適用される：

1. インラインスタイル（`style`属性） ← **最優先**
2. Tailwindクラス（`className`属性）
3. CSS変数（`--color-*`）

## 実装手順

### フェーズ1: themeTokens.ts の拡張 ✅
1. ✅ `applyThemeColorsToElement()`関数を追加
2. ✅ `removeThemeColorsFromElement()`関数を追加
3. ✅ `applyThemeTokensToElementWithInlineStyles()`関数を追加

### フェーズ2: PublicFormViewPage の変更 ✅
1. ✅ 上位div（`min-h-screen`）に`data-form-container`属性を追加
2. ✅ `useEffect`で背景色・文字色を適用（`applyThemeTokensToElementWithInlineStyles`を使用）
3. ✅ `Card`コンポーネントにインラインスタイルを追加（`style`属性で`backgroundColor`, `color`, `borderColor`を設定）
4. ✅ `FieldComponent`内の入力フィールドにインラインスタイルを追加
   - `text`, `email`, `tel`, `textarea`, `number`, `date`, `time`, `datetime-local`, `select`に適用
   - `radio`, `checkbox`に`borderColor`と`accentColor`を適用
   - `terms`のチェックボックスにも適用
5. ✅ ボタン要素にインラインスタイルを追加（送信ボタン）
6. ✅ テキスト要素にインラインスタイルを追加（`h1`, `h2`, `h3`, `p`, `label`）
7. ✅ STEP名・GROUP名のボーダーとテキストにインラインスタイルを適用
8. ✅ 表示モード切替UIにもインラインスタイルを適用

### フェーズ3: FormPreviewPage の変更 ✅
1. ✅ PublicFormViewPageと同様の変更を適用
2. ✅ `data-form-container`属性を追加
3. ✅ `Card`コンポーネントにインラインスタイルを追加
4. ✅ `FieldComponent`に`themeTokens`プロパティを追加し、各要素にインラインスタイルを適用

## 注意事項

1. **Tailwindクラスとの併用**
   - インラインスタイルはTailwindクラスより優先される
   - レイアウト関連のクラス（`px-6`, `py-10`, `rounded-xl`など）は維持
   - カラー系のみインラインスタイルで上書き

2. **デフォルト値の扱い**
   - テーマトークンが設定されていない場合は、Tailwindクラスのデフォルトスタイルを使用
   - インラインスタイルは`undefined`の場合は適用しない

3. **パフォーマンス**
   - インラインスタイルは各要素に個別に適用するため、要素数が多い場合はパフォーマンスに注意
   - 必要に応じて、CSS変数とインラインスタイルを併用

4. **クリーンアップ**
   - `useEffect`のクリーンアップ関数でインラインスタイルを削除
   - メモリリークを防止

## 実装完了項目

### ✅ 実装済み
1. ✅ `themeTokens.ts`にインラインスタイル適用関数を追加
2. ✅ PublicFormViewPage: 上位divに背景色・文字色を適用
3. ✅ PublicFormViewPage: Cardコンポーネントにインラインスタイルを適用
4. ✅ PublicFormViewPage: 入力フィールドにインラインスタイルを適用
5. ✅ PublicFormViewPage: ボタン要素にインラインスタイルを適用
6. ✅ PublicFormViewPage: テキスト要素にインラインスタイルを適用
7. ✅ FormPreviewPage: 同様の変更を適用

### 実装詳細

#### 適用された要素
- **上位div（`data-form-container`）**: 背景色（`color_bg`）、文字色（`color_text`）
- **Cardコンポーネント**: 背景色、文字色、ボーダー色（`color_primary`）
- **入力フィールド（input, textarea, select）**: 背景色、文字色、ボーダー色
- **ラジオボタン・チェックボックス**: ボーダー色、アクセント色（`accentColor`）
- **ボタン要素**: 背景色（`color_primary`）、文字色
- **テキスト要素（h1, h2, h3, p, label）**: 文字色
- **STEP名・GROUP名**: ボーダー色、文字色

#### インラインスタイルの適用方法
```tsx
// 例: 入力フィールド
<input
  style={{
    backgroundColor: themeTokens?.color_bg || undefined,
    color: themeTokens?.color_text || undefined,
    borderColor: themeTokens?.color_primary || undefined,
  }}
  className="..." // Tailwindクラスは維持
/>
```

## テスト項目

1. テーマトークンが設定されている場合、背景色・文字色が正しく適用される
2. テーマトークンが設定されていない場合、デフォルトスタイルが表示される
3. テーマトークンを変更した場合、リアルタイムで反映される
4. 複数のフォームで異なるテーマトークンを設定した場合、それぞれ正しく適用される
5. クリーンアップ関数が正しく動作し、メモリリークが発生しない
6. インラインスタイルがTailwindクラスより優先されることを確認

## 関連ファイル

- `src/utils/themeTokens.ts`: テーマトークン変換ユーティリティ
- `src/pages/public/PublicFormViewPage.tsx`: 公開フォーム画面
- `src/pages/forms/FormPreviewPage.tsx`: プレビュー画面
- `src/components/Card.tsx`: Cardコンポーネント

## 保留タスク

以下のタスクは別途実装予定：

1. ロゴアップロード機能の実装
2. レイアウト幅設定機能の実装
3. ScreenHeader/Badge削除、フォーム名・説明の多言語表示
4. 表示モード機能の削除
