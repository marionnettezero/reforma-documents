# ADR-0012: Finalization of OpenAPI v1.1 Specification

**Status:** Accepted  
**Date:** 2026‑01‑14  
**Updated:** 2026‑01‑19

## Context

The API section notes that the current OpenAPI v1.1 draft lacks certain parameters and that these will be supplemented in the final specification【343970276494006†L6482-L6484】. Without a finalized specification, API consumers cannot fully rely on the contract.

## Decision

We propose to audit all existing endpoints against the implementation, identify missing request and response parameters, and update the OpenAPI v1.1 specification accordingly. The finalized document will be versioned and published alongside the canonical spec. Any breaking changes will be communicated via a deprecation policy.

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

これらのエンドポイントをOpenAPI定義（reforma-openapi-v0.10.0.yaml）およびAPI仕様書（reforma-api-spec-v0.10.0.md）に追加しました。

## Consequences

- **Clarity:** API consumers will have a complete and accurate contract, reducing integration errors.
- **Maintenance:** Requires ongoing synchronization between code and specification; a linting step should be added to CI.
- **Backward compatibility:** Newly added parameters may require clients to update; a migration plan should be provided.
