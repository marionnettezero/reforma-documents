# 計算ルール (computed_rule) if 関数：演算子指定のタスク整理

## 0. ネストについて（画面上の制約）

**現状**:
- **データ構造・評価側**: バックエンド／フロントの評価器は、引数に「ルール（function / field / constant）」をネストする形を**既にサポート**している（例: if の第1引数に function のルールを渡せる）。
- **画面上 (ComputedRuleEditor)**:
  - 引数の型は **「フィールド参照」と「定数値」の 2 種類のみ**（`ComputedRuleArg` = field | constant）。
  - **「引数に関数（別の関数呼び出し）を指定する」選択肢がない**ため、`if(compare(...), then, else)` のようなネストを**UI からは組み立てられない**。
- そのため **「演算子を指定可能にする」＝ compare を追加するだけでは不十分**で、**画面上でネストができるようにする改善**が必要になる。

**結論**:  
「演算子指定」を画面から使えるようにするには、**計算ルールの画面上でネストを可能にする改善**（引数タイプに「関数」を追加し、その引数で別の関数＝例: compare を選べるようにする）が前提／セットになる。タスク一覧では「F0: ネスト対応」として明示する。

---

## 1. 現状の正確な情報

### 1.1 computed_rule の構造（共通）

- **ルール型**: `function` | `field` | `constant`
- **function**: `{ type: "function", name: string, args: (rule | value)[] }`
- **field**: `{ type: "field", field_key: string }`
- **constant**: `{ type: "constant", value: number | string | boolean }`
- **組込関数**: sum, multiply, tax, round, min, max, **if**

### 1.2 if 関数の現仕様

- **シグネチャ**: `if(condition, true_value, false_value)` — 引数 3 個
- **第1引数 (condition)**: 任意の値（field / constant / 関数の戻り値）→ **真理値として解釈**（truthy/falsy）
- **第2・第3引数**: condition が truthy なら true_value、そうでなければ false_value を返す
- **制約**: 「フィールド A が 5 と等しい」「フィールド A が 10 より大きい」といった**演算子付き比較は表現できない**（条件は「値の有無・真偽」のみ）

**例（現状）**:
- `if(is_member, 100, 0)` → is_member が truthy なら 100、否则 0
- 「数量が 10 以上なら 1、否则 0」を **if 単体では書けない**（比較演算子がないため）

### 1.3 参照：条件ルール (visibility_rule / required_rule) の演算子

- **ConditionEvaluatorService**（バックエンド）・**conditionEvaluator.ts**（フロント）で使用
- **比較ルール構造**: `field`（フィールドキー）, `operator`, `value`（比較値・リテラル）
- **対応演算子**: eq, ne, in, contains, gt, gte, lt, lte, between, exists（および and, or, not）
- 計算ルール側で「演算子を指定可能にする」場合は、この演算子セットとの**揃え**を推奨

---

## 2. 方針：演算子指定の入れ方

### 2.1 推奨：組込関数 `compare(left, operator, right)` を追加

- **シグネチャ**: `compare(left, operator, right)` → **boolean**
- **left / right**: 既存の rule（field / constant / 関数の戻り値）をそのまま利用
- **operator**: 文字列定数（例: "eq", "ne", "gt", "gte", "lt", "lte", "contains" など）
- **利用例**: `if(compare(フィールド参照, "gte", 定数10), 1, 0)` のように、**if の第1引数に compare の結果**を渡す
- **利点**
  - if の既存 3 引数仕様は変更不要（後方互換）
  - computed_rule の型は function/field/constant のまま
  - 条件ルールと同様の演算子名で統一可能

### 2.2 対応する演算子（案）

| 演算子   | 意味           | 備考 |
|----------|----------------|------|
| eq       | 等しい         | 条件ルールと同様 |
| ne       | 等しくない     | 同上 |
| gt       | より大きい     | 数値比較 |
| gte      | 以上           | 数値比較 |
| lt       | より小さい     | 数値比較 |
| lte      | 以下           | 数値比較 |
| contains | 文字列の包含   | 左が右を含むか |
| in       | 右（配列）に含まれるか | value 側が配列の場合は検討 |
| exists   | 値が存在するか | 単項に近いが right は無視などで対応可 |

- 初期実装では **eq, ne, gt, gte, lt, lte, contains** を優先し、in / exists / between は必要に応じて追加する形が扱いやすい。

---

## 3. タスク一覧（正確な対象ファイル・内容）

### 3.1 バックエンド (Laravel)

| # | タスク | 対象ファイル・内容 |
|---|--------|---------------------|
| B1 | **compare 関数の実装** | `app/Services/ComputedEvaluatorService.php`<br>• `evaluateFunction` の match に `'compare' => $this->functionCompare($evaluatedArgs)` を追加<br>• `functionCompare(array $args): bool` を新規実装：第1・第2引数を評価値、第2引数を演算子文字列として、eq/ne/gt/gte/lt/lte/contains を処理（既存 ConditionEvaluatorService の compareEqual / compareNumeric / compareContains と同等ロジックを流用または共通化） |
| B2 | **compare の引数検証** | 上記 `functionCompare` 内で、引数 3 個であること・operator が許可リストに含まれることをチェックし、不正時は Exception |
| B3 | **単体テストの追加** | `tests/Unit/ComputedEvaluatorServiceTest.php`<br>• `compare` のテスト（eq, ne, gt, gte, lt, lte, contains）<br>• `if(compare(field_ref, "eq", constant), then, else)` の形で if と組み合わせたテスト |

### 3.2 フロントエンド (React)

| # | タスク | 対象ファイル・内容 |
|---|--------|---------------------|
| **F0** | **ネスト対応（引数に関数を指定可能にする）** | `src/components/ComputedRuleEditor.tsx`<br>• **型**: `ComputedRuleArg` に `{ type: "function"; name: string; args: ComputedRuleArg[] }` を追加（引数が再帰的に function / field / constant を持てるようにする）<br>• **UI**: 各引数の「タイプ」に **「関数」** を追加。選択時はその引数用に**ネストした編集 UI**（関数選択＋その引数）を表示する<br>• **parse/generate**: 既存の parseComputedRuleJson / generateComputedRuleJson が引数内の function を正しく読み書きできるようにする<br>• **バリデーション**: 引数が function の場合はその中身も再帰的にバリデーション（循環・未選択など）<br>※ これにより「if の第1引数 = compare(...)」を画面から組み立てられるようになる |
| F1 | **compare 関数の評価ロジック** | `src/utils/computedEvaluator.ts`<br>• `evaluateFunction` の switch に `case "compare": return functionCompare(evaluatedArgs);` を追加<br>• `functionCompare(args: unknown[]): boolean` を実装（第1・第3引数を値、第2引数を演算子として eq/ne/gt/gte/lt/lte/contains を処理）。`conditionEvaluator.ts` の compareEqual / compareNumeric / compareContains と同等の挙動に揃える |
| F2 | **ComputedRuleEditor に compare を追加** | `src/components/ComputedRuleEditor.tsx`<br>• `COMPUTED_FUNCTIONS` に compare を追加（name: "compare", label/description, minArgs: 3, maxArgs: 3, argLabels: ["左辺", "演算子", "右辺"]）<br>• F0 により「引数タイプ = 関数」を選んだときに compare を選べるようになる |
| F3 | **演算子の UI 選択** | `src/components/ComputedRuleEditor.tsx`<br>• compare の第2引数が「定数」かつ演算子用である場合、入力欄を **ドロップダウン**（eq, ne, gt, gte, lt, lte, contains）にし、選択値を constant として保存する<br>• 既存の「引数は field / constant / function のいずれか」のまま、演算子は constant の文字列で持つ |
| F4 | **型・バリデーション** | `src/components/ComputedRuleEditor.tsx`<br>• compare の引数バリデーション：第2引数が許可演算子リストに含まれること、第1・第3引数が有効な rule であることをチェック<br>• 必要に応じて `ComputedRuleArg` の定数で string を明示（演算子用） |

### 3.3 仕様・ドキュメント

| # | タスク | 内容 |
|---|--------|------|
| D1 | **computed_rule 仕様の更新** | 利用可能な組込関数に `compare(left, operator, right)` を追記し、演算子一覧（eq, ne, gt, gte, lt, lte, contains）と意味、使用例（if と組み合わせる例）を記載 |
| D2 | **CHANGELOG** | バックエンド・フロントエンド両方の CHANGELOG に「computed_rule の if で比較演算子を使うため compare 関数を追加」旨を記載 |

---

## 4. データ構造の例（compare 採用時）

### 4.1 例：「数量が 10 以上なら 1、否则 0」

```json
{
  "type": "function",
  "name": "if",
  "args": [
    {
      "type": "function",
      "name": "compare",
      "args": [
        { "type": "field", "field_key": "quantity" },
        { "type": "constant", "value": "gte" },
        { "type": "constant", "value": 10 }
      ]
    },
    { "type": "constant", "value": 1 },
    { "type": "constant", "value": 0 }
  ]
}
```

### 4.2 例：「フィールド A が文字列 "ok" を含むなら 100、否则 0」

```json
{
  "type": "function",
  "name": "if",
  "args": [
    {
      "type": "function",
      "name": "compare",
      "args": [
        { "type": "field", "field_key": "field_a" },
        { "type": "constant", "value": "contains" },
        { "type": "constant", "value": "ok" }
      ]
    },
    { "type": "constant", "value": 100 },
    { "type": "constant", "value": 0 }
  ]
}
```

---

## 5. 実装順序の提案

1. **バックエンド**: B1 → B2 → B3（compare 実装とテスト）
2. **フロントエンド**: **F0（ネスト対応）** を先に行い、その上で F1（評価）→ F2（compare を関数一覧に）→ F3（演算子 UI）→ F4（バリデーション）。F0 なしだと compare を追加しても「if の条件に compare を入れる」ことを画面から操作できない。
3. **ドキュメント**: D1, D2 は各リリースに合わせて更新

---

## 6. 注意点・既存仕様との整合

- **既存の if(condition, then, else)** はそのまま有効。condition に field/constant を渡す「真理値だけ」の使い方も継続可能。
- **compare の第2引数**は「演算子名の文字列」なので、**constant の value に string を許容**している現行仕様でそのまま扱える（ComputedRuleEditor の定数入力が number | string | boolean であることを確認済み）。
- 条件ルール (visibility_rule 等) は「field + operator + value」のフラット構造だが、computed_rule は「関数のネスト」なので、**compare という関数で包む**形で演算子を指定するのが現構造と整合する。

以上を「計算ルール if で演算子を指定可能にする」ための正確なタスクとして整理した。
