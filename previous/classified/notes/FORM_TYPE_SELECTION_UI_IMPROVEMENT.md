# フォームタイプ選択UIの改善案

## 作成日時
2026-01-20

---

## 現状の問題

### 現在の実装
- **位置**: `FormStructureEditor`コンポーネント内（196-223行目）
- **サイズ**: `rounded-xl border border-white/10 bg-black/20 p-4 mb-4`
- **レイアウト**: 中央揃え、縦方向にスペースを取る
- **問題点**: 
  - 画面の領域を大きく消費している
  - 一度選択すると、この大きなUIは不要になる
  - フォーム構造編集エリアが下に押し下げられる

---

## 改善案

### 案1: コンパクトなインライン表示（推奨）

**実装内容**:
- ラベルとボタンを横並びにする
- パディングとマージンを削減
- フォントサイズを小さくする
- 選択済みの場合は、さらにコンパクトに表示

**メリット**:
- ✅ 画面領域の消費を大幅に削減
- ✅ 一度選択すると小さく表示される
- ✅ 変更も容易（クリックで切り替え可能）

**デメリット**:
- ❌ 初期選択時の視認性がやや低下する可能性

**コード例**:
```tsx
{/* フォームタイプ選択UI - コンパクト版 */}
{formType === null ? (
  // 未選択時: 少し大きめに表示
  <div className="rounded-lg border border-white/10 bg-black/20 p-3 mb-3">
    <div className="flex items-center justify-between">
      <span className="text-xs font-bold">
        {t("form_item_select_type") || "フォームタイプを選択してください"}
      </span>
      <div className="flex gap-2">
        <button
          type="button"
          className={`rounded-lg px-3 py-1 text-xs font-bold border ${
            formType === "step" ? uiTokens.buttonPrimary : uiTokens.buttonSecondary
          }`}
          onClick={() => handleFormTypeChange("step")}
        >
          {t("form_item_step_form") || "STEP式"}
        </button>
        <button
          type="button"
          className={`rounded-lg px-3 py-1 text-xs font-bold border ${
            formType === "single" ? uiTokens.buttonPrimary : uiTokens.buttonSecondary
          }`}
          onClick={() => handleFormTypeChange("single")}
        >
          {t("form_item_single_form") || "単一式"}
        </button>
      </div>
    </div>
  </div>
) : (
  // 選択済み時: 小さなバッジ形式
  <div className="flex items-center gap-2 mb-3">
    <span className="text-xs text-white/60">フォームタイプ:</span>
    <button
      type="button"
      className={`rounded-lg px-2 py-1 text-xs font-bold border ${uiTokens.buttonPrimary}`}
      onClick={() => {
        // 変更確認ダイアログを表示
        const newType = formType === "step" ? "single" : "step";
        handleFormTypeChange(newType);
      }}
      title="クリックで変更"
    >
      {formType === "step" 
        ? (t("form_item_step_form") || "STEP式")
        : (t("form_item_single_form") || "単一式")}
    </button>
  </div>
)}
```

---

### 案2: ドロップダウンメニュー

**実装内容**:
- セレクトボックス形式で表示
- 選択済みの場合は、小さなラベルとドロップダウンアイコンを表示

**メリット**:
- ✅ 画面領域の消費が最小
- ✅ 選択肢が明確

**デメリット**:
- ❌ ネイティブセレクトボックスはスタイリングが難しい
- ❌ カスタムドロップダウンは実装コストが高い

**コード例**:
```tsx
{/* フォームタイプ選択UI - ドロップダウン版 */}
<div className="flex items-center gap-2 mb-3">
  <label className="text-xs text-white/60">
    {t("form_item_select_type") || "フォームタイプ:"}
  </label>
  <select
    value={formType || ""}
    onChange={(e) => {
      const newType = e.target.value as "step" | "single";
      if (newType) {
        handleFormTypeChange(newType);
      }
    }}
    className="rounded-lg px-2 py-1 text-xs font-bold border border-white/10 bg-black/20 text-white"
  >
    <option value="">選択してください</option>
    <option value="step">{t("form_item_step_form") || "STEP式フォーム"}</option>
    <option value="single">{t("form_item_single_form") || "単一式フォーム"}</option>
  </select>
</div>
```

---

### 案3: ヘッダーに統合

**実装内容**:
- メインエリアのヘッダー部分（ScreenHeader）に統合
- 右側に小さなバッジとして表示

**メリット**:
- ✅ 画面領域を全く消費しない
- ✅ 常に見える位置に配置

**デメリット**:
- ❌ ヘッダーの実装を変更する必要がある
- ❌ 他のヘッダー要素とのバランスを考慮する必要がある

**コード例**:
```tsx
// FormEditIntegratedPage.tsx の ScreenHeader に追加
<ScreenHeader
  title={...}
  actions={
    <>
      {/* フォームタイプ選択 */}
      <div className="flex items-center gap-2">
        <span className="text-xs text-white/60">タイプ:</span>
        <button
          type="button"
          className={`rounded-lg px-2 py-1 text-xs font-bold border ${uiTokens.buttonPrimary}`}
          onClick={() => {
            const newType = formType === "step" ? "single" : "step";
            handleFormTypeChange(newType);
          }}
        >
          {formType === "step" ? "STEP式" : "単一式"}
        </button>
      </div>
      {/* 保存ボタンなど */}
    </>
  }
/>
```

---

### 案4: トグルスイッチ形式

**実装内容**:
- トグルスイッチ（iOS風）で表示
- コンパクトで視覚的に分かりやすい

**メリット**:
- ✅ モダンなUI
- ✅ コンパクト
- ✅ 視覚的に分かりやすい

**デメリット**:
- ❌ カスタムコンポーネントの実装が必要
- ❌ 3つの状態（未選択、STEP式、単一式）を表現するのが難しい

---

## UI/UX比較

| 項目 | 案1（インライン） | 案2（ドロップダウン） | 案3（ヘッダー統合） | 案4（トグル） |
|------|------------------|---------------------|-------------------|--------------|
| **画面領域消費** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **視認性** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **操作性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **実装コスト** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| **変更の容易さ** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

---

## 推奨案

### 推奨: 案1（コンパクトなインライン表示）

**理由**:
1. **画面領域の大幅削減**: 未選択時でも現在の1/3程度の領域で済む
2. **選択済み時の最適化**: 選択済みの場合は、さらに小さなバッジ形式で表示
3. **実装が容易**: 既存のコードを最小限の変更で改善可能
4. **操作性**: クリックで簡単に変更可能

**実装方針**:
- 未選択時: コンパクトな横並びレイアウト（現在の約1/3の高さ）
- 選択済み時: 小さなバッジ形式（1行、約20pxの高さ）
- 変更時: クリックで確認ダイアログを表示してから変更

---

## 実装詳細

### 改善後のコード構造

```tsx
{/* フォームタイプ選択UI - 改善版 */}
{formType === null ? (
  // 未選択時: コンパクトな選択UI
  <div className="rounded-lg border border-white/10 bg-black/20 p-2.5 mb-3">
    <div className="flex items-center justify-between gap-3">
      <span className="text-xs font-bold text-white/90">
        {t("form_item_select_type") || "フォームタイプを選択してください"}
      </span>
      <div className="flex gap-2">
        <button
          type="button"
          className={`rounded-lg px-3 py-1.5 text-xs font-bold border transition-all ${
            formType === "step" 
              ? `${uiTokens.buttonPrimary} border-current` 
              : `${uiTokens.buttonSecondary} hover:bg-white/10`
          }`}
          onClick={() => handleFormTypeChange("step")}
        >
          {t("form_item_step_form") || "STEP式"}
        </button>
        <button
          type="button"
          className={`rounded-lg px-3 py-1.5 text-xs font-bold border transition-all ${
            formType === "single" 
              ? `${uiTokens.buttonPrimary} border-current` 
              : `${uiTokens.buttonSecondary} hover:bg-white/10`
          }`}
          onClick={() => handleFormTypeChange("single")}
        >
          {t("form_item_single_form") || "単一式"}
        </button>
      </div>
    </div>
  </div>
) : (
  // 選択済み時: 小さなバッジ形式
  <div className="flex items-center gap-2 mb-3">
    <span className="text-xs text-white/60">
      {t("form_item_type") || "フォームタイプ"}:
    </span>
    <button
      type="button"
      className={`rounded-lg px-2.5 py-1 text-xs font-bold border transition-all ${uiTokens.buttonPrimary} hover:opacity-80`}
      onClick={() => {
        const newType = formType === "step" ? "single" : "step";
        handleFormTypeChange(newType);
      }}
      title={t("form_item_change_type") || "クリックでフォームタイプを変更"}
    >
      {formType === "step" 
        ? (t("form_item_step_form") || "STEP式フォーム")
        : (t("form_item_single_form") || "単一式フォーム")}
    </button>
  </div>
)}
```

### サイズ比較

| 状態 | 現在の高さ | 改善後の高さ | 削減率 |
|------|-----------|------------|--------|
| 未選択時 | ~80px | ~40px | 50% |
| 選択済み時 | ~80px | ~24px | 70% |

---

## まとめ

### 推奨実装
- **案1（コンパクトなインライン表示）**を採用
- 未選択時と選択済み時で表示を切り替え
- 画面領域の消費を50-70%削減

### 実装優先順位
1. ✅ **最優先**: 案1の実装（コンパクトなインライン表示）
2. ⚠️ **将来**: 案3の検討（ヘッダー統合、より高度な改善）

### 期待される効果
- 画面領域の消費を大幅に削減
- フォーム構造編集エリアがより見やすくなる
- 選択済み時の不要な領域を削減

---

## 参考資料

- Material Design: Selection Controls
- Ant Design: Radio Component
- Chakra UI: Radio Group Component
