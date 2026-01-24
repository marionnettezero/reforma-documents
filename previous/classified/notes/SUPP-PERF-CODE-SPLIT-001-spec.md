# SUPP-PERF-CODE-SPLIT-001: コード分割（Code Splitting）最適化 実装仕様

**作成日**: 2026-01-22  
**最終更新日**: 2026-01-22  
**バージョン**: v1.0.0

---

## 概要

ビルド時のバンドルサイズ警告（511.88 kB）を解消するため、コード分割（code splitting）を実装する。ページ単位での動的インポート（lazy loading）を導入し、初回読み込み時間を短縮し、ユーザー体験を向上させる。

---

## 現在の実装状況

### ビルド結果

**現在のバンドルサイズ**:
- `dist/assets/index-whKN_JyE.js`: 511.88 kB（gzip後: 136.84 kB）
- 警告: "Some chunks are larger than 500 kB after minification"

**問題点**:
- すべてのページコンポーネントが1つのバンドルに含まれている
- 初回読み込み時に不要なページのコードも読み込まれる
- モバイルや低速回線での読み込み時間が長くなる可能性

**既存実装**:
- ✅ Viteビルド設定（`vite.config.ts`）
- ✅ React Routerによるルーティング（`App.tsx`）
- ✅ ページコンポーネントの静的インポート

**未実装**:
- ⏳ ページ単位の動的インポート（lazy loading）
- ⏳ チャンク分割設定
- ⏳ ローディング状態の管理

---

## データモデル

### チャンク分割戦略

#### 1. ベンダーチャンク（vendor chunks）

**目的**: サードパーティライブラリを分離

**対象**:
- `react`, `react-dom`, `react-router-dom`
- UIライブラリ（使用している場合）
- その他の外部依存関係

**期待効果**: ベンダーコードは変更頻度が低いため、ブラウザキャッシュを有効活用

#### 2. ページチャンク（page chunks）

**目的**: ページ単位でコードを分割

**対象ページ**:
- 管理画面ページ（Dashboard, FormList, FormEdit, FormItem, ResponseList, etc.）
- 公開フォームページ（PublicFormView, AckView）
- システム管理ページ（AccountList, ThemeList）

**期待効果**: 必要なページのコードのみを読み込み、初回読み込み時間を短縮

#### 3. 共通チャンク（common chunks）

**目的**: 複数ページで使用される共通コンポーネント・ユーティリティを分離

**対象**:
- 共通コンポーネント（ScreenHeader, Card, Spinner, etc.）
- 共通ユーティリティ（apiFetch, errorCodes, etc.）
- 認証関連（AuthContext, RequireAuth, etc.）

**期待効果**: 共通コードの重複を避け、キャッシュ効率を向上

---

## フロントエンド実装

### 1. 動的インポートの実装

**ファイル**: `src/App.tsx`

**変更内容**:

```typescript
import React, { Suspense, lazy } from "react";
import { Navigate, Route, Routes, useLocation, useNavigate } from "react-router-dom";
import { AuthProvider } from "./auth/AuthContext";
import { useAuth } from "./auth/AuthContext";
import { RequireAuth } from "./auth/RequireAuth";
import { RequireRoles } from "./auth/RequireRole";
import type { Role } from "./auth/types";
import { AppLayout } from "./layout/AppLayout";
import { ROUTES } from "./routePaths";
import { getScreenById } from "./specs/screenRegistry";
import { Spinner } from "./components/Spinner";

// 静的インポート（初期表示に必要）
import { LoginPage } from "./pages/LoginPage";
import { LogoutPage } from "./pages/LogoutPage";
import { ErrorPage } from "./pages/ErrorPage";
import { NotFoundPage } from "./pages/NotFoundPage";

// 動的インポート（ページ単位で分割）
const DashboardPage = lazy(() => import("./pages/DashboardPage"));
const FormListPage = lazy(() => import("./pages/forms/FormListPage"));
const FormEditPage = lazy(() => import("./pages/forms/FormEditPage"));
const FormItemPage = lazy(() => import("./pages/forms/FormItemPage"));
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

// ローディングコンポーネント
function PageLoading() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="text-center">
        <Spinner size="md" />
        <p className="mt-4 text-sm text-slate-600 dark:text-slate-300">読み込み中...</p>
      </div>
    </div>
  );
}

// ... 既存のコンポーネント（RootRedirect, Protected, SessionInvalidWatcher, etc.） ...

export function App() {
  return (
    <AuthProvider>
      <ToastProvider>
        <SessionInvalidWatcher />
        <ForbiddenReasonWatcher />
        <ServerErrorWatcher />
        <Suspense fallback={<PageLoading />}>
          <Routes>
            {/* Public */}
            <Route path={ROUTES.LOGIN} element={<LoginPage />} />
            <Route path={ROUTES.FORM_VIEW} element={<PublicFormViewPage />} />
            <Route path={ROUTES.ACK_VIEW} element={<AckViewPage />} />

            {/* Logout (unprotected) */}
            <Route element={<AppLayout />}>
              <Route path={ROUTES.LOGOUT} element={<LogoutPage />} />
            </Route>

            {/* Protected (common layout) */}
            <Route element={<Protected screenId={"SYS_DASH"}><AppLayout /></Protected>}>
              <Route path={ROUTES.SYS_DASH} element={<DashboardPage />} />

              <Route
                path={ROUTES.ACCOUNT_LIST}
                element={
                  <Protected screenId={"ACCOUNT_LIST"}>
                    <AccountListPage />
                  </Protected>
                }
              />

              <Route
                path={ROUTES.THEME_LIST}
                element={
                  <Protected screenId={"THEME_LIST"}>
                    <ThemeListPage />
                  </Protected>
                }
              />

              <Route path={ROUTES.FORM_LIST} element={<FormListPage />} />
              <Route path={ROUTES.FORM_EDIT} element={<FormEditPage />} />
              <Route path={ROUTES.FORM_ITEM} element={<FormItemPage />} />
              <Route path={ROUTES.FORM_PREVIEW} element={<FormPreviewPage />} />

              <Route path={ROUTES.RESPONSE_LIST} element={<ResponseListPage />} />
              <Route path={ROUTES.RESPONSE_DETAIL} element={<ResponseDetailPage />} />

              <Route path={ROUTES.LOG_LIST} element={<LogListPage />} />
              <Route path={ROUTES.LOG_DETAIL} element={<LogDetailPage />} />

              <Route path={ROUTES.SEARCH} element={<SearchPage />} />
              <Route path={ROUTES.ERROR} element={<ErrorPage />} />
            </Route>

            <Route path="/" element={<RootRedirect />} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </Suspense>
      </ToastProvider>
    </AuthProvider>
  );
}
```

### 2. Vite設定の最適化

**ファイル**: `vite.config.ts`

**変更内容**:

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { readFileSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const ROOT_DIR = join(__dirname, ".");

const pkg = JSON.parse(readFileSync(join(ROOT_DIR, "package.json"), "utf-8"));

export default defineConfig({
  base: process.env.VITE_BASE ?? "/reforma/",
  plugins: [react()],
  server: { port: 5173 },
  define: {
    "import.meta.env.VITE_APP_NAME": JSON.stringify(pkg.name),
    "import.meta.env.VITE_APP_VERSION": JSON.stringify(pkg.version),
  },
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
            // その他のベンダーライブラリ（使用している場合）
            // if (id.includes("some-other-library")) {
            //   return "vendor-other";
            // }
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
    // チャンクサイズ警告の閾値を調整（オプション）
    // chunkSizeWarningLimit: 1000,
  },
});
```

### 3. ローディング状態の管理

**ファイル**: `src/components/PageLoading.tsx`（新規作成、オプション）

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

**使用例**:

```typescript
// App.tsx
import { PageLoading } from "./components/PageLoading";

<Suspense fallback={<PageLoading />}>
  {/* ... */}
</Suspense>
```

---

## 期待される効果

### ビルド結果の改善

**分割前**:
- `index-whKN_JyE.js`: 511.88 kB（gzip後: 136.84 kB）

**分割後（予想）**:
- `vendor-react.js`: ~150-200 kB（gzip後: ~50-60 kB）
- `vendor.js`: ~50-100 kB（gzip後: ~15-30 kB）
- `chunk-components.js`: ~50-80 kB（gzip後: ~15-25 kB）
- `chunk-utils.js`: ~20-30 kB（gzip後: ~5-10 kB）
- `pages-forms.js`: ~80-120 kB（gzip後: ~25-35 kB）
- `pages-responses.js`: ~40-60 kB（gzip後: ~12-18 kB）
- `pages-logs.js`: ~30-40 kB（gzip後: ~10-12 kB）
- `pages-system.js`: ~30-40 kB（gzip後: ~10-12 kB）
- `pages-public.js`: ~60-80 kB（gzip後: ~18-25 kB）
- `pages-common.js`: ~20-30 kB（gzip後: ~6-10 kB）

**初回読み込み**:
- メインバンドル: ~200-250 kB（gzip後: ~60-80 kB）
- ページチャンク: 必要なページのみ読み込み（~40-120 kB、gzip後: ~12-35 kB）

**改善効果**:
- 初回読み込み時間: 約30-50%短縮（予想）
- キャッシュ効率: ベンダーコードのキャッシュ活用により、2回目以降の読み込みが高速化
- モバイル対応: 低速回線での読み込み時間が大幅に改善

---

## 実装タスク

### フロントエンド

#### 動的インポート実装
- ⏳ `App.tsx`でページコンポーネントを`lazy()`でラップ
- ⏳ `Suspense`コンポーネントでローディング状態を管理
- ⏳ ローディングコンポーネント（`PageLoading`）の作成（オプション）

#### Vite設定最適化
- ⏳ `vite.config.ts`に`manualChunks`設定を追加
- ⏳ ベンダーチャンクの分割設定
- ⏳ ページチャンクの分割設定
- ⏳ 共通チャンクの分割設定

#### テスト・検証
- ⏳ ビルド実行とチャンクサイズの確認
- ⏳ 各ページの読み込み動作確認
- ⏳ ローディング状態の表示確認
- ⏳ パフォーマンス測定（Lighthouse等）

#### 最適化（オプション）
- ⏳ プリロード（preload）の設定
- ⏳ プリフェッチ（prefetch）の設定
- ⏳ チャンク命名の最適化

---

## 後方互換性

### 既存機能への影響

**影響なし**:
- 既存のルーティング機能
- 既存の認証・認可機能
- 既存のAPI呼び出し
- 既存のUIコンポーネント

**変更点**:
- ページコンポーネントの読み込み方法が動的インポートに変更
- 初回ページアクセス時にローディング状態が表示される（UX改善）

### ブラウザ対応

**対応ブラウザ**:
- モダンブラウザ（Chrome, Firefox, Safari, Edge）の最新版
- `React.lazy()`と`Suspense`はReact 16.6以降でサポート
- 動的インポート（`import()`）はES2020で標準化

**フォールバック**:
- 古いブラウザでは、Viteが自動的にポリフィルを適用
- ローディング状態の表示により、ユーザー体験を維持

---

## 注意事項

### パフォーマンス

1. **チャンクサイズのバランス**:
   - チャンクを細かく分割しすぎると、HTTPリクエスト数が増加し、逆にパフォーマンスが低下する可能性
   - 適切なサイズ（100-200 kB程度）でチャンクを分割

2. **プリロード戦略**:
   - よく使用されるページはプリロードを検討
   - ただし、過度なプリロードは帯域を無駄に消費するため注意

3. **キャッシュ戦略**:
   - ベンダーチャンクは変更頻度が低いため、長期キャッシュが有効
   - ページチャンクは変更頻度が高いため、適切なキャッシュヘッダーを設定

### デバッグ

1. **ソースマップ**:
   - 開発環境ではソースマップが有効
   - 本番環境ではソースマップを無効化（セキュリティとパフォーマンスのため）

2. **チャンク名の確認**:
   - ビルド後の`dist/assets/`ディレクトリでチャンクファイルを確認
   - 期待通りの分割が行われているか確認

3. **ネットワークタブ**:
   - ブラウザの開発者ツールでネットワークタブを確認
   - チャンクの読み込み順序とタイミングを確認

### 実装時の注意

1. **デフォルトエクスポート**:
   - `lazy()`を使用する場合、コンポーネントはデフォルトエクスポートである必要がある
   - 既存のコンポーネントが名前付きエクスポートの場合は、`export default`に変更

2. **エラーバウンダリ**:
   - 動的インポートでエラーが発生した場合のエラーハンドリングを検討
   - `ErrorBoundary`コンポーネントでラップすることを推奨

3. **型安全性**:
   - TypeScriptを使用している場合、`lazy()`の型推論が正しく動作することを確認

---

## 参照

- `vite.config.ts` - Viteビルド設定
- `src/App.tsx` - ルーティング設定
- `src/pages/` - ページコンポーネント
- [Vite公式ドキュメント - Code Splitting](https://vitejs.dev/guide/build.html#code-splitting)
- [React公式ドキュメント - Code Splitting](https://react.dev/reference/react/lazy)
- [Rollup公式ドキュメント - manualChunks](https://rollupjs.org/configuration-options/#output-manualchunks)
