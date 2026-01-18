# ADR-0012: Finalization of OpenAPI v1.1 Specification

**Status:** Accepted  
**Date:** 2026‑01‑14  
**Updated:** 2026‑01‑19

## Context

APIセクションでは、現在のOpenAPI v1.1ドラフトには特定のパラメータが不足しており、これらは最終仕様で補完されることが記載されています【343970276494006†L6482-L6484】。最終化された仕様がない場合、APIコンシューマーは契約に完全に依存することができません。

## Decision

実装に対してすべての既存エンドポイントを監査し、不足しているリクエストおよびレスポンスパラメータを特定し、それに応じてOpenAPI v1.1仕様を更新することを提案します。最終化されたドキュメントはバージョン管理され、正本仕様とともに公開されます。破壊的変更は、非推奨ポリシーを通じて通知されます。

## Implementation

実装コードとの整合性を確認し、以下の12個のエンドポイントが不足していることを確認しました：

1. GET /v1/health - ヘルスチェック（認証不要）
2. POST /v1/forms/{form_key}/step-transition - STEP遷移評価（認証不要）
3. POST /v1/responses/{id}/notifications/resend - 通知再送（system_admin権限必須）
4. POST /v1/responses/{id}/pdf/regenerate - PDF再生成（system_adminまたはroot-only権限必須）
5. GET /v1/system/themes - テーマ一覧（system_admin権限必須）
6. POST /v1/system/themes - テーマ作成（system_admin権限必須）
7. GET /v1/system/themes/{id} - テーマ詳細（system_admin権限必須）
8. PUT /v1/system/themes/{id} - テーマ更新（system_admin権限必須、プリセットテーマはroot-only）
9. DELETE /v1/system/themes/{id} - テーマ削除（system_admin権限必須）
10. GET /v1/system/themes/{id}/usage - テーマ使用状況（system_admin権限必須）
11. POST /v1/system/themes/{id}/copy - テーマコピー（system_admin権限必須）
12. GET /v1/system/roles - ロール一覧（system_admin権限必須）

これらのエンドポイントをOpenAPI定義（reforma-openapi-v0.9.1.yaml）およびAPI仕様書（reforma-api-spec-v0.9.1.md）に追加しました。

## Consequences

- **明確性:** APIコンシューマーは完全で正確な契約を持つことができ、統合エラーを減らします。
- **保守:** コードと仕様書の継続的な同期が必要です。CIにリンティングステップを追加する必要があります。
- **後方互換性:** 新しく追加されたパラメータにより、クライアントの更新が必要になる場合があります。移行計画を提供する必要があります。
