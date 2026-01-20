# フォーム統合画面の左サイドバー閉じる時の問題と調整案

## 作成日時
2026-01-20

---

## 問題

フォーム統合画面（FormEditIntegratedPage）の左サイドメニューを閉じる時に、AppLayout左サイドバー分の幅で残ってしまう問題が発生しています。

### 現状の実装

#### 固定方式（fixed）
```tsx
{leftSidebarMode === "fixed" && (
  <div className={`${leftSidebarOpen ? 'w-[640px]' : 'w-0'} transition-all ${leftSidebarOpen ? 'border-r border-white/10' : ''} overflow-hidden`}>
    {/* コンテンツ */}
  </div>
)}
```

**問題点**:
- `w-0`にしても、要素自体がDOMに存在し、何らかの形でスペースを取っている可能性がある
- `overflow-hidden`だけでは完全に非表示にならない場合がある

#### オーバーレイ方式（overlay）
```tsx
{leftSidebarMode === "overlay" && (
  <>
    {/* サイドバー本体 */}
    <div
      className={`fixed w-[640px] bg-black/95 border-r border-white/10 z-[60] transform transition-transform duration-300 ease-in-out overflow-y-auto ${
        leftSidebarOpen ? 'translate-x-0' : '-translate-x-full'
      }`}
      style={{
        left: `${sidebarWidth}px`, // AppLayoutのサイドバー幅
        top: `${headerHeight}px`,
        height: `calc(100vh - ${headerHeight}px)`,
      }}
    >
      {/* コンテンツ */}
    </div>
  </>
)}
```

**問題点**:
- `-translate-x-full`で非表示にしても、`left: ${sidebarWidth}px`が設定されているため、AppLayoutのサイドバー幅分のスペースが残る可能性がある
- 閉じた時に完全に非表示にする必要がある

---

## 調整案

### 案1: 条件付きレンダリング（推奨）

**実装内容**:
- 固定方式の場合、閉じた時は要素を完全にDOMから削除する
- オーバーレイ方式の場合、閉じた時は要素を完全にDOMから削除する

**メリット**:
- ✅ 完全に非表示になる
- ✅ DOMから削除されるため、パフォーマンスが良い
- ✅ スペースが残らない

**デメリット**:
- ❌ アニメーションが失われる（条件付きレンダリングの場合）
- ❌ アニメーションを維持する場合は、別の方法が必要

**コード例（固定方式）**:
```tsx
{leftSidebarMode === "fixed" && leftSidebarOpen && (
  <div className="w-[640px] transition-all border-r border-white/10 overflow-hidden">
    {/* コンテンツ */}
  </div>
)}
```

**コード例（オーバーレイ方式）**:
```tsx
{leftSidebarMode === "overlay" && leftSidebarOpen && (
  <>
    {/* オーバーレイ背景 */}
    <div
      className="fixed bg-black/50 z-[50] transition-opacity"
      style={{
        left: `${sidebarWidth}px`,
        top: `${headerHeight}px`,
        right: 0,
        bottom: 0,
      }}
      onClick={() => setLeftSidebarOpen(false)}
    />
    
    {/* サイドバー本体 */}
    <div
      className="fixed w-[640px] bg-black/95 border-r border-white/10 z-[60] transform transition-transform duration-300 ease-in-out overflow-y-auto"
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
```

---

### 案2: display: none を使用

**実装内容**:
- 閉じた時に`display: none`を適用する
- アニメーションを維持する場合は、アニメーション後に`display: none`を適用

**メリット**:
- ✅ アニメーションを維持できる（条件付きで適用する場合）
- ✅ DOMから削除されないため、状態管理が容易

**デメリット**:
- ❌ アニメーション中は要素が存在するため、スペースが残る可能性がある
- ❌ アニメーション後に`display: none`を適用する必要がある

**コード例（固定方式）**:
```tsx
{leftSidebarMode === "fixed" && (
  <div 
    className={`transition-all ${leftSidebarOpen ? 'w-[640px] border-r border-white/10' : 'w-0'} overflow-hidden ${
      !leftSidebarOpen ? 'hidden' : ''
    }`}
  >
    {/* コンテンツ */}
  </div>
)}
```

---

### 案3: アニメーション後に条件付きレンダリング

**実装内容**:
- アニメーション中は要素を表示
- アニメーション完了後に要素をDOMから削除
- `onTransitionEnd`イベントを使用

**メリット**:
- ✅ アニメーションを維持できる
- ✅ アニメーション後に完全に非表示になる

**デメリット**:
- ❌ 実装がやや複雑
- ❌ アニメーション時間を管理する必要がある

**コード例（固定方式）**:
```tsx
const [shouldRender, setShouldRender] = useState(leftSidebarOpen);

useEffect(() => {
  if (leftSidebarOpen) {
    setShouldRender(true);
  } else {
    // アニメーション完了後に非表示
    const timer = setTimeout(() => {
      setShouldRender(false);
    }, 300); // transition duration
    return () => clearTimeout(timer);
  }
}, [leftSidebarOpen]);

{leftSidebarMode === "fixed" && shouldRender && (
  <div 
    className={`transition-all ${leftSidebarOpen ? 'w-[640px] border-r border-white/10' : 'w-0'} overflow-hidden`}
    onTransitionEnd={() => {
      if (!leftSidebarOpen) {
        setShouldRender(false);
      }
    }}
  >
    {/* コンテンツ */}
  </div>
)}
```

---

## 推奨実装

### 推奨: 案1（条件付きレンダリング）

**理由**:
1. **シンプル**: 実装が最も簡単
2. **確実**: 完全に非表示になる
3. **パフォーマンス**: DOMから削除されるため、パフォーマンスが良い
4. **オーバーレイ方式に適している**: オーバーレイ方式はアニメーションが重要なので、条件付きレンダリングで十分

**実装方針**:
- 固定方式: `leftSidebarOpen`が`true`の時のみレンダリング
- オーバーレイ方式: `leftSidebarOpen`が`true`の時のみレンダリング
- アニメーションが必要な場合は、案3を検討

---

## 実装詳細

### 固定方式の修正

```tsx
{/* 左サイドバー - 固定方式 */}
{leftSidebarMode === "fixed" && leftSidebarOpen && (
  <div className="w-[640px] transition-all border-r border-white/10 overflow-hidden">
    {/* 閉じた時のトグルボタンは親要素に移動 */}
    {/* コンテンツ */}
  </div>
)}
```

### オーバーレイ方式の修正

```tsx
{/* 左サイドバー - オーバーレイ方式 */}
{leftSidebarMode === "overlay" && leftSidebarOpen && (
  <>
    {/* オーバーレイ背景 */}
    <div
      className="fixed bg-black/50 z-[50] transition-opacity"
      style={{
        left: `${sidebarWidth}px`,
        top: `${headerHeight}px`,
        right: 0,
        bottom: 0,
      }}
      onClick={() => setLeftSidebarOpen(false)}
    />
    
    {/* サイドバー本体 */}
    <div
      className="fixed w-[640px] bg-black/95 border-r border-white/10 z-[60] transform transition-transform duration-300 ease-in-out overflow-y-auto"
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
```

### 閉じた時のトグルボタンの配置

閉じた時のトグルボタンは、親要素（`<div className="flex h-screen overflow-hidden relative p-4">`）に配置する必要があります。

```tsx
{/* 閉じた時のトグルボタン（固定方式） */}
{leftSidebarMode === "fixed" && !leftSidebarOpen && (
  <button
    type="button"
    onClick={() => setLeftSidebarOpen(true)}
    className="absolute left-4 top-4 z-10 p-2 bg-black/80 border border-white/10 rounded-r-lg hover:bg-black/90 transition-all"
    title="サイドバーを開く"
  >
    <span className="text-xl">→</span>
  </button>
)}

{/* 閉じた時のトグルボタン（オーバーレイ方式） */}
{leftSidebarMode === "overlay" && !leftSidebarOpen && (
  <button
    type="button"
    onClick={() => setLeftSidebarOpen(true)}
    className="fixed z-30 p-2 bg-black/80 border border-white/10 rounded-lg hover:bg-black/90 transition-all shadow-lg"
    style={{
      left: `${sidebarWidth + 16}px`,
      top: `${headerHeight + 16}px`,
    }}
    title="サイドバーを開く"
  >
    <span className="text-xl">☰</span>
  </button>
)}
```

---

## まとめ

### 推奨実装
- **案1（条件付きレンダリング）**を採用
- 固定方式・オーバーレイ方式ともに、`leftSidebarOpen`が`true`の時のみレンダリング
- 閉じた時のトグルボタンは親要素に配置

### 期待される効果
- 左サイドバーを閉じた時に、AppLayout左サイドバー分の幅が残らない
- 完全に非表示になる
- パフォーマンスが向上する

---

## 参考資料

- FormEditIntegratedPage.tsx
- AppLayout.tsx
- OVERLAY_ZINDEX_IMPROVEMENT_PROPOSAL.md
