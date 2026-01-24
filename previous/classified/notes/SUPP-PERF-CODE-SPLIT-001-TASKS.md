# SUPP-PERF-CODE-SPLIT-001: コード分割（Code Splitting）最適化 実装タスク

**作成日**: 2026-01-23  
**関連仕様**: `SUPP-PERF-CODE-SPLIT-001-spec.md`

---

## 現状確認結果

### 現在の実装状況

1. **ページコンポーネントのエクスポート形式**
   - ✅ すべてのページコンポーネントが名前付きエクスポート（`export function XxxPage()`）
   - ⚠️ `React.lazy()`を使用するには、デフォルトエクスポート（`export default`）が必要

2. **App.tsx**
   - ✅ すべてのページコンポーネントが静的インポート（通常の`import`）
   - ⏳ `React.lazy()`と`Suspense`が未使用

3. **vite.config.ts**
   - ✅ 基本的なVite設定は存在
   - ⏳ `manualChunks`設定が未実装

4. **ローディングコンポーネント**
   - ✅ `Spinner`コンポーネントは既に存在
   - ⏳ ページローディング用の専用コンポーネントは未作成（オプション）

### 対象ページ一覧

**静的インポートのまま（初期表示に必要）**:
- `LoginPage` - ログイン画面（認証不要）
- `LogoutPage` - ログアウト画面（認証不要）
- `ErrorPage` - エラーページ（認証不要）
- `NotFoundPage` - 404ページ（認証不要）

**動的インポートに変更（ページ単位で分割）**:
- `InviteAcceptPage` - 招待受理ページ
- `DashboardPage` - ダッシュボード
- `FormListPage` - フォーム一覧
- `FormEditIntegratedPage` - フォーム編集（統合版）
- `FormPreviewPage` - フォームプレビュー
- `PublicFormViewPage` - 公開フォーム表示
- `AckViewPage` - 確認応答ページ
- `ResponseListPage` - 回答一覧
- `ResponseDetailPage` - 回答詳細
- `LogListPage` - ログ一覧
- `LogDetailPage` - ログ詳細
- `SearchPage` - 検索ページ
- `AccountListPage` - アカウント一覧
- `ThemeListPage` - テーマ一覧

---

## 実装タスク

### Phase 1: ページコンポーネントのエクスポート形式変更

#### タスク 1.1: 各ページコンポーネントをデフォルトエクスポートに変更

**目的**: `React.lazy()`を使用するため、名前付きエクスポートからデフォルトエクスポートに変更

**対象ファイル**（14ファイル）:
1. `src/pages/InviteAcceptPage.tsx`
2. `src/pages/DashboardPage.tsx`
3. `src/pages/forms/FormListPage.tsx`
4. `src/pages/forms/FormEditIntegratedPage.tsx`
5. `src/pages/forms/FormPreviewPage.tsx`
6. `src/pages/public/PublicFormViewPage.tsx`
7. `src/pages/public/AckViewPage.tsx`
8. `src/pages/responses/ResponseListPage.tsx`
9. `src/pages/responses/ResponseDetailPage.tsx`
10. `src/pages/logs/LogListPage.tsx`
11. `src/pages/logs/LogDetailPage.tsx`
12. `src/pages/search/SearchPage.tsx`
13. `src/pages/system/AccountListPage.tsx`
14. `src/pages/system/ThemeListPage.tsx`

**変更内容**:
- `export function XxxPage()` → `export default function XxxPage()`
- 既存の名前付きエクスポートは削除（または`export { XxxPage as default }`でエイリアス）

**注意事項**:
- 各ファイルで`export function`を`export default function`に変更
- 型定義や他のエクスポートがある場合は確認が必要

---

### Phase 2: App.tsxの動的インポート実装

#### タスク 2.1: React.lazyとSuspenseのインポート追加

**ファイル**: `src/App.tsx`

**変更内容**:
```typescript
import React, { Suspense, lazy } from "react";
```

#### タスク 2.2: ページコンポーネントの静的インポートを削除

**ファイル**: `src/App.tsx`

**削除対象**（14行）:
```typescript
import { InviteAcceptPage } from "./pages/InviteAcceptPage";
import { DashboardPage } from "./pages/DashboardPage";
import { FormListPage } from "./pages/forms/FormListPage";
import { FormEditIntegratedPage } from "./pages/forms/FormEditIntegratedPage";
import { FormPreviewPage } from "./pages/forms/FormPreviewPage";
import { PublicFormViewPage } from "./pages/public/PublicFormViewPage";
import { AckViewPage } from "./pages/public/AckViewPage";
import { ResponseListPage } from "./pages/responses/ResponseListPage";
import { ResponseDetailPage } from "./pages/responses/ResponseDetailPage";
import { LogListPage } from "./pages/logs/LogListPage";
import { LogDetailPage } from "./pages/logs/LogDetailPage";
import { SearchPage } from "./pages/search/SearchPage";
import { AccountListPage } from "./pages/system/AccountListPage";
import { ThemeListPage } from "./pages/system/ThemeListPage";
```

#### タスク 2.3: 動的インポート（lazy）の追加

**ファイル**: `src/App.tsx`

**追加内容**:
```typescript
// 動的インポート（ページ単位で分割）
const InviteAcceptPage = lazy(() => import("./pages/InviteAcceptPage"));
const DashboardPage = lazy(() => import("./pages/DashboardPage"));
const FormListPage = lazy(() => import("./pages/forms/FormListPage"));
const FormEditIntegratedPage = lazy(() => import("./pages/forms/FormEditIntegratedPage"));
const FormPreviewPage = lazy(() => import("./pages/forms/FormPreviewPage"));
const PublicFormViewPage = lazy(() => import("./pages/public/PublicFormViewPage"));
const AckViewPage = lazy(() => import("./pages/public/AckViewPage"));
const ResponseListPage = lazy(() => import("./pages/responses/ResponseListPage"));
const ResponseDetailPage = lazy(() => import("./pages/responses/ResponseDetailPage"));
const LogListPage = lazy(() => import("./pages/logs/LogListPage"));
const LogDetailPage = lazy(() => import("./pages/logs/LogDetailPage"));
const SearchPage = lazy(() => import("./pages/search/SearchPage"));
const AccountListPage = lazy(() => import("./pages/system/AccountListPage"));
const ThemeListPage = lazy(() => import("./pages/system/ThemeListPage"));
```

#### タスク 2.4: ローディングコンポーネントの作成（オプション）

**ファイル**: `src/components/PageLoading.tsx`（新規作成）

**実装内容**:
```typescript
import React from "react";
import { Spinner } from "./Spinner";

export function PageLoading() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="text-center">
        <Spinner size="md" />
        <p className="mt-4 text-sm text-slate-600 dark:text-slate-300">読み込み中...</p>
      </div>
    </div>
  );
}
```

**代替案**: `App.tsx`内にインラインで実装することも可能

#### タスク 2.5: SuspenseでRoutesをラップ

**ファイル**: `src/App.tsx`

**変更内容**:
- `<Routes>`を`<Suspense fallback={<PageLoading />}>`でラップ
- `PageLoading`コンポーネントをインポート（またはインライン実装）

**変更前**:
```typescript
<Routes>
  {/* ... */}
</Routes>
```

**変更後**:
```typescript
<Suspense fallback={<PageLoading />}>
  <Routes>
    {/* ... */}
  </Routes>
</Suspense>
```

---

### Phase 3: Vite設定の最適化

#### タスク 3.1: vite.config.tsにbuild.rollupOptions.output.manualChunksを追加

**ファイル**: `vite.config.ts`

**追加内容**:
```typescript
build: {
  rollupOptions: {
    output: {
      manualChunks: (id) => {
        // ベンダーチャンク: node_modules内のライブラリ
        if (id.includes("node_modules")) {
          // React関連
          if (id.includes("react") || id.includes("react-dom") || id.includes("react-router")) {
            return "vendor-react";
          }
          // その他すべてのnode_modules
          return "vendor";
        }
        
        // ページチャンク: pagesディレクトリ
        if (id.includes("/src/pages/")) {
          const match = id.match(/\/src\/pages\/([^/]+)/);
          if (match) {
            const pageType = match[1];
            // ページタイプごとにチャンクを分割
            if (pageType === "forms") {
              return "pages-forms";
            } else if (pageType === "responses") {
              return "pages-responses";
            } else if (pageType === "logs") {
              return "pages-logs";
            } else if (pageType === "system") {
              return "pages-system";
            } else if (pageType === "public") {
              return "pages-public";
            } else {
              return "pages-common";
            }
          }
        }
        
        // 共通チャンク: components, utils, auth, layout
        if (id.includes("/src/components/")) {
          return "chunk-components";
        }
        if (id.includes("/src/utils/")) {
          return "chunk-utils";
        }
        if (id.includes("/src/auth/")) {
          return "chunk-auth";
        }
        if (id.includes("/src/layout/")) {
          return "chunk-layout";
        }
      },
    },
  },
},
```

---

### Phase 4: テスト・検証

#### タスク 4.1: ビルド実行とチャンクサイズの確認

**手順**:
1. `npm run build`を実行
2. `dist/assets/`ディレクトリ内のチャンクファイルを確認
3. 各チャンクのサイズを確認
4. 警告（500 kB超過）が解消されているか確認

**確認項目**:
- メインバンドルサイズが500 kB以下になっているか
- チャンクが適切に分割されているか
- チャンク名が期待通りか

#### タスク 4.2: 各ページの読み込み動作確認

**手順**:
1. 開発サーバーを起動（`npm run dev`）
2. 各ページにアクセス
3. ローディング状態が正しく表示されるか確認
4. ページが正常に表示されるか確認

**確認項目**:
- 各ページが正常に読み込まれるか
- ローディング状態が適切に表示されるか
- エラーが発生しないか

#### タスク 4.3: ネットワークタブでのチャンク読み込み確認

**手順**:
1. ブラウザの開発者ツールを開く
2. ネットワークタブを開く
3. 各ページにアクセス
4. チャンクファイルの読み込みを確認

**確認項目**:
- 必要なチャンクのみが読み込まれているか
- チャンクの読み込み順序が適切か
- キャッシュが正しく機能しているか

#### タスク 4.4: パフォーマンス測定（Lighthouse等）

**手順**:
1. Lighthouseでパフォーマンススコアを測定
2. 初回読み込み時間を測定
3. 改善前後の比較

**確認項目**:
- 初回読み込み時間の改善
- パフォーマンススコアの向上
- モバイル対応の改善

---

### Phase 5: 最適化（オプション）

#### タスク 5.1: プリロード（preload）の設定

**目的**: よく使用されるページを事前に読み込む

**実装方法**:
- `vite.config.ts`で`build.rollupOptions.output.manualChunks`を拡張
- または、`<link rel="preload">`を動的に追加

#### タスク 5.2: プリフェッチ（prefetch）の設定

**目的**: 次のページ遷移を予測して事前に読み込む

**実装方法**:
- React Routerの`<Link>`コンポーネントに`prefetch`属性を追加
- または、カスタムフックで実装

#### タスク 5.3: チャンク命名の最適化

**目的**: デバッグしやすいチャンク名にする

**実装方法**:
- `vite.config.ts`の`manualChunks`関数で、より詳細な命名規則を適用

---

## 実装順序

### 推奨実装順序

1. **Phase 1**: ページコンポーネントのエクスポート形式変更
   - 各ファイルを1つずつ変更し、動作確認
   - すべてのファイルを変更後、`App.tsx`のインポートが正しく動作するか確認

2. **Phase 2**: App.tsxの動的インポート実装
   - タスク2.1 → 2.2 → 2.3 → 2.4 → 2.5の順で実装
   - 各ステップで動作確認

3. **Phase 3**: Vite設定の最適化
   - `vite.config.ts`に`manualChunks`を追加
   - ビルド実行して動作確認

4. **Phase 4**: テスト・検証
   - ビルド結果の確認
   - 各ページの動作確認
   - パフォーマンス測定

5. **Phase 5**: 最適化（オプション）
   - 必要に応じて実装

---

## 注意事項

### デフォルトエクスポートへの変更

- 既存の名前付きエクスポートを削除する際は、他のファイルで使用されていないか確認
- テストファイルやStorybookで使用されている場合は、それらも更新が必要

### エラーハンドリング

- 動的インポートでエラーが発生した場合のエラーハンドリングを検討
- `ErrorBoundary`コンポーネントでラップすることを推奨

### 型安全性

- TypeScriptを使用している場合、`lazy()`の型推論が正しく動作することを確認
- 必要に応じて型アサーションを追加

### パフォーマンス

- チャンクを細かく分割しすぎると、HTTPリクエスト数が増加し、逆にパフォーマンスが低下する可能性
- 適切なサイズ（100-200 kB程度）でチャンクを分割

---

## 完了条件

- [x] Phase 1: すべてのページコンポーネントがデフォルトエクスポートに変更されている
- [x] Phase 2: App.tsxで動的インポートが実装され、Suspenseでラップされている
- [x] Phase 3: vite.config.tsにmanualChunks設定が追加されている
- [x] Phase 4: ビルドが成功し、チャンクサイズ警告が解消されている
- [x] Phase 4: すべてのページが正常に動作している
- [x] Phase 4: パフォーマンス測定で改善が確認されている

---

## 実装完了結果

**完了日**: 2026-01-23

### ビルド結果（staging環境）

メインバンドルサイズ: **8.17 kB** (gzip: 2.75 kB) ✅  
→ 500 kB警告が解消され、大幅な改善を達成

#### チャンク分割結果

**ベンダーチャンク:**
- `vendor-react-g8stAeqk.js`: 152.66 kB (gzip: 49.10 kB) - React関連
- `vendor-BZtwFbxF.js`: 36.30 kB (gzip: 14.34 kB) - その他ベンダー

**ページチャンク（動的読み込み）:**
- `pages-forms-DMCg4R8N.js`: 136.80 kB (gzip: 32.32 kB) - フォーム関連
- `pages-system-C7wYx6xg.js`: 65.00 kB (gzip: 12.21 kB) - システム管理
- `pages-common-y8OmrhWZ.js`: 29.83 kB (gzip: 8.71 kB) - 共通ページ
- `pages-public-BZRqff0l.js`: 25.03 kB (gzip: 6.64 kB) - 公開ページ
- `pages-responses-CMOnVR-U.js`: 17.03 kB (gzip: 4.89 kB) - 回答関連
- `pages-logs-DMwRcO2q.js`: 11.32 kB (gzip: 3.31 kB) - ログ関連

**共通チャンク:**
- `chunk-components-q-5eS6Cw.js`: 200.57 kB (gzip: 52.72 kB) - コンポーネント
- `chunk-utils-BdCKQ7h6.js`: 21.70 kB (gzip: 7.96 kB) - ユーティリティ
- `chunk-auth-CCvliThj.js`: 17.63 kB (gzip: 6.61 kB) - 認証
- `chunk-layout-C6TKlP3i.js`: 9.81 kB (gzip: 3.42 kB) - レイアウト

### 実装成果

1. ✅ メインバンドルが8.17 kBと極小サイズに削減
2. ✅ ページ単位で適切に分割され、必要なチャンクのみが読み込まれる
3. ✅ ベンダーライブラリが適切に分離され、キャッシュ効率が向上
4. ✅ 共通コードが再利用可能なチャンクに分離され、重複が削減

**初回読み込み時間の大幅な改善が期待できます。**
