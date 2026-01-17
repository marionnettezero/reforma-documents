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

### formsテーブルへの追加カラム

| カラム名 | 型 | NULL許可 | 説明 |
|---------|-----|---------|------|
| `theme_id` | string | YES | テーマID（プリセットテーマ識別子、デフォルト: "default"） |
| `theme_tokens` | json | YES | テーマトークン（CSS変数の値） |

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

### GET /v1/forms/{id}

**レスポンス追加フィールド**:

```json
{
  "id": 1,
  "code": "FORM001",
  // ... 既存フィールド ...
  "theme_id": "default",
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
```

- `theme_id`: `string` (optional) - テーマID
- `theme_tokens`: `object` (optional) - テーマトークンオブジェクト

### PUT /v1/forms/{id}

**リクエスト追加フィールド**:

```json
{
  // ... 既存フィールド ...
  "theme_id": "default",
  "theme_tokens": {
    "color_primary": "#007bff",
    "color_secondary": "#6c757d",
    // ... その他のトークン ...
  }
}
```

- `theme_id`: `string` (optional) - テーマID
- `theme_tokens`: `object` (optional) - テーマトークンオブジェクト

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

1. ✅ マイグレーション: `forms`テーブルに`theme_id`と`theme_tokens`カラムを追加
2. ✅ モデル: `Form`モデルに`theme_id`と`theme_tokens`を追加（fillable, casts）
3. ✅ API: `GET /v1/forms/{id}`のレスポンスに`theme_id`と`theme_tokens`を追加
4. ✅ API: `PUT /v1/forms/{id}`のリクエストに`theme_id`と`theme_tokens`を追加
5. ✅ バリデーション: `theme_tokens`のスキーマバリデーション

### フロントエンド

1. 公開フォーム表示時に`theme_id`と`theme_tokens`を取得
2. フォームコンテナに`data-theme-id`属性を付与
3. `theme_tokens`をCSS変数に展開
4. プリセットテーマの定義と適用

## 参照

- reforma-notes-v1.1.0.md SUPP-THEME-001
- remaining-tasks.md
