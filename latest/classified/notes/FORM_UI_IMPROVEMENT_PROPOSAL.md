# フォーム作成/編集UI改善提案

## 作成日時
2026-01-13

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
1. **項目一覧の視覚化**
   - カード形式での表示
   - 項目の基本情報を一目で確認可能に

2. **詳細設定の分離**
   - 項目クリック → モーダル/サイドパネルで詳細設定
   - 基本設定と高度な設定を分離

3. **設定セクションの折りたたみ**
   - 基本情報、通知設定などを折りたたみ可能に
   - 必要な時だけ展開

#### フェーズ2: 構造改善（中期）
4. **ウィザード形式の導入**
   - 新規作成時のウィザード
   - 既存フォーム編集時は統合UI

5. **ドラッグ&ドロップの強化**
   - STEP/GROUP/項目の順序変更
   - 視覚的フィードバック

#### フェーズ3: 高度な機能（長期）
6. **リアルタイムプレビュー**
   - 設定変更時の即座の反映
   - 条件分岐の動作確認

7. **テンプレート機能**
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

#### 2.1 画面統合
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

#### 2.2 ウィザード形式の導入
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

## 参考資料

- `src/pages/forms/FormEditPage.tsx` (現在のフォーム編集画面)
- `src/pages/forms/FormItemPage.tsx` (現在のフォーム項目設定画面)
- `docs/SUPP-FORM-STEP-001-spec.md` (STEP式フォーム仕様)
