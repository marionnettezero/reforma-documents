# ReForma 正本仕様書 v1.5.1

この正本仕様書は、ReForma プロジェクトにおける分類別仕様書を統合した公式ドキュメントです。v1.5.1 では、共通仕様のタイムゾーンと進捗表示の明確化、およびトースト表示ロジックの実装メモ追加に伴い、common コンポーネントのバージョンが更新されました。

## コンポーネント・マニフェスト

| 分類 | バージョン | ファイル |
| --- | --- | --- |
| common | v1.5.1 | classified/common/reforma-common-spec-v1.5.1.json |
| backend | v1.1.0 | classified/backend/reforma-backend-spec-v1.1.0.json |
| frontend | v1.1.0 | classified/frontend/reforma-frontend-spec-v1.1.0.json |
| api | v1.3.0 | classified/api/reforma-api-spec-v1.3.0.json |
| db | v1.0.0 | classified/db/reforma-db-spec-v1.0.0.json |
| notes | v1.1.0 | classified/notes/reforma-notes-v1.1.0.json |

## canonical_policy

- 各分類別仕様書を最新バージョンへ更新した後、本正本を再生成します。
- 内容の重複はコンテンツのハッシュ値で検出・排除し、バージョン番号や生成日時が新しいものを優先します。
- 競合が発生した場合は、分類別仕様書側で解決してから正本へ取り込みます。

## 更新手順

1. 各分類フォルダ（common, backend, frontend, api, db, notes）の仕様書を編集し、必要であればバージョンを繰り上げます。
2. `canonical/` フォルダにある本ファイルと JSON 版を更新し、コンポーネント・マニフェストのバージョン番号とファイルパスを修正します。
3. 分類別仕様書の更新と正本の更新を同じコミットにまとめ、プルリクエスト等でレビューを受けてからマージします。

## 変更履歴

- **v1.5.1 (2026-01-14)** – 共通仕様書のタイムゾーンと進捗表示の明確化、トースト表示実装メモの追加に伴い、common コンポーネントを v1.5.1 に更新。
- **v1.5.0 (2026-01-14)** – 正本仕様書の初版を作成。
