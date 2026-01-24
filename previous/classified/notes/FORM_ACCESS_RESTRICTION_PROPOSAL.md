# フォームアクセス制限機能の実装提案

## 概要
アカウントに「このフォームとこのフォームのみ操作できる」という制限を追加する機能の実装提案です。

## 現状確認

### 既存の機能
- **ロールベースの権限**: `system_admin`, `form_admin`, `operator`, `viewer`
- **フォーム作成数制限**: `form_create_limit_enabled`, `form_create_limit`（作成数のみ）
- **root権限**: `is_root`（全権限）

### 既存のカラム
- `users`テーブル: `form_create_limit_enabled`, `form_create_limit`
- `forms`テーブル: `created_by`（既存）
- `themes`テーブル: `created_by`（既存）

## パーミッション設計の2層構造

### レイヤー1: 操作パーミッション（Operation Permissions）
- **管理場所**: `/v1/system/roles/permissions`（Settingsテーブル）
- **例**: `forms.read`, `forms.write`, `responses.read`, `responses.write`
- **スコープ**: ロール全体に対する操作レベルの権限
- **将来の拡張**: rbac-matrix.jsonに基づく細かい操作パーミッション管理

### レイヤー2: リソースパーミッション（Resource Permissions）
- **管理場所**: `user_form_access`テーブル（中間テーブル）
- **例**: 「ユーザーAはフォーム1とフォーム2のみアクセス可能」
- **スコープ**: 特定リソース（フォーム）へのアクセス制限
- **今回実装**: フォームアクセス制限機能

### 権限チェックの順序
1. **rootユーザー**: 常に全権限（両レイヤーをスキップ）
2. **操作パーミッション**: ロールに`forms.read`などの操作権限があるかチェック
3. **リソースパーミッション**: フォームアクセス制限が有効な場合、`user_form_access`で特定フォームへのアクセス権をチェック

**重要**: 両レイヤーは独立しており、将来的に`/v1/system/roles/permissions`で細かい操作パーミッション管理に移行しても、リソースパーミッション（フォームアクセス制限）はそのまま機能します。

## 実装提案

### 1. フォームアクセス制限機能（リソースパーミッション）

#### 1.1 データベース設計

**usersテーブルに追加:**
```php
// マイグレーション: add_form_access_restriction_to_users_table.php
$table->boolean('form_access_restriction_enabled')->default(false)->comment('フォームアクセス制限を有効化');
```

**新規テーブル: user_form_access**
```php
// マイグレーション: create_user_form_access_table.php
Schema::create('user_form_access', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained('users')->onDelete('cascade');
    $table->foreignId('form_id')->constrained('forms')->onDelete('cascade');
    $table->timestamps();
    
    $table->unique(['user_id', 'form_id']);
    $table->index(['user_id']);
    $table->index(['form_id']);
});
```

#### 1.2 モデル実装

**User.phpに追加:**
```php
// アクセス可能なフォームのリレーション
public function accessibleForms(): BelongsToMany
{
    return $this->belongsToMany(Form::class, 'user_form_access');
}

// フォームへのアクセス権限チェック（リソースパーミッション）
// 注意: このメソッドは「リソースパーミッション」のみをチェックします
// 「操作パーミッション」（forms.read等）は別途チェックが必要です
public function canAccessForm(int $formId): bool
{
    // rootユーザーは全フォームにアクセス可能
    if ($this->is_root) {
        return true;
    }
    
    // フォームアクセス制限が無効な場合は、リソースパーミッションのチェックをスキップ
    // （操作パーミッションのみで判定）
    if (!$this->form_access_restriction_enabled) {
        return true; // リソースパーミッションの制限なし
    }
    
    // フォームアクセス制限が有効な場合は、user_form_accessテーブルをチェック
    return $this->accessibleForms()->where('forms.id', $formId)->exists();
}

// 操作パーミッションのチェック（将来の拡張用）
// 現在はロールベース、将来的に/v1/system/roles/permissionsで管理
public function hasPermission(string $permission): bool
{
    // rootユーザーは全権限
    if ($this->is_root) {
        return true;
    }
    
    // 将来的に/v1/system/roles/permissionsから取得したパーミッションをチェック
    // 現在はロールベースの簡易チェック
    $rolesPermissions = \App\Models\Setting::get('roles.permissions', []);
    
    foreach ($this->roles as $role) {
        $rolePerms = collect($rolesPermissions)->firstWhere('role', $role->code);
        if ($rolePerms && in_array($permission, $rolePerms['permissions'] ?? [])) {
            return true;
        }
    }
    
    return false;
}
```

**Form.phpに追加:**
```php
// アクセス可能なユーザーのリレーション
public function accessibleUsers(): BelongsToMany
{
    return $this->belongsToMany(User::class, 'user_form_access');
}
```

#### 1.3 コントローラー実装

**FormsController.phpに権限チェックを追加:**
```php
// 2層のパーミッションチェック（操作パーミッション + リソースパーミッション）
private function checkFormAccess(int $formId, string $operation = 'read'): void
{
    $user = auth()->user();
    
    // レイヤー1: 操作パーミッションのチェック
    // 将来的に/v1/system/roles/permissionsで管理される細かい操作パーミッションをチェック
    $permission = match($operation) {
        'read' => 'forms.read',
        'write', 'update', 'create' => 'forms.write',
        'delete' => 'forms.delete',
        default => 'forms.read',
    };
    
    if (!$user->hasPermission($permission)) {
        throw new AuthorizationException('この操作を実行する権限がありません');
    }
    
    // レイヤー2: リソースパーミッションのチェック（特定フォームへのアクセス）
    if (!$user->canAccessForm($formId)) {
        throw new AuthorizationException('このフォームにアクセスする権限がありません');
    }
}

// indexメソッドでフィルタリング
public function index(Request $request): JsonResponse
{
    // ... 既存のコード ...
    
    $user = auth()->user();
    
    // レイヤー1: 操作パーミッションのチェック
    if (!$user->hasPermission('forms.read')) {
        return ApiResponse::error($request, 403, ApiErrorCode::FORBIDDEN, 'messages.permission_denied');
    }
    
    $query = Form::query();
    
    // レイヤー2: リソースパーミッションのフィルタリング
    // フォームアクセス制限が有効なユーザーの場合、アクセス可能なフォームのみ表示
    if ($user->form_access_restriction_enabled && !$user->is_root) {
        $query->whereIn('id', $user->accessibleForms()->pluck('forms.id'));
    }
    
    // ... 既存のコード ...
}

// show, update, deleteメソッドで権限チェック
public function show(Request $request, int $id): JsonResponse
{
    $this->checkFormAccess($id, 'read');
    // ... 既存のコード ...
}

public function update(Request $request, int $id): JsonResponse
{
    $this->checkFormAccess($id, 'write');
    // ... 既存のコード ...
}

public function destroy(Request $request, int $id): JsonResponse
{
    $this->checkFormAccess($id, 'delete');
    // ... 既存のコード ...
}
```

#### 1.4 フロントエンド実装

**AccountListPage.tsxに追加:**
- フォームアクセス制限の有効/無効トグル
- アクセス可能なフォームの選択UI（マルチセレクトまたはチェックボックス）
- フォーム一覧から選択できるUI

**FormListPage.tsx:**
- アクセス権限のないフォームは表示しない（バックエンドでフィルタリング済み）

### 2. created_by / updated_by / deleted_by の追加

#### 2.1 データベース設計

**マイグレーション: add_audit_columns_to_forms_table.php**
```php
Schema::table('forms', function (Blueprint $table) {
    $table->unsignedBigInteger('updated_by')->nullable()->after('created_by');
    $table->unsignedBigInteger('deleted_by')->nullable()->after('deleted_at');
    
    $table->foreign('updated_by')->references('id')->on('users')->onDelete('set null');
    $table->foreign('deleted_by')->references('id')->on('users')->onDelete('set null');
});
```

**マイグレーション: add_audit_columns_to_themes_table.php**
```php
Schema::table('themes', function (Blueprint $table) {
    $table->unsignedBigInteger('updated_by')->nullable()->after('created_by');
    $table->unsignedBigInteger('deleted_by')->nullable()->after('deleted_at');
    
    $table->foreign('updated_by')->references('id')->on('users')->onDelete('set null');
    $table->foreign('deleted_by')->references('id')->on('users')->onDelete('set null');
});
```

**マイグレーション: add_audit_columns_to_users_table.php**
```php
Schema::table('users', function (Blueprint $table) {
    $table->unsignedBigInteger('created_by')->nullable()->after('id');
    $table->unsignedBigInteger('updated_by')->nullable()->after('created_at');
    $table->unsignedBigInteger('deleted_by')->nullable()->after('deleted_at');
    
    $table->foreign('created_by')->references('id')->on('users')->onDelete('set null');
    $table->foreign('updated_by')->references('id')->on('users')->onDelete('set null');
    $table->foreign('deleted_by')->references('id')->on('users')->onDelete('set null');
});
```

#### 2.2 モデル実装

**Form.phpに追加:**
```php
protected $fillable = [
    // ... 既存のフィールド ...
    'updated_by',
    'deleted_by',
];

protected $casts = [
    // ... 既存のキャスト ...
    'updated_by' => 'integer',
    'deleted_by' => 'integer',
];

// リレーション
public function updater(): BelongsTo
{
    return $this->belongsTo(User::class, 'updated_by');
}

public function deleter(): BelongsTo
{
    return $this->belongsTo(User::class, 'deleted_by');
}
```

**Theme.phpに追加:**
```php
protected $fillable = [
    // ... 既存のフィールド ...
    'updated_by',
    'deleted_by',
];

protected $casts = [
    // ... 既存のキャスト ...
    'updated_by' => 'integer',
    'deleted_by' => 'integer',
];

// リレーション
public function updater(): BelongsTo
{
    return $this->belongsTo(User::class, 'updated_by');
}

public function deleter(): BelongsTo
{
    return $this->belongsTo(User::class, 'deleted_by');
}
```

**User.phpに追加:**
```php
protected $fillable = [
    // ... 既存のフィールド ...
    'created_by',
    'updated_by',
    'deleted_by',
];

protected $casts = [
    // ... 既存のキャスト ...
    'created_by' => 'integer',
    'updated_by' => 'integer',
    'deleted_by' => 'integer',
];

// リレーション
public function creator(): BelongsTo
{
    return $this->belongsTo(User::class, 'created_by');
}

public function updater(): BelongsTo
{
    return $this->belongsTo(User::class, 'updated_by');
}

public function deleter(): BelongsTo
{
    return $this->belongsTo(User::class, 'deleted_by');
}
```

#### 2.3 コントローラー実装

**ObserverまたはMiddlewareで自動設定:**
```php
// app/Observers/FormObserver.php
class FormObserver
{
    public function creating(Form $form): void
    {
        if (auth()->check()) {
            $form->created_by = auth()->id();
        }
    }
    
    public function updating(Form $form): void
    {
        if (auth()->check()) {
            $form->updated_by = auth()->id();
        }
    }
    
    public function deleting(Form $form): void
    {
        if (auth()->check()) {
            $form->deleted_by = auth()->id();
            $form->save(); // SoftDeleteの前に保存
        }
    }
}
```

**または、BaseControllerで共通処理:**
```php
// app/Http/Controllers/Controller.php
protected function setAuditFields(Model $model, string $operation = 'update'): void
{
    if (!auth()->check()) {
        return;
    }
    
    $userId = auth()->id();
    
    switch ($operation) {
        case 'create':
            $model->created_by = $userId;
            break;
        case 'update':
            $model->updated_by = $userId;
            break;
        case 'delete':
            $model->deleted_by = $userId;
            break;
    }
}
```

## 実装の優先順位

### Phase 1: 監査カラムの追加（created_by/updated_by/deleted_by）
1. マイグレーションファイルの作成
2. モデルの更新（fillable, casts, リレーション）
3. Observerまたはコントローラーでの自動設定
4. 既存データの移行（必要に応じて）

### Phase 2: フォームアクセス制限機能
1. マイグレーションファイルの作成（usersテーブル、user_form_accessテーブル）
2. モデルの更新（リレーション、canAccessFormメソッド）
3. FormsControllerの権限チェック実装
4. フロントエンドUI実装（AccountListPage.tsx）

## 注意事項

1. **既存データの移行**: 既存のフォーム/テーマ/ユーザーの`created_by`は既に設定されているが、`updated_by`と`deleted_by`はNULLになる
2. **パフォーマンス**: フォーム一覧取得時に`user_form_access`テーブルをJOINするため、インデックスが重要
3. **rootユーザー**: rootユーザーは常に全フォームにアクセス可能（両レイヤーの制限をスキップ）
4. **後方互換性**: フォームアクセス制限が無効な場合は、リソースパーミッションのチェックをスキップ（操作パーミッションのみで判定）
5. **将来の移行**: `/v1/system/roles/permissions`で細かい操作パーミッション管理に移行しても、リソースパーミッション（フォームアクセス制限）は独立して機能する
6. **2層チェック**: 操作パーミッションとリソースパーミッションは独立したレイヤーとして実装し、両方をチェックする必要がある

## 将来の拡張（/v1/system/roles/permissions統合）

将来的にrbac-matrix.jsonに基づく細かい操作パーミッション管理に移行する際は、以下のように拡張可能：

```php
// User.php - 操作パーミッションのチェック（拡張版）
public function hasPermission(string $permission): bool
{
    if ($this->is_root) {
        return true;
    }
    
    // /v1/system/roles/permissionsから取得したパーミッションをチェック
    $rolesPermissions = \App\Models\Setting::get('roles.permissions', []);
    
    foreach ($this->roles as $role) {
        $rolePerms = collect($rolesPermissions)->firstWhere('role', $role->code);
        if ($rolePerms && in_array($permission, $rolePerms['permissions'] ?? [])) {
            return true;
        }
    }
    
    return false;
}
```

この実装により、操作パーミッション（forms.read, forms.write等）とリソースパーミッション（特定フォームへのアクセス）は独立して管理され、将来的な拡張が容易になります。

## ロール別権限マトリックス（Seeder実装版）

### 実装方針
- **現在**: Seederで`/v1/system/roles/permissions`のデフォルト値を投入
- **将来**: rootのみがパーミッション設定操作可能な画面を構築（S-YY: ROLE_PERMISSION_ASSIGN）

### 権限マトリックス表

| 操作カテゴリ | 操作内容 | system_admin | form_admin | operator | viewer | 備考 |
|------------|---------|-------------|-----------|----------|--------|------|
| **フォーム管理** |
| フォーム一覧 | 閲覧 | ✅ | ✅ | ✅ | ✅ | リソースパーミッションでフィルタリング |
| フォーム作成 | 新規作成 | ✅ | ✅ | ❌ | ❌ | form_adminは自分が作成したフォームに全権限 |
| フォーム編集 | 基本設定・項目設定 | ✅ | ✅* | ❌ | ❌ | *許可されたフォーム + 自分が作成したフォーム |
| フォーム削除 | 削除 | ✅ | ✅* | ❌ | ❌ | *許可されたフォーム + 自分が作成したフォーム |
| フォームプレビュー | プレビュー | ✅ | ✅* | ✅* | ✅* | *アクセス可能なフォームのみ |
| フォーム項目CSV | インポート/エクスポート | ✅ | ✅* | ❌ | ❌ | *許可されたフォーム + 自分が作成したフォーム |
| **回答管理** |
| 回答一覧 | 閲覧 | ✅ | ✅* | ✅* | ✅* | *アクセス可能なフォームの回答のみ |
| 回答詳細 | 閲覧 | ✅ | ✅* | ✅* | ✅* | *アクセス可能なフォームの回答のみ |
| 回答CSVエクスポート | CSVダウンロード | ✅ | ✅* | ✅* | ❌ | *アクセス可能なフォームの回答のみ |
| 回答PDF再生成 | PDF再生成 | ✅ | ✅* | ✅* | ❌ | *アクセス可能なフォームの回答のみ |
| 通知再送信 | 通知再送信 | ✅ | ✅* | ✅* | ❌ | *アクセス可能なフォームの回答のみ |
| **システム管理** |
| アカウント管理 | 一覧・作成・編集・削除 | ✅ | ❌ | ❌ | ❌ | rootのみ（S-02～S-05） |
| ログ閲覧 | 処理ログ一覧・詳細 | ✅ | ❌ | ❌ | ❌ | system_adminのみ（L-01, L-02） |
| システム設定 | 設定変更 | ✅** | ❌ | ❌ | ❌ | **rootのみ（S-XX） |
| パーミッション設定 | ロール権限定義 | ✅** | ❌ | ❌ | ❌ | **rootのみ（S-YY） |
| フォームアクセス制限設定 | ユーザー別フォーム制限 | ✅ | ✅ | ❌ | ❌ | system_admin, form_adminのみ |
| **テーマ管理** |
| テーマ一覧 | 閲覧 | ✅ | ✅ | ✅ | ❌ | |
| テーマ作成 | 新規作成 | ✅ | ✅ | ❌ | ❌ | |
| テーマ編集 | 編集 | ✅ | ✅* | ❌ | ❌ | *自分が作成したテーマ |
| テーマ削除 | 削除 | ✅ | ✅* | ❌ | ❌ | *自分が作成したテーマ |
| **ダッシュボード** |
| ダッシュボード | 基本情報表示 | ✅ | ✅ | ✅ | ✅ | ロール別に表示ブロックが異なる |
| エラー情報 | 最新エラー情報 | ✅ | ❌ | ❌ | ❌ | system_adminのみ |

### リソースパーミッション（フォームアクセス制限）の適用

#### form_admin
- **許可されたフォーム**: `user_form_access`テーブルで指定されたフォーム
- **自分が作成したフォーム**: `forms.created_by = user.id`のフォーム
- **両方にアクセス可能**: 許可されたフォーム OR 自分が作成したフォーム

#### operator / viewer
- **許可されたフォーム**: `user_form_access`テーブルで指定されたフォームのみ
- **フォーム作成不可**: 自分が作成したフォームという概念なし

### Seeder実装例

```php
// database/seeders/RolePermissionsSeeder.php
class RolePermissionsSeeder extends Seeder
{
    public function run(): void
    {
        $permissions = [
            [
                'role' => 'system_admin',
                'permissions' => [
                    'forms.read',
                    'forms.write',
                    'forms.delete',
                    'responses.read',
                    'responses.write',
                    'responses.export',
                    'responses.pdf_regenerate',
                    'responses.notification_resend',
                    'users.read',
                    'users.write',
                    'users.delete',
                    'logs.read',
                    'settings.read',
                    'settings.write',
                    'permissions.read',
                    'permissions.write',
                    'themes.read',
                    'themes.write',
                    'themes.delete',
                    'form_access_restriction.write', // フォームアクセス制限の設定
                ],
            ],
            [
                'role' => 'form_admin',
                'permissions' => [
                    'forms.read',
                    'forms.write',
                    'forms.delete',
                    'responses.read',
                    'responses.write',
                    'responses.export',
                    'responses.pdf_regenerate',
                    'responses.notification_resend',
                    'themes.read',
                    'themes.write',
                    'themes.delete',
                    'form_access_restriction.write', // フォームアクセス制限の設定
                ],
            ],
            [
                'role' => 'operator',
                'permissions' => [
                    'forms.read',
                    'responses.read',
                    'responses.write',
                    'responses.export',
                    'responses.pdf_regenerate',
                    'responses.notification_resend',
                ],
            ],
            [
                'role' => 'viewer',
                'permissions' => [
                    'forms.read',
                    'responses.read',
                ],
            ],
        ];

        Setting::set('roles.permissions', $permissions, 'json');
    }
}
```

### 権限チェックの実装例

```php
// User.php - 操作パーミッションのチェック
public function hasPermission(string $permission): bool
{
    if ($this->is_root) {
        return true;
    }
    
    $rolesPermissions = \App\Models\Setting::get('roles.permissions', []);
    
    foreach ($this->roles as $role) {
        $rolePerms = collect($rolesPermissions)->firstWhere('role', $role->code);
        if ($rolePerms && in_array($permission, $rolePerms['permissions'] ?? [])) {
            return true;
        }
    }
    
    return false;
}

// FormsController.php - フォーム編集権限チェック
public function update(Request $request, int $id): JsonResponse
{
    $user = auth()->user();
    
    // レイヤー1: 操作パーミッション
    if (!$user->hasPermission('forms.write')) {
        throw new AuthorizationException('フォーム編集の権限がありません');
    }
    
    // レイヤー2: リソースパーミッション
    $form = Form::findOrFail($id);
    
    // form_adminの場合、許可されたフォーム OR 自分が作成したフォーム
    if ($user->hasRole(RoleCode::FORM_ADMIN)) {
        $canAccess = $user->canAccessForm($id) || $form->created_by === $user->id;
        if (!$canAccess) {
            throw new AuthorizationException('このフォームを編集する権限がありません');
        }
    } else {
        // system_admin, operator, viewer は通常のリソースパーミッションチェック
        if (!$user->canAccessForm($id)) {
            throw new AuthorizationException('このフォームにアクセスする権限がありません');
        }
    }
    
    // ... 既存の更新処理 ...
}
```

### 注意事項

1. **form_adminの特別扱い**: 自分が作成したフォームには、フォームアクセス制限が有効でもアクセス可能
2. **operatorの制限**: フォームの作成・編集は不可。回答の操作のみ可能
3. **viewerの制限**: 回答の閲覧のみ。CSVエクスポート、PDF再生成、通知再送信は不可
4. **rootユーザー**: 全権限（両レイヤーをスキップ）
5. **将来の拡張**: Seederで投入したパーミッションは、将来的にrootのみが操作可能な画面（S-YY）で変更可能

## 実装状況

### Phase 1: 監査カラムの追加（created_by/updated_by/deleted_by） ✅ 完了

**実装日**: 2026-01-21

**実装内容**:
- ✅ `forms`テーブルに`updated_by`, `deleted_by`カラムを追加
- ✅ `themes`テーブルに`updated_by`, `deleted_by`カラムを追加
- ✅ `users`テーブルに`created_by`, `updated_by`, `deleted_by`カラムを追加
- ✅ 各モデル（Form, Theme, User）にリレーションとfillable/castsを追加
- ✅ Observer（FormObserver, ThemeObserver, UserObserver）で自動設定を実装

**コミット情報**:
- バックエンド: `backend-v0.8.52` → `backend-v0.8.53`

### Phase 2: フォームアクセス制限機能 ✅ 完了

**実装日**: 2026-01-21

**バックエンド実装**:
- ✅ `users`テーブルに`form_access_restriction_enabled`カラムを追加
- ✅ `user_form_access`中間テーブルを作成
- ✅ `User`モデルに`accessibleForms()`リレーションと`canAccessForm()`メソッドを追加
- ✅ `Form`モデルに`accessibleUsers()`リレーションを追加
- ✅ `FormsController`に2層のパーミッションチェック（操作パーミッション + リソースパーミッション）を実装
- ✅ `FormsController::index()`でフォームアクセス制限が有効なユーザー向けにフィルタリングを実装
- ✅ `AdminUsersController`にフォームアクセス制限の設定機能を追加（作成・更新・詳細表示）

**フロントエンド実装**:
- ✅ `AccountListPage.tsx`にフォームアクセス制限の有効/無効トグルを追加
- ✅ `AccountListPage.tsx`にアクセス可能なフォームの選択UI（チェックボックス）を追加
- ✅ `AccountListPage.tsx`の詳細表示モーダルにフォームアクセス制限の状態とアクセス可能なフォーム一覧を表示
- ✅ `FormListPage.tsx`はバックエンドでフィルタリング済みのため、アクセス権限のないフォームは表示されない
- ✅ 多言語対応（日本語・英語）を実装

**コミット情報**:
- バックエンド: `backend-v0.8.52` → `backend-v0.8.53`
- フロントエンド: `frontend-0.8.13` → `frontend-0.8.14`

### Phase 3: パスワード管理機能 ✅ 完了

**実装日**: 2026-01-21

**バックエンド実装**:
- ✅ `AuthController`にパスワード変更エンドポイント（`PUT /v1/auth/password`）を追加
- ✅ `AuthController`に招待トークン検証エンドポイント（`GET /v1/auth/invite/{token}`）を追加
- ✅ `AuthController`に招待受理エンドポイント（`POST /v1/auth/invite/accept`）を追加
- ✅ `AdminInviteMail`の招待URLを`/invite/accept?token=`に変更

**フロントエンド実装**:
- ✅ `PasswordChangeDialog.tsx`コンポーネントを新規作成（パスワード変更ダイアログ）
- ✅ `InviteAcceptPage.tsx`ページを新規作成（招待受理・パスワード設定画面）
- ✅ `AppLayout.tsx`にパスワード変更ボタンを追加（サイドバー）
- ✅ `AuthContext.tsx`に`setToken()`関数を追加（招待受理後の自動ログイン用）
- ✅ `App.tsx`に`/invite/accept`ルートを追加
- ✅ `NavIcons.tsx`に`IconKey`コンポーネントを追加
- ✅ パスワード変更・招待受理関連の表示文言を多言語対応に統一

**コミット情報**:
- バックエンド: `backend-v0.8.52` → `backend-v0.8.53`
- フロントエンド: `frontend-0.8.14` → `frontend-0.8.15`

### 未実装項目

- ⏳ `/v1/system/roles/permissions`での細かい操作パーミッション管理（将来の拡張）
- ⏳ rootのみが操作可能なパーミッション設定画面（S-YY: ROLE_PERMISSION_ASSIGN）
