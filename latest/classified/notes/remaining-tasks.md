# ReForma 残タスク一覧

**作成日**: 2026-01-16  
**最終更新**: 2026-01-23（実装状況を確認・更新）  
**補足**: フォームの回答日時（submitted_at）をマイクロ秒まで対応（submissionsテーブルのcreated_at/updated_atをtimestamp(6)に変更）  
**ベース**: reforma-notes-v1.1.0.md の内容と実装状況の照合結果

---

## ドキュメント構成

### 分類別仕様書（classified/）
- **api**: `reforma-api-spec-v0.1.8.md` - API仕様（OpenAPI準拠、多言語対応、条件分岐スキーマ）
- **backend**: `reforma-backend-spec-v0.1.1.md` - バックエンド仕様（Laravel 12）
- **common**: `reforma-common-spec-v1.5.1.md` - 共通仕様（日時・タイムゾーン、進捗表示、Toast表示優先順位）
- **db**: `reforma-db-spec-v0.1.2.md` - DB仕様（テーブル定義、マイグレーション）
- **frontend**: `reforma-frontend-spec-v0.1.1.md` - フロントエンド仕様（React、UI規約、画面仕様）
- **notes**: `reforma-notes-v1.1.0.md` - 補足仕様（実装詳細、追補パッチ）

### 正本仕様書（canonical/）
- **reforma-spec-v0.1.6.md** - 統合版正本仕様書（全分類を統合）
- **reforma-openapi-v0.1.8.yaml/json** - OpenAPI定義（正本）

### その他
- **README.md** - リポジトリ説明、運用ルール
- **CHANGELOG.md** - 変更履歴

---

## 実装済み機能

✅ **添付ファイル機能**
- PDFテンプレートアップロード・管理
- アップロードファイル管理
- PDF生成（pdf_block_key, pdf_page_number対応、複数ページ対応）

✅ **通知機能**
- ユーザー通知（メール送信、CC/BCC対応）
- 管理者通知（複数管理者選択）
- メールテンプレート変数展開
- キュー処理による非同期送信

✅ **期間チェック機能**
- 公開期間チェック（public_period_start, public_period_end）
- 回答期間チェック（answer_period_start, answer_period_end）

✅ **Settings管理**
- Settingsテーブル・モデル実装
- SettingsService実装
- Settings API（GET/PUT /v1/system/settings）

✅ **Root-only機能**
- Root-only middleware実装
- Root-only API保護

✅ **CSVエクスポート基盤**
- CSVエクスポートジョブ開始API
- 進捗管理機能

✅ **検索機能基盤**
- 横断検索API（ユーザー、ログ）

---

## 完了済みタスク

### ✅ A-01: CSVエクスポート機能の完全実装
**完了日**: 2026-01-16  
**実装内容**:
- value/label/bothモード対応
- 共通カラム定義（submission_id, submitted_at, form_code, status）
- フィールド列命名規則（f:{field_key}, f:{field_key}__label）
- フィールドタイプ別の値・ラベル変換ルール
- UTF-8 BOM対応
- RFC4180準拠のエスケープ処理

**参照**: reforma-notes-v1.1.0.md A-01_csv_column_definition

---

### ✅ A-02: 検索機能の完全実装（Submissions検索）
**完了日**: 2026-01-17  
**実装内容**:
- Submissions/Responsesの検索機能
- フィールドタイプ別検索演算子:
  - text/textarea/email/tel: contains
  - number: eq, min, max, between
  - date/datetime: from, to, between
  - select/radio: eq, in
  - checkbox: any_in (default), all_in (optional)
  - terms: eq
- 検索条件のAND結合（デフォルト）
- SQLiteとMySQLの両方で動作するJSON_EXTRACTベースの検索実装

**参照**: reforma-notes-v1.1.0.md A-02_search_rule_matrix

---

### ✅ A-05: 通知再送機能
**完了日**: 2026-01-16  
**実装内容**:
- system_adminがトリガー可能な通知再送API
- キュー処理による非同期送信
- 監査ログ記録（admin_audit_logs）

**参照**: reforma-notes-v1.1.0.md A-05_examples.notification_resend_example

---

### ✅ A-05: PDF再生成機能
**完了日**: 2026-01-16  
**実装内容**:
- デフォルトでは再生成禁止（409エラー）
- system_adminまたはroot-onlyで明示的な操作のみ許可
- 監査ログ記録
- 非同期処理（キュー）

**参照**: reforma-notes-v1.1.0.md A-05_examples.pdf_regeneration_example

---

### ✅ A-06: 条件分岐評価機能
**完了日**: 2026-01-16  
**実装内容**:
- ConditionEvaluatorサービスの実装
- visibility_rule, required_rule, step_transition_ruleの評価
- ConditionStateレスポンス生成（FieldConditionState, StepTransitionState）
- 安全側フォールバック（評価不能時はhide/not_required/deny_transition）
- 最大ネスト1段の制限
- 公開フォームGET、submit、step遷移時の評価

**参照**: 
- reforma-notes-v1.1.0.md A-06_condition_branch_rules
- reforma-notes-v1.1.0.md API 評価フロー
- reforma-notes-v1.1.0.md reforma-notes-v1.0.0-条件分岐-評価結果IF-.json

---

### ✅ SUPP-COMPUTED-001: 計算フィールド機能
**完了日**: 2026-01-17  
**実装内容**:
- form_fieldsテーブルにcomputed_ruleカラム追加（JSON）
- computed型フィールドの定義
- built_in_functions実装（sum, multiply, tax, round, min, max, if）
- ComputedEvaluatorサービスの実装
- 循環検出（max_dependency_depth=1）
- submit時のAPI再計算（クライアント送信値は信用しない）
- エラー時はblank表示、do_not_store

**参照**: reforma-notes-v1.1.0.md reforma-notes-v1.0.0-追補パッチ-表示モード-テーマ-計算フィールド-.json SUPP-COMPUTED-001

---

### ✅ Settings Key Catalog: 初期データ投入
**完了日**: 2026-01-16  
**実装内容**:
- settings-key-catalog.jsonに定義された全キーのシーダー作成
- 認証関連設定（PAT TTL、ローリング延長、パスワードポリシー、ロックポリシー、セッションTTL）
- トークン関連設定（confirm_submission, ack_action, view_pdf）
- 管理アカウント招待設定（TTL、レート制限）
- PDF関連設定（ストレージドライバ、再生成許可）
- キュー関連設定（ドライバ、リトライ設定）

**参照**: reforma-notes-v1.1.0.md reforma-notes-v1.0.0-settings-key-catalog.json

---

### ✅ フロントエンド調整: S-02アカウント一覧の完成（バックエンド）
**完了日**: 2026-01-17（確認）  
**実装内容**:
- GET /v1/system/admin-usersのパラメータ対応:
  - page, per_page: 必須パラメータとして実装済み
  - sort: enum定義（created_at_desc, created_at_asc）対応済み
  - q: キーワード検索（名前・メール）対応済み
  - role: ロールフィルタ対応済み
  - status: ステータスフィルタ対応済み

**参照**: reforma-notes-v1.1.0.md reforma-notes-v1.1.0.txt

---

### ✅ フロントエンド調整: 進捗表示機能の拡張（バックエンド）
**完了日**: 2026-01-17（確認）  
**実装内容**:
- GET /v1/progress/{job_id}で進捗情報を提供:
  - percent: 進捗率（0-100）
  - status: ジョブステータス
  - message: 進捗メッセージ
  - download_url: ダウンロードURL（完了時）
  - expires_at: 有効期限
  - download_expires_at: ダウンロード有効期限

**参照**: reforma-notes-v1.1.0.md reforma-notes-v1.1.0.txt

---

### ✅ SUPP-DISPLAY-MODE-001: 表示モード機能
**完了日**: 2026-01-17  
**実装内容**:
- POST /v1/forms/{form_key}/submitにlocale, modeパラメータ追加（実装済み）
- ラベルスナップショット保存ロジックの改善（locale対応）
  - フィールドラベルのlocale別取得（getFieldLabelSnapshot）
  - 選択肢ラベルのlocale別取得（extractLabelFromOptions）
- submission_valuesテーブルのlabel_json, field_label_snapshotカラムは既に存在
- CSVエクスポート時のmode指定対応（既に実装済み）
- テスト追加（ラベルスナップショット保存、locale別ラベル取得）

**参照**: reforma-notes-v1.1.0.md reforma-notes-v1.0.0-追補パッチ-表示モード-テーマ-計算フィールド-.json SUPP-DISPLAY-MODE-001

---

### ✅ フォームの回答日時をマイクロ秒まで対応
**完了日**: 2026-01-17  
**実装内容**:
- submissionsテーブルのcreated_at, updated_atをマイクロ秒対応に変更
  - MySQL: timestamp(6)に変更
  - SQLite: datetime型はデフォルトでマイクロ秒をサポート
- CSVエクスポート時のtoISOString()は既にマイクロ秒を含む

**参照**: マイグレーション: 2026_01_17_033629_add_microseconds_to_submissions_table.php

---

### ✅ SUPP-THEME-001: テーマ機能
**完了日**: 2026-01-17  
**実装内容**:
- themesテーブルの作成
- formsテーブルにtheme_id, theme_tokensカラム追加
- テーマ管理API（System Admin以上）:
  - GET/POST/PUT/DELETE /v1/system/themes
  - GET /v1/system/themes/{id}/usage（使用状況確認）
  - POST /v1/system/themes/{id}/copy（テーマコピー）
- フォームへのテーマ適用（Form Admin以上）:
  - GET/PUT /v1/forms/{id}にテーマ情報を追加
  - GET /v1/public/forms/{form_key}にテーマ情報を追加
- テーマ解決ロジック（デフォルトテーマのフォールバック）
- プリセットテーマのシーダー（default, dark, minimal）
- 権限チェック（System Admin / Form Admin / root-only）
- テーマトークンのバリデーション
- テスト実装（11テスト、46アサーション）

**参照**: 
- reforma-notes-v1.1.0.md reforma-notes-v1.0.0-追補パッチ-表示モード-テーマ-計算フィールド-.json SUPP-THEME-001
- SUPP-THEME-001-spec.md

---

### ✅ フロントエンド調整: ログイン/ログアウト周りのAPI連携実装
**完了日**: 2026-01-17  
**実装内容**:
- AuthContext.tsx: POST /v1/auth/login API連携実装
- AuthContext.tsx: GET /v1/auth/me API連携実装（アプリ起動時・リロード時のセッション確認）
- AuthContext.tsx: POST /v1/auth/logout API連携実装
- LoginPage.tsx: API連携に置き換え、エラーハンドリング追加、ログイン成功時のToast表示
- LogoutPage.tsx: API連携に置き換え
- RequireAuth.tsx: loading状態を考慮（セッション確認中はリダイレクトしない）
- APIレスポンスのuserオブジェクトをフロントエンドのUser型に変換するmapApiUserToUser関数を追加

**参照**: 
- reforma-api-spec-v0.1.8.md（POST /v1/auth/login, GET /v1/auth/me, POST /v1/auth/logout）

---

### ✅ エラーメッセージの多言語対応（バックエンド）
**完了日**: 2026-01-17  
**実装内容**:
- `lang/ja/messages.php`と`lang/en/messages.php`の作成
- エラーメッセージの翻訳キー定義（全メッセージを翻訳キーに置き換え）
- ApiResponseクラスにロケール取得機能を追加
  - ロケール取得の優先順位:
    1. リクエストパラメータの`locale`（最優先）
    2. `Accept-Language`ヘッダー
    3. デフォルト（日本語）
  - 翻訳キー形式（`messages.xxx`）の自動翻訳機能
  - 置換パラメータ対応（`:count`, `:error`, `:fields`など）
- 全コントローラーのハードコードされたメッセージを翻訳キーに置き換え
  - PublicFormsController, FormsController, ThemesController
  - ResponsesNotificationController, ResponsesPdfRegenerateController
  - AdminUsersController, ResponsesExportController
  - FormsFieldsController, AuthController
  - RolesPermissionsController, SettingsController
  - ResponsesController, ResponsesPdfController
- テスト確認（全て通過）

**参照**: 
- 実装: `app/Support/ApiResponse.php`
- 翻訳ファイル: `lang/ja/messages.php`, `lang/en/messages.php`

---

## 未実装・要対応タスク（バックエンド）

### 1. ジョブキュー処理のsystemdサービス化
**現状**: ジョブクラスは実装済み、systemdサービス化は完了  
**優先度**: 高（本番環境で必須）

**実装済み**:
- ✅ `GeneratePdfJob`: PDF生成ジョブ（タイムアウト300秒、試行3回、`pdfs`キュー）
- ✅ `SendFormSubmissionNotificationJob`: フォーム送信通知ジョブ（タイムアウト300秒、試行3回、`notifications`キュー）
- ✅ キュー設定: `database`接続、`failed_jobs`テーブル
- ✅ systemdサービスファイル（`reforma-queue-worker@.service`）の作成
- ✅ キュー分離戦略（`notifications`, `pdfs`）
- ✅ README.mdにキューワーカー管理手順を追加

**未実装**:
- ❌ CSVエクスポートのジョブキュー対応（現在は同期処理）

**参照**: 
- `queue-worker-systemd-spec.md`（詳細仕様）
- `queue-worker-operation-flow.md`（動作イメージ）
- Laravel Queue Documentation

---

### ✅ 1-1. CSVエクスポートのジョブキュー対応
**完了日**: 2026-01-17  
**実装内容**:
- ✅ `ExportCsvJob`ジョブクラスの作成（タイムアウト600秒、試行2回、`exports`キュー）
- ✅ `ResponsesExportController::startCsv()`の修正（ジョブ投入に変更）
- ✅ 翻訳メッセージの追加（`csv_export_queued`, `csv_export_generating`, `csv_export_saving`）
- ✅ 進捗表示対応（0% → 50% → 100%）
- ✅ README.mdの更新（exportsキュー用ワーカーの起動方法）

**参照**: 
- `csv-export-queue-spec.md`（詳細仕様）
- `csv-export-progress-flow.md`（進捗表示フロー）

---

### ✅ 1-2. ファイルアップロード・CSVインポートのジョブキュー対応
**完了日**: 2026-01-17  
**実装内容**:

**ファイルアップロード**:
- ✅ `ProcessFileUploadJob`ジョブクラスの作成（タイムアウト300秒、試行2回、`uploads`キュー）
- ✅ PDFテンプレートアップロードを非同期処理に変更
- ✅ 添付ファイルアップロードを非同期処理に変更（複数ファイル対応）
- ✅ 進捗表示対応（0% → 30% → 60% → 90% → 100%）
- ✅ 元のファイル名を保持する機能

**CSVインポート**:
- ✅ `CsvImportService`の作成（CSV解析・検証・インポート）
- ✅ `ImportCsvJob`ジョブクラスの作成（タイムアウト1800秒、試行1回、`imports`キュー）
- ✅ 選択肢インポート（`options`タイプ）: 既存フィールドの選択肢を追加・更新
- ✅ 項目全体インポート（`fields`タイプ）: フォーム項目全体を一括置き換え
- ✅ `POST /v1/forms/{id}/fields/import/csv`エンドポイント追加（`type`パラメータでタイプ指定）
- ✅ 進捗表示対応（選択肢: 0% → 10% → 20% → 40% → 100%、項目全体: 0% → 10% → 20% → 40% → 60% → 100%）
- ✅ エラーレポート機能（失敗した行の情報を返却）
- ✅ ルールバリデーション（項目全体インポート時）
- ✅ トランザクション処理（データ整合性保証）

**データベース変更**:
- ✅ `progress_jobs`テーブルに`result_data`カラム追加（JSON形式、CSVインポート結果の詳細情報を保存）

**テスト**:
- ✅ `FileUploadQueueTest`: ファイルアップロードのテスト（4テスト、27アサーション）
- ✅ `CsvImportQueueTest`: CSVインポートのテスト（5テスト、35アサーション）
- ✅ `FormsAttachmentApiTest`: 既存テストの更新（非同期処理対応）

**参照**: 
- `file-upload-queue-spec.md`（詳細仕様）
- `csv-import-spec.md`（CSVインポート詳細仕様）

---

## 未実装・要対応タスク（フロントエンド）

### ✅ 0. BASIC認証対応（環境変数設定）
**完了日**: 2026-01-17  
**優先度**: 中（ステージング環境等でBASIC認証が必要な場合のみ）

**実装内容**:
- ✅ `apiFetch.ts`: BASIC認証ヘッダー自動追加機能（環境変数から取得）
- ✅ `env.ts`: `envString`関数を使用して環境変数を取得
- ✅ 環境変数が設定されていない場合はBASIC認証なしで動作

**環境変数設定**:
- `.env.staging`または`.env.production`に以下を設定:
  - `VITE_API_BASIC_AUTH_USER`: BASIC認証のユーザー名
  - `VITE_API_BASIC_AUTH_PASS`: BASIC認証のパスワード
- 開発環境では環境変数を設定しない（BASIC認証なしで動作）
- 本番環境では通常、BASIC認証は不要（または別の認証方式を使用）

**参照**: 
- `apache-basic-auth-config.md`（Apache設定とフロントエンド対応手順）
- `src/utils/apiFetch.ts`（BASIC認証ヘッダー自動追加機能は実装済み）

---

### ✅ 1. SUPP-DISPLAY-MODE-001: 表示モード機能（フロントエンド側）
**完了日**: 2026-01-19  
**優先度**: 中

**バックエンド実装済み**:
- ✅ submission_valuesテーブルにlabel_json, field_label_snapshotカラム追加（既存）
- ✅ POST /v1/forms/{form_key}/submitにlocale, modeパラメータ追加（実装済み）
- ✅ label/both/valueモード対応（実装済み）
- ✅ 保存の正はvalue、labelはスナップショット（実装済み）
- ✅ ラベルスナップショット保存ロジックの改善（locale対応）
- ✅ CSVエクスポート時のmode指定対応（既に実装済み）

**フロントエンド実装内容**:
- ✅ 公開フォーム: 選択肢表示（label/both/value）の切替UI（`PublicFormViewPage.tsx`）
- ✅ 管理画面プレビュー: locale+mode切替機能（`FormPreviewPage.tsx`）
- ⚠️ ACK画面: labelを既定表示（label_snapshot優先）
  - 注: ACK画面は公開画面のため、回答詳細を表示するにはACK APIのレスポンスに回答詳細を含める拡張が必要（将来の対応として記載）

**実装詳細**:
- 公開フォーム（U-01）: 選択肢フィールド（select/radio/checkbox）の表示モード切替UIを追加
  - 表示モード: label（ラベルのみ）、both（値とラベル）、value（値のみ）
  - 選択肢フィールドがある場合のみ表示モード切替UIを表示
- フォームプレビュー（F-04）: locale+mode切替UI追加
  - ロケール切替: フォームの翻訳ロケールを選択可能
  - 表示モード切替: label/both/valueを選択可能
- ACK画面（A-03）: label_snapshot優先表示
  - 将来の拡張: ACK APIのレスポンスに回答詳細を含める拡張が必要

**参照**: 
- reforma-notes-v1.1.0.md SUPP-DISPLAY-MODE-001
- reforma-notes-v1.0.0-追補パッチ-表示モード-テーマ-計算フィールド-.json

---

### ✅ 2. SUPP-THEME-001: テーマ機能（フロントエンド側）
**完了日**: 2026-01-23（確認）  
**優先度**: 中

**バックエンド実装済み**:
- ✅ themesテーブルの作成
- ✅ formsテーブルにtheme_id, theme_tokensカラム追加
- ✅ テーマ管理API（System Admin以上）:
  - GET/POST/PUT/DELETE /v1/system/themes
  - GET /v1/system/themes/{id}/usage（使用状況確認）
  - POST /v1/system/themes/{id}/copy（テーマコピー）
- ✅ フォームへのテーマ適用（Form Admin以上）:
  - GET/PUT /v1/forms/{id}にテーマ情報を追加
  - GET /v1/public/forms/{form_key}にテーマ情報を追加
- ✅ テーマ解決ロジック（デフォルトテーマのフォールバック）
- ✅ プリセットテーマのシーダー（default, dark, minimal）
- ✅ 権限チェック（System Admin / Form Admin / root-only）
- ✅ テーマトークンのバリデーション
- ✅ テスト実装（11テスト、46アサーション）

**フロントエンド実装済み**:
- ✅ 公開フォーム表示時に`theme_id`と`theme_tokens`を取得
- ✅ `theme_tokens`をCSS変数に展開（フォームコンテナ配下）
- ✅ テーマ管理画面（System Admin用、S-03）
- ✅ フォーム編集（F-02）: テーマ選択UI追加（theme_id選択、theme_tokensカスタマイズ）

**実装詳細**:
- `PublicFormViewPage.tsx`でテーマトークンの適用を実装
- `FormEditIntegratedPage.tsx`でテーマ選択UIを実装
- `ThemeListPage.tsx`でテーマ管理画面を実装

**参照**: 
- reforma-notes-v1.1.0.md SUPP-THEME-001
- SUPP-THEME-001-spec.md
- reforma-notes-v1.0.0-追補パッチ-表示モード-テーマ-計算フィールド-.json

---

### ✅ 3. フロントエンド調整: エラー構造の統一
**完了日**: 2026-01-17  
**優先度**: 高

**バックエンド実装状況**:
- ✅ ApiResponseクラスで統一されたenvelope形式を使用（success, data, message, errors, code, request_id）
- ✅ ApiErrorCode enumでエラーコードを定義
- ✅ root-only拒否時には`errors.reason=ROOT_ONLY`を使用（AdminUsersController、ThemesController）
- ✅ エラーメッセージの多言語対応（完全実装済み）

**フロントエンド実装内容**:
- ✅ エラーコード定義（`src/utils/errorCodes.ts`）: ApiErrorCode enum、ApiErrorResponse型、extractToastMessage関数
- ✅ Toastコンポーネント（`src/components/Toast.tsx`）: 右上固定表示、スタック表示、フェードイン/アウト
- ✅ ToastContext（`src/ui/ToastContext.tsx`）: 重複抑制（1秒以内）、グローバル参照設定
- ✅ apiFetch.ts改修: エラーレスポンス解析とToast表示の優先順位実装（message → errors.reason → code）
- ✅ エラーハンドリング分岐:
  - 401/419: セッション無効 → /logout?reason=session_invalid
  - 403: 権限エラー → /error?code=FORBIDDEN&reason=...
  - 400/409/422: Toast表示
  - 500/503: Toast表示 + エラーページ遷移
- ✅ ServerErrorWatcher: 500/503エラー時のエラーページ遷移
- ✅ App.tsxにToastProvider追加

**実装詳細**:
- Toast表示の優先順位: `extractToastMessage`関数で実装（共通仕様v1.5.1準拠）
- 重複抑制: 同一メッセージ+同一タイプを1秒以内に抑制（最新のみ表示）
- 右上固定表示: `fixed top-4 right-4 z-50`
- スタック表示: 複数メッセージを縦に並べて表示
- エラーコード定義: TypeScript enumで定義（バックエンドのApiErrorCodeと対応）

**参照**: 
- reforma-common-spec-v1.5.1.md（Toast表示優先順位）
- reforma-notes-v1.1.0.md エラー設計
- reforma-frontend-spec-v0.1.1.md（エラーハンドリング）

---

### ✅ 4. 条件分岐UI（F-03/F-05）: 条件分岐ビルダー
**完了日**: 2026-01-19  
**優先度**: 中

**バックエンド実装済み**:
- ✅ ConditionEvaluatorサービスの実装
- ✅ visibility_rule, required_rule, step_transition_ruleの評価
- ✅ ConditionStateレスポンス生成
- ✅ 安全側フォールバック

**フロントエンド実装内容**:
- ✅ F-03（フォーム項目設定）: 条件分岐ビルダーUI（`ConditionRuleBuilder`コンポーネント）
  - ✅ visibility_rule, required_rule, step_transition_rule の完全な条件分岐ビルダーUI
- ✅ 条件分岐ビルダー: field type × operator 許可表の適用
  - ✅ フィールドタイプに応じて使用可能な演算子を動的に制限
  - ✅ `FIELD_TYPE_OPERATORS`マップでフィールドタイプごとの許可演算子を定義
- ✅ 条件分岐ビルダー: operator別 value_input UI
  - ✅ between: 最小値/最大値の2つの入力フィールド
  - ✅ in: カンマ区切りで複数値を入力可能
  - ✅ exists/not_empty/empty: 値入力不要
  - ✅ その他: フィールドタイプに応じた入力タイプ（number, date, time, datetime-local, text）

**実装詳細**:
- 条件分岐ビルダー: row = field_selector / operator_selector / value_input
  - フィールド選択: 自己参照を除外したフィールドリスト
  - 演算子選択: フィールドタイプに応じて使用可能な演算子を動的にフィルタリング
  - 値入力: 演算子に応じた適切な入力UI
- 論理結合: AND/OR明示（複数条件がある場合のみ表示）
  - AND: すべての条件を満たす必要がある
  - OR: いずれかの条件を満たせば良い
- 条件数制限: max_conditions=10（実装済み）
- バリデーション:
  - ✅ field_required: フィールド選択が必須
  - ✅ type_match: フィールドタイプに応じた演算子制限
  - ✅ no_self_reference: 自己参照を除外（フィールド選択時に除外、保存時にチェック）
- ネスト制限: max_nesting=1（v1.x制限）
  - 注: 現在の実装では単一レベルのAND/ORのみサポート（ネストは未実装、将来の拡張として記載）

**参照**: 
- reforma-frontend-spec-v1.0.0-condition-ui-.json
- reforma-frontend-spec-v1.0.0-condition-operator-matrix-ui-.json
- reforma-frontend-spec-v1.0.0-condition-ui-examples-.json
- form-feature-attachments-v1.1.json A-06

---

### ✅ 5. 公開フォーム（U-01）: 条件分岐適用
**完了日**: 2026-01-23（確認）  
**優先度**: 高

**バックエンド実装済み**:
- ✅ GET /v1/public/forms/{form_key}でConditionStateを返す
- ✅ POST /v1/forms/{form_key}/submitでConditionStateを評価
- ✅ 安全側フォールバック

**フロントエンド実装済み**:
- ✅ ConditionStateの適用（fields.visible/required/store）
- ✅ 非表示フィールドの非表示処理
- ✅ 必須解除の適用
- ✅ STEP遷移時の条件チェック（422エラー表示）

**実装詳細**:
- `PublicFormViewPage.tsx`でConditionStateの適用を実装
- フィールド表示制御、必須制御、STEP遷移制御を実装
- エラー表示（422 STEP_TRANSITION_DENIED）を実装

**参照**: 
- reforma-notes-v1.0.0-条件分岐-評価結果IF-.json
- reforma-api-spec-v0.1.8.md（ConditionStateスキーマ）

---

### 6. 計算フィールド機能（フロントエンド側）
**現状**: バックエンド側は完全実装済み、フロントエンド側は未実装  
**優先度**: 低

**バックエンド実装済み**:
- ✅ form_fieldsテーブルにcomputed_ruleカラム追加
- ✅ ComputedEvaluatorサービスの実装
- ✅ built_in_functions実装（sum, multiply, tax, round, min, max, if）
- ✅ 循環検出（max_dependency_depth=1）
- ✅ submit時のAPI再計算

**フロントエンド未実装**:
- ❌ 計算フィールドのreadonly表示
- ❌ 依存フィールド変更時の再計算（UX向上）
- ❌ エラー時のblank表示

**実装要件**:
- 計算フィールド: readonly入力欄として表示
- 即時計算: 依存フィールド変更時に再計算して表示（UX向上）
- エラー処理: 計算エラー時はblank表示、do_not_store

**参照**: 
- reforma-notes-v1.1.0.md SUPP-COMPUTED-001
- reforma-notes-v1.0.0-追補パッチ-表示モード-テーマ-計算フィールド-.json

---

## 画面実装状況（中身の実装が未完了）

### ✅ S-01: システム管理ダッシュボード
**完了日**: 2026-01-23（確認）  
**優先度**: 中

**実装済み機能**:
- ✅ GET /v1/dashboard/summary: ロール別の統計情報取得・表示
- ✅ GET /v1/dashboard/errors: エラー情報取得・表示
- ✅ ロール別のブロック表示（system_admin, form_admin, operator, viewer）

**実装詳細**:
- `DashboardPage.tsx`でAPI連携を実装
- ロール別の表示制御を実装（useHasRoleフックを使用）
- エラー一覧のページネーション対応

**参照**: reforma-api-spec-v0.1.8.md

---

### ✅ F-01: フォーム一覧
**完了日**: 2026-01-23（確認）  
**優先度**: 高

**実装済み機能**:
- ✅ GET /v1/forms: フォーム一覧取得・表示
- ✅ ページネーション（page, per_page）
- ✅ ソート機能（created_at_desc, created_at_asc）
- ✅ 検索・フィルタ機能（キーワード検索、ステータスフィルタ）
- ✅ フォーム作成（POST /v1/forms）
- ✅ フォーム削除（DELETE /v1/forms/{id}）
- ✅ フォーム詳細表示（GET /v1/forms/{id}）
- ✅ フォーム編集（PUT /v1/forms/{id}）
- ✅ フォームプレビュー（F-04）への遷移

**実装詳細**:
- `FormListPage.tsx`でAPI連携を実装
- フォーム詳細取得・編集・プレビュー遷移を実装

**参照**: reforma-api-spec-v0.1.8.md

---

### ✅ F-02: フォーム編集
**完了日**: 2026-01-23（確認）  
**優先度**: 高

**実装済み機能**:
- ✅ GET /v1/forms/{id}: フォーム情報取得・表示
- ✅ PUT /v1/forms/{id}: フォーム情報更新
- ✅ テーマ選択UI（theme_id選択、theme_tokensカスタマイズ）
- ✅ フォーム基本情報の編集（name, code, description等）
- ✅ 通知設定、PDF設定等の編集
- ✅ ファイルアップロードの進捗表示（POST /v1/forms/{id}/attachment/pdf-template, POST /v1/forms/{id}/attachment/files）
  - ✅ 進捗表示（GET /v1/progress/{job_id}）
  - ✅ 非同期処理対応（0% → 30% → 60% → 90% → 100%）

**実装詳細**:
- `FormEditIntegratedPage.tsx`でAPI連携を実装
- `ProgressDisplay`コンポーネントを使用した進捗表示を実装
- テーマ選択UI、フォーム基本情報編集、通知設定編集を実装

**参照**: 
- reforma-api-spec-v0.1.8.md
- SUPP-THEME-001-spec.md
- file-upload-queue-spec.md（ファイルアップロード詳細仕様）

---

### F-03: フォーム項目設定
**現状**: 画面レイアウトのみ実装、API連携未実装  
**優先度**: 高

**未実装機能**:
- ❌ GET /v1/forms/{id}/fields: フィールド一覧取得・表示
- ❌ PUT /v1/forms/{id}/fields: フィールド更新
- ❌ 条件分岐ビルダーUI（visibility_rule, required_rule）
- ❌ フィールド追加・削除・並び替え
- ❌ フィールドタイプ別の設定UI
- ❌ CSVインポート機能（POST /v1/forms/{id}/fields/import/csv）
  - 選択肢インポート（`type=options`）
  - 項目全体インポート（`type=fields`）
  - 進捗表示（GET /v1/progress/{job_id}）
  - エラーレポート表示（result_data.errors）

**実装要件**:
- APIからフィールド一覧を取得して表示
- 条件分岐ビルダー実装（別タスク参照）
- フィールド編集フォーム
- CSVインポートUI（ファイルアップロード、タイプ選択、進捗表示、エラーレポート）

**参照**: 
- reforma-api-spec-v0.1.8.md
- reforma-frontend-spec-v1.0.0-condition-ui-.json
- csv-import-spec.md（CSVインポート詳細仕様）

---

### ✅ F-04: フォームプレビュー
**完了日**: 2026-01-23（確認）  
**優先度**: 中

**実装済み機能**:
- ✅ GET /v1/forms/{id}: フォーム情報取得（form.codeを取得）
- ✅ GET /v1/public/forms/{form_code}: 公開フォームAPIからフォーム情報取得・表示
- ✅ 公開フォーム（U-01）と同じレンダリングロジック
- ✅ プレビュー専用のread-only表示（送信ボタンはdisabled）

**実装詳細**:
- `FormPreviewPage.tsx`でAPI連携を実装
- 公開フォームと同じレンダリングロジックを使用
- 条件分岐評価、テーマ適用、カスタムスタイル適用を実装

**参照**: 
- reforma-api-spec-v0.1.8.md
- SUPP-DISPLAY-MODE-001

---

### ✅ R-01: 回答一覧
**完了日**: 2026-01-23（確認）  
**優先度**: 高

**実装済み機能**:
- ✅ 画面レイアウト（テーブル表示、ローディングスピナー）
- ✅ インラインローディングパターン（チラつき防止）
- ✅ GET /v1/responses: 回答一覧取得・表示
- ✅ ページネーション（page, per_page）
- ✅ ソート機能
- ✅ 検索・フィルタ機能（フォーム別、ステータス別等）
- ✅ CSVエクスポート（POST /v1/responses/export/csv）
- ✅ CSVエクスポートの進捗表示（GET /v1/progress/{job_id}）
  - ✅ 進捗バー表示（0% → 30% → 50% → 80% → 100%）
  - ✅ 完了時のダウンロードURL表示（GET /v1/exports/{job_id}/download）
  - ✅ 有効期限表示（download_expires_at）
  - ✅ エラー時のエラーメッセージ表示

**実装詳細**:
- `ResponseListPage.tsx`でAPI連携を実装
- `ProgressDisplay`コンポーネントを使用した進捗表示を実装
- ポーリング間隔: 2秒（実行中）、完了/失敗時は停止

**参照**: 
- reforma-api-spec-v0.1.8.md
- reforma-notes-v1.1.0.md A-01_csv_column_definition
- csv-export-queue-spec.md（CSVエクスポート詳細仕様）
- csv-export-progress-flow.md（進捗表示フロー）

---

### ✅ R-02: 回答詳細
**完了日**: 2026-01-23（確認）  
**優先度**: 高

**実装済み機能**:
- ✅ GET /v1/responses/{id}: 回答詳細取得・表示
- ✅ フィールドスナップショット表示（label_snapshot優先）

**実装詳細**:
- `ResponseDetailPage.tsx`でAPI連携を実装
- 回答詳細の取得・表示を実装

**注**: PDF表示・ダウンロード、通知再送、PDF再生成機能は実装状況を要確認

**参照**: 
- reforma-api-spec-v0.1.8.md
- reforma-notes-v1.1.0.md A-05_examples

---

### L-01: ログ一覧
**現状**: 画面レイアウト実装済み、モックデータ使用中、API連携未実装  
**優先度**: 中

**実装済み機能**:
- ✅ 画面レイアウト（テーブル表示、ローディングスピナー）
- ✅ インラインローディングパターン（チラつき防止）

**未実装機能**:
- ❌ GET /v1/logs: ログ一覧取得・表示（現在はモックデータ使用）
- ❌ ページネーション（page, per_page）
- ❌ ソート機能
- ❌ 検索・フィルタ機能（タイプ別、ステータス別等）

**実装要件**:
- APIからログ一覧を取得して表示（モックデータを置き換え）
- ログタイプ別の表示（notification, pdf, ack等）

**参照**: reforma-api-spec-v0.1.8.md

---

### L-02: ログ詳細
**現状**: 画面レイアウトのみ実装、API連携未実装  
**優先度**: 中

**未実装機能**:
- ❌ GET /v1/logs/{id}: ログ詳細取得・表示
- ❌ ログペイロードの詳細表示
- ❌ 関連リソースへのリンク（form_id, response_id等）

**実装要件**:
- APIからログ詳細を取得して表示
- ログタイプ別の詳細表示

**参照**: reforma-api-spec-v0.1.8.md

---

### C-01: 検索
**現状**: 画面レイアウトのみ実装、API連携未実装  
**優先度**: 中

**未実装機能**:
- ❌ GET /v1/search: 横断検索API連携
- ❌ 検索結果の表示（フォーム/回答/ログ）
- ❌ 検索結果からの詳細画面への遷移

**実装要件**:
- APIから検索結果を取得して表示
- 検索結果の種類別表示（kind: response, log, form）
- 検索結果からの詳細画面への遷移

**参照**: reforma-api-spec-v0.1.8.md

---

### ✅ S-02: アカウント一覧
**完了日**: 2026-01-17  
**優先度**: 中

**実装済み機能**:
- ✅ GET /v1/system/admin-users: アカウント一覧取得・表示
- ✅ ページネーション（page, per_page）
- ✅ ソート機能（created_at_desc, created_at_asc）
- ✅ 検索・フィルタ機能（キーワード検索、ロールフィルタ、ステータスフィルタ）
- ✅ POST /v1/system/admin-users: アカウント作成
- ✅ PUT /v1/system/admin-users/{id}: アカウント更新
- ✅ GET /v1/system/admin-users/{id}: アカウント詳細取得
- ✅ POST /v1/system/admin-users/invites/resend: 招待再送
- ✅ 詳細/編集モーダルのチラつき改善（モーダル先開き、インラインスピナー）

**参照**: reforma-api-spec-v0.1.8.md

---

### S-03: テーマ一覧
**現状**: 一部実装済み（一覧・作成・削除は実装済み、詳細・編集・使用状況・コピーは未実装）  
**優先度**: 中

**実装済み機能**:
- ✅ GET /v1/system/themes: テーマ一覧取得・表示
- ✅ ページネーション（page, per_page）
- ✅ ソート機能（created_at_desc, created_at_asc）
- ✅ 検索・フィルタ機能（キーワード検索、プリセットフィルタ、アクティブフィルタ）
- ✅ POST /v1/system/themes: テーマ作成
- ✅ DELETE /v1/system/themes/{id}: テーマ削除
- ✅ インラインローディングパターン（チラつき防止）

**未実装機能**:
- ❌ GET /v1/system/themes/{id}: テーマ詳細取得・表示
- ❌ PUT /v1/system/themes/{id}: テーマ更新
- ❌ GET /v1/system/themes/{id}/usage: 使用状況確認
- ❌ POST /v1/system/themes/{id}/copy: テーマコピー
- ❌ テーマトークンの編集UI

**実装要件**:
- テーマ詳細モーダルまたは詳細ページ
- テーマ編集機能（テーマトークンの編集UI含む）
- 使用状況表示（使用中のフォーム数）
- テーマコピー機能

**参照**: 
- reforma-api-spec-v0.1.8.md
- SUPP-THEME-001-spec.md

---

## 未実装・要対応タスク（API実装済み、フロントエンド未実装）

### システム設定管理画面（新規）
**現状**: API実装済み、フロントエンド未実装  
**優先度**: 低（System Admin機能）

**未実装機能**:
- ❌ GET /v1/system/settings: システム設定取得・表示
- ❌ PUT /v1/system/settings: システム設定更新
- ❌ 設定項目の編集UI（Settings Key Catalogに基づく）

**実装要件**:
- System Admin用のシステム設定管理画面
- 設定項目の編集フォーム（キー・値の編集）
- 設定項目の説明表示

**参照**: 
- reforma-api-spec-v0.1.8.md
- reforma-notes-v1.1.0.md reforma-notes-v1.0.0-settings-key-catalog.json

---

### ロール権限管理画面（新規）
**現状**: API実装済み、フロントエンド未実装  
**優先度**: 低（System Admin機能）

**未実装機能**:
- ❌ GET /v1/system/roles/permissions: ロール権限定義取得・表示
- ❌ PUT /v1/system/roles/permissions: ロール権限定義更新
- ❌ ロール権限の編集UI

**実装要件**:
- System Admin用のロール権限管理画面
- ロール別の権限設定UI

**参照**: reforma-api-spec-v0.1.8.md

---

### 監査ログ一覧画面（新規）
**現状**: API実装済み、フロントエンド未実装  
**優先度**: 低（System Admin機能）

**未実装機能**:
- ❌ GET /v1/system/admin-audit-logs: 監査ログ一覧取得・表示
- ❌ ページネーション（page, per_page）
- ❌ ソート機能
- ❌ 検索・フィルタ機能（ユーザー別、アクション別等）

**実装要件**:
- System Admin用の監査ログ一覧画面
- ログタイプ別の表示

**参照**: reforma-api-spec-v0.1.8.md

---

## 優先度の推奨

### 高優先度
1. **公開フォーム（U-01）: 条件分岐適用**（コア機能、必須）
2. **F-02: フォーム編集のAPI連携**（基本機能、ファイルアップロード進捗表示含む）
3. **F-03: フォーム項目設定のAPI連携**（基本機能、CSVインポート機能含む）
4. **R-01: 回答一覧のAPI連携**（基本機能、CSVエクスポート進捗表示含む、モックデータを置き換え）
5. **R-02: 回答詳細のAPI連携**（基本機能）
6. **進捗表示コンポーネント（共通化）**（CSVエクスポート、ファイルアップロード、CSVインポートで共通利用）

### 中優先度
7. **SUPP-DISPLAY-MODE-001: 表示モード機能**（バックエンド実装済み、フロントのみ）
8. **SUPP-THEME-001: テーマ機能**（バックエンド実装済み、フロントのみ）
9. **条件分岐UI（F-03/F-05）: 条件分岐ビルダー**（管理画面機能）
10. **F-04: フォームプレビューのAPI連携**（管理画面機能）
11. **L-01/L-02: ログ一覧・詳細のAPI連携**（管理画面機能、モックデータを置き換え）
12. **C-01: 検索のAPI連携**（管理画面機能）
13. **S-01: ダッシュボードのAPI連携**（管理画面機能）
14. **S-03: テーマ一覧の完全実装**（詳細・編集・使用状況・コピー機能）

### 低優先度（v2候補）
6. **計算フィールド機能**（バックエンド実装済み、フロントのみ）

---

## フロントエンド実装状況（v0.5.43時点）

### 実装済み機能
- ✅ 認証・認可（AuthContext, RequireAuth, RequireRole）
- ✅ セッション無効時の自動リダイレクト
- ✅ 403エラー（ROOT_ONLY等）の専用処理
- ✅ 共通レイアウト（AppLayout、サイドバー折りたたみ対応）
- ✅ 多言語対応（ja/en、Cookie優先）
- ✅ テーマ切替（light/dark/reforma）
- ✅ Debug UI（VITE_DEBUG=true時）
- ✅ 主要画面実装（A-01, A-02, S-01, S-02, S-03, F-01～F-04, U-01, A-03, R-01, R-02, L-01, L-02, C-01, E-01, N-01）
- ✅ エラー構造の統一（共通仕様v1.5.1準拠のToast表示優先順位実装）
- ✅ BASIC認証対応（環境変数設定、apiFetch.tsでの自動ヘッダー追加）
- ✅ 一覧画面のローディング改善（インラインスピナー、API呼び出し遅延、チラつき防止）
- ✅ モーダルのローディング改善（モーダル先開き、インラインスピナー、チラつき防止）

### 実装済みAPI連携
- ✅ S-01: ダッシュボード（完全実装: GET /v1/dashboard/summary, GET /v1/dashboard/errors）
- ✅ S-02: アカウント一覧（完全実装: GET/POST/PUT/DELETE /v1/system/admin-users, GET /v1/system/admin-users/{id}, POST /v1/system/admin-users/invites/resend）
- ✅ F-01: フォーム一覧（完全実装: GET/POST/DELETE /v1/forms, GET /v1/forms/{id}）
- ✅ F-02: フォーム編集（完全実装: GET/PUT /v1/forms/{id}, ファイルアップロード進捗表示含む）
- ✅ F-04: フォームプレビュー（完全実装: GET /v1/public/forms/{form_code}）
- ✅ R-01: 回答一覧（完全実装: GET /v1/responses, CSVエクスポート進捗表示含む）
- ✅ R-02: 回答詳細（完全実装: GET /v1/responses/{id}）
- ✅ S-03: テーマ一覧（一部実装: GET/POST/DELETE /v1/system/themes）
- ✅ U-01: 公開フォーム（完全実装: GET /v1/public/forms/{form_key}, 条件分岐適用、テーマ適用含む）

### 未実装機能
- ❌ 表示モード機能（SUPP-DISPLAY-MODE-001）- 一部実装済み（ResponseListPageでmode使用）
- ❌ 計算フィールド機能
- ❌ L-01: ログ一覧のAPI連携（モックデータ使用中）

### 新規追加タスク（バックエンド仕様追加に伴う）

#### ✅ 進捗表示コンポーネント（共通化）
**完了日**: 2026-01-23（確認）  
**優先度**: 高（CSVエクスポート、ファイルアップロード、CSVインポートで共通利用）

**実装済み機能**:
- ✅ 進捗表示コンポーネント（ProgressDisplay）
- ✅ GET /v1/progress/{job_id}のポーリング機能
- ✅ 進捗バー表示（percent）
- ✅ ステータス表示（queued, running, succeeded, failed）
- ✅ メッセージ表示（message）
- ✅ 完了時のダウンロードURL表示（download_url）
- ✅ 有効期限表示（download_expires_at, expires_at）
- ✅ エラーレポート表示（result_data.errors）

**実装詳細**:
- `ProgressDisplay.tsx`コンポーネントを実装
- ポーリング間隔: 2秒（実行中）、完了/失敗時は停止
- CSVエクスポート、ファイルアップロード、CSVインポートで共通利用

**参照**: 
- csv-export-progress-flow.md（進捗表示フロー）
- file-upload-queue-spec.md（ファイルアップロード詳細仕様）
- csv-import-spec.md（CSVインポート詳細仕様）

---

## 将来削除予定（互換性のため現状維持）

### roleフィールド（単一）の削除
**現状**: OpenAPI定義・バックエンド・フロントエンドで`deprecated: true`として残置  
**削除予定**: 将来のバージョン（v2.x以降を想定）

**現状の実装**:
- **OpenAPI定義**: `reforma-openapi-v0.1.8.yaml`の`User`スキーマに`role`フィールドが`deprecated: true`として定義
- **バックエンド**: `AuthController.php`で`role => $roleCodes[0] ?? null`として返却（互換性のため）
- **フロントエンド**: `AuthContext.tsx`の`mapApiUserToUser`で`role`をマッピング（互換性のため）

**削除時の対応**:
- OpenAPI定義から`role`フィールドを削除
- バックエンドの`AuthController.php`から`role`フィールドの返却を削除
- フロントエンドの`AuthContext.tsx`から`role`フィールドのマッピングを削除
- フロントエンドの`User`型から`role`フィールドを削除
- `screenRegistry.ts`等で`role`を使用している箇所を`roles[]`に置き換え

**参照**: 
- reforma-openapi-v0.1.8.yaml（240-252行目: `role`フィールドの定義）
- app/Http/Controllers/Api/V1/AuthController.php（83行目: `role`フィールドの返却）

---

## 補足

- 各タスクの詳細仕様は `reforma-notes-v1.1.0.md` を参照
- 実装時は OpenAPI 定義（reforma-openapi-v0.1.8.yaml）も更新すること
- 仕様書への反映も忘れずに実施すること
- フロントエンドの現在のバージョン: **v0.5.16**（2026-01-14）
- デザイン変更は不可（既存デザイン維持）
- 仕様書JSONを正としてUIを自動生成する方針を維持
