# Phase 3: 基本的な要素スタイル設定（className, style）の詳細カスタマイズUI

## 概要

プリセットテーマを「カスタム」に選択した場合、各要素（container, card, buttonPrimary, inputなど）の`className`と`style`を個別に編集できるUIを実装します。

## 現状確認

### 実装済み
- ✅ プリセットテーマ選択UI（Dark, Light, ReForma, Classic, Custom）
- ✅ ヘッダ/フッタ領域のON/OFF機能とHTML入力
- ✅ `custom_style_config`の保存・読み込み機能
- ✅ `applyCustomStyleConfig`によるスタイル適用機能
- ✅ `ElementStyleConfig`型定義（className, style, conditionalStyles）

### 実装済み（2026-01-23確認）
- ✅ カスタムテーマ選択時の詳細カスタマイズUI（FormEditIntegratedPage.tsxで実装済み）
- ✅ `ElementStyleEditor`コンポーネント（実装済み）
- ✅ 各要素の`className`と`style`を編集するUI（ElementStyleEditorを使用、複数要素対応）
- ✅ グローバルCSS編集UI（FormEditIntegratedPage.tsxで実装済み）

## 要件

1. **カスタムテーマ選択時のみ詳細カスタマイズUIを表示**
   - プリセットテーマ（Dark, Light, ReForma, Classic）選択時は非表示
   - 「カスタム」選択時のみ表示

2. **各要素のスタイル設定UI**
   - アコーディオン形式で各要素を展開
   - 各要素に対して`className`と`style`を編集可能

3. **ElementStyleEditorコンポーネント**
   - `className`: テキスト入力（スペース区切りで複数クラス指定可能）
   - `style`: テキストエリア（`property: value;`形式、1行に1つ）

4. **グローバルCSS編集UI**
   - テキストエリアでCSSコードを直接編集可能

5. **リアルタイムプレビュー連携**
   - 編集内容がリアルタイムプレビューに反映される

## タスクリスト

### タスク1: ElementStyleEditorコンポーネントの作成
- **ファイル**: `src/components/forms/ElementStyleEditor.tsx`（新規作成）
- **内容**: 
  - `ElementStyleConfig`を編集するためのコンポーネント
  - `className`入力フィールド（テキスト）
  - `style`入力フィールド（テキストエリア、`property: value;`形式）
  - 入力値を`ElementStyleConfig`形式に変換して`onChange`で通知
- **機能**:
  - `className`: スペース区切りの文字列をそのまま保存
  - `style`: テキストをパースして`Record<string, string>`に変換
    - 形式: `property: value;`（1行に1つ）
    - ケバブケース（`background-color`）をキャメルケース（`backgroundColor`）に変換
  - バリデーション: 基本的な形式チェック
- **UI**:
  - ラベル付き入力フィールド
  - プレースホルダーとヘルプテキスト
  - エラー表示（必要に応じて）

### タスク2: 詳細カスタマイズUIセクションの追加
- **ファイル**: `src/pages/forms/FormEditIntegratedPage.tsx`
- **内容**: 
  - カスタムテーマ選択時のみ表示される詳細カスタマイズUIを追加
  - 「テーマ設定」AccordionItem内に配置
  - プリセットテーマ選択UIの下に配置
- **条件表示**:
  - `selectedPresetTheme === 'custom'`の場合のみ表示
- **UI構造**:
  - アコーディオン形式で各要素を展開
  - 各要素ごとに`ElementStyleEditor`を使用

### タスク3: アコーディオン形式の要素設定UI
- **ファイル**: `src/pages/forms/FormEditIntegratedPage.tsx`
- **内容**: 
  - `Accordion`コンポーネントを使用して各要素を展開可能にする
  - 各要素のタイトルと説明を表示
- **対象要素**（優先度順）:
  1. **container**（コンテナ）
  2. **header**（ヘッダ領域）
  3. **footer**（フッタ領域）
  4. **card**（カード）
  5. **buttonPrimary**（プライマリボタン）
  6. **buttonSecondary**（セカンダリボタン）
  7. **input**（入力フィールド）
  8. **title**（タイトル）
  9. **description**（説明文）
  10. **fieldLabel**（フィールドラベル）
  11. **その他の要素**（必要に応じて）

### タスク4: 各要素のElementStyleEditor統合
- **ファイル**: `src/pages/forms/FormEditIntegratedPage.tsx`
- **内容**: 
  - 各要素の`AccordionItem`内に`ElementStyleEditor`を配置
  - `formCustomStyleConfig.elements[要素名]`を`ElementStyleEditor`に渡す
  - `onChange`で`formCustomStyleConfig`を更新
- **実装例**:
  ```typescript
  <AccordionItem title="コンテナ">
    <ElementStyleEditor
      config={formCustomStyleConfig?.elements?.container}
      onChange={(config) => {
        setFormCustomStyleConfig({
          ...(formCustomStyleConfig || {}),
          elements: {
            ...(formCustomStyleConfig?.elements || {}),
            container: config,
          },
        });
      }}
    />
  </AccordionItem>
  ```

### タスク5: グローバルCSS編集UIの追加
- **ファイル**: `src/pages/forms/FormEditIntegratedPage.tsx`
- **内容**: 
  - グローバルCSSを編集するテキストエリアを追加
  - アコーディオンの最後、または別セクションとして配置
- **UI**:
  - ラベル: "グローバルCSS"
  - テキストエリア（複数行、モノスペースフォント）
  - プレースホルダー: `:root { --custom-var: value; }`
  - ヘルプテキスト: "任意のCSSコードを記述できます"

### タスク6: リアルタイムプレビューとの連携確認
- **ファイル**: `src/components/forms/FormRealtimePreview.tsx`
- **内容**: 
  - `customStyleConfig`が更新された際にリアルタイムプレビューに反映されることを確認
  - 既存の`applyCustomStyleConfig`が正しく動作することを確認
- **確認項目**:
  - `className`の適用
  - `style`の適用
  - グローバルCSSの適用

### タスク7: バリデーションとエラーハンドリング
- **ファイル**: `src/components/forms/ElementStyleEditor.tsx`
- **内容**: 
  - `style`テキストのパースエラー処理
  - 無効な形式の入力に対する警告表示
  - エラー時も可能な限り保存可能にする（部分的な適用）

### タスク8: UI/UXの改善
- **ファイル**: `src/components/forms/ElementStyleEditor.tsx`, `src/pages/forms/FormEditIntegratedPage.tsx`
- **内容**: 
  - プレースホルダーの改善
  - ヘルプテキストの追加
  - 視覚的なフィードバック（保存状態など）
  - リセット機能（要素のスタイルをクリア）

## 実装詳細

### ElementStyleEditorコンポーネントの仕様

```typescript
interface ElementStyleEditorProps {
  config?: ElementStyleConfig | null;
  onChange: (config: ElementStyleConfig | null) => void;
}

// 機能:
// 1. className入力（テキスト）
// 2. style入力（テキストエリア、property: value;形式）
// 3. リセットボタン（オプション）
```

### styleテキストのパース仕様

入力形式:
```
backgroundColor: #ffffff;
color: #333333;
borderRadius: 8px;
```

変換後:
```typescript
{
  backgroundColor: '#ffffff',
  color: '#333333',
  borderRadius: '8px'
}
```

- ケバブケース（`background-color`）→ キャメルケース（`backgroundColor`）
- 末尾のセミコロンは任意
- 空行は無視
- パースエラー時は警告を表示し、可能な限り適用

### 要素の優先順位とグループ化

**基本要素**（最優先）:
- container
- header
- footer
- content

**カード関連**:
- card
- cardBody
- headerCard

**ボタン関連**:
- button
- buttonPrimary
- buttonSecondary

**入力関連**:
- input
- fieldLabel

**テキスト関連**:
- title
- description
- groupName

**その他**:
- stepTab
- stepTabActive
- errorMessage
- confirmationSection
- helpText
- helpTextIcon

## 注意点

1. **パフォーマンス**
   - リアルタイムプレビューへの反映は、デバウンスを検討
   - 大量の要素がある場合のレンダリング最適化

2. **データ整合性**
   - `formCustomStyleConfig`の更新時に、既存の設定を保持
   - `presetTheme`が`'custom'`の場合のみ詳細カスタマイズUIを表示

3. **ユーザビリティ**
   - 各要素の説明を追加（ツールチップなど）
   - よく使うスタイルのプリセット（オプション）
   - プレビュー機能の強化

4. **後方互換性**
   - 既存のプリセットテーマ設定は維持
   - カスタム設定とプリセットテーマの切り替えがスムーズに

## 実装順序の推奨

1. **タスク1**: ElementStyleEditorコンポーネントの作成
2. **タスク2**: 詳細カスタマイズUIセクションの追加（最小限）
3. **タスク3-4**: アコーディオン形式の要素設定UI（主要要素から）
4. **タスク5**: グローバルCSS編集UI
5. **タスク6**: リアルタイムプレビューとの連携確認
6. **タスク7**: バリデーションとエラーハンドリング
7. **タスク8**: UI/UXの改善
