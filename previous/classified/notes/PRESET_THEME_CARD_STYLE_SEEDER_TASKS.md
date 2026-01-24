# プリセットテーマのカードスタイル初期値設定タスク

## 概要

プリセットテーマ（ダーク/ライト/classic）のSeederに、管理画面のスタイル（`uiTokens.card`）を参考にしたカードスタイルの初期値を設定します。

## 現状確認（2026-01-20更新）

### 現在のSeederの設定状況

#### ✅ ReFormaテーマ
- **ファイル**: `database/seeders/ThemeSeeder.php`
- **行数**: 203-209行目
- **cardスタイル**: 設定済み
  ```php
  'card' => [
      'style' => [
          'backgroundColor' => '#0b0c10',
          'borderColor' => 'rgba(255, 255, 255, 0.1)',
          'borderRadius' => '8px',
      ],
  ],
```

#### ⚠️ ダークテーマ
- **ファイル**: `database/seeders/ThemeSeeder.php`
- **行数**: 48-54行目
- **cardスタイル**: 設定済みだが、管理画面のスタイルと比較が必要
  ```php
  'card' => [
      'style' => [
          'backgroundColor' => 'rgba(15, 23, 42, 0.4)',
          'borderColor' => 'rgba(255, 255, 255, 0.1)',
          'borderRadius' => '4px',
      ],
  ],
```

#### ⚠️ ライトテーマ
- **ファイル**: `database/seeders/ThemeSeeder.php`
- **行数**: 125-131行目
- **cardスタイル**: 設定済みだが、管理画面のスタイルと比較が必要
  ```php
  'card' => [
      'style' => [
          'backgroundColor' => '#ffffff',
          'borderColor' => '#e2e8f0',
          'borderRadius' => '4px',
      ],
  ],
```

#### ⚠️ Classicテーマ
- **ファイル**: `database/seeders/ThemeSeeder.php`
- **行数**: 281-287行目
- **cardスタイル**: 設定済みだが、管理画面のスタイルと比較が必要
  ```php
  'card' => [
      'style' => [
          'backgroundColor' => '#ffffff',
          'borderColor' => '#e5e7eb',
          'borderRadius' => '0px',
      ],
  ],
```

### 管理画面のスタイル（uiTokens.card）

**ファイル**: `src/ui/theme/tokens.ts`（24-25行目）

```typescript
card: "bg-white text-slate-900 border border-slate-200 shadow-sm 
       dark:bg-slate-900/40 dark:text-slate-100 dark:border-white/10 
       group-data-[theme=reforma]:bg-[#0b0c10] group-data-[theme=reforma]:text-slate-100 
       group-data-[theme=reforma]:border-white/10"
```

#### スタイルの詳細

1. **ライトモード**:
   - `bg-white`: 背景色 `#ffffff`
   - `text-slate-900`: 文字色 `#0f172a`
   - `border border-slate-200`: ボーダー色 `#e2e8f0`
   - `shadow-sm`: 影（Tailwindの`shadow-sm`）

2. **ダークモード**:
   - `dark:bg-slate-900/40`: 背景色 `rgba(15, 23, 42, 0.4)` = `#0f172a`の40%透明度
   - `dark:text-slate-100`: 文字色 `#f1f5f9`
   - `dark:border-white/10`: ボーダー色 `rgba(255, 255, 255, 0.1)`

3. **ReFormaテーマ**:
   - `group-data-[theme=reforma]:bg-[#0b0c10]`: 背景色 `#0b0c10`
   - `group-data-[theme=reforma]:text-slate-100`: 文字色 `#f1f5f9`
   - `group-data-[theme=reforma]:border-white/10`: ボーダー色 `rgba(255, 255, 255, 0.1)`

### 現状の問題点

1. **ダークテーマ**:
   - ✅ `backgroundColor`: `rgba(15, 23, 42, 0.4)` = `dark:bg-slate-900/40`と一致
   - ✅ `borderColor`: `rgba(255, 255, 255, 0.1)` = `dark:border-white/10`と一致
   - ⚠️ `color`（文字色）が設定されていない → `dark:text-slate-100` = `#f1f5f9`を追加すべき
   - ⚠️ `boxShadow`が設定されていない → `shadow-sm`を追加すべき（オプション）

2. **ライトテーマ**:
   - ✅ `backgroundColor`: `#ffffff` = `bg-white`と一致
   - ✅ `borderColor`: `#e2e8f0` = `border-slate-200`と一致
   - ⚠️ `color`（文字色）が設定されていない → `text-slate-900` = `#0f172a`を追加すべき
   - ⚠️ `boxShadow`が設定されていない → `shadow-sm`を追加すべき（オプション）

3. **Classicテーマ**:
   - ✅ `backgroundColor`: `#ffffff` = `bg-white`と一致
   - ⚠️ `borderColor`: `#e5e7eb` = `gray-200`（`slate-200` = `#e2e8f0`に近いが、統一すべきか検討）
   - ⚠️ `color`（文字色）が設定されていない → `text-slate-900` = `#0f172a`を追加すべき
   - ⚠️ `boxShadow`が設定されていない → Classicテーマは`shadow-sm`なしかもしれない（確認が必要）

## タスクリスト（細分化版）

### タスク1: ダークテーマのカードスタイル初期値を改善

#### タスク1-1: 管理画面のスタイルと比較
- **ファイル**: `database/seeders/ThemeSeeder.php`
- **確認箇所**: 48-54行目
- **確認内容**:
  - [ ] 現在の`backgroundColor`が`dark:bg-slate-900/40`と一致しているか確認
  - [ ] 現在の`borderColor`が`dark:border-white/10`と一致しているか確認
  - [ ] `color`（文字色）が設定されているか確認 → ⚠️ 未設定
  - [ ] `boxShadow`が設定されているか確認 → ⚠️ 未設定（オプション）

#### タスク1-2: ダークテーマのカードスタイルを更新
- **ファイル**: `database/seeders/ThemeSeeder.php`
- **修正箇所**: 48-54行目
- **修正内容**:
  - [ ] `color`（文字色）を追加: `#f1f5f9`（`dark:text-slate-100`に相当）
  - [ ] `boxShadow`を追加: `0 1px 2px 0 rgb(0 0 0 / 0.05)`（`shadow-sm`に相当、オプション）
  - [ ] 既存の`backgroundColor`と`borderColor`は維持

---

### タスク2: ライトテーマのカードスタイル初期値を改善

#### タスク2-1: 管理画面のスタイルと比較
- **ファイル**: `database/seeders/ThemeSeeder.php`
- **確認箇所**: 125-131行目
- **確認内容**:
  - [ ] 現在の`backgroundColor`が`bg-white`と一致しているか確認
  - [ ] 現在の`borderColor`が`border-slate-200`と一致しているか確認
  - [ ] `color`（文字色）が設定されているか確認 → ⚠️ 未設定
  - [ ] `boxShadow`が設定されているか確認 → ⚠️ 未設定（オプション）

#### タスク2-2: ライトテーマのカードスタイルを更新
- **ファイル**: `database/seeders/ThemeSeeder.php`
- **修正箇所**: 125-131行目
- **修正内容**:
  - [ ] `color`（文字色）を追加: `#0f172a`（`text-slate-900`に相当）
  - [ ] `boxShadow`を追加: `0 1px 2px 0 rgb(0 0 0 / 0.05)`（`shadow-sm`に相当、オプション）
  - [ ] 既存の`backgroundColor`と`borderColor`は維持

---

### タスク3: Classicテーマのカードスタイル初期値を改善

#### タスク3-1: 管理画面のスタイルと比較
- **ファイル**: `database/seeders/ThemeSeeder.php`
- **確認箇所**: 281-287行目
- **確認内容**:
  - [ ] 現在の`backgroundColor`が`bg-white`と一致しているか確認
  - [ ] 現在の`borderColor`が`border-slate-200`と一致しているか確認 → ⚠️ `#e5e7eb`（`gray-200`）を使用、`#e2e8f0`（`slate-200`）に統一すべきか検討
  - [ ] `color`（文字色）が設定されているか確認 → ⚠️ 未設定
  - [ ] `boxShadow`が設定されているか確認 → ⚠️ 未設定（Classicテーマはフラットデザインなので、`shadow-sm`なしが適切かもしれない）

#### タスク3-2: Classicテーマのカードスタイルを更新
- **ファイル**: `database/seeders/ThemeSeeder.php`
- **修正箇所**: 281-287行目
- **修正内容**:
  - [ ] `color`（文字色）を追加: `#0f172a`（`text-slate-900`に相当）
  - [ ] `borderColor`を`#e2e8f0`（`slate-200`）に統一するか検討
  - [ ] `boxShadow`は追加しない（Classicテーマはフラットデザインのため）
  - [ ] 既存の`backgroundColor`と`borderRadius`は維持

---

### タスク4: ReFormaテーマの確認（参考）

#### タスク4-1: ReFormaテーマのカードスタイルを確認
- **ファイル**: `database/seeders/ThemeSeeder.php`
- **確認箇所**: 203-209行目
- **確認内容**:
  - [ ] 現在の`backgroundColor`が`group-data-[theme=reforma]:bg-[#0b0c10]`と一致しているか確認
  - [ ] 現在の`borderColor`が`group-data-[theme=reforma]:border-white/10`と一致しているか確認
  - [ ] `color`（文字色）が設定されているか確認 → ⚠️ 未設定（`group-data-[theme=reforma]:text-slate-100` = `#f1f5f9`を追加すべき）
  - [ ] `boxShadow`が設定されているか確認 → ⚠️ 未設定（オプション）

#### タスク4-2: ReFormaテーマのカードスタイルを更新（オプション）
- **ファイル**: `database/seeders/ThemeSeeder.php`
- **修正箇所**: 203-209行目
- **修正内容**:
  - [ ] `color`（文字色）を追加: `#f1f5f9`（`group-data-[theme=reforma]:text-slate-100`に相当）
  - [ ] 既存の`backgroundColor`と`borderColor`は維持

---

### タスク5: 動作確認

#### タスク5-1: Seeder実行後の確認
- **確認項目**:
  - [ ] Seederを実行して、各プリセットテーマが正しく作成される
  - [ ] カードスタイルの初期値が正しく設定されている
  - [ ] 管理画面のスタイルと一致している

#### タスク5-2: フォーム表示での確認
- **確認項目**:
  - [ ] ダークテーマでカードのスタイルが正しく適用される
  - [ ] ライトテーマでカードのスタイルが正しく適用される
  - [ ] Classicテーマでカードのスタイルが正しく適用される
  - [ ] ReFormaテーマでカードのスタイルが正しく適用される

## 実装詳細

### カラー値の対応表

| Tailwindクラス | カラー値 | 16進数 |
|---------------|---------|--------|
| `bg-white` | 白 | `#ffffff` |
| `text-slate-900` | 濃いグレー | `#0f172a` |
| `text-slate-100` | 薄いグレー | `#f1f5f9` |
| `border-slate-200` | グレーボーダー | `#e2e8f0` |
| `bg-slate-900/40` | 濃いグレー（40%透明度） | `rgba(15, 23, 42, 0.4)` |
| `border-white/10` | 白（10%透明度） | `rgba(255, 255, 255, 0.1)` |

### shadow-smの値

Tailwindの`shadow-sm`は以下のCSSに相当します：
```css
box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
```

### 修正例

#### ダークテーマの修正例

```php
'card' => [
    'style' => [
        'backgroundColor' => 'rgba(15, 23, 42, 0.4)',  // dark:bg-slate-900/40
        'color' => '#f1f5f9',                          // dark:text-slate-100（追加）
        'borderColor' => 'rgba(255, 255, 255, 0.1)',   // dark:border-white/10
        'borderRadius' => '4px',
        'boxShadow' => '0 1px 2px 0 rgb(0 0 0 / 0.05)', // shadow-sm（追加、オプション）
    ],
],
```

#### ライトテーマの修正例

```php
'card' => [
    'style' => [
        'backgroundColor' => '#ffffff',                 // bg-white
        'color' => '#0f172a',                          // text-slate-900（追加）
        'borderColor' => '#e2e8f0',                    // border-slate-200
        'borderRadius' => '4px',
        'boxShadow' => '0 1px 2px 0 rgb(0 0 0 / 0.05)', // shadow-sm（追加、オプション）
    ],
],
```

#### Classicテーマの修正例

```php
'card' => [
    'style' => [
        'backgroundColor' => '#ffffff',                 // bg-white
        'color' => '#0f172a',                          // text-slate-900（追加）
        'borderColor' => '#e2e8f0',                    // border-slate-200（統一）
        'borderRadius' => '0px',
        // boxShadowは追加しない（フラットデザイン）
    ],
],
```

#### ReFormaテーマの修正例（オプション）

```php
'card' => [
    'style' => [
        'backgroundColor' => '#0b0c10',                // group-data-[theme=reforma]:bg-[#0b0c10]
        'color' => '#f1f5f9',                          // group-data-[theme=reforma]:text-slate-100（追加）
        'borderColor' => 'rgba(255, 255, 255, 0.1)',   // group-data-[theme=reforma]:border-white/10
        'borderRadius' => '8px',
    ],
],
```

## 注意点

1. **boxShadowについて**:
   - `shadow-sm`は軽量な影で、カードに立体感を与える
   - Classicテーマはフラットデザインなので、`boxShadow`は追加しない
   - ダーク/ライト/ReFormaテーマには追加を推奨

2. **borderColorの統一**:
   - Classicテーマは現在`#e5e7eb`（`gray-200`）を使用しているが、`#e2e8f0`（`slate-200`）に統一することで、管理画面のスタイルと一致する

3. **color（文字色）の追加**:
   - 現在、すべてのテーマで`color`が設定されていない
   - 管理画面のスタイル（`uiTokens.card`）には文字色が含まれているため、追加すべき

4. **後方互換性**:
   - 既存のデータベースに影響を与えないよう、Seederの実行時に既存データを削除している
   - 新しい初期値は新規作成時のみ適用される

## 実装順序の推奨

1. **タスク1**: ダークテーマのカードスタイルを更新
2. **タスク2**: ライトテーマのカードスタイルを更新
3. **タスク3**: Classicテーマのカードスタイルを更新
4. **タスク4**: ReFormaテーマのカードスタイルを更新（オプション）
5. **タスク5**: 動作確認

## 進捗状況

- **全体進捗**: 5/5 タスク完了（100%）
- **最終更新**: 2026-01-23
- **完了タスク**: タスク1（ダークテーマ）、タスク2（ライトテーマ）、タスク3（Classicテーマ）、タスク4（ReFormaテーマ）、タスク5（動作確認）
- **進行中タスク**: なし
- **未着手タスク**: なし

## 実装完了内容（2026-01-20）

### ✅ タスク1: ダークテーマのカードスタイル初期値を改善
- `color`を追加: `#f1f5f9`（`dark:text-slate-100`に相当）
- `boxShadow`を追加: `0 1px 2px 0 rgb(0 0 0 / 0.05)`（`shadow-sm`に相当）

### ✅ タスク2: ライトテーマのカードスタイル初期値を改善
- `color`を追加: `#0f172a`（`text-slate-900`に相当）
- `boxShadow`を追加: `0 1px 2px 0 rgb(0 0 0 / 0.05)`（`shadow-sm`に相当）

### ✅ タスク3: Classicテーマのカードスタイル初期値を改善
- `color`を追加: `#0f172a`（`text-slate-900`に相当）
- `borderColor`を`#e2e8f0`（`slate-200`）に統一
- `boxShadow`は追加しない（フラットデザインのため）

### ✅ タスク4: ReFormaテーマのカードスタイルを更新
- `color`を追加: `#f1f5f9`（`group-data-[theme=reforma]:text-slate-100`に相当）
