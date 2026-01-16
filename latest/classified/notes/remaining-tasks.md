# ReForma 残タスク一覧

**作成日**: 2026-01-16  
**最終更新**: 2026-01-17  
**ベース**: reforma-notes-v1.1.0.md の内容と実装状況の照合結果

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

## 未実装・要対応タスク

### 1. SUPP-DISPLAY-MODE-001: 表示モード機能
**現状**: 未実装  
**必要実装**:
- submission_valuesテーブルにlabel_json, field_label_snapshotカラム追加
- POST /v1/forms/{form_key}/submitにlocale, modeパラメータ追加
- label/both/valueモード対応
- 保存の正はvalue、labelはスナップショット
- CSVエクスポート時のmode指定対応

**参照**: reforma-notes-v1.1.0.md reforma-notes-v1.0.0-追補パッチ-表示モード-テーマ-計算フィールド-.json SUPP-DISPLAY-MODE-001

---

### 2. SUPP-THEME-001: テーマ機能
**現状**: 未実装  
**必要実装**:
- formsテーブルにtheme_id, theme_tokensカラム追加
- GET /v1/forms/{id}のレスポンスにtheme_id, theme_tokens追加
- PUT /v1/forms/{id}のリクエストにtheme_id, theme_tokens追加
- テーマトークンスキーマ定義（color_primary, color_secondary等）
- 外部CSS URLはv2で検討（v1.xでは提供しない）

**参照**: reforma-notes-v1.1.0.md reforma-notes-v1.0.0-追補パッチ-表示モード-テーマ-計算フィールド-.json SUPP-THEME-001

---

### 3. フロントエンド調整: エラー構造の統一
**現状**: 実装状況不明  
**必要実装**:
- errors.reason / code / message等の統一
- /reforma/errorとトースト表示の分岐ロジック
- エラーコード定義の明確化

**参照**: 
- reforma-notes-v1.1.0.md reforma-notes-v1.1.0.txt
- reforma-notes-v1.1.0.md エラー設計

---

## 優先度の推奨

### 高優先度
1. フロントエンド調整: エラー構造の統一（ユーザー体験向上）

### 中優先度
2. SUPP-DISPLAY-MODE-001: 表示モード機能（多言語対応）

### 低優先度（v2候補）
3. SUPP-THEME-001: テーマ機能

---

## 補足

- 各タスクの詳細仕様は `reforma-notes-v1.1.0.md` を参照
- 実装時は OpenAPI 定義（reforma-openapi-v0.1.4.yaml）も更新すること
- 仕様書への反映も忘れずに実施すること
