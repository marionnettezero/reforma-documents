# operatorロールのフォームプレビューアクセス対応タスク

## 概要

operatorロールで、一覧に表示されているフォームのプレビューを表示しようとすると、権限がないエラー画面に遷移する問題を解決する。

## 現状確認

### 問題の流れ

1. **フロントエンド側**: FormPreviewPageが `/forms/{form_id}/preview` で表示される
2. **FormPreviewPageの実装**:
   - まず `/v1/forms/{form_id}` を呼び出して `form.code` を取得（65行目）
   - その後 `/v1/public/forms/{formCode}` を呼び出して公開フォームデータを取得（87行目）
3. **権限エラーの発生箇所**: `/v1/forms/{form_id}` の呼び出し時に権限エラーが発生

### 権限チェックの現状

#### フロントエンド側（screen.v1.0.json）
- **FORM_PREVIEW画面のallow_roles**: `["form_admin", "system_admin"]` のみ
- **operatorロールが含まれていない**

#### バックエンド側（FormsController@show）
- **エンドポイント**: `GET /v1/forms/{id}`
- **権限チェック**: `checkFormAccess($id, 'read')` を呼び出し
  - レイヤー1: `forms.read` パーミッションのチェック
  - レイヤー2: `canAccessForm($formId)` のチェック（リソースパーミッション）

#### パーミッション設定（RolePermissionsSeeder）
- **operatorロール**: `forms.read` パーミッションは付与済み（67行目）

#### リソースパーミッション（User@canAccessForm）
- **form_access_restriction_enabled = true の場合**:
  - `user_form_access`テーブルに登録されているフォームのみアクセス可能
  - 一覧（index）も `accessibleForms()` で同様にフィルタしているため、**フォームアクセス制限が有効なとき、一覧に表示されているフォームはすべて `user_form_access` に含まれる**（「一覧には出ているが `user_form_access` にない」という組み合わせは発生しない）

### 問題の原因

1. **フロントエンド側**: FORM_PREVIEW画面の`allow_roles`に`operator`が含まれていない（**主因**）
2. **バックエンド側**: プレビュー取得に`/v1/forms/{id}`を利用している。`checkFormAccess`（`canAccessForm`）によりリソースアクセスを判定。一覧（index）も`accessibleForms()`で同様にフィルタしているため、一覧に表示されているフォームは `canAccessForm` でも通る想定。プレビュー用途に特化したエンドポイントを新設する方針

## 解決方針

### 方針1: フロントエンド側の権限設定を修正し、バックエンド側でプレビュー専用エンドポイントを作成（推奨）

**メリット**:
- プレビュー用途に特化したエンドポイントで、権限チェックを緩和できる
- 既存の`/v1/forms/{id}`エンドポイントの動作を変更しない
- セキュリティを維持しつつ、プレビュー機能を提供できる

**デメリット**:
- 新しいエンドポイントを追加する必要がある

### 方針2: フロントエンド側の権限設定を修正し、フロントエンド側でform_codeを別の方法で取得

**メリット**:
- バックエンド側の変更が不要

**デメリット**:
- フロントエンド側の実装が複雑になる
- 一覧APIからform_codeを取得する必要がある

### 方針3: 既存の`/v1/forms/{id}`エンドポイントの権限チェックを緩和

**メリット**:
- 新しいエンドポイントを追加する必要がない

**デメリット**:
- 既存の動作を変更するため、影響範囲が大きい
- セキュリティリスクが高まる可能性がある

## 推奨実装: 方針1

### タスク1: フロントエンド側の権限設定を修正

#### 1.1 screen.v1.0.jsonの修正
- **ファイル**: `src/specs/screen.v1.0.json`
- **変更内容**: FORM_PREVIEW画面の`allow_roles`に`operator`を追加
- **変更前**: `"allow_roles": ["form_admin", "system_admin"]`
- **変更後**: `"allow_roles": ["form_admin", "system_admin", "operator"]`

#### 1.2 実装ファイル
- `src/specs/screen.v1.0.json`（修正）

---

### タスク2: バックエンド側でプレビュー専用エンドポイントを作成

#### 2.1 ルーティングの追加
- **ファイル**: `routes/api.php`
- **エンドポイント**: `GET /v1/forms/{id}/preview`
- **権限**: `forms.read`パーミッションを持つユーザー（operator含む）
- **リソースパーミッション**: 一覧に表示されているフォーム（`accessibleForms()`でフィルタリング済み）であればアクセス可能

#### 2.2 FormsControllerにpreviewメソッドを追加
- **ファイル**: `app/Http/Controllers/Api/V1/FormsController.php`
- **メソッド**: `preview(Request $request, int $id): JsonResponse`
- **責務**: プレビュー用のフォームデータを返却（form.codeのみ返却）

#### 2.3 権限チェックの実装
- **操作パーミッション**: `forms.read`パーミッションをチェック
- **リソースパーミッション**: 一覧に表示されているフォーム（`accessibleForms()`でフィルタリング済み）であればアクセス可能
  - `form_access_restriction_enabled = true` の場合: `user_form_access`テーブルに登録されているフォームのみ
  - `form_access_restriction_enabled = false` の場合: 全フォームにアクセス可能
  - system_admin, root: 全フォームにアクセス可能

#### 2.4 実装ファイル
- `routes/api.php`（修正）
- `app/Http/Controllers/Api/V1/FormsController.php`（修正）

---

### タスク3: フロントエンド側でプレビュー専用エンドポイントを使用

#### 3.1 FormPreviewPageの修正
- **ファイル**: `src/pages/forms/FormPreviewPage.tsx`
- **変更内容**: `/v1/forms/{form_id}`の代わりに`/v1/forms/{form_id}/preview`を使用
- **変更前**: `apiGetJson<{ success: boolean; data: { form: { code: string } } }>(`/v1/forms/${form_id}`)`
- **変更後**: `apiGetJson<{ success: boolean; data: { form: { code: string } } }>(`/v1/forms/${form_id}/preview`)`

#### 3.2 実装ファイル
- `src/pages/forms/FormPreviewPage.tsx`（修正）

---

## 実装順序

1. **タスク1**: フロントエンド側の権限設定を修正（operatorを追加）
2. **タスク2**: バックエンド側でプレビュー専用エンドポイントを作成
3. **タスク3**: フロントエンド側でプレビュー専用エンドポイントを使用

---

## 技術的な考慮事項

### セキュリティ
- プレビュー専用エンドポイントは、`forms.read`パーミッションを持つユーザーのみアクセス可能
- リソースパーミッションは、一覧に表示されているフォーム（`accessibleForms()`でフィルタリング済み）のみアクセス可能
- 既存の`/v1/forms/{id}`エンドポイントの動作は変更しない

### 後方互換性
- 既存のAPIエンドポイントの動作は変更しない
- フロントエンド側の変更は、新しいエンドポイントを使用するのみ

### テスト
- operatorロールで、一覧に表示されているフォームのプレビューが表示できることを確認
- operatorロールで、一覧に表示されていないフォームのプレビューが表示できないことを確認
- form_admin, system_adminロールで、既存の動作が維持されることを確認

---

## 関連ファイル一覧

### 修正
- `src/specs/screen.v1.0.json`（FORM_PREVIEWのallow_rolesにoperatorを追加）
- `routes/api.php`（プレビュー専用エンドポイントを追加）
- `app/Http/Controllers/Api/V1/FormsController.php`（previewメソッドを追加）
- `src/pages/forms/FormPreviewPage.tsx`（プレビュー専用エンドポイントを使用）

---

## 実装状況

- ✅ タスク1: screen.v1.0.json の FORM_PREVIEW allow_roles に operator 追加（完了）
- ✅ タスク2: GET /v1/forms/{id}/preview と FormsController::preview 追加（完了）
- ✅ タスク3: FormPreviewPage で /v1/forms/{id}/preview を使用（完了）
