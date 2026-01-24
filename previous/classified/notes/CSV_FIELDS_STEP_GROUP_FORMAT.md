# CSVフィールドエクスポート/インポートのSTEP/GROUP対応仕様

## 作成日時
2026-01-20

---

## 概要

現在のCSVフィールドエクスポート/インポート機能は、STEP/GROUP情報に対応していません。STEP式フォーム（STEP > GROUP > 複数項目）と単一式フォーム（GROUP > 複数項目）の両方に対応するため、新しいCSVフォーマットを定義し、バックエンド・フロントエンドの改修を行います。

### 実装状況（2026-01-20時点）

**フロントエンド**:
- ✅ STEP/GROUP構造の管理UI（FormItemPage.tsx）は実装済み
- ✅ ドラッグ&ドロップによるSTEP/GROUP/項目の階層構造編集が可能
- ✅ 条件分岐ルールのビルダーUIが実装済み

**バックエンド**:
- ⏳ STEP/GROUP構造のデータベース保存は未実装（`SUPP-FORM-STEP-001-spec.md`参照）
- ⏳ `forms.step_group_structure` JSONカラムの追加は未実装
- ⏳ `form_fields.step_key`, `form_fields.group_key`カラムの追加は未実装
- ✅ フォーム項目のCRUD操作（FormsFieldsController）は実装済み
- ✅ 条件分岐ルール（step_transition_rule）の評価は実装済み

**本仕様書の位置づけ**:
- STEP/GROUP構造のデータベース保存実装（`SUPP-FORM-STEP-001-spec.md`）と並行して、CSVインポート/エクスポート機能を拡張する仕様
- バックエンド側のデータベーススキーマ変更が完了した後に実装することを想定

---

## 現状の問題点

### 現在のCSVフォーマット

```csv
field_key,type,sort_order,is_required,options_json,visibility_rule,required_rule,step_transition_rule,computed_rule,pdf_block_key,pdf_page_number
field_key_1,select,0,true,"{""label"":""選択してください（日本語）"",""labels"":{""en"":""選択してください（英語）"",""ja"":""選択してください（日本語）""},""options"":[{""label"":""選択肢１"",""value"":""選択肢１""},{""label"":""選択肢２"",""value"":""選択肢２""},{""label"":""選択肢３"",""value"":""選択肢３""}]}",,,,,,
```

**問題点**:
- STEP/GROUP情報（`step_key`, `group_key`）が含まれていない
- STEP/GROUPの表示順序（`step_sort_order`, `group_sort_order`）が含まれていない
- STEP式フォームと単一式フォームの区別ができない
- インポート時にSTEP/GROUP構造を再現できない

---

## 新しいCSVフォーマット

### フォーマット仕様

#### 基本構造

```csv
step_key,group_key,step_sort_order,group_sort_order,step_name_i18n,group_name_i18n,field_key,type,sort_order,is_required,options_json,visibility_rule,required_rule,step_transition_rule,computed_rule,pdf_block_key,pdf_page_number
```

#### カラム説明

| カラム名 | 型 | 必須 | 説明 | 備考 |
|---------|-----|------|------|------|
| `step_key` | string | 条件付き | STEPのキー | STEP式フォームの場合のみ必須。単一式フォームの場合は空文字または`null` |
| `group_key` | string | 必須 | GROUPのキー | すべてのフォームで必須 |
| `step_sort_order` | integer | 条件付き | STEPの表示順序 | STEP式フォームの場合のみ必須。単一式フォームの場合は空文字または`null` |
| `group_sort_order` | integer | 必須 | GROUPの表示順序 | すべてのフォームで必須 |
| `step_name_i18n` | JSON string | 条件付き | STEP名（多言語対応） | STEP式フォームの場合のみ必須。形式: `{"ja":"基本情報","en":"Basic Information"}`。単一式フォームの場合は空文字または`null` |
| `group_name_i18n` | JSON string | 必須 | GROUP名（多言語対応） | すべてのフォームで必須。形式: `{"ja":"個人情報","en":"Personal Information"}` |
| `field_key` | string | 必須 | フィールド識別子 | 既存のカラム |
| `type` | string | 必須 | フィールドタイプ | 既存のカラム（text/email/select等） |
| `sort_order` | integer | 必須 | フィールドの表示順序 | 既存のカラム |
| `is_required` | boolean | 必須 | 固定必須フラグ | 既存のカラム |
| `options_json` | JSON string | 任意 | 選択肢など（JSON） | 既存のカラム |
| `visibility_rule` | JSON string | 任意 | 表示条件ルール（JSON） | 既存のカラム |
| `required_rule` | JSON string | 任意 | 必須条件ルール（JSON） | 既存のカラム |
| `step_transition_rule` | JSON string | 任意 | ステップ遷移ルール（JSON） | 既存のカラム |
| `computed_rule` | JSON string | 任意 | 計算フィールドルール（JSON） | 既存のカラム |
| `pdf_block_key` | string | 任意 | PDFテンプレート内のblock名 | 既存のカラム |
| `pdf_page_number` | integer | 任意 | PDFテンプレートのページ番号 | 既存のカラム |

#### フォーマット例

**STEP式フォームの場合**:
```csv
step_key,group_key,step_sort_order,group_sort_order,step_name_i18n,group_name_i18n,field_key,type,sort_order,is_required,options_json,visibility_rule,required_rule,step_transition_rule,computed_rule,pdf_block_key,pdf_page_number
step_1,group_1,0,0,"{""ja"":""基本情報"",""en"":""Basic Information""}","{""ja"":""個人情報"",""en"":""Personal Information""}",field_key_1,select,0,true,"{""label"":""選択してください"",""options"":[{""label"":""選択肢１"",""value"":""選択肢１""}]}",,,,,,
step_1,group_1,0,0,"{""ja"":""基本情報"",""en"":""Basic Information""}","{""ja"":""個人情報"",""en"":""Personal Information""}",field_key_2,text,1,false,,,,,,,,
step_1,group_2,0,1,"{""ja"":""基本情報"",""en"":""Basic Information""}","{""ja"":""連絡先"",""en"":""Contact""}",field_key_3,email,0,true,,,,,,,,
step_2,group_1,1,0,"{""ja"":""詳細情報"",""en"":""Detailed Information""}","{""ja"":""追加情報"",""en"":""Additional Information""}",field_key_4,number,0,false,,,,,,,,
```

**単一式フォームの場合**:
```csv
step_key,group_key,step_sort_order,group_sort_order,step_name_i18n,group_name_i18n,field_key,type,sort_order,is_required,options_json,visibility_rule,required_rule,step_transition_rule,computed_rule,pdf_block_key,pdf_page_number
,group_1,,0,,"{""ja"":""入力項目"",""en"":""Input Fields""}",field_key_1,select,0,true,"{""label"":""選択してください"",""options"":[{""label"":""選択肢１"",""value"":""選択肢１""}]}",,,,,,
,group_1,,0,,"{""ja"":""入力項目"",""en"":""Input Fields""}",field_key_2,text,1,false,,,,,,,,
,group_2,,1,,"{""ja"":""確認項目"",""en"":""Confirmation Fields""}",field_key_3,email,0,true,,,,,,,,
```

#### フォーマットの特徴

1. **後方互換性**: 既存のフィールド情報（`field_key`以降）は既存フォーマットと同じ
2. **STEP/GROUP情報の明示**: STEP/GROUPのキーと表示順序を明示的に指定
3. **フォームタイプの自動判定**: `step_key`が空の場合は単一式フォームとして扱う
4. **ソート順の保持**: STEP/GROUP/フィールドの表示順序を保持

---

## バックエンド改修仕様

### 1. データベーススキーマ変更

**注意**: 以下のデータベーススキーマ変更は、`SUPP-FORM-STEP-001-spec.md`で定義されている実装タスクと重複しています。CSVインポート/エクスポート機能の実装は、これらのスキーマ変更が完了した後に実施してください。

#### 1.1 form_fieldsテーブルへのカラム追加

**実装状況**: ⏳ 未実装（`SUPP-FORM-STEP-001-spec.md`の実装タスク参照）

```sql
ALTER TABLE form_fields
  ADD COLUMN step_key VARCHAR(255) NULL COMMENT 'STEP識別子（STEP式の場合、NULLの場合は単一式フォーム）' AFTER form_id,
  ADD COLUMN group_key VARCHAR(255) NULL COMMENT 'GROUP識別子' AFTER step_key;

ALTER TABLE form_fields
  ADD INDEX idx_form_step_group (form_id, step_key, group_key);
```

**注意**: 
- 既存データは`step_key = NULL`, `group_key = 'default'`として扱う
- `SUPP-FORM-STEP-001-spec.md`では`group_key`は`NULL`許可となっているが、CSVインポート時は必須として扱う

#### 1.2 formsテーブルへのカラム追加

**実装状況**: ⏳ 未実装（`SUPP-FORM-STEP-001-spec.md`の実装タスク参照）

```sql
ALTER TABLE forms
  ADD COLUMN step_group_structure JSON NULL COMMENT 'STEP/GROUP構造と名前情報（多言語対応）' AFTER theme_tokens;
```

**JSON構造の詳細**: `SUPP-FORM-STEP-001-spec.md`の「データモデル」セクションを参照

### 2. CsvImportServiceの改修

#### 2.1 exportFields()メソッドの改修

**ファイル**: `app/Services/CsvImportService.php`

**変更内容**:
- CSVエクスポート時に`step_key`, `group_key`, `step_sort_order`, `group_sort_order`, `step_name_i18n`, `group_name_i18n`カラムを追加
- `forms.step_group_structure`からSTEP/GROUP情報を取得
- フィールドの`step_key`, `group_key`を取得してCSVに含める
- STEP/GROUPの多言語名称（`step_name_i18n`, `group_name_i18n`）をJSON文字列としてCSVに含める

**実装例**:
```php
public function exportFields(Form $form): string
{
    // STEP/GROUP構造を取得
    $stepGroupStructure = $form->step_group_structure ?? [
        'is_step_form' => false,
        'steps' => null,
        'groups' => [],
    ];
    
    // フィールドを取得（step_key, group_keyを含む）
    $fields = $form->fields()->orderBy('step_key')
        ->orderBy('group_key')
        ->orderBy('sort_order')
        ->get();
    
    // CSVヘッダー
    $headers = [
        'step_key',
        'group_key',
        'step_sort_order',
        'group_sort_order',
        'step_name_i18n',
        'group_name_i18n',
        'field_key',
        'type',
        'sort_order',
        'is_required',
        'options_json',
        'visibility_rule',
        'required_rule',
        'step_transition_rule',
        'computed_rule',
        'pdf_block_key',
        'pdf_page_number',
    ];
    
    $rows = [];
    foreach ($fields as $field) {
        // STEP/GROUPのsort_orderと多言語名称を取得
        $stepSortOrder = null;
        $groupSortOrder = null;
        $stepNameI18n = null;
        $groupNameI18n = null;
        
        if ($stepGroupStructure['is_step_form'] && $field->step_key) {
            // STEP式フォームの場合
            foreach ($stepGroupStructure['steps'] ?? [] as $step) {
                if ($step['step_key'] === $field->step_key) {
                    $stepSortOrder = $step['sort_order'] ?? null;
                    $stepNameI18n = $step['step_name_i18n'] ?? [];
                    foreach ($step['groups'] ?? [] as $group) {
                        if ($group['group_key'] === $field->group_key) {
                            $groupSortOrder = $group['sort_order'] ?? null;
                            $groupNameI18n = $group['group_name_i18n'] ?? [];
                            break;
                        }
                    }
                    break;
                }
            }
        } else {
            // 単一式フォームの場合
            foreach ($stepGroupStructure['groups'] ?? [] as $group) {
                if ($group['group_key'] === $field->group_key) {
                    $groupSortOrder = $group['sort_order'] ?? null;
                    $groupNameI18n = $group['group_name_i18n'] ?? [];
                    break;
                }
            }
        }
        
        $rows[] = [
            $field->step_key ?? '',  // STEP式でない場合は空文字
            $field->group_key ?? 'default',
            $stepSortOrder ?? '',  // STEP式でない場合は空文字
            $groupSortOrder ?? 0,
            $stepNameI18n ? json_encode($stepNameI18n, JSON_UNESCAPED_UNICODE) : '',  // STEP式でない場合は空文字
            $groupNameI18n ? json_encode($groupNameI18n, JSON_UNESCAPED_UNICODE) : '',
            $field->field_key,
            $field->type,
            $field->sort_order,
            $field->is_required ? 'true' : 'false',
            $field->options_json ? json_encode($field->options_json, JSON_UNESCAPED_UNICODE) : '',
            $field->visibility_rule ? json_encode($field->visibility_rule, JSON_UNESCAPED_UNICODE) : '',
            $field->required_rule ? json_encode($field->required_rule, JSON_UNESCAPED_UNICODE) : '',
            $field->step_transition_rule ? json_encode($field->step_transition_rule, JSON_UNESCAPED_UNICODE) : '',
            $field->computed_rule ? json_encode($field->computed_rule, JSON_UNESCAPED_UNICODE) : '',
            $field->pdf_block_key ?? '',
            $field->pdf_page_number ?? '',
        ];
    }
    
    // CSV生成（既存の実装を参照）
    return $this->generateCsv($headers, $rows);
}
```

#### 2.2 importFields()メソッドの改修

**ファイル**: `app/Services/CsvImportService.php`

**変更内容**:
- CSVインポート時に`step_key`, `group_key`, `step_sort_order`, `group_sort_order`, `step_name_i18n`, `group_name_i18n`カラムを読み込む
- STEP/GROUP構造を構築して`forms.step_group_structure`に保存（多言語名称を含む）
- フィールドの`step_key`, `group_key`を設定

**実装例**:
```php
public function importFields(Form $form, string $csvContent): array
{
    $csvData = $this->parseCsv($csvContent);
    
    if (empty($csvData)) {
        throw new \InvalidArgumentException('CSVデータが空です');
    }
    
    // ヘッダーを確認
    $headers = array_shift($csvData);
    $expectedHeaders = [
        'step_key', 'group_key', 'step_sort_order', 'group_sort_order',
        'step_name_i18n', 'group_name_i18n',
        'field_key', 'type', 'sort_order', 'is_required',
        'options_json', 'visibility_rule', 'required_rule',
        'step_transition_rule', 'computed_rule', 'pdf_block_key', 'pdf_page_number',
    ];
    
    // 後方互換性: 旧フォーマット（step_key, group_keyがない場合）を検出
    $isLegacyFormat = !in_array('step_key', $headers);
    
    // STEP/GROUP構造を構築
    $stepGroupStructure = [
        'is_step_form' => false,
        'steps' => null,
        'groups' => [],
    ];
    
    $stepMap = [];
    $groupMap = [];
    $fields = [];
    
    foreach ($csvData as $row) {
        $rowData = array_combine($headers, $row);
        
        // 旧フォーマットの場合はデフォルト値を設定
        if ($isLegacyFormat) {
            $rowData['step_key'] = null;
            $rowData['group_key'] = 'default';
            $rowData['step_sort_order'] = null;
            $rowData['group_sort_order'] = 0;
            $rowData['step_name_i18n'] = null;
            $rowData['group_name_i18n'] = null;
        }
        
        $stepKey = !empty($rowData['step_key']) ? $rowData['step_key'] : null;
        $groupKey = $rowData['group_key'] ?? 'default';
        $stepSortOrder = !empty($rowData['step_sort_order']) ? (int)$rowData['step_sort_order'] : null;
        $groupSortOrder = !empty($rowData['group_sort_order']) ? (int)$rowData['group_sort_order'] : 0;
        
        // 多言語名称をパース
        $stepNameI18n = null;
        if (!empty($rowData['step_name_i18n'])) {
            $decoded = json_decode($rowData['step_name_i18n'], true);
            if (json_last_error() === JSON_ERROR_NONE) {
                $stepNameI18n = $decoded;
            }
        }
        
        $groupNameI18n = null;
        if (!empty($rowData['group_name_i18n'])) {
            $decoded = json_decode($rowData['group_name_i18n'], true);
            if (json_last_error() === JSON_ERROR_NONE) {
                $groupNameI18n = $decoded;
            }
        }
        
        // STEP式フォームかどうかを判定
        if ($stepKey !== null) {
            $stepGroupStructure['is_step_form'] = true;
            
            // STEP情報を収集
            if (!isset($stepMap[$stepKey])) {
                $stepMap[$stepKey] = [
                    'step_key' => $stepKey,
                    'step_name_i18n' => $stepNameI18n ?? [],
                    'sort_order' => $stepSortOrder ?? 0,
                    'groups' => [],
                ];
            }
            
            // GROUP情報を収集
            $stepGroupKey = "{$stepKey}:{$groupKey}";
            if (!isset($groupMap[$stepGroupKey])) {
                $stepMap[$stepKey]['groups'][] = [
                    'group_key' => $groupKey,
                    'group_name_i18n' => $groupNameI18n ?? [],
                    'sort_order' => $groupSortOrder,
                ];
                $groupMap[$stepGroupKey] = true;
            }
        } else {
            // 単一式フォームの場合
            if (!isset($groupMap[$groupKey])) {
                $stepGroupStructure['groups'][] = [
                    'group_key' => $groupKey,
                    'group_name_i18n' => $groupNameI18n ?? [],
                    'sort_order' => $groupSortOrder,
                ];
                $groupMap[$groupKey] = true;
            }
        }
        
        // フィールド情報を収集
        $fields[] = [
            'field_key' => $rowData['field_key'],
            'type' => $rowData['type'],
            'sort_order' => (int)($rowData['sort_order'] ?? 0),
            'is_required' => filter_var($rowData['is_required'] ?? false, FILTER_VALIDATE_BOOLEAN),
            'options_json' => !empty($rowData['options_json']) ? json_decode($rowData['options_json'], true) : null,
            'visibility_rule' => !empty($rowData['visibility_rule']) ? json_decode($rowData['visibility_rule'], true) : null,
            'required_rule' => !empty($rowData['required_rule']) ? json_decode($rowData['required_rule'], true) : null,
            'step_transition_rule' => !empty($rowData['step_transition_rule']) ? json_decode($rowData['step_transition_rule'], true) : null,
            'computed_rule' => !empty($rowData['computed_rule']) ? json_decode($rowData['computed_rule'], true) : null,
            'pdf_block_key' => $rowData['pdf_block_key'] ?? null,
            'pdf_page_number' => !empty($rowData['pdf_page_number']) ? (int)$rowData['pdf_page_number'] : null,
            'step_key' => $stepKey,
            'group_key' => $groupKey,
        ];
    }
    
    // STEP/GROUP構造をソート
    if ($stepGroupStructure['is_step_form']) {
        $stepGroupStructure['steps'] = array_values($stepMap);
        usort($stepGroupStructure['steps'], function ($a, $b) {
            return $a['sort_order'] <=> $b['sort_order'];
        });
        foreach ($stepGroupStructure['steps'] as &$step) {
            usort($step['groups'], function ($a, $b) {
                return $a['sort_order'] <=> $b['sort_order'];
            });
        }
    } else {
        usort($stepGroupStructure['groups'], function ($a, $b) {
            return $a['sort_order'] <=> $b['sort_order'];
        });
    }
    
    // フォームのSTEP/GROUP構造を保存
    $form->step_group_structure = $stepGroupStructure;
    $form->save();
    
    // フィールドを一括更新
    // 既存の実装を参照（PUT /v1/forms/{id}/fields のロジックを使用）
    // ...
    
    return [
        'success' => true,
        'imported_count' => count($fields),
        'step_group_structure' => $stepGroupStructure,
    ];
}
```

### 3. FormFieldモデルの改修

**ファイル**: `app/Models/FormField.php`

**変更内容**:
- `$fillable`に`step_key`, `group_key`を追加
- バリデーションルールに`step_key`, `group_key`を追加

```php
protected $fillable = [
    'form_id',
    'step_key',      // 追加
    'group_key',     // 追加
    'field_key',
    'type',
    'sort_order',
    'is_required',
    'options_json',
    'visibility_rule',
    'required_rule',
    'step_transition_rule',
    'computed_rule',
    'pdf_block_key',
    'pdf_page_number',
];
```

### 4. FormsFieldsControllerの改修

**ファイル**: `app/Http/Controllers/Api/FormsFieldsController.php`

**変更内容**:
- `importCsv()`メソッド: 既存の実装を維持（`CsvImportService::importFields()`の改修により自動的に対応）
- `exportFields()`メソッド: 既存の実装を維持（`CsvImportService::exportFields()`の改修により自動的に対応）

### 5. バリデーション

**追加するバリデーションルール**:
- `step_key`: STEP式フォームの場合のみ必須、文字列、最大255文字
- `group_key`: 必須、文字列、最大255文字
- `step_sort_order`: STEP式フォームの場合のみ必須、整数、0以上
- `group_sort_order`: 必須、整数、0以上
- `step_name_i18n`: STEP式フォームの場合のみ必須、JSON文字列、形式: `{"ja":"...","en":"..."}`（少なくとも1言語の名前が必要）
- `group_name_i18n`: 必須、JSON文字列、形式: `{"ja":"...","en":"..."}`（少なくとも1言語の名前が必要）

---

## フロントエンド改修仕様

### 1. CSVエクスポート機能の改修

#### 1.1 エクスポート処理

**ファイル**: `src/pages/forms/FormItemPage.tsx`（または該当コンポーネント）

**変更内容**:
- エクスポートボタンのクリック時に、新しいフォーマットでCSVをダウンロード
- 既存のAPIエンドポイント（`POST /v1/forms/{id}/fields/export/csv`）を使用（バックエンド側で新フォーマットに対応）

**実装例**:
```typescript
const handleExportFields = async () => {
  try {
    const response = await api.post(`/v1/forms/${formId}/fields/export/csv`);
    const { job_id } = response.data.data;
    
    // 進捗をポーリング
    await pollProgress(job_id, (progress) => {
      if (progress.status === 'succeeded' && progress.download_url) {
        // CSVをダウンロード
        window.location.href = progress.download_url;
      }
    });
  } catch (error) {
    console.error('CSVエクスポートエラー:', error);
    // エラーメッセージを表示
  }
};
```

#### 1.2 CSVプレビュー（オプション）

エクスポート前にCSVの内容をプレビューできる機能を追加することも検討できます。

### 2. CSVインポート機能の改修

#### 2.1 インポート処理

**ファイル**: `src/pages/forms/FormItemPage.tsx`（または該当コンポーネント）

**変更内容**:
- CSVファイルのアップロード時に、新フォーマットと旧フォーマットの両方に対応
- インポート前にCSVの内容を検証（STEP/GROUP構造の整合性チェック）

**実装例**:
```typescript
const handleImportFields = async (file: File) => {
  try {
    // CSVファイルを読み込んで検証
    const csvContent = await readFileAsText(file);
    const isValid = validateCsvFormat(csvContent);
    
    if (!isValid) {
      // エラーメッセージを表示
      return;
    }
    
    // 警告ダイアログを表示（既存の実装を参照）
    const confirmed = await showConfirmDialog({
      title: 'CSVインポート',
      message: '既存の項目がすべて置き換えられます。よろしいですか？',
    });
    
    if (!confirmed) {
      return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', 'fields');
    
    const response = await api.post(`/v1/forms/${formId}/fields/import/csv`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    const { job_id } = response.data.data;
    
    // 進捗をポーリング
    await pollProgress(job_id, (progress) => {
      if (progress.status === 'succeeded') {
        // 成功メッセージを表示
        // フォーム構造を再読み込み
        await reloadFormStructure();
      }
    });
  } catch (error) {
    console.error('CSVインポートエラー:', error);
    // エラーメッセージを表示
  }
};

// CSVフォーマットの検証
const validateCsvFormat = (csvContent: string): boolean => {
  const lines = csvContent.split('\n');
  if (lines.length < 2) {
    return false;
  }
  
  const headers = lines[0].split(',');
  const hasStepKey = headers.includes('step_key');
  const hasGroupKey = headers.includes('group_key');
  const hasFieldKey = headers.includes('field_key');
  
  // 最低限、field_keyが必要
  if (!hasFieldKey) {
    return false;
  }
  
  // 新フォーマット（step_key, group_keyがある）または旧フォーマット（field_key以降がある）を許可
  return true;
};
```

#### 2.2 CSVテンプレートの提供

新フォーマットに対応したCSVテンプレートを提供する機能を追加します。

**実装例**:
```typescript
const handleDownloadTemplate = () => {
  // テンプレートCSVを生成
  const template = generateCsvTemplate();
  
  // ダウンロード
  const blob = new Blob([template], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'fields_template.csv';
  link.click();
};

const generateCsvTemplate = (): string => {
  const headers = [
    'step_key',
    'group_key',
    'step_sort_order',
    'group_sort_order',
    'step_name_i18n',
    'group_name_i18n',
    'field_key',
    'type',
    'sort_order',
    'is_required',
    'options_json',
    'visibility_rule',
    'required_rule',
    'step_transition_rule',
    'computed_rule',
    'pdf_block_key',
    'pdf_page_number',
  ];
  
  const exampleRow = [
    '',  // step_key（単一式の場合は空）
    'group_1',  // group_key
    '',  // step_sort_order（単一式の場合は空）
    '0',  // group_sort_order
    '',  // step_name_i18n（単一式の場合は空）
    '{"ja":"入力項目","en":"Input Fields"}',  // group_name_i18n
    'field_key_1',  // field_key
    'text',  // type
    '0',  // sort_order
    'true',  // is_required
    '',  // options_json
    '',  // visibility_rule
    '',  // required_rule
    '',  // step_transition_rule
    '',  // computed_rule
    '',  // pdf_block_key
    '',  // pdf_page_number
  ];
  
  return [headers.join(','), exampleRow.join(',')].join('\n');
};
```

### 3. UI改善

#### 3.1 インポート/エクスポートボタン

既存のUIを維持しつつ、新フォーマットに対応したことを示すツールチップやヘルプテキストを追加します。

#### 3.2 エラーメッセージ

新フォーマットと旧フォーマットの両方に対応していることを明示するエラーメッセージを追加します。

---

## 後方互換性

### 旧フォーマットのサポート

- **エクスポート**: 常に新フォーマットでエクスポート
- **インポート**: 旧フォーマット（`step_key`, `group_key`がない）と新フォーマットの両方に対応
  - 旧フォーマットの場合: `step_key = null`, `group_key = 'default'`として処理

### 移行ガイド

既存のCSVファイルを新フォーマットに移行する場合:

1. 旧フォーマットのCSVをエクスポート
2. 新フォーマットのCSVをエクスポート（新フォーマットで再エクスポート）
3. 必要に応じて手動で`step_key`, `group_key`を追加

---

## 実装優先順位

### 前提条件

**重要**: 本機能の実装は、`SUPP-FORM-STEP-001-spec.md`で定義されている以下の実装が完了していることを前提とします：

1. ✅ データベーススキーマ変更（`forms.step_group_structure`, `form_fields.step_key`, `form_fields.group_key`）
2. ✅ モデル拡張（`Form`, `FormField`）
3. ✅ API拡張（`PUT /v1/forms/{id}/fields`, `GET /v1/forms/{id}/fields`）

### フェーズ1: バックエンド実装（CSV機能拡張）

**前提**: `SUPP-FORM-STEP-001-spec.md`の実装が完了していること

1. `FormField`モデルの確認（`step_key`, `group_key`が`$fillable`に含まれていることを確認）
2. `CsvImportService::exportFields()`の改修
   - `forms.step_group_structure`からSTEP/GROUP情報を取得
   - フィールドの`step_key`, `group_key`をCSVに含める
3. `CsvImportService::importFields()`の改修
   - CSVから`step_key`, `group_key`, `step_sort_order`, `group_sort_order`を読み込む
   - STEP/GROUP構造を構築して`forms.step_group_structure`に保存
   - フィールドの`step_key`, `group_key`を設定
4. バリデーションルールの追加
   - `step_key`, `group_key`, `step_sort_order`, `group_sort_order`のバリデーション

### フェーズ2: フロントエンド実装

**前提**: フェーズ1が完了していること

1. CSVエクスポート機能の確認
   - 既存のエクスポートボタンが新フォーマットで動作することを確認
   - バックエンド側の変更で自動的に対応されることを確認
2. CSVインポート機能の改修
   - 旧フォーマット（`step_key`, `group_key`がない）の検出と対応
   - CSVフォーマットの検証機能
3. CSVテンプレートの提供機能
   - 新フォーマットに対応したテンプレートCSVの生成
   - ダウンロード機能
4. UI改善
   - エラーメッセージの改善
   - ツールチップやヘルプテキストの追加

### フェーズ3: テスト

1. 単体テスト
   - `CsvImportService::exportFields()`のテスト
   - `CsvImportService::importFields()`のテスト
   - 旧フォーマット対応のテスト
2. 統合テスト
   - CSVエクスポート→インポートの一連の流れのテスト
   - STEP式フォームと単一式フォームの両方のテスト
3. エンドツーエンドテスト
   - フロントエンドからCSVエクスポート/インポートを実行するテスト

---

## 参考資料

- `SUPP-FIELD-CSV-001-spec.md`: 既存のCSVインポート/エクスポート仕様
- `SUPP-FORM-STEP-001-spec.md`: STEP/GROUP構造の実装仕様（**必須参照**）
  - データモデル定義
  - API仕様（`PUT /v1/forms/{id}/fields`, `GET /v1/forms/{id}/fields`）
  - 実装タスク一覧
  - 後方互換性の取り扱い
- `reforma-db-spec-v0.1.2.md`: データベーススキーマ仕様（現在のスキーマ）
- `TODO_STATUS.md`: 実装状況の最新情報
- `REQUIREMENT_CHECK_RESULT.md`: 要件適合性チェック結果

---

## まとめ

新しいCSVフォーマットにより、STEP/GROUP情報を含むフォーム構造を完全にエクスポート/インポートできるようになります。後方互換性を維持しつつ、段階的に実装を進めることで、既存のワークフローに影響を与えずに機能を拡張できます。
