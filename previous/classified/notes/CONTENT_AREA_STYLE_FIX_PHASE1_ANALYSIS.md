# フェーズ1: 確認と分析結果

## 分析日時
2026-01-20

## タスク4-1: applyElementStyle関数の動作確認

### 確認箇所
- **ファイル**: `src/utils/customStyle.ts`
- **行数**: 14-43行目

### 分析結果

#### ✅ 確認できた動作

1. **インラインスタイルの適用方法**:
   ```typescript
   element.style.setProperty(cssProperty, value);
   ```
   - `setProperty`メソッドを使用してインラインスタイルを設定
   - 既存の同じプロパティを上書きする（例: `backgroundColor`が既に設定されている場合、新しい値で上書きされる）

2. **CSSプロパティ名の変換**:
   ```typescript
   const cssProperty = key.replace(/([A-Z])/g, '-$1').toLowerCase();
   ```
   - キャメルケース（`backgroundColor`）をケバブケース（`background-color`）に変換
   - 正しく動作している

3. **classNameの適用**:
   ```typescript
   const existingClasses = element.className.split(' ').filter(c => c);
   const newClasses = config.className.split(' ').filter(c => c);
   const allClasses = [...new Set([...existingClasses, ...newClasses])];
   element.className = allClasses.join(' ');
   ```
   - 既存のクラスを保持しつつ、新しいクラスを追加
   - 重複を除去している

#### ⚠️ 問題点・確認が必要な点

1. **CSS変数との関係**:
   - `setProperty`で設定されるインラインスタイルは、CSS変数（`--color-bg`など）とは別のプロパティ
   - 例: `element.style.setProperty('background-color', '#ffffff')`は、`--color-bg`変数とは独立している
   - **問題**: CSS変数が設定されている場合、インラインスタイルで上書きしても、CSS変数が残っていると優先される可能性がある
   - **確認が必要**: CSS変数とインラインスタイルの優先順位を確認

2. **既存のインラインスタイルの上書き**:
   - `setProperty`は既存の値を上書きするが、他のプロパティは保持される
   - **確認が必要**: `theme_tokens`から適用されたインラインスタイル（`backgroundColor`, `color`など）が正しく上書きされるか

3. **クリーンアップ機能の不足**:
   - `applyElementStyle`関数にはクリーンアップ機能がない
   - 適用したスタイルを削除する機能がない
   - **問題**: `customStyleConfig`が削除された場合、適用したスタイルが残る可能性がある

### 結論

- ✅ `applyElementStyle`関数は基本的に正しく動作している
- ⚠️ CSS変数との関係を確認する必要がある
- ⚠️ 既存のインラインスタイルが正しく上書きされるか確認が必要

---

## タスク4-2: applyCustomStyleConfig関数のcontent要素処理確認

### 確認箇所
- **ファイル**: `src/utils/customStyle.ts`
- **行数**: 76-117行目、特に104行目

### 分析結果

#### ✅ 確認できた動作

1. **content要素の取得**:
   ```typescript
   const elements = containerElement.querySelectorAll(`[data-custom-style="${key}"]`);
   ```
   - `querySelectorAll`を使用して`data-custom-style="content"`属性を持つ要素を取得
   - 複数の要素が取得される可能性がある（現在は1つのはず）

2. **スタイルの適用順序**:
   ```typescript
   // 1. コンテナを処理
   if (config.elements.container) {
     applyElementStyle(containerElement, config.elements.container);
   }
   
   // 2. その他の要素を処理（containerを除く）
   Object.entries(config.elements).forEach(([key, elementConfig]) => {
     if (key === 'container') return;
     // ...
   });
   ```
   - `container`要素が最初に処理される
   - その後、`content`要素などが処理される
   - **確認**: `content`要素は`container`要素の子要素なので、適用順序は正しい

3. **型定義の確認**:
   - `CustomStyleConfig`の`elements`に`content?: ElementStyleConfig`が定義されている
   - 型定義は正しい

#### ⚠️ 問題点・確認が必要な点

1. **要素の存在確認**:
   - `querySelectorAll`は要素が見つからない場合、空のNodeListを返す
   - **確認が必要**: `data-custom-style="content"`属性を持つ要素が実際に存在するか確認
   - **確認が必要**: 要素が取得できているか、実際のDOMを確認

2. **適用タイミング**:
   - `applyCustomStyleConfig`は`useEffect`内で呼び出される
   - **確認が必要**: DOM要素が存在するタイミングで呼び出されているか確認
   - **確認が必要**: `theme_tokens`適用の後に呼び出されているか確認

3. **クリーンアップ機能**:
   - `applyCustomStyleConfig`はクリーンアップ関数を返すが、`applyElementStyle`にはクリーンアップ機能がない
   - **問題**: `customStyleConfig`が削除された場合、適用したスタイルが残る可能性がある

### 結論

- ✅ `applyCustomStyleConfig`関数は`content`要素を処理する仕組みがある
- ⚠️ 実際のDOMで要素が取得できているか確認が必要
- ⚠️ 適用タイミングを確認する必要がある

---

## タスク2-1: PublicFormViewPage.tsxのtheme_tokens適用の動作確認

### 確認箇所
- **ファイル**: `src/pages/public/PublicFormViewPage.tsx`
- **行数**: 786-811行目（theme_tokens適用）、813-837行目（customStyleConfig適用）

### 分析結果

#### ✅ 確認できた動作

1. **theme_tokens適用の条件**:
   ```typescript
   if (!form || !form.theme_tokens || customStyleConfig) return;
   ```
   - `customStyleConfig`が存在する場合、`theme_tokens`適用がスキップされる
   - 正しく動作している

2. **適用方法**:
   ```typescript
   // 1. 上位div（data-form-container）に背景色・文字色をインラインスタイルで適用
   const cleanupContainer = applyThemeTokensToElementWithInlineStyles(container, form.theme_tokens);
   
   // 2. フォーム表示部分（data-form-theme）にCSS変数を適用（カラー系は除外）
   const cssVars = convertThemeTokensToCssVars(form.theme_tokens);
   delete cssVars["--color-bg"];
   delete cssVars["--color-text"];
   applyCssVarsToElement(formThemeContainer, cssVars);
   ```
   - `data-form-container`にインラインスタイル（背景色・文字色）を適用
   - `data-form-theme`（コンテンツ領域）にCSS変数を適用（カラー系は除外）

3. **customStyleConfig適用時のCSS変数削除**:
   ```typescript
   // customStyleConfigが存在する場合、data-form-theme要素（コンテンツ領域）からCSS変数を削除
   const formThemeContainer = document.querySelector(`[data-form-theme]`) as HTMLElement;
   if (formThemeContainer && form?.theme_tokens) {
     const cssVars = convertThemeTokensToCssVars(form.theme_tokens);
     delete cssVars["--color-bg"];
     delete cssVars["--color-text"];
     removeCssVarsFromElement(formThemeContainer, cssVars);
   }
   ```
   - `customStyleConfig`適用時に、既存のCSS変数を削除している

#### ⚠️ 問題点・確認が必要な点

1. **タイミングの問題**:
   - `theme_tokens`適用の`useEffect`（786-811行目）と`customStyleConfig`適用の`useEffect`（813-837行目）は別々に実行される
   - **問題**: `customStyleConfig`が存在する場合、`theme_tokens`適用がスキップされるが、以前に適用されたCSS変数が残っている可能性がある
   - **問題**: `customStyleConfig`が後から設定された場合、既に適用されたCSS変数が残る可能性がある

2. **依存配列の問題**:
   ```typescript
   // theme_tokens適用
   }, [form]);
   
   // customStyleConfig適用
   }, [customStyleConfig, form]);
   ```
   - `theme_tokens`適用の依存配列に`customStyleConfig`が含まれていない
   - **問題**: `customStyleConfig`が後から設定された場合、`theme_tokens`適用の`useEffect`が再実行されない
   - **問題**: `customStyleConfig`が削除された場合、`theme_tokens`が再適用されない可能性がある

3. **インラインスタイルのクリア**:
   - `customStyleConfig`適用時に、CSS変数は削除しているが、インラインスタイルはクリアしていない
   - **問題**: `theme_tokens`から適用されたインラインスタイル（`data-form-theme`要素に直接適用されたもの）が残る可能性がある
   - **確認が必要**: `data-form-theme`要素にインラインスタイルが適用されているか確認

4. **要素の取得方法**:
   - `document.querySelector`を使用して要素を取得している
   - **確認が必要**: 要素が存在するタイミングで取得できているか確認

### 結論

- ✅ `customStyleConfig`が存在する場合、`theme_tokens`適用がスキップされる
- ⚠️ `customStyleConfig`が後から設定された場合、既存のCSS変数が残る可能性がある
- ⚠️ インラインスタイルのクリアが必要
- ⚠️ 依存配列を適切に設定する必要がある

---

## タスク3-1: FormRealtimePreview.tsxのtheme_tokens適用の動作確認

### 確認箇所
- **ファイル**: `src/components/forms/FormRealtimePreview.tsx`
- **行数**: 330-351行目（theme_tokens適用）、354-373行目（customStyleConfig適用）

### 分析結果

#### ✅ 確認できた動作

1. **theme_tokens適用の条件**:
   ```typescript
   if (!themeTokens || !containerRef.current || !formThemeRef.current || customStyleConfig) return;
   ```
   - `customStyleConfig`が存在する場合、`theme_tokens`適用がスキップされる
   - 正しく動作している

2. **適用方法**:
   ```typescript
   const cleanupContainer = applyThemeTokensToElementWithInlineStyles(containerRef.current, themeTokens);
   
   const cssVars = convertThemeTokensToCssVars(themeTokens);
   delete cssVars["--color-bg"];
   delete cssVars["--color-text"];
   applyCssVarsToElement(formThemeRef.current, cssVars);
   ```
   - `PublicFormViewPage.tsx`と同様の処理

3. **customStyleConfig適用時のCSS変数削除**:
   ```typescript
   if (formThemeRef.current && themeTokens) {
     const cssVars = convertThemeTokensToCssVars(themeTokens);
     delete cssVars["--color-bg"];
     delete cssVars["--color-text"];
     removeCssVarsFromElement(formThemeRef.current, cssVars);
   }
   ```
   - `PublicFormViewPage.tsx`と同様の処理

#### ⚠️ 問題点・確認が必要な点

1. **タイミングの問題**:
   - `PublicFormViewPage.tsx`と同様の問題がある
   - **問題**: `customStyleConfig`が後から設定された場合、既に適用されたCSS変数が残る可能性がある

2. **依存配列の問題**:
   ```typescript
   // theme_tokens適用
   }, [themeTokens]);
   
   // customStyleConfig適用
   }, [customStyleConfig, themeTokens]);
   ```
   - `theme_tokens`適用の依存配列に`customStyleConfig`が含まれていない
   - **問題**: `customStyleConfig`が後から設定された場合、`theme_tokens`適用の`useEffect`が再実行されない
   - **問題**: `customStyleConfig`が削除された場合、`theme_tokens`が再適用されない可能性がある

3. **インラインスタイルのクリア**:
   - `PublicFormViewPage.tsx`と同様の問題がある
   - **問題**: インラインスタイルがクリアされていない

4. **refの使用**:
   - `containerRef`と`formThemeRef`を使用している
   - **確認が必要**: refが正しく設定されているか確認

### 結論

- ✅ `PublicFormViewPage.tsx`と同様の実装
- ⚠️ `PublicFormViewPage.tsx`と同様の問題がある
- ⚠️ 修正が必要

---

## 総合的な問題点

### 1. CSS変数とインラインスタイルの優先順位

**問題**:
- CSS変数（`--color-bg`など）が設定されている場合、インラインスタイルで上書きしても、CSS変数が残っていると優先される可能性がある
- 例: `element.style.setProperty('background-color', '#ffffff')`を設定しても、`--color-bg`変数が残っていると、CSS変数が優先される可能性がある

**解決策**:
- `customStyleConfig`が存在する場合、CSS変数を削除してからインラインスタイルを適用する
- 現在はCSS変数を削除しているが、タイミングの問題で正しく動作していない可能性がある

### 2. タイミングの問題

**問題**:
- `theme_tokens`適用の`useEffect`と`customStyleConfig`適用の`useEffect`は別々に実行される
- `customStyleConfig`が後から設定された場合、既に適用されたCSS変数が残る可能性がある

**解決策**:
- `customStyleConfig`適用の`useEffect`で、既存のCSS変数を確実に削除する
- 依存配列を適切に設定し、`customStyleConfig`の変更時に正しく動作するようにする

### 3. インラインスタイルのクリア

**問題**:
- `theme_tokens`から適用されたインラインスタイルが残る可能性がある
- `data-form-theme`要素に直接適用されたインラインスタイルがクリアされていない

**解決策**:
- `customStyleConfig`が存在する場合、`data-form-theme`要素のインラインスタイルをクリアする
- 特に`backgroundColor`と`color`をクリアする

### 4. 依存配列の問題

**問題**:
- `theme_tokens`適用の`useEffect`の依存配列に`customStyleConfig`が含まれていない
- `customStyleConfig`が後から設定された場合、`theme_tokens`適用の`useEffect`が再実行されない

**解決策**:
- 依存配列に`customStyleConfig`を追加する
- または、`customStyleConfig`適用の`useEffect`で、既存のCSS変数とインラインスタイルを確実に削除する

---

## 次のステップ（フェーズ2）

フェーズ1の分析結果を基に、以下の修正を実装する必要があります：

1. **PublicFormViewPage.tsx**:
   - `customStyleConfig`適用の`useEffect`で、既存のCSS変数とインラインスタイルを確実に削除する
   - 依存配列を適切に設定する

2. **FormRealtimePreview.tsx**:
   - `PublicFormViewPage.tsx`と同様の修正を実装する

3. **applyCustomStyleConfig関数**:
   - 必要に応じて、CSS変数を削除してからインラインスタイルを適用する
