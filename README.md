# reforma-documents

ReForma の仕様ドキュメント管理リポジトリ。

## ディレクトリ構成

- `latest/`     : **最新版の仕様書のみを格納**
  - `latest/classified/` : 分類別仕様書（api, backend, common, db, frontend, notes）
  - `latest/canonical/`  : 正本（統合仕様書、OpenAPI定義）
  - `latest/adr/`        : アーキテクチャ決定記録（Architecture Decision Records）
- `previous/`   : **過去バージョンの仕様書を格納**
  - 新しいバージョンが作成された際、古いバージョンは自動的に`previous/`に移動
  - バージョン履歴の追跡と参照のため
- `tools/`      : 正本生成ツール（generate-canonical）。分類別仕様書を更新した後に正本を再生成するための Python スクリプトと README が含まれています。GitHub Actions の `generate_canonical.yml` を設定すると、`classified/**` や `tools/generate-canonical/**` の変更時に自動で実行されます。

**注意**: 旧構成（`classified/`, `canonical/`, `adr/`）は`latest/`配下に移動されました。今後は`latest/`配下のファイルを更新してください。

## 運用ルール（必須）

1. 仕様の更新は `latest/classified/<category>/` を先に更新する
2. 分類側が確定したら、正本 `latest/canonical/reforma-spec-vX.Y.Z.(md|json)` を更新する
3. 正本の冒頭（Component Manifest）に、取り込んだ分類別仕様のバージョンを明記する
4. バージョンは **v1.x.x の3桁固定**（v1.0.0 のように 0 省略禁止）

## ドキュメント管理ポリシー

### バージョン管理

- **最新版のみを`latest/`に格納**: `latest/`ディレクトリには、各仕様書の最新バージョンのみを格納します
- **古いバージョンは`previous/`に移動**: 新しいバージョンが作成された際、古いバージョンのファイル（.md と .json）は`previous/`ディレクトリに移動します
- **バージョン命名規則**: 
  - 分類別仕様書: `reforma-<category>-spec-v<major>.<minor>.<patch>.(md|json)`
  - 正本: `reforma-spec-v<major>.<minor>.<patch>.(md|json)`
  - OpenAPI: `reforma-openapi-v<major>.<minor>.<patch>.(yaml|json)`

### ファイル移動手順

新しいバージョンを作成する際は、以下の手順に従ってください：

1. 新しいバージョンのファイル（例: `reforma-frontend-spec-v0.9.0.md`）を`latest/`配下に作成
2. 対応するJSONファイルも作成（存在する場合）
3. 古いバージョンのファイル（.md と .json）を`previous/`ディレクトリに移動
   - 例: `reforma-frontend-spec-v0.1.1.*` → `previous/classified/frontend/`
4. `previous/`ディレクトリの構造は`latest/`と同じ構造を維持

## 現在の最新バージョン

### 分類別仕様書

- **フロントエンド**: `latest/classified/frontend/reforma-frontend-spec-v0.9.0.md`
- **API**: `latest/classified/api/reforma-api-spec-v0.9.1.md`
- **バックエンド**: `latest/classified/backend/reforma-backend-spec-v0.1.1.md`
- **共通**: `latest/classified/common/reforma-common-spec-v1.5.1.md`
- **DB**: `latest/classified/db/reforma-db-spec-v0.1.2.md`

### 正本

- `latest/canonical/reforma-spec-v0.1.6.md`
- `latest/canonical/reforma-spec-v0.1.6.json`

### OpenAPI 定義

ReForma API の仕様は OpenAPI 形式で管理されます。画面仕様やデータ仕様とは別にバージョン管理し、正本ファイルとして `latest/canonical/` に配置します。

- `latest/canonical/reforma-openapi-v0.9.1.yaml`
- `latest/canonical/reforma-openapi-v0.9.0.json`（JSONファイルは後で生成予定）

**注意**: 古いバージョンのファイルは`previous/`ディレクトリに移動されています。