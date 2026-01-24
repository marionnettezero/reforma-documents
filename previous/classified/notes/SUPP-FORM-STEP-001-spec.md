# SUPP-FORM-STEP-001: STEP式フォーム / 単一式フォーム管理 実装仕様

**作成日**: 2026-01-22  
**最終更新日**: 2026-01-20  
**バージョン**: v1.0.0  
**実装状況**: ✅ **全て実装済み**（2026-01-20完了）

---

## 概要

フォーム項目の管理において、STEP式フォーム（STEP > GROUP > 複数項目）と単一式フォーム（GROUP > 複数項目）の両方をサポートする。STEP/GROUP共に多言語対応した名前を持ち、データの冗長性を避けるため、ハイブリッドアプローチ（formsテーブルのJSONカラム + form_fieldsテーブルの参照キー）で実装する。

---

## 実装状況

### ✅ 実装完了（2026-01-20）

**バックエンド**:
- ✅ STEP/GROUP構造のデータベース保存
  - `forms.step_group_structure` JSONカラム追加
  - `form_fields.step_key`, `form_fields.group_key`カラム追加
  - インデックス追加（`idx_form_step_group`）
- ✅ STEP/GROUP名の多言語対応
  - `step_group_structure`に多言語名を保存
  - APIレスポンスに`step_group_structure`を含める
- ✅ 単一式フォームのサポート
  - `is_step_form`フラグでSTEP式/単一式を区別
  - 単一式フォームは`groups`配列にGROUP情報を格納
- ✅ バリデーション強化
  - STEP/GROUP名の必須チェック（少なくとも1言語の名前が必要）
  - データ整合性チェック（STEP/GROUP構造とフィールドの整合性）
- ✅ 既存データのマイグレーション処理
  - 既存`form_fields`データに`group_key = 'default'`を設定
  - 既存`forms`データにデフォルト`step_group_structure`を設定
- ✅ 公開フォームAPI拡張
  - `GET /v1/public/forms/{form_key}`に`step_group_structure`を追加
  - フィールド情報に`step_key`, `group_key`を追加

**フロントエンド**:
- ✅ 型定義拡張（`Step`, `Group`, `FormField`, `FieldsResponse`）
- ✅ データ取得・構築（`step_group_structure`からSTEP/GROUP構造を構築）
- ✅ 後方互換性の処理（既存データの対応）
- ✅ UI実装
  - フォームタイプ選択UI（STEP式/単一式）
  - STEP名の多言語編集UI
  - GROUP名の多言語編集UI
  - 単一式フォームの初期化処理
- ✅ データ保存（`flattenStepGroupStructure()`, `handleSave()`）
- ✅ バリデーション強化（STEP/GROUP名の必須チェック）
- ✅ 翻訳対応（翻訳キー追加）
- ✅ 公開フォーム表示でのSTEP/GROUP名表示
  - STEP/GROUP構造に基づいてフィールドをグループ化
  - ロケールに応じた多言語名の表示

**詳細な実装状況**: `SUPP-FORM-STEP-001-IMPLEMENTATION-STATUS.md`を参照

---

## バックエンド実装状況

### 現在の実装状況

**実装済み**:
- ✅ STEP/GROUP構造のデータベース保存
- ✅ STEP/GROUP名の多言語対応
- ✅ 単一式フォームのサポート
- ✅ フォーム項目のCRUD操作（FormsFieldsController）
- ✅ 条件分岐ルール（step_transition_rule）の評価
- ✅ フロントエンド側でのSTEP/GROUP構造管理（FormItemPage.tsx）
- ✅ バリデーション強化（STEP/GROUP名の必須チェック、データ整合性チェック）
- ✅ 既存データのマイグレーション処理
- ✅ 公開フォームAPI拡張

---

## データモデル

### 1. formsテーブルの拡張

**追加カラム**:
```sql
ALTER TABLE forms 
ADD COLUMN step_group_structure JSON NULL COMMENT 'STEP/GROUP構造と名前情報（多言語対応）';
```

**JSON構造（STEP式フォーム）**:
```json
{
  "is_step_form": true,
  "steps": [
    {
      "step_key": "step_1",
      "step_name_i18n": {
        "ja": "基本情報",
        "en": "Basic Information"
      },
      "sort_order": 0,
      "groups": [
        {
          "group_key": "group_1",
          "group_name_i18n": {
            "ja": "個人情報",
            "en": "Personal Information"
          },
          "sort_order": 0
        }
      ]
    }
  ]
}
```

**JSON構造（単一式フォーム）**:
```json
{
  "is_step_form": false,
  "steps": null,
  "groups": [
    {
      "group_key": "group_1",
      "group_name_i18n": {
        "ja": "入力項目",
        "en": "Input Fields"
      },
      "sort_order": 0
    }
  ]
}
```

**注意事項**:
- `is_step_form`: STEP式フォームかどうかを示すフラグ
- STEP式の場合: `steps`配列にSTEP情報を格納
- 単一式の場合: `steps`は`null`、`groups`配列にGROUP情報を格納
- 各STEP/GROUPの`sort_order`は表示順序を管理

### 2. form_fieldsテーブルの拡張

**追加カラム**:
```sql
ALTER TABLE form_fields 
ADD COLUMN step_key VARCHAR(255) NULL COMMENT 'STEP識別子（STEP式の場合、NULLの場合は単一式フォーム）',
ADD COLUMN group_key VARCHAR(255) NULL COMMENT 'GROUP識別子',
ADD INDEX idx_form_step_group (form_id, step_key, group_key);
```

**データ構造**:
- `step_key`: STEP式フォームの場合、対応するSTEPのキー。単一式フォームの場合は`NULL`
- `group_key`: フィールドが属するGROUPのキー（必須）
- インデックス: `form_id`, `step_key`, `group_key`の組み合わせで検索を高速化

**後方互換性**:
- 既存データは`step_key = NULL`, `group_key = "default"`として扱う
- `step_group_structure`が`NULL`の場合は、既存のフロントエンド実装と同様に`step_key = "default"`, `group_key = "default"`として処理

---

## バックエンド実装

### 1. Formモデルの拡張

**ファイル**: `app/Models/Form.php`

**追加内容**:
```php
protected $fillable = [
    // ... 既存フィールド
    'step_group_structure',  // 追加
];

protected $casts = [
    // ... 既存キャスト
    'step_group_structure' => 'array',  // 追加
];
```

### 2. FormFieldモデルの拡張

**ファイル**: `app/Models/FormField.php`

**追加内容**:
```php
protected $fillable = [
    // ... 既存フィールド
    'step_key',   // 追加
    'group_key',  // 追加
];
```

### 3. FormsFieldsController::update() の拡張

**ファイル**: `app/Http/Controllers/Api/V1/FormsFieldsController.php`

**変更内容**:

#### 3.1. リクエストバリデーション拡張

```php
$rules = [
    'fields' => ['required', 'array'],
    'fields.*.field_key' => ['required', 'string', 'max:255'],
    'fields.*.type' => ['required', 'string', 'max:64'],
    'fields.*.step_key' => ['nullable', 'string', 'max:255'],  // 追加
    'fields.*.group_key' => ['nullable', 'string', 'max:255'], // 追加
    'fields.*.step_name_i18n' => ['nullable', 'array'],        // 追加
    'fields.*.group_name_i18n' => ['nullable', 'array'],      // 追加
    // ... 既存のバリデーションルール
];
```

#### 3.2. STEP/GROUP構造の抽出と保存

```php
public function update(Request $request, $formId)
{
    $validated = $request->validate($rules);
    $fields = $validated['fields'];
    
    // STEP/GROUP構造を抽出
    $stepGroupStructure = $this->extractStepGroupStructure($fields);
    
    // formsテーブルに保存
    $form = Form::findOrFail($formId);
    $form->step_group_structure = $stepGroupStructure;
    $form->save();
    
    // フィールドにはstep_key/group_keyのみ保存（名前情報は保存しない）
    foreach ($fields as $fieldData) {
        FormField::updateOrCreate(
            [
                'form_id' => $formId,
                'field_key' => $fieldData['field_key']
            ],
            [
                'step_key' => $fieldData['step_key'] ?? null,
                'group_key' => $fieldData['group_key'] ?? 'default',
                // step_name_i18n, group_name_i18nは保存しない（冗長性回避）
                // ... 既存のフィールド更新処理
            ]
        );
    }
    
    return ApiResponse::success($request, [
        'fields' => FormField::where('form_id', $formId)->get(),
    ]);
}

/**
 * STEP/GROUP構造を抽出
 * 
 * @param array $fields フィールド配列
 * @return array STEP/GROUP構造
 */
private function extractStepGroupStructure(array $fields): array
{
    $stepMap = [];
    $groupMap = [];
    $isStepForm = false;
    
    foreach ($fields as $field) {
        $stepKey = $field['step_key'] ?? null;
        $groupKey = $field['group_key'] ?? 'default';
        $stepNameI18n = $field['step_name_i18n'] ?? null;
        $groupNameI18n = $field['group_name_i18n'] ?? null;
        
        // STEP式フォームかどうかを判定
        if ($stepKey !== null && $stepKey !== 'default') {
            $isStepForm = true;
            
            // STEP情報を収集
            if (!isset($stepMap[$stepKey])) {
                $stepMap[$stepKey] = [
                    'step_key' => $stepKey,
                    'step_name_i18n' => $stepNameI18n ?? [],
                    'sort_order' => count($stepMap),
                    'groups' => []
                ];
            }
            
            // GROUP情報を収集（STEP配下）
            $stepGroupKey = "{$stepKey}:{$groupKey}";
            if (!isset($groupMap[$stepGroupKey])) {
                $stepMap[$stepKey]['groups'][] = [
                    'group_key' => $groupKey,
                    'group_name_i18n' => $groupNameI18n ?? [],
                    'sort_order' => count($stepMap[$stepKey]['groups'])
                ];
                $groupMap[$stepGroupKey] = true;
            }
        } else {
            // 単一式フォーム: GROUP情報のみ収集
            if (!isset($groupMap[$groupKey])) {
                $groupMap[$groupKey] = [
                    'group_key' => $groupKey,
                    'group_name_i18n' => $groupNameI18n ?? [],
                    'sort_order' => count($groupMap)
                ];
            }
        }
    }
    
    // 構造を構築
    if ($isStepForm) {
        return [
            'is_step_form' => true,
            'steps' => array_values($stepMap),
            'groups' => null
        ];
    } else {
        return [
            'is_step_form' => false,
            'steps' => null,
            'groups' => array_values($groupMap)
        ];
    }
}
```

### 4. FormsFieldsController::index() の拡張

**ファイル**: `app/Http/Controllers/Api/V1/FormsFieldsController.php`

**変更内容**:

```php
public function index(Request $request, $formId)
{
    $form = Form::findOrFail($formId);
    $fields = FormField::where('form_id', $formId)
        ->orderBy('sort_order')
        ->get();
    
    // step_group_structureを取得
    $stepGroupStructure = $form->step_group_structure ?? [
        'is_step_form' => false,
        'steps' => null,
        'groups' => null
    ];
    
    return ApiResponse::success($request, [
        'fields' => $fields,
        'step_group_structure' => $stepGroupStructure  // 追加
    ]);
}
```

**レスポンス構造**:
```json
{
  "success": true,
  "data": {
    "fields": [
      {
        "id": 1,
        "form_id": 1,
        "field_key": "name",
        "type": "text",
        "step_key": "step_1",
        "group_key": "group_1",
        "sort_order": 0,
        ...
      }
    ],
    "step_group_structure": {
      "is_step_form": true,
      "steps": [
        {
          "step_key": "step_1",
          "step_name_i18n": {
            "ja": "基本情報",
            "en": "Basic Information"
          },
          "sort_order": 0,
          "groups": [
            {
              "group_key": "group_1",
              "group_name_i18n": {
                "ja": "個人情報",
                "en": "Personal Information"
              },
              "sort_order": 0
            }
          ]
        }
      ],
      "groups": null
    }
  }
}
```

---

## フロントエンド実装

### 1. 型定義の拡張

**ファイル**: `src/pages/forms/FormItemPage.tsx`

**変更内容**:

```typescript
type Step = {
  step_key: string | null;  // nullの場合は単一式フォーム
  step_name_i18n: Record<string, string> | null;  // { locale: name }
  groups: Group[];
};

type Group = {
  group_key: string;
  group_name_i18n: Record<string, string>;  // { locale: name }
  fields: FormField[];
};

type FormField = {
  id: number;
  form_id: number;
  field_key: string;
  type: string;
  step_key: string | null;  // 追加
  group_key: string;         // 追加
  step_name_i18n: Record<string, string> | null;  // 追加（APIから取得時のみ）
  group_name_i18n: Record<string, string>;        // 追加（APIから取得時のみ）
  sort_order: number;
  ...
};

type FieldsResponse = {
  success: boolean;
  data: {
    fields: FormField[];
    step_group_structure: {  // 追加
      is_step_form: boolean;
      steps: Array<{
        step_key: string;
        step_name_i18n: Record<string, string>;
        sort_order: number;
        groups: Array<{
          group_key: string;
          group_name_i18n: Record<string, string>;
          sort_order: number;
        }>;
      }> | null;
      groups: Array<{
        group_key: string;
        group_name_i18n: Record<string, string>;
        sort_order: number;
      }> | null;
    };
  };
};
```

### 2. データ取得時の構造構築

**ファイル**: `src/pages/forms/FormItemPage.tsx`

**変更内容**:

```typescript
const loadFields = async () => {
  try {
    const response = await apiGetJson<FieldsResponse>(
      `/v1/forms/${formId}/fields`
    );
    
    if (response.success && response.data) {
      const { fields, step_group_structure } = response.data;
      
      // step_group_structureからSTEP/GROUP構造を構築
      if (step_group_structure.is_step_form && step_group_structure.steps) {
        // STEP式フォーム
        const steps: Step[] = step_group_structure.steps.map((step) => ({
          step_key: step.step_key,
          step_name_i18n: step.step_name_i18n,
          groups: step.groups.map((group) => ({
            group_key: group.group_key,
            group_name_i18n: group.group_name_i18n,
            fields: fields.filter(
              (f) => f.step_key === step.step_key && f.group_key === group.group_key
            ),
          })),
        }));
        setSteps(steps);
        setHasSteps(true);
      } else if (step_group_structure.groups) {
        // 単一式フォーム
        const groups: Group[] = step_group_structure.groups.map((group) => ({
          group_key: group.group_key,
          group_name_i18n: group.group_name_i18n,
          fields: fields.filter((f) => f.group_key === group.group_key),
        }));
        setSteps([
          {
            step_key: null,
            step_name_i18n: null,
            groups: groups,
          },
        ]);
        setHasSteps(false);
      } else {
        // 既存データ（後方互換性）
        // 既存のロジックで処理
      }
    }
  } catch (error) {
    // エラーハンドリング
  }
};
```

### 3. 初期表示時の選択UI

**ファイル**: `src/pages/forms/FormItemPage.tsx`

**実装内容**:

```typescript
// フォームタイプ選択状態
const [formType, setFormType] = useState<"step" | "single" | null>(null);

// 初期表示時の選択UI
{steps.length === 0 && formType === null && (
  <div className="rounded-xl border border-white/10 bg-black/20 p-8">
    <div className="text-center space-y-4">
      <h3 className="text-lg font-bold mb-4">
        {t("form_item_select_type") || "フォームタイプを選択してください"}
      </h3>
      <div className="flex gap-4 justify-center">
        <button
          type="button"
          className={`rounded-xl px-6 py-4 text-sm font-bold border-2 ${
            uiTokens.buttonPrimary
          }`}
          onClick={() => {
            setFormType("step");
            addStep(); // STEPを追加
          }}
        >
          {t("form_item_step_form") || "STEP式フォーム"}
        </button>
        <button
          type="button"
          className={`rounded-xl px-6 py-4 text-sm font-bold border-2 ${
            uiTokens.buttonSecondary
          }`}
          onClick={() => {
            setFormType("single");
            // 単一式フォームの初期化
            const defaultGroup: Group = {
              group_key: "default",
              group_name_i18n: formAddedLanguages.reduce((acc, lang) => {
                acc[lang] = lang === 'ja' ? '入力項目' : 'Input Fields';
                return acc;
              }, {} as Record<string, string>),
              fields: [],
            };
            setSteps([{
              step_key: null,
              step_name_i18n: null,
              groups: [defaultGroup],
            }]);
            setHasSteps(false);
          }}
        >
          {t("form_item_single_form") || "単一式フォーム"}
        </button>
      </div>
    </div>
  </div>
)}
```

### 4. STEP/GROUP名の多言語編集UI

**ファイル**: `src/pages/forms/FormItemPage.tsx`

**実装内容**:

#### 4.1. STEP名編集UI

```typescript
// STEP名の多言語編集UI
<div className="space-y-3">
  <div className="text-xs font-bold">STEP名（多言語対応）</div>
  {formAddedLanguages.map((lang) => (
    <div key={lang}>
      <label className={`block text-xs font-bold mb-1 ${uiTokens.muted}`}>
        {lang === 'ja' ? '日本語' : 'English'}
      </label>
      <input
        className={`w-full rounded-xl border px-3 py-2 text-sm ${uiTokens.input}`}
        value={step.step_name_i18n?.[lang] || ''}
        onChange={(e) => {
          const updatedSteps = [...steps];
          updatedSteps[stepIndex].step_name_i18n = {
            ...updatedSteps[stepIndex].step_name_i18n,
            [lang]: e.target.value,
          };
          setSteps(updatedSteps);
        }}
        placeholder={lang === 'ja' ? 'STEP名を入力' : 'Enter step name'}
      />
    </div>
  ))}
</div>
```

#### 4.2. GROUP名編集UI

```typescript
// GROUP名の多言語編集UI
<div className="space-y-3">
  <div className="text-xs font-bold">GROUP名（多言語対応）</div>
  {formAddedLanguages.map((lang) => (
    <div key={lang}>
      <label className={`block text-xs font-bold mb-1 ${uiTokens.muted}`}>
        {lang === 'ja' ? '日本語' : 'English'}
      </label>
      <input
        className={`w-full rounded-xl border px-3 py-2 text-sm ${uiTokens.input}`}
        value={group.group_name_i18n?.[lang] || ''}
        onChange={(e) => {
          const updatedSteps = [...steps];
          updatedSteps[stepIndex].groups[groupIndex].group_name_i18n = {
            ...updatedSteps[stepIndex].groups[groupIndex].group_name_i18n,
            [lang]: e.target.value,
          };
          setSteps(updatedSteps);
        }}
        placeholder={lang === 'ja' ? 'GROUP名を入力' : 'Enter group name'}
      />
    </div>
  ))}
</div>
```

### 5. データ保存時の変換

**ファイル**: `src/pages/forms/FormItemPage.tsx`

**実装内容**:

```typescript
// STEP/GROUP構造からフラットな配列に変換
function flattenStepGroupStructure(steps: Step[]): FormField[] {
  const fields: FormField[] = [];
  let sortOrder = 0;

  steps.forEach((step) => {
    step.groups.forEach((group) => {
      group.fields.forEach((field) => {
        fields.push({
          ...field,
          step_key: step.step_key,  // nullの場合は単一式フォーム
          group_key: group.group_key,
          step_name_i18n: step.step_name_i18n,  // 保存時に送信（冗長性はバックエンドで排除）
          group_name_i18n: group.group_name_i18n,  // 保存時に送信（冗長性はバックエンドで排除）
          sort_order: sortOrder++,
        });
      });
    });
  });

  return fields;
}

// 保存処理
const handleSave = async () => {
  try {
    setIsSaving(true);
    
    // STEP/GROUP構造をフラットな配列に変換
    const fields = flattenStepGroupStructure(steps);
    
    // APIに送信
    const response = await apiPutJson(
      `/v1/forms/${formId}/fields`,
      { fields }
    );
    
    if (response.success) {
      // 成功時の処理
      showSuccess(t("form_item_save_success") || "保存しました");
    }
  } catch (error) {
    // エラーハンドリング
  } finally {
    setIsSaving(false);
  }
};
```

---

## API仕様

### PUT /v1/forms/{id}/fields

**概要**: フォーム項目一括更新（STEP/GROUP構造対応）

**リクエストボディ**:
```json
{
  "fields": [
    {
      "field_key": "name",
      "type": "text",
      "step_key": "step_1",
      "group_key": "group_1",
      "step_name_i18n": {
        "ja": "基本情報",
        "en": "Basic Information"
      },
      "group_name_i18n": {
        "ja": "個人情報",
        "en": "Personal Information"
      },
      "sort_order": 0,
      "is_required": true,
      ...
    }
  ]
}
```

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "fields": [
      {
        "id": 1,
        "form_id": 1,
        "field_key": "name",
        "step_key": "step_1",
        "group_key": "group_1",
        ...
      }
    ]
  }
}
```

**注意事項**:
- `step_key`: STEP式フォームの場合、必須。単一式フォームの場合は`null`または省略
- `group_key`: 必須
- `step_name_i18n`, `group_name_i18n`: 保存時に送信するが、バックエンドで`forms.step_group_structure`に集約され、`form_fields`には保存されない（冗長性回避）

### GET /v1/forms/{id}/fields

**概要**: フォーム項目一覧取得（STEP/GROUP構造対応）

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "fields": [
      {
        "id": 1,
        "form_id": 1,
        "field_key": "name",
        "step_key": "step_1",
        "group_key": "group_1",
        ...
      }
    ],
    "step_group_structure": {
      "is_step_form": true,
      "steps": [
        {
          "step_key": "step_1",
          "step_name_i18n": {
            "ja": "基本情報",
            "en": "Basic Information"
          },
          "sort_order": 0,
          "groups": [
            {
              "group_key": "group_1",
              "group_name_i18n": {
                "ja": "個人情報",
                "en": "Personal Information"
              },
              "sort_order": 0
            }
          ]
        }
      ],
      "groups": null
    }
  }
}
```

---

## 実装タスク

**実装完了日**: 2026-01-20  
**実装状況**: ✅ 全て実装済み

### バックエンド

#### データベーススキーマ拡張
- ✅ `forms`テーブルに`step_group_structure` JSONカラムを追加（マイグレーション作成）
- ✅ `form_fields`テーブルに`step_key`, `group_key`カラムを追加（マイグレーション作成）
- ✅ `form_fields`テーブルにインデックス追加（`form_id`, `step_key`, `group_key`）

#### モデル拡張
- ✅ `Form`モデルの`$fillable`に`step_group_structure`を追加
- ✅ `Form`モデルの`$casts`に`step_group_structure => 'array'`を追加
- ✅ `FormField`モデルの`$fillable`に`step_key`, `group_key`を追加

#### API拡張
- ✅ `FormsFieldsController::update()`のバリデーション拡張
- ✅ `FormsFieldsController::update()`にSTEP/GROUP構造抽出ロジックを追加
- ✅ `FormsFieldsController::update()`で`forms.step_group_structure`を保存
- ✅ `FormsFieldsController::index()`のレスポンスに`step_group_structure`を追加
- ✅ `PublicFormsController::show()`のレスポンスに`step_group_structure`を追加
- ✅ バリデーション強化（`validateStepGroupNames()`メソッド追加）
- ✅ データ整合性チェック（`validateStepGroupConsistency()`メソッド追加）
- ✅ 既存データのマイグレーション処理

### フロントエンド

#### 型定義拡張
- ✅ `Step`, `Group`, `FormField`型定義を拡張
- ✅ `FieldsResponse`型定義に`step_group_structure`を追加
- ✅ `FormViewResponse`型定義に`step_group_structure`を追加（公開フォーム用）

#### データ取得・構築
- ✅ `loadFields()`関数で`step_group_structure`からSTEP/GROUP構造を構築
- ✅ 後方互換性の処理（既存データの対応）

#### UI実装
- ✅ 初期表示時のフォームタイプ選択UI実装
- ✅ STEP名の多言語編集UI実装
- ✅ GROUP名の多言語編集UI実装
- ✅ 単一式フォームの初期化処理
- ✅ 公開フォーム表示でのSTEP/GROUP名表示

#### データ保存
- ✅ `flattenStepGroupStructure()`関数の実装
- ✅ `handleSave()`関数の修正（STEP/GROUP構造を含むフィールド配列を送信）
- ✅ バリデーション強化（STEP/GROUP名の必須チェック）

#### 翻訳対応
- ✅ `PreferencesContext.tsx`に翻訳キーを追加:
  - `form_item_select_type`: "フォームタイプを選択してください" / "Please select form type"
  - `form_item_step_form`: "STEP式フォーム" / "STEP Form"
  - `form_item_single_form`: "単一式フォーム" / "Single Form"
  - `form_item_step_name`: "STEP名" / "Step Name"
  - `form_item_group_name`: "GROUP名" / "Group Name"
  - `form_item_enter_step_name`: "STEP名を入力" / "Enter step name"
  - `form_item_enter_group_name`: "GROUP名を入力" / "Enter group name"
  - `form_item_step_name_required`: "STEP名を入力してください（少なくとも1言語）" / "Please enter step name (at least one language)"
  - `form_item_group_name_required`: "GROUP名を入力してください（少なくとも1言語）" / "Please enter group name (at least one language)"
  - `form_item_validation_failed`: "バリデーションエラーがあります。入力内容を確認してください。" / "Validation errors found. Please check your input."

---

## 後方互換性

### 既存データの対応

**既存のフォーム項目データ**:
- `step_key`が`NULL`、`group_key`が`"default"`の場合、既存のフロントエンド実装と同様に処理
- `step_group_structure`が`NULL`の場合、以下のデフォルト構造を生成:
  ```json
  {
    "is_step_form": false,
    "steps": null,
    "groups": [
      {
        "group_key": "default",
        "group_name_i18n": {
          "ja": "デフォルトグループ",
          "en": "Default Group"
        },
        "sort_order": 0
      }
    ]
  }
  ```

**マイグレーション時のデータ移行**:
- 既存の`form_fields`データに対して、`step_key = NULL`, `group_key = "default"`を設定
- 既存の`forms`データに対して、上記のデフォルト`step_group_structure`を設定

---

## 注意事項

### バリデーション

1. **STEP式フォームの場合**:
   - `step_key`は必須（`null`不可）
   - `step_name_i18n`は必須（少なくとも1言語の名前が必要）

2. **単一式フォームの場合**:
   - `step_key`は`null`または省略可能
   - `step_name_i18n`は`null`または省略可能

3. **GROUP（共通）**:
   - `group_key`は必須
   - `group_name_i18n`は必須（少なくとも1言語の名前が必要）

### データ整合性

1. **STEP/GROUP構造の整合性**:
   - `form_fields.step_key`と`forms.step_group_structure.steps[].step_key`が一致すること
   - `form_fields.group_key`と`forms.step_group_structure`内の対応するGROUPの`group_key`が一致すること

2. **冗長性の排除**:
   - `step_name_i18n`と`group_name_i18n`は`forms.step_group_structure`にのみ保存
   - `form_fields`テーブルには`step_key`と`group_key`のみ保存（名前情報は保存しない）

### 公開フォーム表示

1. **STEP/GROUP名の表示**:
   - 公開フォーム表示時は、`forms.step_group_structure`からSTEP/GROUP名を取得
   - ロケールに応じた多言語名を表示
   - 単一式フォームの場合、STEP名は表示しない

2. **STEP遷移機能**:
   - STEP式フォームの場合、既存の`step_transition_rule`評価機能を利用
   - 単一式フォームの場合、STEP遷移は発生しない

---

## 参照

- `app/Models/Form.php` - フォームモデル
- `app/Models/FormField.php` - フォーム項目モデル
- `app/Http/Controllers/Api/V1/FormsFieldsController.php` - フォーム項目管理API
- `src/pages/forms/FormItemPage.tsx` - フォーム項目設定画面
- `src/ui/PreferencesContext.tsx` - 翻訳コンテキスト
- `SUPP-I18N-001-spec.md` - 多言語対応機能仕様（参考）
