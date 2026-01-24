# CSVエクスポート修正

## 問題

1. **`response_id`が不要なCSVに追加されている**
   - 項目（fields）のCSVエクスポートに`response_id`が追加されていた
   - `EnsureResponsesCsvHeaderMiddleware`がすべてのCSVエクスポートに`response_id`を追加していた

2. **文字化けの問題**
   - `field_key`が文字化けしていた
   - BOM（Byte Order Mark）の位置がずれていた可能性

## 原因

`EnsureResponsesCsvHeaderMiddleware`が、すべての`/v1/exports/{job_id}/download`エンドポイントに対して`response_id`を追加していました。これは回答（responses）のCSVエクスポート用のミドルウェアなので、項目（fields）のエクスポートには適用すべきではありません。

## 修正内容

### 1. `EnsureResponsesCsvHeaderMiddleware.php`の修正

CSVの内容を確認して、回答（responses）のCSVエクスポートのみに`response_id`を追加するように変更：

- CSVのヘッダー行を確認
- `submission_id`または`response_id`が含まれている場合は回答（responses）のCSV
- `field_key`が含まれている場合は項目（fields）のCSVなので、`response_id`を追加しない

### 2. BOMの扱い

`exportFields`メソッドでBOM（`\xEF\xBB\xBF`）を正しく追加しているため、ExcelでUTF-8として正しく認識されます。ミドルウェアで`response_id`を追加しないように修正したため、BOMはファイルの先頭に正しく配置されます。

## 実装ファイル

- `app/Http/Middleware/EnsureResponsesCsvHeaderMiddleware.php` - CSVの内容を確認して、回答（responses）のCSVのみに`response_id`を追加

## 期待される結果

修正後：
- 項目（fields）のCSVエクスポートには`response_id`が含まれない
- BOMが正しい位置（ファイルの先頭）に配置される
- `field_key`が正しく表示される
