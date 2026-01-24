# 規約/同意文章スクロール検知機能と表形式フィールドの改修提案

**作成日**: 2026-01-20  
**参照**: VALIDATION_RULES_STATUS.md

---

## 1. 規約/同意文章のスクロール検知機能

### 1.1 現状の実装状況

#### ✅ 既存機能
- `terms`フィールドタイプが存在
- チェックボックスによる同意機能は実装済み
- バリデーション（必須チェック）は実装済み

#### ❌ 未実装機能
- **規約/同意文章の表示エリア**: 現在は単純なチェックボックスのみ
- **スクロール検知機能**: 文書エリアが最後までスクロールされたかを検知する機能が未実装
- **スクロール検知に基づくバリデーション**: スクロール完了を条件とするバリデーションが未実装

### 1.2 既存機能での実現可能性

**結論**: ❌ **既存機能では実現不可能**

理由:
1. `terms`フィールドタイプは単純なチェックボックスのみで、文章表示エリアを持たない
2. スクロール検知機能が実装されていない
3. バリデーションルールに「スクロール完了」という条件が存在しない

### 1.3 改修案

#### 1.3.1 概要

`terms`フィールドタイプを拡張し、以下の機能を追加:
- 規約/同意文章の表示エリア（スクロール可能）
- スクロール位置の検知
- スクロール完了を条件とするバリデーション

#### 1.3.2 options_json の構造拡張

```json
{
  "label": "利用規約に同意する",
  "labels": {
    "ja": "利用規約に同意する",
    "en": "I agree to the Terms of Service"
  },
  "validation": {
    "require_scroll_to_bottom": true,
    "scroll_tolerance": 10
  },
  "content": {
    "type": "text",
    "text": "利用規約の本文...",
    "height": "300px"
  }
}
```

または、外部コンテンツを参照する場合:

```json
{
  "label": "利用規約に同意する",
  "validation": {
    "require_scroll_to_bottom": true,
    "scroll_tolerance": 10
  },
  "content": {
    "type": "url",
    "url": "https://example.com/terms.html",
    "height": "400px"
  }
}
```

**パラメータ説明**:
- `validation.require_scroll_to_bottom`: スクロール完了を必須とするか（boolean）
- `validation.scroll_tolerance`: スクロール完了判定の許容誤差（ピクセル、デフォルト: 10px）
- `content.type`: コンテンツタイプ（`text` | `url`）
- `content.text`: テキストコンテンツ（`type: "text"`の場合）
- `content.url`: 外部URL（`type: "url"`の場合）
- `content.height`: 表示エリアの高さ（CSS値、例: "300px", "50vh"）

#### 1.3.3 フロントエンド実装

**ファイル**: `src/pages/public/PublicFormViewPage.tsx`

```typescript
// termsフィールドのレンダリングを拡張
case "terms":
  const requireScroll = field.options_json?.validation?.require_scroll_to_bottom ?? false;
  const scrollTolerance = field.options_json?.validation?.scroll_tolerance ?? 10;
  const content = field.options_json?.content;
  const [isScrolledToBottom, setIsScrolledToBottom] = useState(false);
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  // スクロール検知
  const handleScroll = useCallback(() => {
    if (!scrollContainerRef.current) return;
    const container = scrollContainerRef.current;
    const scrollTop = container.scrollTop;
    const scrollHeight = container.scrollHeight;
    const clientHeight = container.clientHeight;
    const isAtBottom = scrollHeight - scrollTop - clientHeight <= scrollTolerance;
    setIsScrolledToBottom(isAtBottom);
  }, [scrollTolerance]);

  // スクロール完了時のバリデーション状態更新
  useEffect(() => {
    if (isScrolledToBottom && requireScroll) {
      // スクロール完了を条件として、チェックボックスを有効化
      // または、自動的にチェック状態を更新
    }
  }, [isScrolledToBottom, requireScroll]);

  return (
    <div className="space-y-3">
      {/* 規約/同意文章の表示エリア */}
      {content && (
        <div
          ref={scrollContainerRef}
          onScroll={handleScroll}
          className="border border-white/10 rounded-xl bg-black/20 p-4 overflow-y-auto"
          style={{ height: content.height || "300px" }}
        >
          {content.type === "text" && (
            <div className="text-sm text-white/80 whitespace-pre-wrap">
              {content.text}
            </div>
          )}
          {content.type === "url" && (
            <iframe
              src={content.url}
              className="w-full h-full border-0"
              title="Terms and Conditions"
            />
          )}
        </div>
      )}

      {/* スクロール完了インジケーター */}
      {requireScroll && (
        <div className="text-xs text-white/60">
          {isScrolledToBottom ? (
            <span className="text-green-400">✓ 最後まで読みました</span>
          ) : (
            <span>最後までスクロールしてください</span>
          )}
        </div>
      )}

      {/* チェックボックス */}
      <label className="flex items-center gap-2 cursor-pointer">
        <input
          type="checkbox"
          checked={value === true || value === "true" || value === 1}
          onChange={(e) => onChange(e.target.checked)}
          disabled={requireScroll && !isScrolledToBottom}
          className="rounded border-white/20 bg-black/30 text-brand-gold focus:ring-brand-gold/30 disabled:opacity-50"
        />
        <span className="text-sm text-white/80">
          {field.options_json?.label || "同意する"}
        </span>
      </label>
    </div>
  );
```

#### 1.3.4 バリデーション実装

**ファイル**: `src/pages/public/PublicFormViewPage.tsx` の `validate()` 関数

```typescript
const validate = (): boolean => {
  if (!form || !conditionState) return false;

  const newErrors: Record<string, string> = {};

  form.fields.forEach((field) => {
    const fieldState = conditionState.fields[field.field_key];
    if (!fieldState) return;

    if (!fieldState.visible) return;

    const value = answers[field.field_key];

    // termsフィールドの特別なバリデーション
    if (field.type === "terms" && fieldState.required) {
      const requireScroll = field.options_json?.validation?.require_scroll_to_bottom ?? false;
      
      // スクロール完了チェック（フロントエンド状態から取得）
      if (requireScroll) {
        const scrollState = scrollStates[field.field_key]; // スクロール状態を管理
        if (!scrollState?.isScrolledToBottom) {
          const label = field.options_json?.label || field.field_key;
          newErrors[field.field_key] = `${label}を確認するため、最後までスクロールしてください`;
          return;
        }
      }

      // チェックボックスチェック
      if (value !== true && value !== "true" && value !== 1) {
        const label = field.options_json?.label || field.field_key;
        newErrors[field.field_key] = `${label}は必須です`;
        return;
      }
    }

    // その他のバリデーション...
  });

  setErrors(newErrors);
  return Object.keys(newErrors).length === 0;
};
```

#### 1.3.5 バックエンド実装

**ファイル**: `app/Http/Controllers/Api/V1/PublicFormsController.php`

バックエンドでは、スクロール完了の検証は困難なため、フロントエンドで検証済みであることを前提とする。
ただし、`terms`フィールドの必須チェックは既存のロジックで対応可能。

```php
// 既存の必須チェックロジックで対応
// スクロール完了の検証はフロントエンドで行い、
// チェックボックスがチェックされていることを確認する
```

#### 1.3.6 実装の優先順位

**優先度: 中**

理由:
- ユーザビリティ向上に寄与するが、必須機能ではない
- 実装コストは中程度（フロントエンド中心の実装）

---

## 2. 表形式フィールド（マトリクス）

### 2.1 現状の実装状況

#### ✅ 既存機能
- `checkbox`: 複数選択可能
- `radio`: 単一選択
- `date`: 日付入力

#### ❌ 未実装機能
- **表形式フィールド**: ヘッダ（列）×項目（行）のマトリクス表示
- **ヘッダチェック機能**: 項目ヘッダをチェックすると、そのヘッダの全項目が選択される
- **選択制限**: チェックボックス/ラジオボタンでの選択制限（全体/ヘッダ単位）
- **選択数制限**: チェックボックスで全体でいくつ選択可能かの制限

### 2.2 既存機能での実現可能性

**結論**: ❌ **既存機能では実現不可能**

理由:
1. 表形式（マトリクス）のフィールドタイプが存在しない
2. 項目ヘッダと項目の関連付け機能が存在しない
3. ヘッダチェックによる一括選択機能が存在しない
4. 選択制限（全体/ヘッダ単位）の設定機能が存在しない

### 2.3 改修案

#### 2.3.1 概要

新しいフィールドタイプ `matrix` を追加:
- 項目ヘッダ（列）× 項目（行）のマトリクス表示
- チェックボックス/ラジオボタンの選択モード
- ヘッダチェックによる一括選択（チェックボックスのみ）
- 選択制限（全体/ヘッダ単位）

#### 2.3.2 options_json の構造

```json
{
  "label": "希望日時を選択してください",
  "labels": {
    "ja": "希望日時を選択してください",
    "en": "Please select your preferred dates"
  },
  "matrix": {
    "headers": [
      { "value": "2024-10-01", "labels": { "ja": "10月1日", "en": "October 1" } },
      { "value": "2024-10-02", "labels": { "ja": "10月2日", "en": "October 2" } },
      { "value": "2024-10-03", "labels": { "ja": "10月3日", "en": "October 3" } }
    ],
    "items": [
      { "value": "A-1", "labels": { "ja": "午前（9:00-12:00）", "en": "Morning (9:00-12:00)" } },
      { "value": "A-2", "labels": { "ja": "午後（13:00-17:00）", "en": "Afternoon (13:00-17:00)" } },
      { "value": "B-1", "labels": { "ja": "午前（9:00-12:00）", "en": "Morning (9:00-12:00)" } },
      { "value": "B-2", "labels": { "ja": "午後（13:00-17:00）", "en": "Afternoon (13:00-17:00)" } },
      { "value": "C-1", "labels": { "ja": "午前（9:00-12:00）", "en": "Morning (9:00-12:00)" } },
      { "value": "C-2", "labels": { "ja": "午後（13:00-17:00）", "en": "Afternoon (13:00-17:00)" } }
    ],
    "mode": "checkbox",
    "header_check_enabled": true,
    "selection_limit": {
      "type": "global",
      "max": 3
    }
  }
}
```

または、シンプルな形式（`label`のみ）:

```json
{
  "label": "希望日時を選択してください",
  "matrix": {
    "headers": [
      { "value": "2024-10-01", "label": "10月1日" },
      { "value": "2024-10-02", "label": "10月2日" },
      "2024-10-03"
    ],
    "items": [
      { "value": "A-1", "label": "午前（9:00-12:00）" },
      { "value": "A-2", "label": "午後（13:00-17:00）" }
    ],
    "mode": "checkbox",
    "header_check_enabled": true,
    "selection_limit": {
      "type": "global",
      "max": 3
    }
  }
}
```

または、ラジオボタンモード:

```json
{
  "label": "希望日時を選択してください",
  "matrix": {
    "headers": [
      { "value": "2024-10-01", "labels": { "ja": "10月1日", "en": "October 1" } },
      { "value": "2024-10-02", "labels": { "ja": "10月2日", "en": "October 2" } },
      { "value": "2024-10-03", "labels": { "ja": "10月3日", "en": "October 3" } }
    ],
    "items": [
      { "value": "A-1", "labels": { "ja": "午前", "en": "Morning" } },
      { "value": "A-2", "labels": { "ja": "午後", "en": "Afternoon" } }
    ],
    "mode": "radio",
    "selection_limit": {
      "type": "per_header",
      "max": 1
    }
  }
}
```

**パラメータ説明**:
- `matrix.headers`: 項目ヘッダの配列（列ヘッダ、例: 日付、時間帯、カテゴリなど）
  - 文字列形式: `"2024-10-01"` など
  - オブジェクト形式: `{ "value": "2024-10-01", "label": "10月1日" }` または `{ "value": "2024-10-01", "labels": { "ja": "10月1日", "en": "October 1" } }`
- `matrix.items`: 項目の配列（各行の項目、各ヘッダに適用される）
  - オブジェクト形式: `{ "value": "A-1", "label": "午前" }` または `{ "value": "A-1", "labels": { "ja": "午前", "en": "Morning" } }`
- `matrix.mode`: 選択モード（`checkbox` | `radio`）
- `matrix.header_check_enabled`: ヘッダチェック機能を有効にするか（`mode: "checkbox"`の場合のみ、デフォルト: `true`）
- `matrix.selection_limit.type`: 選択制限のタイプ（`global` | `per_header`）
  - `global`: 全体で最大N個選択可能
  - `per_header`: 各ヘッダで最大N個選択可能
- `matrix.selection_limit.max`: 最大選択数（`type: "global"`の場合は全体、`type: "per_header"`の場合は各ヘッダ）

**注意**: 
- `mode: "radio"`の場合、`header_check_enabled`は無効（ヘッダチェック機能は不要）
- `mode: "radio"`の場合、`selection_limit.type: "per_header"`が推奨（各ヘッダで1個選択）
- `matrix.headers`は汎用的な配列で、日付以外（時間帯、カテゴリ、場所など）も使用可能
- ヘッダと項目の両方で、`label`（単一言語）または`labels`（多言語対応）を使用可能
- `labels`が指定されている場合、現在のロケールに応じて適切な言語が表示される

#### 2.3.3 データ構造

**回答値の形式**:

チェックボックスの場合:
```json
{
  "field_key": {
    "header1": ["item1", "item2"],
    "header2": ["item1"],
    "header3": []
  }
}
```

ラジオボタンの場合:
```json
{
  "field_key": {
    "header1": "item1",
    "header2": "item2",
    "header3": null
  }
}
```

**注意**: 
- ヘッダの値（キー）は`matrix.headers`で定義された`value`を使用します。文字列形式の場合はその文字列自体が値となります。
- 日付の場合は`"2024-10-01"`などの文字列、その他の場合は任意の文字列を使用できます。
- ヘッダと項目の両方で、`{value, label}`形式または`{value, labels: {ja, en}}`形式を使用可能です。
- `labels`が指定されている場合、現在のロケール（`locale`）に応じて適切な言語が表示されます。

#### 2.3.4 フロントエンド実装

**ファイル**: `src/pages/public/PublicFormViewPage.tsx`

```typescript
case "matrix":
  const matrixConfig = field.options_json?.matrix;
  if (!matrixConfig) {
    return <div className="text-sm text-white/40">マトリクス設定がありません</div>;
  }

  const headers = matrixConfig.headers || [];
  const items = matrixConfig.items || [];
  const mode = matrixConfig.mode || "checkbox";
  const headerCheckEnabled = matrixConfig.header_check_enabled ?? (mode === "checkbox");
  const selectionLimit = matrixConfig.selection_limit;

  // 回答値の初期化
  const matrixValue = value || {};
  const getCellValue = (header: string, itemValue: string) => {
    if (mode === "checkbox") {
      return Array.isArray(matrixValue[header]) ? matrixValue[header].includes(itemValue) : false;
    } else {
      return matrixValue[header] === itemValue;
    }
  };

  // セル変更ハンドラー
  const handleCellChange = (header: string, itemValue: string, checked: boolean) => {
    const newValue = { ...matrixValue };

    if (mode === "checkbox") {
      if (!newValue[header]) newValue[header] = [];
      const currentArray = Array.isArray(newValue[header]) ? newValue[header] : [];
      
      if (checked) {
        // 選択制限チェック
        if (selectionLimit?.type === "global") {
          const totalSelected = Object.values(newValue).reduce(
            (sum, arr) => sum + (Array.isArray(arr) ? arr.length : 0),
            0
          );
          if (totalSelected >= (selectionLimit.max || Infinity)) {
            showError(`最大${selectionLimit.max}個まで選択できます`);
            return;
          }
        } else if (selectionLimit?.type === "per_header") {
          if (currentArray.length >= (selectionLimit.max || Infinity)) {
            showError(`各ヘッダで最大${selectionLimit.max}個まで選択できます`);
            return;
          }
        }
        
        newValue[header] = [...currentArray, itemValue];
      } else {
        newValue[header] = currentArray.filter((v) => v !== itemValue);
      }
    } else {
      // ラジオボタン
      if (checked) {
        newValue[header] = itemValue;
      } else {
        newValue[header] = null;
      }
    }

    onChange(newValue);
  };

  // ヘッダチェックハンドラー（チェックボックスのみ）
  const handleHeaderCheck = (header: string, checked: boolean) => {
    if (mode !== "checkbox" || !headerCheckEnabled) return;

    const newValue = { ...matrixValue };
    if (checked) {
      newValue[header] = items.map((item) => item.value);
    } else {
      newValue[header] = [];
    }
    onChange(newValue);
  };

  // ヘッダのチェック状態（そのヘッダの全項目が選択されているか）
  const isHeaderChecked = (header: string) => {
    if (mode !== "checkbox") return false;
    const headerValue = matrixValue[header];
    if (!Array.isArray(headerValue) || headerValue.length === 0) return false;
    return items.every((item) => headerValue.includes(item.value));
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full text-sm border-collapse">
        <thead>
          <tr>
            <th className="px-3 py-2 text-left border border-white/10 bg-black/30">
              {/* 空のヘッダセル（項目ラベル用） */}
            </th>
            {headers.map((header) => {
              // ヘッダの表示ラベルを取得（オブジェクトの場合はlabels/label、文字列の場合はそのまま）
              let headerLabel: string;
              let headerValue: string;
              
              if (typeof header === "object") {
                headerValue = header.value || header.label || String(header);
                // 多言語対応: labels > label > value の順で取得
                if (header.labels) {
                  headerLabel = header.labels[locale] || header.labels["ja"] || header.labels["en"] || headerValue;
                } else {
                  headerLabel = header.label || headerValue;
                }
              } else {
                headerValue = header;
                headerLabel = header;
              }
              
              return (
                <th
                  key={headerValue}
                  className="px-3 py-2 text-center border border-white/10 bg-black/30"
                >
                  <div className="flex flex-col items-center gap-1">
                    <div>{headerLabel}</div>
                    {headerCheckEnabled && mode === "checkbox" && (
                      <label className="cursor-pointer">
                        <input
                          type="checkbox"
                          checked={isHeaderChecked(headerValue)}
                          onChange={(e) => handleHeaderCheck(headerValue, e.target.checked)}
                          className="rounded border-white/20 bg-black/30 text-brand-gold focus:ring-brand-gold/30"
                        />
                      </label>
                    )}
                  </div>
                </th>
              );
            })}
          </tr>
        </thead>
        <tbody>
              {items.map((item, itemIndex) => {
                // 項目の表示ラベルを取得（多言語対応: labels > label > value の順で取得）
                const itemLabel = item.labels?.[locale] || item.labels?.["ja"] || item.labels?.["en"] || item.label || item.value;
                
                return (
                  <tr key={item.value}>
                    <td className="px-3 py-2 border border-white/10 bg-black/20">
                      {itemLabel}
                    </td>
              {headers.map((header) => {
                const headerValue = typeof header === "object" ? (header.value || header.label || header) : header;
                const cellValue = getCellValue(headerValue, item.value);
                return (
                  <td
                    key={`${headerValue}-${item.value}`}
                    className="px-3 py-2 text-center border border-white/10 bg-black/20"
                  >
                    {mode === "checkbox" ? (
                      <label className="cursor-pointer">
                        <input
                          type="checkbox"
                          checked={cellValue}
                          onChange={(e) => handleCellChange(headerValue, item.value, e.target.checked)}
                          disabled={disabled}
                          className="rounded border-white/20 bg-black/30 text-brand-gold focus:ring-brand-gold/30 disabled:opacity-50"
                        />
                      </label>
                    ) : (
                      <label className="cursor-pointer">
                        <input
                          type="radio"
                          name={`${field.field_key}-${headerValue}`}
                          value={item.value}
                          checked={cellValue}
                          onChange={(e) => handleCellChange(headerValue, item.value, e.target.checked)}
                          disabled={disabled}
                          className="rounded border-white/20 bg-black/30 text-brand-gold focus:ring-brand-gold/30 disabled:opacity-50"
                        />
                      </label>
                    )}
                  </td>
                );
              })}
                  </tr>
                );
              })}
        </tbody>
      </table>

      {/* 選択制限の表示 */}
      {selectionLimit && (
        <div className="mt-2 text-xs text-white/60">
          {selectionLimit.type === "global" && (
            <span>全体で最大{selectionLimit.max}個まで選択できます</span>
          )}
          {selectionLimit.type === "per_header" && (
            <span>各ヘッダで最大{selectionLimit.max}個まで選択できます</span>
          )}
        </div>
      )}
    </div>
  );
```

#### 2.3.5 バリデーション実装

**ファイル**: `src/pages/public/PublicFormViewPage.tsx` の `validate()` 関数

```typescript
// matrixフィールドのバリデーション
if (field.type === "matrix" && fieldState.required) {
  const matrixValue = value || {};
  const matrixConfig = field.options_json?.matrix;
  const selectionLimit = matrixConfig?.selection_limit;

  // 必須チェック: 少なくとも1つのヘッダで選択されているか
  const hasSelection = Object.values(matrixValue).some((v) => {
    if (Array.isArray(v)) return v.length > 0;
    return v !== null && v !== undefined;
  });

  if (!hasSelection) {
    const label = field.options_json?.label || field.field_key;
    newErrors[field.field_key] = `${label}は必須です`;
    return;
  }

  // 選択制限チェック
  if (selectionLimit) {
    if (selectionLimit.type === "global") {
      const totalSelected = Object.values(matrixValue).reduce(
        (sum, v) => sum + (Array.isArray(v) ? v.length : (v ? 1 : 0)),
        0
      );
      if (totalSelected > (selectionLimit.max || Infinity)) {
        const label = field.options_json?.label || field.field_key;
        newErrors[field.field_key] = `${label}は最大${selectionLimit.max}個まで選択できます`;
        return;
      }
    } else if (selectionLimit.type === "per_header") {
      for (const [header, v] of Object.entries(matrixValue)) {
        const count = Array.isArray(v) ? v.length : (v ? 1 : 0);
        if (count > (selectionLimit.max || Infinity)) {
          const label = field.options_json?.label || field.field_key;
          newErrors[field.field_key] = `${label}の${header}は最大${selectionLimit.max}個まで選択できます`;
          return;
        }
      }
    }
  }
}
```

#### 2.3.6 バックエンド実装

**ファイル**: `app/Services/AnswerNormalizerService.php`

```php
case 'matrix':
    // マトリクス形式の回答値を正規化
    if (!is_array($value)) {
        return [];
    }
    
    $normalized = [];
    foreach ($value as $header => $itemValue) {
        if ($field->options_json['matrix']['mode'] === 'checkbox') {
            // チェックボックスの場合: 配列
            $normalized[$header] = is_array($itemValue) ? $itemValue : [];
        } else {
            // ラジオボタンの場合: 単一値
            $normalized[$header] = $itemValue ?: null;
        }
    }
    
    return $normalized;
```

**ファイル**: `app/Http/Controllers/Api/V1/PublicFormsController.php`

```php
// matrixフィールドのバリデーション
if ($field->type === 'matrix' && $fieldState['required']) {
    $matrixValue = $answers[$fieldKey] ?? [];
    
    // 必須チェック
    $hasSelection = false;
    foreach ($matrixValue as $header => $itemValue) {
        if (is_array($itemValue) && count($itemValue) > 0) {
            $hasSelection = true;
            break;
        } elseif (!is_array($itemValue) && $itemValue !== null) {
            $hasSelection = true;
            break;
        }
    }
    
    if (!$hasSelection) {
        $fieldLabel = $field->options_json['label'] ?? $fieldKey;
        $validationErrors[$fieldKey] = "{$fieldLabel}は必須です";
        continue;
    }
    
    // 選択制限チェック
    $selectionLimit = $field->options_json['matrix']['selection_limit'] ?? null;
    if ($selectionLimit) {
        if ($selectionLimit['type'] === 'global') {
            $totalSelected = 0;
            foreach ($matrixValue as $itemValue) {
                $totalSelected += is_array($itemValue) ? count($itemValue) : ($itemValue ? 1 : 0);
            }
            if ($totalSelected > ($selectionLimit['max'] ?? PHP_INT_MAX)) {
                $fieldLabel = $field->options_json['label'] ?? $fieldKey;
                $validationErrors[$fieldKey] = "{$fieldLabel}は最大{$selectionLimit['max']}個まで選択できます";
            }
        } elseif ($selectionLimit['type'] === 'per_header') {
            foreach ($matrixValue as $header => $itemValue) {
                $count = is_array($itemValue) ? count($itemValue) : ($itemValue ? 1 : 0);
                if ($count > ($selectionLimit['max'] ?? PHP_INT_MAX)) {
                    $fieldLabel = $field->options_json['label'] ?? $fieldKey;
                    $validationErrors[$fieldKey] = "{$fieldLabel}の{$header}は最大{$selectionLimit['max']}個まで選択できます";
                    break;
                }
            }
        }
    }
}
```

#### 2.3.7 実装の優先順位

**優先度: 高**

理由:
- 実用的な機能（予約システムなどでよく使用される）
- 既存機能では代替不可能
- 実装コストは中程度（新規フィールドタイプの追加）

---

## 3. 実装計画

### 3.1 フェーズ1: 規約/同意文章のスクロール検知機能

1. **フロントエンド実装**
   - `terms`フィールドタイプの拡張
   - スクロール検知機能の実装
   - バリデーションロジックの追加

2. **テスト**
   - スクロール検知の動作確認
   - バリデーションの動作確認

### 3.2 フェーズ2: 表形式フィールド（マトリクス）

1. **データベース・モデル**
   - フィールドタイプ `matrix` の追加（既存のenumに追加、または新規対応）

2. **フロントエンド実装**
   - `matrix`フィールドタイプのレンダリング
   - ヘッダチェック機能
   - 選択制限機能
   - バリデーションロジック

3. **バックエンド実装**
   - `AnswerNormalizerService` の拡張
   - `PublicFormsController` のバリデーション拡張

4. **テスト**
   - マトリクス表示の動作確認
   - ヘッダチェックの動作確認
   - 選択制限の動作確認
   - バリデーションの動作確認

---

## 4. 参考資料

- `VALIDATION_RULES_STATUS.md`: 既存のバリデーション実装状況
- `src/pages/public/PublicFormViewPage.tsx`: 公開フォーム表示ページ
- `app/Services/AnswerNormalizerService.php`: 回答値の正規化サービス
- `app/Http/Controllers/Api/V1/PublicFormsController.php`: 公開フォームAPIコントローラー
