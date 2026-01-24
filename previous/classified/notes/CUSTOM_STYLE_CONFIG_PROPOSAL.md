# カスタムスタイル設定機能の提案

## 概要

プレビューや公開フォームのデザインをより自由にカスタマイズできるようにするため、フォーム設定にカスタムスタイル設定機能を追加する提案です。

## 目的

- 顧客の多様なデザイン要求に対応
- **既存のテーマトークン機能を置き換え**（より柔軟で細かい設定が可能）
- 各要素（Card、Field、Buttonなど）に対して個別にCSSクラスやインラインスタイルを適用可能
- プリセットテーマを提供し、テーマ作成の負担を軽減

## 提案するデータ構造

### 1. フォーム設定に追加するフィールド

```typescript
// フォーム設定に追加
interface FormDetailResponse {
  // ... 既存のフィールド
  custom_style_config?: CustomStyleConfig | null;
}

// カスタムスタイル設定の型定義
interface CustomStyleConfig {
  // 要素タイプごとのスタイル設定
  elements: {
    // コンテナ（フォーム全体のラッパー）
    container?: ElementStyleConfig;
    // ヘッダ領域（<header>タグ）
    header?: ElementStyleConfig;
    // コンテンツ領域（STEP/GROUP/FIELDの制御領域）
    content?: ElementStyleConfig;
    // フッタ領域（<footer>タグ）
    footer?: ElementStyleConfig;
    // カード（フォームカード）
    card?: ElementStyleConfig;
    // カードボディ
    cardBody?: ElementStyleConfig;
    // ヘッダーカード（ロゴ・タイトル部分）
    headerCard?: ElementStyleConfig;
    // タイトル（h1）
    title?: ElementStyleConfig;
    // 説明文（p）
    description?: ElementStyleConfig;
    // フィールドラベル
    fieldLabel?: ElementStyleConfig;
    // 入力フィールド（input, textarea, select等）
    input?: ElementStyleConfig;
    // ボタン（送信ボタン、次へボタン等）
    button?: ElementStyleConfig;
    // ボタン（プライマリ）
    buttonPrimary?: ElementStyleConfig;
    // ボタン（セカンダリ）
    buttonSecondary?: ElementStyleConfig;
    // STEPタブ
    stepTab?: ElementStyleConfig;
    // STEPタブ（アクティブ）
    stepTabActive?: ElementStyleConfig;
    // GROUP名
    groupName?: ElementStyleConfig;
    // エラーメッセージ
    errorMessage?: ElementStyleConfig;
    // 確認画面のセクション
    confirmationSection?: ElementStyleConfig;
    // ヘルプテキスト
    helpText?: ElementStyleConfig;
    // ヘルプテキストアイコン
    helpTextIcon?: ElementStyleConfig;
  };
  // グローバルCSS（任意のCSSコード）
  globalCss?: string | null;
  // ヘッダ領域の表示ON/OFF
  headerEnabled?: boolean;
  // ヘッダHTML（カスタマイズ時、デフォルトはnull）
  headerHtml?: string | null;
  // フッタ領域の表示ON/OFF
  footerEnabled?: boolean;
  // フッタHTML（カスタマイズ時、デフォルトはnull）
  footerHtml?: string | null;
  // プリセットテーマ名（"dark" | "light" | "reforma" | "classic" | "custom"）
  presetTheme?: string | null;
}

// 要素スタイル設定
interface ElementStyleConfig {
  // CSSクラス名（複数指定可能、スペース区切り）
  className?: string | null;
  // インラインスタイル（CSSプロパティ名をキーとするオブジェクト）
  style?: Record<string, string> | null;
  // 条件付きスタイル（特定の状態でのスタイル）
  conditionalStyles?: {
    // ホバー時のスタイル
    hover?: ElementStyleConfig;
    // フォーカス時のスタイル
    focus?: ElementStyleConfig;
    // 無効化時のスタイル
    disabled?: ElementStyleConfig;
    // エラー時のスタイル
    error?: ElementStyleConfig;
  } | null;
}
```

### 2. レイアウト構造

フォームの表示領域は以下の3つの領域に分割されます：

```
┌─────────────────────────────────────────────────────────┐
│ ヘッダ領域 (elements.header)                            │
│ ※ デフォルト: ロゴとフォーム名                          │
│ ※ カスタマイズ: headerHtml でHTML入力可能              │
│ ※ <header>タグ、position: sticky で固定表示            │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│ コンテンツ領域 (elements.content)                       │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ ヘッダーカード (elements.headerCard)               │ │
│ │ ┌───────────────────────────────────────────────┐   │ │
│ │ │ タイトル (elements.title)                     │   │ │
│ │ │ 説明文 (elements.description)                 │   │ │
│ │ └───────────────────────────────────────────────┘   │ │
│ └─────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ カード (elements.card)                              │ │
│ │ ┌───────────────────────────────────────────────┐   │ │
│ │ │ カードボディ (elements.cardBody)               │   │ │
│ │ │                                               │   │ │
│ │ │ STEPタブ (elements.stepTab)                   │   │ │
│ │ │ STEPタブ[アクティブ] (elements.stepTabActive) │   │ │
│ │ │                                               │   │ │
│ │ │ GROUP名 (elements.groupName)                  │   │ │
│ │ │                                               │   │ │
│ │ │ フィールドラベル (elements.fieldLabel)        │   │ │
│ │ │ ヘルプアイコン (elements.helpTextIcon)        │   │ │
│ │ │ ヘルプテキスト (elements.helpText)            │   │ │
│ │ │ 入力フィールド (elements.input)                │   │ │
│ │ │ エラーメッセージ (elements.errorMessage)       │   │ │
│ │ │                                               │   │ │
│ │ │ ボタン[プライマリ] (elements.buttonPrimary)   │   │ │
│ │ │ ボタン[セカンダリ] (elements.buttonSecondary) │   │ │
│ │ │ ボタン (elements.button)                      │   │ │
│ │ │                                               │   │ │
│ │ │ 確認画面セクション (elements.confirmationSection)│ │
│ │ └───────────────────────────────────────────────┘   │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│ フッタ領域 (elements.footer)                            │
│ ※ デフォルト: ReForma コピーライト                      │
│ ※ カスタマイズ: footerHtml でHTML入力可能              │
│ ※ <footer>タグ                                         │
└─────────────────────────────────────────────────────────┘
```

#### 全体構造の詳細図

```
┌─────────────────────────────────────────────────────────────────┐
│ コンテナ (elements.container)                                    │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ ヘッダ領域 (elements.header)                                │ │
│ │ ┌─────────────────────────────────────────────────────────┐ │ │
│ │ │ <header>                                                │ │ │
│ │ │   [headerHtml または デフォルトのロゴ・タイトル]        │ │ │
│ │ │ </header>                                               │ │ │
│ │ └─────────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ コンテンツ領域 (elements.content)                            │ │
│ │ ┌───────────────────────────────────────────────────────┐ │ │
│ │ │ ヘッダーカード (elements.headerCard)                   │ │ │
│ │ │ ┌───────────────────────────────────────────────────┐ │ │ │
│ │ │ │ カードボディ (elements.cardBody)                   │ │ │ │
│ │ │ │ ┌───────────────────────────────────────────────┐ │ │ │ │
│ │ │ │ │ タイトル (elements.title)                     │ │ │ │ │
│ │ │ │ │ 説明文 (elements.description)                 │ │ │ │ │
│ │ │ │ └───────────────────────────────────────────────┘ │ │ │ │
│ │ │ └───────────────────────────────────────────────────┘ │ │ │
│ │ └───────────────────────────────────────────────────────┘ │ │
│ │                                                           │ │
│ │ ┌───────────────────────────────────────────────────────┐ │ │
│ │ │ カード (elements.card)                                  │ │ │
│ │ │ ┌───────────────────────────────────────────────────┐ │ │ │
│ │ │ │ カードボディ (elements.cardBody)                   │ │ │ │
│ │ │ │                                                     │ │ │ │
│ │ │ │ [STEPタブエリア]                                    │ │ │ │
│ │ │ │ ┌───────────────────────────────────────────────┐ │ │ │ │
│ │ │ │ │ STEPタブ (elements.stepTab)                   │ │ │ │ │
│ │ │ │ │ STEPタブ[アクティブ] (elements.stepTabActive) │ │ │ │ │
│ │ │ │ └───────────────────────────────────────────────┘ │ │ │ │
│ │ │ │                                                     │ │ │ │
│ │ │ │ [フィールドエリア]                                  │ │ │ │
│ │ │ │ ┌───────────────────────────────────────────────┐ │ │ │ │
│ │ │ │ │ GROUP名 (elements.groupName)                  │ │ │ │ │
│ │ │ │ │                                               │ │ │ │ │
│ │ │ │ │ フィールドラベル (elements.fieldLabel)        │ │ │ │ │
│ │ │ │ │ ヘルプアイコン (elements.helpTextIcon)        │ │ │ │ │
│ │ │ │ │ ヘルプテキスト (elements.helpText)            │ │ │ │ │
│ │ │ │ │ 入力フィールド (elements.input)                │ │ │ │ │
│ │ │ │ │ エラーメッセージ (elements.errorMessage)       │ │ │ │ │
│ │ │ │ └───────────────────────────────────────────────┘ │ │ │ │
│ │ │ │                                                     │ │ │ │
│ │ │ │ [ボタンエリア]                                      │ │ │ │
│ │ │ │ ┌───────────────────────────────────────────────┐ │ │ │ │
│ │ │ │ │ ボタン[プライマリ] (elements.buttonPrimary)   │ │ │ │ │
│ │ │ │ │ ボタン[セカンダリ] (elements.buttonSecondary) │ │ │ │ │
│ │ │ │ │ ボタン (elements.button)                      │ │ │ │ │
│ │ │ │ └───────────────────────────────────────────────┘ │ │ │ │
│ │ │ │                                                     │ │ │ │
│ │ │ │ [確認画面セクション]                                │ │ │ │
│ │ │ │ ┌───────────────────────────────────────────────┐ │ │ │ │
│ │ │ │ │ 確認画面セクション (elements.confirmationSection)│ │ │ │ │
│ │ │ │ └───────────────────────────────────────────────┘ │ │ │ │
│ │ │ └───────────────────────────────────────────────────┘ │ │ │
│ │ └───────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ フッタ領域 (elements.footer)                                │ │
│ │ ┌─────────────────────────────────────────────────────────┐ │ │
│ │ │ <footer>                                                │ │ │
│ │ │   [footerHtml または デフォルトのコピーライト]          │ │ │
│ │ │ </footer>                                               │ │ │
│ │ └─────────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

#### ヘッダ領域の仕様

- **デフォルト表示**: ロゴとフォーム名（現在の実装と同じ）
- **カスタマイズ時**: `headerHtml` にHTMLコードを設定すると、その内容を表示
- **タグ**: `<header>` タグで囲む
- **固定表示**: `position: sticky; top: 0;` でスクロール時にTOPに残る
- **スタイル**: `elements.header` でカスタマイズ可能

#### フッタ領域の仕様

- **デフォルト表示**: ReFormaのコピーライト表示（例: "© 2024 ReForma"）
- **カスタマイズ時**: `footerHtml` にHTMLコードを設定すると、その内容を表示
- **タグ**: `<footer>` タグで囲む
- **スタイル**: `elements.footer` でカスタマイズ可能

#### コンテンツ領域の仕様

- **内容**: STEP / GROUP / FIELD の制御領域（現在のフォーム設定で指定するコンテンツ）
- **スタイル**: `elements.content` でカスタマイズ可能

### 3. 実装例

#### 例1: シンプルなカスタマイズ（クラス名のみ）

```json
{
  "custom_style_config": {
    "elements": {
      "card": {
        "className": "custom-form-card shadow-lg"
      },
      "buttonPrimary": {
        "className": "custom-primary-btn"
      }
    }
  }
}
```

#### 例2: インラインスタイルとクラス名の併用

```json
{
  "custom_style_config": {
    "elements": {
      "container": {
        "className": "custom-form-container",
        "style": {
          "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
          "padding": "2rem"
        }
      },
      "card": {
        "style": {
          "borderRadius": "20px",
          "boxShadow": "0 10px 30px rgba(0,0,0,0.3)"
        }
      }
    }
  }
}
```

#### 例3: 条件付きスタイル

```json
{
  "custom_style_config": {
    "elements": {
      "buttonPrimary": {
        "className": "custom-btn",
        "style": {
          "backgroundColor": "#007bff",
          "color": "#fff"
        },
        "conditionalStyles": {
          "hover": {
            "style": {
              "backgroundColor": "#0056b3",
              "transform": "scale(1.05)"
            }
          },
          "disabled": {
            "style": {
              "opacity": "0.5",
              "cursor": "not-allowed"
            }
          }
        }
      }
    }
  }
}
```

#### 例4: グローバルCSSの使用

```json
{
  "custom_style_config": {
    "elements": {
      "input": {
        "className": "custom-input"
      }
    },
    "globalCss": ".custom-input { transition: all 0.3s ease; } .custom-input:focus { border-color: #007bff; box-shadow: 0 0 0 3px rgba(0,123,255,0.25); }"
  }
}
```

### 4. フィールドのヘルプテキスト設定

各フィールド（項目）にヘルプテキストを設定できる機能を追加します。

#### 4.1 フィールド設定に追加するフィールド

```typescript
// フィールドのoptions_jsonに追加
interface FieldOptionsJson {
  // ... 既存のフィールド
  label?: string;
  labels?: Record<string, string>;
  placeholder?: string;
  // ... その他の既存フィールド
  
  // ヘルプテキストの有効/無効
  help_text_enabled?: boolean;
  // ヘルプテキスト（多言語対応）
  help_text_i18n?: Record<string, string> | null;
}

// フィールドの型定義
interface FormField {
  id: number;
  field_key: string;
  type: string;
  // ... 既存のフィールド
  options_json?: FieldOptionsJson;
}
```

#### 4.2 実装例

```json
{
  "id": 1,
  "field_key": "field_key_1",
  "type": "text",
  "options_json": {
    "label": "お名前",
    "labels": {
      "ja": "お名前",
      "en": "Name"
    },
    "help_text_enabled": true,
    "help_text_i18n": {
      "ja": "フルネームで入力してください",
      "en": "Please enter your full name"
    }
  }
}
```

#### 4.3 表示方法

ヘルプテキストは以下のように表示されます：

```
┌─────────────────────────────────────────────────────────┐
│ フィールドラベル (elements.fieldLabel)                   │
│ 必須マーク [*]                                           │
│ ヘルプアイコン (elements.helpTextIcon) [?]               │
├─────────────────────────────────────────────────────────┤
│ ヘルプテキスト (elements.helpText)                       │
│ ※ help_text_enabledがtrueの場合のみ表示                 │
│ ※ 多言語対応: help_text_i18n[locale]                    │
├─────────────────────────────────────────────────────────┤
│ 入力フィールド (elements.input)                          │
│ [入力エリア]                                             │
├─────────────────────────────────────────────────────────┤
│ エラーメッセージ (elements.errorMessage)                 │
│ ※ エラーがある場合のみ表示                               │
└─────────────────────────────────────────────────────────┘
```

**詳細説明:**
- **ヘルプアイコン**: ラベルの横に「?」アイコンを表示（クリックでツールチップ表示も可）
- **ヘルプテキスト**: ラベルの下、入力フィールドの上に表示
- **多言語対応**: 現在のロケールに応じて`help_text_i18n`から適切な言語を選択

#### 4.4 スタイル設定

ヘルプテキストとヘルプアイコンのスタイルは`custom_style_config`でカスタマイズ可能：

```json
{
  "custom_style_config": {
    "elements": {
      "helpText": {
        "className": "text-sm text-gray-500 mt-1",
        "style": {
          "fontSize": "0.875rem",
          "color": "#6b7280"
        }
      },
      "helpTextIcon": {
        "className": "ml-1 cursor-help",
        "style": {
          "color": "#9ca3af"
        }
      }
    }
  }
}
```

## 実装方針

### 1. フロントエンド側の実装

#### 1.1 ユーティリティ関数の作成

```typescript
// src/utils/customStyle.ts

export interface ElementStyleConfig {
  className?: string | null;
  style?: Record<string, string> | null;
  conditionalStyles?: {
    hover?: ElementStyleConfig;
    focus?: ElementStyleConfig;
    disabled?: ElementStyleConfig;
    error?: ElementStyleConfig;
  } | null;
}

export interface CustomStyleConfig {
  elements: {
    container?: ElementStyleConfig;
    header?: ElementStyleConfig;
    content?: ElementStyleConfig;
    footer?: ElementStyleConfig;
    card?: ElementStyleConfig;
    cardBody?: ElementStyleConfig;
    headerCard?: ElementStyleConfig;
    title?: ElementStyleConfig;
    description?: ElementStyleConfig;
    fieldLabel?: ElementStyleConfig;
    input?: ElementStyleConfig;
    button?: ElementStyleConfig;
    buttonPrimary?: ElementStyleConfig;
    buttonSecondary?: ElementStyleConfig;
    stepTab?: ElementStyleConfig;
    stepTabActive?: ElementStyleConfig;
    groupName?: ElementStyleConfig;
    errorMessage?: ElementStyleConfig;
    confirmationSection?: ElementStyleConfig;
    helpText?: ElementStyleConfig;
    helpTextIcon?: ElementStyleConfig;
  };
  globalCss?: string | null;
  headerHtml?: string | null;
  footerHtml?: string | null;
}

/**
 * 要素スタイル設定を適用
 * @param element 対象要素
 * @param config スタイル設定
 * @param condition 条件（hover, focus, disabled, error）
 */
export function applyElementStyle(
  element: HTMLElement,
  config: ElementStyleConfig | undefined,
  condition?: 'hover' | 'focus' | 'disabled' | 'error'
): void {
  if (!config) return;

  // 条件付きスタイルがある場合はそれを優先
  const activeConfig = condition && config.conditionalStyles?.[condition]
    ? { ...config, ...config.conditionalStyles[condition] }
    : config;

  // クラス名を適用
  if (activeConfig.className) {
    const classes = activeConfig.className.split(' ').filter(Boolean);
    element.classList.add(...classes);
  }

  // インラインスタイルを適用
  if (activeConfig.style) {
    Object.entries(activeConfig.style).forEach(([key, value]) => {
      // CSSプロパティ名をキャメルケースからケバブケースに変換
      const cssProperty = key.replace(/([A-Z])/g, '-$1').toLowerCase();
      element.style.setProperty(cssProperty, value);
    });
  }
}

/**
 * グローバルCSSを適用
 * @param globalCss CSSコード
 * @returns クリーンアップ関数
 */
export function applyGlobalCss(globalCss: string | null | undefined): (() => void) | null {
  if (!globalCss) return null;

  const styleId = 'custom-form-global-css';
  let styleElement = document.getElementById(styleId) as HTMLStyleElement;

  if (!styleElement) {
    styleElement = document.createElement('style');
    styleElement.id = styleId;
    document.head.appendChild(styleElement);
  }

  styleElement.textContent = globalCss;

  return () => {
    if (styleElement && styleElement.parentNode) {
      styleElement.parentNode.removeChild(styleElement);
    }
  };
}
```

#### 1.2 Reactコンポーネントでの使用

```typescript
// PublicFormViewPage.tsx での使用例

import { applyElementStyle, applyGlobalCss, CustomStyleConfig } from '../../utils/customStyle';

// コンポーネント内で
const customStyleConfig: CustomStyleConfig | undefined = form?.custom_style_config;

// グローバルCSSを適用
useEffect(() => {
  const cleanup = applyGlobalCss(customStyleConfig?.globalCss);
  return () => {
    if (cleanup) cleanup();
  };
}, [customStyleConfig?.globalCss]);

// 要素にスタイルを適用
const containerRef = useRef<HTMLDivElement>(null);
useEffect(() => {
  if (containerRef.current && customStyleConfig?.elements.container) {
    applyElementStyle(containerRef.current, customStyleConfig.elements.container);
  }
}, [customStyleConfig?.elements.container]);

// JSXでの使用
<Card
  ref={cardRef}
  className={customStyleConfig?.elements.card?.className || ''}
  style={{
    ...(form?.theme_tokens?.color_bg ? { backgroundColor: form.theme_tokens.color_bg } : {}),
    ...(customStyleConfig?.elements.card?.style || {}),
  }}
>
```

### 2. バックエンド側の実装

#### 2.1 データベースマイグレーション

```php
// database/migrations/xxxx_add_custom_style_config_to_forms.php

Schema::table('forms', function (Blueprint $table) {
    $table->json('custom_style_config')->nullable()->after('theme_tokens');
});
```

#### 2.2 モデルの更新

```php
// app/Models/Form.php

protected $casts = [
    // ... 既存のキャスト
    'custom_style_config' => 'array',
];
```

#### 2.3 APIレスポンスの更新

```php
// app/Http/Controllers/Api/Public/FormsController.php

public function show($form_key)
{
    $form = Form::where('form_key', $form_key)
        ->with(['fields', 'translations'])
        ->firstOrFail();

    return response()->json([
        'data' => [
            'form' => [
                // ... 既存のフィールド
                'custom_style_config' => $form->custom_style_config,
            ],
        ],
    ]);
}
```

### 3. フィールド編集画面でのヘルプテキスト設定UI

#### 3.1 設定UIの配置

- フィールド編集画面（項目設定）に「ヘルプテキスト」セクションを追加
- ラベル設定の下に配置

#### 3.2 UIコンポーネント（フィールド編集）

```typescript
// フィールド編集コンポーネントに追加

<div className="space-y-2">
  <label className="flex items-center gap-2 cursor-pointer">
    <input
      type="checkbox"
      checked={fieldOptions.help_text_enabled ?? false}
      onChange={(e) => {
        setFieldOptions({
          ...fieldOptions,
          help_text_enabled: e.target.checked,
        });
      }}
      className="rounded border-white/20 bg-black/30 text-brand-gold focus:ring-brand-gold/30"
    />
    <span className="text-sm font-bold">ヘルプテキストを表示する</span>
  </label>
  
  {fieldOptions.help_text_enabled && (
    <div className="space-y-2 pl-6">
      <label className="block text-sm font-bold">ヘルプテキスト（日本語）</label>
      <textarea
        value={fieldOptions.help_text_i18n?.ja || ''}
        onChange={(e) => {
          setFieldOptions({
            ...fieldOptions,
            help_text_i18n: {
              ...fieldOptions.help_text_i18n,
              ja: e.target.value,
            },
          });
        }}
        placeholder="ヘルプテキストを入力してください"
        rows={2}
        className="w-full rounded-xl border border-white/10 bg-black/30 px-3 py-2 text-sm"
      />
      
      <label className="block text-sm font-bold">ヘルプテキスト（英語）</label>
      <textarea
        value={fieldOptions.help_text_i18n?.en || ''}
        onChange={(e) => {
          setFieldOptions({
            ...fieldOptions,
            help_text_i18n: {
              ...fieldOptions.help_text_i18n,
              en: e.target.value,
            },
          });
        }}
        placeholder="Help text (English)"
        rows={2}
        className="w-full rounded-xl border border-white/10 bg-black/30 px-3 py-2 text-sm"
      />
    </div>
  )}
</div>
```

#### 3.3 公開フォームでのヘルプテキスト表示実装例

```typescript
// PublicFormViewPage.tsx での実装例

function FieldComponent({ field, value, onChange, error, locale, themeTokens, customStyleConfig }: FieldComponentProps) {
  const getLabel = () => {
    if (field.options_json?.labels?.[locale]) {
      return field.options_json.labels[locale];
    }
    return field.options_json?.label || field.field_key;
  };

  const getHelpText = () => {
    if (!field.options_json?.help_text_enabled) return null;
    return field.options_json.help_text_i18n?.[locale] 
      || field.options_json.help_text_i18n?.["ja"] 
      || field.options_json.help_text_i18n?.["en"] 
      || null;
  };

  const helpText = getHelpText();

  return (
    <div className="space-y-1">
      <label 
        className="block text-xs text-white/70"
        style={{
          color: themeTokens?.color_text || undefined,
        }}
      >
        {getLabel()}
        {field.is_required && <span className="text-red-400 ml-1">*</span>}
        {helpText && (
          <span 
            className={customStyleConfig?.elements.helpTextIcon?.className || "ml-1 cursor-help"}
            style={customStyleConfig?.elements.helpTextIcon?.style}
            title={helpText}
          >
            ?
          </span>
        )}
      </label>
      
      {helpText && (
        <div 
          className={customStyleConfig?.elements.helpText?.className || "text-sm text-white/60 mt-1"}
          style={customStyleConfig?.elements.helpText?.style}
        >
          {helpText}
        </div>
      )}
      
      {/* 入力フィールド */}
      <input
        type="text"
        value={value || ''}
        onChange={(e) => onChange(e.target.value)}
        // ... その他のプロパティ
      />
    </div>
  );
}
```

### 4. フォーム編集画面でのカスタムスタイル設定UI

#### 4.1 設定UIの配置

- フォーム編集画面の「デザイン設定」セクションに追加
- **既存のテーマ設定を置き換え**（新しいスタイル設定UIに統一）

#### 4.2 UI設計の全体像

```
┌─────────────────────────────────────────────────────────┐
│ デザイン設定                                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ [プリセットテーマ選択]                                   │
│ ┌───────────────────────────────────────────────────┐ │
│ │ ○ ダークテーマ                                     │ │
│ │ ○ ライトテーマ                                     │ │
│ │ ○ ReFormaテーマ                                    │ │
│ │ ○ クラッシックテーマ（フラット）                   │ │
│ │ ○ カスタム（詳細設定）                             │ │
│ └───────────────────────────────────────────────────┘ │
│                                                         │
│ [ヘッダ/フッタ設定]                                      │
│ ┌───────────────────────────────────────────────────┐ │
│ │ ☑ ヘッダ領域を表示する                             │ │
│ │   [ヘッダHTML入力エリア]                           │ │
│ │   ┌─────────────────────────────────────────────┐ │ │
│ │   │ <textarea rows="5">                         │ │ │
│ │   │ </textarea>                                 │ │ │
│ │   └─────────────────────────────────────────────┘ │ │
│ │                                                     │ │
│ │ ☑ フッタ領域を表示する                             │ │
│ │   [フッタHTML入力エリア]                           │ │
│ │   ┌─────────────────────────────────────────────┐ │ │
│ │   │ <textarea rows="5">                         │ │ │
│ │   │ </textarea>                                 │ │ │
│ │   └─────────────────────────────────────────────┘ │ │
│ └───────────────────────────────────────────────────┘ │
│                                                         │
│ [詳細カスタマイズ] ※ カスタム選択時のみ表示            │
│ ┌───────────────────────────────────────────────────┐ │
│ │ [アコーディオン] コンテナ                          │ │
│ │ [アコーディオン] ヘッダ領域                        │ │
│ │ [アコーディオン] コンテンツ領域                    │ │
│ │ [アコーディオン] フッタ領域                        │ │
│ │ [アコーディオン] カード                            │ │
│ │ [アコーディオン] タイトル                          │ │
│ │ [アコーディオン] フィールドラベル                  │ │
│ │ [アコーディオン] 入力フィールド                    │ │
│ │ [アコーディオン] ボタン（プライマリ）              │ │
│ │ [アコーディオン] ボタン（セカンダリ）              │ │
│ │ [アコーディオン] ヘルプテキスト                    │ │
│ │ [アコーディオン] エラーメッセージ                  │ │
│ │ ... その他の要素                                   │ │
│ └───────────────────────────────────────────────────┘ │
│                                                         │
│ [グローバルCSS] ※ カスタム選択時のみ表示               │
│ ┌───────────────────────────────────────────────────┐ │
│ │ <textarea rows="10" placeholder="カスタムCSS">    │ │
│ │ </textarea>                                       │ │
│ └───────────────────────────────────────────────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

#### 4.3 プリセットテーマ選択UI

```typescript
// FormEditIntegratedPage.tsx に追加

// プリセットテーマの定義
const PRESET_THEMES = {
  dark: {
    name: "ダークテーマ",
    description: "暗い背景色と明るい文字色のテーマ",
    config: {
      // プリセットのスタイル設定
      elements: {
        container: { style: { backgroundColor: "#1a1a1a", color: "#ffffff" } },
        card: { style: { backgroundColor: "#2d2d2d", borderRadius: "8px" } },
        // ... その他の要素設定
      }
    }
  },
  light: {
    name: "ライトテーマ",
    description: "明るい背景色と暗い文字色のテーマ",
    config: {
      elements: {
        container: { style: { backgroundColor: "#f5f5f5", color: "#333333" } },
        card: { style: { backgroundColor: "#ffffff", borderRadius: "8px", boxShadow: "0 2px 4px rgba(0,0,0,0.1)" } },
        // ... その他の要素設定
      }
    }
  },
  reforma: {
    name: "ReFormaテーマ",
    description: "ReFormaのブランドカラーを使用したテーマ",
    config: {
      elements: {
        container: { style: { backgroundColor: "#000000", color: "#ffffff" } },
        card: { style: { backgroundColor: "#1a1a1a", borderColor: "#d4af37" } },
        buttonPrimary: { style: { backgroundColor: "#d4af37", color: "#000000" } },
        // ... その他の要素設定
      }
    }
  },
  classic: {
    name: "クラッシックテーマ",
    description: "カード表現を使わないフラットなデザイン",
    config: {
      elements: {
        container: { style: { backgroundColor: "#ffffff", color: "#333333" } },
        card: { style: { backgroundColor: "transparent", boxShadow: "none", border: "none" } },
        cardBody: { style: { padding: "0" } },
        // ... その他の要素設定
      }
    }
  }
};

// UIコンポーネント
<div className="space-y-4">
  <h3 className="text-lg font-bold">テーマ設定</h3>
  
  {/* プリセットテーマ選択 */}
  <div className="space-y-2">
    <label className="block text-sm font-bold mb-2">プリセットテーマ</label>
    <div className="grid grid-cols-2 gap-3">
      {Object.entries(PRESET_THEMES).map(([key, theme]) => (
        <label
          key={key}
          className={`flex items-start gap-3 p-4 rounded-xl border-2 cursor-pointer transition-all ${
            customStyleConfig.presetTheme === key
              ? "border-brand-gold bg-brand-gold/10"
              : "border-white/10 bg-white/5 hover:bg-white/10"
          }`}
        >
          <input
            type="radio"
            name="presetTheme"
            value={key}
            checked={customStyleConfig.presetTheme === key}
            onChange={(e) => {
              if (e.target.checked) {
                // プリセットテーマを適用
                setCustomStyleConfig({
                  ...PRESET_THEMES[key].config,
                  presetTheme: key,
                  headerEnabled: customStyleConfig.headerEnabled ?? false,
                  footerEnabled: customStyleConfig.footerEnabled ?? false,
                  headerHtml: customStyleConfig.headerHtml,
                  footerHtml: customStyleConfig.footerHtml,
                });
              }
            }}
            className="mt-1"
          />
          <div className="flex-1">
            <div className="font-bold text-sm">{theme.name}</div>
            <div className="text-xs text-white/60 mt-1">{theme.description}</div>
          </div>
        </label>
      ))}
      
      {/* カスタム選択 */}
      <label
        className={`flex items-start gap-3 p-4 rounded-xl border-2 cursor-pointer transition-all ${
          customStyleConfig.presetTheme === "custom" || !customStyleConfig.presetTheme
            ? "border-brand-gold bg-brand-gold/10"
            : "border-white/10 bg-white/5 hover:bg-white/10"
        }`}
      >
        <input
          type="radio"
          name="presetTheme"
          value="custom"
          checked={customStyleConfig.presetTheme === "custom" || !customStyleConfig.presetTheme}
          onChange={(e) => {
            if (e.target.checked) {
              setCustomStyleConfig({
                ...customStyleConfig,
                presetTheme: "custom",
              });
            }
          }}
          className="mt-1"
        />
        <div className="flex-1">
          <div className="font-bold text-sm">カスタム（詳細設定）</div>
          <div className="text-xs text-white/60 mt-1">各要素を個別にカスタマイズ</div>
        </div>
      </label>
    </div>
  </div>
</div>
```

#### 4.4 ヘッダ/フッタ設定UI

```typescript
// ヘッダ/フッタ設定
<div className="space-y-4">
  <h3 className="text-lg font-bold">ヘッダ/フッタ設定</h3>
  
  {/* ヘッダ設定 */}
  <div className="space-y-2">
    <label className="flex items-center gap-2 cursor-pointer">
      <input
        type="checkbox"
        checked={customStyleConfig.headerEnabled ?? false}
        onChange={(e) => {
          setCustomStyleConfig({
            ...customStyleConfig,
            headerEnabled: e.target.checked,
            headerHtml: e.target.checked ? customStyleConfig.headerHtml : null,
          });
        }}
        className="rounded border-white/20 bg-black/30 text-brand-gold focus:ring-brand-gold/30"
      />
      <span className="text-sm font-bold">ヘッダ領域を表示する</span>
    </label>
    
    {customStyleConfig.headerEnabled && (
      <div className="pl-6 space-y-2">
        <label className="block text-sm font-bold">ヘッダHTML</label>
        <textarea
          value={customStyleConfig.headerHtml || ''}
          onChange={(e) => {
            setCustomStyleConfig({
              ...customStyleConfig,
              headerHtml: e.target.value || null,
            });
          }}
          placeholder="<div>カスタムヘッダコンテンツ</div>"
          rows={5}
          className="w-full rounded-xl border border-white/10 bg-black/30 px-3 py-2 text-sm font-mono"
        />
        <p className="text-xs text-white/60">
          HTMLタグが使用可能です。デフォルトのロゴ・タイトル表示を上書きします。
        </p>
      </div>
    )}
  </div>
  
  {/* フッタ設定 */}
  <div className="space-y-2">
    <label className="flex items-center gap-2 cursor-pointer">
      <input
        type="checkbox"
        checked={customStyleConfig.footerEnabled ?? false}
        onChange={(e) => {
          setCustomStyleConfig({
            ...customStyleConfig,
            footerEnabled: e.target.checked,
            footerHtml: e.target.checked ? customStyleConfig.footerHtml : null,
          });
        }}
        className="rounded border-white/20 bg-black/30 text-brand-gold focus:ring-brand-gold/30"
      />
      <span className="text-sm font-bold">フッタ領域を表示する</span>
    </label>
    
    {customStyleConfig.footerEnabled && (
      <div className="pl-6 space-y-2">
        <label className="block text-sm font-bold">フッタHTML</label>
        <textarea
          value={customStyleConfig.footerHtml || ''}
          onChange={(e) => {
            setCustomStyleConfig({
              ...customStyleConfig,
              footerHtml: e.target.value || null,
            });
          }}
          placeholder="<div>© 2024 カスタムフッタ</div>"
          rows={5}
          className="w-full rounded-xl border border-white/10 bg-black/30 px-3 py-2 text-sm font-mono"
        />
        <p className="text-xs text-white/60">
          HTMLタグが使用可能です。デフォルトのコピーライト表示を上書きします。
        </p>
      </div>
    )}
  </div>
</div>
```

#### 4.5 詳細カスタマイズUI（カスタム選択時のみ表示）

```typescript
// カスタム選択時のみ表示される詳細設定
{customStyleConfig.presetTheme === "custom" || !customStyleConfig.presetTheme ? (
  <div className="space-y-4">
    <h3 className="text-lg font-bold">詳細カスタマイズ</h3>
    
    {/* アコーディオン形式で各要素を設定 */}
    <Accordion>
      {/* コンテナ */}
      <AccordionItem title="コンテナ">
        <ElementStyleEditor
          config={customStyleConfig.elements.container}
          onChange={(config) => {
            setCustomStyleConfig({
              ...customStyleConfig,
              elements: {
                ...customStyleConfig.elements,
                container: config,
              },
            });
          }}
        />
      </AccordionItem>
      
      {/* ヘッダ領域 */}
      <AccordionItem title="ヘッダ領域">
        <ElementStyleEditor
          config={customStyleConfig.elements.header}
          onChange={(config) => {
            setCustomStyleConfig({
              ...customStyleConfig,
              elements: {
                ...customStyleConfig.elements,
                header: config,
              },
            });
          }}
        />
      </AccordionItem>
      
      {/* その他の要素も同様に */}
      {/* ... */}
    </Accordion>
    
    {/* グローバルCSS */}
    <div className="space-y-2">
      <label className="block text-sm font-bold">グローバルCSS</label>
      <textarea
        value={customStyleConfig.globalCss || ''}
        onChange={(e) => {
          setCustomStyleConfig({
            ...customStyleConfig,
            globalCss: e.target.value || null,
          });
        }}
        placeholder=".custom-class { color: red; }"
        rows={10}
        className="w-full rounded-xl border border-white/10 bg-black/30 px-3 py-2 text-sm font-mono"
      />
    </div>
  </div>
) : null}
```

#### 4.6 要素スタイルエディタコンポーネント

```typescript
// ElementStyleEditor.tsx

interface ElementStyleEditorProps {
  config?: ElementStyleConfig;
  onChange: (config: ElementStyleConfig) => void;
}

function ElementStyleEditor({ config, onChange }: ElementStyleEditorProps) {
  const [className, setClassName] = useState(config?.className || '');
  const [styleText, setStyleText] = useState(() => {
    // styleオブジェクトを文字列に変換（簡易版）
    if (!config?.style) return '';
    return Object.entries(config.style)
      .map(([key, value]) => `${key}: ${value};`)
      .join('\n');
  });

  const handleClassNameChange = (value: string) => {
    setClassName(value);
    onChange({
      ...config,
      className: value || null,
    });
  };

  const handleStyleTextChange = (value: string) => {
    setStyleText(value);
    // 文字列をstyleオブジェクトに変換（簡易版）
    const styleObj: Record<string, string> = {};
    value.split('\n').forEach((line) => {
      const match = line.match(/^\s*([^:]+):\s*(.+?);?\s*$/);
      if (match) {
        const [, key, val] = match;
        // ケバブケースをキャメルケースに変換
        const camelKey = key.replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
        styleObj[camelKey] = val.trim();
      }
    });
    onChange({
      ...config,
      style: Object.keys(styleObj).length > 0 ? styleObj : null,
    });
  };

  return (
    <div className="space-y-3">
      {/* CSSクラス名 */}
      <div>
        <label className="block text-xs font-bold mb-1">CSSクラス名</label>
        <input
          type="text"
          value={className}
          onChange={(e) => handleClassNameChange(e.target.value)}
          placeholder="custom-class another-class"
          className="w-full rounded-xl border border-white/10 bg-black/30 px-3 py-2 text-sm"
        />
        <p className="text-xs text-white/60 mt-1">複数のクラスはスペース区切り</p>
      </div>
      
      {/* インラインスタイル */}
      <div>
        <label className="block text-xs font-bold mb-1">インラインスタイル</label>
        <textarea
          value={styleText}
          onChange={(e) => handleStyleTextChange(e.target.value)}
          placeholder="backgroundColor: #ffffff;&#10;color: #333333;"
          rows={5}
          className="w-full rounded-xl border border-white/10 bg-black/30 px-3 py-2 text-sm font-mono"
        />
        <p className="text-xs text-white/60 mt-1">
          形式: property: value; （1行に1つ）
        </p>
      </div>
    </div>
  );
}
```

#### 4.7 UIコンポーネント（旧実装）

```typescript
// FormEditIntegratedPage.tsx に追加

// カスタムスタイル設定の状態
const [customStyleConfig, setCustomStyleConfig] = useState<CustomStyleConfig>({
  elements: {},
  globalCss: null,
  headerHtml: null,
  footerHtml: null,
});

// UIコンポーネント
<div className="space-y-4">
  <h3 className="text-lg font-bold">カスタムスタイル設定</h3>
  
  {/* 要素ごとの設定 */}
  <div className="space-y-4">
    <div>
      <label className="block text-sm font-bold mb-2">コンテナ</label>
      <input
        type="text"
        placeholder="CSSクラス名（例: custom-container）"
        value={customStyleConfig.elements.container?.className || ''}
        onChange={(e) => {
          setCustomStyleConfig({
            ...customStyleConfig,
            elements: {
              ...customStyleConfig.elements,
              container: {
                ...customStyleConfig.elements.container,
                className: e.target.value || null,
              },
            },
          });
        }}
      />
    </div>
    
    {/* 他の要素も同様に設定 */}
  </div>
  
  {/* グローバルCSS */}
  <div>
    <label className="block text-sm font-bold mb-2">グローバルCSS</label>
    <textarea
      placeholder="カスタムCSSコードを入力"
      rows={10}
      value={customStyleConfig.globalCss || ''}
      onChange={(e) => {
        setCustomStyleConfig({
          ...customStyleConfig,
          globalCss: e.target.value || null,
        });
      }}
    />
  </div>
</div>
```

## メリット

1. **柔軟性**: 既存のテーマトークンでは対応できない細かいデザイン要求に対応可能
2. **拡張性**: 新しい要素タイプを簡単に追加可能
3. **後方互換性**: 既存のテーマトークン機能と併用可能
4. **保守性**: 要素タイプごとに設定を分離することで管理が容易

## 注意点

1. **セキュリティ**: 
   - グローバルCSSにはXSS対策が必要（サニタイズ）
   - ヘッダ/フッタHTMLは基本的なサニタイズのみ（バリデーションはほぼ無し）
2. **パフォーマンス**: 大量のインラインスタイルはパフォーマンスに影響する可能性
3. **バリデーション**: 
   - HTML入力は基本的なサニタイズのみ（危険なタグの除去など）
   - CSSコードの入力チェックは最小限（構文チェックは行わない）
4. **プレビュー**: リアルタイムプレビューで即座に反映されるようにする
5. **既存テーマ機能の移行**: 
   - 既存のテーマトークン設定を新しいスタイル設定に自動変換する機能を検討
   - または、既存テーマをプリセットテーマとして提供

## スタイル適用マッピング表

各要素タイプとその適用箇所の対応表：

| 要素タイプ | 適用箇所 | HTML要素 | 説明 |
|-----------|---------|---------|------|
| `container` | フォーム全体のラッパー | `<div data-form-container>` | 最外側のコンテナ |
| `header` | ヘッダ領域 | `<header>` | 固定表示のヘッダ |
| `content` | コンテンツ領域 | `<div>` | STEP/GROUP/FIELDの制御領域 |
| `footer` | フッタ領域 | `<footer>` | フッタ表示 |
| `card` | フォームカード | `<Card>` | カードコンポーネント |
| `cardBody` | カードボディ | `<CardBody>` | カード内のコンテンツ領域 |
| `headerCard` | ヘッダーカード | `<Card>` | ロゴ・タイトル用カード |
| `title` | フォームタイトル | `<h1>` | フォーム名 |
| `description` | フォーム説明文 | `<p>` | フォーム説明 |
| `fieldLabel` | フィールドラベル | `<label>` | 各フィールドのラベル |
| `input` | 入力フィールド | `<input>`, `<textarea>`, `<select>` | 各種入力要素 |
| `button` | ボタン（汎用） | `<button>` | 汎用ボタン |
| `buttonPrimary` | プライマリボタン | `<button>` | 送信、次へ等の主要ボタン |
| `buttonSecondary` | セカンダリボタン | `<button>` | 戻る、キャンセル等の補助ボタン |
| `stepTab` | STEPタブ | `<button>` | STEP式フォームのタブ |
| `stepTabActive` | STEPタブ（アクティブ） | `<button>` | 現在選択中のSTEPタブ |
| `groupName` | GROUP名 | `<h3>` | グループ名表示 |
| `errorMessage` | エラーメッセージ | `<div>` | バリデーションエラー表示 |
| `confirmationSection` | 確認画面セクション | `<div>` | 確認画面の各セクション |
| `helpText` | ヘルプテキスト | `<div>` | フィールドのヘルプテキスト |
| `helpTextIcon` | ヘルプアイコン | `<span>` | ヘルプアイコン（?） |

## 実装優先度

1. **Phase 1**: プリセットテーマ機能（ダーク、ライト、ReForma、クラッシック）
2. **Phase 2**: ヘッダ/フッタ領域のON/OFF機能とHTML入力
3. **Phase 3**: 基本的な要素スタイル設定（className, style）の詳細カスタマイズUI
4. **Phase 4**: グローバルCSS機能
5. **Phase 5**: ヘルプテキスト機能（フィールド設定、表示、スタイル設定）
6. **Phase 6**: 条件付きスタイル（hover, focus等）
7. **Phase 7**: 設定UIの充実（プレビュー機能付き、リアルタイム反映）

## 代替案

### 案1: CSS変数ベースのアプローチ

テーマトークンを拡張し、より多くのCSS変数を定義する方法。ただし、柔軟性は劣る。

### 案2: テンプレートシステム

複数のプリセットテンプレートから選択する方法。カスタマイズ性は劣るが、実装が簡単。

### 案3: 外部CSSファイルのアップロード

CSSファイルをアップロードして適用する方法。柔軟性は高いが、管理が複雑。

## プリセットテーマの変更方法

プリセットテーマ（Dark、Light、ReForma、Classic）を変更する場合は、以下の2つのファイルを同期して修正する必要があります。

### 修正が必要なファイル

1. **バックエンド**: `database/seeders/ThemeSeeder.php`
   - データベースに保存されるプリセットテーマの定義
   - `ThemeSeeder`を実行すると、この定義がデータベースに反映されます
   - 各テーマの`custom_style_config`を修正します

2. **フロントエンド**: `src/constants/presetThemes.ts`
   - フロントエンドで使用されるプリセットテーマの定義
   - フォーム編集画面でプリセットテーマを選択した際に使用されます
   - バックエンドの`ThemeSeeder.php`と**必ず同期**させる必要があります

### 修正手順

1. **バックエンドの修正**
   ```php
   // database/seeders/ThemeSeeder.php
   [
       'code' => 'dark',  // テーマコード
       'name' => 'ダークテーマ',
       'description' => 'ダークモード対応テーマ',
       'theme_tokens' => [
           // theme_tokensは今後使用しない方向だが、後方互換性のため残す
       ],
       'custom_style_config' => [
           'presetTheme' => 'dark',
           'headerEnabled' => true,
           'footerEnabled' => true,
           'globalCss' => ':root { --spacing-scale: 1rem; }',
           'elements' => [
               'container' => [
                   'style' => [
                       'backgroundColor' => '#020617',
                       'color' => '#f1f5f9',
                       'fontFamily' => 'system-ui, -apple-system, sans-serif',
                   ],
               ],
               // ... その他の要素
           ],
       ],
   ],
   ```

2. **フロントエンドの修正**
   ```typescript
   // src/constants/presetThemes.ts
   export const PRESET_THEMES: Record<string, CustomStyleConfig> = {
     dark: {
       presetTheme: 'dark',
       headerEnabled: true,
       footerEnabled: true,
       globalCss: ':root { --spacing-scale: 1rem; }',
       elements: {
         container: {
           style: {
             backgroundColor: '#020617',
             color: '#f1f5f9',
             fontFamily: 'system-ui, -apple-system, sans-serif',
           },
         },
         // ... その他の要素（バックエンドと同じ値にする）
       },
     },
   };
   ```

3. **データベースへの反映**
   - バックエンドのSeederを実行: `php artisan db:seed --class=ThemeSeeder`
   - 既存のテーマデータが削除され、新しい定義で再作成されます

### 注意点

1. **バックエンドとフロントエンドの同期**
   - `ThemeSeeder.php`と`presetThemes.ts`の`custom_style_config`は**必ず同じ値**にする必要があります
   - 不一致があると、フォーム編集画面で選択したプリセットテーマと、データベースに保存される値が異なる可能性があります

2. **theme_tokens について**
   - 今後は`theme_tokens`を使わない方向ですが、後方互換性のため残しています
   - 新しい設定は`custom_style_config`に追加してください
   - `theme_tokens`の設定（`radius`, `spacing_scale`, `font_family`, `button_style`, `input_style`など）は`custom_style_config`に移行済みです

3. **プリセットテーマの追加**
   - 新しいプリセットテーマを追加する場合は、両方のファイルに追加する必要があります
   - `PRESET_THEME_NAMES`配列にも追加が必要です（フロントエンド）

4. **既存フォームへの影響**
   - 既存のフォームでプリセットテーマを使用している場合、Seederを実行すると新しい定義が適用されます
   - ただし、フォーム個別に`custom_style_config`が設定されている場合は、その設定が優先されます

## 結論

提案するカスタムスタイル設定機能により、既存のテーマトークン機能を補完し、より柔軟なデザインカスタマイズが可能になります。段階的な実装により、リスクを抑えながら機能を拡張できます。
