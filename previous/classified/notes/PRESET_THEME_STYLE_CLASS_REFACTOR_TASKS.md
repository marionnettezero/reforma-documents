# プリセットテーマのスタイル/クラスリファクタリングタスク

## 概要

プリセットテーマ（dark / light / reforma）のスタイル設定を、管理画面で使用しているクラスをそのまま使用し、`style`はカラー系のみに制限します。また、テーマ一覧のテーマ作成/編集にカスタムスタイル編集機能を追加します。

## 現状確認（2026-01-20更新）

### 問題点

**現状の問題**:
- `className`を追加しても、`style`で`borderRadius`、`borderWidth`、`boxShadow`などを上書きしているため、画面が変わらない
- `style`の`borderRadius`が`className`の`rounded-2xl`を上書きしてしまう
- `style`の`borderWidth`が`className`の`border`を上書きしてしまう

**解決方針**:
- dark / light / reforma プリセットについては、管理画面で使っているクラス（`uiTokens.card`など）をそのままプリセットの`className`に入れる
- `style`はカラー系のみにする（`backgroundColor`、`color`、`borderColor`など）
- border系（`borderWidth`、`borderRadius`、`boxShadow`など）は`style`から削除し、`className`で管理

### 管理画面のクラス定義

**ファイル**: `src/ui/theme/tokens.ts`

#### card（24-25行目）
```typescript
card:
  "bg-white text-slate-900 border border-slate-200 shadow-sm dark:bg-slate-900/40 dark:text-slate-100 dark:border-white/10 group-data-[theme=reforma]:bg-[#0b0c10] group-data-[theme=reforma]:text-slate-100 group-data-[theme=reforma]:border-white/10",
```

**特徴**:
- `bg-white`: 背景色（ライト）
- `text-slate-900`: 文字色（ライト）
- `border border-slate-200`: ボーダー（ライト）
- `shadow-sm`: 影（ライト）
- `dark:bg-slate-900/40`: 背景色（ダーク）
- `dark:text-slate-100`: 文字色（ダーク）
- `dark:border-white/10`: ボーダー（ダーク）
- `group-data-[theme=reforma]:bg-[#0b0c10]`: 背景色（ReForma）
- `group-data-[theme=reforma]:text-slate-100`: 文字色（ReForma）
- `group-data-[theme=reforma]:border-white/10`: ボーダー（ReForma）

### 現在のプリセットテーマのカードスタイル

#### ダークテーマ（Seeder 48-57行目、PRESET_THEMES 22-32行目）
```php
'card' => [
    'className' => 'rounded-2xl shadow-soft border',
    'style' => [
        'backgroundColor' => 'rgba(15, 23, 42, 0.4)',
        'color' => '#f1f5f9',
        'borderColor' => 'rgba(255, 255, 255, 0.1)',
        'borderWidth' => '1px',        // ⚠️ 削除が必要
        'borderRadius' => '4px',       // ⚠️ 削除が必要
        'boxShadow' => '0 1px 2px 0 rgb(0 0 0 / 0.05)',  // ⚠️ 削除が必要
    ],
],
```

#### ライトテーマ（Seeder 133-142行目、PRESET_THEMES 88-98行目）
```php
'card' => [
    'className' => 'rounded-2xl shadow-soft border',
    'style' => [
        'backgroundColor' => '#ffffff',
        'color' => '#0f172a',
        'borderColor' => '#e2e8f0',
        'borderWidth' => '1px',        // ⚠️ 削除が必要
        'borderRadius' => '4px',       // ⚠️ 削除が必要
        'boxShadow' => '0 1px 2px 0 rgb(0 0 0 / 0.05)',  // ⚠️ 削除が必要
    ],
],
```

#### ReFormaテーマ（Seeder 218-227行目、PRESET_THEMES 154-163行目）
```php
'card' => [
    'className' => 'rounded-2xl shadow-soft border',
    'style' => [
        'backgroundColor' => '#0b0c10',
        'color' => '#f1f5f9',
        'borderColor' => 'rgba(255, 255, 255, 0.1)',
        'borderWidth' => '1px',        // ⚠️ 削除が必要
        'borderRadius' => '8px',       // ⚠️ 削除が必要
    ],
],
```

### テーマ一覧・作成・編集機能の現状

**ファイル**: `src/pages/system/ThemeListPage.tsx`

**確認済み**:
- ✅ テーマ一覧表示機能がある
- ✅ テーマ作成モーダルがある（701-790行目）
- ✅ テーマ編集モーダルがある（792-894行目）
- ✅ テーマ詳細モーダルがある（896-1020行目）
- ⚠️ 現在は`theme_tokens`のみ編集可能
- ⚠️ `custom_style_config`の編集機能がない

**カスタムスタイル編集UI（フォーム設定）**:
- ✅ フォーム設定でカスタムスタイル編集機能がある（`FormEditIntegratedPage.tsx` 2750行目付近）
- ✅ `formCustomStyleConfig`で`elements`と`globalCss`を編集できる
- ✅ ヘッダ/フッタ設定（`headerEnabled`、`footerEnabled`、`headerHtml`、`footerHtml`）がある
- ⚠️ テーマ作成・編集画面に同様の機能を追加する必要がある

**テーマAPIの現状**:
- ✅ テーマ作成API: `POST /v1/system/themes`（`CreateThemeReq`に`theme_tokens`のみ）
- ✅ テーマ更新API: `PUT /v1/system/themes/{id}`（`UpdateThemeReq`に`theme_tokens`のみ）
- ⚠️ `custom_style_config`の送受信が可能か確認が必要

## タスクリスト（細分化版）

### タスク1: プリセットテーマのスタイル/クラスリファクタリング

#### タスク1-1: ダークテーマのカードスタイルを修正
- **ファイル**: `database/seeders/ThemeSeeder.php`、`src/constants/presetThemes.ts`
- **修正内容**:
  - [ ] `className`を`uiTokens.card`のクラスに変更（`rounded-2xl shadow-soft`は不要、`uiTokens.card`に含まれる）
  - [ ] `style`から`borderWidth`、`borderRadius`、`boxShadow`を削除
  - [ ] `style`はカラー系のみ残す（`backgroundColor`、`color`、`borderColor`）
  - **注意**: `uiTokens.card`には`dark:`バリアントが含まれているため、ダークテーマではそのまま使用可能

#### タスク1-2: ライトテーマのカードスタイルを修正
- **ファイル**: `database/seeders/ThemeSeeder.php`、`src/constants/presetThemes.ts`
- **修正内容**:
  - [ ] `className`を`uiTokens.card`のクラスに変更（`rounded-2xl shadow-soft`は不要、`uiTokens.card`に含まれる）
  - [ ] `style`から`borderWidth`、`borderRadius`、`boxShadow`を削除
  - [ ] `style`はカラー系のみ残す（`backgroundColor`、`color`、`borderColor`）
  - **注意**: `uiTokens.card`にはライトテーマ用のクラスが含まれているため、そのまま使用可能

#### タスク1-3: ReFormaテーマのカードスタイルを修正
- **ファイル**: `database/seeders/ThemeSeeder.php`、`src/constants/presetThemes.ts`
- **修正内容**:
  - [ ] `className`を`uiTokens.card`のクラスに変更（`rounded-2xl shadow-soft`は不要、`uiTokens.card`に含まれる）
  - [ ] `style`から`borderWidth`、`borderRadius`を削除
  - [ ] `style`はカラー系のみ残す（`backgroundColor`、`color`、`borderColor`）
  - **注意**: `uiTokens.card`には`group-data-[theme=reforma]:`バリアントが含まれているため、ReFormaテーマではそのまま使用可能

#### タスク1-4: Classicテーマのカードスタイルを確認・調整
- **ファイル**: `database/seeders/ThemeSeeder.php`、`src/constants/presetThemes.ts`
- **確認内容**:
  - [ ] Classicテーマはフラットデザインのため、`uiTokens.card`は使用しない
  - [ ] `className: 'border'`は維持
  - [ ] `style`から`borderWidth`、`borderRadius`を削除（`border`クラスで管理）
  - [ ] `style`はカラー系のみ残す（`backgroundColor`、`color`、`borderColor`）

#### タスク1-5: 他の要素（buttonPrimary、buttonSecondary、input）も同様に修正
- **ファイル**: `database/seeders/ThemeSeeder.php`、`src/constants/presetThemes.ts`
- **確認内容**:
  - [ ] `uiTokens.buttonPrimary`、`uiTokens.buttonSecondary`、`uiTokens.input`を確認
  - [ ] 各要素の`style`から`borderWidth`、`borderRadius`、`boxShadow`を削除
  - [ ] `style`はカラー系のみ残す
  - [ ] `className`に`uiTokens`のクラスを追加（必要に応じて）

---

### タスク2: テーマ一覧のテーマ作成/編集にカスタムスタイル編集機能を追加

#### タスク2-1: テーマ作成/編集UIの確認 ✅
- **確認項目**:
  - [x] テーマ作成UIが存在するか確認 → ✅ `ThemeListPage.tsx` 701-790行目
  - [x] テーマ編集UIが存在するか確認 → ✅ `ThemeListPage.tsx` 792-894行目
  - [x] テーマ作成/編集のAPIエンドポイントを確認 → ✅ `POST /v1/system/themes`、`PUT /v1/system/themes/{id}`
  - [x] テーマ作成/編集のフォーム構造を確認 → ✅ `theme_tokens`のみ編集可能

#### タスク2-2: カスタムスタイル編集コンポーネントの確認
- **確認項目**:
  - [ ] フォーム設定のカスタムスタイル編集UIを確認（`FormEditIntegratedPage.tsx` 2750行目付近）
  - [ ] `elements`編集UIの構造を確認
  - [ ] `globalCss`編集UIの構造を確認
  - [ ] ヘッダ/フッタ設定UIの構造を確認
  - [ ] 再利用可能なコンポーネントとして抽出できるか確認

#### タスク2-3: テーマ作成/編集UIにカスタムスタイル編集を追加
- **ファイル**: `src/pages/system/ThemeListPage.tsx`
- **修正箇所**: 
  - 作成モーダル（701-790行目）
  - 編集モーダル（792-894行目）
- **修正内容**:
  - [ ] カスタムスタイル編集セクションを追加
  - [ ] `elements`編集UIを追加（フォーム設定と同様）
  - [ ] `globalCss`編集UIを追加（フォーム設定と同様）
  - [ ] ヘッダ/フッタ設定UIを追加（`headerEnabled`、`footerEnabled`、`headerHtml`、`footerHtml`）
  - [ ] テーマ保存時に`custom_style_config`を保存
  - [ ] フォーム状態に`formCustomStyleConfig`を追加

#### タスク2-4: バックエンドAPIの確認・修正
- **確認項目**:
  - [ ] テーマ作成API（`POST /v1/system/themes`）が`custom_style_config`を受け取れるか確認
  - [ ] テーマ更新API（`PUT /v1/system/themes/{id}`）が`custom_style_config`を受け取れるか確認
  - [ ] テーマ詳細API（`GET /v1/system/themes/{id}`）が`custom_style_config`を返すか確認
  - [ ] 必要に応じてAPIを修正
  - [ ] バックエンドのテーマモデル/コントローラーを確認

---

### タスク3: 動作確認

#### タスク3-1: プリセットテーマのスタイル適用確認
- **確認項目**:
  - [ ] ダークテーマでカードが正しく表示される（クラスが適用される）
  - [ ] ライトテーマでカードが正しく表示される（クラスが適用される）
  - [ ] ReFormaテーマでカードが正しく表示される（クラスが適用される）
  - [ ] Classicテーマでカードが正しく表示される（クラスが適用される）
  - [ ] `style`のカラー系が正しく適用される
  - [ ] `style`のborder系が削除され、クラスで管理されている

#### タスク3-2: テーマ作成/編集のカスタムスタイル編集確認
- **確認項目**:
  - [ ] テーマ作成時にカスタムスタイルを編集できる
  - [ ] テーマ編集時にカスタムスタイルを編集できる
  - [ ] `elements`の値を変更できる
  - [ ] `globalCss`の値を変更できる
  - [ ] 保存時に`custom_style_config`が正しく保存される

## 実装詳細

### 修正例

#### ダークテーマのカードスタイル修正例

**Seeder**:
```php
'card' => [
    'className' => 'bg-white text-slate-900 border border-slate-200 shadow-sm dark:bg-slate-900/40 dark:text-slate-100 dark:border-white/10 group-data-[theme=reforma]:bg-[#0b0c10] group-data-[theme=reforma]:text-slate-100 group-data-[theme=reforma]:border-white/10',
    'style' => [
        'backgroundColor' => 'rgba(15, 23, 42, 0.4)',  // カラー系のみ
        'color' => '#f1f5f9',                          // カラー系のみ
        'borderColor' => 'rgba(255, 255, 255, 0.1)',   // カラー系のみ
        // borderWidth, borderRadius, boxShadow は削除
    ],
],
```

**PRESET_THEMES定数**:
```typescript
card: {
  className: 'bg-white text-slate-900 border border-slate-200 shadow-sm dark:bg-slate-900/40 dark:text-slate-100 dark:border-white/10 group-data-[theme=reforma]:bg-[#0b0c10] group-data-[theme=reforma]:text-slate-100 group-data-[theme=reforma]:border-white/10',
  style: {
    backgroundColor: 'rgba(15, 23, 42, 0.4)',  // カラー系のみ
    color: '#f1f5f9',                          // カラー系のみ
    borderColor: 'rgba(255, 255, 255, 0.1)',   // カラー系のみ
    // borderWidth, borderRadius, boxShadow は削除
  },
},
```

**注意**: `uiTokens.card`のクラスをそのまま使用するため、`dark:`バリアントが自動的に適用されます。

#### ライトテーマのカードスタイル修正例

**Seeder**:
```php
'card' => [
    'className' => 'bg-white text-slate-900 border border-slate-200 shadow-sm dark:bg-slate-900/40 dark:text-slate-100 dark:border-white/10 group-data-[theme=reforma]:bg-[#0b0c10] group-data-[theme=reforma]:text-slate-100 group-data-[theme=reforma]:border-white/10',
    'style' => [
        'backgroundColor' => '#ffffff',  // カラー系のみ
        'color' => '#0f172a',            // カラー系のみ
        'borderColor' => '#e2e8f0',      // カラー系のみ
        // borderWidth, borderRadius, boxShadow は削除
    ],
],
```

#### ReFormaテーマのカードスタイル修正例

**Seeder**:
```php
'card' => [
    'className' => 'bg-white text-slate-900 border border-slate-200 shadow-sm dark:bg-slate-900/40 dark:text-slate-100 dark:border-white/10 group-data-[theme=reforma]:bg-[#0b0c10] group-data-[theme=reforma]:text-slate-100 group-data-[theme=reforma]:border-white/10',
    'style' => [
        'backgroundColor' => '#0b0c10',              // カラー系のみ
        'color' => '#f1f5f9',                        // カラー系のみ
        'borderColor' => 'rgba(255, 255, 255, 0.1)', // カラー系のみ
        // borderWidth, borderRadius は削除
    ],
],
```

**注意**: `uiTokens.card`には`group-data-[theme=reforma]:`バリアントが含まれているため、ReFormaテーマでは自動的に適用されます。

## 注意点

1. **クラスの適用順序**:
   - `className`でクラスを適用し、`style`でカラー系のみを上書き
   - `style`の`borderWidth`、`borderRadius`、`boxShadow`は削除し、クラスで管理

2. **uiTokens.cardの使用**:
   - `uiTokens.card`には`dark:`と`group-data-[theme=reforma]:`バリアントが含まれている
   - ダークテーマ、ライトテーマ、ReFormaテーマすべてで同じクラスを使用可能
   - テーマに応じて自動的に適切なスタイルが適用される

3. **Classicテーマ**:
   - Classicテーマはフラットデザインのため、`uiTokens.card`は使用しない
   - `className: 'border'`のみを使用
   - `style`はカラー系のみ

4. **後方互換性**:
   - 既存のフォームデータに影響を与えないよう注意
   - Seeder更新時は既存データを削除してから実行されるため、影響は限定的

5. **テーマ作成/編集UI**:
   - フォーム設定のカスタムスタイル編集UIを参考にする
   - `elements`と`globalCss`の編集機能を追加
   - テーマ保存時に`custom_style_config`を保存

## 実装順序の推奨

1. **タスク1**: プリセットテーマのスタイル/クラスリファクタリング（必須）
2. **タスク2**: テーマ一覧のテーマ作成/編集にカスタムスタイル編集機能を追加（必須）
3. **タスク3**: 動作確認（必須）

## 進捗状況

- **全体進捗**: 3/3 タスク完了（100%）
- **最終更新**: 2026-01-23
- **完了タスク**: 
  - ✅ タスク1（プリセットテーマリファクタリング）
  - ✅ タスク2（テーマ作成/編集UI追加）
  - ✅ タスク3（動作確認）
- **進行中タスク**: なし
- **未着手タスク**: なし

## 実装完了内容（2026-01-20）

### タスク1: プリセットテーマのスタイル/クラスリファクタリング ✅

#### タスク1-1: ダークテーマのカードスタイルを修正 ✅
- ✅ Seeder: `className`を`uiTokens.card`のクラスに変更、`style`から`borderWidth`、`borderRadius`、`boxShadow`を削除
- ✅ PRESET_THEMES定数: 同様の修正

#### タスク1-2: ライトテーマのカードスタイルを修正 ✅
- ✅ Seeder: `className`を`uiTokens.card`のクラスに変更、`style`から`borderWidth`、`borderRadius`、`boxShadow`を削除
- ✅ PRESET_THEMES定数: 同様の修正

#### タスク1-3: ReFormaテーマのカードスタイルを修正 ✅
- ✅ Seeder: `className`を`uiTokens.card`のクラスに変更、`style`から`borderWidth`、`borderRadius`を削除
- ✅ PRESET_THEMES定数: 同様の修正

#### タスク1-4: Classicテーマのカードスタイルを確認・調整 ✅
- ✅ Seeder: `style`から`borderWidth`、`borderRadius`を削除（`className: 'border'`は維持）
- ✅ PRESET_THEMES定数: 同様の修正

#### タスク1-5: 他の要素（buttonPrimary、buttonSecondary、input）も同様に修正 ✅
- ✅ Seeder: すべてのテーマで`className`に`uiTokens`のクラスを追加、`style`から`borderWidth`、`borderRadius`、`boxShadow`を削除
- ✅ PRESET_THEMES定数: 同様の修正
- ✅ Classicテーマは`className: 'border'`のみを使用

### タスク2: テーマ一覧のテーマ作成/編集にカスタムスタイル編集機能を追加 ✅

#### タスク2-1: テーマ作成/編集UIの確認 ✅
- ✅ テーマ作成UIが存在することを確認
- ✅ テーマ編集UIが存在することを確認
- ✅ APIエンドポイントを確認

#### タスク2-2: カスタムスタイル編集コンポーネントの確認 ✅
- ✅ `ElementStyleEditor`コンポーネントを確認
- ✅ `globalCss`編集UIの構造を確認
- ✅ ヘッダ/フッタ設定UIの構造を確認

#### タスク2-3: テーマ作成/編集UIにカスタムスタイル編集を追加 ✅
- ✅ 作成モーダルにカスタムスタイル編集セクションを追加
- ✅ 編集モーダルにカスタムスタイル編集セクションを追加
- ✅ `elements`編集UIを追加（container、card、buttonPrimary、buttonSecondary、input）
- ✅ `globalCss`編集UIを追加
- ✅ ヘッダ/フッタ設定UIを追加（`headerEnabled`、`footerEnabled`、`headerHtml`、`footerHtml`）
- ✅ フォーム状態に`formCustomStyleConfig`を追加
- ✅ テーマ保存時に`custom_style_config`を保存

#### タスク2-4: バックエンドAPIの確認・修正 ✅
- ✅ テーマ作成API（`POST /v1/system/themes`）に`custom_style_config`のバリデーションを追加
- ✅ テーマ更新API（`PUT /v1/system/themes/{id}`）に`custom_style_config`のバリデーションを追加
- ✅ テーマ詳細API（`GET /v1/system/themes/{id}`）が`custom_style_config`を返すように修正
- ✅ テーマ一覧API（`GET /v1/system/themes`）が`custom_style_config`を返すように修正
- ✅ テーマコピーAPI（`POST /v1/system/themes/{id}/copy`）が`custom_style_config`をコピーするように修正
