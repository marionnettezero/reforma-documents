# テーマ複製・エクスポート／インポートのデータ欠損確認

テーマの**複製**（copy）と**エクスポート→インポート**（CSV）において、データ損失が発生しないかをテーブル定義と実装の照合で確認した結果をまとめる。

---

## 1. テーマのエクスポート／インポート

### 1.1 仕様

- **エクスポート**: `ThemeExportJob` が全テーマを CSV 形式で出力。進捗ジョブで非同期実行。
- **インポート**: `ThemeImportJob` が CSV をパースして行ごとに `Theme::create` で新規作成。`theme_code` パラメータで全行に共通のコードを指定可能。

### 1.2 結果：テーブル照合後の修正済み

もともとエクスポートCSVに **updated_by** が含まれておらず、インポートでも **updated_by** を渡していなかった。テーブル定義との照合で抜けと判断し、以下を修正した。

- **ThemeExportJob**: 取得カラム・CSVヘッダー・各行に `updated_by` を追加。
- **ThemeImportJob**: 検証済み行に `updated_by` を追加。CSVに列があればその値（数値）、なければ実行ユーザーIDを使用。

---

## 2. テーマ複製（copy）

### 2.1 仕様

- **ThemesController::copy**: 既存テーマを指定し、リクエストで `code` / `name` / `description` を受け取る。  
  `theme_tokens` と `custom_style_config` は元テーマからそのままコピー。`is_preset` は false、`is_active` は元の値をコピー。

### 2.2 結果：テーブル照合後の修正済み

複製時の `Theme::create` に **updated_by** が含まれておらず、新規テーマの `updated_by` が null になっていた。  
`'updated_by' => $user->id` を追加済み。

---

## 3. テーブル定義との照合

マイグレーション `2026_01_01_000002_create_themes_table.php` のカラムと、エクスポート・インポート・複製で扱う項目を照合した。

### 3.1 themes テーブル

| カラム（id/timestamps/deleted_at 除く） | エクスポート | インポート | 複製 |
|----------------------------------------|--------------|------------|------|
| code | ✓ CSV | ✓ CSV または theme_code パラメータ | ✓ リクエスト必須 |
| name | ✓ | ✓ | ✓ リクエスト必須 |
| description | ✓ | ✓ | ✓ リクエスト |
| theme_tokens | ✓ | ✓ | ✓ 元テーマからコピー |
| custom_style_config | ✓ | ✓ | ✓ 元テーマからコピー |
| is_preset | ✓ | ✓ | ✓ 常に false（仕様） |
| is_active | ✓ | ✓ | ✓ 元テーマからコピー |
| created_by | ✓ | ✓（行の値または userId） | ✓ user->id |
| updated_by | ✓ **追加済み** | ✓ **追加済み**（行の値または userId） | ✓ **追加済み**（従来抜け） |
| deleted_by | — | 新規のため未設定（null） | 新規のため未設定（null） |

エクスポートは「論理削除済みを除外」したテーマのみ対象。  
created_at / updated_at はエクスポートには含まれるが、インポートでは新規作成のため DB のデフォルト（現在時刻）が使われ、CSVの日時は復元しない仕様。

### 3.2 今回の修正（テーブル照合で判明した抜け）

- **複製時の `themes.updated_by`**: `Theme::create` に `'updated_by' => $user->id` を追加。
- **エクスポート CSV の `updated_by`**: 取得カラム・ヘッダー・データ行に `updated_by` を追加。
- **インポート時の `updated_by`**: `validatedRows` に `'updated_by' => $updatedBy` を追加。CSVに列があって数値ならその値、否則は `$this->userId`。

---

## 4. 参照した実装

| 処理 | ファイル・メソッド |
|------|--------------------|
| エクスポート | `ThemeExportJob::export()` |
| インポート | `ThemeImportJob::import()` |
| 複製 | `ThemesController::copy()` |
| テーブル定義 | `database/migrations/2026_01_01_000002_create_themes_table.php` |

---

## 5. 結論

- **エクスポート→インポート**: テーブル上のデータカラム（code, name, description, theme_tokens, custom_style_config, is_preset, is_active, created_by, **updated_by**）はすべて CSV に出し入れされる。日付は監査用にエクスポートするが、インポートでは新規のため DB の現在時刻が使われる。
- **テーマ複製**: 元テーマからコピーする項目は漏れなく引き継がれる。`updated_by` が未設定だった抜けを修正済み。
