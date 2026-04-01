# 実行レポート — simple_medium_qwen-large

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-01 23:58:14 |
| シナリオ | simple_medium_qwen-large |
| モード | graphrag |
| モデル | qwen2.5-coder:14b |
| データソース | data/medium |
| クエリ数 | 5 |
| 合計回答時間 | 379.23 秒 |
| 合計トークン（入力） | 214 |
| 合計トークン（出力） | 5 |

---

## Q1. criticalなオープンバグは何件ありますか？

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {severity: 'critical', status: 'open'})
RETURN count(b) AS critical_open_bug_count
```

**Cypher実行結果:**

```
[{'critical_open_bug_count': 22}]
```

**回答:**

22件のcriticalなオープンバグがあります。

| 指標 | 値 |
|------|-----|
| 回答時間 | 59.57 秒 |
| 入力トークン | 39 |
| 出力トークン | 1 |

## Q2. highのバグを一覧で教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {severity: 'high'})
RETURN b.id, b.title, b.severity, b.status
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-002', 'b.title': '検索結果が0件になる', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-005', 'b.title': '商品画像が表示されない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-006', 'b.title': 'カートに追加後に金額がずれる', 'b.severity': 'high', 'b.status': 'in_progress'}, {'b.id': 'BUG-009', 'b.title': '管理者がユーザー削除できない', 'b.severity': 'high', 'b.status': 'resolved'}, {'b.id': 'BUG-013', 'b.title': '決済完了メールが二重送信される', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-018', 'b.title': 'Androidアプリのメモリリーク', 'b.severity': 'high', 'b.status': 'in_progress'}, {'b.id': 'BUG-025', 'b.title': '商品レビューが投稿できない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-026', 'b.title': 'CI/CDパイプラインが失敗する', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-028', 'b.title': 'APIのレートリミットが機能しない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-030', 'b.title': 'ユーザー登録時にメールアドレスの重複チェックが失敗する', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-032', 'b.title': 'データウェアハウスのクエリが5分以上かかる', 'b.severity': 'high', 'b.status': 'in_progress'}, {'b.id': 'BUG-033', 'b.title': '推薦アルゴリズムが同じ商品を繰り返す', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-036', 'b.title': 'アクセスログの集計が日付をまたぐと失敗する', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-037', 'b.title': 'APIゲートウェイの認証トークン検証が遅い', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-042', 'b.title': 'XSS脆弱性がコメント投稿フォームに存在', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-044', 'b.title': 'セッションフィクセーション攻撃が可能', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-052', 'b.title': '決済APIのタイムアウト設定が短すぎる', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-055', 'b.title': '管理者のパスワード有効期限が設定されていない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-056', 'b.title': 'データウェアハウスへのETLが冪等でない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-060', 'b.title': 'APIゲートウェイのキャッシュが正しくパージされない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-061', 'b.title': 'Frontend画面の初期ロードが5秒以上かかる', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-064', 'b.title': '商品の在庫数がリアルタイムに反映されない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-069', 'b.title': '月次レポートの合計値が合わない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-070', 'b.title': 'データパイプラインの監視アラートが機能しない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-073', 'b.title': '脆弱性スキャナがCVEデータベースを更新しない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-075', 'b.title': 'APIゲートウェイでリクエストが稀にドロップする', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-077', 'b.title': 'DataEngineeringチームのジョブスケジューラが重複起動する', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-078', 'b.title': '機械学習のバッチ推論が週末にスキップされる', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-080', 'b.title': 'プラットフォームチームのKubernetesポッドが頻繁に再起動する', 'b.severity': 'high', 'b.status': 'in_progress'}, {'b.id': 'BUG-081', 'b.title': 'Backendのメモリ使用量が時間で増加する', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-088', 'b.title': 'MLモデルの予測に偏り（バイアス）が検出された', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-090', 'b.title': 'プラットフォームのオートスケールが機能しない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-092', 'b.title': '推薦APIのレスポンスタイムが2秒を超える', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-093', 'b.title': '脆弱性スキャンレポートが暗号化されていない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-098', 'b.title': '管理者画面の操作ログが記録されていない', 'b.severity': 'high', 'b.status': 'open'}]
```

**回答:**

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 128.30 秒 |
| 入力トークン | 41 |
| 出力トークン | 1 |

## Q3. 解決済み（resolved）のバグのタイトルを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {status: 'resolved'})
RETURN b.title
```

**Cypher実行結果:**

```
[{'b.title': 'パスワードリセットメールが届かない'}, {'b.title': '管理者がユーザー削除できない'}, {'b.title': '管理画面のページネーションが壊れている'}]
```

**回答:**

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 61.50 秒 |
| 入力トークン | 45 |
| 出力トークン | 1 |

## Q4. 山田太郎が担当しているバグのタイトルを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:ASSIGNED_TO]->(e:Engineer {name: '山田太郎'})
RETURN b.id, b.title, b.severity
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-021', 'b.title': '決済時に在庫チェックが行われない', 'b.severity': 'critical'}, {'b.id': 'BUG-100', 'b.title': '決済モジュールの負荷試験で10%のリクエストが失敗する', 'b.severity': 'critical'}, {'b.id': 'BUG-030', 'b.title': 'ユーザー登録時にメールアドレスの重複チェックが失敗する', 'b.severity': 'high'}, {'b.id': 'BUG-004', 'b.title': 'クレジットカード決済がタイムアウトする', 'b.severity': 'critical'}, {'b.id': 'BUG-001', 'b.title': 'ログイン画面がフリーズする', 'b.severity': 'critical'}, {'b.id': 'BUG-011', 'b.title': 'セッションが30分で切れる', 'b.severity': 'low'}]
```

**回答:**

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 70.15 秒 |
| 入力トークン | 44 |
| 出力トークン | 1 |

## Q5. ECサイトリニューアルプロジェクトのステータスを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (p:Project {name: 'ECサイトリニューアル'})
RETURN p.status
```

**Cypher実行結果:**

```
[{'p.status': 'active'}]
```

**回答:**

ECサイトリニューアルプロジェクトのステータスは「active」です。

| 指標 | 値 |
|------|-----|
| 回答時間 | 59.71 秒 |
| 入力トークン | 45 |
| 出力トークン | 1 |
