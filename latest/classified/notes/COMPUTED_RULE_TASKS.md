# 計算ルール (computed_rule) の現状確認とタスク整理

**作成日**: 2026-01-25  
**対象**:
1. 項目詳細設定の高度な設定「計算ルール (computed_rule)」で、フィールド参照タブでフィールドを選択すると関数・定数値に戻れなくなる事象
2. checkbox の選択肢と text の数値で「合計金額」を表示できるかどうかの現状と対応可否

---

## 1. 現状の整理

### 1.1 計算ルールエディタの構成（フロントエンド）

- **ComputedRuleEditor** (`src/components/ComputedRuleEditor.tsx`) が「関数」「フィールド参照」「定数値」の3タブでルールを編集する。
- 親は `value`（`ComputedRule | null`）と `onChange` で制御。`FieldDetailPanel` では `value={editComputedRule}` / `onChange={setEditComputedRule}`。
- ルールタイプは次の3種:
  - `type: "function"` … 関数名 + 引数配列（各引数は `{ type: "field", field_key }` または `{ type: "constant", value }`）
  - `type: "field"` … 単一フィールド参照 `{ type: "field", field_key }`
  - `type: "constant"` … 定数 `{ type: "constant", value }`

### 1.2 問題1: フィールド参照選択後に「関数」「定数値」に戻れない

**現象**  
フィールド参照タブでフィールドを選択したあと、「関数」または「定数値」タブを押しても、見た目が戻らない、または直後にフィールド参照に戻ってしまう。無効化して再度有効化すると初期状態になり、関数・定数値に戻れる。

**原因（コード上の整理）**

1. **親への通知条件**  
   状態変更時の `useEffect` では、`generateComputedRuleJson(...)` が **有効なルール** を返すときだけ `onChange(rule)` を呼んでいる（`ComputedRuleEditor.tsx` 314–318 行付近）。
   - 「関数」に切り替えた直後は `functionName === ""` かつ `args.length === 0` のため `generateComputedRuleJson` は `null` を返す。
   - このとき `onChange` は呼ばれない。

2. **value による上書き**  
   もう一つの `useEffect` が `[value]` に依存し、`value` から `ruleType` / `fieldKey` 等を復元している（277–302 行付近）。
   - 「関数」に切り替えても `onChange` が走らないため、親の `editComputedRule`（＝`value`）は従来の `{ type: "field", field_key: "xxx" }` のまま。
   - 親が再レンダーすると同じ `value` が再度渡される。`value` の参照が毎回変わると、この effect が毎回実行され、`parseComputedRuleJson(value)` の結果で `ruleType` が再び `"field"` に上書きされる。
   - 結果として「関数」タブに切り替えたつもりが、すぐに「フィールド参照」に戻ったように見える。

3. **無効化→再有効化で直る理由**  
   無効化で `setEditComputedRule(null)` が呼ばれ、再有効化時に `initialRule`（例: `{ type: "function", name: "", args: [] }` や空に近い初期値）が渡される。このときは `value` が「フィールド参照」ではなくなるため、復元 effect が「関数」側の状態を設定し、タブ切り替えが効くように見える。

**結論**  
「フィールド参照」→「関数」/「定数値」への切り替え時に、**不完全なルールでも親に意図を伝える**か、**`value` からの復元が「実質的に同じ内容のとき」は上書きしない**ようにする必要がある。

### 1.3 問題2: checkbox の選択肢と text の数値で合計金額を表示したい

**希望する挙動**  
- checkbox の選択肢に単価（または価格）を持たせる。  
- 選択された選択肢の「金額」の合計と、別の text フィールドに入力した数値とを足して、合計金額フィールド（例: type=computed）に表示したい。

**現状の仕様・実装**

| 項目 | 内容 |
|------|------|
| 計算の実行 | `ComputedEvaluatorService::evaluate()` が `answers` と `form` を受け、computed フィールドのみ評価。 |
| フィールド値の参照 | `evaluateField()` で `$answers[$fieldKey]` をそのまま返す。計算関数にはこの生の値が渡る。 |
| sum の実装 | `functionSum($args)` は各引数を `(float)($arg ?? 0)` で加算（`ComputedEvaluatorService.php` 188–193 行付近）。 |
| checkbox の answers | `AnswerNormalizerService` により **配列** に正規化される（`normalizeArray`）。例: `["100", "200"]`。 |
| text / number | text は文字列、number は `normalizeNumber` で float。どちらも `(float)` で 1 引数として扱いやすい。 |

**制約**

- **checkbox を sum の引数にした場合**  
  - `$answers[$fieldKey]` は配列（例: `["100","200"]`）。  
  - PHP で `(float)(array)` は数値変換で 0（または Notice 付きで 1）となり、**「選択された value の合計」にはならない**。  
- **選択肢ごとの金額を足す**には、  
  - 「checkbox フィールド 1 つを参照したときに、その配列要素を数値化して合計した値」として評価する、  
  - もしくは sum 側で「配列引数は要素を展開して加算する」という意味づけが必要。

**結論**

- **現状のままで「checkbox の選択肢の合計＋text の数値」をそのまま実現するのは困難。**
- 対応するには、次のいずれか（または組み合わせ）の拡張が必要:
  - **A**: フィールド参照解決時に、参照先が checkbox（や配列を返す型）のときは「配列なら各要素を (float) して合計した値」に変換してから計算に渡す。  
  - **B**: sum（または新規関数）で「引数が配列なら展開して合計」する仕様を追加する。  
  - **C**: 選択肢の `value` を数値にしておき、上記 A/B により「選択済み value の合計」が取れるようにする。このうえで、合計フィールドを `sum(checkbox_field, text_field)` のようにすれば「選択金額＋テキスト数値」が可能になる。

### 1.4 利用可能な関数（実装済み・未実装）

**実装済み**（`ComputedEvaluatorService` / `ComputedRuleEditor` で利用可能）:

| 関数名 | 説明 | 引数 |
|--------|------|------|
| **sum** | 加算。引数の合計を返す。 | 可変（1個以上）。各引数はフィールド参照または定数値。 |
| **multiply** | 乗算。引数の積を返す。 | 可変（1個以上）。各引数はフィールド参照または定数値。 |
| **tax** | 税込計算。`value × (1 + rate/100)` を返す。 | 2個（金額、税率%）。 |
| **round** | 四捨五入。 | 1～2個（値、省略時0の桁数）。 |
| **min** | 最小値。引数中の最小値を返す。 | 可変（1個以上）。 |
| **max** | 最大値。引数中の最大値を返す。 | 可変（1個以上）。 |
| **if** | 条件分岐。条件が真なら第2引数、偽なら第3引数を返す。 | 3個（条件、true時の値、false時の値）。 |

**四則演算との対応**:
- **加算**: `sum` で対応済み。
- **乗算**: `multiply` で対応済み。
- **減算**: **subtract は未実装**。`sum(a, multiply(b, -1))` のような組み合わせで a − b は表現可能。
- **除算**: **divide は未実装**。`multiply(値, 定数)` で「定数で割る」は表現可能（例: ÷10 → `multiply(フィールド, 0.1)`）。「フィールド参照で割る」は現状の関数では表現できない。

**未実装**:
- **subtract（減算）**: 未実装。
- **divide（除算）**: 未実装。

---

## 2. タスク一覧

### 問題1 対応: タブ切り替えで関数・定数値に戻れるようにする

| ID | 内容 | 対象 | 備考 |
|----|------|------|------|
| **T1** | ルールタイプ切り替え時も親に通知する | フロント | 「関数」に切り替えた直後など、`generateComputedRuleJson` が `null` を返す場合でも、**意図したルールタイプ**を伝える必要がある。`onChange(null)` だと「計算なし」になってしまうため、**「type だけ確定した不完全ルール」を許容するか**、あるいは **親には従来どおり「有効なときだけ onChange」** にして、**value の同期条件を見直す**かのどちらかで対応する。 |
| **T2** | value 同期の条件を見直す | フロント | `useEffect([value])` で常に `value` から状態を上書きしていると、T1 で「不完全でも通知」したとしても、親が再レンダーするたびに古い `value`（例: フィールド参照）で上書きされる可能性がある。**「value の実質的な内容が前回と同一のときは state を更新しない」**（例: 直前に反映した rule と `JSON.stringify(value)` が等しい）や、**「ルールタイプだけは local state を優先する」**といった条件を入れて、フィールド参照→関数への切り替えが復元で消えないようにする。 |
| **T3** | 挙動の確認（フィールド→関数→引数設定→保存） | 手動 | フィールド参照で 1 件選択 → 「関数」タブ → 関数選択・引数設定 → 保存、の一連が意図どおりになることを確認する。 |

### 問題2 対応: checkbox + text で合計金額を出せるようにする（拡張）

| ID | 内容 | 対象 | 備考 |
|----|------|------|------|
| **T4** | 仕様・設計の決定 | ドキュメント | 「checkbox の選択肢の value を数値として合計する」をどこで行うか（ComputedEvaluator のフィールド参照時 / sum の引数解釈 / 新規関数）を決める。選択肢の `value` を数値または数値化可能な文字列にしておく運用でよいかも整理する。 |
| **T5** | フィールド参照時の配列→数値合計の変換（案 A） | バックエンド | `ComputedEvaluatorService::evaluateField()` で、参照先フィールドの型が checkbox（または answers の値が配列）のとき、各要素を `(float)` して合計した値を返すオプションを検討。既存の「フィールド参照＝生の answers」の意味を変えるため、**計算専用の解釈**として明示するか、設定で切り替えるかを決める。 |
| **T6** | sum の配列展開（案 B） | バックエンド | `functionSum` で、引数が配列なら `array_sum(array_map('floatval', $arg))` のように展開してから加算する。他関数（multiply 等）と仕様を合わせる必要がある。 |
| **T7** | 合計例のドキュメント・運用メモ | ドキュメント | 「checkbox の選択肢に value=価格を設定し、computed で sum(checkbox_field, text_field) で合計する」といった利用例を、上記いずれかの案が入った前提で追記する。 |

### 現状でできることの整理（問題2）

| ID | 内容 | 備考 |
|----|------|------|
| **T0** | 現状で可能な範囲の明文化 | 「number 同士の sum」「text に数値だけ入力すれば sum の引数になる」「checkbox を 1 引数にしたときは 0 になる」など、仕様として短文でまとめておくとよい。 |

---

## 3. 実装時の参照コード

### タブ切り替え・value 同期（問題1）

- `c:\GitHub\reforma-frontend-react\src\components\ComputedRuleEditor.tsx`
  - 277–302 行: `useEffect(() => { ... }, [value]);` … value から状態復元
  - 305–330 行: `useEffect(() => { ... }, [ruleType, functionName, args, fieldKey, constantValue, ...]);` … 状態から JSON 生成と `onChange(rule)`（現状は `if (rule) onChange(rule)`）
  - 377–380 行: 「関数」タブ `onClick` で `setRuleType("function"); setFunctionName(""); setArgs([]);`
  - 391–394 行: 「フィールド参照」タブ `onClick` で `setRuleType("field"); setFieldKey("");`
  - 406–408 行: 「定数値」タブ `onClick` で `setRuleType("constant"); setConstantValue(null);`

### 計算・checkbox の値（問題2）

- `c:\GitHub\reforma-backend-laravel\app\Services\ComputedEvaluatorService.php`
  - 151–171 行: `evaluateField()` … `$answers[$fieldKey]` をそのまま返す
  - 188–194 行: `functionSum()` … `(float)($arg ?? 0)` で加算
- `c:\GitHub\reforma-backend-laravel\app\Services\AnswerNormalizerService.php`
  - 67 行: `'checkbox' => $this->normalizeArray($value)`
  - 105–121 行: `normalizeArray()` … 配列 or カンマ区切り文字列を配列に正規化

---

## 4. 任意項目（未実装・必要に応じて対応）

以下は必須ではなく、必要に応じて対応する任意項目として整理する。

### 4.1 問題2: checkbox + text で合計（拡張）

| ID | 内容 | 対象 |
|----|------|------|
| **T4** | 仕様・設計の決定（配列→合計をどこで行うか） | ドキュメント |
| **T5** | フィールド参照時の配列→数値合計の変換（案 A） | バックエンド |
| **T6** | sum の配列展開（案 B） | バックエンド |
| **T7** | 合計例のドキュメント・運用メモ | ドキュメント |
| **T0** | 現状で可能な範囲の明文化 | ドキュメント |

### 4.2 組込関数の追加

| 項目 | 内容 |
|------|------|
| **subtract（減算）** | 未実装。`sum(a, multiply(b, -1))` で代替可能。 |
| **divide（除算）** | 未実装。定数で割る場合は `multiply(値, 1/n)` で代替可能。フィールド参照で割る場合は現状では表現できない。 |

---

## 5. まとめ

- **問題1（タブが戻らない）**: 原因は「フィールド参照→関数/定数への切り替え時に親へ通知していない」ことと、「value 依存の effect で毎回フィールド参照に上書きされる」こと。**T2（value 同期条件の見直し）** は実装済み。T1（親への通知方針）は T2 によりタブ維持が可能なため必須ではない。
- **問題2（checkbox + text で合計）**: 現状の sum と answers の形のままだと**そのままでは不可**。任意項目（4.1）として T4–T7・T0 を必要に応じて対応する。
- **減算・除算**: subtract / divide は未実装。任意項目（4.2）として必要に応じて追加可能。
