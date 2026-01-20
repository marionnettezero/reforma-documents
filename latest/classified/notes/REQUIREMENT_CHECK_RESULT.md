# 要件適合性チェック結果

## 対象ルート
- `/forms/1/edit` (F-02 フォーム編集)
- `/forms/1/items` (F-03 フォーム項目設定)
- `/forms/1/preview` (F-04 フォームプレビュー)
- `/f/form_001` (U-01 公開フォーム)

## 確認日時
2026-01-13

---

## 1. F-02 フォーム編集 (`/forms/1/edit`)

### ✅ 実装済み
- フォーム基本情報の編集（code, status, 公開期間、回答期間）
- 翻訳（translations）の編集
- 通知設定（ユーザー通知、管理者通知）
- テーマ設定
- ファイルアップロード（PDFテンプレート、添付ファイル）

### ⚠️ 改善点
- 特に問題なし（条件分岐ルールの編集はF-03で実装）

---

## 2. F-03 フォーム項目設定 (`/forms/1/items`)

### ✅ 実装済み
- フィールドの作成・編集・削除
- STEP/GROUP/項目の階層構造対応
- 条件分岐ルールのビルダー（visibility_rule, required_rule, step_transition_rule）
- 条件分岐ビルダーの基本機能：
  - field_selector（フィールド選択）
  - operator_selector（演算子選択）
  - value_input（値入力）
  - AND/OR論理結合（logicalOp）
  - 最大条件数10個の制約（`builder.items.length >= 10`）
  - 自己参照チェック（currentFieldKeyとの比較）
  - フィールド存在チェック

### ❌ 不足・改善点

#### 2.1 ネスティング制約（max_nesting=1）の実装不足
**仕様書要件:**
- `condition-ui-spec-v1.0.json`: `"nesting": "max_1_level_v1"`
- `ReForma_条件分岐_実装整理パック_v1.0.json`: `"max_nesting": 1`

**現状:**
- 現在の実装では、ネスティング（入れ子）の制約が実装されていない
- `builderToRuleJson`関数では、単一条件または複数条件のAND/OR結合のみをサポート
- ネスティング構造（例: `{op: "and", items: [{op: "or", items: [...]}]}`）の生成・検証が行われていない

**推奨対応:**
```typescript
// FormItemPage.tsx の builderToRuleJson 関数に追加
function builderToRuleJson(builder: ConditionRuleBuilder | null, ...): any {
  // ネスティング深度チェックを追加
  // 現在は1レベル（AND/ORの直接結合）のみ許可
  // 将来的にネスティングが必要な場合は、深度を追跡する必要がある
}
```

#### 2.2 exclusive_with制約の実装不足
**仕様書要件:**
- `condition-ui-spec-v1.0.json`: `"exclusive_with": "is_required"` (required_ruleに対して)

**現状:**
- `is_required`（固定必須）と`required_rule`（条件付き必須）の排他制約が実装されていない
- 両方が同時に有効になる可能性がある

**推奨対応:**
```typescript
// FormItemPage.tsx のフィールド編集UIに追加
// required_ruleが有効な場合、is_requiredを無効化
// is_requiredが有効な場合、required_ruleを無効化
```

#### 2.3 条件分岐ルールの保存時のバリデーション強化
**仕様書要件:**
- `ReForma_API_条件分岐評価結果IF_追補_v1.0.patch.json`: ルールが不正な場合、`CONDITION_RULE_INVALID`エラーを返す

**現状:**
- クライアント側でのバリデーションは一部実装されているが、以下の点で不足：
  - 演算子とフィールドタイプの互換性チェック（一部実装済み）
  - 値の型チェック（数値、日付など）
  - ネスティング深度チェック（未実装）

**推奨対応:**
- 保存前にルールの完全性をチェック
- エラー時はユーザーに分かりやすいメッセージを表示

---

## 3. F-04 フォームプレビュー (`/forms/1/preview`)

### ✅ 実装済み
- フォーム基本情報の表示
- フィールドのread-only表示
- 条件分岐評価に基づく表示制御（簡易版）
- ロケール切替
- 表示モード切替（label/both/value）

### ❌ 不足・改善点

#### 3.1 condition_stateの取得が簡易的
**仕様書要件:**
- `ReForma_API_条件分岐評価結果IF_追補_v1.0.patch.json`: 公開フォームGET APIから`condition_state`を取得

**現状:**
- `FormPreviewPage.tsx`（420-440行目）で、簡易的な初期状態のみを生成
- 実際のAPIから`condition_state`を取得していない
- `visibility_rule`が存在しない場合は表示とする簡易処理のみ

**推奨対応:**
```typescript
// FormPreviewPage.tsx の fetchFormData 関数を修正
// 公開フォームAPI（/v1/public/forms/{form_key}）を呼び出して
// condition_stateを取得するか、管理画面用のAPIにcondition_stateを含める
```

#### 3.2 条件分岐評価のリアルタイム更新
**現状:**
- プレビュー画面では条件分岐評価が静的（初期状態のみ）
- 実際のフォーム入力時の動的な表示制御を確認できない

**推奨対応:**
- プレビュー用のダミー回答値を設定できるUIを追加
- 回答値に基づいて条件分岐評価を再実行（API呼び出しまたはクライアント側評価）

---

## 4. U-01 公開フォーム (`/f/form_001`)

### ✅ 実装済み
- フォーム基本情報の表示
- フィールドの動的レンダリング
- condition_stateの取得と表示制御
- バリデーション（必須チェック）
- 送信処理
- STEP_TRANSITION_DENIEDエラーの処理
- テーマトークンの適用

### ❌ 不足・改善点

#### 4.1 ステップ遷移UIの実装不足
**仕様書要件:**
- `form-feature-spec-v1.0.complete.json`: ステップモード（`"input_mode": "step"`）のサポート
- `condition-ui-spec-v1.0.json`: ステップ遷移条件（`transition_rule`）の評価

**現状:**
- `PublicFormViewPage.tsx`のコメントには「ステップ遷移（複数ページフォーム対応）」とあるが、実際のUI実装が見当たらない
- 現在は単一ページのフォーム送信のみ
- ステップ遷移のボタン（「次へ」「戻る」）が実装されていない
- 現在のステップの表示・管理が実装されていない

**推奨対応:**
```typescript
// PublicFormViewPage.tsx に以下を追加：
// 1. 現在のステップを管理するstate
// 2. ステップ遷移API（POST /v1/public/forms/{form_key}/step-transition）の呼び出し
// 3. 「次へ」ボタン（現在のステップのtransition_ruleを評価）
// 4. 「戻る」ボタン（前のステップへ戻る）
// 5. ステップインジケーター（現在のステップ位置を表示）
```

#### 4.2 条件分岐評価のリアルタイム更新
**仕様書要件:**
- `ReForma_API_条件分岐評価結果IF_追補_v1.0.patch.json`: 回答値変更時に条件分岐を再評価

**現状:**
- `evaluateConditionsDebounced`関数（469-499行目）が定義されているが、実際のAPI呼び出しが実装されていない
- コメントに「リアルタイム評価が必要な場合は、条件分岐評価APIを呼び出す」とあるが未実装

**推奨対応:**
```typescript
// PublicFormViewPage.tsx の evaluateConditionsDebounced 関数を実装
// 条件分岐評価API（POST /v1/public/forms/{form_key}/evaluate-conditions）を呼び出し
// または、公開フォームGET APIにanswersパラメータを追加して再取得
```

#### 4.3 計算フィールド（computed）の評価
**仕様書要件:**
- `form-feature-spec-v1.0.complete.json`: 計算フィールドのサポート

**現状:**
- `FieldComponent`で`computed`タイプの表示は実装されているが、実際の計算処理が実装されていない
- `computed_rule`の評価が行われていない

**推奨対応:**
- 計算フィールドの評価ロジックを実装
- 回答値変更時に計算フィールドを再評価

---

## 5. 共通の改善点

### 5.1 エラーハンドリングの統一 ✅ 対応済み
**現状:**
- 各ページでエラーハンドリングが個別に実装されている
- エラーメッセージの表示方法が統一されていない

**対応内容:**
- `src/utils/errorHandler.ts` を作成
  - `extractFieldErrors`: フィールドエラーの抽出
  - `extractStepTransitionError`: ステップ遷移エラーの抽出
  - `handleApiError`: 統合エラーハンドリング関数
- `PublicFormViewPage.tsx` で共通エラーハンドリングを使用するように修正
- エラーメッセージの多言語対応は `errorCodes.ts` の `extractToastMessage` で既に対応済み

**実装日:** 2026-01-13

### 5.2 型定義の統一 ✅ 対応済み
**現状:**
- `ConditionState`型が各ページで個別に定義されている
- 型定義の重複がある

**対応内容:**
- `src/types/condition.ts` を作成
  - `ConditionState`: 条件分岐評価結果
  - `FieldConditionState`: フィールドの条件分岐状態
  - `StepTransitionState`: ステップ遷移状態
  - `ConditionReason`: 評価理由
- `FormPreviewPage.tsx` と `PublicFormViewPage.tsx` で共通型定義を使用するように修正

**実装日:** 2026-01-13

### 5.3 テストカバレッジ
**現状:**
- 条件分岐機能のテストが不足している可能性

**推奨対応:**
- 条件分岐ルールのビルダーのテスト
- 条件分岐評価のテスト
- ステップ遷移のテスト

**備考:** テストカバレッジの向上は今後の課題として残す

---

## 優先度別まとめ

### 🔴 高優先度（必須対応）
1. **ステップ遷移UIの実装** (U-01)
   - ステップモードフォームの基本機能が未実装

2. **condition_stateの正しい取得** (F-04)
   - プレビュー画面で実際の条件分岐評価が確認できない

### 🟡 中優先度（推奨対応）
3. **ネスティング制約の実装** (F-03)
   - 仕様書で要求されているが未実装

4. **exclusive_with制約の実装** (F-03)
   - 仕様書で要求されているが未実装

5. **条件分岐評価のリアルタイム更新** (U-01)
   - ユーザー体験の向上

### 🟢 低優先度（改善提案）
6. **計算フィールドの評価** (U-01)
7. ~~**エラーハンドリングの統一**~~ ✅ 対応済み (2026-01-13)
8. ~~**型定義の統一**~~ ✅ 対応済み (2026-01-13)
9. **テストカバレッジの向上**

---

## 参考資料
- `01.ReForma-basic-spec-v1.1-consolidated.final.json`
- `form-feature-spec-v1.0.complete.json`
- `condition-ui-spec-v1.0.json`
- `condition-ui-examples-v1.0.json`
- `ReForma_API_条件分岐評価結果IF_追補_v1.0.patch.json`
- `ReForma_条件分岐_実装整理パック_v1.0.json`
- `ReForma_条件分岐_評価結果IF_v1.0.json`
