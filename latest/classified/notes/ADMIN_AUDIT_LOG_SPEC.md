# 監査ログの仕様

## 概要

監査ログは、システム管理者（system_admin）向けの「監査ログ一覧」画面で参照するログであり、**処理ログ（L-01）と同じ `admin_logs` テーブル**に保存されています。  
記録対象は「誰が・いつ・どの操作をしたか」を追跡するためのシステム操作です。

---

## 権限

- **監査ログ一覧画面（S-06）**: **system_admin 以上**がアクセス可能
- API: `GET /v1/system/admin-audit-logs` および `GET /v1/system/admin-audit-logs/{id}` は、ルートで `reforma.system_admin` ミドルウェアにより保護されている
- 権限の詳細は `PERMISSIONS_TABLE_WITH_ROOT.md` を参照（ログ関連: `logs.read` 等）

---

## 保存される情報（admin_logs テーブル）

| カラム | 型 | 説明 |
|--------|-----|------|
| id | bigint | 主キー |
| level | string(16) | ログレベル（info / warn / error） |
| category | string(64) | 操作カテゴリ（アクション種別） |
| message | text | メッセージ本文 |
| request_id | uuid, nullable | リクエストID |
| endpoint | string(255), nullable | エンドポイント（API パス等） |
| reason | string(64), nullable | 理由・補足 |
| user_id | bigint, nullable | **操作者（actor）のユーザーID** |
| created_at / updated_at | timestamp | 作成・更新日時 |

---

## 記録されている操作の例

監査ログとして `admin_logs` に書き込んでいる主な処理は以下のとおりです。

| 処理 | カテゴリ例 | 説明 |
|------|------------|------|
| 通知再送 | notification_resend | 回答に紐づく通知の再送（ResponsesNotificationController） |
| PDF再生成 | pdf_regeneration | 回答PDFの再生成（ResponsesPdfRegenerateController） |
| 管理者招待 | admin_invite | 管理者招待メール送信（AdminInviteMail, AdminUsersController） |
| APIエラー | api | 管理APIのエラー（AdminApiErrorLogMiddleware） |
| その他 | （上記以外の category） | アプリ内で `AdminLog::query()->create([...])` を呼んでいる箇所 |

上記のいずれも `user_id` に「その操作を実行したユーザー」が記録され、監査ログ一覧では「操作者」として表示されます。

---

## 監査ログ一覧画面の機能

- **一覧**: `GET /v1/system/admin-audit-logs` で取得。フィルタ（アクション・キーワード、日付範囲）、ソート、ページネーション対応
- **詳細**: `GET /v1/system/admin-audit-logs/{id}` で1件取得しモーダル表示
- **アーカイブ**: 日付範囲を指定して `POST /v1/logs/archive` を実行。処理ログと同じアーカイブフローを使用し、作成されたアーカイブは「ログアーカイブ一覧」でダウンロード・削除可能

---

## 参照

- バックエンド: `app/Http/Controllers/Api/V1/System/AdminAuditLogsController.php`
- モデル: `app/Models/AdminLog.php`
- テーブル: `database/migrations/2026_01_01_000008_create_other_tables.php`（admin_logs）
- フロント: `reforma-frontend-react/src/pages/system/AdminAuditLogListPage.tsx`
- 権限: `PERMISSIONS_TABLE_WITH_ROOT.md`
