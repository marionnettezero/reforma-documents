# ReForma 実装状況と仕様書の乖離・未実装項目分析

**作成日**: 2026-01-18  
**最終更新日**: 2026-01-19（SUPP-DISPLAY-MODE-001: 表示モード機能・条件分岐ビルダーUI実装完了）  
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
- ✅ **実装済み**: 詳細表示機能（579-751行目、2026-01-18に拡張）
  - ✅ 基本情報（ID、コード、ステータス、公開フラグ、対応言語、回答数）
  - ✅ 添付ファイル設定（有効化、タイプ）
  - ✅ 通知設定（ユーザー・管理者、有効化、件名、送信元等）
  - ✅ テーマ設定（テーマ名、テーマコード）
  - ✅ 作成日時・更新日時
- ✅ **実装済み**: 編集機能（`FormEditPage.tsx`で実装済み）
  - ✅ 新規作成と編集を同じ画面（`FormEditPage`）で実装
  - ✅ 新規作成は`FormListPage`で行い、作成後に`FormEditPage`に遷移
  - ✅ 詳細表示から「編集」ボタンで`FormEditPage`に遷移
  - ✅ 通知設定、添付ファイル設定、テーマ設定等の編集機能が実装済み

#### 実装内容
- ✅ `FormListPage.tsx`の詳細表示モーダルに不足項目を追加（2026-01-18）
  - 添付ファイル設定セクション
  - 通知設定（ユーザー）セクション
  - 通知設定（管理者）セクション
  - テーマ設定セクション
- ✅ `FormEditPage.tsx`で編集機能が実装済み
  - 新規作成と編集を同じ画面で実装
  - すべてのフィールドの編集が可能

#### 確認事項
- 詳細表示は読み取り専用で、編集は`FormEditPage`に遷移する設計
- 新規作成と編集を同じ画面（`FormEditPage`）で実装（2026-01-18）

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

### remaining-tasks.mdの未実装項目の実装状況確認

#### 実装済み項目（remaining-tasks.mdでは未実装と記載されているが、実際には実装済み）
- ✅ **DashboardPage**: API連携実装済み（`/v1/dashboard/summary`、`/v1/dashboard/errors`）
- ✅ **ResponseListPage**: API連携実装済み（`/v1/responses`、CSVエクスポート機能も実装済み）
- ✅ **LogListPage**: API連携実装済み（`/v1/logs`）
- ✅ **PublicFormViewPage**: 条件分岐適用実装済み（`conditionState`を使用して表示制御）
- ✅ **PublicFormViewPage**: 計算フィールド表示実装済み（`computed`タイプに対応）
- ✅ **FormItemPage**: 条件分岐ルール編集機能実装済み（`ConditionRuleEditor`コンポーネントを使用）
- ✅ **FormPreviewPage**: API連携実装済み（`/v1/forms/{id}`、`/v1/forms/{id}/fields`）
- ✅ **AckViewPage**: API連携実装済み（`/v1/forms/{form_key}/ack`）

#### 実装済み項目（remaining-tasks.mdでは未実装と記載されていたが、実装完了）
- ✅ **SUPP-DISPLAY-MODE-001: 表示モード機能（フロントエンド側）** - 実装完了（2026-01-19）
  - ✅ 公開フォーム: 選択肢表示（label/both/value）の切替UI
  - ✅ 管理画面プレビュー: locale+mode切替機能
  - ⚠️ ACK画面: labelを既定表示（label_snapshot優先）
    - 注: ACK画面は公開画面のため、回答詳細を表示するにはACK APIのレスポンスに回答詳細を含める拡張が必要（将来の対応として記載）

#### 実装済み項目（remaining-tasks.mdでは未実装と記載されていたが、実装完了）
- ✅ **条件分岐UI（F-03/F-05）: 条件分岐ビルダー** - 実装完了（2026-01-19）
  - ✅ 条件分岐ビルダーUI（`ConditionRuleBuilder`コンポーネント）
  - ✅ visibility_rule, required_rule, step_transition_rule の完全な条件分岐ビルダーUI
  - ✅ 複数条件の追加・削除（最大10個）
  - ✅ AND/ORの論理結合を明示的に選択可能
  - ✅ field type × operator 許可表の適用（フィールドタイプに応じて使用可能な演算子を制限）
  - ✅ operator別 value_input UI（between: 最小値/最大値、in: カンマ区切り複数値、その他: 単一値）
  - ✅ バリデーション: 自己参照チェック、フィールド存在チェック
  - 注: 簡易的な条件分岐ルール編集機能（`ConditionRuleUI`）は後方互換性のため保持

#### 未実装項目（remaining-tasks.mdの記載通り）
- なし（全て実装完了）

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

4. ✅ **フォーム一覧の詳細・編集機能**（detail-edit-fields-review.md）- 実装完了（2026-01-18）
   - ✅ 詳細表示に不足項目を追加（通知設定、PDF設定、テーマ設定等）
   - ✅ 編集機能は`FormEditPage`で実装済み（新規作成と編集を同じ画面で実装）

5. ✅ **SUPP-DISPLAY-MODE-001: 表示モード機能（フロントエンド側）**（remaining-tasks.md）- 実装完了（2026-01-19）
   - ✅ 公開フォーム: 選択肢表示（label/both/value）の切替UI
   - ✅ 管理画面プレビュー: locale+mode切替機能
   - ⚠️ ACK画面: labelを既定表示（label_snapshot優先）
     - 注: ACK画面は公開画面のため、回答詳細を表示するにはACK APIのレスポンスに回答詳細を含める拡張が必要（将来の対応として記載）

6. ✅ **条件分岐UI（F-03/F-05）: 条件分岐ビルダー**（remaining-tasks.md）- 実装完了（2026-01-19）
   - ✅ 完全な条件分岐ビルダーUI（`ConditionRuleBuilder`コンポーネント）
   - ✅ 複数条件の追加・削除（最大10個）
   - ✅ AND/ORの論理結合を明示的に選択可能
   - ✅ field type × operator 許可表の適用（フィールドタイプに応じて使用可能な演算子を制限）
   - ✅ operator別 value_input UI（between: 最小値/最大値、in: カンマ区切り複数値、その他: 単一値）
   - ✅ バリデーション: 自己参照チェック、フィールド存在チェック
   - 注: 簡易的な条件分岐ルール編集機能（`ConditionRuleUI`）は後方互換性のため保持

### 実装済み項目（仕様書と一致）

- ✅ CSVインポート機能（csv-import-spec.md）
- ✅ ファイルアップロードのジョブキュー対応（file-upload-queue-spec.md）
- ✅ キューワーカーのsystemdサービス化（queue-worker-systemd-spec.md）
- ✅ アカウント一覧の詳細・編集機能（detail-edit-fields-review.mdの指摘事項は全て実装済み）
- ✅ テーマ一覧の基本機能（詳細・編集・使用状況確認・コピー機能は全て実装済み）
- ✅ 進捗表示コンポーネント（csv-export-progress-flow.md, remaining-tasks.md）
- ✅ テーマ機能の完全実装（公開フォームでのテーマ適用、フォーム編集でのテーマ選択UI）
- ✅ フォーム一覧の詳細・編集機能（detail-edit-fields-review.md）
- ✅ DashboardPage: API連携実装済み（`/v1/dashboard/summary`、`/v1/dashboard/errors`）
- ✅ ResponseListPage: API連携実装済み（`/v1/responses`、CSVエクスポート機能も実装済み）
- ✅ LogListPage: API連携実装済み（`/v1/logs`）
- ✅ PublicFormViewPage: 条件分岐適用実装済み（`conditionState`を使用して表示制御）
- ✅ PublicFormViewPage: 計算フィールド表示実装済み（`computed`タイプに対応）
- ✅ FormItemPage: 条件分岐ルール編集機能実装済み（`ConditionRuleBuilder`コンポーネントを使用、完全な条件分岐ビルダーUI）
- ✅ FormPreviewPage: API連携実装済み（`/v1/forms/{id}`、`/v1/forms/{id}/fields`）
- ✅ AckViewPage: API連携実装済み（`/v1/forms/{form_key}/ack`）

---

## 推奨対応優先度

### 高優先度
1. ✅ **CSVエクスポートのジョブキュー対応**（バックエンド）- 実装完了（2026-01-18）

2. ✅ **進捗表示コンポーネント**（フロントエンド）- 実装完了（2026-01-18）
   - ✅ CSVエクスポート、ファイルアップロード、CSVインポートで共通利用
   - ✅ ユーザー体験の向上に必須

### 中優先度
3. ✅ **フォーム一覧の詳細・編集機能**（フロントエンド）- 実装完了（2026-01-18）
   - ✅ 詳細表示に不足項目を追加
   - ✅ 編集機能は`FormEditPage`で実装済み（新規作成と編集を同じ画面で実装）

4. ✅ **テーマ機能の完全実装**（フロントエンド）- 実装完了（2026-01-18）
   - ✅ 使用状況確認とコピー機能の追加（実装済み）
   - ✅ 公開フォームでのテーマ適用（実装済み）
   - ✅ フォーム編集でのテーマ選択UI（実装済み）

5. ✅ **SUPP-DISPLAY-MODE-001: 表示モード機能**（フロントエンド）- 実装完了（2026-01-19）
   - ✅ 公開フォーム: 選択肢表示（label/both/value）の切替UI
   - ✅ 管理画面プレビュー: locale+mode切替機能
   - ⚠️ ACK画面: labelを既定表示（label_snapshot優先）
     - 注: ACK画面は公開画面のため、回答詳細を表示するにはACK APIのレスポンスに回答詳細を含める拡張が必要（将来の対応として記載）

6. ✅ **条件分岐UI（F-03/F-05）: 条件分岐ビルダー**（フロントエンド）- 実装完了（2026-01-19）
   - ✅ 完全な条件分岐ビルダーUI（`ConditionRuleBuilder`コンポーネント）
   - ✅ 複数条件の追加・削除（最大10個）
   - ✅ AND/ORの論理結合を明示的に選択可能
   - ✅ field type × operator 許可表の適用（フィールドタイプに応じて使用可能な演算子を制限）
   - ✅ operator別 value_input UI（between: 最小値/最大値、in: カンマ区切り複数値、その他: 単一値）
   - ✅ バリデーション: 自己参照チェック、フィールド存在チェック
   - 注: 簡易的な条件分岐ルール編集機能（`ConditionRuleUI`）は後方互換性のため保持

---

## 補足

- `remaining-tasks.md`の記載内容と実際の実装に一部乖離があるため、定期的な見直しを推奨
- 仕様書の更新時は、実装状況も同時に確認すること
