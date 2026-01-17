# ReForma 残タスク一覧

**作成日**: 2026-01-16  
**最終更新**: 2026-01-17  
**補足**: フォームの回答日時（submitted_at）をマイクロ秒まで対応（submissionsテーブルのcreated_at/updated_atをtimestamp(6)に変更）  
**ベース**: reforma-notes-v1.1.0.md の内容と実装状況の照合結果

---

## ドキュメント構成

### 分類別仕様書（classified/）
- **api**: `reforma-api-spec-v0.1.4.md` - API仕様（OpenAPI準拠、多言語対応、条件分岐スキーマ）
- **backend**: `reforma-backend-spec-v0.1.1.md` - バックエンド仕様（Laravel 12）
- **common**: `reforma-common-spec-v1.5.1.md` - 共通仕様（日時・タイムゾーン、進捗表示、Toast表示優先順位）
- **db**: `reforma-db-spec-v0.1.1.md` - DB仕様（テーブル定義、マイグレーション）
- **frontend**: `reforma-frontend-spec-v0.1.1.md` - フロントエンド仕様（React、UI規約、画面仕様）
- **notes**: `reforma-notes-v1.1.0.md` - 補足仕様（実装詳細、追補パッチ）

### 正本仕様書（canonical/）
- **reforma-spec-v0.1.6.md** - 統合版正本仕様書（全分類を統合）
- **reforma-openapi-v0.1.4.yaml/json** - OpenAPI定義（正本）

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
- reforma-api-spec-v0.1.4.md（POST /v1/auth/login, GET /v1/auth/me, POST /v1/auth/logout）

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
**現状**: ジョブクラスは実装済み、systemdサービス化は未実装  
**優先度**: 高（本番環境で必須）

**実装済み**:
- ✅ `GeneratePdfJob`: PDF生成ジョブ（タイムアウト300秒、試行3回）
- ✅ `SendFormSubmissionNotificationJob`: フォーム送信通知ジョブ（タイムアウト300秒、試行3回）
- ✅ キュー設定: `database`接続、`failed_jobs`テーブル

**未実装**:
- ❌ systemdサービスファイルの作成
- ❌ ワーカープロセスの管理（起動・停止・再起動）
- ❌ 複数キュー対応（優先度別キュー分離）
- ❌ デプロイ時のグレースフル再起動処理
- ❌ 監視・ログ管理

**実装要件**:
- systemdサービスファイル（`reforma-queue-worker@.service`）の作成
- 環境変数設定（`QUEUE_CONNECTION`, `DB_QUEUE`等）
- ワーカー数の設定（デフォルト: 1、必要に応じて複数）
- キュー分離戦略（`default`, `notifications`, `pdfs`）
- デプロイスクリプトの更新（キューワーカーの再起動処理）
- メモリリーク対策（`--max-jobs`, `--max-time`オプション）

**参照**: 
- `queue-worker-systemd-spec.md`（詳細仕様）
- Laravel Queue Documentation

---

## 未実装・要対応タスク（フロントエンド）

### 0. BASIC認証対応（環境変数設定）
**現状**: バックエンド側（Apache設定）とフロントエンド側（apiFetch.ts）の実装は完了  
**優先度**: 中（ステージング環境等でBASIC認証が必要な場合のみ）

**フロントエンド対応が必要な内容**:
- ❌ 環境変数の設定（`.env.staging`または`.env.production`）
  - `VITE_API_BASIC_AUTH_USER`: BASIC認証のユーザー名
  - `VITE_API_BASIC_AUTH_PASS`: BASIC認証のパスワード
- ❌ ビルド時の環境変数設定確認
- ❌ デプロイ時の環境変数設定確認

**実装要件**:
- ステージング環境等でBASIC認証が必要な場合、環境変数を設定する
- 開発環境では環境変数を設定しない（BASIC認証なしで動作）
- 本番環境では通常、BASIC認証は不要（または別の認証方式を使用）

**参照**: 
- `apache-basic-auth-config.md`（Apache設定とフロントエンド対応手順）
- `src/utils/apiFetch.ts`（BASIC認証ヘッダー自動追加機能は実装済み）

---

### 1. SUPP-DISPLAY-MODE-001: 表示モード機能（フロントエンド側）
**現状**: バックエンド側は完全実装済み、フロントエンド側は未実装  
**優先度**: 中

**バックエンド実装済み**:
- ✅ submission_valuesテーブルにlabel_json, field_label_snapshotカラム追加（既存）
- ✅ POST /v1/forms/{form_key}/submitにlocale, modeパラメータ追加（実装済み）
- ✅ label/both/valueモード対応（実装済み）
- ✅ 保存の正はvalue、labelはスナップショット（実装済み）
- ✅ ラベルスナップショット保存ロジックの改善（locale対応）
- ✅ CSVエクスポート時のmode指定対応（既に実装済み）

**フロントエンド未実装**:
- ❌ 公開フォーム: 選択肢表示（label/both/value）の切替UI
- ❌ 管理画面プレビュー: locale+mode切替機能
- ❌ ACK画面: labelを既定表示（label_snapshot優先）

**実装要件**:
- 公開フォーム（U-01）: 選択肢フィールド（select/radio/checkbox）の表示モード切替
- フォームプレビュー（F-04）: locale+mode切替UI追加
- ACK画面（A-03）: label_snapshotがあればそれを優先表示

**参照**: 
- reforma-notes-v1.1.0.md SUPP-DISPLAY-MODE-001
- reforma-notes-v1.0.0-追補パッチ-表示モード-テーマ-計算フィールド-.json

---

### 2. SUPP-THEME-001: テーマ機能（フロントエンド側）
**現状**: バックエンド側は完全実装済み、フロントエンド側は未実装  
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

**フロントエンド未実装**:
- ❌ 公開フォーム表示時に`theme_id`と`theme_tokens`を取得
- ❌ フォームコンテナに`data-theme-id`属性を付与
- ❌ `theme_tokens`をCSS変数に展開（:rootではなくフォームコンテナ配下）
- ❌ プリセットテーマの定義と適用
- ❌ テーマ管理画面（System Admin用）

**実装要件**:
- 公開フォーム（U-01）: `GET /v1/public/forms/{form_key}`からテーマ情報を取得し、フォームコンテナに適用
- フォーム編集（F-02）: テーマ選択UI追加（theme_id選択、theme_tokensカスタマイズ）
- テーマ管理画面（新規）: System Admin用のテーマCRUD画面

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

### 4. 条件分岐UI（F-03/F-05）: 条件分岐ビルダー
**現状**: バックエンド側は完全実装済み、フロントエンド側は未実装  
**優先度**: 中

**バックエンド実装済み**:
- ✅ ConditionEvaluatorサービスの実装
- ✅ visibility_rule, required_rule, step_transition_ruleの評価
- ✅ ConditionStateレスポンス生成
- ✅ 安全側フォールバック

**フロントエンド未実装**:
- ❌ F-03（フォーム項目設定）: 条件分岐ビルダーUI（visibility_rule, required_rule）
- ❌ F-05（ステップ設定）: 条件分岐ビルダーUI（transition_rule）
- ❌ 条件分岐ビルダー: field type × operator 許可表の適用
- ❌ 条件分岐ビルダー: operator別 value_input UI

**実装要件**:
- 条件分岐ビルダー: row = field_selector / operator_selector / value_input
- 論理結合: AND/OR明示（暗黙優先順位なし）
- ネスト制限: max_nesting=1（v1.x制限）
- 条件数制限: max_conditions=10
- バリデーション: field_required, type_match, no_self_reference

**参照**: 
- reforma-frontend-spec-v1.0.0-condition-ui-.json
- reforma-frontend-spec-v1.0.0-condition-operator-matrix-ui-.json
- reforma-frontend-spec-v1.0.0-condition-ui-examples-.json
- form-feature-attachments-v1.1.json A-06

---

### 5. 公開フォーム（U-01）: 条件分岐適用
**現状**: バックエンド側は完全実装済み、フロントエンド側は未実装  
**優先度**: 高

**バックエンド実装済み**:
- ✅ GET /v1/public/forms/{form_key}でConditionStateを返す
- ✅ POST /v1/forms/{form_key}/submitでConditionStateを評価
- ✅ 安全側フォールバック

**フロントエンド未実装**:
- ❌ ConditionStateの適用（fields.visible/required/store）
- ❌ 非表示フィールドの非表示処理
- ❌ 必須解除の適用
- ❌ STEP遷移時の条件チェック（422エラー表示）

**実装要件**:
- ConditionState適用: APIから取得したConditionStateをUIに反映
- フィールド表示制御: visible=falseのフィールドを非表示
- 必須制御: required=falseのフィールドを任意化
- STEP遷移: transition_rule評価結果に基づく遷移制御
- エラー表示: 422 STEP_TRANSITION_DENIED時のエラー表示

**参照**: 
- reforma-notes-v1.0.0-条件分岐-評価結果IF-.json
- reforma-api-spec-v0.1.4.md（ConditionStateスキーマ）

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

### S-01: システム管理ダッシュボード
**現状**: 画面レイアウトのみ実装、API連携未実装  
**優先度**: 中

**未実装機能**:
- ❌ GET /v1/dashboard/summary: ロール別の統計情報取得・表示
- ❌ GET /v1/dashboard/errors: エラー情報取得・表示
- ❌ ロール別のブロック表示（現状はモック）

**実装要件**:
- APIから統計情報を取得して表示
- ロール別の表示制御（system_admin, form_admin, operator, viewer）

**参照**: reforma-api-spec-v0.1.4.md

---

### F-01: フォーム一覧
**現状**: 画面レイアウトのみ実装、API連携未実装  
**優先度**: 高

**未実装機能**:
- ❌ GET /v1/forms: フォーム一覧取得・表示
- ❌ ページネーション（page, per_page）
- ❌ ソート機能
- ❌ 検索・フィルタ機能
- ❌ フォーム作成（POST /v1/forms）
- ❌ フォーム削除（DELETE /v1/forms/{id}）

**実装要件**:
- APIからフォーム一覧を取得して表示
- 仕様書JSON（ui.list.columns）に準拠した列表示
- アクション（actions）に準拠した操作ボタン

**参照**: reforma-api-spec-v0.1.4.md

---

### F-02: フォーム編集
**現状**: 画面レイアウトのみ実装、API連携未実装  
**優先度**: 高

**未実装機能**:
- ❌ GET /v1/forms/{id}: フォーム情報取得・表示
- ❌ PUT /v1/forms/{id}: フォーム情報更新
- ❌ テーマ選択UI（theme_id選択、theme_tokensカスタマイズ）
- ❌ フォーム基本情報の編集（name, code, description等）
- ❌ 通知設定、PDF設定等の編集

**実装要件**:
- APIからフォーム情報を取得して表示
- 仕様書JSON（ui.fields）に準拠した入力項目表示
- 保存時のバリデーション・エラーハンドリング

**参照**: 
- reforma-api-spec-v0.1.4.md
- SUPP-THEME-001-spec.md

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

**実装要件**:
- APIからフィールド一覧を取得して表示
- 条件分岐ビルダー実装（別タスク参照）
- フィールド編集フォーム

**参照**: 
- reforma-api-spec-v0.1.4.md
- reforma-frontend-spec-v1.0.0-condition-ui-.json

---

### F-04: フォームプレビュー
**現状**: 画面レイアウトのみ実装、API連携未実装  
**優先度**: 中

**未実装機能**:
- ❌ GET /v1/forms/{id}: フォーム情報取得・表示
- ❌ 公開フォーム（U-01）と同じレンダリングロジック
- ❌ locale+mode切替UI（表示モード機能）
- ❌ プレビュー専用のread-only表示

**実装要件**:
- APIからフォーム情報を取得
- ScreenRendererを使用した動的レンダリング
- locale+mode切替UI追加

**参照**: 
- reforma-api-spec-v0.1.4.md
- SUPP-DISPLAY-MODE-001

---

### R-01: 回答一覧
**現状**: 画面レイアウトのみ実装、API連携未実装  
**優先度**: 高

**未実装機能**:
- ❌ GET /v1/responses: 回答一覧取得・表示
- ❌ ページネーション（page, per_page）
- ❌ ソート機能
- ❌ 検索・フィルタ機能（フォーム別、ステータス別等）
- ❌ CSVエクスポート（POST /v1/responses/export/csv）
- ❌ 進捗表示（GET /v1/progress/{job_id}）

**実装要件**:
- APIから回答一覧を取得して表示
- 検索機能の実装
- CSVエクスポート機能（非同期処理、進捗表示）

**参照**: 
- reforma-api-spec-v0.1.4.md
- reforma-notes-v1.1.0.md A-01_csv_column_definition

---

### R-02: 回答詳細
**現状**: 画面レイアウトのみ実装、API連携未実装  
**優先度**: 高

**未実装機能**:
- ❌ GET /v1/responses/{id}: 回答詳細取得・表示
- ❌ GET /v1/responses/{id}/pdf: PDF表示・ダウンロード
- ❌ フィールドスナップショット表示（label_snapshot優先）
- ❌ 通知再送機能（POST /v1/responses/{id}/notifications/resend）
- ❌ PDF再生成機能（POST /v1/responses/{id}/pdf/regenerate）

**実装要件**:
- APIから回答詳細を取得して表示
- フィールド値・ラベルの表示（表示モード対応）
- PDF表示・ダウンロード機能
- 通知再送・PDF再生成機能（System Admin以上）

**参照**: 
- reforma-api-spec-v0.1.4.md
- reforma-notes-v1.1.0.md A-05_examples

---

### L-01: ログ一覧
**現状**: 画面レイアウトのみ実装、API連携未実装  
**優先度**: 中

**未実装機能**:
- ❌ GET /v1/logs: ログ一覧取得・表示
- ❌ ページネーション（page, per_page）
- ❌ ソート機能
- ❌ 検索・フィルタ機能（タイプ別、ステータス別等）

**実装要件**:
- APIからログ一覧を取得して表示
- ログタイプ別の表示（notification, pdf, ack等）

**参照**: reforma-api-spec-v0.1.4.md

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

**参照**: reforma-api-spec-v0.1.4.md

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

**参照**: reforma-api-spec-v0.1.4.md

---

### S-02: アカウント一覧
**現状**: 部分的に実装済み（GET /v1/system/admin-usersは実装済み、スタブモードあり）  
**優先度**: 中

**未実装機能**:
- ❌ POST /v1/system/admin-users: アカウント作成
- ❌ PUT /v1/system/admin-users/{id}: アカウント更新
- ❌ GET /v1/system/admin-users/{id}: アカウント詳細取得
- ❌ POST /v1/system/admin-users/invites/resend: 招待再送

**実装要件**:
- アカウント作成フォーム
- アカウント編集フォーム
- アカウント詳細表示
- 招待再送機能

**参照**: reforma-api-spec-v0.1.4.md

---

### テーマ管理画面（新規）
**現状**: 未実装  
**優先度**: 中

**未実装機能**:
- ❌ GET /v1/system/themes: テーマ一覧取得・表示
- ❌ POST /v1/system/themes: テーマ作成
- ❌ PUT /v1/system/themes/{id}: テーマ更新
- ❌ DELETE /v1/system/themes/{id}: テーマ削除
- ❌ GET /v1/system/themes/{id}/usage: 使用状況確認
- ❌ POST /v1/system/themes/{id}/copy: テーマコピー

**実装要件**:
- System Admin用のテーマCRUD画面
- テーマトークンの編集UI
- 使用状況表示

**参照**: 
- reforma-api-spec-v0.1.4.md
- SUPP-THEME-001-spec.md

---

## 優先度の推奨

### 高優先度
1. **公開フォーム（U-01）: 条件分岐適用**（コア機能、必須）
2. **F-01: フォーム一覧のAPI連携**（基本機能）
3. **F-02: フォーム編集のAPI連携**（基本機能）
4. **F-03: フォーム項目設定のAPI連携**（基本機能）
5. **R-01: 回答一覧のAPI連携**（基本機能）
6. **R-02: 回答詳細のAPI連携**（基本機能）

### 中優先度
7. **SUPP-DISPLAY-MODE-001: 表示モード機能**（バックエンド実装済み、フロントのみ）
8. **SUPP-THEME-001: テーマ機能**（バックエンド実装済み、フロントのみ）
9. **条件分岐UI（F-03/F-05）: 条件分岐ビルダー**（管理画面機能）
10. **F-04: フォームプレビューのAPI連携**（管理画面機能）
11. **L-01/L-02: ログ一覧・詳細のAPI連携**（管理画面機能）
12. **C-01: 検索のAPI連携**（管理画面機能）
13. **S-01: ダッシュボードのAPI連携**（管理画面機能）
14. **S-02: アカウント一覧の完全実装**（管理画面機能）
15. **テーマ管理画面（新規）**（System Admin機能）

### 低優先度（v2候補）
6. **計算フィールド機能**（バックエンド実装済み、フロントのみ）

---

## フロントエンド実装状況（v0.5.16時点）

### 実装済み機能
- ✅ 認証・認可（AuthContext, RequireAuth, RequireRole）
- ✅ セッション無効時の自動リダイレクト
- ✅ 403エラー（ROOT_ONLY等）の専用処理
- ✅ 共通レイアウト（AppLayout、サイドバー折りたたみ対応）
- ✅ 多言語対応（ja/en、Cookie優先）
- ✅ テーマ切替（light/dark/reforma）
- ✅ Debug UI（VITE_DEBUG=true時）
- ✅ 主要画面実装（A-01, A-02, S-01, S-02, F-01～F-04, U-01, A-03, R-01, R-02, L-01, L-02, C-01, E-01, N-01）

### 未実装機能
- ❌ 表示モード機能（SUPP-DISPLAY-MODE-001）
- ❌ テーマ機能（SUPP-THEME-001）
- ❌ 条件分岐UI（F-03/F-05）
- ❌ 条件分岐適用（U-01）
- ❌ 計算フィールド機能

### 実装済み機能（追加）
- ✅ エラー構造の統一（共通仕様v1.5.1準拠のToast表示優先順位実装）

---

## 将来削除予定（互換性のため現状維持）

### roleフィールド（単一）の削除
**現状**: OpenAPI定義・バックエンド・フロントエンドで`deprecated: true`として残置  
**削除予定**: 将来のバージョン（v2.x以降を想定）

**現状の実装**:
- **OpenAPI定義**: `reforma-openapi-v0.1.4.yaml`の`User`スキーマに`role`フィールドが`deprecated: true`として定義
- **バックエンド**: `AuthController.php`で`role => $roleCodes[0] ?? null`として返却（互換性のため）
- **フロントエンド**: `AuthContext.tsx`の`mapApiUserToUser`で`role`をマッピング（互換性のため）

**削除時の対応**:
- OpenAPI定義から`role`フィールドを削除
- バックエンドの`AuthController.php`から`role`フィールドの返却を削除
- フロントエンドの`AuthContext.tsx`から`role`フィールドのマッピングを削除
- フロントエンドの`User`型から`role`フィールドを削除
- `screenRegistry.ts`等で`role`を使用している箇所を`roles[]`に置き換え

**参照**: 
- reforma-openapi-v0.1.4.yaml（240-252行目: `role`フィールドの定義）
- app/Http/Controllers/Api/V1/AuthController.php（83行目: `role`フィールドの返却）

---

## 補足

- 各タスクの詳細仕様は `reforma-notes-v1.1.0.md` を参照
- 実装時は OpenAPI 定義（reforma-openapi-v0.1.4.yaml）も更新すること
- 仕様書への反映も忘れずに実施すること
- フロントエンドの現在のバージョン: **v0.5.16**（2026-01-14）
- デザイン変更は不可（既存デザイン維持）
- 仕様書JSONを正としてUIを自動生成する方針を維持
