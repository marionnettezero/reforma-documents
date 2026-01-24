# SUPP-THEME-001: テーマ機能 実装仕様

**作成日**: 2026-01-17  
**ベース**: reforma-notes-v1.1.0.md SUPP-THEME-001

---

## 概要

v1.xでは安全にテーマトークン（CSS変数）とプリセットテーマ選択で提供。外部CSS URLはv2候補。

## 基本方針

- **アプローチ**: `theme_tokens_only + template_pack`
- **外部CSS URL**: v1.xでは提供しない（v2で検討）
- **セキュリティ**: CSPポリシーに準拠

## データモデル

### themesテーブル（新規作成）

| カラム名 | 型 | NULL許可 | 説明 |
|---------|-----|---------|------|
| `id` | bigint | NO | 主キー |
| `code` | string | NO | テーマコード（ユニーク、例: "default", "dark", "minimal"） |
| `name` | string | NO | テーマ名（表示用） |
| `description` | text | YES | テーマの説明 |
| `theme_tokens` | json | NO | テーマトークン（CSS変数の値） |
| `is_preset` | boolean | NO | プリセットテーマかどうか（デフォルト: false） |
| `is_active` | boolean | NO | 有効かどうか（デフォルト: true） |
| `created_by` | bigint | YES | 作成者ID（プリセットテーマはNULL） |
| `created_at` | timestamp | NO | 作成日時 |
| `updated_at` | timestamp | NO | 更新日時 |
| `deleted_at` | timestamp | YES | 削除日時（論理削除） |

**インデックス**:
- `code` (UNIQUE)
- `is_active`
- `is_preset`

### formsテーブルへの追加カラム

| カラム名 | 型 | NULL許可 | 説明 |
|---------|-----|---------|------|
| `theme_id` | bigint | YES | テーマID（themesテーブルへの外部キー、デフォルト: NULL） |
| `theme_tokens` | json | YES | テーマトークン（フォーム固有のカスタマイズ、デフォルト: NULL） |

**注意**: 
- `theme_id`が指定されている場合、`theme_tokens`は`themes`テーブルから取得
- `theme_id`がNULLで`theme_tokens`が指定されている場合、フォーム固有のカスタムテーマとして使用
- 両方NULLの場合、デフォルトテーマ（code="default"）を使用

### テーマトークンスキーマ

```json
{
  "color_primary": "#xxxxxx",      // プライマリカラー
  "color_secondary": "#xxxxxx",    // セカンダリカラー
  "color_bg": "#xxxxxx",           // 背景色
  "color_text": "#xxxxxx",          // テキスト色
  "radius": "0|4|8|12",            // 角丸（px）
  "spacing_scale": "sm|md|lg",     // スペーシングスケール
  "font_family": "system|noto_sans|custom (v2)",  // フォントファミリー
  "button_style": "solid|outline",  // ボタンスタイル
  "input_style": "standard|filled"  // 入力フィールドスタイル
}
```

### デフォルト値

- `theme_id`: `"default"`
- `theme_tokens`: `null`（プリセットテーマを使用）

## API仕様

### テーマ管理API（System Admin以上）

#### GET /v1/system/themes

**権限**: System Admin以上  
**説明**: テーマ一覧を取得

**クエリパラメータ**:
- `page`: integer (required) - ページ番号
- `per_page`: integer (required) - 1ページあたりの件数（1-200）
- `sort`: string (optional) - ソート順（`created_at_desc`, `created_at_asc`, `name_asc`, `name_desc`）
- `is_preset`: boolean (optional) - プリセットテーマのみ取得
- `is_active`: boolean (optional) - 有効なテーマのみ取得（デフォルト: true、フォーム選択肢用）
- `q`: string (optional) - キーワード検索（code, name）

**注意**: 
- `is_active`パラメータが指定されていない場合、デフォルトで`is_active=true`のみ返す（フォーム選択肢用）
- 管理画面で全テーマを確認する場合は`is_active`を指定しないか、明示的に`false`を含める

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "themes": [
      {
        "id": 1,
        "code": "default",
        "name": "デフォルトテーマ",
        "description": "標準的なデフォルトテーマ",
        "theme_tokens": { ... },
        "is_preset": true,
        "is_active": true,
        "created_by": null,
        "created_at": "2026-01-17T00:00:00.000000Z",
        "updated_at": "2026-01-17T00:00:00.000000Z"
      }
    ],
    "pagination": {
      "current_page": 1,
      "per_page": 20,
      "total": 10,
      "last_page": 1
    }
  }
}
```

#### POST /v1/system/themes

**権限**: System Admin以上  
**説明**: テーマを作成

**リクエストボディ**:
```json
{
  "code": "custom_theme_1",
  "name": "カスタムテーマ1",
  "description": "カスタムテーマの説明",
  "theme_tokens": {
    "color_primary": "#007bff",
    "color_secondary": "#6c757d",
    "color_bg": "#ffffff",
    "color_text": "#212529",
    "radius": "4",
    "spacing_scale": "md",
    "font_family": "system",
    "button_style": "solid",
    "input_style": "standard"
  },
  "is_active": true
}
```

**バリデーション**:
- `code`: required, string, max:255, unique:themes,code
- `name`: required, string, max:255
- `description`: optional, string
- `theme_tokens`: required, array（テーマトークンスキーマに準拠）
- `is_active`: optional, boolean, default: true

#### GET /v1/system/themes/{id}

**権限**: System Admin以上  
**説明**: テーマ詳細を取得

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "theme": {
      "id": 1,
      "code": "default",
      "name": "デフォルトテーマ",
      "description": "標準的なデフォルトテーマ",
      "theme_tokens": { ... },
      "is_preset": true,
      "is_active": true,
      "created_by": null,
      "created_at": "2026-01-17T00:00:00.000000Z",
      "updated_at": "2026-01-17T00:00:00.000000Z"
    }
  }
}
```

#### PUT /v1/system/themes/{id}

**権限**: 
- 通常テーマ（`is_preset=false`）: System Admin以上
- プリセットテーマ（`is_preset=true`）: root-only（`is_root=true`必須）

**説明**: テーマを更新

**リクエストボディ**:
```json
{
  "name": "更新されたテーマ名",
  "description": "更新された説明",
  "theme_tokens": { ... },
  "is_active": true
}
```

**注意**: 
- `code`は更新不可（プリセットテーマのcodeも更新不可）
- `is_preset`は更新不可
- `created_by`は更新不可
- プリセットテーマの更新はroot-only権限が必要

#### DELETE /v1/system/themes/{id}

**権限**: System Admin以上  
**説明**: テーマを削除（論理削除）

**注意**: 
- プリセットテーマ（`is_preset=true`）は削除不可
- 使用中のテーマ（フォームで使用されている）は削除不可（使用状況確認APIで確認可能）

#### GET /v1/system/themes/{id}/usage

**権限**: System Admin以上  
**説明**: テーマの使用状況を確認（どのフォームで使用されているか）

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "theme": {
      "id": 1,
      "code": "default",
      "name": "デフォルトテーマ"
    },
    "usage": {
      "form_count": 5,
      "forms": [
        {
          "id": 1,
          "code": "FORM001",
          "name": "フォーム1"
        },
        {
          "id": 2,
          "code": "FORM002",
          "name": "フォーム2"
        }
      ]
    }
  }
}
```

#### POST /v1/system/themes/{id}/copy

**権限**: System Admin以上  
**説明**: テーマをコピーして新規テーマを作成

**リクエストボディ**:
```json
{
  "code": "copied_theme_1",
  "name": "コピーされたテーマ",
  "description": "既存テーマからコピー"
}
```

**バリデーション**:
- `code`: required, string, max:255, unique:themes,code
- `name`: required, string, max:255
- `description`: optional, string

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "theme": {
      "id": 2,
      "code": "copied_theme_1",
      "name": "コピーされたテーマ",
      "theme_tokens": { ... },
      "is_preset": false,
      "is_active": true
    }
  }
}
```

**注意**: 
- 元のテーマの`theme_tokens`をコピー
- `is_preset`は常に`false`（コピーされたテーマはプリセットではない）
- `is_active`は元のテーマと同じ値をコピー

### 公開フォームAPI（認証不要）

#### GET /v1/public/forms/{form_key}

**権限**: 認証不要  
**説明**: 公開フォーム表示情報を取得（テーマ情報を含む）

**レスポンス追加フィールド**:
```json
{
  "success": true,
  "data": {
    "form": {
      "form_key": "FORM001",
      "title": "フォームタイトル",
      // ... 既存フィールド ...
      "theme_id": 1,
      "theme_code": "default",
      "theme_tokens": {
        "color_primary": "#007bff",
        "color_secondary": "#6c757d",
        "color_bg": "#ffffff",
        "color_text": "#212529",
        "radius": "4",
        "spacing_scale": "md",
        "font_family": "system",
        "button_style": "solid",
        "input_style": "standard"
      }
    }
  }
}
```

**注意**: 
- 公開フォームでは`theme_id`と`theme_code`、`theme_tokens`のみを返す（テーマ詳細情報は不要）
- テーマ解決ロジックは`GET /v1/forms/{id}`と同じ

### フォームへのテーマ適用API（Form Admin以上）

#### GET /v1/forms/{id}

**権限**: 認証必須  
**説明**: フォーム詳細を取得（テーマ情報を含む）

**レスポンス追加フィールド**:
```json
{
  "id": 1,
  "code": "FORM001",
  // ... 既存フィールド ...
  "theme_id": 1,
  "theme": {
    "id": 1,
    "code": "default",
    "name": "デフォルトテーマ",
    "theme_tokens": { ... }
  },
  "theme_tokens": {
    "color_primary": "#007bff",
    // ... カスタムトークン（theme_tokensが指定されている場合） ...
  }
}
```

**注意**: 
- `theme_id`が指定されている場合、`theme`オブジェクトと`theme_tokens`（themesテーブルから取得）を返す
- `theme_id`がNULLで`theme_tokens`が指定されている場合、`theme_tokens`のみを返す
- 両方NULLの場合、デフォルトテーマ（code="default"）の情報を返す

#### PUT /v1/forms/{id}

**権限**: Form Admin以上  
**説明**: フォームを更新（テーマ適用を含む）

**リクエスト追加フィールド**:
```json
{
  // ... 既存フィールド ...
  "theme_id": 1,
  "theme_tokens": {
    "color_primary": "#007bff",
    "color_secondary": "#6c757d",
    // ... その他のトークン ...
  }
}
```

**バリデーション**:
- `theme_id`: optional, integer, exists:themes,id,where:is_active,true（is_active=trueのテーマのみ）
- `theme_tokens`: optional, array（テーマトークンスキーマに準拠）

**注意**: 
- `is_active=false`のテーマは選択肢に表示されない（テーマ一覧APIでも`is_active=true`のみ返すオプションあり）
- `is_active=false`のテーマを直接指定しても適用不可（バリデーションエラー）

**注意**: 
- `theme_id`と`theme_tokens`の両方を指定した場合、`theme_tokens`が優先される（フォーム固有のカスタマイズ）
- `theme_id`のみ指定した場合、指定されたテーマのトークンを使用
- `theme_tokens`のみ指定した場合、フォーム固有のカスタムテーマとして使用
- 両方NULLの場合、デフォルトテーマ（code="default"）を使用

## フロントエンド実装方針

### UI適用

1. **公開フォーム root に data-theme-id を付与**
   ```html
   <div data-theme-id="default" class="reforma-form">
     <!-- フォームコンテンツ -->
   </div>
   ```

2. **theme_tokens を CSS variables に展開**
   - `:root`ではなく、フォームコンテナ配下に展開
   ```css
   .reforma-form[data-theme-id="default"] {
     --color-primary: #007bff;
     --color-secondary: #6c757d;
     --color-bg: #ffffff;
     --color-text: #212529;
     --radius: 4px;
     --spacing-scale: md;
     --font-family: system-ui, -apple-system, sans-serif;
     --button-style: solid;
     --input-style: standard;
   }
   ```

3. **プリセットテーマ**
   - フロントエンドに同梱（またはAPIから取得）
   - プリセットテーマの定義例:
     - `default`: デフォルトテーマ
     - `dark`: ダークテーマ
     - `minimal`: ミニマルテーマ

## CSPポリシー

v1.xでは外部CSS URLを許可しないため、以下のCSPポリシーを適用:

```json
{
  "allow_external_css": false,
  "style_src": ["'self'"],
  "font_src": ["'self'"],
  "img_src": ["'self'", "data:"]
}
```

## v2で検討する機能

- 任意の外部CSS URL指定（安全/運用のため）
- 任意HTML埋め込み

## 実装タスク

### バックエンド

#### データモデル

1. ✅ マイグレーション: `themes`テーブルを作成
2. ✅ マイグレーション: `forms`テーブルに`theme_id`と`theme_tokens`カラムを追加
3. ✅ モデル: `Theme`モデルを作成
4. ✅ モデル: `Form`モデルに`theme_id`と`theme_tokens`を追加（fillable, casts）
5. ✅ シーダー: プリセットテーマ（default, dark, minimal）を作成

#### テーマ管理API（System Admin以上）

6. ✅ コントローラ: `System\ThemesController`を作成
7. ✅ API: `GET /v1/system/themes` - テーマ一覧取得（is_activeフィルタ対応）
8. ✅ API: `POST /v1/system/themes` - テーマ作成
9. ✅ API: `GET /v1/system/themes/{id}` - テーマ詳細取得
10. ✅ API: `PUT /v1/system/themes/{id}` - テーマ更新（プリセットテーマはroot-only）
11. ✅ API: `DELETE /v1/system/themes/{id}` - テーマ削除（論理削除、使用中は不可）
12. ✅ API: `GET /v1/system/themes/{id}/usage` - テーマ使用状況確認
13. ✅ API: `POST /v1/system/themes/{id}/copy` - テーマコピー
14. ✅ バリデーション: `theme_tokens`のスキーマバリデーション
15. ✅ 権限チェック: System Admin以上のみアクセス可能（プリセットテーマ更新はroot-only）
16. ✅ 削除チェック: 使用中のテーマは削除不可

#### フォームへのテーマ適用API（Form Admin以上）

14. ✅ API: `GET /v1/forms/{id}`のレスポンスに`theme_id`、`theme`、`theme_tokens`を追加
15. ✅ API: `PUT /v1/forms/{id}`のリクエストに`theme_id`と`theme_tokens`を追加
16. ✅ API: `GET /v1/public/forms/{form_key}`のレスポンスに`theme_id`、`theme_code`、`theme_tokens`を追加
17. ✅ 権限チェック: Form Admin以上のみフォーム編集可能
18. ✅ ロジック: テーマ解決（theme_id → theme_tokens、デフォルトテーマのフォールバック）

#### テスト

19. ✅ テーマ管理APIのテスト（System Admin権限チェック含む、11テスト、46アサーション）
20. ✅ フォームへのテーマ適用のテスト（Form Admin権限チェック含む、4テスト、26アサーション）
21. ✅ テーマトークンのバリデーションテスト（含む）

### フロントエンド

1. ✅ 公開フォーム表示時に`theme_id`と`theme_tokens`を取得
2. ✅ フォームコンテナに`data-theme-id`属性を付与
3. ✅ `theme_tokens`をCSS変数に展開
4. ✅ プリセットテーマの定義と適用（バックエンドで管理、API経由で取得・適用）

## 参照

- reforma-notes-v1.1.0.md SUPP-THEME-001
- remaining-tasks.md
