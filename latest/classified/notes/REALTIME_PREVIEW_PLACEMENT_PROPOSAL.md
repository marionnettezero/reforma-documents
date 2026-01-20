# リアルタイムプレビューの表示場所提案

## 作成日時
2026-01-20

---

## 現状のレイアウト構造

### 現在の3カラムレイアウト
```
┌─────────────┬──────────────────────┬──────────────┐
│             │                      │              │
│  左サイドバー  │    メインエリア        │  右サイドパネル │
│  (640px)    │   (flex-1)          │  (条件付き)   │
│             │                      │              │
│ ・基本情報    │ ・フォーム構造編集      │ ・フィールド詳細 │
│ ・通知設定    │ ・FormStructureEditor │ ・FieldDetailPanel│
│ ・テーマ設定  │                      │  (selectedField)│
│             │                      │              │
└─────────────┴──────────────────────┴──────────────┘
```

### 特徴
- **左サイドバー**: 固定幅640px、オーバーレイ方式（デフォルト）
- **メインエリア**: フォーム構造編集（STEP/GROUP/項目の階層構造）
- **右サイドパネル**: フィールド詳細編集（`selectedField`がある時のみ表示）

---

## リアルタイムプレビューの表示場所案

### 案1: 右サイドパネルとタブ切り替え（推奨）

**実装内容**:
- 右サイドパネルにタブを追加
- 「フィールド詳細」と「プレビュー」を切り替え可能
- フィールド編集時は「フィールド詳細」、それ以外は「プレビュー」を表示

**メリット**:
- ✅ 既存のレイアウト構造を維持
- ✅ 画面領域を追加で消費しない
- ✅ フィールド編集とプレビューを同じ場所で切り替え可能
- ✅ 実装が容易（既存の右サイドパネルを拡張）

**デメリット**:
- ❌ フィールド編集とプレビューを同時に見られない
- ❌ タブ切り替えが必要

**レイアウト**:
```
┌─────────────┬──────────────────────┬──────────────┐
│  左サイドバー  │    メインエリア        │  [フィールド詳細] │
│             │                      │  [プレビュー]  │
│             │                      │              │
│             │                      │  ┌──────────┐│
│             │                      │  │ プレビュー ││
│             │                      │  │ コンテンツ ││
│             │                      │  │          ││
│             │                      │  └──────────┘│
└─────────────┴──────────────────────┴──────────────┘
```

**コード例**:
```tsx
{/* 右サイドパネル（フィールド詳細 / プレビュー） */}
<div className="w-80 border-l border-white/10 bg-black/10">
  <div className="flex border-b border-white/10">
    <button
      type="button"
      className={`flex-1 px-4 py-2 text-sm font-bold ${
        rightPanelMode === "field" 
          ? `${uiTokens.buttonPrimary} border-b-2 border-current` 
          : `${uiTokens.buttonSecondary}`
      }`}
      onClick={() => setRightPanelMode("field")}
    >
      フィールド詳細
    </button>
    <button
      type="button"
      className={`flex-1 px-4 py-2 text-sm font-bold ${
        rightPanelMode === "preview" 
          ? `${uiTokens.buttonPrimary} border-b-2 border-current` 
          : `${uiTokens.buttonSecondary}`
      }`}
      onClick={() => setRightPanelMode("preview")}
    >
      プレビュー
    </button>
  </div>
  
  {rightPanelMode === "field" && selectedField && (
    <FieldDetailPanel {...fieldDetailProps} />
  )}
  
  {rightPanelMode === "preview" && (
    <FormPreviewPanel
      form={form}
      steps={steps}
      fields={structureFields}
      translations={translations}
      theme={selectedTheme}
    />
  )}
</div>
```

---

### 案2: メインエリアと分割表示（上下分割）

**実装内容**:
- メインエリアを上下に分割
- 上部: フォーム構造編集
- 下部: リアルタイムプレビュー
- 分割線をドラッグして高さを調整可能

**メリット**:
- ✅ 編集とプレビューを同時に確認可能
- ✅ リアルタイムで変更を確認できる
- ✅ 視覚的に分かりやすい

**デメリット**:
- ❌ 各エリアの高さが制限される
- ❌ スクロールが増える可能性
- ❌ 実装がやや複雑（リサイザー機能が必要）

**レイアウト**:
```
┌─────────────┬──────────────────────┬──────────────┐
│  左サイドバー  │  ┌──────────────────┐│  右サイドパネル │
│             │  │ フォーム構造編集    ││              │
│             │  ├──────────────────┤│              │
│             │  │ リアルタイムプレビュー││              │
│             │  └──────────────────┘│              │
└─────────────┴──────────────────────┴──────────────┘
```

---

### 案3: メインエリアと分割表示（左右分割）

**実装内容**:
- メインエリアを左右に分割
- 左側: フォーム構造編集
- 右側: リアルタイムプレビュー
- 分割線をドラッグして幅を調整可能

**メリット**:
- ✅ 編集とプレビューを同時に確認可能
- ✅ 横方向のスペースを有効活用
- ✅ 大画面で効果的

**デメリット**:
- ❌ 各エリアの幅が制限される
- ❌ 小画面では使いにくい
- ❌ 実装がやや複雑（リサイザー機能が必要）

**レイアウト**:
```
┌─────────────┬──────────────┬──────────────┬──────────────┐
│  左サイドバー  │ フォーム構造編集 │ リアルタイムプレビュー│  右サイドパネル │
│             │              │              │              │
│             │              │              │              │
└─────────────┴──────────────┴──────────────┴──────────────┘
```

---

### 案4: フローティングプレビューパネル

**実装内容**:
- プレビューをフローティングパネルとして表示
- 画面右下に固定位置で表示
- ドラッグで移動可能、リサイズ可能
- 最小化/最大化ボタン

**メリット**:
- ✅ 既存レイアウトに影響しない
- ✅ ユーザーが自由に配置可能
- ✅ 必要に応じて非表示にできる

**デメリット**:
- ❌ 他のUI要素と重なる可能性
- ❌ 実装が複雑（ドラッグ&ドロップ、リサイズ機能）
- ❌ モバイルでは使いにくい

**レイアウト**:
```
┌─────────────┬──────────────────────┬──────────────┐
│  左サイドバー  │    メインエリア        │  右サイドパネル │
│             │                      │              │
│             │                      │              │
│             │              ┌──────┐│              │
│             │              │プレビュー││              │
│             │              └──────┘│              │
└─────────────┴──────────────────────┴──────────────┘
```

---

### 案5: 別タブ/ウィンドウ

**実装内容**:
- プレビューを別タブまたは別ウィンドウで開く
- メインエリアのヘッダーに「プレビューを開く」ボタンを追加
- 新しいタブ/ウィンドウでリアルタイムプレビューを表示

**メリット**:
- ✅ 既存レイアウトに全く影響しない
- ✅ 大画面で効果的（2画面並べて使用）
- ✅ 実装が比較的容易

**デメリット**:
- ❌ タブ/ウィンドウの切り替えが必要
- ❌ モバイルでは使いにくい
- ❌ リアルタイム性がやや低下（タブ切り替えが必要）

**レイアウト**:
```
┌─────────────┬──────────────────────┬──────────────┐
│  左サイドバー  │    メインエリア        │  右サイドパネル │
│             │  [プレビューを開く]    │              │
│             │                      │              │
└─────────────┴──────────────────────┴──────────────┘
         ↓ クリック
┌─────────────────────────────────────────────┐
│  別タブ/ウィンドウ: リアルタイムプレビュー      │
│                                              │
│  [フォームプレビューコンテンツ]                │
│                                              │
└─────────────────────────────────────────────┘
```

---

## UI/UX比較

| 項目 | 案1（タブ切り替え） | 案2（上下分割） | 案3（左右分割） | 案4（フローティング） | 案5（別タブ） |
|------|------------------|--------------|--------------|------------------|------------|
| **画面領域消費** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **同時確認** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **実装コスト** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **操作性** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **モバイル対応** | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ |
| **リアルタイム性** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 推奨案

### 推奨: 案1（右サイドパネルとタブ切り替え）

**理由**:
1. **既存レイアウトの維持**: 3カラムレイアウトを維持し、既存のUIに影響が少ない
2. **実装が容易**: 既存の右サイドパネルを拡張するだけ
3. **画面領域の効率**: 追加の画面領域を消費しない
4. **ユーザビリティ**: フィールド編集とプレビューを同じ場所で切り替え可能
5. **段階的実装**: まずはタブ切り替えで実装し、将来的に案2や案3に拡張可能

**実装方針**:
- 右サイドパネルにタブを追加（「フィールド詳細」「プレビュー」）
- デフォルトは「プレビュー」を表示
- フィールドを選択した時は自動的に「フィールド詳細」に切り替え（オプション）
- プレビューはリアルタイムで更新（フォーム構造、フィールド、翻訳、テーマの変更を反映）

**将来の拡張**:
- 案2（上下分割）や案3（左右分割）への移行も検討可能
- ユーザー設定で表示方法を選択可能にする

---

## 実装詳細

### 案1の実装構造

```tsx
// FormEditIntegratedPage.tsx

const [rightPanelMode, setRightPanelMode] = useState<"field" | "preview">("preview");

// フィールド選択時に自動的に「フィールド詳細」に切り替え（オプション）
useEffect(() => {
  if (selectedField) {
    setRightPanelMode("field");
  }
}, [selectedField]);

// レンダリング
{/* 右サイドパネル（フィールド詳細 / プレビュー） */}
<div className="w-80 border-l border-white/10 bg-black/10 flex flex-col">
  {/* タブ */}
  <div className="flex border-b border-white/10">
    <button
      type="button"
      className={`flex-1 px-4 py-2 text-sm font-bold transition-all ${
        rightPanelMode === "field" 
          ? `${uiTokens.buttonPrimary} border-b-2 border-current` 
          : `${uiTokens.buttonSecondary} hover:bg-white/5`
      }`}
      onClick={() => setRightPanelMode("field")}
      disabled={!selectedField}
    >
      {t("field_detail") || "フィールド詳細"}
    </button>
    <button
      type="button"
      className={`flex-1 px-4 py-2 text-sm font-bold transition-all ${
        rightPanelMode === "preview" 
          ? `${uiTokens.buttonPrimary} border-b-2 border-current` 
          : `${uiTokens.buttonSecondary} hover:bg-white/5`
      }`}
      onClick={() => setRightPanelMode("preview")}
    >
      {t("preview") || "プレビュー"}
    </button>
  </div>
  
  {/* コンテンツ */}
  <div className="flex-1 overflow-y-auto">
    {rightPanelMode === "field" && selectedField && (
      <FieldDetailPanel {...fieldDetailProps} />
    )}
    
    {rightPanelMode === "preview" && (
      <FormPreviewPanel
        form={form}
        steps={steps}
        fields={structureFields}
        translations={translations}
        theme={selectedTheme}
        locale={locale}
      />
    )}
  </div>
</div>
```

### FormPreviewPanelコンポーネント

```tsx
// components/forms/FormPreviewPanel.tsx

interface FormPreviewPanelProps {
  form: FormData;
  steps: StructureStep[];
  fields: StructureFormField[];
  translations: Record<string, Record<string, string>>;
  theme: ThemeData;
  locale: string;
}

export function FormPreviewPanel({
  form,
  steps,
  fields,
  translations,
  theme,
  locale,
}: FormPreviewPanelProps) {
  // フォーム構造をプレビュー用に変換
  const previewData = useMemo(() => {
    return buildPreviewData(steps, fields, translations, locale);
  }, [steps, fields, translations, locale]);
  
  return (
    <div className="p-4 space-y-4">
      <div className="text-xs text-white/60 mb-2">
        {t("realtime_preview") || "リアルタイムプレビュー"}
      </div>
      
      {/* プレビューコンテンツ */}
      <div className="bg-white rounded-lg p-4 text-black">
        {/* フォームプレビューをレンダリング */}
        <FormRenderer
          form={previewData}
          theme={theme}
          locale={locale}
        />
      </div>
    </div>
  );
}
```

---

## まとめ

### 推奨実装
- **案1（右サイドパネルとタブ切り替え）**を採用
- 既存のレイアウト構造を維持
- 実装が容易で、段階的に拡張可能

### 実装優先順位
1. ✅ **最優先**: 案1の実装（右サイドパネルにタブ追加）
2. ⚠️ **将来**: 案2や案3の検討（分割表示、より高度な機能）

### 期待される効果
- リアルタイムでフォームの見た目を確認可能
- 既存のUIに影響を与えずに実装可能
- ユーザビリティの向上

---

## 参考資料

- Material Design: Tabs
- Ant Design: Tabs Component
- Chakra UI: Tabs Component
- FormPreviewPage.tsx（既存のプレビューページ実装）
