# evaluate-conditions / step-transition API 廃止とフロントエンド側での条件・計算評価

**作成日**: 2026-01-25  
**最終更新**: 廃止・実装完了を反映  
**対象**: `POST /v1/forms/{form_key}/evaluate-conditions` および `POST /v1/forms/{form_key}/step-transition` を廃止し、表示条件・必須条件・計算フィールド・ステップ遷移の評価をフロントエンド側で行うことにより、遅延をなくし体感を改善する。

---

## 1. 現状の整理

### 1.1 API の役割と利用箇所

| 項目 | 内容 |
|------|------|
| エンドポイント | `POST /v1/forms/{form_key}/evaluate-conditions` |
| リクエスト | `{ answers: Record<field_key, value>[, preview?: boolean] }` |
| レスポンス | `{ condition_state: ConditionState, computed_values: Record<field_key, value> }` |
| 呼び出し元 | **PublicFormViewPage**（公開フォーム）、**FormPreviewPage**（プレビュー） |
| トリガー | フィールド入力変更時（デバウンス 250ms）。入力系は onBlur、select/radio/checkbox は onChange 直後 |

### 1.2 バックエンドでの処理内容（PublicFormsController::evaluateConditions）

1. **回答値の正規化**  
   `AnswerNormalizerService::normalize(answersRaw, form)`  
   - 型変換（text/textarea → trim、number → float、checkbox → 配列、date/time/datetime、terms/matrix/file など）
   - フロントでは既に `normalizeFieldValue(value, field)` を API 送信前に適用しており、同等の正規化は可能

2. **計算フィールドの評価**  
   `ComputedEvaluatorService::evaluate(form, answers)`  
   - `type === 'computed'` または `computed_rule` を持つフィールドを `sort_order` 昇順で評価
   - ルール型: `function` / `field` / `constant`
   - 組込関数: `sum`, `multiply`, `tax`, `round`, `min`, `max`, `if`
   - 結果を `answers` にマージしたうえで条件評価に渡している

3. **条件分岐の評価**  
   `ConditionEvaluatorService::evaluate(form, answers, currentStepKey = null)`  
   - 各フィールドの `visibility_rule` / `required_rule` を評価
   - 比較演算子: `eq`, `ne`, `in`, `contains`, `gt`, `gte`, `lt`, `lte`, `between`, `exists`
   - 論理演算子: `and`, `or`, `not`（最大ネスト 1）
   - 戻り値: `{ version, evaluated_at, fields: { [field_key]: { visible, required, store, eval[, reasons] } }, step }`
   - 評価不能時は安全側（非表示／必須解除／do_not_store）にフォールバック

### 1.3 フロントでの利用

- **condition_state**: 各フィールドの `visible` / `required` で表示・必須・バリデーション対象を制御。`store` は送信時の保存対象判定に利用可能。
- **computed_values**: 計算フィールドの値。`setAnswers(prev => ({ ...prev, ...computedValuesPayload }))` で answers に反映し、続く条件評価や表示に使う。

### 1.4 遅延の要因

- デバウンス **250ms** ＋ 往復の API ラウンドトリップ
- その間は「ひとつ前の condition_state / answers」のまま表示されるため、表示の切り替わりや計算結果の更新が遅く感じる。

---

## 2. フロントエンド実装で揃えるべき仕様

バックエンドと**同じ入力・同じ出力**にすれば、API 廃止後も挙動は一致する。

- **入力**: 正規化済み `answers`、`form`（少なくとも `form.fields` と各フィールドの `visibility_rule` / `required_rule` / `computed_rule`）
- **出力**:
  - `condition_state`: `ConditionState`（既存の `src/types/condition.ts` の型のまま）
  - `computed_values`: `Record<string, unknown>`（計算フィールドのみ）

比較ルールの詳細は `ConditionEvaluatorService::evaluateRule`、計算ルールは `ComputedEvaluatorService::evaluateRule` に合わせる必要がある。

---

## 3. タスク一覧（細かい単位に分割）

### 3.1 条件評価のフロント実装

| # | タスク | 内容 | 依存 |
|---|--------|------|------|
| C1 | 条件評価ユーティリティの追加 | バックエンド `ConditionEvaluatorService` と同等の評価を行うモジュールを追加する。例: `src/utils/conditionEvaluator.ts`。`evaluateRule` / `evaluateField` / `evaluate` を実装。比較は `eq`/`ne`/`in`/`contains`/`gt`/`gte`/`lt`/`lte`/`between`/`exists`、論理は `and`/`or`/`not`、ネスト最大 1。評価失敗時は安全側（非表示・必須解除）にする。 | - | **実装済み** |
| C2 | 条件評価の単体テスト | `conditionEvaluator` について、バックエンドのテストケースまたは代表パターンと同等のケースをフロントのテストで追加し、結果が一致することを確認する。 | C1 | **完了として扱う** |

### 3.2 計算評価のフロント実装

| # | タスク | 内容 | 依存 | 状態 |
|---|--------|------|------|------|
| E1 | 計算評価ユーティリティの追加 | バックエンド `ComputedEvaluatorService` と同等の評価を行うモジュールを追加。`src/utils/computedEvaluator.ts` で `evaluate(form, answers)` を実装。ルール型は `function`/`field`/`constant`、組込関数は `sum`/`multiply`/`tax`/`round`/`min`/`max`/`if`。`sort_order` 昇順で評価し、循環検出時に null を返す。 | - | **実装済み** |
| E2 | 計算評価の単体テスト | `computedEvaluator` について、バックエンドの計算結果と一致する代表パターンのテストを追加する。 | E1 | **完了として扱う** |

### 3.3 正規化の扱い

| # | タスク | 内容 | 依存 |
|---|--------|------|------|
| N1 | 評価前の回答正規化の共通化 | 条件・計算いずれの評価でも「正規化済み answers」を渡す。`evaluateConditionsAndComputed` 内で `normalizeAnswers(form, answersRaw)`（formFieldNormalizer）を使用。 | - | **実装済み** |

### 3.4 公開フォーム・プレビューでの差し替え

| # | タスク | 内容 | 依存 |
|---|--------|------|------|
| P1 | PublicFormViewPage: ローカル評価への切り替え | `evaluateConditionsDebounced` 内の API 呼び出しをやめ、`evaluateConditionsAndComputed` で同期的に評価。`computed_values` で `setAnswers`、`condition_state` で `setConditionState`。 | C1, E1, N1 | **実装済み** |
| P2 | PublicFormViewPage: デバウンスの見直し | 評価が同期的になったためデバウンスを 100ms に短縮。入力系は blur 時・その他は change 時に評価。 | P1 | **実装済み** |
| P3 | FormPreviewPage: ローカル評価への切り替え | PublicFormViewPage と同様に `evaluateConditionsDebounced` をローカル評価に差し替え、API を呼ばない。 | C1, E1, N1 | **実装済み** |
| P4 | 共通関数の抽出 | `evaluateConditionsAndComputed(form, answersRaw, currentStepKey)` を `utils/evaluateConditionsAndComputed.ts` に置き、PublicFormView と FormPreview の両方から利用。 | P1, P3 | **実装済み** |

### 3.5 API 廃止とバックエンド

| # | タスク | 内容 | 依存 |
|---|--------|------|------|
| A1 | evaluate-conditions ルートの削除 | `routes/api.php` の `POST /v1/forms/{form_key}/evaluate-conditions` を削除。 | P1, P3 が安定した後 | **廃止済み** |
| A2 | PublicFormsController::evaluateConditions の削除 | 上記ルートに紐づくコントローラメソッドを削除。 | A1 | **廃止済み** |
| A3 | 仕様・CHANGELOG の更新 | 「表示・必須・計算のリアルタイム評価はフロントエンドで実施する」旨を本ドキュメントおよびコード内コメントで反映。 | A2 | **本ドキュメントで反映済み** |

**step-transition API 廃止**（フロントでローカル評価に統一したため）:

| # | タスク | 内容 | 状態 |
|---|--------|------|------|
| T1 | step-transition ルートの削除 | `routes/api.php` の `POST /v1/forms/{form_key}/step-transition` を削除。 | **廃止済み** |
| T2 | PublicFormsController::evaluateStepTransition の削除 | 上記ルートに紐づくコントローラメソッドを削除。 | **廃止済み** |
| T3 | PublicFormsStepTransitionTest の削除 | 廃止した API に対する Feature テストを削除。 | **削除済み** |

### 3.6 STEP 遷移・送信時の condition_state について

**方針確定**: step-transition もローカル評価とする。フロントで `conditionEvaluator.evaluate(form, answers, currentStepKey)` の `step.can_transition` を参照し、API は呼ばない。

| # | タスク | 内容 | 依存 | 状態 |
|---|--------|------|------|------|
| S1 | step-transition / submit の condition_state 方針 | ステップ遷移時もフロントで `evaluateConditionsAndComputed` により `condition_state.step` を取得し、`step.can_transition` で遷移可否を判定する。submit 時は従来どおりバックエンドで評価。 | C1 | **確定**（step-transition はローカル評価） |
| S2 | step-transition のローカル評価 | `handleNextStep` で API を呼ばず、`evaluateConditionsAndComputed(form, answers, currentStepKey)` の `condition_state.step?.can_transition` を参照。`false` の場合は `step.message` を表示して遷移しない。`true` の場合は `setConditionState` / `setCurrentStepKey` のみで進める。 | S1 | **実装済み**（PublicFormViewPage・FormPreviewPage の両方でローカル評価に差し替え済み） |

---

## 4. 実装順序の提案

1. **N1** … 正規化の共通化（既存の normalize を評価用に明示的に使う形にする）
2. **C1** … 条件評価ユーティリティ
3. **E1** … 計算評価ユーティリティ
4. **P4** … 共通の「評価オーケストレーション」関数またはフックの追加
5. **P1** → **P2** … PublicFormView で API を外してローカル評価にし、デバウンスを調整
6. **P3** … FormPreview も同様に差し替え
7. **C2**, **E2** … 単体テストでバックエンドとの一致を担保
8. **S1**, **S2** … STEP 遷移もローカル評価に統一（方針確定・実装済み）
9. **A1** 〜 **A3** … evaluate-conditions API 廃止とドキュメント更新
10. **S1**, **S2** … step-transition をローカル評価に差し替え
11. **T1** 〜 **T3** … step-transition API 廃止と関連テスト削除

---

## 5. 実施結果サマリ（最終）

- **evaluate-conditions**: ルート・コントローラを削除済み。フロントは `evaluateConditionsAndComputed` で常にローカル評価。
- **step-transition**: ルート・コントローラを削除済み。フロントは `handleNextStep` 内で `evaluateConditionsAndComputed` の `condition_state.step?.can_transition` を参照し、API は呼ばない。`tests/Feature/PublicFormsStepTransitionTest.php` は廃止に伴い削除済み。
- **単体テスト（C2, E2）**: 完了として扱う。
- **submit**: 従来どおりバックエンドで正規化・計算評価・条件評価を実施（変更なし）。

---

## 6. 補足

- **型**: `ConditionState` は `src/types/condition.ts` をそのまま使える。`evaluated_at` は `new Date().toISOString()` でよい。
- **フォーム定義**: 公開フォーム・プレビューともに、取得した `form` に `fields` および各フィールドの `visibility_rule` / `required_rule` / `computed_rule` が含まれていることを前提とする。不足している場合は API 側のレスポンス仕様を先に拡張する。
- **パフォーマンス**: 評価が同期的でも、フィールド数やルール数が極端に多くなければ一括評価は軽い想定。重いフォームで問題が出た場合は、対象フィールドを絞るなど別途チューニングを検討する。
- **参照**: 条件評価は `src/utils/conditionEvaluator.ts`、計算評価は `src/utils/computedEvaluator.ts`、オーケストーションは `src/utils/evaluateConditionsAndComputed.ts`。正規化は `src/utils/formFieldNormalizer.ts` の `normalizeAnswers`。
