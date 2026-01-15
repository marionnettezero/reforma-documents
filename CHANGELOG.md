# Changelog

## v1.5.3 - 2026-01-15

分類別仕様書 **api v1.3.2** のリリースに伴い、旧 API 仕様 v1.3.0 で定義されていたが v1.3.1 で漏れていたエンドポイントやパラメータを統合しました。これにより、v1.3.0 と v1.3.1 の内容をすべて含む統合版となっています。機械共有用 JSON ファイルも v1.3.2 に更新しました。他の分類（common, backend, frontend, db, notes）のバージョンは変更ありません。

- classified/api v1.3.2  – v1.3.1 を基に旧バージョン v1.3.0 の欠落分を統合
- classified/common v1.5.1
- classified/backend v1.1.0
- classified/frontend v1.1.0
- classified/db v1.0.0
- classified/notes v1.1.0

## v1.5.2 - 2026-01-15

分類別仕様書 **api v1.3.1** のリリースに伴い、正本への取り込み用に API 仕様書を全面更新しました。今回の更新では、API 仕様を全文日本語化し、機械共有用の JSON ファイルも生成しました。他の分類（common, backend, frontend, db, notes）のバージョンは変更ありません。

- classified/api v1.3.1  – OpenAPI v1.3.0 に基づく全面更新（日本語化と JSON 追加）
- classified/common v1.5.1
- classified/backend v1.1.0
- classified/frontend v1.1.0
- classified/db v1.0.0
- classified/notes v1.1.0

## v1.5.1 - 2026-01-15

分類別仕様書 **common v1.5.1** のリリースに伴い、正本を v1.5.1 へ更新しました。今回の変更では、共通仕様書でタイムゾーンや非同期処理の進捗表示の取り扱いを明確にし、トースト表示メッセージの実装メモを追記しています。また、他の分類（backend, frontend, api, db, notes）のバージョンは変更ありません。

- classified/common v1.5.1  – タイムゾーンと進捗エンドポイントの明確化、トースト表示実装メモを追加
- classified/backend v1.1.0
- classified/frontend v1.1.0
- classified/api v1.3.0
- classified/db v1.0.0
- classified/notes v1.1.0

## v1.5.0 - 2026-01-14

初版の正本仕様書を生成し、各分類別の最新バージョンを統合しました。

- classified/common v1.5.0
- classified/backend v1.1.0
- classified/frontend v1.1.0
- classified/api v1.3.0
- classified/db v1.0.0
- classified/notes v1.1.0

## openapi-v1.3.0 - 2026-01-15

OpenAPI 仕様書 (v1.3.0) を独立した正本として追加しました。API の変更履歴は画面仕様とは別に管理し、リポジトリの `canonical/` ディレクトリに YAML と JSON の両形式で配置しています。

- canonical/reforma-openapi-v1.3.0.yaml
- canonical/reforma-openapi-v1.3.0.json