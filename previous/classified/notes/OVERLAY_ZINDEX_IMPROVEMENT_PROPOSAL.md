# オーバーレイのz-indexと位置調整の改善案

## 作成日時
2026-01-20

---

## 現状の問題

### 現在のレイアウト構造
```
┌─────────────────────────────────────────────────────────┐
│ AppLayout                                               │
│ ┌──────────┬──────────────────────────────────────────┐│
│ │          │ Header (sticky top-0 z-10)               ││
│ │ 左サイド  │ ┌────────────────────────────────────┐ ││
│ │ メニュー  │ │ Breadcrumbs + GlobalSettingsPanel  │ ││
│ │ (w-72)   │ └────────────────────────────────────┘ ││
│ │          │                                          ││
│ │          │ FormEditIntegratedPage                   ││
│ │          │ ┌────────────────────────────────────┐ ││
│ │          │ │ フォーム設定オーバーレイ (z-50)      │ ││
│ │          │ │ fixed left-0 top-0                 │ ││
│ │          │ │ → AppLayoutの要素に被る！           │ ││
│ │          │ └────────────────────────────────────┘ ││
│ └──────────┴──────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

### 問題点
1. **フォーム設定オーバーレイ**: `fixed left-0 top-0 z-50`で、AppLayoutの左サイドバー（`sticky top-0`）やヘッダー（`z-10`）に被る
2. **フィールド詳細パネル**: 右側に表示されるが、GlobalSettingsPanelと競合する可能性
3. **z-indexの階層**: オーバーレイ（`z-50`）がAppLayoutの要素（`z-10`）より上にあるため、意図せず被る

---

## 改善案

### 案1: 左サイドバーの開始位置を調整（推奨）

**実装内容**:
- フォーム設定オーバーレイの開始位置を、AppLayoutの左サイドバーの右側から開始
- ヘッダーの下から開始するように調整
- z-indexを適切に設定

**メリット**:
- ✅ AppLayoutの要素と被らない
- ✅ 視覚的に自然
- ✅ 実装が比較的容易

**デメリット**:
- ❌ AppLayoutのサイドバー幅を動的に取得する必要がある
- ❌ レスポンシブ対応が必要

**コード例**:
```tsx
// AppLayoutのサイドバー幅を取得
const sidebarWidth = sidebarCollapsed ? 80 : 288; // w-20 = 80px, w-72 = 288px

// フォーム設定オーバーレイ
{leftSidebarMode === "overlay" && (
  <>
    {/* オーバーレイ背景 */}
    {leftSidebarOpen && (
      <div
        className="fixed inset-0 bg-black/50 z-40 transition-opacity"
        style={{ left: `${sidebarWidth}px` }} // 左サイドバーの右側から開始
        onClick={() => setLeftSidebarOpen(false)}
      />
    )}
    
    {/* サイドバー本体 */}
    <div
      className={`fixed top-0 h-full w-[640px] bg-black/95 border-r border-white/10 z-50 transform transition-transform duration-300 ease-in-out overflow-y-auto ${
        leftSidebarOpen ? 'translate-x-0' : '-translate-x-full'
      }`}
      style={{ left: `${sidebarWidth}px` }} // 左サイドバーの右側から開始
    >
      {/* コンテンツ */}
    </div>
  </>
)}
```

---

### 案2: z-indexの階層を整理

**実装内容**:
- AppLayoutの要素をより高いz-indexに設定
- オーバーレイをAppLayoutの要素より低いz-indexに設定
- ただし、オーバーレイはAppLayoutの要素の上に表示する必要がある

**メリット**:
- ✅ z-indexの階層が明確になる
- ✅ 実装が比較的容易

**デメリット**:
- ❌ AppLayoutの要素が常に上に表示されるため、オーバーレイの目的が達成できない
- ❌ 根本的な解決にならない

**z-index階層案**:
```
z-60: GlobalSettingsPanel（最前面）
z-50: フォーム設定オーバーレイ
z-40: オーバーレイ背景
z-30: フィールド詳細パネル
z-20: AppLayoutヘッダー
z-10: AppLayout左サイドバー
```

---

### 案3: ヘッダーの下から開始

**実装内容**:
- フォーム設定オーバーレイをヘッダーの下から開始
- `top-0`ではなく、ヘッダーの高さ分のマージンを追加

**メリット**:
- ✅ ヘッダーと被らない
- ✅ 実装が容易

**デメリット**:
- ❌ 左サイドバーとは被る可能性がある
- ❌ 完全な解決にならない

**コード例**:
```tsx
<div
  className={`fixed left-0 h-[calc(100vh-64px)] w-[640px] bg-black/95 border-r border-white/10 z-50 transform transition-transform duration-300 ease-in-out overflow-y-auto ${
    leftSidebarOpen ? 'translate-x-0' : '-translate-x-full'
  }`}
  style={{ top: '64px' }} // ヘッダーの高さ分下げる
>
```

---

### 案4: コンテキストに応じたz-index調整（推奨）

**実装内容**:
- AppLayoutの要素のz-indexを確認
- オーバーレイのz-indexを、AppLayoutの要素より高いが、GlobalSettingsPanelより低い値に設定
- 左サイドバーの開始位置を、AppLayoutの左サイドバーの右側から開始

**メリット**:
- ✅ すべての要素と適切に重なり順序を制御
- ✅ 視覚的に自然
- ✅ 完全な解決

**デメリット**:
- ❌ AppLayoutの構造を理解する必要がある
- ❌ 実装がやや複雑

**z-index階層（推奨）**:
```
z-100: GlobalSettingsPanel（最前面、常に表示）
z-60:  フォーム設定オーバーレイ（フォーム編集画面の最前面）
z-50:  オーバーレイ背景
z-40:  フィールド詳細パネル
z-30:  AppLayoutヘッダー（sticky top-0）
z-20:  AppLayout左サイドバー（sticky top-0）
z-10:  通常のコンテンツ
```

**コード例**:
```tsx
// AppLayoutのサイドバー幅を取得（useContextまたはpropsで渡す）
const { sidebarWidth, headerHeight } = useAppLayoutContext();

// フォーム設定オーバーレイ
{leftSidebarMode === "overlay" && (
  <>
    {/* オーバーレイ背景 */}
    {leftSidebarOpen && (
      <div
        className="fixed bg-black/50 z-50 transition-opacity"
        style={{
          left: `${sidebarWidth}px`,
          top: `${headerHeight}px`,
          right: 0,
          bottom: 0,
        }}
        onClick={() => setLeftSidebarOpen(false)}
      />
    )}
    
    {/* サイドバー本体 */}
    <div
      className={`fixed h-[calc(100vh-${headerHeight}px)] w-[640px] bg-black/95 border-r border-white/10 z-60 transform transition-transform duration-300 ease-in-out overflow-y-auto ${
        leftSidebarOpen ? 'translate-x-0' : '-translate-x-full'
      }`}
      style={{
        left: `${sidebarWidth}px`,
        top: `${headerHeight}px`,
      }}
    >
      {/* コンテンツ */}
    </div>
  </>
)}
```

---

### 案5: CSS変数で動的に調整

**実装内容**:
- CSS変数でAppLayoutのサイドバー幅とヘッダー高さを定義
- オーバーレイでその変数を参照

**メリット**:
- ✅ 動的な調整が容易
- ✅ メンテナンスが容易

**デメリット**:
- ❌ CSS変数の管理が必要
- ❌ ブラウザ互換性の考慮が必要

**コード例**:
```css
/* AppLayout.css */
:root {
  --app-sidebar-width: 288px; /* w-72 */
  --app-header-height: 64px;
}

/* FormEditIntegratedPage.css */
.form-overlay {
  left: var(--app-sidebar-width);
  top: var(--app-header-height);
  height: calc(100vh - var(--app-header-height));
}
```

---

## UI/UX比較

| 項目 | 案1（位置調整） | 案2（z-index） | 案3（ヘッダー下） | 案4（コンテキスト） | 案5（CSS変数） |
|------|---------------|---------------|-----------------|------------------|--------------|
| **完全性** | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **実装コスト** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **メンテナンス性** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **レスポンシブ** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 推奨案

### 推奨: 案4（コンテキストに応じたz-index調整）

**理由**:
1. **完全な解決**: すべての要素と適切に重なり順序を制御
2. **視覚的に自然**: AppLayoutの要素と被らない
3. **拡張性**: 将来的に他のオーバーレイを追加する場合も対応可能
4. **明確な階層**: z-indexの階層が明確で、メンテナンスが容易

**実装方針**:
1. AppLayoutのサイドバー幅とヘッダー高さを取得（Context APIまたはprops）
2. オーバーレイの開始位置を、サイドバーの右側、ヘッダーの下から開始
3. z-indexを適切に設定（GlobalSettingsPanel > フォーム設定オーバーレイ > ヘッダー > サイドバー）
4. 右サイドパネル（フィールド詳細）も同様に調整

---

## 実装詳細

### AppLayoutContextの作成

```tsx
// contexts/AppLayoutContext.tsx
import { createContext, useContext } from 'react';

interface AppLayoutContextValue {
  sidebarWidth: number;
  headerHeight: number;
  sidebarCollapsed: boolean;
}

const AppLayoutContext = createContext<AppLayoutContextValue | null>(null);

export function useAppLayoutContext() {
  const context = useContext(AppLayoutContext);
  if (!context) {
    throw new Error('useAppLayoutContext must be used within AppLayoutProvider');
  }
  return context;
}

// AppLayout.tsx
export function AppLayout() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const sidebarWidth = sidebarCollapsed ? 80 : 288; // w-20 = 80px, w-72 = 288px
  const headerHeight = 64; // ヘッダーの高さ（実際の値に合わせて調整）
  
  return (
    <AppLayoutContext.Provider value={{ sidebarWidth, headerHeight, sidebarCollapsed }}>
      {/* 既存のAppLayoutコンテンツ */}
    </AppLayoutContext.Provider>
  );
}
```

### FormEditIntegratedPageでの使用

```tsx
// FormEditIntegratedPage.tsx
import { useAppLayoutContext } from '../../contexts/AppLayoutContext';

export function FormEditIntegratedPage() {
  const { sidebarWidth, headerHeight } = useAppLayoutContext();
  
  // フォーム設定オーバーレイ
  {leftSidebarMode === "overlay" && (
    <>
      {/* オーバーレイ背景 */}
      {leftSidebarOpen && (
        <div
          className="fixed bg-black/50 z-50 transition-opacity"
          style={{
            left: `${sidebarWidth}px`,
            top: `${headerHeight}px`,
            right: 0,
            bottom: 0,
          }}
          onClick={() => setLeftSidebarOpen(false)}
        />
      )}
      
      {/* サイドバー本体 */}
      <div
        className={`fixed w-[640px] bg-black/95 border-r border-white/10 z-60 transform transition-transform duration-300 ease-in-out overflow-y-auto ${
          leftSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
        style={{
          left: `${sidebarWidth}px`,
          top: `${headerHeight}px`,
          height: `calc(100vh - ${headerHeight}px)`,
        }}
      >
        {/* コンテンツ */}
      </div>
    </>
  )}
  
  // 右サイドパネル（フィールド詳細）も同様に調整
  {selectedField && (
    <div
      className="fixed w-80 border-l border-white/10 bg-black/10 z-40"
      style={{
        right: 0,
        top: `${headerHeight}px`,
        height: `calc(100vh - ${headerHeight}px)`,
      }}
    >
      <FieldDetailPanel {...fieldDetailProps} />
    </div>
  )}
}
```

---

## まとめ

### 推奨実装
- **案4（コンテキストに応じたz-index調整）**を採用
- AppLayoutContextでサイドバー幅とヘッダー高さを提供
- オーバーレイの開始位置を動的に調整
- z-indexの階層を明確に定義

### 実装優先順位
1. ✅ **最優先**: AppLayoutContextの作成
2. ✅ **次**: フォーム設定オーバーレイの位置調整
3. ✅ **次**: フィールド詳細パネルの位置調整
4. ⚠️ **将来**: レスポンシブ対応の強化

### 期待される効果
- AppLayoutの要素と被らない
- 視覚的に自然なUI
- メンテナンスが容易な構造

---

## 参考資料

- CSS z-index stacking context
- Material Design: Navigation Drawer
- React Context API
- Tailwind CSS: Fixed positioning
