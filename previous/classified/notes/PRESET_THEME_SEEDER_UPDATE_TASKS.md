# プリセットテーマ Seeder データ修正タスク

## 概要

管理画面のテーマ設定を再現するように、プリセットテーマのSeederデータを修正します。

## 要件

1. **Dark**: 現在の管理画面のダークテーマを再現
2. **Light**: 現在の管理画面のライトテーマを再現
3. **ReForma**: 現在の管理画面のReFormaテーマを再現
4. **Classic**: カードスタイルを使用しないフラットな状態にし、一般的な配色にする
5. **ヘッダ領域/フッタ領域**: 各テーマのスタイルを適用

## 現状確認

### 管理画面のテーマ設定（tokens.tsより）

#### Light テーマ
- ページ背景: `bg-white` (#ffffff)
- テキスト: `text-slate-900` (#0f172a)
- カード背景: `bg-white` (#ffffff)
- カードボーダー: `border-slate-200` (#e2e8f0)
- ボタンPrimary: `bg-slate-900 text-white` (#0f172a / #ffffff)
- 入力: `bg-white border-slate-300` (#ffffff / #cbd5e1)

#### Dark テーマ
- ページ背景: `dark:bg-slate-950` (#020617)
- テキスト: `dark:text-slate-100` (#f1f5f9)
- カード背景: `dark:bg-slate-900/40` (rgba(15, 23, 42, 0.4))
- カードボーダー: `dark:border-white/10` (rgba(255, 255, 255, 0.1))
- ボタンPrimary: `dark:bg-white dark:text-slate-900` (#ffffff / #0f172a)
- 入力: `dark:bg-slate-900/60 dark:border-white/10` (rgba(15, 23, 42, 0.6) / rgba(255, 255, 255, 0.1))

#### ReForma テーマ
- ページ背景: `bg-transparent` (透明)
- テキスト: `text-slate-100` (#f1f5f9)
- カード背景: `bg-[#0b0c10]` (#0b0c10)
- カードボーダー: `border-white/10` (rgba(255, 255, 255, 0.1))
- ボタンPrimary: `bg-white/10 text-slate-100` (rgba(255, 255, 255, 0.1) / #f1f5f9)
- 入力: `bg-black border-white/10` (#000000 / rgba(255, 255, 255, 0.1))

### Tailwind Slate カラーパレット（参考値）
- slate-50: #f8fafc
- slate-100: #f1f5f9
- slate-200: #e2e8f0
- slate-300: #cbd5e1
- slate-400: #94a3b8
- slate-500: #64748b
- slate-600: #475569
- slate-700: #334155
- slate-800: #1e293b
- slate-900: #0f172a
- slate-950: #020617

## タスクリスト

### タスク1: Dark テーマの修正
- **ファイル**: `database/seeders/ThemeSeeder.php`
- **内容**: 
  - `theme_tokens`を管理画面のダークテーマに合わせて修正
    - `color_primary`: `#ffffff` (白、ボタン背景)
    - `color_bg`: `#020617` (slate-950)
    - `color_text`: `#f1f5f9` (slate-100)
  - `custom_style_config`の`elements`を修正
    - `container`: 背景色 `#020617`、文字色 `#f1f5f9`
    - `card`: 背景色 `rgba(15, 23, 42, 0.4)`、ボーダー色 `rgba(255, 255, 255, 0.1)`
    - `buttonPrimary`: 背景色 `#ffffff`、文字色 `#0f172a`
    - `input`: 背景色 `rgba(15, 23, 42, 0.6)`、文字色 `#f1f5f9`、ボーダー色 `rgba(255, 255, 255, 0.1)`
  - `header`と`footer`の要素を追加
    - `header`: 背景色 `rgba(2, 6, 23, 0.4)`、文字色 `#f1f5f9`、ボーダー色 `rgba(255, 255, 255, 0.1)`
    - `footer`: 背景色 `rgba(2, 6, 23, 0.4)`、文字色 `#f1f5f9`、ボーダー色 `rgba(255, 255, 255, 0.1)`

### タスク2: Light テーマの修正
- **ファイル**: `database/seeders/ThemeSeeder.php`
- **内容**: 
  - `theme_tokens`を管理画面のライトテーマに合わせて修正
    - `color_primary`: `#0f172a` (slate-900、ボタン背景)
    - `color_bg`: `#ffffff` (白)
    - `color_text`: `#0f172a` (slate-900)
  - `custom_style_config`の`elements`を修正
    - `container`: 背景色 `#ffffff`、文字色 `#0f172a`
    - `card`: 背景色 `#ffffff`、ボーダー色 `#e2e8f0`
    - `buttonPrimary`: 背景色 `#0f172a`、文字色 `#ffffff`
    - `input`: 背景色 `#ffffff`、文字色 `#0f172a`、ボーダー色 `#cbd5e1`
  - `header`と`footer`の要素を追加
    - `header`: 背景色 `rgba(255, 255, 255, 0.7)`、文字色 `#0f172a`、ボーダー色 `#e2e8f0`
    - `footer`: 背景色 `rgba(255, 255, 255, 0.7)`、文字色 `#0f172a`、ボーダー色 `#e2e8f0`

### タスク3: ReForma テーマの修正
- **ファイル**: `database/seeders/ThemeSeeder.php`
- **内容**: 
  - `theme_tokens`を管理画面のReFormaテーマに合わせて修正
    - `color_primary`: `rgba(255, 255, 255, 0.1)` (白10%、ボタン背景)
    - `color_bg`: `transparent` または `#000000` (透明または黒)
    - `color_text`: `#f1f5f9` (slate-100)
  - `custom_style_config`の`elements`を修正
    - `container`: 背景色 `transparent`、文字色 `#f1f5f9`
    - `card`: 背景色 `#0b0c10`、ボーダー色 `rgba(255, 255, 255, 0.1)`
    - `buttonPrimary`: 背景色 `rgba(255, 255, 255, 0.1)`、文字色 `#f1f5f9`
    - `input`: 背景色 `#000000`、文字色 `#f1f5f9`、ボーダー色 `rgba(255, 255, 255, 0.1)`
  - `header`と`footer`の要素を追加
    - `header`: 背景色 `rgba(0, 0, 0, 0.6)`、文字色 `#f1f5f9`、ボーダー色 `rgba(255, 255, 255, 0.1)`
    - `footer`: 背景色 `rgba(0, 0, 0, 0.6)`、文字色 `#f1f5f9`、ボーダー色 `rgba(255, 255, 255, 0.1)`

### タスク4: Classic テーマの修正
- **ファイル**: `database/seeders/ThemeSeeder.php`
- **内容**: 
  - カードスタイルを使用しないフラットな状態にする
  - 一般的な配色にする（白背景、黒文字、グレーのアクセント）
  - `theme_tokens`を修正
    - `color_primary`: `#6b7280` (gray-500、一般的なグレー)
    - `color_bg`: `#ffffff` (白)
    - `color_text`: `#1f2937` (gray-800)
    - `radius`: `0` (角丸なし)
  - `custom_style_config`の`elements`を修正
    - `container`: 背景色 `#ffffff`、文字色 `#1f2937`
    - `card`: 背景色 `#ffffff`、ボーダーなし（または薄いグレー）、`borderRadius: '0px'`
    - `buttonPrimary`: 背景色 `#6b7280`、文字色 `#ffffff`、`borderRadius: '0px'`
    - `input`: 背景色 `#ffffff`、文字色 `#1f2937`、ボーダー色 `#d1d5db`、`borderRadius: '0px'`
  - `header`と`footer`の要素を追加
    - `header`: 背景色 `#f9fafb`、文字色 `#1f2937`、ボーダー色 `#e5e7eb`
    - `footer`: 背景色 `#f9fafb`、文字色 `#1f2937`、ボーダー色 `#e5e7eb`

### タスク5: フロントエンドのpresetThemes.tsを同期
- **ファイル**: `src/constants/presetThemes.ts`
- **内容**: 
  - バックエンドのSeederデータと同期させる
  - 各テーマの`custom_style_config`をSeederと同じ値に更新
  - `header`と`footer`の要素を追加

## 注意点

1. **カラー値の形式**
   - 不透明度を含む場合は`rgba()`形式を使用
   - 完全な不透明度の場合は16進数形式（`#ffffff`）を使用

2. **ヘッダ/フッタ領域**
   - `custom_style_config.elements`に`header`と`footer`を追加
   - 各テーマのスタイルに合わせた背景色、文字色、ボーダー色を設定

3. **Classic テーマ**
   - カードスタイルを使用しない = カードの背景色とコンテナの背景色を同じにする
   - ボーダーを薄くするか、なしにする
   - 角丸を0にする

4. **バックエンドとフロントエンドの同期**
   - Seederを更新したら、フロントエンドの`presetThemes.ts`も同じ値に更新する必要がある

## 実装順序の推奨

1. **タスク1-4**: バックエンドのSeederデータを修正（Dark, Light, ReForma, Classic）
2. **タスク5**: フロントエンドのpresetThemes.tsを同期

## 進捗状況

- **全体進捗**: 5/5 タスク完了（100%）
- **最終更新**: 2026-01-23
- **完了タスク**: 
  - ✅ タスク1（Darkテーマの修正）
  - ✅ タスク2（Lightテーマの修正）
  - ✅ タスク3（ReFormaテーマの修正）
  - ✅ タスク4（Classicテーマの修正）
  - ✅ タスク5（フロントエンドのpresetThemes.tsを同期）
- **進行中タスク**: なし
- **未着手タスク**: なし

## 実装完了内容（2026-01-23）

### ✅ タスク1-4: バックエンドのSeederデータ修正
- Dark, Light, ReForma, Classicテーマすべてに`header`と`footer`の要素を追加
- `theme_tokens`を管理画面の設定に合わせて修正
- `custom_style_config`の`elements`を管理画面のスタイルに合わせて修正

### ✅ タスク5: フロントエンドのpresetThemes.tsを同期
- バックエンドのSeederデータと同期
- 各テーマの`custom_style_config`をSeederと同じ値に更新
- `header`と`footer`の要素を追加
