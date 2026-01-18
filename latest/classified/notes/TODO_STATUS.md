# ReForma 実装状況とTODO一覧

## 実装済み項目

### バックエンド（Laravel）

#### コア機能
- ✅ 認証システム（Sanctum）
- ✅ フォーム管理（CRUD、翻訳、通知設定、テーマ設定）
- ✅ フォーム項目管理（フィールド定義、条件ルール）
- ✅ 回答管理（一覧、詳細、削除、CSVエクスポート、ジョブキュー対応）
- ✅ ログ管理（AdminLog、一覧、詳細）
- ✅ テーマ管理（CRUD、プリセット/カスタム）
- ✅ 管理者アカウント管理（CRUD、招待メール、ロール管理）
- ✅ 横断検索API（admin_user, log）

#### メール機能
- ✅ 管理者アカウント招待メール（AdminInviteMail）
- ✅ フォーム送信通知メール（ユーザー/管理者）
- ✅ ジョブキュー対応（ShouldQueue）

#### その他
- ✅ BASIC認証対応（staging環境用）
- ✅ 監査ログ（AdminLog）記録

### フロントエンド（React）

#### 管理画面
- ✅ ログイン/ログアウト
- ✅ ダッシュボード
- ✅ フォーム一覧（作成、削除、詳細モーダル）
- ✅ フォーム編集（基本情報、翻訳、通知設定、添付ファイル設定）
- ✅ フォーム項目設定（STEP/GROUP/項目階層、ドラッグアンドドロップ、条件ルールUI）
- ✅ 回答一覧（フィルタリング、ページネーション）
- ✅ 回答詳細（API連携済み）
- ✅ ログ一覧（フィルタリング、ページネーション）
- ✅ ログ詳細（API連携済み）
- ✅ テーマ一覧（CRUD、詳細モーダル）
- ✅ テーマ編集（theme_tokens編集対応）
- ✅ アカウント管理（CRUD、ロール管理）

#### 認証・設定
- ✅ BASIC認証対応（フロントエンド）
- ✅ 多言語対応（i18n）

---

## 未実装項目

### フロントエンド（React）

#### 1. 横断検索画面（SearchPage.tsx）
- **現状**: モック実装のみ
- **必要な実装**:
  - `/v1/search` APIとの連携
  - 検索タイプの選択（admin_user, log）
  - ページネーション
  - 検索結果の表示とリンク
  - ローディング状態とエラーハンドリング

#### 2. フォームプレビュー画面（FormPreviewPage.tsx）
- **現状**: ✅ 実装済み
- **実装済み**:
  - ✅ `/v1/forms/{id}` APIとの連携（フォーム基本情報取得）
  - ✅ `/v1/forms/{id}/fields?include_rules=true` APIとの連携（フォーム項目取得）
  - ✅ フォーム項目の動的レンダリング（read-only、全フィールドタイプ対応）
  - ✅ 公開フォームと同じUIで表示（read-only）
  - ✅ 条件分岐評価と表示制御（簡易版、visibility_ruleに基づく）
  - ✅ 計算フィールドの表示
  - ✅ 多言語対応（翻訳情報の表示）

#### 3. 公開フォーム画面（PublicFormViewPage.tsx）
- **現状**: ✅ 実装済み（基本機能）
- **実装済み**:
  - ✅ `/v1/public/forms/{form_key}` APIとの連携
  - ✅ フォーム項目の動的レンダリング（text, textarea, select, checkbox, radio, number, date等）
  - ✅ バリデーション（必須チェック、required_rule）
  - ✅ 送信処理（`/v1/forms/{form_key}/submit`）
  - ✅ 条件分岐の評価と表示制御（visibility_rule）
  - ✅ 計算フィールドの表示
- **今後の拡張予定**:
  - ステップ遷移（複数ページフォーム対応）- 現時点では単一ページフォームのみ対応
  - リアルタイム条件分岐評価（回答値変更時のサーバー側評価、デバウンス付き）

#### 4. ACK画面（AckViewPage.tsx）
- **現状**: ✅ 実装済み
- **実装済み**:
  - ✅ `/v1/forms/{form_key}/ack` APIとの連携
  - ✅ URLパラメータからsubmission_idとtokenを取得
  - ✅ 受付完了メッセージの表示
  - ✅ 受付番号（submission_id）の表示
  - ✅ PDF URLの表示（将来の拡張に対応）

---

### バックエンド（Laravel）

#### 1. 回答詳細API（ResponsesController.php）
- **現状**: ✅ 実装済み
- **実装済み**:
  - ✅ `notifications` 情報の取得と返却（NotificationSentLogから取得）
  - ✅ `pdfs` 情報の取得と返却（PdfStorageServiceを使用してPDFパス/URLを取得）
  - ✅ フロントエンドでの通知履歴とPDF情報の表示

#### 2. 公開フォームAPI（PublicFormsController.php）
- **現状**: ✅ 完全実装済み
- **実装済み**:
  - ✅ `submit()` メソッドでPDF生成とURL取得（PDF生成が可能な場合）
  - ✅ `ack()` メソッドでPDF URL返却（PDFが存在する場合、または生成を試みる）
  - ✅ `submit()` メソッドで確認トークン（confirm_token）の生成と保存
  - ✅ `ack()` メソッドでtokenからsubmissionを検索する処理（実装済み）
  - ✅ トークンの有効期限チェック（設定テーブルから取得、デフォルト72時間）

#### 3. 通知ジョブ（SendFormSubmissionNotificationJob.php）
- **現状**: ✅ ACK URLとPDF URL実装済み
- **実装済み**:
  - ✅ `{{confirm_url.ack}}` プレースホルダーの実装
  - ✅ `{{confirm_url.pdf}}` プレースホルダーの実装（PDF生成が可能で、PDFが存在する場合）

#### 4. CSVエクスポートのジョブキュー対応（ResponsesExportController.php）
- **現状**: ✅ 実装済み（2026-01-18）
- **実装済み**:
  - ✅ `ExportCsvJob`ジョブクラスの作成（タイムアウト600秒、試行2回、`exports`キュー）
  - ✅ `ResponsesExportController::startCsv()`の修正（ジョブ投入に変更）
  - ✅ 進捗表示の段階的更新（0% → 30% → 50% → 80% → 100%）
  - ✅ 翻訳メッセージの確認（既に存在していた）

#### 5. 横断検索API（SearchController.php）
- **現状**: `admin_user` と `log` のみ対応
- **拡張候補**: `form` と `response` の検索も追加可能

---

## 実装優先度の推奨

### 高優先度
1. ✅ **横断検索画面**（SearchPage.tsx）- 管理画面の基本機能（実装済み）
2. ✅ **公開フォーム画面**（PublicFormViewPage.tsx）- システムの核心機能（基本実装済み）
3. ✅ **ACK画面**（AckViewPage.tsx）- 送信完了フローに必要（実装済み）

### 中優先度
4. ✅ **フォームプレビュー画面**（FormPreviewPage.tsx）- 管理画面での確認用（実装済み）
5. ✅ **回答詳細APIの拡張**（notifications, pdfs）- 詳細情報の表示（実装済み）

### 低優先度
6. ✅ **PDF URLの実装** - PDF生成機能の実装後に（実装済み）
7. ✅ **token検索機能** - 将来的な拡張（実装済み）

---

## 補足

- フォーム項目設定（FormItemPage.tsx）は完全実装済み
- 回答一覧・詳細、ログ一覧・詳細は完全実装済み
- テーマ管理は完全実装済み（theme_tokens編集対応済み）
- 管理者アカウント招待機能は完全実装済み（メール送信、監査ログ記録含む）
- 横断検索画面は完全実装済み（API連携、ページネーション、検索タイプ選択対応済み）
- 公開フォーム画面は基本実装済み（単一ページフォーム対応、ステップ遷移は将来の拡張予定）
- ACK画面は完全実装済み（API連携、受付番号表示、PDF URL表示対応済み）
- フォームプレビュー画面は完全実装済み（read-only表示、公開フォームと同じUI、条件分岐評価対応済み）
- 回答詳細APIは完全実装済み（notifications、pdfs情報の取得と表示対応済み）
- PDF URL機能は完全実装済み（ACK API、メール通知テンプレート、フォーム送信時のPDF生成とURL取得対応済み）
- token検索機能は完全実装済み（submissionsテーブルにconfirm_tokenカラム追加、フォーム送信時のトークン生成と保存、ACK APIでのtoken検索、設定テーブルから有効期限を取得する有効期限チェック対応済み）
