# 項目バリデーションルールの実装状況

## 確認日時
2026-01-13

---

## 概要

現在のReFormaシステムにおける項目（フィールド）のバリデーションルールの実装状況をまとめます。

---

## 1. フロントエンド（React）でのバリデーション

### 1.1 実装箇所
- **ファイル**: `src/pages/public/PublicFormViewPage.tsx`
- **関数**: `validate()` (502-526行目)

### 1.2 現在の実装内容

#### ✅ 実装済み
1. **必須チェック（条件付き）**
   - `conditionState.fields[field_key].required === true` の場合のみ必須チェック
   - 表示されていないフィールド（`visible === false`）はバリデーション対象外
   - 空値チェック:
     - `null`
     - `undefined`
     - `""` (空文字列)
     - `[]` (空配列、checkbox等)

2. **値の正規化**
   - `normalizeFieldValue()` 関数でフィールドタイプに応じた正規化
   - 文字列: `trim()` 処理
   - 数値: `parseFloat()` 処理
   - checkbox: 配列形式に統一
   - terms: boolean値に変換

#### ❌ 未実装・不足（フロントエンド）
1. **フィールドタイプ固有のバリデーション**（バックエンドは実装済み）
   - `email`: メールアドレス形式チェック
   - `tel`: 電話番号形式チェック
   - `number`: 数値範囲チェック（min/max）
   - `date/time/datetime`: 日付形式チェック
   - `file`: ファイルサイズ・拡張子チェック
     - **⚠️ セキュリティ上の懸念**: 不特定のユーザーからのファイルアップロード受付は要検討事項

2. **文字数制限**（バックエンドは実装済み）
   - `text`: 最大文字数チェック
   - `textarea`: 最大文字数チェック

3. **選択肢の妥当性チェック**（バックエンドは実装済み）
   - `select/radio/checkbox`: 選択値が定義された選択肢に含まれるかチェック

4. **パターンマッチング**（バックエンドは実装済み）
   - 正規表現による形式チェック（郵便番号、電話番号など）

5. **カスタムバリデーションルール**（バックエンドは実装済み）
   - `options_json` に定義されたバリデーションルールの適用

---

## 2. バックエンド（Laravel）でのバリデーション

### 2.1 実装箇所
- **ファイル**: `app/Http/Controllers/Api/V1/PublicFormsController.php`
- **メソッド**: `submit()` (131-299行目)

### 2.2 現在の実装内容

#### ✅ 実装済み
1. **リクエストパラメータのバリデーション**
   ```php
   $validated = $request->validate([
       'answers' => ['required', 'array'],
       'locale' => ['nullable', 'string', 'in:' . implode(',', $supportedLanguages)],
       'mode' => ['nullable', 'string', 'in:both,value,label'],
   ]);
   ```

2. **条件分岐評価に基づく必須チェック**
   - `ConditionEvaluatorService` で条件分岐を評価
   - `conditionState['fields'][field_key]['visible'] === true` かつ
   - `conditionState['fields'][field_key]['required'] === true` の場合のみ必須チェック
   - 空値チェック: `null` または `''` (空文字列)

3. **回答値の正規化**
   - `AnswerNormalizerService` でフィールドタイプに応じた正規化

4. **計算フィールドの評価**
   - `ComputedEvaluatorService` で計算フィールドを評価
   - クライアント送信値は信用せず、サーバー側で再計算

#### ✅ 実装済み（2026-01-20）
1. **フィールドタイプ固有のバリデーション**
   - ✅ `email`: メールアドレス形式チェック（`FieldValidationService`）
   - ✅ `tel`: 電話番号形式チェック（パターン指定時、`FieldValidationService`）
   - ✅ `number`: 数値範囲チェック（min/max、`FieldValidationService`）
   - ✅ `date/time/datetime`: 日付形式チェック（`FieldValidationService`）
   - ⚠️ `file`: ファイルサイズ・拡張子チェック（基本チェックのみ、実ファイルアップロード時は未実装）
     - **⚠️ セキュリティ上の懸念**: 不特定のユーザーからのファイルアップロード受付は、マルウェアや不正ファイルのアップロードリスクがあるため、実装前にセキュリティ対策の検討が必要

2. **文字数制限**
   - ✅ `text/textarea`: 最大文字数チェック（`FieldValidationService`）

3. **選択肢の妥当性チェック**
   - ✅ `select/radio/checkbox`: 選択値が定義された選択肢に含まれるかチェック（`FieldValidationService`）

4. **パターンマッチング**
   - ✅ 正規表現による形式チェック（`FieldValidationService`）

5. **カスタムバリデーションルール**
   - ✅ `options_json.validation` に定義されたバリデーションルールの適用（`FieldValidationService`）

6. **matrixフィールドタイプのバリデーション**
   - ✅ マトリクス形式のデータ検証（`FieldValidationService`）
   - ✅ 選択制限チェック（全体/ヘッダ単位、`FieldValidationService`）

#### ❌ 未実装・不足
1. **ファイルアップロード時の詳細バリデーション**
   - 実ファイルアップロード時のファイルサイズ・拡張子チェック（現在は基本チェックのみ）
   - **⚠️ 要検討事項**: 不特定のユーザーからのファイルアップロード受付は、セキュリティ上の懸念があるため、以下の点を検討する必要がある:
     - マルウェアスキャンの実装
     - ファイルタイプの厳格な検証（MIMEタイプ、マジックナンバー）
     - ファイル保存先の分離とアクセス制御
     - ファイルサイズ制限の適切な設定
     - アップロード可能なファイルタイプのホワイトリスト方式
     - レート制限（DoS攻撃対策）

---

## 3. 条件分岐ルールのバリデーション

### 3.1 実装箇所
- **ファイル**: `app/Services/RuleValidatorService.php`
- **メソッド**: `validateForm()` (33-59行目)

### 3.2 実装内容

#### ✅ 実装済み
1. **ルール構造の検証**
   - `visibility_rule`, `required_rule`, `step_transition_rule` の検証
   - ネスティング深度チェック（max_nesting=1）
   - 論理演算子（and/or/not）の検証
   - 比較演算子の検証

2. **フィールド参照の検証**
   - 参照field_keyの存在チェック
   - 自己参照チェック（未実装の可能性あり）

3. **演算子の妥当性チェック**
   - 有効な演算子: `eq`, `ne`, `in`, `contains`, `gt`, `gte`, `lt`, `lte`, `between`, `exists`

#### ⚠️ 部分実装
1. **型整合性チェック**
   - コメントに「簡易版」とあり、基本的な検証のみ
   - 実行時の型チェックは `ConditionEvaluatorService` で行われる

---

## 4. フィールド定義（FormField）の構造

### 4.1 データベース構造
- **テーブル**: `form_fields`
- **主要カラム**:
  - `type`: フィールドタイプ（text, email, number, select等）
  - `is_required`: 固定必須フラグ（boolean）
  - `options_json`: フィールド設定（JSON）

### 4.2 options_json の構造
```json
{
  "label": "フィールドラベル",
  "labels": {
    "ja": "日本語ラベル",
    "en": "English Label"
  },
  "placeholder": "プレースホルダー",
  "options": [
    {"value": "value1", "label": "ラベル1", "labels": {...}}
  ],
  "min": 0,        // number型用
  "max": 100,       // number型用
  "step": 1,        // number型用
  "rows": 5         // textarea型用
}
```

### 4.3 バリデーションルールの定義場所
- **現状**: `options_json` にバリデーションルールを定義する仕様は**未定義**
- **推奨**: `options_json` に以下のような構造を追加
  ```json
  {
    "validation": {
      "max_length": 100,
      "pattern": "^[0-9]{3}-[0-9]{4}$",
      "min": 0,
      "max": 100
    }
  }
  ```

---

## 5. バリデーションの実行タイミング

### 5.1 フロントエンド
1. **送信時**: `handleSubmit()` 内で `validate()` を呼び出し
2. **リアルタイム**: 未実装（入力中のバリデーションは行っていない）

### 5.2 バックエンド
1. **送信時**: `PublicFormsController::submit()` で必須チェック
2. **条件分岐評価**: `ConditionEvaluatorService` で条件分岐を評価
3. **正規化**: `AnswerNormalizerService` で値の正規化

---

## 6. エラーメッセージの表示

### 6.1 フロントエンド
- **必須エラー**: `${label}は必須です` (固定メッセージ)
- **フィールドエラー**: `errors[field_key]` に格納し、フィールド下部に表示
- **Toast**: `showError("入力内容に誤りがあります")` を表示

### 6.2 バックエンド
- **必須エラー**: `messages.submission_required_fields_missing` (多言語対応)
- **422エラー**: `errors.fields` にフィールド別エラーを格納
- **エラーメッセージ**: 多言語対応（`lang/ja/messages.php`, `lang/en/messages.php`）

---

## 7. 改善提案

### 7.1 優先度: 高
1. ✅ **フィールドタイプ固有のバリデーション実装**（バックエンド実装済み: 2026-01-20）
   - ✅ `email`: メールアドレス形式チェック
   - ✅ `number`: 数値範囲チェック（min/max）
   - ✅ `date/time/datetime`: 日付形式チェック

2. ✅ **選択肢の妥当性チェック**（バックエンド実装済み: 2026-01-20）
   - ✅ `select/radio/checkbox`: 選択値が定義された選択肢に含まれるかチェック

### 7.2 優先度: 中
3. ✅ **文字数制限**（バックエンド実装済み: 2026-01-20）
   - ✅ `text/textarea`: 最大文字数チェック

4. ✅ **パターンマッチング**（バックエンド実装済み: 2026-01-20）
   - ✅ 正規表現による形式チェック（郵便番号、電話番号など）

5. **リアルタイムバリデーション**（未実装）
   - 入力中のバリデーション（UX向上）

### 7.3 優先度: 低
6. ✅ **カスタムバリデーションルール**（バックエンド実装済み: 2026-01-20）
   - ✅ `options_json.validation` に定義されたバリデーションルールの適用

7. **バリデーションルールのUI設定**（未実装）
   - 管理画面でバリデーションルールを設定できるUI

### 7.4 フロントエンド実装（未実装）
- バックエンドで実装済みのフィールドタイプ固有のバリデーションをフロントエンドでも実装することを推奨（UX向上のため）

---

## 8. フィールドタイプ固有のバリデーション改修仕様

### 8.1 概要
フィールドタイプ固有のバリデーション（email形式、数値範囲、日付形式など）を実装するための改修仕様です。

### 8.2 options_json の構造拡張

#### 8.2.1 バリデーションルールの定義
`options_json` に `validation` オブジェクトを追加します。

```json
{
  "label": "メールアドレス",
  "labels": {
    "ja": "メールアドレス",
    "en": "Email Address"
  },
  "placeholder": "example@domain.com",
  "validation": {
    "max_length": 255,
    "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
    "min": 0,
    "max": 100,
    "min_date": "2024-01-01",
    "max_date": "2024-12-31",
    "allowed_extensions": ["pdf", "jpg", "png"],
    "max_file_size": 5242880
  }
}
```

#### 8.2.2 フィールドタイプ別のバリデーションルール

| フィールドタイプ | 対応バリデーションルール | 説明 |
|----------------|----------------------|------|
| `text` | `max_length` | 最大文字数 |
| `text` | `min_length` | 最小文字数（オプション） |
| `text` | `pattern` | 正規表現パターン |
| `textarea` | `max_length` | 最大文字数 |
| `textarea` | `min_length` | 最小文字数（オプション） |
| `email` | `pattern` | メールアドレス形式（デフォルトで適用） |
| `email` | `max_length` | 最大文字数 |
| `tel` | `pattern` | 電話番号形式（オプション） |
| `number` | `min` | 最小値 |
| `number` | `max` | 最大値 |
| `number` | `step` | ステップ値（既存） |
| `date` | `min_date` | 最小日付（YYYY-MM-DD形式） |
| `date` | `max_date` | 最大日付（YYYY-MM-DD形式） |
| `time` | `min_time` | 最小時刻（HH:MM形式） |
| `time` | `max_time` | 最大時刻（HH:MM形式） |
| `datetime` | `min_datetime` | 最小日時（ISO8601形式） |
| `datetime` | `max_datetime` | 最大日時（ISO8601形式） |
| `select` | `options` | 選択肢の妥当性チェック（既存） |
| `radio` | `options` | 選択肢の妥当性チェック（既存） |
| `checkbox` | `options` | 選択肢の妥当性チェック（既存） |
| `file` | `allowed_extensions` | 許可された拡張子の配列 |
| `file` | `max_file_size` | 最大ファイルサイズ（バイト） |
| `file` | `min_file_size` | 最小ファイルサイズ（バイト、オプション） |

**⚠️ 注意**: `file`タイプの実装は、不特定のユーザーからのファイルアップロード受付に関するセキュリティ上の懸念があるため、実装前にセキュリティ対策の検討が必要です。

### 8.3 フロントエンド（React）の改修仕様

#### 8.3.1 バリデーション関数の作成
**ファイル**: `src/utils/fieldValidation.ts` (新規作成)

```typescript
/**
 * フィールドタイプ固有のバリデーション関数
 */

export interface FieldValidationRule {
  max_length?: number;
  min_length?: number;
  pattern?: string;
  min?: number;
  max?: number;
  min_date?: string;
  max_date?: string;
  min_time?: string;
  max_time?: string;
  min_datetime?: string;
  max_datetime?: string;
  allowed_extensions?: string[];
  max_file_size?: number;
  min_file_size?: number;
}

export interface ValidationResult {
  isValid: boolean;
  error?: string;
}

/**
 * フィールド値をバリデーション
 */
export function validateFieldValue(
  value: any,
  fieldType: string,
  validationRules?: FieldValidationRule,
  options?: { options?: Array<{ value: string }> }
): ValidationResult {
  // 空値チェックは必須チェックで行うため、ここではスキップ
  if (value === null || value === undefined || value === '') {
    return { isValid: true };
  }

  // フィールドタイプ別のバリデーション
  switch (fieldType) {
    case 'text':
    case 'textarea':
      return validateText(value, validationRules);
    case 'email':
      return validateEmail(value, validationRules);
    case 'tel':
      return validateTel(value, validationRules);
    case 'number':
      return validateNumber(value, validationRules);
    case 'date':
      return validateDate(value, validationRules);
    case 'time':
      return validateTime(value, validationRules);
    case 'datetime':
      return validateDateTime(value, validationRules);
    case 'select':
    case 'radio':
      return validateSelect(value, options?.options);
    case 'checkbox':
      return validateCheckbox(value, options?.options);
    case 'file':
      return validateFile(value, validationRules);
    default:
      return { isValid: true };
  }
}

function validateText(value: string, rules?: FieldValidationRule): ValidationResult {
  if (typeof value !== 'string') {
    return { isValid: false, error: '文字列である必要があります' };
  }

  if (rules?.max_length && value.length > rules.max_length) {
    return { isValid: false, error: `最大${rules.max_length}文字まで入力できます` };
  }

  if (rules?.min_length && value.length < rules.min_length) {
    return { isValid: false, error: `最低${rules.min_length}文字以上入力してください` };
  }

  if (rules?.pattern) {
    const regex = new RegExp(rules.pattern);
    if (!regex.test(value)) {
      return { isValid: false, error: '形式が正しくありません' };
    }
  }

  return { isValid: true };
}

function validateEmail(value: string, rules?: FieldValidationRule): ValidationResult {
  // デフォルトのメールアドレス形式チェック
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!emailPattern.test(value)) {
    return { isValid: false, error: 'メールアドレスの形式が正しくありません' };
  }

  // カスタムパターンがある場合はそれを使用
  if (rules?.pattern) {
    const regex = new RegExp(rules.pattern);
    if (!regex.test(value)) {
      return { isValid: false, error: 'メールアドレスの形式が正しくありません' };
    }
  }

  // 最大文字数チェック
  if (rules?.max_length && value.length > rules.max_length) {
    return { isValid: false, error: `最大${rules.max_length}文字まで入力できます` };
  }

  return { isValid: true };
}

function validateTel(value: string, rules?: FieldValidationRule): ValidationResult {
  if (rules?.pattern) {
    const regex = new RegExp(rules.pattern);
    if (!regex.test(value)) {
      return { isValid: false, error: '電話番号の形式が正しくありません' };
    }
  }

  return { isValid: true };
}

function validateNumber(value: number, rules?: FieldValidationRule): ValidationResult {
  if (typeof value !== 'number' || isNaN(value)) {
    return { isValid: false, error: '数値である必要があります' };
  }

  if (rules?.min !== undefined && value < rules.min) {
    return { isValid: false, error: `${rules.min}以上である必要があります` };
  }

  if (rules?.max !== undefined && value > rules.max) {
    return { isValid: false, error: `${rules.max}以下である必要があります` };
  }

  return { isValid: true };
}

function validateDate(value: string, rules?: FieldValidationRule): ValidationResult {
  const date = new Date(value);
  if (isNaN(date.getTime())) {
    return { isValid: false, error: '日付の形式が正しくありません' };
  }

  if (rules?.min_date) {
    const minDate = new Date(rules.min_date);
    if (date < minDate) {
      return { isValid: false, error: `${rules.min_date}以降の日付を入力してください` };
    }
  }

  if (rules?.max_date) {
    const maxDate = new Date(rules.max_date);
    if (date > maxDate) {
      return { isValid: false, error: `${rules.max_date}以前の日付を入力してください` };
    }
  }

  return { isValid: true };
}

function validateTime(value: string, rules?: FieldValidationRule): ValidationResult {
  const timePattern = /^([0-1][0-9]|2[0-3]):[0-5][0-9]$/;
  if (!timePattern.test(value)) {
    return { isValid: false, error: '時刻の形式が正しくありません（HH:MM形式）' };
  }

  if (rules?.min_time && value < rules.min_time) {
    return { isValid: false, error: `${rules.min_time}以降の時刻を入力してください` };
  }

  if (rules?.max_time && value > rules.max_time) {
    return { isValid: false, error: `${rules.max_time}以前の時刻を入力してください` };
  }

  return { isValid: true };
}

function validateDateTime(value: string, rules?: FieldValidationRule): ValidationResult {
  const date = new Date(value);
  if (isNaN(date.getTime())) {
    return { isValid: false, error: '日時の形式が正しくありません' };
  }

  if (rules?.min_datetime) {
    const minDateTime = new Date(rules.min_datetime);
    if (date < minDateTime) {
      return { isValid: false, error: `${rules.min_datetime}以降の日時を入力してください` };
    }
  }

  if (rules?.max_datetime) {
    const maxDateTime = new Date(rules.max_datetime);
    if (date > maxDateTime) {
      return { isValid: false, error: `${rules.max_datetime}以前の日時を入力してください` };
    }
  }

  return { isValid: true };
}

function validateSelect(value: string, options?: Array<{ value: string }>): ValidationResult {
  if (!options || options.length === 0) {
    return { isValid: true };
  }

  const validValues = options.map(opt => opt.value);
  if (!validValues.includes(value)) {
    return { isValid: false, error: '選択肢から選択してください' };
  }

  return { isValid: true };
}

function validateCheckbox(value: string[], options?: Array<{ value: string }>): ValidationResult {
  if (!Array.isArray(value)) {
    return { isValid: false, error: '配列である必要があります' };
  }

  if (!options || options.length === 0) {
    return { isValid: true };
  }

  const validValues = options.map(opt => opt.value);
  const invalidValues = value.filter(v => !validValues.includes(v));
  if (invalidValues.length > 0) {
    return { isValid: false, error: '選択肢から選択してください' };
  }

  return { isValid: true };
}

function validateFile(value: File | File[], rules?: FieldValidationRule): ValidationResult {
  const files = Array.isArray(value) ? value : [value];

  for (const file of files) {
    // 拡張子チェック
    if (rules?.allowed_extensions && rules.allowed_extensions.length > 0) {
      const extension = file.name.split('.').pop()?.toLowerCase();
      if (!extension || !rules.allowed_extensions.includes(extension)) {
        return { isValid: false, error: `許可された拡張子: ${rules.allowed_extensions.join(', ')}` };
      }
    }

    // ファイルサイズチェック
    if (rules?.max_file_size && file.size > rules.max_file_size) {
      const maxSizeMB = (rules.max_file_size / 1024 / 1024).toFixed(2);
      return { isValid: false, error: `ファイルサイズは${maxSizeMB}MB以下である必要があります` };
    }

    if (rules?.min_file_size && file.size < rules.min_file_size) {
      const minSizeMB = (rules.min_file_size / 1024 / 1024).toFixed(2);
      return { isValid: false, error: `ファイルサイズは${minSizeMB}MB以上である必要があります` };
    }
  }

  return { isValid: true };
}
```

#### 8.3.2 PublicFormViewPage.tsx の改修
**ファイル**: `src/pages/public/PublicFormViewPage.tsx`

```typescript
// インポート追加
import { validateFieldValue, type FieldValidationRule } from "../../utils/fieldValidation";

// validate() 関数を拡張
const validate = (): boolean => {
  if (!form || !conditionState) return false;

  const newErrors: Record<string, string> = {};

  form.fields.forEach((field) => {
    const fieldState = conditionState.fields[field.field_key];
    if (!fieldState) return;

    // 表示されていないフィールドはバリデーション対象外
    if (!fieldState.visible) return;

    const value = answers[field.field_key];

    // 必須チェック
    if (fieldState.required) {
      if (value === null || value === undefined || value === "" || (Array.isArray(value) && value.length === 0)) {
        const label = field.options_json?.label || field.field_key;
        newErrors[field.field_key] = `${label}は必須です`;
        return; // 必須エラーの場合は他のバリデーションをスキップ
      }
    }

    // フィールドタイプ固有のバリデーション
    const validationRules: FieldValidationRule | undefined = field.options_json?.validation;
    const validationResult = validateFieldValue(
      value,
      field.type,
      validationRules,
      { options: field.options_json?.options }
    );

    if (!validationResult.isValid && validationResult.error) {
      newErrors[field.field_key] = validationResult.error;
    }
  });

  setErrors(newErrors);
  return Object.keys(newErrors).length === 0;
};
```

#### 8.3.3 リアルタイムバリデーション（オプション）
入力中のバリデーションを実装する場合：

```typescript
// handleFieldChange 関数を拡張
const handleFieldChange = (fieldKey: string, value: any) => {
  const field = form?.fields.find((f) => f.field_key === fieldKey);
  if (!field) return;

  const normalizedValue = normalizeFieldValue(value, field);
  const newAnswers = { ...answers, [fieldKey]: normalizedValue };

  setAnswers(newAnswers);

  // リアルタイムバリデーション（必須チェックは除く）
  const fieldState = conditionState?.fields[fieldKey];
  if (fieldState?.visible && normalizedValue !== null && normalizedValue !== "") {
    const validationRules: FieldValidationRule | undefined = field.options_json?.validation;
    const validationResult = validateFieldValue(
      normalizedValue,
      field.type,
      validationRules,
      { options: field.options_json?.options }
    );

    if (!validationResult.isValid && validationResult.error) {
      setErrors((prev) => ({ ...prev, [fieldKey]: validationResult.error }));
    } else {
      setErrors((prev) => {
        const next = { ...prev };
        delete next[fieldKey];
        return next;
      });
    }
  } else {
    setErrors((prev) => {
      const next = { ...prev };
      delete next[fieldKey];
      return next;
    });
  }

  // 条件分岐評価（デバウンス付き）
  evaluateConditionsDebounced(newAnswers);
};
```

### 8.4 バックエンド（Laravel）の改修仕様

#### 8.4.1 バリデーションサービスの作成
**ファイル**: `app/Services/FieldValidationService.php` (新規作成)

```php
<?php
/**
 * ReForma Backend - フィールドバリデーションサービス
 * ============================================================
 * 
 * 【責務】
 * - フィールドタイプ固有のバリデーション
 * - options_json の validation ルールに基づく検証
 */

namespace App\Services;

use App\Models\FormField;

class FieldValidationService
{
    /**
     * フィールド値をバリデーション
     *
     * @param mixed $value 値
     * @param FormField $field フィールド定義
     * @return array ['is_valid' => bool, 'error' => string|null]
     */
    public function validate($value, FormField $field): array
    {
        // 空値チェックは必須チェックで行うため、ここではスキップ
        if ($value === null || $value === '') {
            return ['is_valid' => true, 'error' => null];
        }

        $validationRules = $field->options_json['validation'] ?? null;

        return match ($field->type) {
            'text', 'textarea' => $this->validateText($value, $validationRules),
            'email' => $this->validateEmail($value, $validationRules),
            'tel' => $this->validateTel($value, $validationRules),
            'number' => $this->validateNumber($value, $validationRules),
            'date' => $this->validateDate($value, $validationRules),
            'time' => $this->validateTime($value, $validationRules),
            'datetime' => $this->validateDateTime($value, $validationRules),
            'select', 'radio' => $this->validateSelect($value, $field->options_json['options'] ?? []),
            'checkbox' => $this->validateCheckbox($value, $field->options_json['options'] ?? []),
            'file' => $this->validateFile($value, $validationRules),
            default => ['is_valid' => true, 'error' => null],
        };
    }

    private function validateText($value, ?array $rules): array
    {
        if (!is_string($value)) {
            return ['is_valid' => false, 'error' => '文字列である必要があります'];
        }

        if (isset($rules['max_length']) && mb_strlen($value) > $rules['max_length']) {
            return ['is_valid' => false, 'error' => "最大{$rules['max_length']}文字まで入力できます"];
        }

        if (isset($rules['min_length']) && mb_strlen($value) < $rules['min_length']) {
            return ['is_valid' => false, 'error' => "最低{$rules['min_length']}文字以上入力してください"];
        }

        if (isset($rules['pattern'])) {
            if (!preg_match($rules['pattern'], $value)) {
                return ['is_valid' => false, 'error' => '形式が正しくありません'];
            }
        }

        return ['is_valid' => true, 'error' => null];
    }

    private function validateEmail($value, ?array $rules): array
    {
        // デフォルトのメールアドレス形式チェック
        if (!filter_var($value, FILTER_VALIDATE_EMAIL)) {
            return ['is_valid' => false, 'error' => 'メールアドレスの形式が正しくありません'];
        }

        // カスタムパターンがある場合はそれを使用
        if (isset($rules['pattern'])) {
            if (!preg_match($rules['pattern'], $value)) {
                return ['is_valid' => false, 'error' => 'メールアドレスの形式が正しくありません'];
            }
        }

        if (isset($rules['max_length']) && mb_strlen($value) > $rules['max_length']) {
            return ['is_valid' => false, 'error' => "最大{$rules['max_length']}文字まで入力できます"];
        }

        return ['is_valid' => true, 'error' => null];
    }

    private function validateTel($value, ?array $rules): array
    {
        if (isset($rules['pattern'])) {
            if (!preg_match($rules['pattern'], $value)) {
                return ['is_valid' => false, 'error' => '電話番号の形式が正しくありません'];
            }
        }

        return ['is_valid' => true, 'error' => null];
    }

    private function validateNumber($value, ?array $rules): array
    {
        if (!is_numeric($value)) {
            return ['is_valid' => false, 'error' => '数値である必要があります'];
        }

        $numValue = (float) $value;

        if (isset($rules['min']) && $numValue < $rules['min']) {
            return ['is_valid' => false, 'error' => "{$rules['min']}以上である必要があります"];
        }

        if (isset($rules['max']) && $numValue > $rules['max']) {
            return ['is_valid' => false, 'error' => "{$rules['max']}以下である必要があります"];
        }

        return ['is_valid' => true, 'error' => null];
    }

    private function validateDate($value, ?array $rules): array
    {
        try {
            $date = new \DateTime($value);
        } catch (\Exception $e) {
            return ['is_valid' => false, 'error' => '日付の形式が正しくありません'];
        }

        if (isset($rules['min_date'])) {
            $minDate = new \DateTime($rules['min_date']);
            if ($date < $minDate) {
                return ['is_valid' => false, 'error' => "{$rules['min_date']}以降の日付を入力してください"];
            }
        }

        if (isset($rules['max_date'])) {
            $maxDate = new \DateTime($rules['max_date']);
            if ($date > $maxDate) {
                return ['is_valid' => false, 'error' => "{$rules['max_date']}以前の日付を入力してください"];
            }
        }

        return ['is_valid' => true, 'error' => null];
    }

    private function validateTime($value, ?array $rules): array
    {
        if (!preg_match('/^([0-1][0-9]|2[0-3]):[0-5][0-9]$/', $value)) {
            return ['is_valid' => false, 'error' => '時刻の形式が正しくありません（HH:MM形式）'];
        }

        if (isset($rules['min_time']) && $value < $rules['min_time']) {
            return ['is_valid' => false, 'error' => "{$rules['min_time']}以降の時刻を入力してください"];
        }

        if (isset($rules['max_time']) && $value > $rules['max_time']) {
            return ['is_valid' => false, 'error' => "{$rules['max_time']}以前の時刻を入力してください"];
        }

        return ['is_valid' => true, 'error' => null];
    }

    private function validateDateTime($value, ?array $rules): array
    {
        try {
            $dateTime = new \DateTime($value);
        } catch (\Exception $e) {
            return ['is_valid' => false, 'error' => '日時の形式が正しくありません'];
        }

        if (isset($rules['min_datetime'])) {
            $minDateTime = new \DateTime($rules['min_datetime']);
            if ($dateTime < $minDateTime) {
                return ['is_valid' => false, 'error' => "{$rules['min_datetime']}以降の日時を入力してください"];
            }
        }

        if (isset($rules['max_datetime'])) {
            $maxDateTime = new \DateTime($rules['max_datetime']);
            if ($dateTime > $maxDateTime) {
                return ['is_valid' => false, 'error' => "{$rules['max_datetime']}以前の日時を入力してください"];
            }
        }

        return ['is_valid' => true, 'error' => null];
    }

    private function validateSelect($value, array $options): array
    {
        if (empty($options)) {
            return ['is_valid' => true, 'error' => null];
        }

        $validValues = array_column($options, 'value');
        if (!in_array($value, $validValues, true)) {
            return ['is_valid' => false, 'error' => '選択肢から選択してください'];
        }

        return ['is_valid' => true, 'error' => null];
    }

    private function validateCheckbox($value, array $options): array
    {
        if (!is_array($value)) {
            return ['is_valid' => false, 'error' => '配列である必要があります'];
        }

        if (empty($options)) {
            return ['is_valid' => true, 'error' => null];
        }

        $validValues = array_column($options, 'value');
        $invalidValues = array_diff($value, $validValues);
        if (!empty($invalidValues)) {
            return ['is_valid' => false, 'error' => '選択肢から選択してください'];
        }

        return ['is_valid' => true, 'error' => null];
    }

    private function validateFile($value, ?array $rules): array
    {
        // ファイルバリデーションは実際のファイルアップロード時に実装
        // ここでは基本的なチェックのみ
        return ['is_valid' => true, 'error' => null];
    }
}
```

#### 8.4.2 PublicFormsController.php の改修
**ファイル**: `app/Http/Controllers/Api/V1/PublicFormsController.php`

```php
// コンストラクタに追加
public function __construct(
    private ConditionEvaluatorService $conditionEvaluator,
    private AnswerNormalizerService $answerNormalizer,
    private ComputedEvaluatorService $computedEvaluator,
    private FieldValidationService $fieldValidator, // 追加
    private PdfGenerationService $pdfGenerator,
    private PdfStorageService $pdfStorage
) {
}

// submit() メソッド内でバリデーションを追加
// 条件分岐評価に基づく必須フィールドのバリデーションの後に追加

// フィールドタイプ固有のバリデーション
$validationErrors = [];
foreach ($conditionState['fields'] as $fieldKey => $fieldState) {
    if ($fieldState['visible'] && $fieldState['store'] === 'store') {
        $field = $form->fields->firstWhere('field_key', $fieldKey);
        if (!$field) {
            continue;
        }

        $fieldValue = $answers[$fieldKey] ?? null;
        
        // 空値の場合は必須チェックで処理済みのためスキップ
        if ($fieldValue === null || $fieldValue === '') {
            continue;
        }

        $validationResult = $this->fieldValidator->validate($fieldValue, $field);
        if (!$validationResult['is_valid']) {
            $fieldLabel = $field->options_json['label'] ?? $fieldKey;
            $validationErrors[$fieldKey] = $validationResult['error'] ?? 'バリデーションエラー';
        }
    }
}

if (!empty($validationErrors)) {
    return ApiResponse::error($request, 422, ApiErrorCode::VALIDATION_FAILED, 
        'messages.submission_validation_failed', null, ['fields' => $validationErrors]);
}
```

### 8.5 エラーメッセージの多言語対応

#### 8.5.1 フロントエンド
エラーメッセージを多言語対応にする場合、`useT()` フックを使用：

```typescript
// fieldValidation.ts を改修
import { useT } from "../ui/PreferencesContext";

// エラーメッセージを翻訳キーに変更
function validateEmail(value: string, rules?: FieldValidationRule, t?: (key: string) => string): ValidationResult {
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!emailPattern.test(value)) {
    return { 
      isValid: false, 
      error: t ? t('validation.email_format') : 'メールアドレスの形式が正しくありません' 
    };
  }
  // ...
}
```

#### 8.5.2 バックエンド
エラーメッセージを多言語対応にする場合、`lang/ja/messages.php` と `lang/en/messages.php` に追加：

```php
// lang/ja/messages.php
return [
    // ...
    'validation.email_format' => 'メールアドレスの形式が正しくありません',
    'validation.max_length' => '最大:max文字まで入力できます',
    'validation.min_length' => '最低:min文字以上入力してください',
    'validation.number_min' => ':min以上である必要があります',
    'validation.number_max' => ':max以下である必要があります',
    // ...
];
```

### 8.6 実装の優先順位と段階的実装計画

#### フェーズ1: 基本バリデーション（優先度: 高）
1. ✅ **email形式チェック**（バックエンド実装済み: 2026-01-20）
   - ❌ フロントエンド: `validateEmail()` 実装（未実装）
   - ✅ バックエンド: `validateEmail()` 実装（`FieldValidationService`）
   - ✅ デフォルトでメールアドレス形式をチェック

2. ✅ **number範囲チェック**（バックエンド実装済み: 2026-01-20）
   - ❌ フロントエンド: `validateNumber()` 実装（未実装）
   - ✅ バックエンド: `validateNumber()` 実装（`FieldValidationService`）
   - ✅ `options_json.validation.min/max` を使用

3. ✅ **選択肢の妥当性チェック**（バックエンド実装済み: 2026-01-20）
   - ❌ フロントエンド: `validateSelect()`, `validateCheckbox()` 実装（未実装）
   - ✅ バックエンド: `validateSelect()`, `validateCheckbox()` 実装（`FieldValidationService`）
   - ✅ `options_json.options` を使用

#### フェーズ2: 拡張バリデーション（優先度: 中）
4. ✅ **date/time/datetime範囲チェック**（バックエンド実装済み: 2026-01-20）
   - ❌ フロントエンド: `validateDate()`, `validateTime()`, `validateDateTime()` 実装（未実装）
   - ✅ バックエンド: 実装済み（`FieldValidationService`）
   - ✅ `options_json.validation.min_date/max_date` を使用

5. ✅ **文字数制限**（バックエンド実装済み: 2026-01-20）
   - ❌ フロントエンド: `validateText()` に `max_length` チェック追加（未実装）
   - ✅ バックエンド: 実装済み（`FieldValidationService`）
   - ✅ `options_json.validation.max_length` を使用

#### フェーズ3: 高度なバリデーション（優先度: 低）
6. ✅ **パターンマッチング**（バックエンド実装済み: 2026-01-20）
   - ❌ フロントエンド: `validateText()` に `pattern` チェック追加（未実装）
   - ✅ バックエンド: 実装済み（`FieldValidationService`）
   - ✅ `options_json.validation.pattern` を使用

7. ⚠️ **ファイルバリデーション**（部分実装・要検討事項）
   - ❌ フロントエンド: `validateFile()` 実装（未実装）
   - ⚠️ バックエンド: 基本チェックのみ（実ファイルアップロード時は未実装）
   - `options_json.validation.allowed_extensions/max_file_size` を使用
   - **⚠️ セキュリティ上の懸念**: 不特定のユーザーからのファイルアップロード受付は、マルウェアや不正ファイルのアップロードリスクがあるため、実装前にセキュリティ対策の検討が必要
     - マルウェアスキャンの実装
     - ファイルタイプの厳格な検証（MIMEタイプ、マジックナンバー）
     - ファイル保存先の分離とアクセス制御
     - アップロード可能なファイルタイプのホワイトリスト方式
     - レート制限（DoS攻撃対策）

8. **リアルタイムバリデーション**（未実装）
   - フロントエンド: `handleFieldChange()` にリアルタイムバリデーション追加
   - UX向上のためのオプション機能

### 8.7 テスト計画

#### 8.7.1 フロントエンドテスト
- 各バリデーション関数のユニットテスト
- 統合テスト（PublicFormViewPage でのバリデーション動作確認）

#### 8.7.2 バックエンドテスト
- FieldValidationService のユニットテスト
- PublicFormsController::submit() の統合テスト

---

## 9. 参考資料

- `src/pages/public/PublicFormViewPage.tsx` (フロントエンドバリデーション)
- `app/Http/Controllers/Api/V1/PublicFormsController.php` (バックエンドバリデーション)
- `app/Services/RuleValidatorService.php` (条件分岐ルールのバリデーション)
- `app/Services/AnswerNormalizerService.php` (回答値の正規化)
- `app/Services/ConditionEvaluatorService.php` (条件分岐評価)
