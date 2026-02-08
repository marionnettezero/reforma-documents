# 項目バリデーションルールの実装状況

## 確認日時
2026-01-13（初版）  
2026-02-07（実装状況をコードベースに合わせて更新）  
2026-02-07（任意2項目実施・多言語化・他タブUX・最終残作業なし）

---

## 概要

現在のReFormaシステムにおける項目（フィールド）のバリデーションルールの実装状況をまとめます。

### 実装確認結果サマリ（2026-02-07 コードベース確認）

| 項目 | フロントエンド | バックエンド |
|------|----------------|--------------|
| 必須チェック（条件付き） | ✅ | ✅ |
| フィールドタイプ固有（email/number/日付/選択肢等） | ✅ `fieldValidation.ts` | ✅ `FieldValidationService` |
| 文字数・パターン・カスタムルール | ✅ | ✅ |
| condition_rule（値 op フィールド/定数） | ✅ | ✅ |
| matrix 選択制限 | ✅ ページ内 / 構造はバックエンド | ✅ |
| ファイル（サイズ・拡張子・MIME） | ✅ File 用 / 送信時はバックエンド | ✅ アップロード時実施（`max_file_size` に統一済み） |
| リアルタイムバリデーション | ✅ | — |
| 未実装・要対応 | 特になし（バリデーションは「入力条件」タブでUI実装済み。10節参照） | ファイル周りセキュリティは将来的な検討事項 |

---

## 1. フロントエンド（React）でのバリデーション

### 1.1 実装箇所
- **バリデーションロジック**: `src/utils/fieldValidation.ts`（`validateFieldValue`, `evaluateValidationConditionRule`）
- **公開フォーム**: `src/pages/public/PublicFormViewPage.tsx`（`validate()`, `handleFieldChange` 内のリアルタイムバリデーション）
- **プレビュー**: `src/pages/forms/FormPreviewPage.tsx`（`validate()`）
- **フィールド詳細パネル**: `src/components/FieldDetailPanel.tsx`（プレビュー用）

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

3. **フィールドタイプ固有のバリデーション**（`fieldValidation.ts`）
   - ✅ `text` / `textarea`: `max_length`, `min_length`, `pattern`
   - ✅ `email`: メール形式（デフォルト＋カスタム pattern）, `max_length`
   - ✅ `tel`: `pattern` 指定時
   - ✅ `number`: `min` / `max`
   - ✅ `date` / `time` / `datetime`（`datetime-local`）: 形式＋`min_*`/`max_*`
   - ✅ `select` / `radio` / `checkbox`: 選択肢の妥当性（`options`）
   - ✅ `file`: `allowed_extensions`, `max_file_size`, `min_file_size`（File オブジェクト時）

4. **検証条件（condition_rule）**
   - ✅ `evaluateValidationConditionRule`: 当該フィールドの値 op フィールド/定数（eq, ne, gt, gte, lt, lte, in, contains）

5. **matrix フィールド**
   - ✅ 選択制限チェック（global / per_header）は `PublicFormViewPage.tsx` の `validate()` 内で実施
   - matrix の構造・項目値の妥当性は `fieldValidation.ts` にはなく、バックエンドで検証

6. **リアルタイムバリデーション**
   - ✅ `handleFieldChange` 内で、値変更時に `validateFieldValue` を実行しエラー表示を更新（必須チェックは送信時のみ）

#### ⚠️ 注意・未実装（フロントエンド）
- **文字数**: `fieldValidation.ts` では `stringLength(value)`（`Array.from(value).length`）でカウントしており、PHP の `mb_strlen` と整合するよう修正済み。
- **file**: 公開フォームで実ファイル送信時はバックエンドで検証。フロントの `validateFile` は選択直後の File オブジェクト用。
- **バリデーションUI**: フィールド詳細の「入力条件」タブで `options_json.validation` をフォーム入力可能（10節参照）。

---

## 2. バックエンド（Laravel）でのバリデーション

### 2.1 実装箇所
- **コントローラ**: `app/Http/Controllers/Api/V1/PublicFormsController.php` の `submit()`（必須チェック・ファイルアップロード時検証・回答値の `FieldValidationService::validate` 呼び出し）
- **サービス**: `app/Services/FieldValidationService.php`（フィールドタイプ別検証、`evaluateConditionRule`、`validatePatternSyntax`）
- **フォーム編集時**: `app/Http/Controllers/Api/V1/FormsFieldsController.php`（`FieldValidationService` 利用）

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
   - ✅ `file`: 実ファイルアップロード時に `FieldValidationService::validateFile` で検証（`PublicFormsController::submit` 内で `$request->hasFile` のとき実行）。`validation.max_file_size`（バイト、後方互換で `max_size` も参照）, `allowed_extensions`, `allowed_mime_types` を参照。
     - **ファイル周りセキュリティ**: マルウェアスキャン・レート制限等は将来的な検討事項。

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

#### 将来的な検討事項
1. **ファイル周りセキュリティ**
   - 不特定ユーザーからのアップロードを許可する場合の追加対策（マルウェアスキャン、マジックナンバー、保存先分離・レート制限など）は、将来的な検討事項とする。

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
2. **リアルタイム**: ✅ 実装済み。`handleFieldChange` 内で値変更時に `validateFieldValue` を実行し、`errors` を更新（必須は送信時のみ）

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

5. ✅ **リアルタイムバリデーション**（実装済み）
   - `handleFieldChange` 内で入力中に `validateFieldValue` を実行

### 7.3 優先度: 低
6. ✅ **カスタムバリデーションルール**（フロント・バックエンドとも実装済み）
   - ✅ `options_json.validation` に定義されたバリデーションルールの適用

7. **バリデーションルールのUI設定**（実装済み）
   - フィールド詳細の「入力条件」タブで、最大文字数・パターン・数値範囲・日付範囲・ファイル制限・condition_rule を設定可能。詳細は「10. バリデーション専用UI（入力条件）」参照。

### 7.4 フロントエンド実装
- ✅ フィールドタイプ固有のバリデーションは `src/utils/fieldValidation.ts` で実装済み。公開フォーム・プレビューで利用。

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
1. ✅ **email形式チェック**
   - ✅ フロントエンド: `fieldValidation.ts` の `validateEmail()`
   - ✅ バックエンド: `FieldValidationService::validateEmail()`

2. ✅ **number範囲チェック**
   - ✅ フロントエンド: `validateNumber()`（`options_json.validation.min/max`）
   - ✅ バックエンド: `FieldValidationService::validateNumber()`

3. ✅ **選択肢の妥当性チェック**
   - ✅ フロントエンド: `validateSelect()`, `validateCheckbox()`（`options_json.options`）
   - ✅ バックエンド: `FieldValidationService::validateSelect()`, `validateCheckbox()`

#### フェーズ2: 拡張バリデーション（優先度: 中）
4. ✅ **date/time/datetime範囲チェック**
   - ✅ フロントエンド: `validateDate()`, `validateTime()`, `validateDateTime()`
   - ✅ バックエンド: `FieldValidationService` で同等実装

5. ✅ **文字数制限**
   - ✅ フロントエンド: `validateText()` の `max_length` / `min_length`（※文字数は `value.length`、多バイトはバックエンドと差あり得る）
   - ✅ バックエンド: `mb_strlen` で検証

#### フェーズ3: 高度なバリデーション（優先度: 低）
6. ✅ **パターンマッチング**
   - ✅ フロントエンド: `validateText()` 等で `pattern`（正規表現）
   - ✅ バックエンド: `matchPattern` / `normalizePatternForPreg` で検証

7. ✅ **ファイルバリデーション**（実装済み。キー名は `max_file_size` に統一済み）
   - ✅ フロントエンド: `validateFile()`（`allowed_extensions`, `max_file_size`, `min_file_size`）
   - ✅ バックエンド: アップロード時に `validateFile()`（`max_file_size` を優先、後方互換で `max_size` も参照）, `allowed_extensions`, `allowed_mime_types`
   - ファイル周りセキュリティは将来的な検討事項。

8. ✅ **リアルタイムバリデーション**
   - ✅ フロントエンド: `handleFieldChange()` 内で `validateFieldValue` を実行

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

---

## 10. バリデーション専用UI（入力条件）

### 10.1 現状：実装済み

**項目詳細設定（FieldDetailPanel）の「入力条件」タブ**で、`options_json.validation` を編集するUIが**既に実装されている**。ドキュメントで案として挙げていた「バリデーション専用UI」は、この機能と重複する。

- **タブ名**: 「入力条件」（タブキー `validation`）
- **対象フィールドタイプ**: text, textarea, email, tel, number, date, time, datetime, file（label / terms は非表示）
- **有効化**: 「有効化」ボタンで `editValidationRules` を有効にすると、以下をフォーム入力で設定可能。保存時に `options_json.validation` にマッピングされる。

| タイプ | 設定可能な項目（UIあり） |
|--------|--------------------------|
| text / textarea / email / tel | 最大文字数 (max_length)、最小文字数 (min_length)、正規表現パターン (pattern) |
| number | 最小値 (min)、最大値 (max) |
| date | 最小日付 (min_date)、最大日付 (max_date) |
| time | 最小時刻 (min_time)、最大時刻 (max_time) |
| datetime | 最小日時 (min_datetime)、最大日時 (max_datetime) |
| file | 許可拡張子 (allowed_extensions、カンマ区切り)、最大ファイルサイズ (max_file_size) [MB]、最小ファイルサイズ (min_file_size) [MB] |
| 上記いずれか | 検証条件 (condition_rule): 演算子 (op)、比較先 (value_type: フィールド/定数)、field_key または value |

- **condition_rule** も同一タブ内に UI があり、演算子・フィールド/定数・値の入力が可能。

したがって、「バリデーション専用UIは未実装」とする記述は誤り。**専用UIは「入力条件」タブとして既に存在する。**

### 10.2 正規表現パターンの構文チェック（実装済み）

- **API**: `POST /v1/forms/{id}/fields/validate-pattern`（body: `{ pattern: string }`）。レスポンス `data: { valid: true }` または `{ valid: false, error: string }`。保存は行わない。
- **フロント**: 入力条件タブの「正規表現パターン (pattern)」入力の横に「構文チェック」ボタンを配置。クリックで上記 API を呼び、直下に「パターンとして有効です」（緑）またはエラーメッセージ（赤）を表示。パターン文字列を変更すると結果をクリア。
- **バックエンド**: `FieldValidationService::validatePatternSyntax` を利用。既存の保存時バリデーション（`validateFieldValidationPatterns`）は変更なし。

### 10.3 UX調整案（ラベル・ヘルプ・必須項目の明示など）

以下は今後の検討用。他機能に影響しない範囲で、必要に応じて適用する。

#### ラベル・見出しの整理

| 現状 | 提案 | 備考 |
|------|------|------|
| タブ名「入力条件」のみ | タブに簡易説明を追加（ツールチップやサブラベル）「入力値の形式・文字数・範囲などを設定」 | 初見で何を設定するタブか分かりやすくする |
| 「最大文字数 (max_length)」など技術名併記 | そのままでも可。管理画面利用者が開発者でない場合は「最大文字数」のみにし、詳細はヘルプで説明 | 用途に応じて選択 |
| 「検証条件 (condition_rule)」 | 「値の条件（他フィールドや定数との比較）」など意味が伝わるラベルを併記 | 演算子・比較先の意味が取りやすいようにする |

#### ヘルプ文の整理

| 項目 | 現状 | 提案 |
|------|------|------|
| 正規表現パターン | 「正規表現パターンを入力してください（例: …）。デリミタなしでも保存できます。」 | 構文チェックの説明を追加「入力後は『構文チェック』で有効性を確認できます」 |
| 最大/最小文字数 | プレースホルダーのみ（例: 100, 1） | 空欄の場合は「未設定（制限なし）」とヘルプに一言 |
| 数値 min/max | プレースホルダーのみ | 同上。未設定時は範囲制限なしであることを明記 |
| 日付・時刻範囲 | 同上 | 形式（YYYY-MM-DD, HH:MM）をヘルプに明記 |
| ファイル 拡張子 | カンマ区切りと分かるが明示なし | 「カンマ区切りで入力（例: pdf, jpg, png）」をヘルプに追加 |
| ファイル 最大サイズ [MB] | 単位は表示済み | 「0 または空欄で制限なし」をヘルプに追加 |

#### 必須項目の明示

| 現状 | 提案 |
|------|------|
| 入力条件は「有効化」すると項目が表示されるが、どの項目が必須かはラベルからは分からない | 保存時にのみ必須の項目（例: 条件の演算子・比較先）には、ラベル横に「必須」バッジやアスタリスクを表示 |
| 数値範囲で min のみ・max のみの片方だけ設定可能 | ヘルプで「片方だけの設定も可能」と明記し、未設定側は制限なしと説明 |

#### エラー表示・保存時フィードバック

| 現状 | 提案 |
|------|------|
| 保存時に正規表現が不正だと 422 でエラー | 入力条件タブを開いた状態で保存失敗時、該当フィールドの「正規表現パターン」付近にエラーメッセージを表示する（既存の validationErrors をタブ内でも表示） |
| 入力条件の「無効化」で validation が空になる | 無効化時に「設定していた値は破棄されます」と確認メッセージを出す（任意） |

#### アクセシビリティ・キーボード

- 「構文チェック」ボタンに `aria-describedby` で結果メッセージの id を紐づけると、スクリーンリーダーで結果が読み上げられやすい。
- 入力条件ブロックに `role="group"` と `aria-labelledby` で見出しを紐づけると、フォーム構造が明確になる。

#### 優先度の目安

- **高**: 保存時エラー時に「どのフィールドの何が不正か」を入力条件タブ内でも表示する（デグレなし）。
- **中**: ヘルプ文の追加・正規表現の「構文チェック」の説明（今回の構文チェック実装と合わせて実施済みに近い）。
- **低**: ラベルの言い換え、必須バッジ、無効化時の確認、アクセシビリティ属性。

### 10.4 実施済みと残タスク

#### 実施済み（保存時エラー表示・優先度高 UX）

- **保存時エラーを入力条件タブ内に表示**
  - 一括保存（PUT /forms/{id}/fields）で 422 が返り、`errors.errors` にフィールド別メッセージが含まれる場合、親で `validationErrors` にマージするよう修正（FormEditIntegratedPage）。
  - 入力条件タブ先頭で、編集中フィールドの `validationErrors[editFieldKey]` があるときのみ、赤枠のアラートでメッセージを表示（FieldDetailPanel）。正規表現パターン入力の onChange で当該フィールドのエラーをクリア。
- **ヘルプ文の追加（優先度高〜中）**
  - 正規表現: 「入力後は『構文チェック』で有効性を確認できます」を追加。
  - 最大/最小文字数・数値 min/max: 「未設定の場合は制限なし」を追加。
  - 日付: 「形式 YYYY-MM-DD。未設定の場合は制限なし」を追加。
  - 時刻: 「形式 HH:MM。未設定の場合は制限なし」を追加。
  - 日時: 「未設定の場合は制限なし」を追加。
  - ファイル 最大サイズ: 「0 または空欄で制限なし」を追加。
  - ファイル 拡張子: 既存ヘルプ「カンマ区切りで拡張子を入力してください（例: pdf, jpg, png）」のまま。

#### 実施済み（中・低優先度を含む）

- **数値範囲**: ヘルプに「片方だけの設定も可能。未設定側は制限なし」を追加。
- **タブ「入力条件」**: ボタンに `title="入力値の形式・文字数・範囲などを設定"` を付与（ツールチップで簡易説明）。
- **検証条件 (condition_rule)**: ラベルにアスタリスク（*）を追加し、直下に HelpText「値の条件（他フィールドや定数との比較）。使用する場合は演算子・比較先の指定が必須です。」を追加。
- **必須の明示**: 検証条件セクションのラベルに * を表示。演算子・比較先は既存で「必須」表記済み。
- **無効化の確認**: 「無効化」クリック時に ConfirmDialog で「入力条件を無効化」「設定していた値は破棄されます。よろしいですか？」を表示し、確認後にのみ無効化。
- **アクセシビリティ**: 構文チェックボタンに `aria-describedby` で結果メッセージの id を紐づけ。結果メッセージに `id` と `role="status"` を付与。入力条件ブロックに `role="group"` と `aria-labelledby="validation-section-label"` を付与。

### 10.5 任意項目の実施済み（多言語化・他タブのUX）

- **ヘルプ文・確認メッセージの多言語化**
  - `PreferencesContext` の ja/en に、入力条件タブ用の翻訳キーを追加（`validation_help_*`, `validation_disable_confirm_*`, `validation_pattern_*`, `field_detail_tab_*_tooltip` 等）。
  - `FieldDetailPanel` 内の該当ラベル・ヘルプ・ConfirmDialog・構文チェックボタン文言をすべて `t("キー")` に変更。ロケール切り替えで英語表示に対応。
- **他タブのツールチップ・role="group"**
  - 全タブ（基本設定・選択肢・入力条件・条件分岐・高度な設定）のボタンに `title` を付与（ツールチップ）。キー: `field_detail_tab_basic_tooltip`, `field_detail_tab_options_tooltip`, `validation_tab_title_tooltip`, `field_detail_tab_conditions_tooltip`, `field_detail_tab_advanced_tooltip`。
  - 各タブのコンテンツブロックに `role="group"` と `aria-labelledby` を付与。見出しは `h2` + `className="sr-only"` で非表示ラベルとして配置（基本設定・選択肢・条件分岐・高度な設定）。入力条件は既存の `validation-section-label` を継続利用。

### 10.6 最終的な残作業

入力条件タブまわりのUX・保存時エラー表示・アクセシビリティ・多言語化、および他タブのツールチップ・`role="group"` まで実施済み。

**現時点で残っている作業はない。** 今後の機能追加や仕様変更に応じて、必要に応じて本ドキュメントと実装を更新する。
