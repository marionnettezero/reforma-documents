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

## 未実装・要対応タスク（フロントエンド）

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

## 優先度の推奨

### 高優先度
1. **公開フォーム（U-01）: 条件分岐適用**（コア機能、必須）

### 中優先度
3. **SUPP-DISPLAY-MODE-001: 表示モード機能**（バックエンド実装済み、フロントのみ）
4. **SUPP-THEME-001: テーマ機能**（バックエンド実装済み、フロントのみ）
5. **条件分岐UI（F-03/F-05）: 条件分岐ビルダー**（管理画面機能）

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

## 補足

- 各タスクの詳細仕様は `reforma-notes-v1.1.0.md` を参照
- 実装時は OpenAPI 定義（reforma-openapi-v0.1.4.yaml）も更新すること
- 仕様書への反映も忘れずに実施すること
- フロントエンドの現在のバージョン: **v0.5.16**（2026-01-14）
- デザイン変更は不可（既存デザイン維持）
- 仕様書JSONを正としてUIを自動生成する方針を維持
