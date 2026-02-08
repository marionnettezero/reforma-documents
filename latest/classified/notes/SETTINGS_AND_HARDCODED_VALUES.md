# 設定（setting テーブル）とハードコード値の調査結果

**作成日**: 2026-01-28  
**最終調査・更新**: 2026-02-07  
**対象**: ReForma Backend (Laravel) の `settings` テーブルおよびアプリ内の期限・期間・TTL 等のハードコード

---

## 0. 設定の優先順位（方針）

**.env で指定している項目は可能な限り setting テーブルにキーを持たせ、次の順で参照する。**

1. **setting テーブル** … `Setting::get('key')` または `Setting::getOrConfig()` で取得。存在すればそれを採用。
2. **.env** … 未設定時は `env('REFORMA_XXX')` の値（config 経由で読み込まれる）。
3. **config のデフォルト** … それも無い場合は `config('reforma.xxx', default)` の default。

- **PAT 有効期限**: `Setting::get('auth.admin.pat.ttl_days') ?? config('reforma.auth.pat_ttl_days', 30)`（AuthController, AdminPatMiddleware）。
- **REFORMA 用（API・PDF・ロゴ・フォームファイル等）**: `Setting::getOrConfig($settingKey, $configKey, $default)` で「setting → config」の順で取得（§2.6 参照）。  
  `getOrConfig` は settings テーブルが存在しない場合（例: テストでマイグレーション未実行）は config にフォールバックする。

---

## 1. 概要

本ドキュメントは以下をまとめたものである。

- **ハードコードされている期限・期間・値** と、setting テーブルで **利用可能なキー** の対応
- **コードで参照している setting キー** と **Seeder で投入しているキー** の一覧
- **Seeder で投入しているがコード未参照** のキー（将来用・実装予定）

---

## 2. ハードコード値と setting の対応一覧

### 2.1 署名付き URL の有効期限

| 対象 | 箇所（例） | 現状 | 利用キー | 備考 |
|------|------------|------|----------|------|
| **PDF URL** | PdfStorageService, PublicFormsController, SendFormSubmissionNotificationJob, ResponsesController, ResponsesPdfController 等 | **Setting::get** | **pdf.signed_url_ttl_seconds**（Seeder で 3600 秒） | PdfStorageService::url() で参照。単位は秒。未指定時 3600。 |
| **ロゴ・アップロード・アーカイブ URL** | LogoStorageService, FormFileStorageService, ArchiveDownloadService および FormsController, PublicFormsController, LogsController, ProcessFormFileUploadJob 等 | **Setting::get** | **signed_url.ttl_seconds**（Seeder で 3600 秒） | 各サービス url() / downloadUrl() で参照。単位は秒。未指定時 3600。 |

→ 上記 2 キーは SettingsSeeder で投入済み。各ストレージサービスの url() / downloadUrl() で第2引数を省略すると設定値（秒→分に換算）が使われる。

---

### 2.2 フォームエクスポートのダウンロード URL 有効期限

| 対象 | 箇所 | 現状 | 備考 |
|------|------|------|------|
| エクスポート DL URL | ExportsController, BaseExportJob, ExportCsvJob, ExportFieldsJob, ExportFieldOptionsJob, FormExportJob | **Setting::get / SettingsService** | **export.download_url_ttl_seconds**（Seeder で 3600）。コードで参照済み。 |

---

### 2.3 確認トークン・招待トークンの TTL

| 対象 | 箇所 | 現状 | 備考 |
|------|------|------|------|
| 公開フォーム確認トークン | PublicFormsController | Setting::get('**confirm_token.ttl_hours**', 72) | **confirm_token.ttl_hours** を Seeder で 72 として投入済み。 |
| 管理アカウント招待 | AdminUsersController | Setting::get('**admin_invite.ttl_hours**', 72) | **admin_invite.ttl_hours** を Seeder で 72 として投入済み。 |

---

### 2.4 エクスポート・ジョブの TTL

| キー | 使用箇所 | デフォルト値 | Seeder |
|------|----------|--------------|--------|
| **export.download_url_ttl_seconds** | ExportsController, BaseExportJob, ExportCsvJob, ExportFieldsJob, ExportFieldOptionsJob | 3600 | **投入済み**（3600） |
| **export.allow_resign_after_url_expired** | ExportsController（getSettingBool → SettingsService） | true | **投入済み**（true） |
| **progress.job_ttl_seconds** | BaseExportJob, ExportCsvJob, ExportFieldsJob, ExportFieldOptionsJob | 86400 | **投入済み**（86400） |

---

### 2.5 PAT（ログイントークン）の有効期限

| 対象 | 箇所 | 現状 | 備考 |
|------|------|------|------|
| PAT TTL | AuthController, AdminPatMiddleware | **Setting::get('auth.admin.pat.ttl_days') ?? config('reforma.auth.pat_ttl_days', 30)** | Seeder で **auth.admin.pat.ttl_days**（30）を投入。優先: setting → .env → config。**30日固定ではなく設定で変更可能**。 |
| ローリング延長 | AdminPatMiddleware | **Setting::get** で制御 | **rolling_extension.enabled**（true/false）で有効/無効。**rolling_extension.update_frequency** で延長頻度（下記）。 |
| 延長頻度（update_frequency） | AdminPatMiddleware | 文字列 | **once_per_day**（同一日付で1回・デフォルト）, **once_per_hour**（1時間に1回）, **every_request**（毎リクエスト）, **never**（延長しない）。未知の値は once_per_day 扱い。 |

---

### 2.6 REFORMA 用設定（API・PDF・ロゴ・フォームファイル・通知）

**.env の REFORMA_* に対応する項目** を setting テーブルにキーとして持ち、**Setting::getOrConfig($settingKey, $configKey, $default)** で「setting → config」の順で参照する。

| 設定キー（setting） | config キー | 使用箇所 |
|---------------------|-------------|----------|
| **api.base** | reforma.api_base | ProgressController, HealthController, RootController |
| **api.version_path** | reforma.api_version_path | HealthController, RootController |
| **api.openapi_version** | reforma.openapi_version | HealthController, RootController, BuildInfoService |
| **pdf.storage_disk** | reforma.pdf.storage_disk | PdfStorageService |
| **pdf.template_path** | reforma.pdf.template_path | PdfStorageService |
| **pdf.attachment_path** | reforma.pdf.attachment_path | PdfStorageService |
| **pdf.output_path** | reforma.pdf.output_path | PdfStorageService |
| **pdf.pdflib_license** | reforma.pdf.pdflib_license | PdfGenerationService |
| **pdf.pdflib_search_paths** | reforma.pdf.pdflib_search_paths | PdfGenerationService（setting はカンマ区切り文字列、取得時に配列化） |
| **logo.storage_disk** | reforma.logo.storage_disk | LogoStorageService |
| **logo.path** | reforma.logo.path | LogoStorageService |
| **form_files.storage_disk** | reforma.form_files.storage_disk | FormFileStorageService |
| **form_files.path** | reforma.form_files.path | FormFileStorageService |
| **form_files.temp_path** | reforma.form_files.temp_path | FormFileStorageService |
| **notification.default_emails** | reforma.notification.default_emails | **保留**（将来用に Seeder で投入済み） |

上記キーは SettingsSeeder で投入済み。

---

### 2.7 その他のハードコード（期限以外）

- **FormExportJob**: timeout 600 秒、tries 2 → ジョブ設定のため設定化の優先度は低い。
- **API の per_page**: min:1, max:200 → 仕様値のため現状のままでよい。
- **SettingsController::list**: per_page 未指定時 50 → 必要に応じて設定キー化可能。
- **進捗 percent（30, 60, 80 等）**: UI 用の区切りのため設定化不要。

---

## 3. 不足キー（解消済み）

以下のキーは **以前「コードで参照しているが Seeder に無い」または「Seeder のみでコード未参照」とされていたが、現在は SettingsSeeder で投入済みかつコードで参照済み**である。

| キー | 備考 |
|------|------|
| confirm_token.ttl_hours | Seeder で 72 を投入済み。 |
| export.download_url_ttl_seconds | Seeder で 3600 を投入済み。 |
| export.allow_resign_after_url_expired | Seeder で true を投入済み。 |
| progress.job_ttl_seconds | Seeder で 86400 を投入済み。 |
| signed_url.ttl_seconds | Seeder で 3600 を投入済み。LogoStorageService / FormFileStorageService / ArchiveDownloadService で参照済み。 |
| pdf.signed_url_ttl_seconds | Seeder で 3600 を投入済み。PdfStorageService で参照済み。 |

---

## 4. SettingsSeeder で投入しているがコードで未参照のキー

以下は **現在の SettingsSeeder で投入しているが、アプリコードから参照されていない** キーである。将来の実装用または管理用としてキーを保持している。

| キー | Seeder 値 | 備考 |
|------|-----------|------|
| **notification.default_emails** | '' | デフォルト通知先メール（カンマ区切り）。**保留**（将来対応）。 |

※ **roles.permissions** は SettingsSeeder ではなく **RolePermissionsSeeder** で投入。User, RolesPermissionsController で参照。

---

## 5. コードで使用している setting キー（一覧）

| キー | 使用箇所 | Seeder | 取得方法 |
|------|----------|--------|----------|
| auth.admin.pat.ttl_days | AuthController, AdminPatMiddleware | SettingsSeeder（30） | Setting::get ?? config |
| auth.admin.pat.rolling_extension.enabled | AdminPatMiddleware | SettingsSeeder（true） | Setting::get |
| auth.admin.pat.rolling_extension.update_frequency | AdminPatMiddleware | SettingsSeeder（once_per_day） | Setting::get |
| auth.password_policy.min_length | AuthController | SettingsSeeder（8） | Setting::get |
| auth.password_policy.require.lowercase / .uppercase / .digit / .symbol | AuthController | SettingsSeeder（true） | Setting::get |
| confirm_token.ttl_hours | PublicFormsController | SettingsSeeder（72） | Setting::get |
| admin_invite.ttl_hours | AdminUsersController | SettingsSeeder（72） | Setting::get |
| pdf.regeneration.default_allowed | ResponsesPdfRegenerateController | SettingsSeeder（false） | Setting::get |
| export.download_url_ttl_seconds | ExportsController, BaseExportJob, ExportCsvJob, ExportFieldsJob, ExportFieldOptionsJob | SettingsSeeder（3600） | Setting::get / SettingsService |
| export.allow_resign_after_url_expired | ExportsController | SettingsSeeder（true） | getSettingBool → SettingsService |
| progress.job_ttl_seconds | BaseExportJob, ExportCsvJob, ExportFieldsJob, ExportFieldOptionsJob | SettingsSeeder（86400） | Setting::get |
| api.base | ProgressController, HealthController, RootController | SettingsSeeder | Setting::getOrConfig |
| api.version_path | HealthController, RootController | SettingsSeeder | Setting::getOrConfig |
| api.openapi_version | HealthController, RootController, BuildInfoService | SettingsSeeder | Setting::getOrConfig |
| pdf.storage_disk, template_path, attachment_path, output_path | PdfStorageService | SettingsSeeder | Setting::getOrConfig |
| pdf.pdflib_license, pdflib_search_paths | PdfGenerationService | SettingsSeeder | Setting::getOrConfig |
| logo.storage_disk, logo.path | LogoStorageService | SettingsSeeder | Setting::getOrConfig |
| form_files.storage_disk, path, temp_path | FormFileStorageService | SettingsSeeder | Setting::getOrConfig |
| pdf.signed_url_ttl_seconds | PdfStorageService::url() | SettingsSeeder（3600） | Setting::get（秒→分に換算） |
| signed_url.ttl_seconds | LogoStorageService::url(), FormFileStorageService::url(), ArchiveDownloadService::downloadUrl() | SettingsSeeder（3600） | Setting::get（秒→分に換算） |
| roles.permissions | User, RolesPermissionsController | RolePermissionsSeeder | Setting::get |

---

## 6. 動作確認（調査時点）

- **SettingsSeederTest**: Seeder で投入される全キーの存在・型・値をアサート。通過。
- **HealthVersionTest, RootLandingTest**: API 情報（api.base, version_path, openapi_version）を getOrConfig で取得。通過。
- **SettingsControllerTest**: 設定の取得・更新。通過。
- **getOrConfig**: settings テーブルが存在しない場合（テストで DB 未セットアップ）は `QueryException` を捕捉し config にフォールバックするため、従来どおり動作する。

※ FormsApiTest の theme_tokens 関連 2 件の失敗は、設定キーとは無関係の既存事象の可能性あり。

---

## 7. 対応方針のまとめ

1. **署名付き URL 有効期限**  
   - **pdf.signed_url_ttl_seconds**（PDF 専用）は PdfStorageService::url() で参照済み。**signed_url.ttl_seconds**（ロゴ・アップロード・アーカイブ）は LogoStorageService / FormFileStorageService / ArchiveDownloadService で参照済み。いずれも単位は秒で、未指定時 3600。呼び出し元で第2引数を省略すると設定値が使われる。
2. **エクスポート・ジョブ・確認トークン・招待 TTL**  
   - 該当キーはすべて SettingsSeeder で投入済み。コードで参照済み。
3. **REFORMA 用（API・PDF・ロゴ・フォームファイル）**  
   - Setting::getOrConfig で「setting → .env → config」の順で取得。Seeder でキー投入済み。
4. **未参照・保留キー**  
   - **notification.default_emails** は保留（将来対応）。auth.admin.pat.rolling_extension.* は AdminPatMiddleware で参照済み。

---

## 8. 変更時の注意

- **pdf.signed_url_ttl_seconds** は **PDF 用のみ**。ロゴ・アップロード・アーカイブには **signed_url.ttl_seconds** を使う。
- **roles.permissions** は SettingsSeeder ではなく **RolePermissionsSeeder** で投入する。SettingsController の list に含まれるかは実装次第。
- 未使用キーを Seeder から削除する場合、既に DB に存在する行はそのまま残る。不要なら別途削除用マイグレーションやスクリプトを検討する。

---

## 9. フロントエンドとの関係（調査結果）

**結論: setting テーブルを利用するバックエンド修正全般において、フロントエンド側のコード修正は不要である。**

### 9.1 フロントエンドが値を受け取る経路

| 設定の種類 | フロントでの参照方法 | 修正要否 |
|------------|----------------------|----------|
| **API ベース・バージョン** | ビルド時 **VITE_API_BASE** / **VITE_API_VERSION**（env.ts）で固定。バックエンドの /health や api_base は参照していない。 | **不要**。バックエンドで setting から変更しても、フロントは従来どおり env の値でリクエストする。同一デプロイで .env と setting を揃えておけば問題なし。 |
| **パスワードポリシー** | ログイン・招待受理・パスワード変更時に API レスポンスの **password_policy** をそのまま表示・バリデーションに利用（InviteAcceptPage, PasswordChangeDialog）。 | **不要**。バックエンドが Setting::get で返しているだけなので、レスポンスの形は変わらない。 |
| **テーマ・フォーム** | フォーム取得 API の **theme_tokens**, **logo_url** などをそのまま表示・編集に利用。 | **不要**。署名付き URL の TTL やストレージパスはバックエンド内で完結し、フロントに渡るのは「URL 文字列」のみ。 |
| **システム設定一覧** | **GET /v1/system/settings/list** で一覧取得し、**GET/PUT /v1/system/settings/{key}** で表示・更新。キーはバックエンドの DB 由来で、フロントはキー名をハードコードしていない。 | **不要**。Seeder で追加したキーは list にそのまま載り、既存の一覧・編集 UI で表示・更新できる。 |
| **進捗・エクスポート** | **ProgressDisplay** は **API_BASE + API_VERSION** から `/v1/progress/{id}` を組み立て。エクスポート DL の有効期限はバックエンド側のみ。 | **不要**。 |
| **バックエンドバージョン** | **getBackendVersion()** が **/v1/health** を呼ぶが、URL は **API_BASE / API_VERSION**（env）で組み立て。レスポンスの **data.build.version** のみ利用。 | **不要**。 |

### 9.2 補足

- **署名付き URL の TTL**（pdf.signed_url_ttl_seconds, signed_url.ttl_seconds）はバックエンドだけで使用。フロントは「発行された URL」を受け取って表示するだけなので、TTL 変更に伴うフロント修正は不要。
- **PAT のローリング延長**（rolling_extension.*）は認証ミドルウェア内の挙動。フロントはトークン送信のみで、延長の有無・頻度を意識しない。
- バックエンドの **api_base / api_version_path** を **setting で変更**し、かつフロントの **VITE_*** と異なる値にした場合、フロントは従来の URL にリクエストするため、そのままでは不整合になる。そのような運用にする場合は、**ビルド時の VITE_API_BASE / VITE_API_VERSION をバックエンドの設定と一致させる**か、将来フロントで「/health やルートから api 情報を取得して動的にベース URL を決める」対応が必要になる。現状の「.env と setting を揃えてデプロイする」運用ならフロント修正は不要。

---

## 10. 回答詳細の PDF / ファイル URL と有効期限

フロントの「回答詳細」では **PDF の URL** と **ファイル（アップロード）の URL** が表示される。有効期限の扱いは次のとおり。

### 10.1 PDF

- **発行タイミング**: 回答詳細 API（**GET /v1/responses/{id}**）のたびに、バックエンド（ResponsesController::show）が `pdfStorage->url($pdfPath)` で **その都度新しい署名付き URL** を生成し、レスポンスの `pdfs[].url` に含める。
- **有効期限が切れた場合**  
  - **回答詳細を開き直す／画面を更新する**だけで、再度 API が呼ばれ **新しい URL が発行される**ため、実質的に URL は延長される。  
  - 「**PDF 再生成**」は PDF 本体を作り直す機能だが、再生成後に詳細を再取得すると、その時点で新しい `pdfs[].url` が返る。  
- **結論**: PDF は **再表示（詳細の再取得）で URL が延長される**。再生成は「PDF ファイルを作り直す」用途であり、その結果としても新しい URL が得られる。

### 10.2 ファイル（アップロード）

- **保存内容**: アップロード処理（ProcessFormFileUploadJob）で、`value_json` に **path / filename / url**（その時点の署名付き URL）が保存される。有効期限は **signed_url.ttl_seconds**（例: 3600 秒）。
- **回答詳細 API**: ResponsesController::show は **value_json をそのまま**返す（`'value_json' => $value->value_json`）。DB に保存された URL がそのまま返るため、**有効期限切れ後はその URL では参照できなくなる**。
- **現状の対策**: **「期限切れファイル用に新しい署名付き URL を発行する」API は存在しない**。リンクは期限切れのままとなる。
- **対策（実装済み）**  
  **回答詳細 API の変更**を採用済み。ファイル型の value（`value_json` に **path** がある場合）について、ResponsesController::show で `FormFileStorageService::url($path)` を都度呼び、レスポンスの **value_json.url** を新しい署名付き URL で上書きして返している。PDF と同様に「詳細を開き直す／更新する」だけでファイル URL も延長される。フロント側の変更は不要。  
- **別案（未実装）**  
  専用エンドポイント（例: `GET /v1/responses/{id}/files/{field_key}/url`）で新しい URL を返す方式。上記のため現時点では不要。
