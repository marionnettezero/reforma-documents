# ダウンロードURL認証エラー調査結果

## 問題

ダウンロードURLにアクセスした際に、`Route [login] not defined`エラーが発生。

## 原因

### 1. 認証トークンが送信されていない

**現状の実装**:
- `ProgressDisplay.tsx`: `<a href={downloadUrl} download>`を使用
- `FormItemPage.tsx`: `window.open(downloadUrl, '_blank')`を使用
- `FieldDetailPanel.tsx`: `window.open(downloadUrl, '_blank')`を使用

**問題点**:
- 通常のブラウザナビゲーション（`<a href>`や`window.open()`）では、`Authorization: Bearer <token>`ヘッダーが自動的に送信されない
- 認証トークンは`localStorage`に保存されているが、通常のHTTPリクエストでは自動的に送信されない
- `apiFetch`を使用していないため、認証ヘッダーが含まれていない

### 2. Sanctumの認証方法

- `auth:sanctum`ミドルウェアは、Bearer tokenまたはCookieベースの認証をサポート
- しかし、APIエンドポイントではBearer tokenが期待されている
- Cookieベースの認証は、同一ドメインのSPA（Single Page Application）で使用される

## 解決策

### 推奨: fetch APIを使用してダウンロード

`fetch` APIを使用してダウンロードすることで、認証ヘッダーを送信できます。

**実装例**:
```typescript
const downloadFile = async (downloadUrl: string) => {
  const authToken = localStorage.getItem("reforma.auth.token");
  const fullUrl = `${window.location.origin}${downloadUrl}`;
  
  const response = await fetch(fullUrl, {
    headers: {
      'Authorization': `Bearer ${authToken}`,
    },
  });
  
  if (!response.ok) {
    throw new Error('Download failed');
  }
  
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'export.csv'; // ファイル名を設定
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
};
```

### 代替案1: 一時的な署名付きURL（推奨しない）

バックエンド側で一時的な署名付きURLを生成する方法もありますが、実装が複雑になります。

### 代替案2: クエリパラメータにトークンを追加（非推奨）

セキュリティリスクがあるため、推奨しません。

## 実装内容 ✅ 実装済み

### 1. `src/utils/apiFetch.ts`
- `downloadFile()`関数を追加
- 認証トークンを`Authorization: Bearer <token>`ヘッダーで送信
- `fetch` APIを使用してファイルをダウンロード
- Blobとして取得し、`<a>`要素でダウンロードを実行

### 2. `src/components/ProgressDisplay.tsx`
- `<a href>`を`<button onClick>`に変更
- `downloadFile()`関数を使用して認証付きでダウンロード
- エラー時は従来の方法（`window.open()`）でフォールバック

### 3. `src/pages/forms/FormItemPage.tsx`
- `window.open()`を`downloadFile()`関数に置き換え
- エラー時は従来の方法でフォールバック

### 4. `src/components/FieldDetailPanel.tsx`
- `window.open()`を`downloadFile()`関数に置き換え
- エラー時は従来の方法でフォールバック

## 実装ファイル

- `src/utils/apiFetch.ts` - `downloadFile()`関数を追加
- `src/components/ProgressDisplay.tsx` - ダウンロードボタンを修正
- `src/pages/forms/FormItemPage.tsx` - エクスポート完了時のダウンロード処理を修正
- `src/components/FieldDetailPanel.tsx` - エクスポート完了時のダウンロード処理を修正
