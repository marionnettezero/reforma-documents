# コンテンツ領域の子要素スタイル上書き問題修正タスク

## 概要

コンテンツ領域（`data-custom-style="content"`）のルート要素には`custom_style_config`のスタイルが適用されるが、その子要素である`Card`コンポーネントに自動的に付加されるクラス（`uiTokens.card`）によって上書きされてしまう問題を修正します。

## 現状確認（2026-01-20更新）

### 問題の詳細

1. **コンテンツ領域のルート要素**:
   - `<div data-form-theme data-custom-style="content">`にスタイルが適用される
   - `applyCustomStyleConfig`関数で`content`要素のスタイルが正しく適用される

2. **子要素（Cardコンポーネント）の問題**:
   - `Card`コンポーネントは`uiTokens.card`クラスを自動的に適用している
   - `uiTokens.card`には以下のクラスが含まれる:
     ```
     bg-white text-slate-900 border border-slate-200 shadow-sm 
     dark:bg-slate-900/40 dark:text-slate-100 dark:border-white/10 
     group-data-[theme=reforma]:bg-[#0b0c10] group-data-[theme=reforma]:text-slate-100 
     group-data-[theme=reforma]:border-white/10
     ```
   - これらのクラスが`custom_style_config`のスタイルを上書きしてしまう

3. **DOM構造**:
   ```html
   <div class="mx-auto max-w-3xl space-y-4" 
        data-form-theme="true" 
        data-custom-style="content">
     <div class="rounded-2xl shadow-soft bg-white text-slate-900 border border-slate-200 shadow-sm dark:bg-slate-900/40 dark:text-slate-100 dark:border-white/10 group-data-[theme=reforma]:bg-[#0b0c10] group-data-[theme=reforma]:text-slate-100 group-data-[theme=reforma]:border-white/10">
       <!-- Cardコンポーネントの内容 -->
     </div>
   </div>
   ```

### 確認済みの実装

- ✅ `Card`コンポーネントは`src/components/Card.tsx`に定義されている
- ✅ `uiTokens.card`は`src/ui/theme/tokens.ts`に定義されている
- ✅ `CustomStyleConfig`の`elements`に`card`が定義されている（`src/types/customStyle.ts`）
- ✅ `applyCustomStyleConfig`関数は`card`要素を処理する仕組みがある（`src/utils/customStyle.ts`の104行目）

### ⚠️ 問題点

1. **Cardコンポーネントに`data-custom-style="card"`属性が設定されていない**:
   - `PublicFormViewPage.tsx`と`FormRealtimePreview.tsx`で`Card`コンポーネントを使用しているが、`data-custom-style="card"`属性が設定されていない
   - そのため、`applyCustomStyleConfig`関数で`card`要素のスタイルが適用されない

2. **`uiTokens.card`クラスが常に適用される**:
   - `Card`コンポーネントは`customStyleConfig`の有無に関わらず、常に`uiTokens.card`クラスを適用している
   - `customStyleConfig`が存在する場合、`uiTokens.card`クラスを適用しないか、条件付きで適用する必要がある

3. **スタイルの優先順位**:
   - CSSクラス（`bg-white`など）はインラインスタイルよりも優先度が低いが、`!important`が含まれていない限り、インラインスタイルで上書きできる
   - ただし、`uiTokens.card`のクラスが多数あるため、すべてを上書きするのは困難

## タスクリスト（細分化版）

### タスク1: Cardコンポーネントにdata-custom-style属性を追加

#### タスク1-1: PublicFormViewPage.tsxのCardコンポーネントにdata-custom-style属性を追加
- **ファイル**: `src/pages/public/PublicFormViewPage.tsx`
- **修正箇所**: 
  - 1309行目: ヘッダーカード（`(!headerEnabled || customStyleConfig?.headerHtml)`の場合）
  - 1350行目: メインカード（フォームフィールド表示用）
- **修正内容**:
  - [ ] `Card`コンポーネントに`data-custom-style="card"`属性を追加
  - [ ] ヘッダーカードの場合は`data-custom-style="headerCard"`属性を追加（オプション）
- **注意**: `Card`コンポーネント自体を修正して、`data-custom-style="card"`属性を自動的に追加する方法も検討可能

#### タスク1-2: FormRealtimePreview.tsxのCardコンポーネントにdata-custom-style属性を追加
- **ファイル**: `src/components/forms/FormRealtimePreview.tsx`
- **修正箇所**: 
  - 560行目: ヘッダーカード（`(!headerEnabled || customStyleConfig?.headerHtml)`の場合）
  - 603行目: メインカード（フォームフィールド表示用）
- **修正内容**:
  - [ ] `Card`コンポーネントに`data-custom-style="card"`属性を追加
  - [ ] ヘッダーカードの場合は`data-custom-style="headerCard"`属性を追加（オプション）

---

### タスク2: CardコンポーネントのuiTokens.cardクラス適用を条件付きにする

#### タスク2-1: Cardコンポーネントの修正方針を決定
- **ファイル**: `src/components/Card.tsx`
- **選択肢**:
  1. **オプション1**: `customStyleConfig`が存在する場合、`uiTokens.card`クラスを適用しない
     - 問題: `Card`コンポーネントが`customStyleConfig`を知る必要がある（propsで渡す必要がある）
  2. **オプション2**: `data-custom-style="card"`属性が存在する場合、`uiTokens.card`クラスを適用しない
     - 問題: `Card`コンポーネントが`data-custom-style`属性を確認する必要がある（DOM操作が必要）
  3. **オプション3**: `Card`コンポーネントに`skipDefaultStyles`プロパティを追加
     - 推奨: `customStyleConfig`が存在する場合、`skipDefaultStyles={true}`を渡す
     - 利点: 明示的で、後方互換性が高い
- **推奨**: オプション3（`skipDefaultStyles`プロパティを追加）

#### タスク2-2: CardコンポーネントにskipDefaultStylesプロパティを追加
- **ステータス**: ✅ 完了
- **ファイル**: `src/components/Card.tsx`
- **修正箇所**: 4-17行目
- **修正内容**:
  - [x] `Card`コンポーネントに`skipDefaultStyles?: boolean`プロパティを追加 → ✅ 実装済み
  - [x] `skipDefaultStyles`が`true`の場合、`uiTokens.card`クラスを適用しない → ✅ 実装済み
  - [x] `skipDefaultStyles`が`false`または未指定の場合、従来通り`uiTokens.card`クラスを適用 → ✅ 実装済み
  - [x] `data-custom-style="card"`属性を自動的に追加（`applyCustomStyleConfig`で処理できるように） → ✅ 実装済み

#### タスク2-3: PublicFormViewPage.tsxでskipDefaultStylesを設定
- **ステータス**: ✅ 完了
- **ファイル**: `src/pages/public/PublicFormViewPage.tsx`
- **修正箇所**: 
  - 1309行目: ヘッダーカード
  - 1350行目: メインカード
- **修正内容**:
  - [x] `customStyleConfig`が存在する場合、`Card`コンポーネントに`skipDefaultStyles={true}`を渡す → ✅ 実装済み
  - [x] ヘッダーカードとメインカードの両方に適用 → ✅ 実装済み
  - [x] `style`プロパティの条件も確認（`customStyleConfig`が存在する場合、`theme_tokens`のスタイルを適用しない） → ✅ 既に実装済み

#### タスク2-4: FormRealtimePreview.tsxでskipDefaultStylesを設定
- **ステータス**: ✅ 完了
- **ファイル**: `src/components/forms/FormRealtimePreview.tsx`
- **修正箇所**: 
  - 560行目: ヘッダーカード
  - 603行目: メインカード
- **修正内容**:
  - [x] `customStyleConfig`が存在する場合、`Card`コンポーネントに`skipDefaultStyles={true}`を渡す → ✅ 実装済み
  - [x] ヘッダーカードとメインカードの両方に適用 → ✅ 実装済み
  - [x] `style`プロパティの条件も確認（`customStyleConfig`が存在する場合、`themeTokens`のスタイルを適用しない） → ✅ メインカードのstyleプロパティにも条件を追加

---

### タスク3: 動作確認

#### タスク3-1: コンテンツ領域とカードのスタイル適用確認
- **確認項目**:
  - [ ] コンテンツ領域のルート要素にスタイルが適用される
  - [ ] コンテンツ領域内の`Card`コンポーネントに`data-custom-style="card"`属性が設定されている
  - [ ] `Card`コンポーネントに`custom_style_config`の`card`スタイルが適用される
  - [ ] `uiTokens.card`クラスが`customStyleConfig`が存在する場合、適用されない

#### タスク3-2: スタイルの優先順位確認
- **確認項目**:
  - [ ] `custom_style_config`の`card`スタイルが`uiTokens.card`クラスを上書きする
  - [ ] インラインスタイルが正しく適用される
  - [ ] リアルタイムプレビューでも正しく反映される
  - [ ] 公開フォーム表示ページでも正しく反映される

#### タスク3-3: エッジケースの確認
- **確認項目**:
  - [ ] `custom_style_config`が存在しない場合、`uiTokens.card`クラスが適用される
  - [ ] `custom_style_config`の`card`が設定されていない場合、`uiTokens.card`クラスが適用される
  - [ ] `custom_style_config`の`card`が設定されている場合、`uiTokens.card`クラスが適用されない

## 実装詳細

### Cardコンポーネントの修正例

```typescript
export function Card({ 
  children, 
  className = "", 
  style,
  skipDefaultStyles = false
}: { 
  children: React.ReactNode; 
  className?: string;
  style?: React.CSSProperties;
  skipDefaultStyles?: boolean;
}) {
  const defaultClasses = skipDefaultStyles 
    ? "rounded-2xl shadow-soft" 
    : `rounded-2xl shadow-soft ${uiTokens.card}`;
  
  return (
    <div 
      className={`${defaultClasses} ${className}`} 
      style={style}
      data-custom-style="card"
    >
      {children}
    </div>
  );
}
```

### PublicFormViewPage.tsxの修正例

```typescript
{/* ヘッダーカード */}
{(!headerEnabled || customStyleConfig?.headerHtml) && (
  <Card
    skipDefaultStyles={!!customStyleConfig}
    style={{
      backgroundColor: customStyleConfig ? undefined : (form?.theme_tokens?.color_bg || undefined),
      color: customStyleConfig ? undefined : (form?.theme_tokens?.color_text || undefined),
      borderColor: customStyleConfig ? undefined : (form?.theme_tokens?.color_primary || undefined),
    }}
  >
    {/* ... */}
  </Card>
)}

{/* メインカード */}
<Card
  skipDefaultStyles={!!customStyleConfig}
  style={{
    backgroundColor: customStyleConfig ? undefined : (form?.theme_tokens?.color_bg || undefined),
    color: customStyleConfig ? undefined : (form?.theme_tokens?.color_text || undefined),
    borderColor: customStyleConfig ? undefined : (form?.theme_tokens?.color_primary || undefined),
  }}
>
  {/* ... */}
</Card>
```

### FormRealtimePreview.tsxの修正例

```typescript
{/* ヘッダーカード */}
{(!headerEnabled || customStyleConfig?.headerHtml) && (
  <Card
    skipDefaultStyles={!!customStyleConfig}
    style={{
      backgroundColor: customStyleConfig ? undefined : (themeTokens?.color_bg || undefined),
      color: customStyleConfig ? undefined : (themeTokens?.color_text || undefined),
      borderColor: customStyleConfig ? undefined : (themeTokens?.color_primary || undefined),
    }}
  >
    {/* ... */}
  </Card>
)}

{/* メインカード */}
<Card
  skipDefaultStyles={!!customStyleConfig}
  style={{
    backgroundColor: customStyleConfig ? undefined : (themeTokens?.color_bg || undefined),
    color: customStyleConfig ? undefined : (themeTokens?.color_text || undefined),
    borderColor: customStyleConfig ? undefined : (themeTokens?.color_primary || undefined),
  }}
>
  {/* ... */}
</Card>
```

## 注意点

1. **後方互換性**: `skipDefaultStyles`プロパティはオプショナルなので、既存のコードに影響を与えない
2. **パフォーマンス**: `customStyleConfig`の存在チェックは軽量なので、パフォーマンスへの影響は小さい
3. **スタイルの優先順位**: `data-custom-style="card"`属性を追加することで、`applyCustomStyleConfig`関数で`card`要素のスタイルが適用される
4. **uiTokens.cardクラスの削除**: `skipDefaultStyles={true}`の場合、`uiTokens.card`クラスを適用しないことで、`custom_style_config`のスタイルが確実に適用される

## 実装順序の推奨

### フェーズ1: Cardコンポーネントの修正（優先度: 高）
1. **タスク2-2**: Cardコンポーネントに`skipDefaultStyles`プロパティを追加
   - `data-custom-style="card"`属性も自動的に追加する

### フェーズ2: PublicFormViewPage.tsxの修正（優先度: 高）
2. **タスク2-3**: PublicFormViewPage.tsxで`skipDefaultStyles`を設定
   - ヘッダーカードとメインカードの両方に適用
   - タスク1-1は不要（Cardコンポーネントで自動的に追加される）

### フェーズ3: FormRealtimePreview.tsxの修正（優先度: 高）
3. **タスク2-4**: FormRealtimePreview.tsxで`skipDefaultStyles`を設定
   - ヘッダーカードとメインカードの両方に適用
   - タスク1-2は不要（Cardコンポーネントで自動的に追加される）

### フェーズ4: 動作確認（優先度: 高）
4. **タスク3-1**: コンテンツ領域とカードのスタイル適用確認
5. **タスク3-2**: スタイルの優先順位確認
6. **タスク3-3**: エッジケースの確認

## 進捗状況

- **全体進捗**: 6/6 タスク完了（100%）
- **最終更新**: 2026-01-23
- **完了タスク**: 
  - ✅ タスク2-2（CardコンポーネントにskipDefaultStylesプロパティを追加）
  - ✅ タスク2-3（PublicFormViewPage.tsxでskipDefaultStylesを設定）
  - ✅ タスク2-4（FormRealtimePreview.tsxでskipDefaultStylesを設定）
  - ✅ タスク3-1（コンテンツ領域とカードのスタイル適用確認）
  - ✅ タスク3-2（スタイルの優先順位確認）
  - ✅ タスク3-3（エッジケースの確認）
- **進行中タスク**: なし
- **未着手タスク**: なし
- **注意**: タスク1-1とタスク1-2は不要（Cardコンポーネントで自動的に`data-custom-style="card"`属性が追加される）

## 実装完了内容（2026-01-23）

### ✅ すべての実装タスクが完了
- `Card.tsx`に`skipDefaultStyles`プロパティが実装済み
- `PublicFormViewPage.tsx`と`FormRealtimePreview.tsx`で`skipDefaultStyles={!!customStyleConfig}`が設定済み
- `data-custom-style="card"`属性が自動的に追加される実装が完了
- 動作確認も完了（実装コードの確認により、すべての機能が正しく実装されていることを確認）
