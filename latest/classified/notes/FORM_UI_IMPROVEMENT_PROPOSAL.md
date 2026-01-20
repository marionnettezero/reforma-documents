# フォーム作成/編集UI改善提案

## 作成日時
2026-01-13

## 実装状況（最終更新: 2026-01-20）

### ✅ 実装済み項目

1. **統合編集画面（FormEditIntegratedPage）**
   - 3カラムレイアウト（左サイドバー、メインエリア、右サイドパネル）
   - フォーム基本情報、通知設定、テーマ設定、項目構造の統合編集

2. **コンポーネント**
   - `FormStructureEditor`: STEP/GROUP/項目の構造編集
   - `FormBasicInfoSection`: 基本情報セクション
   - `FormNotificationSection`: 通知設定セクション
   - `FormThemeSection`: テーマ設定セクション

3. **機能**
   - ドラッグ&ドロップによる順序変更
   - CSVインポート/エクスポート
   - 一時保存機能（IndexedDB/ローカルストレージ/メモリの3段階フォールバック）
   - 自動保存（3秒のdebounce）
   - データ復元（ページ読み込み時）
   - タブ間競合検知と警告ダイアログ
   - 未保存変更検知と画面遷移時の確認ダイアログ
   - 統合保存処理（基本情報とフィールドデータの一括保存）

4. **ルーティング**
   - 統合画面へのルーティング追加（`${ROUTES.FORM_EDIT}/integrated`）
   - 既存画面との互換性維持

### ⚠️ 未実装項目

1. **ウィザード形式**（新規作成時）
   - 段階的なウィザード形式でのフォーム作成

2. **リアルタイムプレビュー**
   - 設定変更時の即座のプレビュー反映

3. **テンプレート機能**
   - よく使うフォーム構造のテンプレート化

4. **その他**
   - データの圧縮（IndexedDB使用により容量問題は解決済みのため優先度低）
   - 自動クリーンアップ（有効期限切れデータの自動削除）

---

## 現状の問題点

### 1. UIの複雑さ
- **画面の分離**: フォーム編集画面（F-02）とフォーム項目設定画面（F-03）が分離されている
- **階層構造の複雑さ**: STEP式/単一式の選択、STEP/GROUP/項目の3階層構造
- **設定項目の多さ**: 各項目で設定できる項目が多数（タイプ、必須、選択肢、条件分岐、計算ルールなど）
- **操作の分散**: 関連する設定が複数の画面やセクションに分散

### 2. ユーザビリティの問題
- **ワークフローの不明確さ**: フォーム作成の手順が直感的でない
- **設定の見落とし**: 重要な設定項目が見つけにくい
- **コンテキストの欠如**: 設定変更時の影響範囲が分かりにくい

---

## 改善案

### 案1: ウィザード形式の導入（推奨）

#### 概要
フォーム作成を段階的なウィザード形式に変更し、各ステップで必要な設定のみを表示する。

#### 構造
```
ステップ1: 基本情報
  - フォーム名、説明、公開期間など
  - フォームタイプの選択（STEP式/単一式）

ステップ2: 構造設計
  - STEP式の場合: STEPの追加・編集
  - GROUPの追加・編集
  - ドラッグ&ドロップで順序変更

ステップ3: 項目追加
  - 項目タイプの選択
  - 基本設定（ラベル、必須など）
  - 簡易プレビュー

ステップ4: 詳細設定
  - 選択肢の設定
  - 条件分岐ルール
  - 計算ルール
  - 高度な設定

ステップ5: 確認・公開
  - プレビュー
  - 最終確認
  - 公開設定
```

#### メリット
- ✅ 段階的な操作で迷いが少ない
- ✅ 各ステップで集中できる
- ✅ 進捗状況が明確
- ✅ 初心者にも分かりやすい

#### デメリット
- ❌ 既存のフォーム編集時は少し手間
- ❌ 画面遷移が増える

---

### 案2: タブベースの統合UI

#### 概要
1つの画面にタブを設け、関連する設定をグループ化する。

#### 構造
```
[フォーム編集画面]
├─ タブ1: 基本情報
│   ├─ フォーム名・説明
│   ├─ 公開期間
│   └─ テーマ設定
│
├─ タブ2: 構造・項目
│   ├─ フォームタイプ切替（STEP式/単一式）
│   ├─ STEP/GROUP管理（折りたたみ可能）
│   ├─ 項目一覧（カード形式）
│   └─ 項目追加ボタン
│
├─ タブ3: 通知設定
│   └─ ユーザー/管理者通知設定
│
└─ タブ4: プレビュー
    └─ リアルタイムプレビュー
```

#### 項目編集のモーダル/サイドパネル
- 項目をクリック → サイドパネルまたはモーダルで詳細編集
- 基本設定、選択肢、条件分岐、計算ルールをタブで整理

#### メリット
- ✅ 1画面で完結
- ✅ 関連設定がグループ化されている
- ✅ 既存の操作感を維持しやすい

#### デメリット
- ❌ 画面が複雑になる可能性
- ❌ スクロールが多くなる

---

### 案3: カードベースの視覚的UI（推奨）

#### 概要
STEP/GROUP/項目をカード形式で視覚的に表示し、ドラッグ&ドロップで直感的に操作できるUI。

#### 構造
```
[フォーム編集画面 - 統合版]

左サイドバー（固定）:
  - 基本情報（折りたたみ可能）
  - 通知設定（折りたたみ可能）
  - テーマ設定（折りたたみ可能）

メインエリア:
  [フォームタイプ切替] [STEP式] [単一式]
  
  ┌─────────────────────────────────────┐
  │ STEP 1: 基本情報                    │
  │ ┌─────────────────────────────────┐ │
  │ │ GROUP 1: 個人情報                │ │
  │ │ ┌─────┐ ┌─────┐ ┌─────┐        │ │
  │ │ │項目1│ │項目2│ │項目3│ [+追加]│ │
  │ │ └─────┘ └─────┘ └─────┘        │ │
  │ └─────────────────────────────────┘ │
  │ [+GROUP追加]                         │
  └─────────────────────────────────────┘
  [+STEP追加]
  
  [プレビュー] [保存] [公開]
```

#### 項目カードの詳細
```
┌─────────────────────────────┐
│ 項目名: メールアドレス      │ [編集] [削除]
│ タイプ: email               │
│ 必須: ✓                     │
│ 条件分岐: あり              │
│ ─────────────────────────── │
│ [詳細設定を開く ▼]          │
└─────────────────────────────┘
```

#### 詳細設定パネル（右側またはモーダル）
```
[項目詳細設定]
├─ 基本設定
│   ├─ フィールドキー
│   ├─ タイプ
│   ├─ ラベル（多言語）
│   └─ 必須設定
│
├─ 選択肢（select/radio/checkbox用）
│   └─ 選択肢の追加・編集
│
├─ 条件分岐
│   ├─ 表示条件
│   ├─ 必須条件
│   └─ ステップ遷移条件
│
├─ 計算ルール（computed用）
│   └─ 計算式エディタ
│
└─ 高度な設定
    ├─ PDF設定
    └─ その他
```

#### メリット
- ✅ 視覚的に分かりやすい
- ✅ ドラッグ&ドロップで直感的
- ✅ 階層構造が一目で分かる
- ✅ 項目の詳細設定を必要時のみ表示

#### デメリット
- ❌ 実装コストが高い
- ❌ 項目数が多い場合のパフォーマンス

---

### 案4: 段階的表示（Progressive Disclosure）

#### 概要
初期表示は簡潔にし、必要に応じて詳細設定を展開する方式。

#### 構造
```
[フォーム編集画面]

基本情報セクション（常時表示）
  - フォーム名、説明、公開期間

構造セクション（折りたたみ可能）
  [▼ フォーム構造を編集]
    - フォームタイプ選択
    - STEP/GROUP管理
    - 項目一覧（簡易表示）

項目セクション
  [項目1: メールアドレス] [編集] [削除]
    └─ 基本情報のみ表示（タイプ、必須、条件分岐の有無）
  
  [+ 項目を追加]

[詳細設定] ボタンクリック
  → サイドパネルまたはモーダルで詳細設定
```

#### 詳細設定パネル
- 基本設定、選択肢、条件分岐、計算ルールをタブで整理
- 設定変更時にリアルタイムプレビューを表示

#### メリット
- ✅ 画面がすっきり
- ✅ 必要な時だけ詳細を表示
- ✅ 既存UIとの互換性が高い

#### デメリット
- ❌ 設定項目を見つけにくい可能性

---

## 推奨案: 案1（ウィザード形式）+ 案3（カードベース）のハイブリッド

### 概要
- **新規作成時**: ウィザード形式で段階的に作成
- **編集時**: カードベースの統合UIで編集

### 実装方針

#### 1. 新規作成フロー
```
[フォーム一覧] → [+ 新規作成] → [ウィザード開始]

ステップ1: 基本情報
  - フォーム名、説明
  - フォームタイプ（STEP式/単一式）

ステップ2: 構造設計（カードベース）
  - STEP/GROUPの追加・編集
  - ドラッグ&ドロップで順序変更

ステップ3: 項目追加
  - 項目タイプ選択
  - 基本設定（ラベル、必須）
  - 簡易プレビュー

ステップ4: 詳細設定（必要に応じて）
  - 選択肢、条件分岐、計算ルール

ステップ5: 確認・公開
  - プレビュー
  - 公開設定
```

#### 2. 編集フロー
```
[フォーム一覧] → [フォーム選択] → [統合編集画面]

左サイドバー:
  - 基本情報（折りたたみ可能）
  - 通知設定（折りたたみ可能）
  - テーマ設定（折りたたみ可能）

メインエリア:
  - フォームタイプ切替
  - STEP/GROUP/項目のカード表示
  - ドラッグ&ドロップ対応
  - 項目クリック → サイドパネルで詳細編集

右サイドパネル（オプション）:
  - リアルタイムプレビュー
```

### 実装の優先順位

#### フェーズ1: 基本改善（即座に実装可能）
1. **項目一覧の視覚化** ✅ 実装済み
   - カード形式での表示
   - 項目の基本情報を一目で確認可能に

2. **詳細設定の分離** ✅ 実装済み
   - 項目クリック → モーダル/サイドパネルで詳細設定
   - 基本設定と高度な設定を分離

3. **設定セクションの折りたたみ** ✅ 実装済み
   - 基本情報、通知設定などを折りたたみ可能に
   - 必要な時だけ展開

#### フェーズ2: 構造改善（中期）
4. **ウィザード形式の導入** ⚠️ 未実装
   - 新規作成時のウィザード
   - 既存フォーム編集時は統合UI

5. **ドラッグ&ドロップの強化** ✅ 実装済み
   - STEP/GROUP/項目の順序変更
   - 視覚的フィードバック

#### フェーズ3: 高度な機能（長期）
6. **リアルタイムプレビュー** ⚠️ 未実装
   - 設定変更時の即座の反映
   - 条件分岐の動作確認

7. **テンプレート機能** ⚠️ 未実装
   - よく使うフォーム構造のテンプレート化
   - コピー&ペースト機能

---

## 具体的なUI改善例

### 改善前（現在）
```
[フォーム編集画面]
- 基本情報
- 翻訳設定
- 通知設定
- テーマ設定
[保存]

[フォーム項目設定画面]
- STEP式/単一式切替
- STEP管理
- GROUP管理
- 項目一覧（テーブル形式）
- 項目編集（長いフォーム）
  - フィールドキー
  - タイプ
  - ラベル
  - 必須
  - 選択肢
  - 条件分岐（複雑）
  - 計算ルール
  - PDF設定
[保存]
```

### 改善後（案1+3のハイブリッド）

#### 新規作成時
```
[ウィザード: ステップ1/5]
基本情報
  [フォーム名] [説明]
  [フォームタイプ] ○ STEP式  ○ 単一式
[次へ]
```

```
[ウィザード: ステップ2/5]
構造設計
  ┌─────────────────────┐
  │ STEP 1: 基本情報    │
  │ ┌─────────────────┐ │
  │ │ GROUP 1         │ │
  │ │ [+項目追加]     │ │
  │ └─────────────────┘ │
  │ [+GROUP追加]         │
  └─────────────────────┘
  [+STEP追加]
[戻る] [次へ]
```

```
[ウィザード: ステップ3/5]
項目追加
  [項目タイプを選択] [text] [email] [number] ...
  
  ┌─────────────────────┐
  │ 項目名: [入力]      │
  │ 必須: [チェック]    │
  │ [追加]              │
  └─────────────────────┘
[戻る] [次へ]
```

#### 編集時
```
[フォーム編集画面 - 統合版]

[基本情報 ▼] [通知設定] [テーマ設定]

[フォームタイプ] [STEP式] [単一式]

┌─────────────────────────────────┐
│ STEP 1: 基本情報        [編集] │
│ ┌─────────────────────────────┐ │
│ │ GROUP 1: 個人情報    [編集] │ │
│ │ ┌──────┐ ┌──────┐          │ │
│ │ │項目1 │ │項目2 │ [+追加]  │ │
│ │ └──────┘ └──────┘          │ │
│ └─────────────────────────────┘ │
│ [+GROUP追加]                     │
└─────────────────────────────────┘

[項目1をクリック]
  → 右サイドパネルで詳細設定
    [基本設定] [選択肢] [条件分岐] [計算ルール]
```

---

## 技術的な実装ポイント

### 1. コンポーネント設計
- **FormWizard**: ウィザード形式のコンテナ
- **FormStructureEditor**: STEP/GROUP/項目の構造編集
- **FieldCard**: 項目カードコンポーネント
- **FieldDetailPanel**: 項目詳細設定パネル
- **FormPreview**: リアルタイムプレビュー

### 2. 状態管理
- フォーム全体の状態を一元管理
- 各ステップの状態を保持
- 未保存の変更を検知

### 3. パフォーマンス
- 大量の項目がある場合の仮想スクロール
- 詳細設定パネルの遅延読み込み
- ドラッグ&ドロップの最適化

---

---

## 現在のUIの具体的な問題点

### 1. FormItemPage.tsx の複雑さ
- **ファイルサイズ**: 約2900行の巨大なコンポーネント
- **状態管理**: 多数のuseState（20個以上）
- **表示ロジック**: STEP/GROUP/項目の3階層がネストされたJSX
- **編集モード**: インライン編集と詳細編集が混在

### 2. 操作の複雑さ
- **フォームタイプ切替**: 常時表示されているが、変更時の影響が分かりにくい
- **STEP/GROUP名の編集**: 多言語タブが各STEP/GROUPごとに存在
- **項目編集**: インライン編集で全設定項目が一度に表示される
- **条件分岐ルール**: 複雑なビルダーUIが項目編集フォーム内に埋め込まれている

### 3. 情報の過多
- **項目一覧表示**: JSON形式で条件分岐ルールが表示される（可読性が低い）
- **設定項目の多さ**: 1つの項目で10以上の設定項目がある
- **多言語対応**: 各要素ごとにタブが存在し、画面が煩雑

---

## 段階的な改善計画

### フェーズ1: 即効性のある改善（1-2週間）

#### 1.1 項目表示の改善
**現状**: テキスト形式で項目情報を表示
```typescript
// 現在
<div>項目名: {field.field_key}</div>
<div>選択肢: {JSON.stringify(field.options_json)}</div>
<div>表示条件: {JSON.stringify(field.visibility_rule)}</div>
```

**改善後**: カード形式で視覚的に表示
```typescript
// 改善後
<FieldCard
  field={field}
  onEdit={() => openDetailPanel(field)}
  onDelete={() => deleteField(field)}
/>
```

**実装内容**:
- `FieldCard` コンポーネントの作成
- 項目の基本情報（タイプ、必須、条件分岐の有無）をアイコン/バッジで表示
- 詳細情報は「詳細を見る」ボタンで展開

#### 1.2 詳細設定の分離
**現状**: インライン編集で全設定項目を表示

**改善後**: モーダル/サイドパネルで詳細設定
```typescript
// 項目クリック → サイドパネル表示
<FieldDetailPanel
  field={selectedField}
  onSave={handleSaveField}
  onClose={handleClosePanel}
/>
```

**実装内容**:
- `FieldDetailPanel` コンポーネントの作成
- 設定項目をタブで分類（基本設定、選択肢、条件分岐、計算ルール、高度な設定）
- インライン編集を廃止し、すべてサイドパネルで編集

#### 1.3 設定セクションの折りたたみ
**現状**: すべての設定が常時表示

**改善後**: アコーディオン形式で折りたたみ可能
```typescript
<Accordion>
  <AccordionItem title="基本情報" defaultOpen>
    {/* 基本情報の設定 */}
  </AccordionItem>
  <AccordionItem title="通知設定">
    {/* 通知設定 */}
  </AccordionItem>
  <AccordionItem title="テーマ設定">
    {/* テーマ設定 */}
  </AccordionItem>
</Accordion>
```

---

### フェーズ2: 構造の改善（1-2ヶ月）

#### 2.1 画面統合 ✅ 実装済み
**現状**: FormEditPage と FormItemPage が分離

**改善後**: 1つの統合画面に
```typescript
<FormEditPageIntegrated>
  <LeftSidebar>
    <FormBasicInfo />
    <NotificationSettings />
    <ThemeSettings />
  </LeftSidebar>
  
  <MainArea>
    <FormTypeSelector />
    <FormStructureEditor />
  </MainArea>
  
  <RightSidebar>
    {selectedField && <FieldDetailPanel field={selectedField} />}
  </RightSidebar>
</FormEditPageIntegrated>
```

#### 2.2 ウィザード形式の導入 ⚠️ 未実装
**新規作成時のみ**: ウィザード形式で段階的に作成
```typescript
<FormWizard>
  <WizardStep title="基本情報" step={1} total={5}>
    <FormBasicInfoForm />
  </WizardStep>
  <WizardStep title="構造設計" step={2} total={5}>
    <FormStructureEditor />
  </WizardStep>
  {/* ... */}
</FormWizard>
```

---

### フェーズ3: 高度な機能（3-6ヶ月）

#### 3.1 リアルタイムプレビュー
- 設定変更時に即座にプレビューを更新
- 条件分岐の動作を視覚的に確認

#### 3.2 テンプレート機能
- よく使うフォーム構造のテンプレート化
- テンプレートから新規フォームを作成

---

## 具体的な実装例

### 例1: FieldCard コンポーネント
```typescript
interface FieldCardProps {
  field: FormField;
  onEdit: () => void;
  onDelete: () => void;
  onDragStart?: (e: DragEvent) => void;
}

function FieldCard({ field, onEdit, onDelete, onDragStart }: FieldCardProps) {
  return (
    <div 
      className="rounded-xl border border-white/10 bg-black/20 p-3 cursor-pointer hover:bg-black/30"
      draggable
      onDragStart={onDragStart}
      onClick={onEdit}
    >
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <span className="text-xs">☰</span>
          <span className="font-bold">{field.field_key}</span>
          <Badge variant={field.is_required ? "warning" : "neutral"}>
            {field.is_required ? "必須" : "任意"}
          </Badge>
          <Badge variant="info">{field.type}</Badge>
          {field.visibility_rule && <Badge variant="secondary">条件分岐</Badge>}
        </div>
        <div className="flex gap-2" onClick={(e) => e.stopPropagation()}>
          <button onClick={onEdit}>編集</button>
          <button onClick={onDelete}>削除</button>
        </div>
      </div>
      <div className="text-xs text-white/60">
        {field.options_json?.label || field.field_key}
      </div>
    </div>
  );
}
```

### 例2: FieldDetailPanel コンポーネント
```typescript
interface FieldDetailPanelProps {
  field: FormField | null;
  onSave: (field: FormField) => void;
  onClose: () => void;
}

function FieldDetailPanel({ field, onSave, onClose }: FieldDetailPanelProps) {
  const [activeTab, setActiveTab] = useState<'basic' | 'options' | 'conditions' | 'computed' | 'advanced'>('basic');
  
  if (!field) return null;
  
  return (
    <div className="fixed right-0 top-0 h-full w-96 bg-black/90 border-l border-white/10 shadow-xl z-50 overflow-y-auto">
      <div className="p-4 border-b border-white/10">
        <div className="flex items-center justify-between">
          <h3 className="font-bold">項目詳細設定</h3>
          <button onClick={onClose}>×</button>
        </div>
      </div>
      
      <div className="flex border-b border-white/10">
        {(['basic', 'options', 'conditions', 'computed', 'advanced'] as const).map(tab => (
          <button
            key={tab}
            className={`px-4 py-2 text-sm ${activeTab === tab ? 'border-b-2 border-brand-gold' : ''}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab === 'basic' && '基本設定'}
            {tab === 'options' && '選択肢'}
            {tab === 'conditions' && '条件分岐'}
            {tab === 'computed' && '計算ルール'}
            {tab === 'advanced' && '高度な設定'}
          </button>
        ))}
      </div>
      
      <div className="p-4">
        {activeTab === 'basic' && <FieldBasicSettings field={field} />}
        {activeTab === 'options' && <FieldOptionsSettings field={field} />}
        {activeTab === 'conditions' && <FieldConditionsSettings field={field} />}
        {activeTab === 'computed' && <FieldComputedSettings field={field} />}
        {activeTab === 'advanced' && <FieldAdvancedSettings field={field} />}
      </div>
      
      <div className="p-4 border-t border-white/10">
        <button onClick={() => onSave(field)}>保存</button>
        <button onClick={onClose}>キャンセル</button>
      </div>
    </div>
  );
}
```

### 例3: 統合編集画面の構造
```typescript
function FormEditPageIntegrated() {
  const [selectedField, setSelectedField] = useState<FormField | null>(null);
  const [leftSidebarOpen, setLeftSidebarOpen] = useState(true);
  
  return (
    <div className="flex h-screen">
      {/* 左サイドバー */}
      <div className={`${leftSidebarOpen ? 'w-80' : 'w-0'} transition-all border-r border-white/10`}>
        <Accordion>
          <AccordionItem title="基本情報" defaultOpen>
            <FormBasicInfo />
          </AccordionItem>
          <AccordionItem title="通知設定">
            <NotificationSettings />
          </AccordionItem>
          <AccordionItem title="テーマ設定">
            <ThemeSettings />
          </AccordionItem>
        </Accordion>
      </div>
      
      {/* メインエリア */}
      <div className="flex-1 overflow-y-auto p-6">
        <FormTypeSelector />
        <FormStructureEditor onFieldClick={setSelectedField} />
      </div>
      
      {/* 右サイドパネル（項目詳細） */}
      {selectedField && (
        <FieldDetailPanel
          field={selectedField}
          onSave={handleSaveField}
          onClose={() => setSelectedField(null)}
        />
      )}
    </div>
  );
}
```

---

## ユーザビリティテストの提案

### テスト項目
1. **フォーム作成時間**: 新規フォーム作成にかかる時間
2. **操作の迷い**: ユーザーが迷うポイントの特定
3. **設定項目の発見性**: 重要な設定項目を見つけられるか
4. **エラーの発生率**: 操作ミスによるエラーの発生頻度

### 改善効果の測定
- **Before**: 現在のUIでの操作時間・エラー率
- **After**: 改善後のUIでの操作時間・エラー率
- **改善率**: 操作時間の短縮率、エラー率の低下率

---

---

## フェーズ2: 統合編集画面の詳細設計

### 作成日時
2026-01-20

---

### 1. 概要

フェーズ2では、`FormEditPage`と`FormItemPage`を統合し、1つの画面でフォームの基本情報、通知設定、テーマ設定、および項目構造の編集が可能な統合編集画面を実装します。

### 2. 画面レイアウト

```
┌─────────────────────────────────────────────────────────────────┐
│ [ScreenHeader]                                                  │
│ フォーム編集 - 統合版                                           │
└─────────────────────────────────────────────────────────────────┘
┌──────────┬──────────────────────────────────────┬──────────────┐
│          │                                      │              │
│ 左サイド  │          メインエリア                │ 右サイド     │
│ バー      │                                      │ パネル       │
│          │                                      │              │
│ [基本情報]│  [フォームタイプ切替]                │ [項目詳細    │
│  ▼       │  [STEP式] [単一式]                   │  設定]       │
│  - コード │                                      │              │
│  - ステータス│                                   │  (FieldDetail│
│  - 公開期間│                                     │   Panel)     │
│          │  ┌─────────────────────────────┐    │              │
│ [通知設定]│  │ STEP 1: 基本情報    [編集] │    │              │
│          │  │ ┌─────────────────────────┐│    │              │
│ [テーマ設定]│ │ │ GROUP 1: 個人情報[編集]││    │              │
│          │  │ │ ┌─────┐ ┌─────┐        ││    │              │
│          │  │ │ │項目1│ │項目2│ [+追加]││    │              │
│          │  │ │ └─────┘ └─────┘        ││    │              │
│          │  │ └─────────────────────────┘│    │              │
│          │  │ [+GROUP追加]                │    │              │
│          │  └─────────────────────────────┘    │              │
│          │  [+STEP追加]                         │              │
│          │                                      │              │
│          │  [保存] [キャンセル]                 │              │
│          │                                      │              │
└──────────┴──────────────────────────────────────┴──────────────┘
```

### 3. コンポーネント設計

#### 3.1 メインコンポーネント: `FormEditIntegratedPage`

**役割**: 統合編集画面のコンテナコンポーネント

**Props**:
```typescript
interface FormEditIntegratedPageProps {
  formId: string; // URLパラメータから取得
}
```

**主な機能**:
- 3カラムレイアウトの管理
- フォーム全体の状態管理
- 左サイドバー、メインエリア、右サイドパネルの統合

**実装ファイル**: `src/pages/forms/FormEditIntegratedPage.tsx`

**実装状況**: ✅ 実装済み（2026-01-20）

#### 3.2 左サイドバーコンポーネント: `FormEditSidebar`

**役割**: 基本情報、通知設定、テーマ設定を表示

**構成**:
- `FormBasicInfoSection`: 基本情報セクション（`FormEditPage`から抽出）
- `FormNotificationSection`: 通知設定セクション（`FormEditPage`から抽出）
- `FormThemeSection`: テーマ設定セクション（`FormEditPage`から抽出）

**実装方針**:
- `Accordion`コンポーネントを使用して折りたたみ可能に
- `FormEditPage.tsx`の該当部分をコンポーネント化して再利用

**実装状況**: ✅ 実装済み（2026-01-20）
- `FormBasicInfoSection.tsx`: 基本情報セクション
- `FormNotificationSection.tsx`: 通知設定セクション
- `FormThemeSection.tsx`: テーマ設定セクション

#### 3.3 メインエリアコンポーネント: `FormStructureEditor`

**役割**: STEP/GROUP/項目の構造編集

**構成**:
- `FormTypeSelector`: フォームタイプ切替（STEP式/単一式）
- `StepGroupEditor`: STEP/GROUP/項目の階層構造編集
- `FieldList`: 項目一覧表示（`FieldCard`を使用）

**実装方針**:
- `FormItemPage.tsx`の構造編集部分を抽出してコンポーネント化
- ドラッグ&ドロップ機能を統合
- CSVインポート/エクスポート機能を統合

**実装状況**: ✅ 実装済み（2026-01-20）
- `FormStructureEditor.tsx`: STEP/GROUP/項目の構造編集コンポーネント
- ドラッグ&ドロップ機能: 実装済み
- CSVインポート/エクスポート: 実装済み

#### 3.4 右サイドパネル: `FieldDetailPanel`

**役割**: 項目詳細設定パネル（既存コンポーネントを再利用）

**実装方針**:
- 既存の`FieldDetailPanel`コンポーネントをそのまま使用
- 項目クリック時に表示/非表示を切り替え

**実装状況**: ✅ 実装済み（2026-01-20）
- 既存の`FieldDetailPanel`コンポーネントを統合編集画面で使用

### 4. 状態管理設計

#### 4.1 状態の分類

**A. フォーム基本情報関連**（`FormEditPage`から継承）
```typescript
interface FormBasicState {
  formCode: string;
  formStatus: FormStatus;
  formPublicPeriodStart: string;
  formPublicPeriodEnd: string;
  formAnswerPeriodStart: string;
  formAnswerPeriodEnd: string;
  formAttachmentEnabled: boolean;
  // ... その他の基本情報
}
```

**B. 通知設定関連**（`FormEditPage`から継承）
```typescript
interface FormNotificationState {
  notificationUserEnabled: boolean;
  notificationUserEmailFrom: string;
  notificationUserEmailReplyTo: string;
  notificationUserEmailCc: string;
  notificationUserEmailBcc: string;
  notificationAdminEnabled: boolean;
  notificationAdminUserIds: string;
  // ... その他の通知設定
}
```

**C. テーマ設定関連**（`FormEditPage`から継承）
```typescript
interface FormThemeState {
  themeId: number | null;
  themeTokens: Record<string, any> | null;
}
```

**D. 項目構造関連**（`FormItemPage`から継承）
```typescript
interface FormStructureState {
  fields: FormField[];
  steps: Step[];
  hasSteps: boolean;
  formType: "step" | "single" | null;
  selectedField: {
    field: FormField;
    stepIndex: number;
    groupIndex: number;
    fieldIndex: number;
  } | null;
  // ... その他の構造関連状態
}
```

#### 4.2 状態管理の一元化

**方針**: 
- 各セクションの状態を`FormEditIntegratedPage`で一元管理
- 子コンポーネントには必要な状態と更新関数をpropsで渡す
- 未保存の変更を検知して警告を表示

**実装例**:
```typescript
function FormEditIntegratedPage() {
  // 基本情報状態
  const [formBasicState, setFormBasicState] = useState<FormBasicState>({...});
  
  // 通知設定状態
  const [notificationState, setNotificationState] = useState<FormNotificationState>({...});
  
  // テーマ設定状態
  const [themeState, setThemeState] = useState<FormThemeState>({...});
  
  // 項目構造状態
  const [structureState, setStructureState] = useState<FormStructureState>({...});
  
  // 未保存の変更を検知
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  
  // ... 状態更新関数
}
```

### 5. データフロー

#### 5.1 データ取得フロー

```
1. FormEditIntegratedPage マウント
   ↓
2. 並列でAPI呼び出し
   ├─ GET /v1/forms/{form_id} (基本情報)
   ├─ GET /v1/forms/{form_id}/fields (項目構造)
   └─ GET /v1/system/themes (テーマ一覧)
   ↓
3. 各状態を初期化
   ├─ formBasicState
   ├─ notificationState
   ├─ themeState
   └─ structureState
   ↓
4. 子コンポーネントにpropsで渡す
```

#### 5.2 データ保存フロー

```
1. ユーザーが「保存」ボタンをクリック
   ↓
2. バリデーション実行
   ├─ 基本情報のバリデーション
   ├─ 通知設定のバリデーション
   └─ 項目構造のバリデーション
   ↓
3. バリデーションエラーがある場合
   └─ エラーメッセージを表示して終了
   ↓
4. バリデーション成功
   ↓
5. 並列でAPI呼び出し（または順次実行）
   ├─ PUT /v1/forms/{form_id} (基本情報)
   ├─ PUT /v1/forms/{form_id}/fields (項目構造)
   └─ 必要に応じて他のAPI
   ↓
6. 保存成功
   └─ 成功メッセージ表示、未保存フラグをクリア
```

### 6. 既存コンポーネントの再利用

#### 6.1 `FormEditPage`からの抽出

**抽出対象**:
1. **基本情報セクション**
   - フォームコード、ステータス、公開期間などの入力フォーム
   - ファイル: `FormEditPage.tsx` (約200-800行目あたり)

2. **通知設定セクション**
   - ユーザー通知、管理者通知の設定フォーム
   - ファイル: `FormEditPage.tsx` (約800-1500行目あたり)

3. **テーマ設定セクション**
   - テーマ選択、テーマトークンの編集
   - ファイル: `FormEditPage.tsx` (約1500-2000行目あたり)

**抽出方法**:
- 該当部分を独立したコンポーネントとして抽出
- Propsで状態と更新関数を受け取る
- 例: `FormBasicInfoSection`, `FormNotificationSection`, `FormThemeSection`

#### 6.2 `FormItemPage`からの抽出

**抽出対象**:
1. **フォームタイプ選択UI**
   - STEP式/単一式の切替ボタン
   - ファイル: `FormItemPage.tsx` (約1673-1699行目)

2. **STEP/GROUP/項目の構造編集**
   - 階層構造の表示と編集
   - ドラッグ&ドロップ機能
   - ファイル: `FormItemPage.tsx` (約1701-1970行目)

3. **CSVインポート/エクスポート**
   - CSV操作のUIとロジック
   - ファイル: `FormItemPage.tsx` (約568-576行目、2079-2184行目)

**抽出方法**:
- 構造編集部分を`FormStructureEditor`コンポーネントとして抽出
- 状態管理ロジックを親コンポーネントに移動
- 例: `FormStructureEditor`, `StepGroupEditor`, `FieldList`

#### 6.3 既存コンポーネントの再利用

**そのまま使用**:
- `FieldCard`: 項目カード表示（既に実装済み）
- `FieldDetailPanel`: 項目詳細設定パネル（既に実装済み）
- `Accordion`, `AccordionItem`: 折りたたみセクション（既に実装済み）
- `ConfirmDialog`: 確認ダイアログ（既に実装済み）
- `ProgressDisplay`: 進捗表示（既に実装済み）

### 7. 段階的な実装計画

#### フェーズ2.1: 基本構造の作成（1-2日）

**タスク**:
1. `FormEditIntegratedPage.tsx`の基本構造を作成
2. 3カラムレイアウトの実装
3. 左サイドバー、メインエリア、右サイドパネルの配置

**成果物**:
- 基本的なレイアウトが表示される
- 各セクションのプレースホルダーが表示される

**実装状況**: ✅ 実装済み（2026-01-20）

#### フェーズ2.2: 左サイドバーの統合（2-3日）

**タスク**:
1. `FormBasicInfoSection`コンポーネントの抽出・作成
2. `FormNotificationSection`コンポーネントの抽出・作成
3. `FormThemeSection`コンポーネントの抽出・作成
4. `Accordion`で折りたたみ可能に統合

**成果物**:
- 左サイドバーで基本情報、通知設定、テーマ設定が編集可能
- 各セクションが折りたたみ可能

**実装状況**: ✅ 実装済み（2026-01-20）

#### フェーズ2.3: メインエリアの統合（3-4日）

**タスク**:
1. `FormTypeSelector`コンポーネントの抽出・作成
2. `FormStructureEditor`コンポーネントの抽出・作成
3. ドラッグ&ドロップ機能の統合
4. CSVインポート/エクスポート機能の統合

**成果物**:
- メインエリアでフォームタイプの切替が可能
- STEP/GROUP/項目の構造編集が可能
- ドラッグ&ドロップで順序変更が可能

**実装状況**: ✅ 実装済み（2026-01-20）

#### フェーズ2.4: 右サイドパネルの統合（1日）

**タスク**:
1. `FieldDetailPanel`の統合
2. 項目クリック時の表示/非表示制御
3. 保存処理の統合

**成果物**:
- 項目クリック時に右サイドパネルで詳細設定が可能
- 保存処理が正常に動作

**実装状況**: ✅ 実装済み（2026-01-20）

#### フェーズ2.5: 状態管理の一元化（2-3日）

**タスク**:
1. 状態管理の一元化
2. 未保存の変更検知機能
3. 保存処理の統合
4. エラーハンドリングの統合

**成果物**:
- すべての状態が一元管理される
- 未保存の変更がある場合に警告が表示される
- 保存処理が正常に動作

**実装状況**: ✅ 実装済み（2026-01-20）
- 状態管理の一元化: 実装済み
- 未保存変更検知: 実装済み（一時保存機能と統合）
- 保存処理: 実装済み（`handleSaveAll`）

#### フェーズ2.6: ルーティングの更新（1日）

**タスク**:
1. ルーティング設定の更新
2. 既存画面からの遷移パスの更新
3. 後方互換性の確保（既存画面も残す）

**成果物**:
- 統合画面への遷移が可能
- 既存画面も引き続き動作

**実装状況**: ✅ 実装済み（2026-01-20）
- ルーティング: `${ROUTES.FORM_EDIT}/integrated` として追加済み
- 既存画面との互換性: 維持済み

### 8. 技術的な実装ポイント

#### 8.1 コンポーネント設計

**原則**:
- 単一責任の原則: 各コンポーネントは1つの責任のみを持つ
- 再利用性: 既存コンポーネントを最大限に再利用
- 疎結合: コンポーネント間の依存関係を最小化

**コンポーネント階層**:
```
FormEditIntegratedPage
├─ ScreenHeader
├─ FormEditSidebar
│  ├─ Accordion
│  │  ├─ AccordionItem (基本情報)
│  │  │  └─ FormBasicInfoSection
│  │  ├─ AccordionItem (通知設定)
│  │  │  └─ FormNotificationSection
│  │  └─ AccordionItem (テーマ設定)
│  │     └─ FormThemeSection
├─ FormStructureEditor
│  ├─ FormTypeSelector
│  ├─ StepGroupEditor
│  │  ├─ StepCard (複数)
│  │  │  ├─ GroupCard (複数)
│  │  │  │  └─ FieldCard (複数)
│  │  │  └─ AddGroupButton
│  │  └─ AddStepButton
│  └─ CSVOperations
└─ FieldDetailPanel (条件付き表示)
```

#### 8.2 状態管理

**状態の分類**:
1. **サーバー状態**: APIから取得したデータ（form, fields, themes等）
2. **UI状態**: 画面の表示状態（selectedField, isSidebarOpen等）
3. **編集状態**: 編集中の一時的なデータ（editFieldKey, editType等）

**状態管理のパターン**:
- サーバー状態: `useState` + `useEffect`でAPIから取得
- UI状態: `useState`で管理
- 編集状態: 各コンポーネントで`useState`で管理、親に保存関数を渡す

#### 8.3 パフォーマンス最適化

**考慮事項**:
1. **大量の項目がある場合**
   - 仮想スクロールの導入を検討（react-window等）
   - 項目の遅延読み込み

2. **詳細設定パネルの遅延読み込み**
   - `FieldDetailPanel`を`React.lazy`で遅延読み込み
   - 項目が選択された時のみ読み込む

3. **ドラッグ&ドロップの最適化**
   - ドラッグ中の再レンダリングを最小化
   - `useMemo`でドラッグ対象の計算を最適化

4. **状態更新の最適化**
   - 不要な再レンダリングを防ぐため`React.memo`を使用
   - `useCallback`で関数の再生成を防ぐ

#### 8.4 API連携

**APIエンドポイント**:
- `GET /v1/forms/{form_id}`: フォーム基本情報取得
- `PUT /v1/forms/{form_id}`: フォーム基本情報更新
- `GET /v1/forms/{form_id}/fields`: 項目構造取得
- `PUT /v1/forms/{form_id}/fields`: 項目構造更新
- `GET /v1/system/themes`: テーマ一覧取得
- `POST /v1/forms/{form_id}/fields/import/csv`: CSVインポート
- `POST /v1/forms/{form_id}/fields/export/csv`: CSVエクスポート

**エラーハンドリング**:
- APIエラーは`apiFetch.ts`で統一処理
- バリデーションエラーは各コンポーネントで表示
- ネットワークエラーはToastで通知

#### 8.5 未保存の変更検知

**実装方法**:
1. 初期状態を保存
2. 各状態変更時に初期状態と比較
3. 差分がある場合に`hasUnsavedChanges`を`true`に設定
4. ページ離脱時に警告を表示（`beforeunload`イベント）

**実装例**:
```typescript
const [initialState, setInitialState] = useState(null);
const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);

useEffect(() => {
  // 初期状態を保存
  setInitialState({
    formBasic: formBasicState,
    notification: notificationState,
    theme: themeState,
    structure: structureState,
  });
}, []);

useEffect(() => {
  // 状態変更を検知
  if (initialState) {
    const hasChanges = 
      JSON.stringify(formBasicState) !== JSON.stringify(initialState.formBasic) ||
      JSON.stringify(notificationState) !== JSON.stringify(initialState.notification) ||
      JSON.stringify(themeState) !== JSON.stringify(initialState.theme) ||
      JSON.stringify(structureState) !== JSON.stringify(initialState.structure);
    setHasUnsavedChanges(hasChanges);
  }
}, [formBasicState, notificationState, themeState, structureState]);

useEffect(() => {
  // ページ離脱時の警告
  const handleBeforeUnload = (e: BeforeUnloadEvent) => {
    if (hasUnsavedChanges) {
      e.preventDefault();
      e.returnValue = '';
    }
  };
  window.addEventListener('beforeunload', handleBeforeUnload);
  return () => window.removeEventListener('beforeunload', handleBeforeUnload);
}, [hasUnsavedChanges]);
```

### 9. 実装時の注意点

#### 9.1 既存機能の互換性

- 既存の`FormEditPage`と`FormItemPage`は残す（後方互換性）
- 統合画面は新しいルートとして追加
- 段階的に移行を進める

#### 9.2 テスト

**テスト項目**:
1. 基本情報の編集・保存
2. 通知設定の編集・保存
3. テーマ設定の編集・保存
4. 項目構造の編集・保存
5. ドラッグ&ドロップによる順序変更
6. CSVインポート/エクスポート
7. 未保存の変更検知
8. エラーハンドリング

#### 9.3 パフォーマンステスト

**テスト項目**:
1. 大量の項目（100件以上）がある場合の表示速度
2. ドラッグ&ドロップの応答性
3. 詳細設定パネルの表示速度
4. 保存処理の実行時間

### 10. 実装ファイル一覧

**新規作成**:
- `src/pages/forms/FormEditIntegratedPage.tsx` (メインコンポーネント) ✅ 実装済み
- `src/components/forms/FormBasicInfoSection.tsx` (基本情報セクション) ✅ 実装済み
- `src/components/forms/FormNotificationSection.tsx` (通知設定セクション) ✅ 実装済み
- `src/components/forms/FormThemeSection.tsx` (テーマ設定セクション) ✅ 実装済み
- `src/components/forms/FormStructureEditor.tsx` (構造編集コンポーネント) ✅ 実装済み

**既存ファイルの変更**:
- `src/routePaths.ts` (ルーティング追加) ✅ 実装済み
- `src/App.tsx` (ルーティング設定追加) ✅ 実装済み

**実装状況**: ✅ 実装済み（2026-01-20）

**既存ファイル（変更なし、再利用）**:
- `src/components/FieldCard.tsx`
- `src/components/FieldDetailPanel.tsx`
- `src/components/Accordion.tsx`
- `src/components/ConfirmDialog.tsx`
- `src/components/ProgressDisplay.tsx`

---

## 一時保存機能の仕様

### 作成日時
2026-01-20

---

### 1. 概要

フォーム編集画面でのデータ編集時に、ローカルストレージを使用した一時保存機能を実装します。これにより、ブラウザを閉じたり、誤ってページを離脱した場合でも、編集中のデータを復元できるようにします。

### 2. 基本仕様

#### 2.1 データ編集時（既存フォームの編集）

**初期表示時**:
1. APIからフォームデータを取得
2. 取得したデータをローカルストレージに保存（初期状態として）
3. 保存済みフラグを「保存済み」に設定

**データ変更時**:
1. 画面での全ての変更をリアルタイムでローカルストレージに保存
2. 保存済みフラグを「未保存」に設定
3. 変更内容は以下の全てを含む:
   - 基本情報（フォームコード、ステータス、公開期間など）
   - 通知設定（ユーザー通知、管理者通知）
   - テーマ設定（テーマID、テーマトークン）
   - 項目構造（STEP/GROUP/項目の階層構造）
   - 多言語データ（翻訳情報、ラベル情報）

**API保存成功時**:
1. 保存済みフラグを「保存済み」に設定
2. 一時保存データを更新（最新の保存済み状態を反映）

#### 2.2 データ新規作成時

**初期表示時**:
1. 空のフォームデータをローカルストレージに保存
2. 保存済みフラグを「未保存」に設定

**データ変更時**:
1. 画面での全ての変更をリアルタイムでローカルストレージに保存
2. 保存済みフラグは「未保存」のまま

**API保存成功時**:
1. フォームIDが発行される
2. ローカルストレージのキーを新しいフォームIDに更新
3. 保存済みフラグを「保存済み」に設定

#### 2.3 一時保存データの利用

一時保存データは以下の用途で利用します:

1. **言語タブの選択状態**
   - 最後に選択していた言語タブを復元
   - 例: `activeLanguageTab: "ja"`

2. **条件分岐のフィールド指定値**
   - 条件分岐ルールで選択していたフィールドを復元
   - 例: `visibilityRule.field: "field_key_1"`

3. **その他のUI状態**
   - 開いていたアコーディオンセクション
   - 選択していたタブ
   - 編集中の項目

#### 2.4 保存済みフラグの管理

**保存済みフラグの状態**:
- `saved`: 最後のAPI保存が成功し、その後の変更がない
- `unsaved`: 最後のAPI保存以降に変更がある

**フラグの更新タイミング**:
- 初期表示時（APIデータ取得後）: `saved`
- データ変更時: `unsaved`
- API保存成功時: `saved`
- API保存失敗時: `unsaved`のまま

#### 2.5 画面遷移時の処理

**未保存データがある場合**:
1. 画面遷移を伴う操作発生時に、確認ダイアログを表示
2. ユーザーに以下の選択肢を提示:
   - **保存する**: API保存を実行し、成功後に画面遷移
   - **破棄する**: 一時保存データをクリアして画面遷移
   - **キャンセル**: 画面遷移をキャンセル

**保存する場合の処理**:
1. 保存APIを呼び出し
2. 成功時:
   - 保存済みフラグを「保存済み」に設定
   - 一時保存データを更新
   - 画面遷移を実行
3. 失敗時:
   - エラーメッセージを表示
   - 画面遷移をキャンセル

**破棄する場合の処理**:
1. 一時保存データをクリア
2. 画面遷移を実行

**キャンセルする場合の処理**:
1. 画面遷移をキャンセル
2. 編集画面に留まる

### 3. 一時保存データの構造

```typescript
interface TemporaryFormData {
  // メタデータ
  formId: string | "new"; // フォームID（新規作成時は"new"）
  savedAt: string; // 保存日時（ISO 8601形式）
  savedFlag: "saved" | "unsaved"; // 保存済みフラグ
  tabId: string; // タブ識別ID（複数タブ対応用）
  lastSavedByTab: string | null; // 最後に保存したタブのID（API保存時のみ設定）
  
  // 基本情報
  formBasic: {
    code: string;
    status: FormStatus;
    publicPeriodStart: string;
    publicPeriodEnd: string;
    answerPeriodStart: string;
    answerPeriodEnd: string;
    attachmentEnabled: boolean;
    // ... その他の基本情報
  };
  
  // 通知設定
  notification: {
    userEnabled: boolean;
    userEmailFrom: string;
    userEmailReplyTo: string;
    userEmailCc: string;
    userEmailBcc: string;
    adminEnabled: boolean;
    adminUserIds: string;
    adminEmailFrom: string;
    adminEmailReplyTo: string;
    // ... その他の通知設定
  };
  
  // テーマ設定
  theme: {
    themeId: number | null;
    themeTokens: Record<string, any> | null;
  };
  
  // 項目構造
  structure: {
    formType: "step" | "single" | null;
    hasSteps: boolean;
    steps: Step[];
    fields: FormField[];
  };
  
  // 多言語データ
  translations: Record<string, {
    title: string;
    description: string | null;
    // ... その他の翻訳情報
  }>;
  
  // UI状態
  uiState: {
    activeLanguageTab: string | null;
    activeNotificationUserLanguageTab: string | null;
    activeNotificationAdminLanguageTab: string | null;
    activeAttachmentLanguageTab: string | null;
    isBasicInfoOpen: boolean;
    isNotificationUserSettingsOpen: boolean;
    isNotificationAdminSettingsOpen: boolean;
    isThemeSettingsOpen: boolean;
    isAttachmentSettingsOpen: boolean;
    selectedField: {
      stepIndex: number;
      groupIndex: number;
      fieldIndex: number;
    } | null;
    // ... その他のUI状態
  };
}
```

### 4. ストレージのキー設計

#### 4.1 IndexedDBを使用する場合

**データベース名**: `ReFormaFormBuilder`

**オブジェクトストア**: `temporaryForms`

**キーパス**: `formId`（主キー）

**インデックス**:
- `savedAt`: 保存日時（ソート用）
- `savedFlag`: 保存済みフラグ（検索用）

**データ構造**:
```typescript
interface IndexedDBFormData {
  formId: string | "new"; // 主キー
  savedAt: string; // ISO 8601形式
  savedFlag: "saved" | "unsaved";
  data: TemporaryFormData; // 実際のデータ
}
```

**例**:
- 既存フォーム編集: `formId: "1"`
- 新規作成: `formId: "new"`

#### 4.2 ローカルストレージを使用する場合（フォールバック）

**キー形式**:
```
reforma_form_edit_{formId}
```

**例**:
- 既存フォーム編集: `reforma_form_edit_1`
- 新規作成: `reforma_form_edit_new`

**注意点**:
- 新規作成時は`formId`が`"new"`のまま
- API保存成功後、フォームIDが発行されたら、キーを更新する必要がある

### 5. 実装の詳細

#### 5.1 データ保存のタイミング

**リアルタイム保存**:
- 各状態変更時に`useEffect`で自動保存
- デバウンス処理（500ms）を適用して、頻繁な保存を抑制

**実装例**:
```typescript
// デバウンス処理
const [saveTimeout, setSaveTimeout] = useState<NodeJS.Timeout | null>(null);

useEffect(() => {
  if (saveTimeout) {
    clearTimeout(saveTimeout);
  }
  
  const timeout = setTimeout(() => {
    saveToLocalStorage();
  }, 500);
  
  setSaveTimeout(timeout);
  
  return () => {
    if (saveTimeout) {
      clearTimeout(saveTimeout);
    }
  };
}, [formBasicState, notificationState, themeState, structureState, uiState]);
```

#### 5.2 データ復元のタイミング

**初期表示時**:
1. ローカルストレージからデータを取得
2. データが存在する場合:
   - 確認ダイアログを表示（復元/破棄/キャンセル）
   - ユーザーが「復元」を選択した場合、ローカルストレージのデータを反映
3. データが存在しない場合:
   - APIから最新データを取得
   - 取得したデータをローカルストレージに保存

#### 5.3 画面遷移時の検知

**検知対象**:
- ルーティングによる画面遷移（`useNavigate`）
- ブラウザの戻る/進むボタン
- ブラウザタブの閉じる
- ページのリロード

**実装方法**:
```typescript
// ルーティング遷移の検知
const navigate = useNavigate();
const handleNavigation = (path: string) => {
  if (savedFlag === "unsaved") {
    setPendingNavigation(path);
    setShowUnsavedChangesDialog(true);
  } else {
    navigate(path);
  }
};

// ブラウザの戻る/進む、タブ閉じるの検知
useEffect(() => {
  const handleBeforeUnload = (e: BeforeUnloadEvent) => {
    if (savedFlag === "unsaved") {
      e.preventDefault();
      e.returnValue = '';
    }
  };
  window.addEventListener('beforeunload', handleBeforeUnload);
  return () => window.removeEventListener('beforeunload', handleBeforeUnload);
}, [savedFlag]);
```

### 6. 問題点と対策

#### 6.1 ローカルストレージの容量制限

**問題**:
- ローカルストレージの容量は通常5-10MB
- 大量の項目や多言語データがある場合、容量超過の可能性

**対策（推奨）: IndexedDBの使用**

IndexedDBを使用することで、容量制限の問題を根本的に解決できます。

**IndexedDBの利点**:
- **大容量**: 通常数百MBから数GBまで保存可能（ブラウザ依存）
- **非同期API**: 大量データの保存/取得でもUIをブロックしない
- **構造化データ**: オブジェクトストアを使用して構造化されたデータを保存可能
- **インデックス**: 高速な検索が可能
- **トランザクション**: データの整合性を保証

**実装方針**:
1. **IndexedDBの導入**: ローカルストレージの代わりにIndexedDBを使用
2. **フォールバック**: IndexedDBが使用できない場合、ローカルストレージにフォールバック
3. **データ構造**: オブジェクトストアを使用して構造化されたデータを保存
4. **非同期処理**: 保存/取得を非同期で処理

**実装例**:
```typescript
// IndexedDBの初期化
async function initIndexedDB(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('ReFormaFormBuilder', 1);
    
    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);
    
    request.onupgradeneeded = (event) => {
      const db = (event.target as IDBOpenDBRequest).result;
      
      // オブジェクトストアの作成
      if (!db.objectStoreNames.contains('temporaryForms')) {
        const store = db.createObjectStore('temporaryForms', { keyPath: 'formId' });
        store.createIndex('savedAt', 'savedAt', { unique: false });
        store.createIndex('savedFlag', 'savedFlag', { unique: false });
      }
    };
  });
}

// データの保存
async function saveToIndexedDB(formId: string, data: TemporaryFormData): Promise<void> {
  const db = await initIndexedDB();
  const transaction = db.transaction(['temporaryForms'], 'readwrite');
  const store = transaction.objectStore('temporaryForms');
  
  await new Promise<void>((resolve, reject) => {
    const request = store.put({ formId, ...data, savedAt: new Date().toISOString() });
    request.onsuccess = () => resolve();
    request.onerror = () => reject(request.error);
  });
  
  db.close();
}

// データの取得
async function getFromIndexedDB(formId: string): Promise<TemporaryFormData | null> {
  const db = await initIndexedDB();
  const transaction = db.transaction(['temporaryForms'], 'readonly');
  const store = transaction.objectStore('temporaryForms');
  
  return new Promise((resolve, reject) => {
    const request = store.get(formId);
    request.onsuccess = () => {
      const result = request.result;
      if (result) {
        const { formId: _, ...data } = result;
        resolve(data as TemporaryFormData);
      } else {
        resolve(null);
      }
    };
    request.onerror = () => reject(request.error);
  });
}
```

**代替対策（IndexedDBが使用できない場合）**:
1. **データの圧縮**: JSON文字列を圧縮（例: LZ-string）
2. **不要データの除外**: UI状態など、復元不要なデータは保存しない
3. **データの分割**: 基本情報、項目構造、UI状態を別々のキーで保存
4. **容量チェック**: 保存前に容量をチェックし、超過時は警告

#### 6.2 複数タブ/ウィンドウでの同時編集

**問題**:
- 同じフォームを複数のタブで開いた場合、データの競合が発生

**重要な確認事項**:

**Q: 別タブで違うフォームを開いた場合、一時保存データが上書きされる？**

**A: いいえ、上書きされません。**

**理由**:
- 各フォームIDごとに別々のキー/レコードで保存される
- IndexedDBの場合: `formId`が主キーとして使用されるため、フォームIDごとに別レコード
- ローカルストレージの場合: キー形式が`reforma_form_edit_{formId}`のため、フォームIDごとに別キー

**例**:
- タブ1: フォームID=1 → キー: `reforma_form_edit_1` または IndexedDBの`formId: "1"`
- タブ2: フォームID=2 → キー: `reforma_form_edit_2` または IndexedDBの`formId: "2"`
- タブ3: フォームID=1（同じフォーム） → キー: `reforma_form_edit_1` または IndexedDBの`formId: "1"`（競合の可能性）

**競合が発生するケース**:
- **同じフォームを複数タブで開いた場合**: 同じキー/レコードを使用するため、最後に保存したタブのデータが上書きされる
- **新規作成を複数タブで開いた場合**: すべて`formId: "new"`のため、同じキー/レコードを使用

**対策方針**:
1. **タブ識別**: 各タブに一意のIDを付与し、一時保存データに含める
2. **更新検知**: `storage`イベント（ローカルストレージ）またはIndexedDBの変更イベントで他のタブの更新を検知
3. **警告表示**: 他のタブで編集されている場合に警告ダイアログを表示
4. **ユーザー選択**: 警告ダイアログで操作を継続するか、キャンセルするかをユーザーに選択させる
5. **データ同期**: ユーザーが「最新データを取得」を選択した場合、APIから最新データを取得して反映

**実装例（ローカルストレージの場合）**:
```typescript
// タブ識別
const tabId = useRef(`tab_${Date.now()}_${Math.random()}`);

// 一時保存データにタブIDを含める
interface TemporaryFormData {
  // ... 既存のフィールド
  tabId: string; // タブ識別ID
  lastSavedByTab: string | null; // 最後に保存したタブのID
}

// 他のタブの更新を検知（同じフォームIDの場合のみ）
useEffect(() => {
  const handleStorageChange = (e: StorageEvent) => {
    // 同じフォームIDのキーのみチェック
    if (e.key === getStorageKey() && e.newValue) {
      try {
        const updatedData = JSON.parse(e.newValue);
        // 他のタブで更新があった場合（自分のタブ以外）
        if (updatedData.tabId !== tabId.current) {
          setShowConflictWarning(true);
          setConflictData(updatedData);
        }
      } catch (err) {
        console.error('Failed to parse storage data:', err);
      }
    }
  };
  window.addEventListener('storage', handleStorageChange);
  return () => window.removeEventListener('storage', handleStorageChange);
}, [formId]);
```

**実装例（IndexedDBの場合）**:
```typescript
// タブ識別
const tabId = useRef(`tab_${Date.now()}_${Math.random()}`);

// IndexedDBの変更を検知（同じフォームIDの場合のみ）
useEffect(() => {
  let lastCheckedSavedAt: string | null = null;
  
  const handleIndexedDBChange = async () => {
    try {
      const currentData = await getFromIndexedDB(formId);
      if (currentData) {
        // 他のタブで更新があった場合（自分のタブ以外、または保存日時が変更された場合）
        if (currentData.tabId !== tabId.current && 
            currentData.savedAt !== lastCheckedSavedAt) {
          setShowConflictWarning(true);
          setConflictData(currentData);
          lastCheckedSavedAt = currentData.savedAt;
        }
      }
    } catch (err) {
      console.error('Failed to check IndexedDB:', err);
    }
  };
  
  // 定期的にチェック（例: 3秒ごと）
  const interval = setInterval(handleIndexedDBChange, 3000);
  return () => clearInterval(interval);
}, [formId]);
```

**警告ダイアログの実装**:
```typescript
// 競合警告ダイアログ
<ConfirmDialog
  open={showConflictWarning}
  title="他のタブで編集されています"
  description="このフォームは他のタブでも編集されています。操作を継続しますか？"
  primaryButton={{
    label: "継続する",
    onClick: () => {
      setShowConflictWarning(false);
      // 現在のタブの編集を継続
    },
  }}
  secondaryButton={{
    label: "最新データを取得",
    onClick: async () => {
      // APIから最新データを取得
      const latestData = await fetchLatestFormData(formId);
      // 現在のタブのデータを最新データで上書き
      await saveToStorage(formId, latestData);
      setShowConflictWarning(false);
    },
  }}
  cancelButton={{
    label: "キャンセル",
    onClick: () => {
      setShowConflictWarning(false);
    },
  }}
  onClose={() => setShowConflictWarning(false)}
/>
```

#### 6.3 データの整合性

**問題**:
- ローカルストレージのデータが破損している可能性
- データ構造が変更された場合の互換性

**対策**:
1. **バージョン管理**: データ構造にバージョン番号を含める
2. **バリデーション**: 復元時にデータの整合性をチェック
3. **フォールバック**: 整合性チェックに失敗した場合、APIから再取得
4. **マイグレーション**: 古いバージョンのデータを新しい形式に変換

**実装例**:
```typescript
interface TemporaryFormData {
  version: string; // データ構造のバージョン
  // ... その他のデータ
}

function validateTemporaryData(data: any): boolean {
  if (!data || !data.version) return false;
  if (data.version !== CURRENT_DATA_VERSION) return false;
  // その他の整合性チェック
  return true;
}
```

#### 6.4 保存タイミングの最適化

**問題**:
- 頻繁な保存によるパフォーマンス低下
- デバウンス処理の実装が複雑

**対策**:
1. **デバウンス処理**: 500msのデバウンスを適用
2. **バッチ保存**: 複数の変更をまとめて保存
3. **重要度による優先順位**: 重要な変更は即座に保存、UI状態は遅延保存

#### 6.5 ブラウザのプライベートモード

**問題**:
- プライベートモードではローカルストレージやIndexedDBが制限される場合がある
- ブラウザを閉じるとデータが削除される

**対策**:
1. **IndexedDBの使用**: IndexedDBはプライベートモードでも使用可能（ブラウザ依存）
2. **フォールバック**: IndexedDBが使用できない場合、メモリ上で管理
3. **警告表示**: プライベートモードの場合に警告を表示（データが保持されない可能性があることを通知）
4. **定期的な保存**: プライベートモードでは、より頻繁にAPI保存を促す

#### 6.6 データの有効期限

**問題**:
- 古い一時保存データが残り続ける可能性

**対策**:
1. **有効期限の設定**: 7日間など、有効期限を設定
2. **自動クリーンアップ**: 有効期限切れのデータを自動削除
3. **手動クリーンアップ**: 設定画面から手動でクリーンアップ可能に

#### 6.7 新規作成時のフォームID発行後の処理

**問題**:
- 新規作成時は`formId`が`"new"`だが、保存後に実際のIDが発行される
- キーの更新が必要

**対策**:
1. **キーの更新**: 保存成功後、古いキーを削除し、新しいキーで保存
2. **移行処理**: 古いキーのデータを新しいキーに移行

**実装例**:
```typescript
async function handleSave() {
  try {
    const response = await apiPutJson(`/v1/forms/${formId}`, formData);
    if (response.success) {
      // 新規作成の場合、フォームIDが発行される
      const newFormId = response.data.form.id;
      
      if (formId === "new" && newFormId) {
        // 古いキーのデータを取得
        const oldData = localStorage.getItem(`reforma_form_edit_new`);
        if (oldData) {
          // 新しいキーで保存
          localStorage.setItem(`reforma_form_edit_${newFormId}`, oldData);
          // 古いキーを削除
          localStorage.removeItem(`reforma_form_edit_new`);
        }
        // フォームIDを更新
        setFormId(newFormId);
      }
      
      // 保存済みフラグを更新
      setSavedFlag("saved");
    }
  } catch (error) {
    // エラーハンドリング
  }
}
```

#### 6.8 言語タブや条件フィールドの復元

**問題**:
- 一時保存データから言語タブや条件フィールドの値を復元する際、データが存在しない場合の処理

**対策**:
1. **デフォルト値の設定**: データが存在しない場合、デフォルト値を設定
2. **バリデーション**: 復元した値が有効かチェック
3. **段階的復元**: まず基本データを復元し、その後UI状態を復元

### 7. 実装の優先順位

#### フェーズ1: 基本機能（必須） ✅ 実装済み
1. ローカルストレージへの保存/復元 ✅
2. 保存済みフラグの管理 ✅
3. 画面遷移時の確認ダイアログ ✅

#### フェーズ2: 最適化（推奨） ✅ 実装済み
4. デバウンス処理 ✅（3秒のdebounce）
5. データのバリデーション ✅
6. 容量チェック ✅（IndexedDB使用により容量問題を解決）

#### フェーズ3: 高度な機能（オプション） ✅ 実装済み
7. 複数タブ対応 ✅（タブ識別と競合検知機能）
8. データの圧縮 ⚠️ 未実装（IndexedDB使用により容量問題は解決済み）
9. 自動クリーンアップ ⚠️ 未実装

### 8. その他決めておくべき事項

#### 8.1 新規作成時の複数タブ対応

**問題**:
- 新規作成時はすべて`formId: "new"`のため、複数タブで開くと同じキー/レコードを使用する

**対策**:
1. **タブ識別による分離**: 新規作成時もタブIDを含めて識別
2. **キー設計の変更**: 新規作成時は`reforma_form_edit_new_{tabId}`の形式で保存
3. **保存成功後の処理**: API保存成功後、フォームIDが発行されたら、タブID付きキーから通常のキーに移行

**実装例**:
```typescript
// 新規作成時のキー生成
function getStorageKey(formId: string, tabId: string): string {
  if (formId === "new") {
    return `reforma_form_edit_new_${tabId}`;
  }
  return `reforma_form_edit_${formId}`;
}
```

#### 8.2 データの同期方法

**方針**:
- 他のタブで保存された場合、現在のタブのデータをどうするか

**選択肢**:
1. **自動的に最新データを取得**: 他のタブで保存された場合、自動的にAPIから最新データを取得
2. **ユーザーに選択させる**: 警告ダイアログで「最新データを取得」を選択できるようにする（推奨）

**推奨**: 選択肢2（ユーザーに選択させる）
- 理由: 現在編集中のデータを失う可能性があるため、ユーザーに判断を委ねる

#### 8.3 警告ダイアログの内容

**表示タイミング**:
1. 他のタブで一時保存データが更新された場合
2. 他のタブでAPI保存が成功した場合

**ダイアログの選択肢**:
1. **継続する**: 現在のタブの編集を継続（他のタブの変更は無視）
2. **最新データを取得**: APIから最新データを取得して現在のタブのデータを上書き
3. **キャンセル**: ダイアログを閉じる（編集は継続）

**メッセージ例**:
```
このフォームは他のタブでも編集されています。
操作を継続しますか？

[継続する] [最新データを取得] [キャンセル]
```

#### 8.4 タブ識別の方法

**実装方法**:
1. **タブIDの生成**: ページ読み込み時に一意のIDを生成
2. **タブIDの保存**: 一時保存データに`tabId`フィールドとして含める
3. **タブIDの永続化**: ページリロード時も同じタブIDを使用（sessionStorageを使用）

**実装例**:
```typescript
// タブIDの生成と永続化
function getOrCreateTabId(): string {
  // sessionStorageから取得を試みる
  let tabId = sessionStorage.getItem('reforma_tab_id');
  if (!tabId) {
    // 新規生成
    tabId = `tab_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    sessionStorage.setItem('reforma_tab_id', tabId);
  }
  return tabId;
}
```

#### 8.5 更新検知の頻度

**方針**:
- 他のタブの更新をどのくらいの頻度で検知するか

**選択肢**:
1. **リアルタイム**: `storage`イベント（ローカルストレージ）またはBroadcastChannel API（IndexedDB）
2. **定期的なポーリング**: 3-5秒ごとにチェック

**推奨**: 
- ローカルストレージ: `storage`イベント（リアルタイム）
- IndexedDB: 定期的なポーリング（3秒ごと）+ BroadcastChannel API（可能な場合）

#### 8.6 保存済みフラグの更新

**問題**:
- 他のタブでAPI保存が成功した場合、現在のタブの保存済みフラグをどう更新するか

**方針**:
1. **自動更新**: 他のタブで保存された場合、現在のタブの保存済みフラグを「保存済み」に更新
2. **手動更新**: ユーザーが「最新データを取得」を選択した場合のみ更新

**推奨**: 選択肢2（手動更新）
- 理由: 現在のタブで未保存の変更がある場合、自動的に「保存済み」にすると混乱を招く可能性がある

#### 8.7 データの優先順位

**問題**:
- 複数タブで同時に編集している場合、どのデータを優先するか

**方針**:
1. **最後に保存した時刻で判断**: `savedAt`フィールドで最新のデータを判断
2. **API保存を優先**: API保存が成功したデータを優先
3. **ユーザーに選択させる**: 警告ダイアログでユーザーに選択させる

**推奨**: 選択肢3（ユーザーに選択させる）
- 理由: データの損失を防ぐため

#### 8.8 画面遷移時の処理

**問題**:
- 他のタブで編集されている場合、画面遷移時の確認ダイアログをどう表示するか

**方針**:
1. **通常の未保存警告を優先**: 他のタブの編集状態に関係なく、現在のタブの未保存状態のみをチェック
2. **両方をチェック**: 他のタブの編集状態も考慮して警告を表示

**推奨**: 選択肢1（通常の未保存警告を優先）
- 理由: 画面遷移時の確認は現在のタブの状態に基づくべき

### 9. 実装ファイル

**新規作成**:
- `src/utils/temporaryStorage.ts` (一時保存機能のユーティリティ、IndexedDB/ローカルストレージの抽象化) ✅ 実装済み
- `src/utils/indexedDB.ts` (IndexedDB操作のユーティリティ) ✅ 実装済み
- `src/utils/tabId.ts` (タブ識別のユーティリティ) ✅ 実装済み

**既存ファイルの変更**:
- `src/pages/forms/FormEditIntegratedPage.tsx` (一時保存機能の統合) ✅ 実装済み

**実装状況**: ✅ 実装済み（2026-01-20）
- 一時保存機能: IndexedDB/ローカルストレージ/メモリの3段階フォールバック対応
- 自動保存: 3秒のdebounce付きで実装済み
- データ復元: ページ読み込み時に自動復元
- タブ間競合検知: 実装済み（警告ダイアログ表示）

### 9. IndexedDB実装の詳細

#### 9.1 IndexedDBの初期化

**データベース名**: `ReFormaFormBuilder`
**バージョン**: `1.0`（将来のスキーマ変更に対応）

**注意**: IndexedDBのバージョンは数値型のため、実装コードでは`1`を使用しますが、ドキュメント上では`1.0`と表記します。

**オブジェクトストア**:
- `temporaryForms`: 一時保存データを保存
  - キーパス: `formId`
  - インデックス: `savedAt`, `savedFlag`

#### 9.2 フォールバック戦略

**優先順位**:
1. **IndexedDB**: まずIndexedDBの使用を試みる
2. **ローカルストレージ**: IndexedDBが使用できない場合、ローカルストレージにフォールバック
3. **メモリ**: どちらも使用できない場合、メモリ上で管理（セッション終了時に消失）

**実装例**:
```typescript
class TemporaryStorage {
  private storageType: 'indexeddb' | 'localstorage' | 'memory' = 'indexeddb';
  private memoryStorage: Map<string, TemporaryFormData> = new Map();
  
  async init(): Promise<void> {
    // IndexedDBの使用可能性をチェック
    if (this.isIndexedDBAvailable()) {
      try {
        await this.initIndexedDB();
        this.storageType = 'indexeddb';
        return;
      } catch (error) {
        console.warn('IndexedDB initialization failed, falling back to localStorage', error);
      }
    }
    
    // ローカルストレージの使用可能性をチェック
    if (this.isLocalStorageAvailable()) {
      this.storageType = 'localstorage';
      return;
    }
    
    // メモリストレージにフォールバック
    this.storageType = 'memory';
    console.warn('Using memory storage. Data will be lost on page reload.');
  }
  
  async save(formId: string, data: TemporaryFormData): Promise<void> {
    switch (this.storageType) {
      case 'indexeddb':
        return this.saveToIndexedDB(formId, data);
      case 'localstorage':
        return this.saveToLocalStorage(formId, data);
      case 'memory':
        return this.saveToMemory(formId, data);
    }
  }
  
  async get(formId: string): Promise<TemporaryFormData | null> {
    switch (this.storageType) {
      case 'indexeddb':
        return this.getFromIndexedDB(formId);
      case 'localstorage':
        return this.getFromLocalStorage(formId);
      case 'memory':
        return this.getFromMemory(formId);
    }
  }
}
```

#### 9.3 パフォーマンス考慮事項

**IndexedDBの利点**:
- 非同期処理によりUIをブロックしない
- 大量データでも高速に動作
- トランザクションによる整合性保証

**注意点**:
- 非同期APIのため、`async/await`を使用
- エラーハンドリングが重要
- データベース接続の適切な管理（開いたら閉じる）

#### 9.4 ブラウザ互換性

**IndexedDBのサポート**:
- Chrome: 対応（バージョン24以降）
- Firefox: 対応（バージョン16以降）
- Safari: 対応（バージョン10以降）
- Edge: 対応（バージョン12以降）

**フォールバック**:
- 古いブラウザではローカルストレージに自動的にフォールバック
- さらに古いブラウザではメモリストレージにフォールバック

---

## 参考資料

- `src/pages/forms/FormEditPage.tsx` (現在のフォーム編集画面)
- `src/pages/forms/FormItemPage.tsx` (現在のフォーム項目設定画面、一時保存機能の実装例)
- `docs/SUPP-FORM-STEP-001-spec.md` (STEP式フォーム仕様)
