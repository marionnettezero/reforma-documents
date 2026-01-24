# リアルタイムプレビュー機能強化タスク

## 概要

リアルタイムプレビューに以下の機能を追加します：
1. ボタンの表示（送信ボタン、次へボタン、戻るボタン）でボタンスタイルを確認できるようにする
2. STEP式フォームの場合、STEP移動ができるようにする

## 現状確認

### 問題点

1. **ボタンが表示されない**:
   - `FormRealtimePreview.tsx`にはボタンが実装されていない
   - ボタンのスタイル（`buttonPrimary`, `buttonSecondary`）を確認できない

2. **STEP移動ができない**:
   - STEPタブは表示されているが、クリックできない（575-604行目）
   - `currentStepKey`はpropsとして受け取っているが、内部状態として管理していない
   - STEP移動の機能がない

### 確認済みの実装

- ✅ `PublicFormViewPage.tsx`には送信ボタン、次へボタン、戻るボタンが実装されている（1509-1850行目あたり）
- ✅ `FormRealtimePreview.tsx`にはSTEPタブが表示されている（575-604行目）
- ✅ `FormRealtimePreview.tsx`のpropsに`stepGroupStructure`がある

## タスクリスト

### タスク1: FormRealtimePreviewにcurrentStepKeyの内部状態を追加
- **ファイル**: `src/components/forms/FormRealtimePreview.tsx`
- **内容**: 
  - `currentStepKey`を内部状態として管理する`useState`を追加
  - propsの`stepGroupStructure`から最初のSTEPを初期値として設定
  - STEP式フォームの場合のみ状態を管理
- **実装**:
  ```typescript
  const [currentStepKey, setCurrentStepKey] = useState<string | null>(() => {
    if (stepGroupStructure?.is_step_form && stepGroupStructure.steps && stepGroupStructure.steps.length > 0) {
      const sortedSteps = [...stepGroupStructure.steps].sort((a, b) => a.sort_order - b.sort_order);
      return sortedSteps[0].step_key;
    }
    return null;
  });
  ```

### タスク2: STEPタブをクリック可能にする
- **ファイル**: `src/components/forms/FormRealtimePreview.tsx`
- **内容**: 
  - STEPタブを`button`要素に変更
  - クリック時に`setCurrentStepKey`を呼び出してSTEPを切り替え
  - 現在のSTEPをハイライト表示
- **修正箇所**: 575-604行目のSTEPタブ部分
- **実装**:
  ```typescript
  {stepList.map((step) => {
    const stepName = step.step_name_i18n[locale] || step.step_name_i18n["ja"] || step.step_name_i18n["en"] || step.step_key;
    const isActive = step.step_key === currentStepKey;
    return (
      <button
        key={step.step_key}
        type="button"
        onClick={() => setCurrentStepKey(step.step_key)}
        className={...}
        style={...}
      >
        {stepName}
      </button>
    );
  })}
  ```

### タスク3: フィールドをcurrentStepKeyでフィルタリング
- **ファイル**: `src/components/forms/FormRealtimePreview.tsx`
- **内容**: 
  - 表示するフィールドを`currentStepKey`でフィルタリング
  - STEP式フォームの場合、現在のSTEPのフィールドのみを表示
- **修正箇所**: フィールド表示部分（607-649行目あたり）
- **実装**:
  ```typescript
  const filteredFields = stepGroupStructure?.is_step_form && currentStepKey !== null
    ? fields.filter((field) => field.step_key === currentStepKey)
    : fields;
  ```

### タスク4: ボタンコンポーネントの追加（送信ボタン、次へボタン、戻るボタン）
- **ファイル**: `src/components/forms/FormRealtimePreview.tsx`
- **内容**: 
  - `PublicFormViewPage.tsx`と同様のボタンを追加
  - 送信ボタン（プライマリボタン）
  - 次へボタン（プライマリボタン、STEP式フォームの場合）
  - 戻るボタン（セカンダリボタン、STEP式フォームの場合）
  - ボタンは`data-custom-style`属性を設定してスタイル適用可能にする
- **配置場所**: メインカードの`CardBody`内、フィールド表示の後
- **実装**:
  ```typescript
  {/* ボタンエリア */}
  <div className="flex flex-wrap gap-2 justify-end pt-4 border-t border-white/10">
    {/* 戻るボタン（STEP式フォームで最初のSTEPでない場合） */}
    {stepGroupStructure?.is_step_form && stepList.length > 0 && currentStepIndex > 0 && (
      <button
        type="button"
        onClick={() => {
          const prevStep = stepList[currentStepIndex - 1];
          if (prevStep) setCurrentStepKey(prevStep.step_key);
        }}
        data-custom-style="buttonSecondary"
        className="..."
        style={...}
      >
        戻る
      </button>
    )}
    
    {/* 次へボタン（STEP式フォームで最後のSTEPでない場合）または送信ボタン */}
    {stepGroupStructure?.is_step_form && stepList.length > 0 ? (
      currentStepIndex < stepList.length - 1 ? (
        <button
          type="button"
          onClick={() => {
            const nextStep = stepList[currentStepIndex + 1];
            if (nextStep) setCurrentStepKey(nextStep.step_key);
          }}
          data-custom-style="buttonPrimary"
          className="..."
          style={...}
        >
          次へ
        </button>
      ) : (
        <button
          type="button"
          data-custom-style="buttonPrimary"
          className="..."
          style={...}
        >
          送信
        </button>
      )
    ) : (
      <button
        type="button"
        data-custom-style="buttonPrimary"
        className="..."
        style={...}
      >
        送信
      </button>
    )}
  </div>
  ```

### タスク5: ボタンのスタイル適用確認
- **ファイル**: `src/components/forms/FormRealtimePreview.tsx`
- **内容**: 
  - ボタンに`data-custom-style`属性を設定
  - `applyCustomStyleConfig`が正しくボタンにスタイルを適用することを確認
  - `customStyleConfig`が存在する場合は`themeTokens`のスタイルを適用しない
- **確認項目**:
  - `buttonPrimary`のスタイルが適用される
  - `buttonSecondary`のスタイルが適用される
  - `customStyleConfig`のスタイルが優先される

## 実装詳細

### STEP移動の実装

1. **初期値の設定**:
   - STEP式フォームの場合、最初のSTEP（`sort_order`が最小）を初期値とする
   - 単一式フォームの場合は`null`

2. **STEP切り替え**:
   - STEPタブをクリックすると、該当するSTEPに切り替わる
   - フィールドは現在のSTEPのもののみを表示

3. **ボタンの表示条件**:
   - 戻るボタン: STEP式フォームで最初のSTEPでない場合に表示
   - 次へボタン: STEP式フォームで最後のSTEPでない場合に表示
   - 送信ボタン: 最後のSTEP、または単一式フォームの場合に表示

### ボタンのスタイル適用

1. **data-custom-style属性**:
   - 送信ボタン・次へボタン: `data-custom-style="buttonPrimary"`
   - 戻るボタン: `data-custom-style="buttonSecondary"`

2. **themeTokensとの統合**:
   - `customStyleConfig`が存在する場合は`themeTokens`のスタイルを適用しない
   - `customStyleConfig`が存在しない場合は`themeTokens`のスタイルを適用

3. **スタイルの優先順位**:
   - `customStyleConfig`のスタイルが最優先
   - `themeTokens`のスタイルは`customStyleConfig`がない場合のみ適用

## 注意点

1. **プレビュー機能**:
   - ボタンは実際には送信しない（プレビュー用）
   - `onClick`ではSTEP移動のみを行う

2. **STEP移動**:
   - STEP移動時はバリデーションを行わない（プレビュー用）
   - フィールドの値は保持しない（プレビュー用）

3. **パフォーマンス**:
   - STEP切り替え時の再レンダリングを最小限にする
   - `useMemo`や`useCallback`を適切に使用

4. **後方互換性**:
   - 既存のprops（`stepGroupStructure`, `fields`など）は維持
   - 単一式フォームでも動作する

## 実装順序の推奨

1. **タスク1**: FormRealtimePreviewにcurrentStepKeyの内部状態を追加
2. **タスク2**: STEPタブをクリック可能にする
3. **タスク3**: フィールドをcurrentStepKeyでフィルタリング
4. **タスク4**: ボタンコンポーネントの追加
5. **タスク5**: ボタンのスタイル適用確認

## 進捗状況

- **全体進捗**: 5/5 タスク完了（100%）
- **最終更新**: 2026-01-23
- **完了タスク**: 
  - ✅ タスク1: FormRealtimePreviewにcurrentStepKeyの内部状態を追加（170-176行目で実装済み）
  - ✅ タスク2: STEPタブをクリック可能にする（376-396行目で実装済み）
  - ✅ タスク3: フィールドをcurrentStepKeyでフィルタリング（202-204行目で実装済み）
  - ✅ タスク4: ボタンコンポーネントの追加（449-531行目で実装済み）
  - ✅ タスク5: ボタンのスタイル適用確認（data-custom-style属性設定済み）
- **進行中タスク**: なし
- **未着手タスク**: なし

## 実装完了内容（2026-01-23）

### ✅ すべてのタスクが実装完了
- `FormRealtimePreview.tsx`にすべての機能が実装済み
- STEP移動機能、ボタン表示、スタイル適用が正常に動作
