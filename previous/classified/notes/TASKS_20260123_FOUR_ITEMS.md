# タスク一覧（2026-01-23 依頼の4項目）

## 1. ログアウトダイアログの DEBUG UI を削除する

### 現状
- **ファイル**: `reforma-frontend-react/src/layout/AppLayout.tsx`
- **場所**: ログアウト確認用 `ConfirmDialog` 内（約 528–551 行目）
- `{DEBUG_UI && (<div className="mt-4"><ScreenDebugPanel ... /></div>)}` で、`ScreenDebugPanel` が表示されている
- `getLatestApiCalls` 使用のため、`getLatestApiCalls` の import が他で使われていなければ削除の可否を確認

### サブタスク
| # | 内容 | 対象 |
|---|------|------|
| 1.1 | ログアウト `ConfirmDialog` 内の `{DEBUG_UI && (... ScreenDebugPanel ...)}` ブロックを削除 | `AppLayout.tsx` |
| 1.2 | `DEBUG_UI` の import がログアウト以外で使われていなければ削除（他で使用中なら残す） | `AppLayout.tsx` |
| 1.3 | `ScreenDebugPanel` の import がログアウト以外で使われていなければ削除 | `AppLayout.tsx` |
| 1.4 | `getLatestApiCalls` の import がログアウトの Debug 専用なら削除 | `AppLayout.tsx` |

---

## 2. アカウント詳細の作成日時/更新日時を共通モジュールで表示（作成者/更新者を含む）

### 現状
- **アカウント詳細**: `AccountListPage.tsx` の詳細モーダル（約 1454–1479 行）
  - `created_at` / `updated_at` を個別の `div` + `Badge` で表示
  - `created_by` / `updated_by` は未表示
- **共通コンポーネント**: `MetaInfo`（`src/components/MetaInfo.tsx`）
  - `created_at`, `created_by`, `created_by_label`, `updated_at`, `updated_by`, `updated_by_label` を表示
  - テーマ詳細（`ThemeListPage`）で使用
- **API**: `AdminUsersController::show()`（`/v1/system/admin-users/{id}`）
  - `created_at`, `updated_at` のみ返却。`created_by`, `updated_by` は返していない
- **DB**: `users` テーブルに `created_by`, `updated_by` あり（`0001_01_01_000000_create_users_table.php`）

### サブタスク
| # | 内容 | 対象 |
|---|------|------|
| 2.1 | `AdminUsersController::show()` の返却に `created_by`, `updated_by` を追加 | `app/Http/Controllers/Api/V1/System/AdminUsersController.php` |
| 2.2 | 表示名が必要な場合、`created_by`/`updated_by` の join または別取得で `created_by_label`/`updated_by_label` を返す（任意。無ければ `MetaInfo` は `#id` 表示） | 同上 or User リレーション |
| 2.3 | `AccountListPage` の User 型に `created_by`, `updated_by`（と `created_by_label`/`updated_by_label` があるなら）を追加 | `AccountListPage.tsx` |
| 2.4 | アカウント詳細の「メタデータ（作成日時・更新日時）」ブロックを削除し、`MetaInfo` に差し替え。`invited_at` は `MetaInfo` に含まないため、従来どおり別ブロックで表示 | `AccountListPage.tsx` |
| 2.5 | `MetaInfo` に `invited_at` を渡す必要があるか検討。不要なら `MetaInfo` の前/後に `invited_at` のみの表示を維持 | `AccountListPage.tsx` |

---

## 3. 回答一覧の CSV エクスポートに「response_id」が含まれているかの確認

### 現状
- **CsvExportService**
  - システムカラム: `['submission_id', 'submitted_at', 'form_code', 'status']`
  - ヘッダーは `getSystemColumnLabel()` の**ラベル**（`submission_id` → `回答ID` / `Response ID`）を使用。キー名 `submission_id` はヘッダーに出ない
- **EnsureResponsesCsvHeaderMiddleware**
  - 1 行目に `'submission_id'` または `'response_id'` が**含まれる**かで「回答のCSV」と判定
  - 含まれていなければ「回答のCSV」とみなし、`submission_id` も `response_id` もない場合に限り、先頭に `"response_id\n"` を付与（互換用）
- **実際の出力**
  - ヘッダーは「回答ID」または「Response ID」のため、`headerLine` に `submission_id` / `response_id` は出現しない
  - そのため `isResponsesExport` が else に入り、`content` に `submission_id` / `response_id` がなければ `response_id` を付与する条件を満たす
  - 結果として、**「response_id」列が先頭に追加され、先頭列が空のデータになっている可能性**
- **テスト**: `ResponsesExportFlowTest` が `assertStringContainsString('response_id', ...)` で通過。ミドルウェアが `response_id` を入れているため

### サブタスク
| # | 内容 | 対象 |
|---|------|------|
| 3.1 | 回答 CSV の 1 行目（ヘッダー）に `response_id` または `submission_id` が現状どう出るか、`CsvExportService` と `EnsureResponsesCsvHeaderMiddleware` の組み合わせで整理 | ドキュメント or コメント |
| 3.2 | 「`response_id` を先頭に付与する」仕様を維持するか、`submission_id`（またはそのラベル）が既にあるときは付与しないようミドルウェアを変更するか方針決定 | - |
| 3.3 | 方針に合わせてミドルウェアを修正（例: ヘッダーに「回答ID」「Response ID」「submission_id」のいずれかがあれば `response_id` を付与しない） | `EnsureResponsesCsvHeaderMiddleware.php` |
| 3.4 | `ResponsesExportFlowTest` の `response_id` アサーションを、採用した仕様に合わせて修正 | `tests/Feature/ResponsesExportFlowTest.php` |

---

## 4. ログアーカイブ一覧を開いたときの LogsController::show() の Type Error を解消する

### 現状・原因
- **エラー**: `LogsController::show(): Argument #2 ($id) must be of type int, string given`
- **経路**: `GET /v1/logs/archives` でログアーカイブ一覧を取得しようとすると発生
- **理由（ルート順）**: `routes/api.php` で  
  - `Route::get('/logs/{id}', ... 'show')` が  
  - `Route::get('/logs/archives', ... 'archives')` より**先**に定義されている  
  - `GET /v1/logs/archives` が `/logs/{id}` にマッチし、`id = "archives"`（string）で `show()` が呼ばれる
- **show のシグネチャ**: `show(Request $request, int $id)` のため、`string` で TypeError

### サブタスク
| # | 内容 | 対象 |
|---|------|------|
| 4.1 | `Route::get('/logs/archives', ...)` を `Route::get('/logs/{id}', ...)` **より前**に定義する | `routes/api.php` |
| 4.2 | 必要であれば、`/logs/export` や `/logs/archive` など、`/logs/{id}` と衝突しうるパスも、`/logs/{id}` より前に並べる | `routes/api.php` |
| 4.3 | 修正後、`GET /v1/logs/archives` が `archives()` にルーティングされ、`show()` の Type Error が解消されることを確認 | 手動 or テスト |

---

## ルート順の補足（タスク 4）

`api.php` の該当部分（要確認）:

```php
Route::get('/logs', [LogsController::class, 'index']);
Route::get('/logs/{id}', [LogsController::class, 'show']);      // 先
Route::post('/logs/export', ...);
Route::post('/logs/archive', ...);
Route::get('/logs/archives', [LogsController::class, 'archives']); // 後 → /logs/archives が /logs/{id} にマッチ
Route::get('/logs/archives/{id}/download', ...);
Route::delete('/logs/archives/{id}', ...);
```

推奨順（`/logs/{id}` で喰われるのを防ぐ）:

```php
Route::get('/logs', [LogsController::class, 'index']);
Route::post('/logs/export', ...);
Route::post('/logs/archive', ...);
Route::get('/logs/archives', [LogsController::class, 'archives']);
Route::get('/logs/archives/{id}/download', ...)->where('id', '[0-9]+');
Route::delete('/logs/archives/{id}', ...)->where('id', '[0-9]+');
Route::get('/logs/{id}', [LogsController::class, 'show']);  // 具体的なパスの後に定義
```

---

## 実施順の提案

1. **4** を最初に実施（ルート順の修正のみで解消、影響範囲が分かりやすい）
2. **1**（ログアウト DEBUG UI 削除）
3. **2**（アカウント詳細の MetaInfo 化。API の `created_by`/`updated_by` 追加 → フロントの `MetaInfo` 差し替え）
4. **3**（response_id の仕様確認とミドルウェア・テストの見直し）
