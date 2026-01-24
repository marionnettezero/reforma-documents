# テーマ作成/編集モーダル共通化タスク

## 概要

テーマの新規作成モーダルと編集モーダルを1つの共通モーダルコンポーネントに統合し、コードの重複を削減します。

## 現状確認（2026-01-20）

### 作成モーダル

**ファイル**: `src/pages/system/ThemeListPage.tsx` (727-1046行目)

**構造**:
- タイトル: `t("theme_create")`
- テーマコード（入力可能、必須）✅
- テーマ名（入力可能、必須）
- 説明（入力可能）
- テーマトークン(JSON)（入力可能、必須）
- カスタムスタイル設定
  - ヘッダ/フッタ設定
  - 詳細カスタマイズ（コンテナ、カード、ボタン、入力フィールド）
  - グローバルCSS
- ボタン（作成、キャンセル）

**特徴**:
- アコーディオンなし（フラットな構造）
- テーマコードが入力可能
- 有効/無効チェックボックスなし
- スクロール対応なし

### 編集モーダル

**ファイル**: `src/pages/system/ThemeListPage.tsx` (1048-1380行目)

**構造**:
- タイトル: `t("theme_edit_title") || t("theme_edit") || "テーマ編集"`
- 基本情報アコーディオン（開く）✅
  - テーマコード（読み取り専用）✅
  - テーマ名（入力可能、必須）
  - 説明（入力可能）
- カスタムスタイル設定アコーディオン（閉じる）
  - ヘッダ/フッタ設定
  - 詳細カスタマイズ（コンテナ、カード、ボタン、入力フィールド）
  - グローバルCSS
- テーマトークン(JSON)※旧スタイル情報アコーディオン（閉じる）
- 有効/無効チェックボックス
- ボタン（更新、キャンセル）

**特徴**:
- アコーディオンで整理されている
- テーマコードが読み取り専用
- 有効/無効チェックボックスあり
- スクロール対応あり（`max-h-[calc(100vh-16rem)] overflow-y-auto`）

### 主な違い

| 項目 | 作成モーダル | 編集モーダル |
|------|------------|------------|
| テーマコード | 入力可能（必須） | 読み取り専用 |
| アコーディオン | なし | あり（基本情報、カスタムスタイル、テーマトークン） |
| 有効/無効チェックボックス | なし | あり |
| スクロール対応 | なし | あり |
| ボタンラベル | 作成 | 更新 |
| タイトル | `theme_create` | `theme_edit_title` |

### 共通部分

- テーマ名（入力可能、必須）
- 説明（入力可能）
- テーマトークン(JSON)（入力可能、必須）
- カスタムスタイル設定（完全に同じ構造）
  - ヘッダ/フッタ設定
  - 詳細カスタマイズ（コンテナ、カード、ボタン、入力フィールド）
  - グローバルCSS

## 共通化の方針

### アプローチ1: 1つのモーダルでモード切り替え（推奨）

**メリット**:
- コードの重複を完全に削減
- メンテナンスが容易
- UIの一貫性が保たれる

**実装方法**:
- `isEditMode` フラグで作成/編集を切り替え
- テーマコードの表示/入力を条件分岐
- 有効/無効チェックボックスを編集モード時のみ表示
- アコーディオン構造を統一（編集モーダルの構造を採用）
- タイトルとボタンラベルをモードに応じて変更

### アプローチ2: 共通コンポーネントとして抽出

**メリット**:
- 再利用性が高い
- テストが容易

**デメリット**:
- コンポーネントの抽出に時間がかかる
- 現時点では1箇所でしか使用されない

## タスクリスト

### タスク1: モーダルの状態管理を統合
- [ ] `showCreateModal` と `showEditModal` を `showThemeModal` に統合
- [ ] `isEditMode` フラグを追加（`selectedTheme !== null` で判定）
- [ ] モーダルを開く関数を統合（`openThemeModal(theme?: Theme)`）

### タスク2: モーダルコンテンツを統合
- [ ] 作成モーダルのコンテンツを削除
- [ ] 編集モーダルのコンテンツをベースに、作成モードにも対応
- [ ] テーマコードの表示/入力を条件分岐
  - 編集モード: 読み取り専用
  - 作成モード: 入力可能（必須）
- [ ] 有効/無効チェックボックスを編集モード時のみ表示

### タスク3: タイトルとボタンの動的変更
- [ ] タイトルをモードに応じて変更
  - 作成: `t("theme_create_title") || t("theme_create") || "テーマ作成"`
  - 編集: `t("theme_edit_title") || t("theme_edit") || "テーマ編集"`
- [ ] ボタンラベルをモードに応じて変更
  - 作成: `t("creating") : t("create_new")`
  - 編集: `t("account_edit_updating") : t("account_edit_update_button")`

### タスク4: フォーム初期化の統合
- [ ] `openThemeModal` 関数でフォーム状態を初期化
- [ ] 編集モード時は `selectedTheme` から値を読み込み
- [ ] 作成モード時はデフォルト値を設定

### タスク5: 保存処理の統合
- [ ] `handleCreate` と `handleUpdate` を `handleSave` に統合
- [ ] モードに応じて API を呼び分け
  - 作成: `POST /v1/system/themes`
  - 編集: `PUT /v1/system/themes/{id}`

### タスク6: アコーディオン構造の統一
- [ ] 作成モーダルにもアコーディオン構造を適用
- [ ] 基本情報アコーディオン（デフォルトで開く）
- [ ] カスタムスタイル設定アコーディオン（デフォルトで閉じる）
- [ ] テーマトークンアコーディオン（デフォルトで閉じる）

### タスク7: スクロール対応の統一
- [ ] 作成モーダルにもスクロール対応を追加
- [ ] `max-h-[calc(100vh-16rem)] overflow-y-auto` を適用

### タスク8: 多言語対応の統一
- [ ] 作成モーダルにも多言語キーを適用
- [ ] すべてのラベルを多言語対応

## 実装詳細

### 統合後のモーダル構造

```tsx
<ConfirmDialog
  open={showThemeModal}
  title={isEditMode 
    ? (t("theme_edit_title") || t("theme_edit") || "テーマ編集")
    : (t("theme_create_title") || t("theme_create") || "テーマ作成")
  }
  onClose={handleCloseModal}
>
  <div className="space-y-4 max-h-[calc(100vh-16rem)] overflow-y-auto">
    <Accordion>
      {/* 基本情報 */}
      <AccordionItem title={t("theme_basic_info") || "基本情報"} defaultOpen={true}>
        <div className="space-y-4">
          {/* テーマコード */}
          {isEditMode ? (
            // 読み取り専用
            <input value={selectedTheme.code} disabled readOnly />
          ) : (
            // 入力可能
            <input value={formCode} onChange={...} />
          )}
          
          {/* テーマ名 */}
          <input value={formName} onChange={...} />
          
          {/* 説明 */}
          <textarea value={formDescription} onChange={...} />
        </div>
      </AccordionItem>

      {/* カスタムスタイル設定 */}
      <AccordionItem title={t("theme_custom_style_config") || "カスタムスタイル設定"} defaultOpen={false}>
        {/* 共通のカスタムスタイル設定UI */}
      </AccordionItem>

      {/* テーマトークン */}
      <AccordionItem title={t("theme_tokens_legacy") || "テーマトークン (JSON)※旧スタイル情報"} defaultOpen={false}>
        {/* テーマトークン入力 */}
      </AccordionItem>
    </Accordion>

    {/* 有効/無効チェックボックス（編集モード時のみ） */}
    {isEditMode && (
      <div>
        <label>
          <input type="checkbox" checked={formIsActive} onChange={...} />
          <span>{t("active") || "有効"}</span>
        </label>
      </div>
    )}

    {/* ボタン */}
    <div className="flex gap-3 pt-4 border-t border-gray-200">
      <button onClick={handleSave}>
        {isEditMode 
          ? (formSubmitting ? t("account_edit_updating") : t("account_edit_update_button"))
          : (formSubmitting ? t("creating") : t("create_new"))
        }
      </button>
      <button onClick={handleCloseModal}>
        {t("cancel")}
      </button>
    </div>
  </div>
</ConfirmDialog>
```

## 注意点

1. **後方互換性**: 既存の動作に影響を与えないよう注意
2. **フォーム状態のリセット**: モーダルを閉じる際にフォーム状態を適切にリセット
3. **エラーハンドリング**: 作成と編集でエラーメッセージが異なる可能性があるため、適切に処理
4. **バリデーション**: 作成時と編集時でバリデーションルールが異なる可能性があるため、確認が必要

## 進捗状況

- **全体進捗**: 0/8 タスク完了（0%）
- **最終更新**: 2026-01-20
- **完了タスク**: なし
- **進行中タスク**: なし
- **未着手タスク**: タスク1-8（すべて）
