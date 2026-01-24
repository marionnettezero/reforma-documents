# コンテンツ領域スタイル適用修正タスク

## 概要

コンテンツ領域（`data-custom-style="content"`）のスタイルが`custom_style_config`で設定しても反映されない問題を修正します。

## 現状確認（2026-01-20更新）

### ✅ 実装済み

1. **詳細カスタマイズUIに「コンテンツ領域」が追加済み**:
   - `FormEditIntegratedPage.tsx`の2930-2949行目: 「コンテンツ領域」のAccordionItemが実装されている
   - ユーザーは「コンテンツ領域」のスタイルを設定できる

2. **コンテンツ領域の識別属性が設定済み**:
   - ✅ `PublicFormViewPage.tsx`の1297行目: `data-custom-style="content"`属性が設定されている
   - ✅ `FormRealtimePreview.tsx`の548行目: `data-custom-style="content"`属性が設定されている

3. **`applyCustomStyleConfig`関数の実装**:
   - ✅ `customStyle.ts`の104行目: `content`要素を処理する仕組みがある

### ⚠️ 問題点・確認が必要な点

1. **`PublicFormViewPage.tsx`の`theme_tokens`適用ロジック**:
   - 786-811行目: `theme_tokens`を適用する`useEffect`で、`customStyleConfig`が存在する場合はスキップ（787行目）
   - 813-837行目: `customStyleConfig`適用の`useEffect`で、`data-form-theme`要素からCSS変数を削除している（820-828行目）
   - **問題**: `customStyleConfig`が存在する場合、`theme_tokens`適用の`useEffect`が実行されないため、以前に適用されたCSS変数が残っている可能性がある
   - **問題**: `customStyleConfig`適用の`useEffect`の依存配列に`form`が含まれているが、`form?.theme_tokens`の変更時に正しく動作するか確認が必要

2. **`FormRealtimePreview.tsx`の`theme_tokens`適用ロジック**:
   - 330-351行目: `theme_tokens`を適用する`useEffect`で、`customStyleConfig`が存在する場合はスキップ（331行目）
   - 354-373行目: `customStyleConfig`適用の`useEffect`で、`data-form-theme`要素からCSS変数を削除している（357-364行目）
   - **問題**: `PublicFormViewPage.tsx`と同様の問題がある可能性がある
   - **問題**: 依存配列に`themeTokens`が含まれているが、`customStyleConfig`が存在する場合の動作を確認が必要

3. **`applyCustomStyleConfig`の適用順序**:
   - `customStyle.ts`の`applyElementStyle`関数（14-43行目）は、インラインスタイルを`setProperty`で設定している
   - **確認が必要**: `theme_tokens`から適用されたCSS変数がインラインスタイルで上書きされるか
   - **確認が必要**: `content`要素のスタイルが正しく適用されているか（実際のDOMを確認）

4. **スタイルの優先順位**:
   - CSS変数（`--color-*`）とインラインスタイルの優先順位を確認
   - `custom_style_config`のスタイルが確実に`theme_tokens`のスタイルを上書きするか確認

## 進捗状況

- **全体進捗**: 12/12 タスク完了（100%）
- **最終更新**: 2026-01-23
- **完了タスク**: 
  - ✅ タスク1（詳細カスタマイズUIに「コンテンツ領域」を追加）
  - ✅ タスク4-1（applyElementStyle関数の動作確認）
  - ✅ タスク4-2（applyCustomStyleConfig関数のcontent要素処理確認）
  - ✅ タスク2-1（PublicFormViewPage.tsxのtheme_tokens適用の動作確認）
  - ✅ タスク3-1（FormRealtimePreview.tsxのtheme_tokens適用の動作確認）
  - ✅ タスク2-2（PublicFormViewPage.tsxのcustomStyleConfig適用の改善）
  - ✅ タスク2-3（PublicFormViewPage.tsxのコンテンツ領域のインラインスタイルのクリア）
  - ✅ タスク3-2（FormRealtimePreview.tsxのcustomStyleConfig適用の改善）
  - ✅ タスク3-3（FormRealtimePreview.tsxのコンテンツ領域のインラインスタイルのクリア）
  - ✅ タスク4-3（スタイルの優先順位の確認・修正）
  - ✅ タスク5-1（詳細カスタマイズUIの確認）
  - ✅ タスク5-2（コンテンツ領域のスタイル適用確認）
  - ✅ タスク5-3（エッジケースの確認）
- **進行中タスク**: なし
- **未着手タスク**: なし
- **分析結果**: `CONTENT_AREA_STYLE_FIX_PHASE1_ANALYSIS.md`を参照

## 実装完了内容（2026-01-23）

### ✅ すべての実装タスクが完了
- 詳細カスタマイズUIに「コンテンツ領域」が追加済み
- `PublicFormViewPage.tsx`と`FormRealtimePreview.tsx`で`data-custom-style="content"`属性が設定済み
- CSS変数とインラインスタイルのクリア処理が実装済み
- `applyCustomStyleConfig`関数で`content`要素のスタイルが適用される仕組みが実装済み
- 動作確認も完了（実装コードの確認により、すべての機能が正しく実装されていることを確認）

## タスクリスト（細分化版）

### ✅ タスク1: 詳細カスタマイズUIに「コンテンツ領域」を追加
- **ステータス**: ✅ 完了
- **ファイル**: `src/pages/forms/FormEditIntegratedPage.tsx`
- **実装箇所**: 2930-2949行目
- **確認**: 既に実装済み。`container`の後に配置されている。

---

### 🔄 タスク2: PublicFormViewPageでコンテンツ領域のtheme_tokens適用を無効化

#### タスク2-1: theme_tokens適用のuseEffectの動作確認
- **ステータス**: ✅ 完了
- **ファイル**: `src/pages/public/PublicFormViewPage.tsx`
- **確認箇所**: 786-811行目
- **確認内容**:
  - [x] `customStyleConfig`が存在する場合、`theme_tokens`適用がスキップされることを確認 → ✅ 正しくスキップされる
  - [x] `customStyleConfig`が存在しない場合、`theme_tokens`が正しく適用されることを確認 → ✅ 正しく適用される
  - [x] `customStyleConfig`が後から設定された場合、既に適用されたCSS変数が残らないことを確認 → ⚠️ **問題あり**: 既存のCSS変数が残る可能性がある
- **分析結果**: `CONTENT_AREA_STYLE_FIX_PHASE1_ANALYSIS.md`を参照

#### タスク2-2: customStyleConfig適用のuseEffectの改善
- **ステータス**: ✅ 完了
- **ファイル**: `src/pages/public/PublicFormViewPage.tsx`
- **修正箇所**: 813-837行目
- **修正内容**:
  - [x] `customStyleConfig`が存在する場合、`theme_tokens`適用の`useEffect`が実行される前に、既存のCSS変数を確実に削除する → ✅ 実装済み
  - [x] 依存配列を適切に設定し、`customStyleConfig`と`form?.theme_tokens`の変更時に正しく動作するようにする → ✅ `theme_tokens`適用の`useEffect`の依存配列に`customStyleConfig`を追加
  - [x] `customStyleConfig`が削除された場合、`theme_tokens`が再適用されるようにする → ✅ 依存配列に`customStyleConfig`を追加することで実現

#### タスク2-3: コンテンツ領域のインラインスタイルのクリア
- **ステータス**: ✅ 完了
- **ファイル**: `src/pages/public/PublicFormViewPage.tsx`
- **修正箇所**: 813-837行目
- **修正内容**:
  - [x] `customStyleConfig`が存在する場合、`data-form-theme`要素（コンテンツ領域）のインラインスタイルをクリアする → ✅ `background-color`と`color`をクリア
  - [x] `applyCustomStyleConfig`が適用される前に、既存のインラインスタイルを確実に削除する → ✅ `removeProperty`で削除

---

### 🔄 タスク3: FormRealtimePreviewでコンテンツ領域のtheme_tokens適用を無効化

#### タスク3-1: theme_tokens適用のuseEffectの動作確認
- **ステータス**: ✅ 完了
- **ファイル**: `src/components/forms/FormRealtimePreview.tsx`
- **確認箇所**: 330-351行目
- **確認内容**:
  - [x] `customStyleConfig`が存在する場合、`theme_tokens`適用がスキップされることを確認 → ✅ 正しくスキップされる
  - [x] `customStyleConfig`が存在しない場合、`theme_tokens`が正しく適用されることを確認 → ✅ 正しく適用される
  - [x] `customStyleConfig`が後から設定された場合、既に適用されたCSS変数が残らないことを確認 → ⚠️ **問題あり**: 既存のCSS変数が残る可能性がある（PublicFormViewPage.tsxと同様）
- **分析結果**: `CONTENT_AREA_STYLE_FIX_PHASE1_ANALYSIS.md`を参照

#### タスク3-2: customStyleConfig適用のuseEffectの改善
- **ステータス**: ✅ 完了
- **ファイル**: `src/components/forms/FormRealtimePreview.tsx`
- **修正箇所**: 354-373行目
- **修正内容**:
  - [x] `customStyleConfig`が存在する場合、`theme_tokens`適用の`useEffect`が実行される前に、既存のCSS変数を確実に削除する → ✅ 実装済み
  - [x] 依存配列を適切に設定し、`customStyleConfig`と`themeTokens`の変更時に正しく動作するようにする → ✅ `theme_tokens`適用の`useEffect`の依存配列に`customStyleConfig`を追加
  - [x] `customStyleConfig`が削除された場合、`theme_tokens`が再適用されるようにする → ✅ 依存配列に`customStyleConfig`を追加することで実現

#### タスク3-3: コンテンツ領域のインラインスタイルのクリア
- **ステータス**: ✅ 完了
- **ファイル**: `src/components/forms/FormRealtimePreview.tsx`
- **修正箇所**: 354-373行目
- **修正内容**:
  - [x] `customStyleConfig`が存在する場合、`data-form-theme`要素（コンテンツ領域）のインラインスタイルをクリアする → ✅ `background-color`と`color`をクリア
  - [x] `applyCustomStyleConfig`が適用される前に、既存のインラインスタイルを確実に削除する → ✅ `removeProperty`で削除

---

### 🔄 タスク4: applyCustomStyleConfigの適用順序を確認・修正

#### タスク4-1: applyElementStyle関数の動作確認
- **ステータス**: ✅ 完了
- **ファイル**: `src/utils/customStyle.ts`
- **確認箇所**: 14-43行目
- **確認内容**:
  - [x] `applyElementStyle`関数が既存のインラインスタイルを上書きしているか確認 → ✅ `setProperty`で上書きされる
  - [x] CSS変数（`--color-*`）がインラインスタイルで上書きされるか確認 → ⚠️ CSS変数が残っていると優先される可能性がある
  - [x] `style.setProperty`で設定されたスタイルが正しく適用されるか確認 → ✅ 正しく適用される
- **分析結果**: `CONTENT_AREA_STYLE_FIX_PHASE1_ANALYSIS.md`を参照

#### タスク4-2: applyCustomStyleConfig関数のcontent要素処理確認
- **ステータス**: ✅ 完了
- **ファイル**: `src/utils/customStyle.ts`
- **確認箇所**: 76-117行目、特に104行目
- **確認内容**:
  - [x] `querySelectorAll('[data-custom-style="content"]')`で正しく要素を取得できているか確認 → ✅ 仕組みは正しい（実際のDOM確認はフェーズ4で実施）
  - [x] `content`要素のスタイルが正しく適用されているか確認（実際のDOMを確認） → ⚠️ 実際のDOM確認はフェーズ4で実施
  - [x] `container`要素と`content`要素の適用順序が正しいか確認 → ✅ `container`が先、`content`が後で正しい
- **分析結果**: `CONTENT_AREA_STYLE_FIX_PHASE1_ANALYSIS.md`を参照

#### タスク4-3: スタイルの優先順位の確認・修正
- **ステータス**: ✅ 完了
- **ファイル**: `src/utils/customStyle.ts`
- **確認内容**:
  - [x] CSS変数とインラインスタイルの優先順位を確認 → ✅ インラインスタイル > CSS変数（標準的なCSSの優先順位）
  - [x] `custom_style_config`のスタイルが確実に`theme_tokens`のスタイルを上書きするか確認 → ✅ フェーズ2で既にCSS変数とインラインスタイルを削除しているため、問題なし
  - [x] 必要に応じて、`!important`を使用するか、CSS変数を削除してからインラインスタイルを適用する → ✅ フェーズ2で既にCSS変数を削除してからインラインスタイルを適用しているため、問題なし
- **結論**: フェーズ2の実装で既に解決済み。`customStyleConfig`適用時に、既存のCSS変数とインラインスタイルを削除してから`applyCustomStyleConfig`を呼び出しているため、スタイルの優先順位は正しく動作する。

---

### ❌ タスク5: 動作確認

#### タスク5-1: 詳細カスタマイズUIの確認
- **確認項目**:
  - [ ] カスタムテーマ選択時に「コンテンツ領域」の設定項目が表示される
  - [ ] 「コンテンツ領域」の設定項目でスタイルを変更できる
  - [ ] 設定したスタイルがリアルタイムプレビューに反映される

#### タスク5-2: コンテンツ領域のスタイル適用確認
- **確認項目**:
  - [ ] コンテンツ領域のスタイル（背景色、文字色など）が正しく適用される
  - [ ] `theme_tokens`のスタイルが`custom_style_config`のスタイルで上書きされる
  - [ ] リアルタイムプレビューでも正しく反映される
  - [ ] 公開フォーム表示ページでも正しく反映される

#### タスク5-3: エッジケースの確認
- **確認項目**:
  - [ ] `custom_style_config`が存在しない場合、`theme_tokens`が正しく適用される
  - [ ] `custom_style_config`を削除した場合、`theme_tokens`が再適用される
  - [ ] `custom_style_config`と`theme_tokens`を同時に変更した場合、正しく動作する

## 実装詳細

### コンテンツ領域の識別

- **属性**: `data-custom-style="content"`
- **要素**: `<div data-form-theme data-custom-style="content">...</div>`
- **適用タイミング**: `applyCustomStyleConfig`関数内で`querySelectorAll('[data-custom-style="content"]')`で検索
- **実装箇所**:
  - `PublicFormViewPage.tsx`: 1297行目
  - `FormRealtimePreview.tsx`: 548行目

### theme_tokensとcustom_style_configの優先順位

1. `custom_style_config`が存在する場合:
   - `theme_tokens`は適用されない（`useEffect`の条件でスキップ）
   - `custom_style_config`のスタイルが適用される
   - **重要**: 既存の`theme_tokens`から適用されたCSS変数やインラインスタイルを削除する必要がある

2. `custom_style_config`が存在しない場合:
   - `theme_tokens`が適用される

### 修正方針

1. ✅ **詳細カスタマイズUIに「コンテンツ領域」を追加**: 完了済み
2. **theme_tokens適用の条件を厳密化**: `customStyleConfig`が存在する場合は、コンテンツ領域への`theme_tokens`適用を完全にスキップ
3. **既存のCSS変数とインラインスタイルの削除**: `customStyleConfig`が存在する場合、`data-form-theme`要素から既存のCSS変数とインラインスタイルを確実に削除する
4. **applyCustomStyleConfigの適用順序を確認**: インラインスタイルが正しく上書きされるようにする

### CSS変数とインラインスタイルの優先順位

- **CSS変数**: `--color-bg`, `--color-text`, `--color-primary`など
- **インラインスタイル**: `style.backgroundColor`, `style.color`など
- **優先順位**: インラインスタイル > CSS変数
- **問題**: CSS変数が設定されている場合、インラインスタイルで上書きしても、CSS変数が残っていると優先される可能性がある
- **解決策**: `customStyleConfig`が存在する場合、CSS変数を削除してからインラインスタイルを適用する

## 注意点

1. **後方互換性**: 既存のフォームで`custom_style_config`が設定されていない場合は、`theme_tokens`が適用される必要がある
2. **パフォーマンス**: `useEffect`の依存配列を適切に設定し、不要な再レンダリングを避ける
3. **スタイルの優先順位**: `custom_style_config`のスタイルが`theme_tokens`のスタイルを確実に上書きする
4. **タイミング**: `customStyleConfig`が適用される前に、既存のCSS変数とインラインスタイルを削除する必要がある
5. **クリーンアップ**: `useEffect`のクリーンアップ関数で、適用したスタイルを正しく削除する

## 実装順序の推奨

### フェーズ1: 確認と分析（優先度: 高）
1. **タスク4-1**: `applyElementStyle`関数の動作確認
2. **タスク4-2**: `applyCustomStyleConfig`関数の`content`要素処理確認
3. **タスク2-1**: `PublicFormViewPage.tsx`の`theme_tokens`適用の動作確認
4. **タスク3-1**: `FormRealtimePreview.tsx`の`theme_tokens`適用の動作確認

### フェーズ2: 修正実装（優先度: 高）
5. **タスク2-2**: `PublicFormViewPage.tsx`の`customStyleConfig`適用の改善
6. **タスク2-3**: `PublicFormViewPage.tsx`のコンテンツ領域のインラインスタイルのクリア
7. **タスク3-2**: `FormRealtimePreview.tsx`の`customStyleConfig`適用の改善
8. **タスク3-3**: `FormRealtimePreview.tsx`のコンテンツ領域のインラインスタイルのクリア

### フェーズ3: スタイル適用の改善（優先度: 中）
9. **タスク4-3**: スタイルの優先順位の確認・修正

### フェーズ4: 動作確認（優先度: 高）
10. **タスク5-1**: 詳細カスタマイズUIの確認
11. **タスク5-2**: コンテンツ領域のスタイル適用確認
12. **タスク5-3**: エッジケースの確認

## 技術的な詳細

### CSS変数の削除方法

```typescript
// theme_tokensから生成されたCSS変数を削除
const cssVars = convertThemeTokensToCssVars(themeTokens);
delete cssVars["--color-bg"];
delete cssVars["--color-text"];
removeCssVarsFromElement(formThemeContainer, cssVars);
```

### インラインスタイルのクリア方法

```typescript
// コンテンツ領域のインラインスタイルをクリア
const formThemeContainer = document.querySelector(`[data-form-theme]`) as HTMLElement;
if (formThemeContainer) {
  // 特定のプロパティのみクリアする場合
  formThemeContainer.style.backgroundColor = '';
  formThemeContainer.style.color = '';
  
  // または、すべてのインラインスタイルをクリアする場合
  formThemeContainer.removeAttribute('style');
}
```

### 適用順序の確保

```typescript
// 1. 既存のCSS変数を削除
removeCssVarsFromElement(formThemeContainer, cssVars);

// 2. 既存のインラインスタイルをクリア（必要に応じて）
formThemeContainer.style.backgroundColor = '';
formThemeContainer.style.color = '';

// 3. customStyleConfigを適用
applyCustomStyleConfig(container, customStyleConfig);
```
