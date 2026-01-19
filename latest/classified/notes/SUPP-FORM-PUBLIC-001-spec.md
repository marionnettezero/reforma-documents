# SUPP-FORM-PUBLIC-001: フォーム公開状態管理の簡素化 実装仕様

**作成日**: 2026-01-20  
**最終更新日**: 2026-01-20  
**バージョン**: v1.0.0

---

## 概要

フォームの公開状態管理において、`status`、`is_public`フラグ、`public_period`の3種類の管理方法が重複していたため、`is_public`フラグを削除し、`status = 'published'` + `public_period`のみで公開状態を管理するように簡素化する。

**変更前の公開判定ロジック**:
- `status = 'published'` AND `is_public = true` AND 公開期間内

**変更後の公開判定ロジック**:
- `status = 'published'` AND 公開期間内

---

## バックエンド実装

### 1. データベースマイグレーション

#### 1.1. is_publicカラム削除マイグレーション

**ファイル**: `database/migrations/2026_01_20_100000_remove_is_public_from_forms_table.php`

**実装内容**:
```php
public function up(): void
{
    Schema::table('forms', function (Blueprint $table) {
        // インデックスを削除（status, is_publicの複合インデックス）
        $table->dropIndex(['status', 'is_public']);
        
        // is_publicカラムを削除
        $table->dropColumn('is_public');
        
        // statusのみのインデックスを追加
        $table->index(['status']);
    });
}

public function down(): void
{
    Schema::table('forms', function (Blueprint $table) {
        // statusのみのインデックスを削除
        $table->dropIndex(['status']);
        
        // is_publicカラムを復元
        $table->boolean('is_public')->default(false)->after('status')->comment('公開フラグ');
        
        // 複合インデックスを復元
        $table->index(['status', 'is_public']);
    });
}
```

**変更内容**:
- 複合インデックス`['status', 'is_public']`を削除
- `is_public`カラムを削除
- `['status']`のみのインデックスを追加（パフォーマンス向上のため）

### 2. Formモデルの修正

#### 2.1. fillableとcastsからis_publicを削除

**ファイル**: `app/Models/Form.php`

**変更内容**:
```php
// 変更前
protected $fillable = [
    'code',
    'status',
    'is_public',  // ← 削除
    'public_period_start',
    // ...
];

protected $casts = [
    'is_public' => 'boolean',  // ← 削除
    'attachment_enabled' => 'boolean',
    // ...
];

// 変更後
protected $fillable = [
    'code',
    'status',
    'public_period_start',
    // ...
];

protected $casts = [
    'attachment_enabled' => 'boolean',
    // ...
];
```

**動作**:
- `is_public`が`$fillable`から削除されるため、一括代入で設定不可
- `is_public`が`$casts`から削除されるため、自動型変換が行われない

### 3. PublicFormsControllerの修正

#### 3.1. 公開フォーム取得時のis_public条件を削除

**ファイル**: `app/Http/Controllers/Api/V1/PublicFormsController.php`

**変更箇所**: 
- `show()`メソッド（60-65行目）
- `submit()`メソッド（141-146行目）
- `ack()`メソッド（313-317行目）

**変更内容**:
```php
// 変更前
$form = Form::where('code', $formKey)
    ->where('is_public', true)  // ← 削除
    ->where('status', 'published')
    ->first();

// 変更後
$form = Form::where('code', $formKey)
    ->where('status', 'published')
    ->first();
```

**動作**:
- 公開フォームの取得条件が`status = 'published'`のみとなる
- 公開期間チェックは既存のロジックで継続して実行される

### 4. FormsControllerの修正

#### 4.1. バリデーションからis_publicを削除

**ファイル**: `app/Http/Controllers/Api/V1/FormsController.php`

**変更箇所**: 
- `store()`メソッド（148行目）
- `update()`メソッド（298行目）

**変更内容**:
```php
// 変更前
$validated = $request->validate([
    'code' => ['required', 'string', 'max:255', 'unique:forms,code', 'regex:/^[a-zA-Z0-9_]+$/'],
    'is_public' => ['nullable', 'boolean'],  // ← 削除
    'translations' => ['nullable', 'array'],
    // ...
]);

// 変更後
$validated = $request->validate([
    'code' => ['required', 'string', 'max:255', 'unique:forms,code', 'regex:/^[a-zA-Z0-9_]+$/'],
    'translations' => ['nullable', 'array'],
    // ...
]);
```

#### 4.2. フォーム作成時のis_public設定を削除

**変更箇所**: `store()`メソッド（168-173行目）

**変更内容**:
```php
// 変更前
$form = Form::create([
    'code' => $validated['code'],
    'status' => 'draft',
    'is_public' => $validated['is_public'] ?? false,  // ← 削除
    'created_by' => $user->id,
]);

// 変更後
$form = Form::create([
    'code' => $validated['code'],
    'status' => 'draft',
    'created_by' => $user->id,
]);
```

#### 4.3. フォーム更新時のis_public設定を削除

**変更箇所**: `update()`メソッド（330-333行目）

**変更内容**:
```php
// 変更前
if (isset($validated['is_public'])) {
    $form->is_public = $validated['is_public'];
}

// 変更後
// 削除（is_publicの設定処理を削除）
```

#### 4.4. レスポンスからis_publicを削除

**変更箇所**: 
- `index()`メソッド（101行目）
- `store()`メソッド（200行目）
- `show()`メソッド（237行目）
- `update()`メソッド（422行目）

**変更内容**:
```php
// 変更前
return [
    'id' => $form->id,
    'code' => $form->code,
    'status' => $form->status,
    'is_public' => $form->is_public,  // ← 削除
    'attachment_enabled' => $form->attachment_enabled,
    // ...
];

// 変更後
return [
    'id' => $form->id,
    'code' => $form->code,
    'status' => $form->status,
    'attachment_enabled' => $form->attachment_enabled,
    // ...
];
```

---

## フロントエンド実装

### 5. FormEditPageの修正

#### 5.1. Form型定義からis_publicを削除

**ファイル**: `src/pages/forms/FormEditPage.tsx`

**変更内容**:
```typescript
// 変更前
type Form = {
  id: number;
  code: string;
  status: FormStatus;
  is_public: boolean;  // ← 削除
  public_period_start: string | null;
  // ...
};

// 変更後
type Form = {
  id: number;
  code: string;
  status: FormStatus;
  public_period_start: string | null;
  // ...
};
```

#### 5.2. 状態変数からformIsPublicを削除

**変更内容**:
```typescript
// 変更前
const [formCode, setFormCode] = useState("");
const [formStatus, setFormStatus] = useState<FormStatus>("draft");
const [formIsPublic, setFormIsPublic] = useState(false);  // ← 削除
const [formPublicPeriodStart, setFormPublicPeriodStart] = useState<string>("");

// 変更後
const [formCode, setFormCode] = useState("");
const [formStatus, setFormStatus] = useState<FormStatus>("draft");
const [formPublicPeriodStart, setFormPublicPeriodStart] = useState<string>("");
```

#### 5.3. フォーム取得時のis_public処理を削除

**変更箇所**: フォームデータ取得時の初期化処理（277-280行目、1002行目）

**変更内容**:
```typescript
// 変更前
setFormCode(formData.code);
setFormStatus(formData.status);
setFormIsPublic(formData.is_public);  // ← 削除
setFormPublicPeriodStart(formData.public_period_start ? new Date(formData.public_period_start).toISOString().slice(0, 16) : "");

// 変更後
setFormCode(formData.code);
setFormStatus(formData.status);
setFormPublicPeriodStart(formData.public_period_start ? new Date(formData.public_period_start).toISOString().slice(0, 16) : "");
```

#### 5.4. フォーム保存時のis_public送信を削除

**変更箇所**: フォーム保存処理（392-395行目）

**変更内容**:
```typescript
// 変更前
const req: any = {
  status: formStatus,
  is_public: formIsPublic,  // ← 削除
  public_period_start: formPublicPeriodStart ? new Date(formPublicPeriodStart).toISOString() : null,
  // ...
};

// 変更後
const req: any = {
  status: formStatus,
  public_period_start: formPublicPeriodStart ? new Date(formPublicPeriodStart).toISOString() : null,
  // ...
};
```

#### 5.5. UIから公開チェックボックスを削除

**変更箇所**: フォーム編集UI（570-580行目）

**変更内容**:
```typescript
// 変更前
<div>
  <label className="flex items-center gap-2">
    <input
      type="checkbox"
      checked={formIsPublic}
      onChange={(e) => setFormIsPublic(e.target.checked)}
    />
    <span className="text-sm">公開</span>
  </label>
</div>
</div>
<div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">

// 変更後
</div>
{/* 公開期間フィールド（status = 'published'の時のみ表示） */}
{formStatus === 'published' && (
<div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
```

**動作**:
- 公開チェックボックスを削除
- 公開期間フィールドは`status = 'published'`の時のみ表示されるように変更

### 6. FormListPageの修正

#### 6.1. Form型定義からis_publicを削除

**ファイル**: `src/pages/forms/FormListPage.tsx`

**変更内容**:
```typescript
// 変更前
type Form = {
  id: number;
  code: string;
  status: FormStatus;
  is_public: boolean;  // ← 削除
  public_period_start: string | null;
  // ...
};

// 変更後
type Form = {
  id: number;
  code: string;
  status: FormStatus;
  public_period_start: string | null;
  // ...
};
```

#### 6.2. 詳細モーダルの公開表示をstatusで判断

**変更箇所**: フォーム詳細モーダル（574-580行目）

**変更内容**:
```typescript
// 変更前
<div className="flex items-start gap-4">
  <div className="w-32 shrink-0 text-sm font-bold">{t("form_detail_is_public") || "公開"}</div>
  <div className="text-sm flex-1">
    <Badge variant={selectedForm.is_public ? "success" : "neutral"}>
      {selectedForm.is_public ? (locale === "ja" ? "公開" : "Public") : (locale === "ja" ? "非公開" : "Private")}
    </Badge>
  </div>
</div>

// 変更後
<div className="flex items-start gap-4">
  <div className="w-32 shrink-0 text-sm font-bold">{t("form_detail_is_public") || "公開状態"}</div>
  <div className="text-sm flex-1">
    <Badge variant={selectedForm.status === "published" ? "success" : "neutral"}>
      {selectedForm.status === "published" ? (locale === "ja" ? "公開中" : "Published") : (locale === "ja" ? "非公開" : "Not Published")}
    </Badge>
  </div>
</div>
```

**動作**:
- `is_public`フラグではなく`status = 'published'`で公開状態を判断
- ラベルを「公開」から「公開状態」に変更

### 7. FormPreviewPageの修正

#### 7.1. Form型定義からis_publicを削除

**ファイル**: `src/pages/forms/FormPreviewPage.tsx`

**変更内容**:
```typescript
// 変更前
type Form = {
  id: number;
  code: string;
  status: string;
  is_public: boolean;  // ← 削除
  theme_id?: number;
  // ...
};

// 変更後
type Form = {
  id: number;
  code: string;
  status: string;
  theme_id?: number;
  // ...
};
```

#### 7.2. Badge表示をstatusで判断

**変更箇所**: プレビュー画面のBadge表示（500-502行目）

**変更内容**:
```typescript
// 変更前
<Badge>code: {form.code}</Badge>
<Badge>status: {form.status}</Badge>
{form.is_public && <Badge variant="success">公開中</Badge>}

// 変更後
<Badge>code: {form.code}</Badge>
<Badge>status: {form.status}</Badge>
{form.status === "published" && <Badge variant="success">公開中</Badge>}
```

**動作**:
- `is_public`フラグではなく`status = 'published'`で「公開中」Badgeを表示

---

## データモデル

### formsテーブル

**変更前の構造**:
- `id`: bigint
- `code`: string (unique)
- `status`: string (draft/published/closed)
- `is_public`: boolean (default: false) ← **削除**
- `public_period_start`: timestamp (nullable)
- `public_period_end`: timestamp (nullable)
- `answer_period_start`: timestamp (nullable)
- `answer_period_end`: timestamp (nullable)
- `timestamps`
- `soft_deletes`
- インデックス: `['status', 'is_public']` ← **削除**

**変更後の構造**:
- `id`: bigint
- `code`: string (unique)
- `status`: string (draft/published/closed)
- `public_period_start`: timestamp (nullable)
- `public_period_end`: timestamp (nullable)
- `answer_period_start`: timestamp (nullable)
- `answer_period_end`: timestamp (nullable)
- `timestamps`
- `soft_deletes`
- インデックス: `['status']` ← **追加**

**公開判定ロジック**:
```php
// 変更前
$form->status === 'published' && $form->is_public === true && 公開期間内

// 変更後
$form->status === 'published' && 公開期間内
```

---

## API仕様

### 変更点

#### GET /v1/forms

**レスポンス変更**:
```json
// 変更前
{
  "success": true,
  "data": {
    "forms": [
      {
        "id": 1,
        "code": "form001",
        "status": "published",
        "is_public": true,  // ← 削除
        "public_period_start": "2026-01-01T00:00:00Z",
        // ...
      }
    ]
  }
}

// 変更後
{
  "success": true,
  "data": {
    "forms": [
      {
        "id": 1,
        "code": "form001",
        "status": "published",
        "public_period_start": "2026-01-01T00:00:00Z",
        // ...
      }
    ]
  }
}
```

#### GET /v1/forms/{id}

**レスポンス変更**: 同様に`is_public`フィールドを削除

#### POST /v1/forms

**リクエスト変更**:
```json
// 変更前
{
  "code": "form001",
  "is_public": true,  // ← 削除（バリデーションエラー）
  "translations": [...]
}

// 変更後
{
  "code": "form001",
  "translations": [...]
}
```

#### PUT /v1/forms/{id}

**リクエスト変更**: 同様に`is_public`フィールドを削除

#### GET /v1/public/forms/{form_key}

**公開判定ロジック変更**:
- 変更前: `status = 'published'` AND `is_public = true` AND 公開期間内
- 変更後: `status = 'published'` AND 公開期間内

---

## 実装タスク

### バックエンド

#### データベース
- ✅ `is_public`カラムを削除するマイグレーションを作成
- ✅ 複合インデックス`['status', 'is_public']`を削除
- ✅ 単一インデックス`['status']`を追加

#### モデル
- ✅ Formモデルの`$fillable`から`'is_public'`を削除
- ✅ Formモデルの`$casts`から`'is_public' => 'boolean'`を削除

#### コントローラー
- ✅ PublicFormsControllerの`show()`メソッドから`is_public`条件を削除
- ✅ PublicFormsControllerの`submit()`メソッドから`is_public`条件を削除
- ✅ PublicFormsControllerの`ack()`メソッドから`is_public`条件を削除
- ✅ FormsControllerの`store()`メソッドから`is_public`バリデーションを削除
- ✅ FormsControllerの`update()`メソッドから`is_public`バリデーションを削除
- ✅ FormsControllerの`store()`メソッドから`is_public`設定を削除
- ✅ FormsControllerの`update()`メソッドから`is_public`設定を削除
- ✅ FormsControllerの`index()`メソッドからレスポンスの`is_public`を削除
- ✅ FormsControllerの`store()`メソッドからレスポンスの`is_public`を削除
- ✅ FormsControllerの`show()`メソッドからレスポンスの`is_public`を削除
- ✅ FormsControllerの`update()`メソッドからレスポンスの`is_public`を削除

### フロントエンド

#### FormEditPage
- ✅ Form型定義から`is_public: boolean`を削除
- ✅ `formIsPublic`状態変数を削除
- ✅ フォーム取得時の`setFormIsPublic`を削除
- ✅ フォーム保存時の`is_public`送信を削除
- ✅ UIから公開チェックボックスを削除
- ✅ 公開期間フィールドを`status = 'published'`の時のみ表示するように変更

#### FormListPage
- ✅ Form型定義から`is_public: boolean`を削除
- ✅ 詳細モーダルの「公開」表示を`status = 'published'`で判断するように変更

#### FormPreviewPage
- ✅ Form型定義から`is_public: boolean`を削除
- ✅ Badge表示を`status = 'published'`で判断するように変更

---

## 実装済み機能

### 公開状態管理の簡素化（実装済み）

**変更内容**:
- `is_public`フラグを削除し、`status = 'published'` + 公開期間のみで公開状態を管理
- データベース、モデル、コントローラー、フロントエンドのすべての層で`is_public`を削除
- 公開判定ロジックを簡素化

**実装日**: 2026-01-20

---

## 注意事項

### データ移行について

**注意**: 本変更ではデータ移行は不要です。`is_public`カラムの削除のみを行います。

**理由**:
- `is_public = true`のフォームは`status = 'published'`に設定されている想定
- `is_public = false`のフォームは`status = 'draft'`または`status = 'closed'`に設定されている想定
- 既存の公開判定ロジック（`status = 'published'` AND `is_public = true`）は、変更後（`status = 'published'`）と実質的に同じ動作となる

### 後方互換性

**破壊的変更**: 本変更は破壊的変更です。

**影響範囲**:
- APIレスポンスから`is_public`フィールドが削除される
- APIリクエストで`is_public`を送信するとバリデーションエラーとなる
- フロントエンドで`is_public`を参照している箇所はすべて修正が必要

**対応**:
- フロントエンドとバックエンドを同時にデプロイする必要がある
- 既存のAPIクライアントが`is_public`を参照している場合は修正が必要

### 公開判定ロジック

**変更前**:
```php
$form->status === 'published' && $form->is_public === true && 公開期間内
```

**変更後**:
```php
$form->status === 'published' && 公開期間内
```

**注意点**:
- `status = 'published'`であっても、公開期間外の場合は公開されない
- `status = 'draft'`または`status = 'closed'`の場合は、公開期間内であっても公開されない

---

## 参照

- `database/migrations/2026_01_20_100000_remove_is_public_from_forms_table.php` - マイグレーションファイル
- `app/Models/Form.php` - Formモデル
- `app/Http/Controllers/Api/V1/PublicFormsController.php` - 公開フォームAPI
- `app/Http/Controllers/Api/V1/FormsController.php` - フォーム管理API
- `src/pages/forms/FormEditPage.tsx` - フォーム編集画面
- `src/pages/forms/FormListPage.tsx` - フォーム一覧画面
- `src/pages/forms/FormPreviewPage.tsx` - フォームプレビュー画面
