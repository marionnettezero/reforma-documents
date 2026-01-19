# SUPP-COMPUTED-EDITOR-001: computed_ruleビジュアルエディタ 実装仕様

**作成日**: 2026-01-22  
**最終更新日**: 2026-01-22  
**バージョン**: v1.0.0

---

## 概要

フォーム項目の`computed_rule`（計算ルール）を、生のJSON入力ではなく、ビジュアルエディタで編集可能にする。内部でJSONを生成し、`ComputedEvaluatorService`が評価可能な形式で保存する。利用可能な関数（sum, multiply, tax, round, min, max, if）をUIで選択し、引数（フィールド参照/定数値）を視覚的に設定できるようにする。

---

## バックエンド実装状況

### 現在の実装状況

**既存実装**:
- ✅ `form_fields`テーブルに`computed_rule` JSONカラムが存在
- ✅ `ComputedEvaluatorService`が実装済み（sum, multiply, tax, round, min, max, if関数対応）
- ✅ 計算ルールの評価ロジックが実装済み
- ✅ 循環検出機能が実装済み（max_dependency_depth=1）

**未実装**:
- ⏳ `computed_rule`のビジュアルエディタUI
- ⏳ JSON生成/パースロジック（フロントエンド）
- ⏳ バリデーションUI（関数引数数チェック、フィールド参照存在チェック）

---

## データモデル

### computed_ruleのJSON構造

**実装に基づく構造**（`ComputedEvaluatorService`準拠）:

#### 1. 関数ルール（type: "function"）

```json
{
  "type": "function",
  "name": "sum",
  "args": [
    {
      "type": "field",
      "field_key": "price1"
    },
    {
      "type": "field",
      "field_key": "price2"
    }
  ]
}
```

#### 2. フィールド参照ルール（type: "field"）

```json
{
  "type": "field",
  "field_key": "price1"
}
```

#### 3. 定数ルール（type: "constant"）

```json
{
  "type": "constant",
  "value": 100
}
```

**注意事項**:
- `type`: 必須。`"function" | "field" | "constant"`のいずれか
- `name`: `type="function"`の場合に必須。関数名（`"sum" | "multiply" | "tax" | "round" | "min" | "max" | "if"`）
- `args`: `type="function"`の場合に必須。引数配列（各要素は`{type: "field", field_key: "..."}`または`{type: "constant", value: ...}`）
- `field_key`: `type="field"`の場合に必須。参照先フィールドのキー
- `value`: `type="constant"`の場合に必須。定数値（数値、文字列、真偽値）

---

## 利用可能な関数と引数仕様

### 1. sum関数

**説明**: 引数の合計を計算

**引数**:
- 可変引数（1個以上）
- 各引数は数値型（フィールド参照または定数値）

**例**:
```json
{
  "type": "function",
  "name": "sum",
  "args": [
    {"type": "field", "field_key": "price1"},
    {"type": "field", "field_key": "price2"},
    {"type": "constant", "value": 100}
  ]
}
```

### 2. multiply関数

**説明**: 引数の積を計算

**引数**:
- 可変引数（1個以上）
- 各引数は数値型（フィールド参照または定数値）

**例**:
```json
{
  "type": "function",
  "name": "multiply",
  "args": [
    {"type": "field", "field_key": "quantity"},
    {"type": "field", "field_key": "price"}
  ]
}
```

### 3. tax関数

**説明**: 税込金額を計算（`value * (1 + rate / 100)`）

**引数**:
- 第1引数: 金額（フィールド参照または定数値）
- 第2引数: 税率（%）（フィールド参照または定数値）

**例**:
```json
{
  "type": "function",
  "name": "tax",
  "args": [
    {"type": "field", "field_key": "subtotal"},
    {"type": "constant", "value": 10}
  ]
}
```

### 4. round関数

**説明**: 数値を四捨五入

**引数**:
- 第1引数: 値（フィールド参照または定数値）
- 第2引数: 桁数（定数値、省略時は0）

**例**:
```json
{
  "type": "function",
  "name": "round",
  "args": [
    {"type": "field", "field_key": "amount"},
    {"type": "constant", "value": 2}
  ]
}
```

### 5. min関数

**説明**: 引数の最小値を返す

**引数**:
- 可変引数（1個以上）
- 各引数は数値型（フィールド参照または定数値）

**例**:
```json
{
  "type": "function",
  "name": "min",
  "args": [
    {"type": "field", "field_key": "price1"},
    {"type": "field", "field_key": "price2"}
  ]
}
```

### 6. max関数

**説明**: 引数の最大値を返す

**引数**:
- 可変引数（1個以上）
- 各引数は数値型（フィールド参照または定数値）

**例**:
```json
{
  "type": "function",
  "name": "max",
  "args": [
    {"type": "field", "field_key": "price1"},
    {"type": "field", "field_key": "price2"}
  ]
}
```

### 7. if関数

**説明**: 条件分岐（`condition ? true_value : false_value`）

**引数**:
- 第1引数: 条件（フィールド参照または定数値、真偽値として評価）
- 第2引数: true値（フィールド参照または定数値）
- 第3引数: false値（フィールド参照または定数値）

**例**:
```json
{
  "type": "function",
  "name": "if",
  "args": [
    {"type": "field", "field_key": "is_member"},
    {"type": "constant", "value": 100},
    {"type": "constant", "value": 0}
  ]
}
```

---

## フロントエンド実装

### 1. 型定義

**ファイル**: `src/pages/forms/FormItemPage.tsx`（または新規ファイル）

**型定義**:

```typescript
// 計算ルールの型定義
type ComputedRuleType = "function" | "field" | "constant";

type ComputedRuleArg = 
  | { type: "field"; field_key: string }
  | { type: "constant"; value: number | string | boolean };

type ComputedRule = 
  | { type: "function"; name: string; args: ComputedRuleArg[] }
  | { type: "field"; field_key: string }
  | { type: "constant"; value: number | string | boolean };

// 関数定義
type FunctionDefinition = {
  name: string;
  label: string;
  description: string;
  minArgs: number;
  maxArgs: number | null; // nullの場合は可変引数
  argLabels: string[]; // 引数のラベル（例: ["金額", "税率(%)"]）
};

// 利用可能な関数定義
const COMPUTED_FUNCTIONS: FunctionDefinition[] = [
  {
    name: "sum",
    label: "合計 (sum)",
    description: "引数の合計を計算します",
    minArgs: 1,
    maxArgs: null,
    argLabels: ["値1", "値2", "..."]
  },
  {
    name: "multiply",
    label: "積 (multiply)",
    description: "引数の積を計算します",
    minArgs: 1,
    maxArgs: null,
    argLabels: ["値1", "値2", "..."]
  },
  {
    name: "tax",
    label: "税込計算 (tax)",
    description: "税込金額を計算します（金額 × (1 + 税率/100)）",
    minArgs: 2,
    maxArgs: 2,
    argLabels: ["金額", "税率(%)"]
  },
  {
    name: "round",
    label: "四捨五入 (round)",
    description: "数値を四捨五入します",
    minArgs: 1,
    maxArgs: 2,
    argLabels: ["値", "桁数"]
  },
  {
    name: "min",
    label: "最小値 (min)",
    description: "引数の最小値を返します",
    minArgs: 1,
    maxArgs: null,
    argLabels: ["値1", "値2", "..."]
  },
  {
    name: "max",
    label: "最大値 (max)",
    description: "引数の最大値を返します",
    minArgs: 1,
    maxArgs: null,
    argLabels: ["値1", "値2", "..."]
  },
  {
    name: "if",
    label: "条件分岐 (if)",
    description: "条件に応じて値を返します（条件 ? true値 : false値）",
    minArgs: 3,
    maxArgs: 3,
    argLabels: ["条件", "true値", "false値"]
  }
];
```

### 2. ComputedRuleEditorコンポーネント

**ファイル**: `src/components/ComputedRuleEditor.tsx`（新規作成）

**コンポーネント仕様**:

```typescript
type ComputedRuleEditorProps = {
  value: ComputedRule | null;
  onChange: (rule: ComputedRule | null) => void;
  availableFields: Array<{ field_key: string; type: string; label?: string }>;
  currentFieldKey?: string; // 自己参照チェック用
  validationErrors?: Record<string, string>;
  onValidationError?: (errors: Record<string, string>) => void;
};
```

**UI構成**:

1. **ルールタイプ選択**（ラジオボタンまたはタブ）
   - "関数" (function)
   - "フィールド参照" (field)
   - "定数値" (constant)

2. **関数選択**（type="function"の場合）
   - ドロップダウンで関数を選択
   - 選択した関数の説明を表示

3. **引数管理**（type="function"の場合）
   - 引数リスト（追加/削除ボタン付き）
   - 各引数のタイプ選択（field / constant）
   - フィールド参照選択（ドロップダウン）
   - 定数値入力（数値/文字列/真偽値）

4. **フィールド参照設定**（type="field"の場合）
   - フィールド選択ドロップダウン

5. **定数値設定**（type="constant"の場合）
   - 値タイプ選択（数値/文字列/真偽値）
   - 値入力フィールド

6. **JSONプレビュー**（折りたたみ可能）
   - 生成されたJSONを表示
   - コピーボタン（オプション）

### 3. JSON生成ロジック

**ファイル**: `src/components/ComputedRuleEditor.tsx`

**実装内容**:

```typescript
/**
 * ビジュアルエディタの状態からcomputed_rule JSONを生成
 */
function generateComputedRuleJson(
  ruleType: ComputedRuleType,
  functionName: string | null,
  args: ComputedRuleArg[],
  fieldKey: string | null,
  constantValue: number | string | boolean | null
): ComputedRule | null {
  if (ruleType === "function") {
    if (!functionName || args.length === 0) {
      return null;
    }
    return {
      type: "function",
      name: functionName,
      args: args
    };
  } else if (ruleType === "field") {
    if (!fieldKey) {
      return null;
    }
    return {
      type: "field",
      field_key: fieldKey
    };
  } else if (ruleType === "constant") {
    if (constantValue === null || constantValue === undefined) {
      return null;
    }
    return {
      type: "constant",
      value: constantValue
    };
  }
  return null;
}
```

### 4. JSONパースロジック

**ファイル**: `src/components/ComputedRuleEditor.tsx`

**実装内容**:

```typescript
/**
 * 既存のcomputed_rule JSONをビジュアルエディタの状態に復元
 */
function parseComputedRuleJson(ruleJson: any): {
  ruleType: ComputedRuleType;
  functionName: string | null;
  args: ComputedRuleArg[];
  fieldKey: string | null;
  constantValue: number | string | boolean | null;
} {
  if (!ruleJson || typeof ruleJson !== "object") {
    return {
      ruleType: "constant",
      functionName: null,
      args: [],
      fieldKey: null,
      constantValue: null
    };
  }

  if (ruleJson.type === "function") {
    return {
      ruleType: "function",
      functionName: ruleJson.name || null,
      args: Array.isArray(ruleJson.args) ? ruleJson.args : [],
      fieldKey: null,
      constantValue: null
    };
  } else if (ruleJson.type === "field") {
    return {
      ruleType: "field",
      functionName: null,
      args: [],
      fieldKey: ruleJson.field_key || null,
      constantValue: null
    };
  } else if (ruleJson.type === "constant") {
    return {
      ruleType: "constant",
      functionName: null,
      args: [],
      fieldKey: null,
      constantValue: ruleJson.value ?? null
    };
  }

  // デフォルト値
  return {
    ruleType: "constant",
    functionName: null,
    args: [],
    fieldKey: null,
    constantValue: null
  };
}
```

### 5. バリデーション実装

**ファイル**: `src/components/ComputedRuleEditor.tsx`

**バリデーション項目**:

```typescript
function validateComputedRule(
  ruleType: ComputedRuleType,
  functionName: string | null,
  args: ComputedRuleArg[],
  fieldKey: string | null,
  constantValue: number | string | boolean | null,
  availableFields: Array<{ field_key: string }>,
  currentFieldKey?: string
): Record<string, string> {
  const errors: Record<string, string> = {};

  if (ruleType === "function") {
    if (!functionName) {
      errors.function = "関数を選択してください";
    } else {
      const funcDef = COMPUTED_FUNCTIONS.find(f => f.name === functionName);
      if (funcDef) {
        if (args.length < funcDef.minArgs) {
          errors.args = `引数は最低${funcDef.minArgs}個必要です`;
        }
        if (funcDef.maxArgs !== null && args.length > funcDef.maxArgs) {
          errors.args = `引数は最大${funcDef.maxArgs}個までです`;
        }
      }
    }

    // 引数のバリデーション
    args.forEach((arg, index) => {
      if (arg.type === "field") {
        if (!arg.field_key) {
          errors[`arg_${index}`] = "フィールドを選択してください";
        } else if (arg.field_key === currentFieldKey) {
          errors[`arg_${index}`] = "自己参照は許可されていません";
        } else if (!availableFields.find(f => f.field_key === arg.field_key)) {
          errors[`arg_${index}`] = "存在しないフィールドです";
        }
      } else if (arg.type === "constant") {
        if (arg.value === null || arg.value === undefined || arg.value === "") {
          errors[`arg_${index}`] = "定数値を入力してください";
        }
      }
    });
  } else if (ruleType === "field") {
    if (!fieldKey) {
      errors.field = "フィールドを選択してください";
    } else if (fieldKey === currentFieldKey) {
      errors.field = "自己参照は許可されていません";
    } else if (!availableFields.find(f => f.field_key === fieldKey)) {
      errors.field = "存在しないフィールドです";
    }
  } else if (ruleType === "constant") {
    if (constantValue === null || constantValue === undefined || constantValue === "") {
      errors.constant = "定数値を入力してください";
    }
  }

  return errors;
}
```

### 6. FieldEditFormへの統合

**ファイル**: `src/pages/forms/FormItemPage.tsx`

**変更内容**:

```typescript
// 状態管理の変更
// 変更前: const [editComputedRule, setEditComputedRule] = useState<string>("");
// 変更後:
const [editComputedRule, setEditComputedRule] = useState<ComputedRule | null>(null);

// startEditField関数の変更
function startEditField(stepIndex: number, groupIndex: number, fieldIndex: number) {
  // ... 既存の処理
  
  // computed_ruleのパース
  if (field.computed_rule) {
    const parsed = parseComputedRuleJson(field.computed_rule);
    setEditComputedRule(generateComputedRuleJson(
      parsed.ruleType,
      parsed.functionName,
      parsed.args,
      parsed.fieldKey,
      parsed.constantValue
    ));
  } else {
    setEditComputedRule(null);
  }
}

// saveField関数の変更
function saveField(stepIndex: number, groupIndex: number, fieldIndex: number) {
  // ... 既存の処理
  
  // computed_ruleの処理
  let computedRule: any = null;
  if (editComputedRule) {
    computedRule = editComputedRule; // 既にJSON形式
    // read_only属性を設定
    if (editComputedRule.type === "function" || editComputedRule.type === "field") {
      optionsJson.read_only = true;
    }
  }
  
  // ... 既存の処理
}

// FieldEditForm内の変更
// 変更前: <textarea value={editComputedRule} ... />
// 変更後:
<ComputedRuleEditor
  value={editComputedRule}
  onChange={setEditComputedRule}
  availableFields={fields.map(f => ({
    field_key: f.field_key,
    type: f.type,
    label: f.options_json?.label || f.field_key
  }))}
  currentFieldKey={editFieldKey}
  validationErrors={validationErrors}
  onValidationError={(errors) => {
    setValidationErrors({ ...validationErrors, ...errors });
  }}
/>
```

---

## API仕様

### 既存API（変更なし）

`computed_rule`は既存の`PUT /v1/forms/{id}/fields` APIで送信される。

**リクエストボディ例**:

```json
{
  "fields": [
    {
      "field_key": "total",
      "type": "computed",
      "computed_rule": {
        "type": "function",
        "name": "sum",
        "args": [
          {"type": "field", "field_key": "price1"},
          {"type": "field", "field_key": "price2"}
        ]
      },
      "options_json": {
        "read_only": true,
        "label": "合計"
      },
      ...
    }
  ]
}
```

---

## 実装タスク

### フロントエンド

#### 型定義・定数定義
- ⏳ `ComputedRule`, `ComputedRuleArg`, `ComputedRuleType`型定義を追加
- ⏳ `COMPUTED_FUNCTIONS`定数配列を定義

#### ComputedRuleEditorコンポーネント
- ⏳ `ComputedRuleEditor.tsx`を新規作成
- ⏳ ルールタイプ選択UI実装
- ⏳ 関数選択ドロップダウン実装
- ⏳ 引数管理UI実装（追加/削除/並び替え）
- ⏳ 引数タイプ選択UI実装（field/constant）
- ⏳ フィールド参照選択ドロップダウン実装
- ⏳ 定数値入力UI実装（数値/文字列/真偽値）
- ⏳ JSONプレビュー表示実装（折りたたみ可能）

#### JSON生成・パースロジック
- ⏳ `generateComputedRuleJson`関数実装
- ⏳ `parseComputedRuleJson`関数実装

#### バリデーション
- ⏳ `validateComputedRule`関数実装
- ⏳ 関数引数数チェック実装
- ⏳ フィールド参照存在チェック実装
- ⏳ 自己参照チェック実装
- ⏳ エラーメッセージ表示実装

#### FieldEditForm統合
- ⏳ `editComputedRule`の型を`string`から`ComputedRule | null`に変更
- ⏳ `startEditField`関数でJSONパース処理を追加
- ⏳ `saveField`関数でJSON生成処理を更新
- ⏳ `FieldEditForm`内のテキストエリアを`ComputedRuleEditor`に置き換え

#### 翻訳対応
- ⏳ `PreferencesContext.tsx`に翻訳キーを追加:
  - `computed_rule_editor_title`: "計算ルール" / "Computed Rule"
  - `computed_rule_type_function`: "関数" / "Function"
  - `computed_rule_type_field`: "フィールド参照" / "Field Reference"
  - `computed_rule_type_constant`: "定数値" / "Constant"
  - `computed_rule_select_function`: "関数を選択" / "Select Function"
  - `computed_rule_add_arg`: "引数を追加" / "Add Argument"
  - `computed_rule_remove_arg`: "引数を削除" / "Remove Argument"
  - `computed_rule_arg_type_field`: "フィールド参照" / "Field Reference"
  - `computed_rule_arg_type_constant`: "定数値" / "Constant"
  - `computed_rule_select_field`: "フィールドを選択" / "Select Field"
  - `computed_rule_enter_constant`: "定数値を入力" / "Enter Constant"
  - `computed_rule_json_preview`: "JSONプレビュー" / "JSON Preview"
  - `computed_rule_self_reference_error`: "自己参照は許可されていません" / "Self reference is not allowed"

---

## 後方互換性

### 既存データの対応

**既存のcomputed_rule JSON**:
- 既存のJSON形式（`ComputedEvaluatorService`が評価可能な形式）はそのまま使用可能
- ビジュアルエディタで編集すると、正規化された形式で保存される

**JSON形式の不一致**:
- JSONファイル仕様（`ref:フィールドキー`形式）と実装（`{type: "field", field_key: "..."}`形式）が異なる場合、実装形式を優先
- 既存データがJSONファイル仕様形式の場合、パース時に実装形式に変換

---

## 注意事項

### バリデーション

1. **関数選択時**:
   - 関数が選択されていること
   - 引数数が関数の要件（minArgs, maxArgs）を満たしていること

2. **フィールド参照時**:
   - 参照先フィールドが存在すること
   - 自己参照でないこと（警告表示）

3. **定数値時**:
   - 値が入力されていること
   - 数値型の場合は数値として有効であること

### データ整合性

1. **循環参照の検出**:
   - ビジュアルエディタでは直接検出しない（バックエンドの`ComputedEvaluatorService`が検出）
   - 自己参照のみ警告表示

2. **フィールド型の整合性**:
   - 関数の引数として適切な型のフィールドを参照しているかは、バックエンドで検証
   - フロントエンドでは警告のみ表示（必須チェックは行わない）

### UI/UX

1. **引数の追加/削除**:
   - 可変引数関数（sum, multiply, min, max）では引数を自由に追加/削除可能
   - 固定引数関数（tax, round, if）では引数数を固定

2. **JSONプレビュー**:
   - 折りたたみ可能なセクションで表示
   - デバッグ用途として使用

3. **エラーメッセージ**:
   - 各入力項目の下にエラーメッセージを表示
   - バリデーションエラーがある場合は保存ボタンを無効化（オプション）

---

## 参照

- `app/Services/ComputedEvaluatorService.php` - 計算ルール評価サービス
- `app/Models/FormField.php` - フォーム項目モデル
- `src/pages/forms/FormItemPage.tsx` - フォーム項目設定画面
- `src/ui/PreferencesContext.tsx` - 翻訳コンテキスト
- `ReForma_追補パッチ_表示モード_テーマ_計算フィールド_v1.0.1.json` - 計算フィールド仕様（参考）
