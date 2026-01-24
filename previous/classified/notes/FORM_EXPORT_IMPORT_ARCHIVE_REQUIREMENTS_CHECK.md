# フォームエクスポート/インポート/アーカイブ機能 要求確認

## 要求の整理

### 要求1: フォームエクスポート/インポート機能

**目的**: stagingで作成したフォームの構成を本番に持っていく

**要件**:
1. フォーム全体（基本/項目等の回答以外の情報）のエクスポート機能
2. それをインポートする機能
3. ロゴ、添付ファイルを含む
4. form_admin / system_admin が利用可能

### 要求2: フォームアーカイブ機能

**目的**: 古いフォームのデータを回答データも含めてアーカイブ化

**要件**:
1. S3にzip等で圧縮して保存
2. アーカイブ化したデータは物理削除
3. アーカイブの復元機能で新しいフォームとして復元可能
4. 物理削除後にテーブルのフラグメントも解消
5. 関連データも含めて削除（ユーザのアップロードしたファイル、生成されたPDFも含む）
6. system_admin が利用可能

---

## 実装状況の確認

### 要求1: フォームエクスポート/インポート機能

#### ✅ 1.1 フォーム全体（回答以外）のエクスポート機能

**実装状況**: ✅ 実装済み

**実装内容**:
- `FormExportJob`でフォーム基本情報、翻訳データ、項目データをエクスポート
- 回答データ（submissions, submission_values）は含まれていない ✅
- `FormsController@export`でエンドポイント提供

**確認ポイント**:
- ✅ フォーム基本情報（formsテーブル）
- ✅ 翻訳データ（form_translationsテーブル）
- ✅ 項目データ（form_fieldsテーブル）
- ✅ ロゴファイル（logo_path）
- ✅ PDFテンプレート（pdf_template_path）
- ✅ 添付ファイル（attachment_files_json、翻訳データの添付ファイルも含む）

#### ✅ 1.2 インポート機能

**実装状況**: ✅ 実装済み

**実装内容**:
- `FormImportJob`でJSON/ZIPファイルからフォームデータをインポート
- フォームコードの重複チェック（上書きまたは新規コード生成）
- ファイルのコピー（ロゴ、PDFテンプレート、添付ファイル）
- `FormsController@import`でエンドポイント提供

**確認ポイント**:
- ✅ JSON/ZIPファイルの展開
- ✅ データ検証
- ✅ フォームコードの重複処理
- ✅ フォーム基本情報の作成
- ✅ 翻訳データの作成
- ✅ 項目データの作成
- ✅ ファイルのコピー（ロゴ、PDFテンプレート、添付ファイル）

#### ✅ 1.3 ロゴ、添付ファイルを含む

**実装状況**: ✅ 実装済み

**確認ポイント**:
- ✅ ロゴファイル（LogoStorageService経由）
- ✅ PDFテンプレート（PdfStorageService経由）
- ✅ 添付ファイル（PdfStorageService経由、フォームと翻訳データの両方）

#### ✅ 1.4 form_admin / system_admin が利用可能

**実装状況**: ✅ 実装済み

**実装内容**:
- `FormsController@export`: `checkFormAccess($id, 'read')`を使用
  - `forms.read`権限チェック
  - form_admin / system_admin が利用可能 ✅
- `FormsController@import`: `forms.write`権限チェック
  - form_admin / system_admin が利用可能 ✅

**確認ポイント**:
- ✅ export: form_admin / system_admin が利用可能
- ✅ import: form_admin / system_admin が利用可能

---

### 要求2: フォームアーカイブ機能

#### ✅ 2.1 S3にzip等で圧縮して保存

**実装状況**: ✅ 実装済み

**実装内容**:
- `FormArchiveJob`でZIPファイルを作成
- S3にアップロード（`archives/forms/{form_id}/archive-{form_code}-{timestamp}.zip`）
- `FormsController@archive`でエンドポイント提供

**確認ポイント**:
- ✅ ZIPファイルとして圧縮
- ✅ S3にアップロード

#### ✅ 2.2 アーカイブ化したデータは物理削除

**実装状況**: ✅ 実装済み

**実装内容**:
- トランザクション内で物理削除を実行
  - `submission_values` の削除
  - `submissions` の削除
  - `form_fields` の削除
  - `form_translations` の削除
  - `forms` の物理削除（`forceDelete()`）

**確認ポイント**:
- ✅ 物理削除を実行
- ✅ トランザクション管理

#### ✅ 2.3 アーカイブの復元機能で新しいフォームとして復元可能

**実装状況**: ✅ 実装済み

**実装内容**:
- `FormArchiveRestoreJob`でS3からアーカイブを取得し、新しいフォームとして復元
- 送信データ、送信値データも復元
- `FormsController@restoreArchive`でエンドポイント提供

**確認ポイント**:
- ✅ S3からアーカイブを取得
- ✅ 新しいフォームとして復元
- ✅ 送信データ、送信値データも復元

#### ✅ 2.4 物理削除後にテーブルのフラグメントも解消

**実装状況**: ✅ 実装済み

**実装内容**:
- `OPTIMIZE TABLE`を実行
  - `submission_values`
  - `submissions`
  - `form_fields`
  - `form_translations`
  - `forms`

**確認ポイント**:
- ✅ テーブルのフラグメント解消

#### ✅ 2.5 関連データも含めて削除（ユーザのアップロードしたファイル、生成されたPDFも含む）

**実装状況**: ✅ 実装済み（2026-01-23確認）

**実装内容**:
- ✅ ロゴファイル（LogoStorageService経由）
- ✅ PDFテンプレート（PdfStorageService経由）
- ✅ 添付ファイル（PdfStorageService経由、フォームと翻訳データの両方）
- ✅ **生成されたPDF（submissionごとに生成されるPDF）がアーカイブに含まれている**
- ✅ **ユーザがアップロードしたファイル（FormFileStorageServiceで保存されるファイル）がアーカイブに含まれている**

**実装詳細**:
- `FormArchiveJob`の`buildArchiveData`メソッドで実装済み
  - 各submissionごとに生成されたPDF（`generated_pdf`）を取得してアーカイブに含める
  - submission_valuesからfileタイプのフィールドのファイルパスを取得してアーカイブに含める（`user_uploaded_file`）

#### ✅ 2.6 system_admin が利用可能

**実装状況**: ✅ 実装済み

**実装内容**:
- `FormsController@archive`: `hasRole(RoleCode::SYSTEM_ADMIN)`チェック
- `FormsController@restoreArchive`: `hasRole(RoleCode::SYSTEM_ADMIN)`チェック

**確認ポイント**:
- ✅ archive: system_admin のみ利用可能
- ✅ restoreArchive: system_admin のみ利用可能

---

## まとめ

### ✅ 要求1: フォームエクスポート/インポート機能

**実装状況**: ✅ **要求を満たしている**

すべての要件が実装済みです。

### ✅ 要求2: フォームアーカイブ機能

**実装状況**: ✅ **バックエンド実装済み**（2026-01-23確認）

**バックエンド実装状況**:
- ✅ 生成されたPDF（submissionごとに生成されるPDF）がアーカイブに含まれている
- ✅ ユーザがアップロードしたファイル（FormFileStorageServiceで保存されるファイル）がアーカイブに含まれている
- ✅ `FormArchiveJob`の`buildArchiveData`メソッドで実装済み

**フロントエンド実装状況**: ✅ **実装済み**（2026-01-23実装完了）

**実装済み項目**:
1. ✅ FormListPage: エクスポート/インポート/アーカイブボタンが実装済み
2. ✅ FormArchiveListPage: アーカイブ一覧画面が実装済み（復元ボタン、削除ボタン含む）
3. ✅ サイドメニュー: フォームアーカイブ一覧をフォーム一覧の下に追加済み
4. ✅ ルーティング・画面仕様書: FORM_ARCHIVE_LIST画面の定義が追加済み
