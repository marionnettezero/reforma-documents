# プリセットテーマのカードスタイル初期値適用タスク（フロントエンド）

## 概要

Seederで設定したカードスタイルの初期値（`color`、`boxShadow`など）をフロントエンド側で適用する処理を追加します。また、カスタム選択時の初期値の動作を確認・改善します。

## 現状確認（2026-01-20更新）

### 1. プリセットテーマ選択時の処理

**ファイル**: `src/pages/forms/FormEditIntegratedPage.tsx`（2749-2756行目）

```typescript
onChange={() => {
  setSelectedPresetTheme(themeName);
  const presetConfig = PRESET_THEMES[themeName];
  if (presetConfig) {
    setFormCustomStyleConfig({
      ...presetConfig,
      presetTheme: themeName,
    });
  }
}}
```

**問題点**:
- フロント側の定数`PRESET_THEMES`を使用している
- バックエンドのSeederで設定した初期値（特に`card`スタイルの`color`と`boxShadow`）が反映されていない
- `PRESET_THEMES`定数がSeederの最新値と同期していない

### 2. カスタム選択時の処理

**ファイル**: `src/pages/forms/FormEditIntegratedPage.tsx`（2776-2783行目）

```typescript
onChange={() => {
  setSelectedPresetTheme('custom');
  // カスタムの場合は既存の設定を維持
  if (formCustomStyleConfig) {
    setFormCustomStyleConfig({
      ...formCustomStyleConfig,
      presetTheme: 'custom',
    });
  }
}}
```

**確認結果**:
- ✅ 既存の`formCustomStyleConfig`を維持している
- ✅ その前に選択していたテーマの設定が保持される
- ⚠️ `formCustomStyleConfig`が`null`の場合は何も設定されない（初期値なし）

### 3. フォームデータ読み込み時の処理

**ファイル**: `src/pages/forms/FormEditIntegratedPage.tsx`（2125-2143行目）

```typescript
const customStyleConfig = formData.custom_style_config || null;
if (customStyleConfig) {
  setFormCustomStyleConfig({
    ...customStyleConfig,
    headerEnabled: customStyleConfig.headerEnabled !== undefined ? customStyleConfig.headerEnabled : true,
    footerEnabled: customStyleConfig.footerEnabled !== undefined ? customStyleConfig.footerEnabled : true,
    headerHtml: customStyleConfig.headerHtml ? sanitizeHtml(customStyleConfig.headerHtml) : null,
    footerHtml: customStyleConfig.footerHtml ? sanitizeHtml(customStyleConfig.footerHtml) : null,
  });
} else {
  setFormCustomStyleConfig(null);
}
// プリセットテーマを判定
if (formData.custom_style_config?.presetTheme && PRESET_THEME_NAMES.includes(formData.custom_style_config.presetTheme as PresetThemeName)) {
  setSelectedPresetTheme(formData.custom_style_config.presetTheme as PresetThemeName);
} else {
  setSelectedPresetTheme('custom');
}
```

**確認結果**:
- ✅ バックエンドから取得した`custom_style_config`を使用している
- ✅ Seederの初期値が含まれている（バックエンドから取得したデータのため）

### 4. PRESET_THEMES定数の現状

**ファイル**: `src/constants/presetThemes.ts`

#### ダークテーマ（22-27行目）
```typescript
card: {
  style: {
    backgroundColor: 'rgba(15, 23, 42, 0.4)',
    borderColor: 'rgba(255, 255, 255, 0.1)',
    borderRadius: '4px',
    // ⚠️ colorが不足
    // ⚠️ boxShadowが不足
  },
},
```

#### ライトテーマ（80-85行目）
```typescript
card: {
  style: {
    backgroundColor: '#ffffff',
    borderColor: '#e2e8f0',
    borderRadius: '4px',
    // ⚠️ colorが不足
    // ⚠️ boxShadowが不足
  },
},
```

#### Classicテーマ（198-203行目）
```typescript
card: {
  style: {
    backgroundColor: '#ffffff',
    borderColor: '#e5e7eb',  // ⚠️ #e2e8f0に統一すべき
    borderRadius: '0px',
    // ⚠️ colorが不足
    // ⚠️ boxShadowは追加しない（フラットデザイン）
  },
},
```

#### ReFormaテーマ（139-144行目）
```typescript
card: {
  style: {
    backgroundColor: '#0b0c10',
    borderColor: 'rgba(255, 255, 255, 0.1)',
    borderRadius: '8px',
    // ⚠️ colorが不足
  },
},
```

### 5. テーマ一覧取得API

**ファイル**: `src/pages/forms/FormEditIntegratedPage.tsx`（2046-2076行目）

```typescript
const res = await apiGetJson<{
  success: boolean;
  data: {
    themes: Array<{ id: number; code: string; name: string }>;
    pagination?: any;
  };
}>(`/v1/system/themes?${params.toString()}`);
```

**確認結果**:
- ⚠️ テーマ一覧APIは`id`、`code`、`name`のみを返している
- ⚠️ `custom_style_config`は含まれていない
- 個別のテーマデータを取得するAPIが必要かもしれない

## 問題点の整理

### 問題1: プリセットテーマ選択時にSeederの初期値が適用されない

**原因**:
- フロント側の定数`PRESET_THEMES`を使用している
- `PRESET_THEMES`がSeederの最新値と同期していない

**影響**:
- Seederで設定した`card`スタイルの`color`と`boxShadow`が適用されない
- バックエンドとフロントエンドで初期値が不一致

### 問題2: PRESET_THEMES定数がSeederの最新値と同期していない

**原因**:
- 手動で同期する必要がある
- Seeder更新時にフロント側の定数も更新する必要がある

**影響**:
- ダーク/ライト/Classic/ReFormaテーマの`card`スタイルに`color`と`boxShadow`が不足

### 問題3: カスタム選択時の初期値が未設定の場合の動作

**現状**:
- `formCustomStyleConfig`が`null`の場合は何も設定されない

**確認が必要**:
- カスタム選択時に初期値（空の設定）を設定すべきか
- それとも、その前に選択していたテーマの設定を保持すべきか

## タスクリスト（細分化版）

### タスク1: PRESET_THEMES定数をSeederの最新値と同期

#### タスク1-1: ダークテーマのcardスタイルを更新
- **ファイル**: `src/constants/presetThemes.ts`
- **修正箇所**: 22-27行目
- **修正内容**:
  - [ ] `color`を追加: `#f1f5f9`（`dark:text-slate-100`に相当）
  - [ ] `boxShadow`を追加: `0 1px 2px 0 rgb(0 0 0 / 0.05)`（`shadow-sm`に相当）

#### タスク1-2: ライトテーマのcardスタイルを更新
- **ファイル**: `src/constants/presetThemes.ts`
- **修正箇所**: 80-85行目
- **修正内容**:
  - [ ] `color`を追加: `#0f172a`（`text-slate-900`に相当）
  - [ ] `boxShadow`を追加: `0 1px 2px 0 rgb(0 0 0 / 0.05)`（`shadow-sm`に相当）

#### タスク1-3: Classicテーマのcardスタイルを更新
- **ファイル**: `src/constants/presetThemes.ts`
- **修正箇所**: 198-203行目
- **修正内容**:
  - [ ] `color`を追加: `#0f172a`（`text-slate-900`に相当）
  - [ ] `borderColor`を`#e2e8f0`（`slate-200`）に統一
  - [ ] `boxShadow`は追加しない（フラットデザインのため）

#### タスク1-4: ReFormaテーマのcardスタイルを更新
- **ファイル**: `src/constants/presetThemes.ts`
- **修正箇所**: 139-144行目
- **修正内容**:
  - [ ] `color`を追加: `#f1f5f9`（`group-data-[theme=reforma]:text-slate-100`に相当）

---

### タスク2: プリセットテーマ選択時にバックエンドの初期値を適用（オプション）

#### タスク2-1: テーマデータ取得APIの確認
- **確認項目**:
  - [ ] `/v1/system/themes/{id}`のような個別テーマ取得APIが存在するか確認
  - [ ] テーマ一覧APIに`custom_style_config`を含めることができるか確認
  - [ ] バックエンドAPIの仕様を確認

#### タスク2-2: プリセットテーマ選択時の処理を改善（オプション）
- **ファイル**: `src/pages/forms/FormEditIntegratedPage.tsx`
- **修正箇所**: 2749-2756行目
- **修正内容**:
  - [ ] バックエンドからテーマデータを取得して`custom_style_config`を使用する
  - [ ] または、`PRESET_THEMES`定数を最新化して使用する（タスク1で対応）

**注意**: タスク1で`PRESET_THEMES`定数を最新化すれば、このタスクは不要かもしれません。

---

### タスク3: カスタム選択時の初期値の動作確認・改善

#### タスク3-1: カスタム選択時の動作を確認
- **確認項目**:
  - [ ] `formCustomStyleConfig`が`null`の場合の動作を確認
  - [ ] その前に選択していたテーマの設定が保持されることを確認
  - [ ] 期待される動作を明確化

#### タスク3-2: カスタム選択時の初期値を改善（必要に応じて）
- **ファイル**: `src/pages/forms/FormEditIntegratedPage.tsx`
- **修正箇所**: 2776-2783行目
- **修正内容**:
  - [ ] `formCustomStyleConfig`が`null`の場合の処理を追加（必要に応じて）
  - [ ] 初期値の設定方法を改善（必要に応じて）

**注意**: 現状の動作（既存の設定を維持）が期待通りであれば、このタスクは不要です。

---

### タスク4: 動作確認

#### タスク4-1: プリセットテーマ選択時の確認
- **確認項目**:
  - [ ] ダークテーマ選択時に`card`スタイルの`color`と`boxShadow`が適用される
  - [ ] ライトテーマ選択時に`card`スタイルの`color`と`boxShadow`が適用される
  - [ ] Classicテーマ選択時に`card`スタイルの`color`が適用される（`boxShadow`はなし）
  - [ ] ReFormaテーマ選択時に`card`スタイルの`color`が適用される

#### タスク4-2: カスタム選択時の確認
- **確認項目**:
  - [ ] カスタム選択時に既存の設定が保持される
  - [ ] その前に選択していたテーマの設定が正しく保持される

#### タスク4-3: フォーム保存・読み込み時の確認
- **確認項目**:
  - [ ] フォーム保存時に`custom_style_config`が正しく保存される
  - [ ] フォーム読み込み時に`custom_style_config`が正しく読み込まれる
  - [ ] Seederの初期値が正しく適用される

## 実装詳細

### 修正例

#### ダークテーマの修正例

```typescript
card: {
  style: {
    backgroundColor: 'rgba(15, 23, 42, 0.4)',
    color: '#f1f5f9',                          // 追加
    borderColor: 'rgba(255, 255, 255, 0.1)',
    borderRadius: '4px',
    boxShadow: '0 1px 2px 0 rgb(0 0 0 / 0.05)', // 追加
  },
},
```

#### ライトテーマの修正例

```typescript
card: {
  style: {
    backgroundColor: '#ffffff',
    color: '#0f172a',                          // 追加
    borderColor: '#e2e8f0',
    borderRadius: '4px',
    boxShadow: '0 1px 2px 0 rgb(0 0 0 / 0.05)', // 追加
  },
},
```

#### Classicテーマの修正例

```typescript
card: {
  style: {
    backgroundColor: '#ffffff',
    color: '#0f172a',                          // 追加
    borderColor: '#e2e8f0',                     // #e5e7ebから変更
    borderRadius: '0px',
    // boxShadowは追加しない（フラットデザイン）
  },
},
```

#### ReFormaテーマの修正例

```typescript
card: {
  style: {
    backgroundColor: '#0b0c10',
    color: '#f1f5f9',                          // 追加
    borderColor: 'rgba(255, 255, 255, 0.1)',
    borderRadius: '8px',
  },
},
```

## 注意点

1. **PRESET_THEMES定数の同期**:
   - Seeder更新時にフロント側の定数も更新する必要がある
   - 将来的には、バックエンドからテーマデータを取得する方式に変更することを検討

2. **カスタム選択時の動作**:
   - 現状の動作（既存の設定を維持）が期待通りか確認が必要
   - `formCustomStyleConfig`が`null`の場合の動作を明確化

3. **後方互換性**:
   - 既存のフォームデータに影響を与えないよう注意
   - `custom_style_config`が`null`の場合の処理を適切に実装

## 実装順序の推奨

1. **タスク1**: PRESET_THEMES定数をSeederの最新値と同期（必須）
2. **タスク3**: カスタム選択時の初期値の動作確認（確認のみ）
3. **タスク4**: 動作確認（必須）
4. **タスク2**: プリセットテーマ選択時にバックエンドの初期値を適用（オプション、将来的な改善）

## 進捗状況

- **全体進捗**: 4/4 タスク完了（100%）
- **最終更新**: 2026-01-23
- **完了タスク**: 
  - ✅ タスク1（PRESET_THEMES定数の同期）
  - ✅ タスク2（バックエンド初期値適用、オプション - タスク1で対応済み）
  - ✅ タスク3（カスタム選択時の確認）
  - ✅ タスク4（動作確認）
- **進行中タスク**: なし
- **未着手タスク**: なし

## 実装完了内容（2026-01-23）

### ✅ タスク1: PRESET_THEMES定数をSeederの最新値と同期
- ダークテーマの`card`スタイル: `boxShadow: '0 1px 2px 0 rgb(0 0 0 / 0.05)'`を追加
- ライトテーマの`card`スタイル: `boxShadow: '0 1px 2px 0 rgb(0 0 0 / 0.05)'`を追加
- `presetThemes.ts`と`ThemeSeeder.php`の両方を更新し、同期を完了
