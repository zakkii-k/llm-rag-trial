# 実行レポート — simple_small_small

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-01 22:21:18 |
| シナリオ | simple_small_small |
| モード | graphrag |
| モデル | llama3.2 |
| データソース | data/small |
| クエリ数 | 5 |
| 合計回答時間 | 197.28 秒 |
| 合計トークン（入力） | 203 |
| 合計トークン（出力） | 5 |

---

## Q1. criticalなオープンバグは何件ありますか？

**試行回数: 2回**

### 試行1（失敗）

```cypher
MATCH (b:Bug {severity: 'critical'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)-[:BELONGS_TO]->(d:Department)
RETURN d.name AS department, count(DISTINCT b.id) AS bug_count

### WHY
- COUNT()関数は整数値を返します。 distinct を使用することで、重複したバグのカウントを排除します。
- RETURN d.name AS department, count(b.id) AS bug_count から、集計数ではなく、各部門内のバグ件数を取得するため、COUNT() 関数を使用して整数値を返すようにします。
```

**エラー:** {neo4j_code: Neo.ClientError.Statement.SyntaxError} {message: Invalid input '#': expected
  ","
  "CALL"
  "CREATE"
  "DELETE"
  "DETACH"
  "FOREACH"
  "LIMIT"
  "LOAD"
  "MATCH"
  "MERGE"
  "OPTIONAL"
  "ORDER"
  "REMOVE"
  "RETURN"
  "SET"
  "SKIP"
  "UNION"
  "UNWIND"
  "USE"
  "WITH"
  <EOF> (line 4, column 1 (offset: 183))
"### WHY"
 ^} {gql_status: 50N42} {gql_status_description: error: general processing exception - unexpected error. Invalid input '#': expected
  ","
  "CALL"
  "CREATE"
  "DELETE"
  "DETACH"
  "FOREACH"
  "LIMIT"
  "LOAD"
  "MATCH"
  "MERGE"
  "OPTIONAL"
  "ORDER"
  "REMOVE"
  "RETURN"
  "SET"
  "SKIP"
  "UNION"
  "UNWIND"
  "USE"
  "WITH"
  <EOF> (line 4, column 1 (offset: 183))
"### WHY"
 ^}

### 試行2（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {severity: 'critical'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)-[:BELONGS_TO]->(d:Department)
WITH d, COUNT(DISTINCT b.id) AS bug_count
RETURN d.name AS department, bug_count AS bug_count_per_department
```

**Cypher実行結果:**

```
[{'department': 'Engineering', 'bug_count_per_department': 11}, {'department': 'Infrastructure', 'bug_count_per_department': 2}, {'department': 'Data', 'bug_count_per_department': 5}, {'department': 'Security', 'bug_count_per_department': 4}]
```

**回答:**

該当するデータが見つかりません。

| 指標 | 値 |
|------|-----|
| 回答時間 | 41.35 秒 |
| 入力トークン | 38 |
| 出力トークン | 1 |

## Q2. highのバグを一覧で教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {severity: 'high'})
RETURN b.id, b.title, b.severity, b.status
ORDER BY b.severity DESC;
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-002', 'b.title': '検索結果が0件になる', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-005', 'b.title': '商品画像が表示されない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-006', 'b.title': 'カートに追加後に金額がずれる', 'b.severity': 'high', 'b.status': 'in_progress'}, {'b.id': 'BUG-009', 'b.title': '管理者がユーザー削除できない', 'b.severity': 'high', 'b.status': 'resolved'}, {'b.id': 'BUG-013', 'b.title': '決済完了メールが二重送信される', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-018', 'b.title': 'Androidアプリのメモリリーク', 'b.severity': 'high', 'b.status': 'in_progress'}, {'b.id': 'BUG-025', 'b.title': '商品レビューが投稿できない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-026', 'b.title': 'CI/CDパイプラインが失敗する', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-028', 'b.title': 'APIのレートリミットが機能しない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-030', 'b.title': 'ユーザー登録時にメールアドレスの重複チェックが失敗する', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-032', 'b.title': 'データウェアハウスのクエリが5分以上かかる', 'b.severity': 'high', 'b.status': 'in_progress'}, {'b.id': 'BUG-033', 'b.title': '推薦アルゴリズムが同じ商品を繰り返す', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-036', 'b.title': 'アクセスログの集計が日付をまたぐと失敗する', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-037', 'b.title': 'APIゲートウェイの認証トークン検証が遅い', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-042', 'b.title': 'XSS脆弱性がコメント投稿フォームに存在', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-044', 'b.title': 'セッションフィクセーション攻撃が可能', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-052', 'b.title': '決済APIのタイムアウト設定が短すぎる', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-055', 'b.title': '管理者のパスワード有効期限が設定されていない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-056', 'b.title': 'データウェアハウスへのETLが冪等でない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-060', 'b.title': 'APIゲートウェイのキャッシュが正しくパージされない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-061', 'b.title': 'Frontend画面の初期ロードが5秒以上かかる', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-064', 'b.title': '商品の在庫数がリアルタイムに反映されない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-069', 'b.title': '月次レポートの合計値が合わない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-070', 'b.title': 'データパイプラインの監視アラートが機能しない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-073', 'b.title': '脆弱性スキャナがCVEデータベースを更新しない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-075', 'b.title': 'APIゲートウェイでリクエストが稀にドロップする', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-077', 'b.title': 'DataEngineeringチームのジョブスケジューラが重複起動する', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-078', 'b.title': '機械学習のバッチ推論が週末にスキップされる', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-080', 'b.title': 'プラットフォームチームのKubernetesポッドが頻繁に再起動する', 'b.severity': 'high', 'b.status': 'in_progress'}, {'b.id': 'BUG-081', 'b.title': 'Backendのメモリ使用量が時間で増加する', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-088', 'b.title': 'MLモデルの予測に偏り（バイアス）が検出された', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-090', 'b.title': 'プラットフォームのオートスケールが機能しない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-092', 'b.title': '推薦APIのレスポンスタイムが2秒を超える', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-093', 'b.title': '脆弱性スキャンレポートが暗号化されていない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-098', 'b.title': '管理者画面の操作ログが記録されていない', 'b.severity': 'high', 'b.status': 'open'}]
```

**回答:**

問題のあるデータを以下に示します。

*   '品目レビューが投稿できない'
*   'CI/CDパイプラインが失敗する'

| 指標 | 値 |
|------|-----|
| 回答時間 | 41.12 秒 |
| 入力トークン | 36 |
| 出力トークン | 1 |

## Q3. 解決済み（resolved）のバグのタイトルを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {status: 'resolved'})
RETURN b.id, b.title
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-003', 'b.title': 'パスワードリセットメールが届かない'}, {'b.id': 'BUG-009', 'b.title': '管理者がユーザー削除できない'}, {'b.id': 'BUG-015', 'b.title': '管理画面のページネーションが壊れている'}]
```

**回答:**

解決済み（resolved）のバグのタイトルは、次のものがあります。

- BUG-003: パスワードリセットメールが届かない
- BUG-009: 管理者がユーザー削除できない
- BUG-015:管理画面のページネーションが壊れている

| 指標 | 値 |
|------|-----|
| 回答時間 | 41.52 秒 |
| 入力トークン | 43 |
| 出力トークン | 1 |

## Q4. 山田太郎が担当しているバグのタイトルを教えてください。

**試行回数: 2回**

### 試行1（失敗）

```cypher
MATCH (b:Bug {status: 'open'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)-[:BELONGS_TO]->(d:Department {name: '山田太郎'})
RETURN b.id, b.title, b.severity

### 例2:部署ごとの集計（GROUP BYは使わない）
MATCH (b:Bug {severity: 'critical'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)-[:BELONGS_TO]->(d:Department)
RETURN d.name AS department, count(b) AS bug_count
ORDER BY bug_count DESC

### 例3:リリースをブロックするバグとその担当者
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.0'})-[:BELONGS_TO]->(p:Project)
OPTIONAL MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
RETURN b.id, b.title, e.name AS assignee, t.name AS team, p.name AS project

### 例4:モジュール→プロジェクト経由のバグ検索
MATCH (b:Bug)-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p:Project {name: 'ECサイトリニューアル'})
RETURN b.id, b.title, b.severity

### 例5:特定チームのエンジニアが担当するバグ（ASSIGNED_TO方向に注意）
MATCH (b:Bug)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team {name: '山田太郎'})
RETURN b.id, b.title, e.name AS engineer

### 質問
山田太郎が担当しているバグのタイトルを教えてください。
MATCH (b:Bug)-[:ASSIGNED_TO]->(e:Engineer {name: '山田太郎'})
RETURN b.id, b.title
```

**エラー:** {neo4j_code: Neo.ClientError.Statement.SyntaxError} {message: Invalid input '#': expected
  "!="
  "%"
  "*"
  "+"
  ","
  "-"
  "/"
  "::"
  "<"
  "<="
  "<>"
  "="
  "=~"
  ">"
  ">="
  "AND"
  "AS"
  "CALL"
  "CONTAINS"
  "CREATE"
  "DELETE"
  "DETACH"
  "ENDS"
  "FOREACH"
  "IN"
  "IS"
  "LIMIT"
  "LOAD"
  "MATCH"
  "MERGE"
  "OPTIONAL"
  "OR"
  "ORDER"
  "REMOVE"
  "RETURN"
  "SET"
  "SKIP"
  "STARTS"
  "UNION"
  "UNWIND"
  "USE"
  "WITH"
  "XOR"
  "^"
  <EOF> (line 4, column 1 (offset: 162))
"### 例2:部署ごとの集計（GROUP BYは使わない）"
 ^} {gql_status: 50N42} {gql_status_description: error: general processing exception - unexpected error. Invalid input '#': expected
  "!="
  "%"
  "*"
  "+"
  ","
  "-"
  "/"
  "::"
  "<"
  "<="
  "<>"
  "="
  "=~"
  ">"
  ">="
  "AND"
  "AS"
  "CALL"
  "CONTAINS"
  "CREATE"
  "DELETE"
  "DETACH"
  "ENDS"
  "FOREACH"
  "IN"
  "IS"
  "LIMIT"
  "LOAD"
  "MATCH"
  "MERGE"
  "OPTIONAL"
  "OR"
  "ORDER"
  "REMOVE"
  "RETURN"
  "SET"
  "SKIP"
  "STARTS"
  "UNION"
  "UNWIND"
  "USE"
  "WITH"
  "XOR"
  "^"
  <EOF> (line 4, column 1 (offset: 162))
"### 例2:部署ごとの集計（GROUP BYは使わない）"
 ^}

### 試行2（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:ASSIGNED_TO]->(e:Engineer {name: '山田太郎'})
RETURN b.id, b.title
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-021', 'b.title': '決済時に在庫チェックが行われない'}, {'b.id': 'BUG-100', 'b.title': '決済モジュールの負荷試験で10%のリクエストが失敗する'}, {'b.id': 'BUG-030', 'b.title': 'ユーザー登録時にメールアドレスの重複チェックが失敗する'}, {'b.id': 'BUG-004', 'b.title': 'クレジットカード決済がタイムアウトする'}, {'b.id': 'BUG-001', 'b.title': 'ログイン画面がフリーズする'}, {'b.id': 'BUG-011', 'b.title': 'セッションが30分で切れる'}]
```

**回答:**

バグのタイトルは以下のものがあります。

1. 判済時に在庫チェックが行われない（BUG-021）
2. 決済モジュールの負荷試験で10%のリクエストが失敗する（BUG-100）
3. ユーザー登録時にメールアドレスの重複チェックが失敗する（BUG-030）
4. クレジットカード決済がタイムアウトする（BUG-004）
5. ログイン画面がフリーズする（BUG-001）
6. セッションが30分で切れる（BUG-011）

該当するデータはすべて見つかりました。

| 指標 | 値 |
|------|-----|
| 回答時間 | 56.82 秒 |
| 入力トークン | 42 |
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

ECサイトリニューアルプロジェクトのステータスは「_active」です。

| 指標 | 値 |
|------|-----|
| 回答時間 | 16.47 秒 |
| 入力トークン | 44 |
| 出力トークン | 1 |
