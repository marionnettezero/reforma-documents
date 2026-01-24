# プリセットテーマのButton/Input/Textareaスタイル同期タスク

## 概要

Seederで設定したButton、Input、Textareaのスタイル初期値をPRESET_THEMES定数と同期させます。管理画面のスタイル（`uiTokens`）も参考にしながら、不足している項目を追加します。

## 現状確認（2026-01-20更新）

### 管理画面のスタイル（uiTokens）

**ファイル**: `src/ui/theme/tokens.ts`

#### buttonPrimary（55-56行目）
```typescript
buttonPrimary: "inline-flex items-center justify-center rounded-xl px-4 py-2 text-sm font-semibold transition shadow-sm bg-slate-900 text-white hover:bg-slate-800 active:translate-y-px dark:bg-white dark:text-slate-900 dark:hover:bg-slate-100 group-data-[theme=reforma]:bg-white/10 group-data-[theme=reforma]:text-slate-100 group-data-[theme=reforma]:hover:bg-white/15"
```

**スタイルの詳細**:
- ライトモード: `bg-slate-900 text-white shadow-sm`
- ダークモード: `dark:bg-white dark:text-slate-900`
- ReFormaテーマ: `group-data-[theme=reforma]:bg-white/10 group-data-[theme=reforma]:text-slate-100`
- `shadow-sm`: 影（`0 1px 2px 0 rgb(0 0 0 / 0.05)`）
- `border`は明示的にない（デフォルトではborderなし）

#### buttonSecondary（58-59行目）
```typescript
buttonSecondary: "inline-flex items-center justify-center rounded-xl px-4 py-2 text-sm font-semibold transition border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 active:translate-y-px dark:border-white/10 dark:bg-slate-900/40 dark:text-slate-100 dark:hover:bg-slate-900/60 group-data-[theme=reforma]:border-white/10 group-data-[theme=reforma]:bg-white/5 group-data-[theme=reforma]:text-slate-100 group-data-[theme=reforma]:hover:bg-white/10"
```

**スタイルの詳細**:
- ライトモード: `border border-slate-300 bg-white text-slate-700`
- ダークモード: `dark:border-white/10 dark:bg-slate-900/40 dark:text-slate-100`
- ReFormaテーマ: `group-data-[theme=reforma]:border-white/10 group-data-[theme=reforma]:bg-white/5 group-data-[theme=reforma]:text-slate-100`
- `border border-slate-300`: ボーダー（`#cbd5e1`）
- `borderWidth`は明示的にない（デフォルトで1px）

#### input（51-52行目）
```typescript
input: "w-full rounded-xl border px-3 py-2 text-sm outline-none transition bg-white text-slate-900 placeholder-slate-400 border-slate-300 focus:ring-2 focus:ring-slate-400/30 focus:border-slate-400 dark:bg-slate-900/60 dark:text-slate-100 dark:placeholder-slate-400 dark:border-white/10 dark:focus:ring-white/15 dark:focus:border-white/20 group-data-[theme=reforma]:bg-black group-data-[theme=reforma]:text-slate-100 group-data-[theme=reforma]:placeholder-slate-500 group-data-[theme=reforma]:border-white/10 group-data-[theme=reforma]:focus:ring-white/15 group-data-[theme=reforma]:focus:border-white/20"
```

**スタイルの詳細**:
- ライトモード: `bg-white text-slate-900 border border-slate-300`
- ダークモード: `dark:bg-slate-900/60 dark:text-slate-100 dark:border-white/10`
- ReFormaテーマ: `group-data-[theme=reforma]:bg-black group-data-[theme=reforma]:text-slate-100 group-data-[theme=reforma]:border-white/10`
- `border border-slate-300`: ボーダー（`#cbd5e1`）
- `borderWidth`は明示的にない（デフォルトで1px）

### SeederとPRESET_THEMES定数の比較

#### ダークテーマ

**Seeder** (`ThemeSeeder.php` 57-78行目):
```php
'buttonPrimary' => [
    'style' => [
        'backgroundColor' => '#ffffff',
        'color' => '#0f172a',
        'borderRadius' => '4px',
    ],
],
'buttonSecondary' => [
    'style' => [
        'backgroundColor' => '#6c757d',
        'color' => '#ffffff',
        'borderRadius' => '4px',
    ],
],
'input' => [
    'style' => [
        'backgroundColor' => 'rgba(15, 23, 42, 0.6)',
        'color' => '#f1f5f9',
        'borderColor' => 'rgba(255, 255, 255, 0.1)',
        'borderRadius' => '4px',
    ],
],
```

**PRESET_THEMES** (`presetThemes.ts` 29-50行目):
```typescript
buttonPrimary: {
  style: {
    backgroundColor: '#ffffff',
    color: '#0f172a',
    borderRadius: '4px',
    // ⚠️ boxShadowが不足（shadow-sm）
  },
},
buttonSecondary: {
  style: {
    backgroundColor: '#6c757d',
    color: '#ffffff',
    borderRadius: '4px',
    // ⚠️ borderColorが不足（dark:border-white/10 = rgba(255, 255, 255, 0.1)）
    // ⚠️ borderWidthが不足（1px）
  },
},
input: {
  style: {
    backgroundColor: 'rgba(15, 23, 42, 0.6)',
    color: '#f1f5f9',
    borderColor: 'rgba(255, 255, 255, 0.1)',
    borderRadius: '4px',
    // ⚠️ borderWidthが不足（1px）
  },
},
```

#### ライトテーマ

**Seeder** (`ThemeSeeder.php` 136-158行目):
```php
'buttonPrimary' => [
    'style' => [
        'backgroundColor' => '#0f172a',
        'color' => '#ffffff',
        'borderRadius' => '4px',
    ],
],
'buttonSecondary' => [
    'style' => [
        'backgroundColor' => '#6c757d',
        'color' => '#ffffff',
        'borderRadius' => '4px',
    ],
],
'input' => [
    'style' => [
        'backgroundColor' => 'transparent',
        'color' => '#0f172a',
        'borderColor' => '#cbd5e1',
        'borderWidth' => '1px',
        'borderRadius' => '4px',
    ],
],
```

**PRESET_THEMES** (`presetThemes.ts` 87-109行目):
```typescript
buttonPrimary: {
  style: {
    backgroundColor: '#0f172a',
    color: '#ffffff',
    borderRadius: '4px',
    // ⚠️ boxShadowが不足（shadow-sm）
  },
},
buttonSecondary: {
  style: {
    backgroundColor: '#6c757d',
    color: '#ffffff',
    borderRadius: '4px',
    // ⚠️ borderColorが不足（border-slate-300 = #cbd5e1）
    // ⚠️ borderWidthが不足（1px）
  },
},
input: {
  style: {
    backgroundColor: 'transparent',
    color: '#0f172a',
    borderColor: '#cbd5e1',
    borderWidth: '1px',
    borderRadius: '4px',
    // ✅ 一致
  },
},
```

#### ReFormaテーマ

**Seeder** (`ThemeSeeder.php` 215-237行目):
```php
'buttonPrimary' => [
    'style' => [
        'backgroundColor' => 'rgba(255, 255, 255, 0.1)',
        'color' => '#f1f5f9',
        'borderRadius' => '8px',
    ],
],
'buttonSecondary' => [
    'style' => [
        'backgroundColor' => '#6c757d',
        'color' => '#ffffff',
        'borderRadius' => '8px',
    ],
],
'input' => [
    'style' => [
        'backgroundColor' => 'transparent',
        'color' => '#f1f5f9',
        'borderColor' => 'rgba(255, 255, 255, 0.1)',
        'borderWidth' => '1px',
        'borderRadius' => '8px',
    ],
],
```

**PRESET_THEMES** (`presetThemes.ts` 146-168行目):
```typescript
buttonPrimary: {
  style: {
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    color: '#f1f5f9',
    borderRadius: '8px',
    // ⚠️ boxShadowが不足（shadow-sm、オプション）
  },
},
buttonSecondary: {
  style: {
    backgroundColor: '#6c757d',
    color: '#ffffff',
    borderRadius: '8px',
    // ⚠️ borderColorが不足（group-data-[theme=reforma]:border-white/10 = rgba(255, 255, 255, 0.1)）
    // ⚠️ borderWidthが不足（1px）
  },
},
input: {
  style: {
    backgroundColor: 'transparent',
    color: '#f1f5f9',
    borderColor: 'rgba(255, 255, 255, 0.1)',
    borderWidth: '1px',
    borderRadius: '8px',
    // ✅ 一致
  },
},
```

#### Classicテーマ

**Seeder** (`ThemeSeeder.php` 294-320行目):
```php
'buttonPrimary' => [
    'style' => [
        'backgroundColor' => 'transparent',
        'color' => '#6b7280',
        'borderColor' => '#6b7280',
        'borderWidth' => '1px',
        'borderRadius' => '0px',
    ],
],
'buttonSecondary' => [
    'style' => [
        'backgroundColor' => 'transparent',
        'color' => '#6c757d',
        'borderColor' => '#6c757d',
        'borderWidth' => '1px',
        'borderRadius' => '0px',
    ],
],
'input' => [
    'style' => [
        'backgroundColor' => 'transparent',
        'color' => '#1f2937',
        'borderColor' => '#d1d5db',
        'borderWidth' => '1px',
        'borderRadius' => '0px',
    ],
],
```

**PRESET_THEMES** (`presetThemes.ts` 205-231行目):
```typescript
buttonPrimary: {
  style: {
    backgroundColor: 'transparent',
    color: '#6b7280',
    borderColor: '#6b7280',
    borderWidth: '1px',
    borderRadius: '0px',
    // ✅ 一致
  },
},
buttonSecondary: {
  style: {
    backgroundColor: 'transparent',
    color: '#6c757d',
    borderColor: '#6c757d',
    borderWidth: '1px',
    borderRadius: '0px',
    // ✅ 一致
  },
},
input: {
  style: {
    backgroundColor: 'transparent',
    color: '#1f2937',
    borderColor: '#d1d5db',
    borderWidth: '1px',
    borderRadius: '0px',
    // ✅ 一致
  },
},
```

## 問題点の整理

### 問題1: buttonPrimaryに`boxShadow`が不足

**影響を受けるテーマ**:
- ダークテーマ
- ライトテーマ
- ReFormaテーマ（オプション）

**不足項目**:
- `boxShadow: '0 1px 2px 0 rgb(0 0 0 / 0.05)'`（`shadow-sm`に相当）

### 問題2: buttonSecondaryに`borderColor`と`borderWidth`が不足

**影響を受けるテーマ**:
- ダークテーマ: `borderColor: 'rgba(255, 255, 255, 0.1)'`, `borderWidth: '1px'`
- ライトテーマ: `borderColor: '#cbd5e1'`, `borderWidth: '1px'`
- ReFormaテーマ: `borderColor: 'rgba(255, 255, 255, 0.1)'`, `borderWidth: '1px'`
- Classicテーマ: ✅ 既に設定済み

### 問題3: inputに`borderWidth`が不足（ダークテーマのみ）

**影響を受けるテーマ**:
- ダークテーマ: `borderWidth: '1px'`
- ライト/ReForma/Classicテーマ: ✅ 既に設定済み

## タスクリスト（細分化版）

### タスク1: buttonPrimaryのスタイルを更新

#### タスク1-1: ダークテーマのbuttonPrimaryを更新
- **ファイル**: `src/constants/presetThemes.ts`
- **修正箇所**: 29-35行目
- **修正内容**:
  - [ ] `boxShadow`を追加: `0 1px 2px 0 rgb(0 0 0 / 0.05)`（`shadow-sm`に相当）

#### タスク1-2: ライトテーマのbuttonPrimaryを更新
- **ファイル**: `src/constants/presetThemes.ts`
- **修正箇所**: 87-93行目
- **修正内容**:
  - [ ] `boxShadow`を追加: `0 1px 2px 0 rgb(0 0 0 / 0.05)`（`shadow-sm`に相当）

#### タスク1-3: ReFormaテーマのbuttonPrimaryを更新（オプション）
- **ファイル**: `src/constants/presetThemes.ts`
- **修正箇所**: 146-152行目
- **修正内容**:
  - [ ] `boxShadow`を追加: `0 1px 2px 0 rgb(0 0 0 / 0.05)`（`shadow-sm`に相当、オプション）

---

### タスク2: buttonSecondaryのスタイルを更新

#### タスク2-1: ダークテーマのbuttonSecondaryを更新
- **ファイル**: `src/constants/presetThemes.ts`
- **修正箇所**: 36-42行目
- **修正内容**:
  - [ ] `borderColor`を追加: `rgba(255, 255, 255, 0.1)`（`dark:border-white/10`に相当）
  - [ ] `borderWidth`を追加: `1px`

#### タスク2-2: ライトテーマのbuttonSecondaryを更新
- **ファイル**: `src/constants/presetThemes.ts`
- **修正箇所**: 94-100行目
- **修正内容**:
  - [ ] `borderColor`を追加: `#cbd5e1`（`border-slate-300`に相当）
  - [ ] `borderWidth`を追加: `1px`

#### タスク2-3: ReFormaテーマのbuttonSecondaryを更新
- **ファイル**: `src/constants/presetThemes.ts`
- **修正箇所**: 153-159行目
- **修正内容**:
  - [ ] `borderColor`を追加: `rgba(255, 255, 255, 0.1)`（`group-data-[theme=reforma]:border-white/10`に相当）
  - [ ] `borderWidth`を追加: `1px`

---

### タスク3: inputのスタイルを更新

#### タスク3-1: ダークテーマのinputを更新
- **ファイル**: `src/constants/presetThemes.ts`
- **修正箇所**: 43-50行目
- **修正内容**:
  - [ ] `borderWidth`を追加: `1px`

---

### タスク4: 動作確認

#### タスク4-1: buttonPrimaryの確認
- **確認項目**:
  - [ ] ダークテーマ選択時に`boxShadow`が適用される
  - [ ] ライトテーマ選択時に`boxShadow`が適用される
  - [ ] ReFormaテーマ選択時に`boxShadow`が適用される（オプション）

#### タスク4-2: buttonSecondaryの確認
- **確認項目**:
  - [ ] ダークテーマ選択時に`borderColor`と`borderWidth`が適用される
  - [ ] ライトテーマ選択時に`borderColor`と`borderWidth`が適用される
  - [ ] ReFormaテーマ選択時に`borderColor`と`borderWidth`が適用される
  - [ ] Classicテーマ選択時に既存の設定が維持される

#### タスク4-3: inputの確認
- **確認項目**:
  - [ ] ダークテーマ選択時に`borderWidth`が適用される
  - [ ] ライト/ReForma/Classicテーマ選択時に既存の設定が維持される

## 実装詳細

### 修正例

#### ダークテーマのbuttonPrimary修正例

```typescript
buttonPrimary: {
  style: {
    backgroundColor: '#ffffff',
    color: '#0f172a',
    borderRadius: '4px',
    boxShadow: '0 1px 2px 0 rgb(0 0 0 / 0.05)', // 追加
  },
},
```

#### ダークテーマのbuttonSecondary修正例

```typescript
buttonSecondary: {
  style: {
    backgroundColor: '#6c757d',
    color: '#ffffff',
    borderColor: 'rgba(255, 255, 255, 0.1)',    // 追加
    borderWidth: '1px',                         // 追加
    borderRadius: '4px',
  },
},
```

#### ダークテーマのinput修正例

```typescript
input: {
  style: {
    backgroundColor: 'rgba(15, 23, 42, 0.6)',
    color: '#f1f5f9',
    borderColor: 'rgba(255, 255, 255, 0.1)',
    borderWidth: '1px',                         // 追加
    borderRadius: '4px',
  },
},
```

#### ライトテーマのbuttonPrimary修正例

```typescript
buttonPrimary: {
  style: {
    backgroundColor: '#0f172a',
    color: '#ffffff',
    borderRadius: '4px',
    boxShadow: '0 1px 2px 0 rgb(0 0 0 / 0.05)', // 追加
  },
},
```

#### ライトテーマのbuttonSecondary修正例

```typescript
buttonSecondary: {
  style: {
    backgroundColor: '#6c757d',
    color: '#ffffff',
    borderColor: '#cbd5e1',                     // 追加
    borderWidth: '1px',                         // 追加
    borderRadius: '4px',
  },
},
```

#### ReFormaテーマのbuttonPrimary修正例（オプション）

```typescript
buttonPrimary: {
  style: {
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    color: '#f1f5f9',
    borderRadius: '8px',
    boxShadow: '0 1px 2px 0 rgb(0 0 0 / 0.05)', // 追加（オプション）
  },
},
```

#### ReFormaテーマのbuttonSecondary修正例

```typescript
buttonSecondary: {
  style: {
    backgroundColor: '#6c757d',
    color: '#ffffff',
    borderColor: 'rgba(255, 255, 255, 0.1)',    // 追加
    borderWidth: '1px',                         // 追加
    borderRadius: '8px',
  },
},
```

## 注意点

1. **boxShadowについて**:
   - `shadow-sm`は軽量な影で、ボタンに立体感を与える
   - buttonPrimaryには追加を推奨
   - buttonSecondaryには追加しない（管理画面のスタイルに含まれていない）

2. **borderColorとborderWidthについて**:
   - buttonSecondaryには`border`が必須（管理画面のスタイルに含まれている）
   - inputには`borderWidth`が明示的に設定されている場合がある

3. **Classicテーマ**:
   - buttonPrimary/buttonSecondary/inputは既に`borderColor`と`borderWidth`が設定済み
   - 修正不要

4. **後方互換性**:
   - 既存のフォームデータに影響を与えないよう注意
   - `custom_style_config`が`null`の場合の処理を適切に実装

## 実装順序の推奨

1. **タスク1**: buttonPrimaryのスタイルを更新
2. **タスク2**: buttonSecondaryのスタイルを更新
3. **タスク3**: inputのスタイルを更新
4. **タスク4**: 動作確認

## 進捗状況

- **全体進捗**: 4/4 タスク完了（100%）
- **最終更新**: 2026-01-23
- **完了タスク**: 
  - ✅ タスク1（buttonPrimaryの更新）
  - ✅ タスク2（buttonSecondaryの更新）
  - ✅ タスク3（inputの更新）
  - ✅ タスク4（動作確認）
- **進行中タスク**: なし
- **未着手タスク**: なし

## 実装完了内容（2026-01-23）

### ✅ タスク1: buttonPrimaryのスタイル更新
- ダークテーマ: `boxShadow: '0 1px 2px 0 rgb(0 0 0 / 0.05)'`を追加
- ライトテーマ: `boxShadow: '0 1px 2px 0 rgb(0 0 0 / 0.05)'`を追加
- ReFormaテーマ: `boxShadow: '0 1px 2px 0 rgb(0 0 0 / 0.05)'`を追加

### ✅ タスク2: buttonSecondaryのスタイル更新
- ダークテーマ: `borderWidth: '1px'`を追加
- ライトテーマ: `borderWidth: '1px'`を追加
- ReFormaテーマ: `borderWidth: '1px'`を追加

### ✅ タスク3: inputのスタイル更新
- ダークテーマ: `borderWidth: '1px'`を追加

### ✅ タスク4: 動作確認
- `presetThemes.ts`と`ThemeSeeder.php`の両方を更新し、同期を完了
