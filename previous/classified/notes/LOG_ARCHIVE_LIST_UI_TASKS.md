# ログアーカイブ一覧画面 実装タスク

## 概要

ログアーカイブ機能はバックエンドで実装済みですが、ログアーカイブ一覧を表示するフロントエンドUIが未実装です。本ドキュメントは、ログアーカイブ一覧画面の実装タスクを整理したものです。

## 現状確認

### バックエンド: 実装済み

#### 実装済みAPI
- ✅ `POST /v1/logs/archive` - ログアーカイブ作成（LogsController@archive）
- ✅ `DELETE /v1/logs/archives/{id}` - ログアーカイブ削除（LogsController@deleteArchive）
- ✅ `GET /v1/logs/archives` - ログアーカイブ一覧取得（LogsController@archives）

#### 実装済みモデル・ジョブ
- ✅ `LogArchive`モデル（`app/Models/LogArchive.php`）
- ✅ `LogArchiveJob`（`app/Jobs/LogArchiveJob.php`）
- ✅ `log_archives`テーブル（マイグレーション実装済み）

### フロントエンド: 実装済み（2026-01-23）

#### 実装済みUI
- ✅ **LogArchiveListPage**: ログアーカイブ一覧画面（実装済み）
- ✅ **LogListPage**: エクスポート/アーカイブボタン（実装済み）
- ✅ **ルーティング**: ログアーカイブ一覧画面のルーティング（実装済み）
- ✅ **画面仕様書**: ログアーカイブ一覧画面の定義（実装済み）
- ✅ **サイドメニュー**: ログアーカイブ一覧をログ一覧の下に追加（実装済み）

## タスク1: バックエンド - ログアーカイブ一覧API実装

### 1.1 エンドポイント追加

#### 1.1.1 エンドポイント仕様
- **パス**: `GET /v1/logs/archives`
- **権限**: system_admin以上（`$user->hasRole(RoleCode::SYSTEM_ADMIN)`または`$user->is_root`）
- **クエリパラメータ**: 
  - `page` (required): ページ番号（最小値: 1）
  - `per_page` (required): 1ページあたりの件数（最小値: 1、最大値: 200）
  - `date_from` (optional): アーカイブ日時の開始日
  - `date_to` (optional): アーカイブ日時の終了日

#### 1.1.2 実装内容
- **ファイル**: `app/Http/Controllers/Api/V1/LogsController.php`
- **メソッド**: `archives`
- **処理フロー**:
  1. 権限チェック（system_admin以上）
  2. クエリパラメータのバリデーション
  3. `LogArchive`クエリを構築
  4. 日付範囲でのフィルタリング（`archived_at`）
  5. ページネーション処理
  6. アーカイブ情報を取得（`archiver`リレーションを含む）
  7. レスポンスを返却

#### 1.1.3 レスポンス形式
```json
{
  "success": true,
  "data": {
    "archives": {
      "items": [
        {
          "id": 1,
          "archive_path": "archives/logs/archive-20260123120000.zip",
          "archive_size": 1024000,
          "archived_at": "2026-01-23T12:00:00Z",
          "archived_by": 1,
          "archiver": {
            "id": 1,
            "email": "admin@example.com"
          },
          "filter_level": "error",
          "filter_date_from": "2026-01-01",
          "filter_date_to": "2026-01-31",
          "log_count": 1000,
          "metadata_json": {},
          "created_at": "2026-01-23T12:00:00Z",
          "updated_at": "2026-01-23T12:00:00Z"
        }
      ],
      "total": 10,
      "page": 1,
      "per_page": 20
    }
  },
  "message": null
}
```

#### 1.1.4 実装ファイル
- `app/Http/Controllers/Api/V1/LogsController.php`に`archives`メソッドを追加
- `routes/api.php`にルーティングを追加

---

## タスク2: フロントエンド - ログアーカイブ一覧画面実装

### 2.1 LogArchiveListPageの作成

#### 2.1.1 画面仕様
- **画面ID**: `LOG_ARCHIVE_LIST`
- **パス**: `/logs/archives`
- **権限**: system_admin以上
- **機能**:
  - ログアーカイブ一覧の表示（ページネーション対応）
  - 各アーカイブの情報表示（アーカイブ日時、サイズ、ログ数、フィルタ条件等）
  - 削除ボタン（root のみ表示）
  - 日付範囲でのフィルタリング

#### 2.1.2 実装内容
- **ファイル**: `src/pages/logs/LogArchiveListPage.tsx`（新規作成）
- **機能**:
  1. アーカイブ一覧の取得（`GET /v1/logs/archives`）
  2. ページネーション処理
  3. 日付範囲フィルタリング
  4. 各アーカイブの情報表示
  5. 削除ボタンの実装（root のみ表示、確認ダイアログ付き）
  6. エラーハンドリング

#### 2.1.3 表示項目
- アーカイブID
- アーカイブ日時
- アーカイブサイズ（バイト単位、適切な単位に変換して表示）
- アーカイブ実行ユーザー
- フィルタ条件（レベル、日付範囲）
- アーカイブされたログ数
- 操作（削除ボタン - root のみ）

#### 2.1.4 実装ファイル
- `src/pages/logs/LogArchiveListPage.tsx`（新規作成）

---

## タスク3: フロントエンド - LogListPageにアーカイブボタン追加

### 3.1 アーカイブボタンの追加

#### 3.1.1 実装内容
- **ファイル**: `src/pages/logs/LogListPage.tsx`（既存ファイルに追加）
- **場所**: 検索条件パネルの左側（「左側にボタンが必要な場合はここに追加」のコメント部分）
- **権限**: system_admin以上のみ表示
- **機能**:
  1. アーカイブボタンの追加
  2. クリック時にアーカイブ確認ダイアログを表示
  3. 現在のフィルタ条件（level, date_from, date_to）を取得
  4. `POST /v1/logs/archive`を呼び出し
  5. 進捗管理（ProgressDisplayコンポーネントを使用）
  6. 成功時はトースト表示
  7. エラーハンドリング

#### 3.1.2 アーカイブ確認ダイアログ
- 現在のフィルタ条件を表示
- アーカイブ対象のログ数を表示（オプション）
- 確認メッセージ（物理削除の警告）

#### 3.1.3 実装ファイル
- `src/pages/logs/LogListPage.tsx`（既存ファイルに追加）

---

## タスク4: ルーティング・画面仕様書の追加

### 4.1 ルーティング追加

#### 4.1.1 routePaths.tsへの追加
- **ファイル**: `src/routePaths.ts`（既存ファイルに追加）
- **追加内容**:
  ```typescript
  // L-03
  LOG_ARCHIVE_LIST: p("LOG_ARCHIVE_LIST"),
  ```

#### 4.1.2 App.tsxへのルーティング追加
- **ファイル**: `src/App.tsx`（既存ファイルに追加）
- **追加内容**: `LOG_ARCHIVE_LIST`画面へのルーティング

### 4.2 画面仕様書への追加

#### 4.2.1 screen.v1.0.jsonへの追加
- **ファイル**: `src/specs/screen.v1.0.json`（既存ファイルに追加）
- **追加内容**: `LOG_ARCHIVE_LIST`画面の定義
  - `screen_id`: `"LOG_ARCHIVE_LIST"`
  - `route.path`: `"/logs/archives"`
  - `route.required_roles`: `["system_admin"]`
  - `ui.list`: アーカイブ一覧の列定義

#### 4.2.2 実装ファイル
- `src/routePaths.ts`（既存ファイルに追加）
- `src/App.tsx`（既存ファイルに追加）
- `src/specs/screen.v1.0.json`（既存ファイルに追加）

---

## 実装順序の推奨

### Phase 1: バックエンド実装
1. LogsController@archivesメソッドの実装
2. routes/api.phpにルーティング追加

### Phase 2: フロントエンド実装
1. 画面仕様書への追加（screen.v1.0.json）
2. ルーティング追加（routePaths.ts, App.tsx）
3. LogArchiveListPageの作成
4. LogListPageにアーカイブボタン追加

---

## 技術的な考慮事項

### 権限管理
- アーカイブ一覧: system_admin以上
- アーカイブ削除: rootのみ

### パフォーマンス
- ページネーション対応（デフォルト: 20件/ページ）
- 日付範囲でのフィルタリング

### エラーハンドリング
- API呼び出しエラーのハンドリング
- 権限エラーのハンドリング
- 削除確認ダイアログ

### UI/UX
- アーカイブサイズの適切な表示（KB, MB, GB）
- 日付の適切なフォーマット
- ローディング状態の表示
- エラーメッセージの表示

---

## 関連ファイル一覧

### バックエンド（修正）
- `app/Http/Controllers/Api/V1/LogsController.php`（archivesメソッド追加）
- `routes/api.php`（ルーティング追加）

### フロントエンド（新規作成・修正）
- `src/pages/logs/LogArchiveListPage.tsx`（新規作成）
- `src/pages/logs/LogListPage.tsx`（既存ファイルに追加）
- `src/routePaths.ts`（既存ファイルに追加）
- `src/App.tsx`（既存ファイルに追加）
- `src/specs/screen.v1.0.json`（既存ファイルに追加）

---

## テスト項目

### バックエンド
- [x] アーカイブ一覧APIの実装（実装済み）
- [x] ページネーション処理（実装済み）
- [x] 日付範囲フィルタリング（実装済み）
- [x] 権限チェック（system_admin以上）（実装済み）
- [x] エラーハンドリング（実装済み）

### フロントエンド
- [x] アーカイブ一覧画面の表示（実装済み）
- [x] ページネーション処理（実装済み）
- [x] 日付範囲フィルタリング（実装済み）
- [x] 削除ボタンの表示（root のみ）（実装済み）
- [x] 削除確認ダイアログ（実装済み）
- [x] アーカイブ削除処理（実装済み）
- [x] LogListPageにエクスポート/アーカイブボタン追加（実装済み）
- [x] アーカイブ処理の進捗管理（実装済み）
- [x] エラーハンドリング（実装済み）
- [x] 権限チェック（system_admin以上）（実装済み）
- [x] サイドメニューへの追加（実装済み）

---

## 参考情報

### 既存の類似機能
- **フォームアーカイブ一覧**: 同様の構造で実装予定（未実装）
- **ログ一覧**: `LogListPage.tsx`を参考にする
- **進捗管理**: `ProgressDisplay.tsx`を使用

### 関連ドキュメント
- `FORM_ARCHIVE_AND_LOG_ARCHIVE_TASKS.md`: ログアーカイブ機能の実装タスク
- `FORM_EXPORT_IMPORT_ARCHIVE_TASKS.md`: フォームアーカイブ機能の実装タスク
