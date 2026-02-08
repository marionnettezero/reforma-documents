# 公開フォームでの必須条件・表示条件の動作確認とタスク整理

**作成日**: 2026-01-25  
**対象**: 項目詳細設定の「入力条件タブ」の必須条件、「条件分岐タブ」の表示条件が、公開フォーム側で指定した値で正しく評価されない事象の調査・対応

**実施済み（2026-01-25）**: T4〜T7 を実装。入力値の変化に応じて条件再評価APIを呼び、表示・必須をリアルタイムに更新するようにした。

---

## 1. 現状の整理

### 1.1 条件評価の流れ（バックエンド）

| タイミング | 処理 | 入力 | 出力 |
|-----------|------|------|------|
| フォーム表示取得 `GET /v1/public/forms/{form_key}` | `ConditionEvaluatorService::evaluate($form, $answers)` | `$answers` は **空**（`computedEvaluator->evaluate($form, [])` の結果のみ） | `condition_state` |
| STEP遷移評価 `POST /v1/forms/{form_key}/step-transition` | 同上（`current_step_key` + `answers` 付き） | **現在の answers** | `condition_state` |
| 回答送信 `POST /v1/forms/{form_key}/submit` | 同上 | **送信時の answers** | レスポンスに `condition_state` を含む |

- 表示条件（`visibility_rule`）・必須条件（`required_rule`）はいずれも **回答値 `$answers`** を参照して `ConditionEvaluatorService::evaluateRule()` で評価される。
- 比較は `rule['field']` のフィールド値 `$answers[$fieldKey]` と `rule['value']` で実施（eq / in / contains 等）。

### 1.2 公開フォームフロントエンドの実装

| 処理 | 実装 | 問題 |
|------|------|------|
| 初回ロード | `GET /v1/public/forms/{form_key}` の `res.data.form.condition_state` を `setConditionState` で表示制御に利用 | この時点の `condition_state` は **回答なし** で評価された結果のため、もともと「指定した値」に依存する表示・必須は正しくない |
| 入力値変更時 | `evaluateConditionsDebounced(currentAnswers)` を呼ぶが、**APIは呼ばず** コメント上「既存の condition_state を基に表示制御」とあるだけ | **条件の再評価が一切行われない**。表示・必須は初回のまま |
| 「次へ」クリック（STEP式） | `setCurrentStepKey(nextStep.step_key)` のみ。**`POST .../step-transition` は呼ばれていない** | STEP遷移時に `condition_state` が更新されない。遷移可否もフロントでは判定していない |
| 送信時 | `POST /v1/forms/{form_key}/submit` を実行。成功時 `res.data.condition_state` で `setConditionState` を更新 | 送信結果の `condition_state` は正しいが、**送信前の画面表示・必須チェックは古いまま** |

このため、「指定した値で評価されていない」と見える主因は、

1. **表示・必須のリアルタイム更新がない**（回答変更時に再評価APIを呼んでいない）
2. **STEP遷移時にサーバー評価を呼んでおらず、遷移後の表示・必須も更新されない**
3. **初回表示は常に「回答なし」での評価結果**のまま

という実装状況にあります。

### 1.3 プレビュー（FormPreviewPage）

- フォーム取得は `GET /v1/public/forms/{formCode}?preview=true`。
- `condition_state` の利用方法は公開フォームと同様。
- `evaluateConditionsDebounced` も **API呼び出しは行っておらず**、同じく「既存の condition_state を基に表示制御」のみ。

### 1.4 ルールの「値」の扱い（value / label）

- 条件ルールの比較値は `rule.value`（または `rule.value` の配列）として保存・評価される。
- 編集画面の `builderToRuleJson` は `item.value` / `item.valueArray` をそのまま `rule.value` に乗せている。
- **オプション型（select / radio / checkbox）で「表示ラベル」と「保存 value」が異なる場合**、ビルダー側でどちらを `item.value` にしているかが、バックエンドの `eq` / `in` と一致するかどうかに直結する。
- 「指定した値で評価されていない」が「送信時は正しいが画面では変」なのか「送信時も期待と違う」のかによって、ここを確認する必要あり。

---

## 2. タスク一覧（細かく整理）

### 2.1 必須条件・表示条件が「指定した値」で動いているか確認するタスク

| # | タスク | 内容 | 優先度 |
|---|--------|------|--------|
| T1 | 初回表示時の condition_state の前提確認 | GET 表示取得では常に `answers=[]` で評価されることを仕様として押さえ、そのうえで「初回から表示条件で隠れているフィールドが非表示になる」など期待どおりか確認する | 高 |
| T2 | 送信時に必須・表示が正しく評価されているか確認 | 表示条件・必須条件を設定したフォームで、条件を満たす／満たさない answers を送信し、必須エラー・保存対象フィールド・`condition_state` が期待通りかテストする（既存の PublicFormsApiTest のパターンで可能） | 高 |
| T3 | ルールの「値」が value / label のどちらで保存されているか確認 | 条件分岐ビルダーで select/radio の「〇〇を選んだら」を指定したとき、`visibility_rule` / `required_rule` の `value` に **option.value** が入っているか **option.label（表示文）** が入っているかを確認する。公開フォームの回答は通常 value で送るので、不一致なら「指定した値で評価されない」原因になる | 高 |

### 2.2 公開フォームで条件をリアルタイムに反映させるタスク

| # | タスク | 内容 | 優先度 |
|---|--------|------|--------|
| T4 | 条件再評価APIの追加または既存の利用 | バックエンドに「現在の answers だけで condition_state を返す」APIがあるか確認する。なければ `POST /v1/forms/{form_key}/evaluate-conditions`（例）を追加するか、既存の `POST .../step-transition` を「STEPなし・遷移なし」でも呼べる形に拡張する | 高 | ✅ 実施済み |
| T5 | 公開フォーム：回答変更時に条件再評価APIを呼ぶ | PublicFormViewPage の `evaluateConditionsDebounced` 内で、正規化した `currentAnswers` を送り、返却の `condition_state` で `setConditionState` する。`POST .../step-transition` を流用する場合は、単一フォームや「同一STEP内の変更」用に `current_step_key` を省略可能にするなどして呼び分ける | 高 | ✅ 実施済み |
| T6 | 公開フォーム：STEP「次へ」の前に step-transition を呼ぶ | 「次へ」クリック時に、`POST /v1/forms/{form_key}/step-transition` を `current_step_key` + 現在の `answers` で実行する。成功時は返却の `condition_state` で `setConditionState` してから `setCurrentStepKey` する。拒否時は既存の handleApiError / onStepTransitionError でメッセージと `condition_state` を反映する | 高 | ✅ 実施済み |
| T7 | プレビューでの同期 | FormPreviewPage でも、公開フォームと同様に「回答変更時の条件再評価」「STEP遷移時の step-transition 呼び出し」を入れるかどうか方針を決め、必要なら T5・T6 と同等の実装を行う | 中 | ✅ 実施済み |

### 2.3 仕様・テストの整理

| # | タスク | 内容 | 優先度 |
|---|--------|------|--------|
| T8 | 仕様書での前提の明文化 | 「フォーム表示取得の condition_state は回答未入力状態での評価結果であること」「表示・必須を回答に応じて変えるには条件再評価APIの利用が前提であること」を、公開フォームまたは条件分岐の仕様に追記する | 低 |
| T9 | E2Eまたは結合テストの追加 | 表示条件・必須条件を設定した公開フォームについて、「ある値を選ぶと項目が出現する／必須になる」ことを、回答変更→表示・必須の変化→送信まで含めてテストする | 中 |

---

## 3. 推奨する実施順序

1. **T2, T3**  
   送信時とルール値の仕様を確認し、「指定した値で評価されない」原因が「リアルタイム更新していないこと」なのか「value/label の不一致」なのかを切り分ける。
2. **T1**  
   初回表示の期待（回答なし前提）をはっきりさせる。
3. **T4 → T5 → T6**  
   条件再評価のAPIを整え、公開フォームで回答変更時・STEP遷移時に正しい `condition_state` を取得して表示・必須に反映する。
4. **T7**  
   プレビューも同じ体験にするか検討し、必要なら実装。
5. **T8, T9**  
   仕様の明文化と、E2E/結合テストの追加。

---

## 4. 参照箇所（コード）

- フロント（公開フォーム）  
  - `PublicFormViewPage.tsx`: `evaluateConditionsDebounced`（316–346行付近）, `condition_state` の取得・更新（160, 570–571, 644–645）, 「次へ」クリック（1366–1377）
- フロント（プレビュー）  
  - `FormPreviewPage.tsx`: `evaluateConditionsDebounced`（193–224行付近）, `condition_state` の取得（97）
- バックエンド  
  - `PublicFormsController.php`: `show`（condition_state を answers なしで評価）, `evaluateStepTransition`, `submit`
  - `ConditionEvaluatorService.php`: `evaluate`, `evaluateRule`, 比較値 `rule['value']`
- ルート  
  - `POST /v1/forms/{form_key}/evaluate-conditions`（条件再評価・リアルタイム用、body: `answers`, 任意 `preview`）
  - `POST /v1/forms/{form_key}/step-transition`（`routes/api.php`）
- 422 STEP_TRANSITION_DENIED 時は `errors.condition_state` に評価結果を含めて返却（フロントの `extractStepTransitionError` で `errors.condition_state` を参照）
