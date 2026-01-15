# reforma-documents

ReForma の仕様ドキュメント管理リポジトリ。

## ディレクトリ構成

- `classified/` : **日常的に更新する一次仕様（分類別）**
- `canonical/`  : **正本（印刷/PDF・参照用）**（classified を統合した成果物）
- `adr/`        : 保留/決定事項（Architecture Decision Records）
- `tools/`      : 正本生成ツール（generate-canonical）。分類別仕様書を更新した後に正本を再生成するための Python スクリプトと README が含まれています。GitHub Actions の `generate_canonical.yml` を設定すると、`classified/**` や `tools/generate-canonical/**` の変更時に自動で実行されます。

## 運用ルール（必須）

1. 仕様の更新は `classified/<category>/` を先に更新する
2. 分類側が確定したら、正本 `canonical/reforma-spec-vX.Y.Z.(md|json)` を更新する
3. 正本の冒頭（Component Manifest）に、取り込んだ分類別仕様のバージョンを明記する
4. バージョンは **v1.x.x の3桁固定**（v1.0.0 のように 0 省略禁止）

## いまの正本

分類別仕様書の更新（v1.5.3）に合わせて、正本の最新版を **v1.5.3** に更新しました。以下のファイルが現在の正本です。

- `canonical/reforma-spec-v1.5.4.md`
- `canonical/reforma-spec-v1.5.4.json`

## いまの OpenAPI 定義

ReForma API の仕様は OpenAPI 形式で管理されます。画面仕様やデータ仕様とは別にバージョン管理し、正本ファイルとして `canonical/` に配置します。

- `canonical/reforma-openapi-v1.3.0.yaml`
- `canonical/reforma-openapi-v1.3.0.json`