# ReForma 仕様書レビュー報告書

**作成日**: 2026-01-19  
**対象**: `latest/canonical`, `latest/adr`, `latest/classified` の全仕様書

---

## 1. 古い仕様書・更新が必要な仕様書

### 1.1 統合版正本仕様書（canonical）

#### ❌ `reforma-spec-v0.1.6.md` / `reforma-spec-v0.1.6.json`
- **生成日時**: 2026-01-16T00:00:00.000000+00:00
- **問題点**: 
  - 最新の実装（2026-01-19完了の条件分岐ビルダーUIなど）が反映されていない
  - コンポーネント・マニフェストのバージョン情報が古い可能性
- **推奨対応**: 最新の分類別仕様書から再生成

#### ⚠️ `reforma-openapi-v0.1.8.yaml` / `reforma-openapi-v0.1.8.json`
- **バージョン**: v0.1.8
- **問題点**: 
  - ADR-0012で提案されているOpenAPI v1.1への移行が未完了
  - 最新の実装（条件分岐ビルダーUI、表示モード機能など）が反映されているか確認が必要
- **推奨対応**: 
  - 最新の実装状況を確認し、必要に応じて更新
  - ADR-0012に基づくv1.1への移行計画を検討

---

### 1.2 分類別仕様書（classified）

#### ⚠️ `api/reforma-api-spec-v0.1.8.md` / `reforma-api-spec-v0.1.8.json`
- **バージョン**: v0.1.8
- **更新日時**: 2026-01-17T00:00:00Z
- **問題点**: 
  - 最新の実装（2026-01-19完了の条件分岐ビルダーUI）が反映されていない可能性
  - 条件分岐ビルダーUIの実装詳細が記載されていない
- **推奨対応**: 
  - 条件分岐ビルダーUIの実装内容を反映
  - フロントエンド仕様との整合性を確認

#### ✅ `frontend/reforma-frontend-spec-v0.1.1.md` / `reforma-frontend-spec-v0.1.1.json`
- **バージョン**: v0.1.1
- **生成日時**: 2026-01-14T11:37:59.767769+00:00
- **状態**: 比較的新しいが、最新の実装（条件分岐ビルダーUI、表示モード機能）が反映されているか確認が必要

#### ✅ `backend/reforma-backend-spec-v0.1.1.md` / `reforma-backend-spec-v0.1.1.json`
- **バージョン**: v0.1.1
- **生成日時**: 2026-01-14T11:37:59.885164+00:00
- **状態**: 比較的新しい

#### ✅ `common/reforma-common-spec-v1.5.1.md` / `reforma-common-spec-v1.5.1.json`
- **バージョン**: v1.5.1
- **最終更新**: v1.5.2 (2026-01-17)
- **状態**: 最新（画面タイトルとパンくずの表示仕様が追加済み）

#### ✅ `db/reforma-db-spec-v0.1.2.md` / `reforma-db-spec-v0.1.2.json`
- **バージョン**: v0.1.2
- **生成日時**: 2026-01-17T00:00:00Z
- **状態**: 最新（テーマ機能、表示モード機能、計算フィールド機能が追加済み）

---

### 1.3 ADR（Architecture Decision Records）

#### ❌ ADR-0001: Queue 実装方式
- **Status**: Proposed（保留）
- **問題点**: TBD（決定保留中）
- **推奨対応**: 実装方針を決定し、Statusを更新

#### ❌ ADR-0006: Multiple Root User Policy
- **Status**: Proposed
- **問題点**: 実装されていない（複数rootアカウント対応が未実装）
- **推奨対応**: 
  - 実装計画を検討
  - または、実装しない場合はStatusをRejectedに変更

#### ❌ ADR-0007: Full-Text Search Index
- **Status**: Proposed
- **問題点**: 実装されていない（全文検索機能が未実装）
- **推奨対応**: 
  - 実装計画を検討
  - または、実装しない場合はStatusをRejectedに変更

#### ❌ ADR-0011: Root Grant/Revoke API Endpoints
- **Status**: Proposed
- **問題点**: 実装されていない（`POST /v1/system/root/grant`、`POST /v1/system/root/revoke`が未実装）
- **推奨対応**: 
  - ADR-0006（Multiple Root Policy）の実装後に実装を検討
  - または、実装しない場合はStatusをRejectedに変更

#### ⚠️ ADR-0012: Finalization of OpenAPI v1.1 Specification
- **Status**: Proposed
- **問題点**: 
  - 現在のOpenAPIバージョンはv0.1.8で、v1.1への移行が未完了
  - 実装と仕様書の同期が不完全な可能性
- **推奨対応**: 
  - 実装と仕様書の完全な同期を実施
  - OpenAPI v1.1への移行計画を検討

---

## 2. 実装漏れの可能性がある項目

### 2.1 条件分岐ビルダーUIの仕様書への反映

#### 問題点
- **実装完了日**: 2026-01-19
- **実装内容**: 
  - `ConditionRuleBuilder`コンポーネント（複数条件対応、AND/OR論理結合、フィールドタイプ×演算子許可表、演算子別値入力UI）
  - バリデーション（自己参照チェック、フィールド存在チェック）
- **仕様書への反映状況**: 
  - `reforma-api-spec-v0.1.8.md`: 条件分岐ルールのJSON形式は記載されているが、UI実装詳細が不足
  - `reforma-frontend-spec-v0.1.1.md`: 条件分岐ビルダーUIの実装詳細が不足
  - `reforma-spec-v0.1.6.md`: 最新の実装が反映されていない

#### 推奨対応
- `reforma-frontend-spec-v0.1.1.md`に条件分岐ビルダーUIの実装詳細を追加
- `reforma-api-spec-v0.1.8.md`に条件分岐ルールのUI実装に関する補足説明を追加
- `reforma-spec-v0.1.6.md`を最新の分類別仕様書から再生成

---

### 2.2 表示モード機能の仕様書への反映

#### 問題点
- **実装完了日**: 2026-01-19
- **実装内容**: 
  - 公開フォーム: 選択肢表示（label/both/value）の切替UI
  - 管理画面プレビュー: locale+mode切替機能
- **仕様書への反映状況**: 
  - `reforma-api-spec-v0.1.8.md`: 表示モード機能（locale/modeパラメータ）は記載されている（v0.1.5で追加）
  - `reforma-frontend-spec-v0.1.1.md`: UI実装詳細が不足

#### 推奨対応
- `reforma-frontend-spec-v0.1.1.md`に表示モード機能のUI実装詳細を追加

---

### 2.3 未実装機能（ADRで提案されているが実装されていない）

#### ADR-0006: Multiple Root User Policy
- **実装状況**: 未実装
- **影響**: 複数rootアカウント対応ができない
- **推奨対応**: 実装計画を検討、またはStatusをRejectedに変更

#### ADR-0007: Full-Text Search Index
- **実装状況**: 未実装
- **影響**: 全文検索機能が利用できない
- **推奨対応**: 実装計画を検討、またはStatusをRejectedに変更

#### ADR-0011: Root Grant/Revoke API Endpoints
- **実装状況**: 未実装
- **影響**: root権限の付与・剥奪がAPI経由でできない
- **推奨対応**: ADR-0006の実装後に実装を検討、またはStatusをRejectedに変更

---

## 3. 推奨対応優先度

### 高優先度
1. **`reforma-spec-v0.1.6.md`の再生成**
   - 最新の分類別仕様書から再生成し、最新の実装状況を反映

2. **`reforma-frontend-spec-v0.1.1.md`の更新**
   - 条件分岐ビルダーUIの実装詳細を追加
   - 表示モード機能のUI実装詳細を追加

3. **`reforma-api-spec-v0.1.8.md`の確認・更新**
   - 最新の実装（条件分岐ビルダーUI、表示モード機能）が反映されているか確認
   - 必要に応じて更新

### 中優先度
4. **ADR-0012の対応**
   - 実装と仕様書の完全な同期を実施
   - OpenAPI v1.1への移行計画を検討

5. **未実装ADRの対応**
   - ADR-0006, ADR-0007, ADR-0011の実装計画を検討
   - 実装しない場合はStatusをRejectedに変更

### 低優先度
6. **ADR-0001の対応**
   - Queue実装方式の決定（TBD状態の解消）

---

## 4. まとめ

### 古い仕様書・更新が必要な仕様書
- ❌ `canonical/reforma-spec-v0.1.6.md` - 2026-01-16生成（最新の実装が反映されていない）
- ⚠️ `canonical/reforma-openapi-v0.1.8.yaml/json` - v1.1への移行が未完了
- ⚠️ `classified/api/reforma-api-spec-v0.1.8.md` - 最新の実装が反映されているか確認が必要
- ⚠️ `classified/frontend/reforma-frontend-spec-v0.1.1.md` - 最新の実装詳細が不足

### 未実装機能（ADRで提案されているが実装されていない）
- ❌ ADR-0006: Multiple Root User Policy
- ❌ ADR-0007: Full-Text Search Index
- ❌ ADR-0011: Root Grant/Revoke API Endpoints

### 実装漏れの可能性がある項目
- ⚠️ 条件分岐ビルダーUIの仕様書への反映（実装完了: 2026-01-19）
- ⚠️ 表示モード機能の仕様書への反映（実装完了: 2026-01-19）

---

## 5. 補足

- 最新の実装状況は`IMPLEMENTATION_GAP_ANALYSIS.md`を参照
- 残タスクは`remaining-tasks.md`を参照
- 仕様書の更新時は、対応するJSONファイルも同時に更新すること
