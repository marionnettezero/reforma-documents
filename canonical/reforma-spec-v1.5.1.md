# ReForma 正本仕様書 v1.5.1

このドキュメントは最新の分類別仕様書から自動生成されています。

## コンポーネント・マニフェスト

| 分類 | バージョン | ファイル |
| --- | --- | --- |
| api | v1.3.2 | classified/api/reforma-api-spec-v1.3.2.json |
| backend | v1.1.0 | classified/backend/reforma-backend-spec-v1.1.0.json |
| common | v1.5.1 | classified/common/reforma-common-spec-v1.5.1.json |
| db | v1.0.0 | classified/db/reforma-db-spec-v1.0.0.json |
| frontend | v1.1.0 | classified/frontend/reforma-frontend-spec-v1.1.0.json |

## canonical_policy

分類別仕様書を更新した後にこのスクリプトを実行し、最新の仕様書群を統合します。重複した内容はハッシュ値で排除し、バージョン番号と生成日時が新しいファイルを優先します。

## 更新手順

1. `classified/` 以下の各カテゴリの仕様書を更新してバージョンを上げます。
2. `python tools/generate-canonical/generate_canonical.py` を実行して `canonical/` フォルダに新しい正本ファイルを生成します。
3. 生成された JSON と Markdown の正本ファイルをコミットし、プルリクエスト経由でレビューを受けてマージします。

## 変更履歴

- 1.5.3 (2026-01-15): Updated API spec to v1.3.2 by merging endpoints and parameters missing in v1.3.1
- 1.5.2 (2026-01-15): Preparation for canonical update following API spec v1.3.1 release (Japanese translation and JSON)
- 1.5.1 (2026-01-14): Clarified default timezone (Asia/Tokyo) and explicit vs. UTC usage in common spec
- 1.5.0 (2026-01-14): Initial canonical spec creation
- v1.5.1 (2026-01-15): Canonical spec generated automatically.
