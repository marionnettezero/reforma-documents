# SUPP-I18N-001: 多言語対応機能 実装仕様

**作成日**: 2026-01-20  
**最終更新日**: 2026-01-20  
**バージョン**: v1.1.0

---

## 概要

フォームの基本情報（タイトル、説明、メールテンプレート等）およびフォーム項目（フィールドラベル、選択肢ラベル）の多言語対応を実装。言語マスタをSettingsで管理し、動的に言語タブを生成して編集可能にする。

---

## バックエンド実装

### 1. 言語マスタ管理（Settings）

#### 1.1. Settingモデルの拡張

**ファイル**: `app/Models/Setting.php`

**追加メソッド**:
```php
/**
 * サポートされている言語リストを取得
 * 
 * @return array 言語コードの配列（例: ['ja', 'en']）
 */
public static function getSupportedLanguages(): array
{
    $languages = self::get('supported_languages', ['ja', 'en']);
    
    // 配列でない場合はデフォルト値を返す
    if (!is_array($languages)) {
        return ['ja', 'en'];
    }
    
    // 空配列の場合はデフォルト値を返す
    if (empty($languages)) {
        return ['ja', 'en'];
    }
    
    return $languages;
}
```

**動作**:
- DBに`supported_languages`が存在する場合はその値を返す
- 存在しない場合はデフォルト値`['ja', 'en']`を返す
- 型チェックと空配列チェックを実装

#### 1.2. 言語マスタ取得API

**エンドポイント**: `GET /v1/system/supported-languages`

**権限**: 認証済みユーザーなら誰でもアクセス可能（権限不要）

**コントローラー**: `app/Http/Controllers/Api/V1/System/SettingsController.php`

**追加メソッド**:
```php
/**
 * サポートされている言語リストを取得する
 * --------------------------------------------------------
 * フォーム作成・編集時に利用可能な言語を取得
 * 権限不要で取得可能
 *
 * @param Request $request
 * @return JsonResponse
 */
public function supportedLanguages(Request $request): JsonResponse
{
    $languages = Setting::getSupportedLanguages();
    
    return ApiResponse::success($request, [
        'languages' => $languages,
    ], null);
}
```

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "languages": ["ja", "en"]
  }
}
```

**ルーティング**: `routes/api.php`
```php
// サポートされている言語リスト取得（認証済みユーザーなら誰でもアクセス可能）
Route::get('/system/supported-languages', [\App\Http\Controllers\Api\V1\System\SettingsController::class, 'supportedLanguages']);
```

### 2. バリデーションルールの動的生成

#### 2.1. FormsControllerの修正

**ファイル**: `app/Http/Controllers/Api/V1/FormsController.php`

**変更箇所**:
- `store()`メソッド（151行目）
- `update()`メソッド（298行目）

**変更内容**:
```php
// 変更前
'translations.*.locale' => ['required_with:translations', 'string', 'in:ja,en'],

// 変更後
$supportedLanguages = \App\Models\Setting::getSupportedLanguages();
'translations.*.locale' => ['required_with:translations', 'string', 'in:' . implode(',', $supportedLanguages)],
```

#### 2.2. PublicFormsControllerの修正

**ファイル**: `app/Http/Controllers/Api/V1/PublicFormsController.php`

**変更箇所**: `submit()`メソッド（136行目）

**変更内容**:
```php
// 変更前
'locale' => ['nullable', 'string', 'in:ja,en'],

// 変更後
$supportedLanguages = \App\Models\Setting::getSupportedLanguages();
'locale' => ['nullable', 'string', 'in:' . implode(',', $supportedLanguages)],
```

#### 2.3. ApiResponseのロケール取得ロジック修正

**ファイル**: `app/Support/ApiResponse.php`

**変更箇所**: `getLocale()`メソッド（98-122行目）

**変更内容**:
```php
// 変更前
if ($localeParam && in_array($localeParam, ['ja', 'en'], true)) {
    return $localeParam;
}
// ...
if (in_array($langCode, ['ja', 'en'], true)) {
    return $langCode;
}
return 'ja';

// 変更後
$supportedLanguages = \App\Models\Setting::getSupportedLanguages();
$defaultLocale = $supportedLanguages[0] ?? 'ja';

if ($localeParam && in_array($localeParam, $supportedLanguages, true)) {
    return $localeParam;
}
// ...
if (in_array($langCode, $supportedLanguages, true)) {
    return $langCode;
}
return $defaultLocale;
```

---

## フロントエンド実装

### 3. フォーム基本情報の多言語対応（FormEditPage）

#### 3.1. 言語マスタ取得

**ファイル**: `src/pages/forms/FormEditPage.tsx`

**実装内容**:
- `GET /v1/system/supported-languages`から利用可能な言語を取得
- `useEffect`で初回レンダリング時に取得

**State追加**:
```typescript
const [supportedLanguages, setSupportedLanguages] = useState<string[]>(['ja', 'en']);
const [addedLanguages, setAddedLanguages] = useState<string[]>(['ja']); // 追加された言語のリスト
const [activeLanguageTab, setActiveLanguageTab] = useState<string | null>('ja'); // 現在選択中のタブ
const [translations, setTranslations] = useState<Record<string, { title: string; description: string }>>({
  ja: { title: '', description: '' },
});
```

#### 3.2. 翻訳データ構造の変更

**変更前**:
```typescript
const [translationJa, setTranslationJa] = useState({ title: "", description: "" });
const [translationEn, setTranslationEn] = useState({ title: "", description: "" });
```

**変更後**:
```typescript
const [translations, setTranslations] = useState<Record<string, { title: string; description: string }>>({
  ja: { title: '', description: '' },
});
```

#### 3.3. 言語タブUIコンポーネント

**実装内容**:
- タブヘッダー: 追加された言語ごとにタブボタンを表示
- タブ削除ボタン（×）: 各タブに削除ボタンを追加（最低1つは残す）
- タブコンテンツ: 選択中の言語の入力欄を表示
- 言語追加ボタン: ドロップダウンから未追加の言語を選択

**UI構造**:
```
[翻訳情報]
┌─────────────────────────────────────────┐
│ [日本語 (ja)] [English (en)] [+ 言語追加] │ ← タブヘッダー
├─────────────────────────────────────────┤
│ タイトル: [____________] *              │
│ 説明:     [____________]                 │ ← タブコンテンツ
└─────────────────────────────────────────┘
```

#### 3.4. 保存処理の修正

**変更内容**:
```typescript
// 変更前
const translationsData: Array<{ locale: string; title: string; description?: string | null }> = [];
if (translationJa.title.trim()) {
  translationsData.push({
    locale: "ja",
    title: translationJa.title.trim(),
    description: translationJa.description.trim() || null,
  });
}
if (translationEn.title.trim()) {
  translationsData.push({
    locale: "en",
    title: translationEn.title.trim(),
    description: translationEn.description.trim() || null,
  });
}

// 変更後
const translationsData: Array<{ locale: string; title: string; description?: string | null }> = [];
Object.entries(translations).forEach(([locale, data]) => {
  if (data.title.trim()) {
    translationsData.push({
      locale,
      title: data.title.trim(),
      description: data.description.trim() || null,
    });
  }
});
```

#### 3.5. データ取得時の初期化処理

**実装内容**:
- バックエンドから取得した`translations`配列を`translations`オブジェクトに変換
- 既存の翻訳がある言語を`addedLanguages`に追加
- 最初の言語タブを自動選択

---

### 4. フォーム項目の多言語対応（FormItemPage）

#### 4.1. 言語マスタとフォーム翻訳情報の取得

**ファイル**: `src/pages/forms/FormItemPage.tsx`

**実装内容**:
- `GET /v1/system/supported-languages`から利用可能な言語を取得
- `GET /v1/forms/{form_id}`からフォームの翻訳情報を取得し、追加された言語を特定

**State追加**:
```typescript
const [supportedLanguages, setSupportedLanguages] = useState<string[]>(['ja', 'en']);
const [formAddedLanguages, setFormAddedLanguages] = useState<string[]>(['ja']); // フォームで追加された言語
const [activeLanguageTab, setActiveLanguageTab] = useState<string | null>('ja'); // 現在選択中のタブ
const [editFieldLabel, setEditFieldLabel] = useState<Record<string, string>>({}); // フィールドラベルの多言語データ {locale: label}
const [editOptionsLabels, setEditOptionsLabels] = useState<Record<string, Record<string, string>>>({}); // 選択肢ラベルの多言語データ {optionValue: {locale: label}}
```

#### 4.2. フィールド編集開始時の多言語データ初期化

**実装内容**:
- `startEditField()`関数内で、`field.options_json`から多言語データを抽出
- フィールドラベル: `options_json.label`と`options_json.labels[locale]`を取得
- 選択肢ラベル: `options_json.options[].label`と`options_json.options[].labels[locale]`を取得

#### 4.3. 保存処理の多言語データ統合

**実装内容**:
- `saveField()`関数内で、多言語データを`options_json`に統合
- フィールドラベル: `options_json.label`（デフォルト）と`options_json.labels[locale]`（多言語）を設定
- 選択肢ラベル: `options_json.options[].label`（デフォルト）と`options_json.options[].labels[locale]`（多言語）を設定

**options_json構造**:
```json
{
  "label": "フィールドラベル（デフォルト）",
  "labels": {
    "ja": "フィールドラベル（日本語）",
    "en": "Field Label (English)"
  },
  "options": [
    {
      "value": "option1",
      "label": "選択肢1（デフォルト）",
      "labels": {
        "ja": "選択肢1（日本語）",
        "en": "Option 1 (English)"
      }
    }
  ]
}
```

#### 4.4. フィールド編集UIの多言語タブ化

**実装内容**:
- `FieldEditForm`コンポーネントに多言語対応のpropsを追加
- フィールドラベル編集部分をタブ化
- 選択肢ラベル編集部分をタブ化（選択肢ごとに各言語のラベルを編集）

**UI構造**:
```
[フィールドラベル]
┌─────────────────────────────────────────┐
│ [日本語 (ja)] [English (en)]            │ ← タブヘッダー
├─────────────────────────────────────────┤
│ ラベル: [____________]                  │ ← タブコンテンツ
└─────────────────────────────────────────┘

[選択肢ラベル]
┌─────────────────────────────────────────┐
│ [日本語 (ja)] [English (en)]            │ ← タブヘッダー
├─────────────────────────────────────────┤
│ option1: [____________]                 │
│ option2: [____________]                   │ ← タブコンテンツ（選択肢ごと）
└─────────────────────────────────────────┘
```

---

## データモデル

### form_translationsテーブル（拡張予定）

**現在の構造**:
- `id`: bigint
- `form_id`: bigint
- `locale`: string (ja/en)
- `title`: string
- `description`: text (nullable)
- `notification_user_email_template`: text (nullable) - ユーザー向けメールテンプレート（多言語）※実装済み
- `notification_user_email_subject`: string (nullable) - ユーザー向けメール件名（多言語）※実装済み
- `notification_admin_email_template`: text (nullable) - 管理者向けメールテンプレート（多言語）※実装済み
- `notification_admin_email_subject`: string (nullable) - 管理者向けメール件名（多言語）※実装済み
- `timestamps`

**実装状況**: メールテンプレート関連カラムは2026-01-20に実装済み。マイグレーション: `2026_01_19_074919_add_email_template_fields_to_form_translations_table.php`

### form_fieldsテーブルのoptions_json構造

**多言語対応後の構造**:
```json
{
  "label": "フィールドラベル（デフォルト、後方互換性のため保持）",
  "labels": {
    "ja": "フィールドラベル（日本語）",
    "en": "Field Label (English)"
  },
  "options": [
    {
      "value": "option1",
      "label": "選択肢ラベル（デフォルト、後方互換性のため保持）",
      "labels": {
        "ja": "選択肢ラベル（日本語）",
        "en": "Option Label (English)"
      }
    }
  ]
}
```

**後方互換性**:
- `label`フィールドは既存データとの互換性のため保持
- `labels[locale]`が存在する場合は優先的に使用
- `labels[locale]`が存在しない場合は`label`をフォールバックとして使用

---

## API仕様

### GET /v1/system/supported-languages

**権限**: 認証済みユーザーなら誰でもアクセス可能

**説明**: システムでサポートされている言語リストを取得

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "languages": ["ja", "en"]
  }
}
```

**デフォルト値**: DBに値がない場合は`["ja", "en"]`を返す

---

## 実装タスク

### バックエンド

#### 言語マスタ管理
- ✅ Settingモデルに`getSupportedLanguages()`メソッドを追加
- ✅ `GET /v1/system/supported-languages` APIエンドポイントを作成
- ✅ ルーティング追加（認証済みユーザーなら誰でもアクセス可能）

#### バリデーションルールの動的生成
- ✅ FormsControllerの`store()`メソッドを修正
- ✅ FormsControllerの`update()`メソッドを修正
- ✅ PublicFormsControllerの`submit()`メソッドを修正
- ✅ ApiResponse::getLocale()を言語マスタ対応に修正

### フロントエンド

#### フォーム基本情報の多言語対応
- ✅ FormEditPage: 言語マスタ取得API呼び出しを実装
- ✅ FormEditPage: 翻訳データ構造を動的構造に変更
- ✅ FormEditPage: 言語タブUIコンポーネントを実装
- ✅ FormEditPage: 言語追加機能を実装
- ✅ FormEditPage: 保存処理を動的構造に対応
- ✅ FormEditPage: データ取得時の初期化処理を実装

#### フォーム項目の多言語対応
- ✅ FormItemPage: 言語マスタ取得API呼び出しを実装
- ✅ FormItemPage: フォーム翻訳情報取得を実装
- ✅ FormItemPage: フィールド編集開始時の多言語データ初期化を実装
- ✅ FormItemPage: 保存処理の多言語データ統合を実装
- ✅ FormItemPage: フィールド編集UIの多言語タブ化を実装

#### メールテンプレート多言語対応
- ✅ form_translationsテーブルにメールテンプレート関連カラムを追加（マイグレーション作成）
- ✅ FormTranslationモデルのfillableにメールテンプレート関連フィールドを追加
- ✅ FormsControllerのstore()とupdate()メソッドでメールテンプレート関連フィールドのバリデーションを追加
- ✅ FormsControllerのshow()メソッドでレスポンスにメールテンプレート関連フィールドを含める
- ✅ FormsControllerのstore()とupdate()メソッドでform_translationsテーブルにメールテンプレート関連データを保存
- ✅ SendFormSubmissionNotificationJobでform_translationsテーブルからメールテンプレートを取得するロジックに変更
- ✅ FormEditPageの翻訳情報タブにメールテンプレート関連の入力欄を追加
- ✅ FormEditPageの保存処理とデータ取得時にメールテンプレート関連データを処理
- ✅ formsテーブルからメールテンプレート関連カラムを削除（マイグレーション作成）
- ✅ Formモデルのfillableからメールテンプレート関連フィールドを削除

#### フォームコードのバリデーション
- ✅ FormsControllerのstore()メソッドでフォームコードのバリデーションルールに英数字とアンダースコアのみを許可する正規表現を追加
- ✅ FormsControllerのupdate()メソッドでフォームコードのバリデーションルールに英数字とアンダースコアのみを許可する正規表現を追加
- ✅ FormEditPageのフォームコード入力欄にリアルタイムバリデーションを追加
- ✅ FormEditPageのフォームコード入力欄のエラーメッセージ表示を追加

---

## 実装済み機能

### form_translationsテーブルの拡張（実装済み）

**追加済みカラム**:
- `notification_user_email_template`: text (nullable) - ユーザー向けメールテンプレート（多言語）
- `notification_user_email_subject`: string (nullable) - ユーザー向けメール件名（多言語）
- `notification_admin_email_template`: text (nullable) - 管理者向けメールテンプレート（多言語）
- `notification_admin_email_subject`: string (nullable) - 管理者向けメール件名（多言語）

**実装内容**:
- フォームの基本情報に関連する多言語データを`form_translations`テーブルに格納
- フォーム項目の多言語データは`form_fields.options_json`内の`labels[locale]`構造で管理（既存実装）
- メール送信時は`form_translations`テーブルからロケールに応じたテンプレートを取得（デフォルトは'ja'）

---

## 注意事項（対応済み）

### フォームコードのバリデーション（実装済み）

**実装内容**: 
- ✅ バックエンド: FormsControllerの`store()`と`update()`メソッドで正規表現バリデーション（`regex:/^[a-zA-Z0-9_]+$/`）を追加
- ✅ フロントエンド: FormEditPageのフォームコード入力欄にリアルタイムバリデーションを追加（英数字とアンダースコア以外の文字を入力不可）
- ✅ フロントエンド: 不正な文字が入力された場合にエラーメッセージを表示

**実装日**: 2026-01-20

---

## 参照

- `app/Models/Setting.php` - 言語マスタ取得メソッド
- `app/Http/Controllers/Api/V1/System/SettingsController.php` - 言語マスタ取得API
- `app/Http/Controllers/Api/V1/FormsController.php` - フォーム管理API（バリデーション修正）
- `app/Http/Controllers/Api/V1/PublicFormsController.php` - 公開フォームAPI（バリデーション修正）
- `app/Support/ApiResponse.php` - ロケール取得ロジック
- `src/pages/forms/FormEditPage.tsx` - フォーム基本情報の多言語対応UI
- `src/pages/forms/FormItemPage.tsx` - フォーム項目の多言語対応UI
