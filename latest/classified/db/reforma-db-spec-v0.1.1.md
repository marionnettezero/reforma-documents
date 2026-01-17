# ReForma DB仕様書 (v0.1.1 統合版)
この文書は、実装されているマイグレーションファイルを基に最新のDB仕様をまとめたものです。

**注意**: このMarkdownファイルの変更は、対応するJSONファイル（reforma-db-spec-v0.1.1.json）にも反映してください。

## バージョンおよびメタ情報
- **バージョン**: v0.1.2
- **生成日時**: 2026-01-17T00:00:00Z
- **更新内容**: テーマ機能、表示モード機能、計算フィールド機能、マイクロ秒対応の追加

---

## テーブル一覧

### forms
フォーム定義のマスタテーブル

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---------|-----|------|-----------|------|
| id | bigint unsigned | NO | - | 主キー |
| code | varchar(255) | NO | - | フォーム識別子（form_key、ユニーク） |
| status | varchar(16) | NO | 'draft' | ステータス（draft/published/closed） |
| is_public | boolean | NO | false | 公開フラグ |
| public_period_start | timestamp | YES | NULL | 公開開始日時 |
| public_period_end | timestamp | YES | NULL | 公開終了日時 |
| answer_period_start | timestamp | YES | NULL | 回答開始日時 |
| answer_period_end | timestamp | YES | NULL | 回答終了日時 |
| attachment_enabled | boolean | NO | false | 添付ファイルの利用有無 |
| attachment_type | varchar(32) | YES | NULL | 添付ファイルの種類（pdf_template, uploaded_files） |
| pdf_template_path | varchar(512) | YES | NULL | PDFテンプレートのストレージパス（pdf_templateの場合のみ） |
| attachment_files_json | json | YES | NULL | アップロードしたファイルのパス配列（uploaded_filesの場合のみ） |
| notification_user_enabled | boolean | NO | false | ユーザー通知の有効/無効 |
| notification_user_email_template | text | YES | NULL | ユーザー宛メールテンプレート |
| notification_user_email_subject | varchar(255) | YES | NULL | ユーザー宛メールタイトル |
| notification_user_email_from | varchar(255) | YES | NULL | ユーザー宛メール送信元 |
| notification_user_email_reply_to | varchar(255) | YES | NULL | ユーザー宛メール返信先 |
| notification_user_email_cc | json | YES | NULL | ユーザー宛メールCC（JSON配列） |
| notification_user_email_bcc | json | YES | NULL | ユーザー宛メールBCC（JSON配列） |
| notification_admin_enabled | boolean | NO | false | 管理者通知の有効/無効 |
| notification_admin_user_ids | json | YES | NULL | 通知先管理者ID配列（JSON配列） |
| notification_admin_email_template | text | YES | NULL | 管理者宛メールテンプレート |
| notification_admin_email_subject | varchar(255) | YES | NULL | 管理者宛メールタイトル |
| notification_admin_email_from | varchar(255) | YES | NULL | 管理者宛メール送信元 |
| notification_admin_email_reply_to | varchar(255) | YES | NULL | 管理者宛メール返信先 |
| theme_id | bigint unsigned | YES | NULL | テーマID（themesテーブルへの外部キー） |
| theme_tokens | json | YES | NULL | テーマトークン（フォーム固有のカスタマイズ） |
| created_by | bigint unsigned | YES | NULL | 作成者ID |
| created_at | timestamp | YES | NULL | 作成日時 |
| updated_at | timestamp | YES | NULL | 更新日時 |
| deleted_at | timestamp | YES | NULL | 削除日時（論理削除） |

**インデックス**:
- `idx_forms_status_is_public`: (status, is_public)
- `idx_forms_code`: (code)
- `idx_forms_theme_id`: (theme_id)

**外部キー**:
- `fk_forms_created_by`: created_by → users.id (ON DELETE SET NULL)
- `fk_forms_theme_id`: theme_id → themes.id (ON DELETE SET NULL)

---

### form_fields
フォームの入力項目定義テーブル

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---------|-----|------|-----------|------|
| id | bigint unsigned | NO | - | 主キー |
| form_id | bigint unsigned | NO | - | フォームID |
| field_key | varchar(255) | NO | - | フィールド識別子 |
| type | varchar(64) | NO | - | input種別（text/email/select等） |
| sort_order | integer | NO | 0 | 表示順序 |
| is_required | boolean | NO | false | 固定必須フラグ |
| options_json | json | YES | NULL | 選択肢など（JSON） |
| visibility_rule | json | YES | NULL | 表示条件ルール（JSON） |
| required_rule | json | YES | NULL | 必須条件ルール（JSON） |
| step_transition_rule | json | YES | NULL | ステップ遷移ルール（JSON） |
| computed_rule | json | YES | NULL | 計算フィールドルール（JSON） |
| pdf_block_key | varchar(255) | YES | NULL | PDFテンプレート内のblock名 |
| pdf_page_number | integer | YES | NULL | PDFテンプレートのページ番号（1始まり、デフォルトは1） |
| created_at | timestamp | YES | NULL | 作成日時 |
| updated_at | timestamp | YES | NULL | 更新日時 |

**インデックス**:
- `idx_form_fields_form_id_sort_order`: (form_id, sort_order)
- `uk_form_fields_form_id_field_key`: (form_id, field_key) UNIQUE

**外部キー**:
- `fk_form_fields_form_id`: form_id → forms.id (ON DELETE CASCADE)

---

### submissions
フォーム送信データテーブル（responsesと同義）

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---------|-----|------|-----------|------|
| id | bigint unsigned | NO | - | 主キー |
| form_id | bigint unsigned | NO | - | フォームID |
| status | varchar(16) | NO | 'received' | ステータス（received/confirmed） |
| created_at | timestamp(6) | YES | NULL | 作成日時（マイクロ秒対応） |
| updated_at | timestamp(6) | YES | NULL | 更新日時（マイクロ秒対応） |

**インデックス**:
- `idx_submissions_form_id_created_at`: (form_id, created_at)
- `idx_submissions_status`: (status)

**外部キー**:
- `fk_submissions_form_id`: form_id → forms.id (ON DELETE CASCADE)

---

### submission_values
送信データの値テーブル

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---------|-----|------|-----------|------|
| id | bigint unsigned | NO | - | 主キー |
| submission_id | bigint unsigned | NO | - | 送信ID |
| field_key | varchar(255) | NO | - | フィールド識別子 |
| field_label_snapshot | varchar(255) | YES | NULL | フィールドラベルのスナップショット |
| value_json | json | NO | - | 回答値（JSON） |
| label_json | json | YES | NULL | ラベルスナップショット（JSON） |
| created_at | timestamp | YES | NULL | 作成日時 |
| updated_at | timestamp | YES | NULL | 更新日時 |

**インデックス**:
- `idx_submission_values_submission_id_field_key`: (submission_id, field_key)

**外部キー**:
- `fk_submission_values_submission_id`: submission_id → submissions.id (ON DELETE CASCADE)

---

### themes
テーマ定義のマスタテーブル

| カラム名 | 型 | NULL | デフォルト | 説明 |
|---------|-----|------|-----------|------|
| id | bigint unsigned | NO | - | 主キー |
| code | varchar(255) | NO | - | テーマコード（ユニーク） |
| name | varchar(255) | NO | - | テーマ名（表示用） |
| description | text | YES | NULL | テーマの説明 |
| theme_tokens | json | NO | - | テーマトークン（CSS変数の値） |
| is_preset | boolean | NO | false | プリセットテーマかどうか |
| is_active | boolean | NO | true | 有効かどうか |
| created_by | bigint unsigned | YES | NULL | 作成者ID（プリセットテーマはNULL） |
| created_at | timestamp | NO | - | 作成日時 |
| updated_at | timestamp | NO | - | 更新日時 |
| deleted_at | timestamp | YES | NULL | 削除日時（論理削除） |

**インデックス**:
- `idx_themes_code`: (code) UNIQUE
- `idx_themes_is_active`: (is_active)
- `idx_themes_is_preset`: (is_preset)

**外部キー**:
- `fk_themes_created_by`: created_by → users.id (ON DELETE SET NULL)

---

## 変更履歴

### v0.1.2 (2026-01-17)
- テーマ機能の追加（themesテーブル、forms.theme_id, forms.theme_tokens）
- 表示モード機能の追加（submission_values.label_json, submission_values.field_label_snapshot）
- 計算フィールド機能の追加（form_fields.computed_rule）
- マイクロ秒対応（submissions.created_at, submissions.updated_atをtimestamp(6)に変更）

### v0.1.1 (2026-01-16)
- 添付ファイル機能の追加（forms.attachment_enabled, attachment_type, pdf_template_path, attachment_files_json）
- PDF生成機能の追加（form_fields.pdf_block_key, pdf_page_number）
- 期間チェック機能の追加（forms.public_period_start, public_period_end, answer_period_start, answer_period_end）
- 通知機能の追加（forms.notification_user_*, notification_admin_*）

### v0.1.0 (2026-01-14)
- 初版作成
