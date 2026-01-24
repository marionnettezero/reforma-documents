# theme_tokens から custom_style_config への移行タスク

## 概要

今後`theme_tokens`を使わない方向に進むため、`theme_tokens`にあった設定を`custom_style_config`で再現できるようにします。

## 現状確認

### theme_tokens のプロパティ

現在の`theme_tokens`には以下のプロパティがあります：

1. **color_primary**: プライマリカラー（ボタン背景色など）
2. **color_secondary**: セカンダリカラー（現在は使用されていない可能性）
3. **color_bg**: 背景色
4. **color_text**: 文字色
5. **radius**: 角丸の値（'0', '4', '8'など）
6. **spacing_scale**: スペーシングスケール（'sm', 'md'など）
7. **font_family**: フォントファミリー（'system'など）
8. **button_style**: ボタンスタイル（'solid', 'outline'など）
9. **input_style**: 入力フィールドスタイル（'filled', 'standard'など）

### custom_style_config の現在の構造

`custom_style_config`には以下の要素があります：
- `container`, `header`, `content`, `footer`
- `card`, `cardBody`, `headerCard`
- `title`, `description`, `fieldLabel`
- `input`, `button`, `buttonPrimary`, `buttonSecondary`
- `stepTab`, `stepTabActive`, `groupName`
- `errorMessage`, `confirmationSection`, `helpText`, `helpTextIcon`

### 移行マッピング

| theme_tokens プロパティ | custom_style_config への移行先 |
|------------------------|-------------------------------|
| `color_primary` | `buttonPrimary.style.backgroundColor`（既に設定済み） |
| `color_secondary` | `buttonSecondary.style.backgroundColor`（新規追加） |
| `color_bg` | `container.style.backgroundColor`（既に設定済み） |
| `color_text` | `container.style.color`（既に設定済み） |
| `radius` | 各要素の`style.borderRadius`（一部設定済み、全要素に適用） |
| `spacing_scale` | グローバルCSSまたは各要素の`style.padding`/`style.margin` |
| `font_family` | `container.style.fontFamily`（新規追加） |
| `button_style` | `buttonPrimary.style`に反映（solid: 背景色あり、outline: ボーダーのみ） |
| `input_style` | `input.style`に反映（filled: 背景色あり、standard: 背景色なし/薄い） |

## タスクリスト

### ✅ タスク1: custom_style_config の型定義を拡張
- **ファイル**: `src/types/customStyle.ts`
- **内容**: 
  - 必要に応じて型定義を確認（現状で十分な可能性あり）
  - `ElementStyleConfig`の`style`は`Record<string, string>`なので、追加のプロパティは既に対応可能
- **実装状況**: ✅ 既に対応可能（型定義の拡張不要）

### ⚠️ タスク2: radius を全要素に適用
- **ファイル**: `database/seeders/ThemeSeeder.php`, `src/constants/presetThemes.ts`
- **内容**: 
  - `theme_tokens.radius`の値を各要素の`style.borderRadius`に設定
  - 対象要素: `card`, `buttonPrimary`, `buttonSecondary`, `input`, `button`など
  - 値の変換: `'0'` → `'0px'`, `'4'` → `'4px'`, `'8'` → `'8px'`
- **実装状況**: ⚠️ class（Tailwindクラス: `rounded-xl`など）で対応されているため、`style.borderRadius`への設定は不要

### ✅ タスク3: font_family を container に追加
- **ファイル**: `database/seeders/ThemeSeeder.php`, `src/constants/presetThemes.ts`
- **内容**: 
  - `theme_tokens.font_family`の値を`container.style.fontFamily`に設定
  - 値: `'system'` → `'system-ui, -apple-system, sans-serif'`など
- **実装状況**: ✅ 実装済み（全テーマで`container.style.fontFamily`に設定済み）

### ✅ タスク4: spacing_scale をグローバルCSSまたは各要素に反映
- **ファイル**: `database/seeders/ThemeSeeder.php`, `src/constants/presetThemes.ts`
- **内容**: 
  - `theme_tokens.spacing_scale`の値を`globalCss`または各要素の`style.padding`/`style.margin`に反映
  - 値のマッピング:
    - `'sm'`: 小さいスペーシング（例: `padding: '0.5rem'`）
    - `'md'`: 中程度のスペーシング（例: `padding: '1rem'`）
    - `'lg'`: 大きいスペーシング（例: `padding: '1.5rem'`）
  - または`globalCss`にCSS変数として定義
- **実装状況**: ✅ 実装済み（全テーマで`globalCss`にCSS変数として定義済み）

### ✅ タスク5: button_style を buttonPrimary に反映
- **ファイル**: `database/seeders/ThemeSeeder.php`, `src/constants/presetThemes.ts`
- **内容**: 
  - `theme_tokens.button_style`に基づいて`buttonPrimary.style`を調整
  - `'solid'`: 背景色を設定（既に設定済み）
  - `'outline'`: 背景色を`transparent`または`'none'`にし、`borderColor`と`borderWidth`を設定
- **実装状況**: ✅ 実装済み（Classicテーマで`outline`スタイル実装済み、`borderWidth`も追加済み）

### ✅ タスク6: input_style を input に反映
- **ファイル**: `database/seeders/ThemeSeeder.php`, `src/constants/presetThemes.ts`
- **内容**: 
  - `theme_tokens.input_style`に基づいて`input.style`を調整
  - `'filled'`: 背景色を設定（既に設定済み）
  - `'standard'`: 背景色を`transparent`または`'none'`にし、ボーダーのみ
- **実装状況**: ✅ 実装済み（Light, ReForma, Classicテーマで`standard`スタイル実装済み、`borderWidth`も追加済み）

### ✅ タスク7: color_secondary を buttonSecondary に追加
- **ファイル**: `database/seeders/ThemeSeeder.php`, `src/constants/presetThemes.ts`
- **内容**: 
  - `theme_tokens.color_secondary`の値を`buttonSecondary.style.backgroundColor`に設定
  - または`buttonSecondary.style.borderColor`に設定（outlineスタイルの場合）
- **実装状況**: ✅ 実装済み（全テーマで`buttonSecondary.style.backgroundColor`に`#6c757d`として設定済み）

### ✅ タスク8: 各プリセットテーマの custom_style_config を更新
- **ファイル**: `database/seeders/ThemeSeeder.php`, `src/constants/presetThemes.ts`
- **内容**: 
  - Dark, Light, ReForma, Classicの各テーマについて、上記のタスク2-7を適用
  - `theme_tokens`の値を`custom_style_config`に移行
- **実装状況**: ✅ 実装済み（全テーマで移行完了、`borderWidth`も追加済み）

## 進捗状況

- **全体進捗**: 8/8 タスク完了（100%）
- **最終更新**: 2026-01-23
- **完了タスク**: 
  - ✅ タスク1（型定義確認）
  - ⚠️ タスク2（radius - classで対応済みのため不要）
  - ✅ タスク3（font_family）
  - ✅ タスク4（spacing_scale）
  - ✅ タスク5（button_style）
  - ✅ タスク6（input_style）
  - ✅ タスク7（color_secondary）
  - ✅ タスク8（全テーマ更新）

## 実装完了内容（2026-01-23）

### ✅ タスク3: font_family を container に追加
- 全テーマ（Dark, Light, ReForma, Classic）で`container.style.fontFamily`に`'system-ui, -apple-system, sans-serif'`を設定

### ✅ タスク4: spacing_scale をグローバルCSSに反映
- 全テーマで`globalCss`にCSS変数として定義:
  - Dark/Light/ReForma: `:root { --spacing-scale: 1rem; }`（`spacing_scale: 'md'`）
  - Classic: `:root { --spacing-scale: 0.5rem; }`（`spacing_scale: 'sm'`）

### ✅ タスク5: button_style を buttonPrimary に反映
- Classicテーマで`button_style: 'outline'`に対応:
  - `backgroundColor: 'transparent'`
  - `borderColor: '#6b7280'`
  - `borderWidth: '1px'`（追加）

### ✅ タスク6: input_style を input に反映
- Light, ReForma, Classicテーマで`input_style: 'standard'`に対応:
  - `backgroundColor: 'transparent'`
  - `borderColor`を設定
  - `borderWidth: '1px'`（追加）

### ✅ タスク7: color_secondary を buttonSecondary に追加
- 全テーマで`buttonSecondary.style.backgroundColor`に`#6c757d`を設定
- Classicテーマでは`borderColor`にも設定（outlineスタイル）

### ✅ タスク8: 各プリセットテーマの custom_style_config を更新
- Dark, Light, ReForma, Classicの全テーマで上記のタスク3-7を適用
- `presetThemes.ts`と`ThemeSeeder.php`の両方を更新し、同期を完了

## 実装詳細

### radius の適用例

```php
// Dark テーマ
'card' => [
    'style' => [
        'backgroundColor' => 'rgba(15, 23, 42, 0.4)',
        'borderColor' => 'rgba(255, 255, 255, 0.1)',
        'borderRadius' => '4px', // theme_tokens.radius = '4'
    ],
],
'buttonPrimary' => [
    'style' => [
        'backgroundColor' => '#ffffff',
        'color' => '#0f172a',
        'borderRadius' => '4px', // theme_tokens.radius = '4'
    ],
],
'input' => [
    'style' => [
        'backgroundColor' => 'rgba(15, 23, 42, 0.6)',
        'color' => '#f1f5f9',
        'borderColor' => 'rgba(255, 255, 255, 0.1)',
        'borderRadius' => '4px', // theme_tokens.radius = '4'
    ],
],
```

### font_family の適用例

```php
'container' => [
    'style' => [
        'backgroundColor' => '#020617',
        'color' => '#f1f5f9',
        'fontFamily' => 'system-ui, -apple-system, sans-serif', // theme_tokens.font_family = 'system'
    ],
],
```

### spacing_scale の適用例（globalCss使用）

```php
'globalCss' => ':root { --spacing-scale: 1rem; }', // theme_tokens.spacing_scale = 'md'
```

または各要素に直接適用：

```php
'card' => [
    'style' => [
        'padding' => '1rem', // theme_tokens.spacing_scale = 'md'
    ],
],
```

### button_style の適用例

```php
// 'solid' の場合（既存）
'buttonPrimary' => [
    'style' => [
        'backgroundColor' => '#ffffff',
        'color' => '#0f172a',
    ],
],

// 'outline' の場合（Classicテーマ）
'buttonPrimary' => [
    'style' => [
        'backgroundColor' => 'transparent',
        'color' => '#6b7280',
        'borderColor' => '#6b7280',
        'borderWidth' => '1px',
    ],
],
```

### input_style の適用例

```php
// 'filled' の場合（Darkテーマ）
'input' => [
    'style' => [
        'backgroundColor' => 'rgba(15, 23, 42, 0.6)',
        'color' => '#f1f5f9',
        'borderColor' => 'rgba(255, 255, 255, 0.1)',
    ],
],

// 'standard' の場合（Light, ReForma, Classicテーマ）
'input' => [
    'style' => [
        'backgroundColor' => 'transparent',
        'color' => '#0f172a',
        'borderColor' => '#cbd5e1',
        'borderWidth' => '1px',
    ],
],
```

## 注意点

1. **後方互換性**
   - 既存のフォームで`theme_tokens`を使用している場合、`custom_style_config`が存在しない場合は`theme_tokens`を適用するロジックは維持する必要がある
   - ただし、今後は`custom_style_config`のみを使用する方向

2. **値の変換**
   - `radius`: 文字列（'0', '4', '8'）→ CSS値（'0px', '4px', '8px'）
   - `font_family`: 'system' → 'system-ui, -apple-system, sans-serif'

3. **spacing_scale の扱い**
   - グローバルCSS変数として定義するか、各要素に直接適用するか検討が必要
   - 現時点では、グローバルCSS変数として定義する方が柔軟性が高い

4. **button_style と input_style**
   - これらの値に基づいて、既存のスタイルを調整する必要がある
   - `button_style: 'outline'`の場合は、背景色を`transparent`にし、ボーダーを設定

## 実装順序の推奨

1. **タスク1**: 型定義の確認（必要に応じて拡張）
2. **タスク2-7**: 各プロパティの移行ロジックを実装
3. **タスク8**: 各プリセットテーマの`custom_style_config`を更新
