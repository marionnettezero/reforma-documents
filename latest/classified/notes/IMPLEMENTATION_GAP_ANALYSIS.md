# ReForma 実装状況と仕様書の乖離・未実装項目分析

**作成日**: 2026-01-18  
**最終更新日**: 2026-01-18（進捗表示コンポーネント・テーマ機能実装完了）  
**対象**: `reforma-documents/latest/classified/notes/` の仕様書（`apache-basic-auth-config.md`以外）

---

## 1. CSVエクスポートのジョブキュー対応（csv-export-queue-spec.md）

### 仕様書の内容
- `ExportCsvJob`ジョブクラスの作成
- `ResponsesExportController::startCsv()`の修正（ジョブ投入に変更）
- 進捗表示対応（0% → 30% → 50% → 80% → 100%）
- `exports`キューへの投入

### 現在の実装状況
- ✅ **実装済み**: `ExportCsvJob`が作成された（2026-01-18）
- ✅ **実装済み**: `ResponsesExportController::startCsv()`がジョブ投入に変更された
- ✅ **実装済み**: 進捗表示の段階的更新（0% → 30% → 50% → 80% → 100%）

### 実装内容
- ✅ `app/Jobs/ExportCsvJob.php`の作成
- ✅ `ResponsesExportController::startCsv()`の修正（ジョブ投入に変更）
- ✅ 進捗表示の段階的更新（0% → 30% → 50% → 80% → 100%）
- ✅ 翻訳メッセージの確認（既に存在していた）

### 確認事項
- 仕様書（csv-export-queue-spec.md）と実装が一致している（問題なし）

---

## 2. CSVインポート機能（csv-import-spec.md）

### 仕様書の内容
- 選択肢インポート（`options`タイプ）
- 項目全体インポート（`fields`タイプ）
- 進捗表示対応
- エラーレポート機能

### 現在の実装状況
- ✅ **実装済み**: `ImportCsvJob`が存在する
- ✅ **実装済み**: `POST /v1/forms/{id}/fields/import/csv`エンドポイントが存在する
- ✅ **実装済み**: 進捗表示対応済み

### 確認事項
- 仕様書と実装が一致している（問題なし）

---

## 3. ファイルアップロードのジョブキュー対応（file-upload-queue-spec.md）

### 仕様書の内容
- `ProcessFileUploadJob`ジョブクラスの作成
- PDFテンプレートアップロードの非同期処理
- 添付ファイルアップロードの非同期処理
- 進捗表示対応

### 現在の実装状況
- ✅ **実装済み**: `ProcessFileUploadJob`が存在する
- ✅ **実装済み**: 進捗表示対応済み

### 確認事項
- 仕様書と実装が一致している（問題なし）

---

## 4. キューワーカーのsystemdサービス化（queue-worker-systemd-spec.md）

### 仕様書の内容
- systemdサービスファイル（`reforma-queue-worker@.service`）の作成
- 複数キュー対応（`notifications`, `pdfs`, `exports`, `imports`, `uploads`）
- 自動再起動設定

### 現在の実装状況
- ✅ **実装済み**: `scripts/reforma-queue-worker@.service`が存在する
- ✅ **実装済み**: `OPERATION_MANUAL.md`に手順が記載されている

### 確認事項
- 仕様書と実装が一致している（問題なし）

---

## 5. 各画面詳細/編集項目の確認（detail-edit-fields-review.md）

### 5.1 S-02: アカウント一覧（AccountListPage.tsx）

#### 仕様書の不足項目
- 詳細表示: `updated_at`, `is_root`, `form_create_limit_enabled`, `form_create_limit`
- 編集: `is_root`（root-only）, `form_create_limit_enabled`, `form_create_limit`

#### 現在の実装状況
- ✅ **実装済み**: `updated_at`の表示（1129-1135行目）
- ✅ **実装済み**: `is_root`の表示・編集（root-only、1137-1143行目、821-831行目、982-992行目）
- ✅ **実装済み**: `form_create_limit_enabled`, `form_create_limit`の編集（413-414行目、498-499行目）

#### 確認事項
- 仕様書の指摘事項は全て実装済み（問題なし）

---

### 5.2 S-03: テーマ一覧（ThemeListPage.tsx）

#### 仕様書の不足項目
- 詳細表示・編集機能全体
- `usage_count`の表示
- `GET /v1/system/themes/{id}/usage`の実装
- `POST /v1/system/themes/{id}/copy`の実装

#### 現在の実装状況
- ✅ **実装済み**: 詳細表示機能（729-799行目）
- ✅ **実装済み**: 編集機能（637-727行目）
- ✅ **実装済み**: `usage_count`の表示（514-515行目、一覧に表示）
- ✅ **実装済み**: `GET /v1/system/themes/{id}/usage`の呼び出し（詳細モーダルで使用状況を取得、274行目）
- ✅ **実装済み**: `POST /v1/system/themes/{id}/copy`の呼び出し（コピー機能のUI実装済み、385行目、618行目、956行目）

#### 確認事項
- 仕様書の指摘事項は全て実装済み（問題なし）

---

### 5.3 F-01: フォーム一覧（FormListPage.tsx）

#### 仕様書の不足項目
- 詳細表示・編集機能全体
- 多数のフィールド（通知設定、PDF設定、テーマ設定等）

#### 現在の実装状況
- ✅ **実装済み**: 詳細表示機能（579-651行目、基本的な情報のみ）
- ❌ **未実装**: 編集機能（編集モーダルがない）
- ❌ **未実装**: 詳細表示に不足している項目:
  - `attachment_enabled`, `attachment_type`
  - `notification_user_enabled`, `notification_user_email_template`等
  - `notification_admin_enabled`, `notification_admin_user_ids`等
  - `theme_id`, `theme_tokens`
  - `updated_at`（作成日時は表示されているが、更新日時が未確認）

#### 乖離内容
- 詳細表示は基本的な情報のみで、仕様書で要求されている多数のフィールドが未表示
- 編集機能が未実装

---

## 6. CSVエクスポートのプログレス表示フロー（csv-export-progress-flow.md）

### 仕様書の内容
- 進捗表示コンポーネント（`CsvExportProgress`）
- ポーリング機能（2秒間隔）
- 進捗バー表示（0% → 30% → 50% → 80% → 100%）
- 完了時のダウンロードURL表示

### 現在の実装状況
- ✅ **実装済み**: 共通進捗表示コンポーネント（`ProgressDisplay.tsx`）が作成された（2026-01-18）
- ✅ **実装済み**: CSVエクスポート時の進捗表示機能（`ResponseListPage.tsx`）
- ✅ **実装済み**: ファイルアップロード時の進捗表示機能（`FormEditPage.tsx`）
- ✅ **実装済み**: CSVインポート時の進捗表示機能（`FormItemPage.tsx`）

### 実装内容
- ✅ `src/components/ProgressDisplay.tsx`の作成
  - ポーリング機能（2秒間隔、デフォルト）
  - 進捗バー表示、ステータス表示、メッセージ表示
  - 完了時のダウンロードURL表示
  - エラーレポート表示（`result_data.errors`）
- ✅ `ResponseListPage.tsx`にCSVエクスポート機能と進捗表示を統合
- ✅ `FormEditPage.tsx`にファイルアップロード機能と進捗表示を統合
- ✅ `FormItemPage.tsx`にCSVインポート機能と進捗表示を統合

### 確認事項
- 仕様書（csv-export-progress-flow.md）と実装が一致している（問題なし）

---

## 7. 進捗表示コンポーネント（remaining-tasks.md）

### 仕様書の内容
- 共通の進捗表示コンポーネント（`ProgressDisplay`等）
- `GET /v1/progress/{job_id}`のポーリング機能
- 進捗バー表示、ステータス表示、メッセージ表示
- 完了時のダウンロードURL表示
- エラーレポート表示（`result_data.errors`）

### 現在の実装状況
- ✅ **実装済み**: 共通進捗表示コンポーネント（`ProgressDisplay.tsx`）が作成された（2026-01-18）
- ✅ **実装済み**: CSVエクスポートで使用（`ResponseListPage.tsx`）
- ✅ **実装済み**: ファイルアップロードで使用（`FormEditPage.tsx`）
- ✅ **実装済み**: CSVインポートで使用（`FormItemPage.tsx`）

### 実装内容
- ✅ `src/components/ProgressDisplay.tsx`の作成
  - `GET /v1/progress/{job_id}`のポーリング機能（2秒間隔）
  - 進捗バー表示、ステータス表示、メッセージ表示
  - 完了時のダウンロードURL表示
  - エラーレポート表示（`result_data.errors`）
- ✅ 各画面への統合完了

### 確認事項
- `remaining-tasks.md`の「新規追加タスク」として記載されていたが、実装完了（2026-01-18）

---

## 8. テーマ機能（SUPP-THEME-001-spec.md）

### 仕様書の内容
- テーマ管理API（System Admin以上）
- フォームへのテーマ適用API（Form Admin以上）
- 公開フォームでのテーマ適用

### 現在の実装状況（バックエンド）
- ✅ **実装済み**: テーマ管理API（GET/POST/PUT/DELETE /v1/system/themes）
- ✅ **実装済み**: 使用状況確認API（GET /v1/system/themes/{id}/usage）
- ✅ **実装済み**: テーマコピーAPI（POST /v1/system/themes/{id}/copy）
- ✅ **実装済み**: フォームへのテーマ適用（GET/PUT /v1/forms/{id}）

### 現在の実装状況（フロントエンド）
- ✅ **実装済み**: テーマ一覧・作成・削除（ThemeListPage.tsx）
- ✅ **実装済み**: テーマ詳細・編集（ThemeListPage.tsx）
- ✅ **実装済み**: 使用状況確認APIの呼び出し（詳細モーダルで使用状況を取得、274行目）
- ✅ **実装済み**: テーマコピー機能のUI（コピーボタンとモーダル実装済み、385行目、618行目、956行目）
- ✅ **実装済み**: 公開フォームでのテーマ適用（`theme_tokens`をCSS変数に展開、2026-01-18）
- ✅ **実装済み**: フォーム編集でのテーマ選択UI（FormEditPage.tsxにテーマ選択を追加、2026-01-18）

### 実装内容
- ✅ `PublicFormViewPage.tsx`でテーマトークンをCSS変数に展開
  - フォームコンテナに`data-theme-id`属性を付与
  - `theme_tokens`をCSS変数（`--color-primary`、`--color-secondary`等）に変換
  - `useEffect`で動的にCSS変数を設定
- ✅ `FormEditPage.tsx`にテーマ選択UIを追加
  - テーマ一覧API（`GET /v1/system/themes`）を呼び出し
  - セレクトボックスでテーマを選択可能
  - 選択したテーマIDをフォーム更新時に送信

### 確認事項
- テーマ一覧の使用状況確認とコピー機能は実装済み
- 公開フォームでのテーマ適用とフォーム編集でのテーマ選択UIは実装完了（2026-01-18）

---

## 9. システムアーキテクチャ（system-architecture.md）

### 仕様書の内容
- システム全体構成の説明
- コンポーネント詳細
- データフロー
- ジョブキューシステム
- 認証・認可フロー
- デプロイ構成

### 現在の実装状況
- ✅ **実装済み**: 記載されている内容と実装が一致している
- ✅ **実装済み**: systemdサービスファイルが存在する
- ✅ **実装済み**: キューワーカーの管理手順が`OPERATION_MANUAL.md`に記載されている

### 確認事項
- 仕様書と実装が一致している（問題なし）

---

## 10. その他の仕様書（reforma-notes-v1.1.0.md, remaining-tasks.md）

### 確認事項
- `remaining-tasks.md`には多くの実装済み項目が記載されているが、一部の記載と実際の実装に乖離がある
- 「CSVエクスポートのジョブキュー対応」は実装済み（2026-01-18に実装完了）

---

## まとめ

### 重大な乖離・未実装項目

#### バックエンド
1. ✅ **CSVエクスポートのジョブキュー対応**（csv-export-queue-spec.md）- 実装完了（2026-01-18）
   - ✅ `ExportCsvJob`が作成された
   - ✅ `ResponsesExportController::startCsv()`がジョブ投入に変更された
   - ✅ 進捗表示の段階的更新（0% → 30% → 50% → 80% → 100%）

#### フロントエンド
2. ✅ **進捗表示コンポーネント**（csv-export-progress-flow.md, remaining-tasks.md）- 実装完了（2026-01-18）
   - ✅ 共通の進捗表示コンポーネント（`ProgressDisplay.tsx`）が実装された
   - ✅ CSVエクスポート、ファイルアップロード、CSVインポートで使用されている

3. ✅ **テーマ機能の一部**（SUPP-THEME-001-spec.md）- 実装完了（2026-01-18）
   - ✅ **実装済み**: 使用状況確認APIの呼び出し（詳細モーダルで使用状況を取得）
   - ✅ **実装済み**: テーマコピー機能のUI（コピーボタンとモーダル実装済み）
   - ✅ **実装済み**: 公開フォームでのテーマ適用（`theme_tokens`をCSS変数に展開）
   - ✅ **実装済み**: フォーム編集でのテーマ選択UI

4. ❌ **フォーム一覧の詳細・編集機能**（detail-edit-fields-review.md）
   - 編集機能が未実装
   - 詳細表示に多数のフィールドが不足（通知設定、PDF設定、テーマ設定等）

### 実装済み項目（仕様書と一致）

- ✅ CSVインポート機能（csv-import-spec.md）
- ✅ ファイルアップロードのジョブキュー対応（file-upload-queue-spec.md）
- ✅ キューワーカーのsystemdサービス化（queue-worker-systemd-spec.md）
- ✅ アカウント一覧の詳細・編集機能（detail-edit-fields-review.mdの指摘事項は全て実装済み）
- ✅ テーマ一覧の基本機能（詳細・編集・使用状況確認・コピー機能は全て実装済み）
- ✅ 進捗表示コンポーネント（csv-export-progress-flow.md, remaining-tasks.md）
- ✅ テーマ機能の完全実装（公開フォームでのテーマ適用、フォーム編集でのテーマ選択UI）

---

## 推奨対応優先度

### 高優先度
1. ✅ **CSVエクスポートのジョブキュー対応**（バックエンド）- 実装完了（2026-01-18）

2. ✅ **進捗表示コンポーネント**（フロントエンド）- 実装完了（2026-01-18）
   - ✅ CSVエクスポート、ファイルアップロード、CSVインポートで共通利用
   - ✅ ユーザー体験の向上に必須

### 中優先度
3. **フォーム一覧の詳細・編集機能**（フロントエンド）
   - 基本機能の完成に必要
   - 多数のフィールドがあるため、段階的実装推奨

4. ✅ **テーマ機能の完全実装**（フロントエンド）- 実装完了（2026-01-18）
   - ✅ 使用状況確認とコピー機能の追加（実装済み）
   - ✅ 公開フォームでのテーマ適用（実装済み）
   - ✅ フォーム編集でのテーマ選択UI（実装済み）

---

## 補足

- `remaining-tasks.md`の記載内容と実際の実装に一部乖離があるため、定期的な見直しを推奨
- 仕様書の更新時は、実装状況も同時に確認すること
