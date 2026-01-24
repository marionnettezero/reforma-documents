# Phase 1: プリセットテーマ機能実装タスク

## 現状確認

### バックエンド側

1. **themesテーブル構造**
   - `id`: 主キー
   - `code`: テーマコード（ユニーク）
   - `name`: テーマ名
   - `description`: 説明
   - `theme_tokens`: JSON（既存のテーマトークン）
   - `is_preset`: boolean（プリセットテーマかどうか）
   - `is_active`: boolean（有効かどうか）
   - `created_by`: 作成者ID

2. **formsテーブル構造**
   - `theme_id`: テーマID（外部キー）
   - `theme_tokens`: JSON（フォーム固有のカスタマイズ）

3. **既存のThemeSeeder**
   - `default`: デフォルトテーマ
   - `dark`: ダークテーマ
   - `minimal`: ミニマルテーマ

4. **テーマ解決ロジック（resolveThemeData）**
   - `theme_tokens`が指定されている場合、フォーム固有のカスタムテーマとして使用
   - `theme_id`が指定されている場合、指定されたテーマのトークンを使用
   - 両方NULLの場合、デフォルトテーマ（code="default"）を使用

### フロントエンド側

1. **FormThemeSectionコンポーネント**
   - テーマ選択（select）
   - テーマトークン編集（textarea、JSON形式）

2. **FormEditIntegratedPage**
   - `formThemeId`: テーマID
   - `formThemeTokens`: テーマトークン

## 実装方針

### 1. データ構造

- **themesテーブル**: `custom_style_config`カラムを追加（プリセットテーマのスタイル設定を保存）
- **formsテーブル**: `custom_style_config`カラムを追加（フォーム固有のスタイル設定を保存）
- **プリセットテーマ**: `code`で識別（"dark", "light", "reforma", "classic"）

### 2. プリセットテーマの適用方法

- フォーム編集画面でプリセットテーマを選択
- 選択時に、該当テーマの`custom_style_config`をフォームの`custom_style_config`にコピー
- フォーム固有のカスタマイズは`forms.custom_style_config`に保存

### 3. 既存テーマ機能との関係

- **既存の`theme_id`と`theme_tokens`は維持**（後方互換性のため）
- 新しい`custom_style_config`は既存機能と併用可能
- 将来的に`theme_tokens`を`custom_style_config`に移行する可能性があるが、Phase 1では併用

## タスクリスト

**全タスク完了 ✅** (18/18)

### バックエンド側

#### タスク1: データベースマイグレーション - formsテーブルにcustom_style_configを追加 ✅
- **ファイル**: `database/migrations/xxxx_add_custom_style_config_to_forms_table.php`
- **内容**: 
  - `custom_style_config` JSONカラムを追加（nullable）
  - `theme_tokens`の後に配置
- **確認事項**: 既存データへの影響なし（nullable）
- **状態**: 完了（2026_01_21_234945_add_custom_style_config_to_forms_table.php）

#### タスク2: データベースマイグレーション - themesテーブルにcustom_style_configを追加 ✅
- **ファイル**: `database/migrations/xxxx_add_custom_style_config_to_themes_table.php`
- **内容**: 
  - `custom_style_config` JSONカラムを追加（nullable）
  - プリセットテーマのスタイル設定を保存
- **確認事項**: 既存データへの影響なし（nullable）
- **状態**: 完了（2026_01_21_234958_add_custom_style_config_to_themes_table.php）

#### タスク3: Formモデルの更新 ✅
- **ファイル**: `app/Models/Form.php`
- **内容**: 
  - `fillable`に`custom_style_config`を追加
  - `casts`に`'custom_style_config' => 'array'`を追加
- **状態**: 完了

#### タスク4: Themeモデルの更新 ✅
- **ファイル**: `app/Models/Theme.php`
- **内容**: 
  - `fillable`に`custom_style_config`を追加
  - `casts`に`'custom_style_config' => 'array'`を追加
- **状態**: 完了

#### タスク5: ThemeSeederの更新 - 4つのプリセットテーマを追加 ✅
- **ファイル**: `database/seeders/ThemeSeeder.php`
- **内容**: 
  - 既存の`default`, `dark`, `minimal`は維持（`custom_style_config`は後で追加可能）
  - 新しいプリセットテーマを追加：
    - `light`: ライトテーマ（`custom_style_config`を含む）
    - `reforma`: ReFormaテーマ（`custom_style_config`を含む）
    - `classic`: クラッシックテーマ（フラット、`custom_style_config`を含む）
  - 既存の`dark`テーマにも`custom_style_config`を追加（または新規作成）
  - 各テーマに`custom_style_config`を設定
  - `is_preset`を`true`に設定
- **注意**: 
  - 既存の`dark`テーマの`code`は維持（`updateOrCreate`で更新）
  - プリセットテーマの`code`は固定（"dark", "light", "reforma", "classic"）
  - `custom_style_config`の構造は提案書に準拠
- **状態**: 完了（4つのテーマにcustom_style_configが設定済み）

#### タスク6: FormsController - resolveThemeDataメソッドの拡張 ✅
- **ファイル**: `app/Http/Controllers/Api/V1/FormsController.php`
- **内容**: 
  - `resolveThemeData`メソッドを拡張して`custom_style_config`も返却
  - フォームの`custom_style_config`が優先、なければテーマの`custom_style_config`を使用
  - 戻り値に`custom_style_config`を追加
- **状態**: 完了

#### タスク7: FormsController - APIレスポンスにcustom_style_configを追加 ✅
- **ファイル**: `app/Http/Controllers/Api/V1/FormsController.php`
- **内容**: 
  - `show`メソッドのレスポンスに`custom_style_config`を追加
  - `update`メソッドのレスポンスに`custom_style_config`を追加
  - `resolveThemeData`から取得した`custom_style_config`を使用
- **状態**: 完了

#### タスク8: FormsController - フォーム更新時にcustom_style_configを保存 ✅
- **ファイル**: `app/Http/Controllers/Api/V1/FormsController.php`
- **内容**: 
  - `update`メソッドで`custom_style_config`を受け取り、保存
  - バリデーションルールに`custom_style_config`を追加（array, nullable）
  - バリデーションは最小限（基本的な構造チェックのみ）
- **状態**: 完了

#### タスク9: PublicFormsController - resolveThemeDataメソッドの拡張 ✅
- **ファイル**: `app/Http/Controllers/Api/V1/PublicFormsController.php`
- **内容**: 
  - `resolveThemeData`メソッドを拡張して`custom_style_config`も返却
  - フォームの`custom_style_config`が優先、なければテーマの`custom_style_config`を使用
- **状態**: 完了

#### タスク10: PublicFormsController - 公開フォームAPIレスポンスにcustom_style_configを追加 ✅
- **ファイル**: `app/Http/Controllers/Api/V1/PublicFormsController.php`
- **内容**: 
  - `show`メソッドのレスポンスに`custom_style_config`を追加
  - `resolveThemeData`から取得した`custom_style_config`を使用
- **状態**: 完了

### フロントエンド側

**全タスク完了 ✅** (8/8)

#### タスク11: CustomStyleConfig型定義の作成 ✅
- **ファイル**: `src/types/customStyle.ts`（新規作成）
- **内容**: 
  - `CustomStyleConfig`インターフェース
  - `ElementStyleConfig`インターフェース
  - 提案書の型定義を実装
- **状態**: 完了

#### タスク12: プリセットテーマ定義の作成 ✅
- **ファイル**: `src/constants/presetThemes.ts`（新規作成）
- **内容**: 
  - `PRESET_THEMES`定数
  - 4つのプリセットテーマ（dark, light, reforma, classic）の`custom_style_config`を定義
  - 各テーマのスタイル設定を詳細に記述
- **状態**: 完了

#### タスク13: FormEditIntegratedPage - プリセットテーマ選択UIの追加 ✅
- **ファイル**: `src/pages/forms/FormEditIntegratedPage.tsx`
- **内容**: 
  - `customStyleConfig`のstateを追加
  - プリセットテーマ選択UI（ラジオボタン）を追加
  - 既存の`FormThemeSection`を置き換えまたは拡張
  - プリセットテーマ選択時に`custom_style_config`を適用
- **状態**: 完了

#### タスク14: FormEditIntegratedPage - フォーム保存時にcustom_style_configを送信 ✅
- **ファイル**: `src/pages/forms/FormEditIntegratedPage.tsx`
- **内容**: 
  - `handleSaveForm`で`custom_style_config`を送信
  - APIリクエストに`custom_style_config`を含める
- **状態**: 完了

#### タスク15: FormEditIntegratedPage - フォーム取得時にcustom_style_configを読み込み ✅
- **ファイル**: `src/pages/forms/FormEditIntegratedPage.tsx`
- **内容**: 
  - `fetchFormDetail`で`custom_style_config`を取得
  - stateに設定
- **状態**: 完了

#### タスク16: PublicFormViewPage - custom_style_config適用ロジックの実装 ✅
- **ファイル**: `src/pages/public/PublicFormViewPage.tsx`
- **内容**: 
  - `custom_style_config`を取得
  - 各要素にスタイルを適用するロジックを実装
  - 既存の`theme_tokens`と併用
- **状態**: 完了

#### タスク17: FormRealtimePreview - custom_style_config適用ロジックの実装 ✅
- **ファイル**: `src/components/forms/FormRealtimePreview.tsx`
- **内容**: 
  - `custom_style_config`をpropsで受け取る
  - 各要素にスタイルを適用するロジックを実装
- **状態**: 完了

#### タスク18: カスタムスタイル適用ユーティリティの作成 ✅
- **ファイル**: `src/utils/customStyle.ts`（新規作成）
- **内容**: 
  - `applyElementStyle`関数
  - `applyGlobalCss`関数
  - 提案書の実装を参考
- **状態**: 完了

## 実装順序の推奨

1. **バックエンド側の基盤構築**（タスク1-10）
   - データベースマイグレーション（タスク1-2）
   - モデル更新（タスク3-4）
   - Seeder更新（タスク5）
   - API更新（タスク6-10）

2. **フロントエンド側の基盤構築**（タスク11-12, 18）
   - 型定義（タスク11）
   - プリセットテーマ定義（タスク12）
   - ユーティリティ関数（タスク18）

3. **フォーム編集画面の実装**（タスク13-15）
   - UI追加（タスク13）
   - 保存・読み込みロジック（タスク14-15）

4. **公開フォーム・プレビューの実装**（タスク16-17）
   - スタイル適用ロジック（タスク16-17）

## 注意点

1. **既存テーマ機能との併用**
   - `theme_id`と`theme_tokens`は維持
   - `custom_style_config`は新しい機能として追加
   - 将来的な移行を考慮

2. **プリセットテーマのcode**
   - `dark`, `light`, `reforma`, `classic`を使用
   - 既存の`dark`テーマとの競合を避ける（既存の`dark`を更新するか、新しいcodeを使用）

3. **バリデーション**
   - `custom_style_config`のバリデーションは最小限（基本的な構造チェックのみ）
   - 詳細なバリデーションはPhase 2以降で実装

4. **後方互換性**
   - 既存のフォームは`custom_style_config`がnullでも動作する
   - 既存の`theme_tokens`は引き続き使用可能
