# 実行レポート — multihop_small_small

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-01 22:28:41 |
| シナリオ | multihop_small_small |
| モード | graphrag |
| モデル | llama3.2 |
| データソース | data/small |
| クエリ数 | 5 |
| 合計回答時間 | 127.92 秒 |
| 合計トークン（入力） | 273 |
| 合計トークン（出力） | 5 |

---

## Q1. Engineering部署のエンジニアが担当しているcriticalなオープンバグを全て教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {severity: 'critical'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)-[:BELONGS_TO]->(d:Department {name: 'Engineering'})
RETURN b.id, b.title, e.name AS assignee
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-094', 'b.title': 'APIゲートウェイのSSL証明書の有効期限が切れそう', 'assignee': '藤田恵美'}, {'b.id': 'BUG-043', 'b.title': 'APIキーがログに平文で出力される', 'assignee': '藤田恵美'}, {'b.id': 'BUG-038', 'b.title': '通知サービスでiOS/Android両方に二重送信される', 'assignee': '山本香織'}, {'b.id': 'BUG-083', 'b.title': 'MobileチームのCI環境でコードサインのキーがExpireしている', 'assignee': '坂本竜一'}, {'b.id': 'BUG-096', 'b.title': 'Androidのアプリ内購入フローが失敗する', 'assignee': '加藤誠'}, {'b.id': 'BUG-007', 'b.title': 'iOSアプリが起動時にクラッシュする', 'assignee': '佐藤美咲'}, {'b.id': 'BUG-029', 'b.title': 'データベース接続プールが枯渇する', 'assignee': '田中一郎'}, {'b.id': 'BUG-021', 'b.title': '決済時に在庫チェックが行われない', 'assignee': '山田太郎'}, {'b.id': 'BUG-100', 'b.title': '決済モジュールの負荷試験で10%のリクエストが失敗する', 'assignee': '山田太郎'}, {'b.id': 'BUG-004', 'b.title': 'クレジットカード決済がタイムアウトする', 'assignee': '山田太郎'}, {'b.id': 'BUG-001', 'b.title': 'ログイン画面がフリーズする', 'assignee': '山田太郎'}]
```

**回答:**

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 18.76 秒 |
| 入力トークン | 48 |
| 出力トークン | 1 |

## Q2. v1.1リリースをブロックしているバグが属するモジュールのプロジェクト名を教えてください。

**試行回数: 2回**

### 試行1（失敗）

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.1'})-[:BELONGS_TO]->(p:Project)
RETURN p.name AS project_name

このCypherクエリは、バグが`v1.1`リリースをブロックしている場合、そのバグが属するモジュールのプロジェクト名を返します。
```

**エラー:** {neo4j_code: Neo.ClientError.Statement.SyntaxError} {message: Invalid input 'このCypherクエリは': expected
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
  <EOF> (line 4, column 1 (offset: 113))
"このCypherクエリは、バグが`v1.1`リリースをブロックしている場合、そのバグが属するモジュールのプロジェクト名を返します。"
 ^} {gql_status: 50N42} {gql_status_description: error: general processing exception - unexpected error. Invalid input 'このCypherクエリは': expected
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
  <EOF> (line 4, column 1 (offset: 113))
"このCypherクエリは、バグが`v1.1`リリースをブロックしている場合、そのバグが属するモジュールのプロジェクト名を返します。"
 ^}

### 試行2（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.1'})-[:BELONGS_TO]->(p:Project)
WITH b, p
RETURN p.name AS project_name, count(DISTINCT b) AS bug_count
```

**Cypher実行結果:**

```
[{'project_name': 'ECサイトリニューアル', 'bug_count': 24}]
```

**回答:**

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 40.64 秒 |
| 入力トークン | 54 |
| 出力トークン | 1 |

## Q3. ECサイトリニューアルプロジェクトのモジュールで発見されたバグのうち、Backendチームが担当しているものを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p:Project {name: 'ECサイトリニューアル'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Backend'})
RETURN b.id, b.title, b.severity
```

**Cypher実行結果:**

```
[]
```

**回答:**

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 17.85 秒 |
| 入力トークン | 59 |
| 出力トークン | 1 |

## Q4. criticalバグを担当しているエンジニアが所属する部署ごとのバグ件数を教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {severity: 'critical'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
RETURN t.name AS department, count(DISTINCT e) AS engineer_count, count(b) AS bug_count
ORDER BY bug_count DESC
```

**Cypher実行結果:**

```
[{'department': 'Backend', 'engineer_count': 2, 'bug_count': 5}, {'department': 'Mobile', 'engineer_count': 4, 'bug_count': 4}, {'department': 'Security', 'engineer_count': 2, 'bug_count': 4}, {'department': 'DataEngineering', 'engineer_count': 2, 'bug_count': 3}, {'department': 'DevOps', 'engineer_count': 1, 'bug_count': 2}, {'department': 'MachineLearning', 'engineer_count': 2, 'bug_count': 2}, {'department': 'API', 'engineer_count': 1, 'bug_count': 2}]
```

**回答:**

各部署のcriticalバグを担当しているエンジニアの数は、次の通りです。

- 背-end: 5 人
- モバイル: 4 人
- セキュリティ: 4 人
- データエンジニアリング: 3 人
- デヴォップス: 2 人
- マシンホット: 2 人
- API: 2 人

| 指標 | 値 |
|------|-----|
| 回答時間 | 29.22 秒 |
| 入力トークン | 50 |
| 出力トークン | 1 |

## Q5. モバイルアプリ開発プロジェクトのv1.0リリースをブロックしているバグの担当エンジニアが所属するチームを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.0'})-[:BELONGS_TO]->(p:Project)
OPTIONAL MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
RETURN t.name AS team, e.name AS assignee
```

**Cypher実行結果:**

```
[{'team': 'Mobile', 'assignee': '加藤誠'}, {'team': 'Mobile', 'assignee': '加藤誠'}, {'team': 'DevOps', 'assignee': '中村大輔'}, {'team': 'Mobile', 'assignee': '坂本竜一'}, {'team': 'Mobile', 'assignee': '佐藤美咲'}, {'team': 'Mobile', 'assignee': '坂本竜一'}, {'team': 'Mobile', 'assignee': '加藤誠'}, {'team': 'Mobile', 'assignee': '山本香織'}, {'team': 'Mobile', 'assignee': '佐藤美咲'}, {'team': 'DataEngineering', 'assignee': '井上真由'}, {'team': 'Platform', 'assignee': '藤原大樹'}, {'team': 'DataEngineering', 'assignee': '石川莉奈'}, {'team': 'DataEngineering', 'assignee': '井上真由'}, {'team': 'DataEngineering', 'assignee': '石川莉奈'}, {'team': 'DataEngineering', 'assignee': '石川莉奈'}, {'team': 'Platform', 'assignee': '岡田和也'}, {'team': 'DataEngineering', 'assignee': '石川莉奈'}, {'team': 'DataEngineering', 'assignee': '井上真由'}, {'team': 'MachineLearning', 'assignee': '上田健'}, {'team': 'MachineLearning', 'assignee': '木村雄介'}, {'team': 'MachineLearning', 'assignee': '木村雄介'}, {'team': 'MachineLearning', 'assignee': '上田健'}, {'team': 'MachineLearning', 'assignee': '上田健'}, {'team': 'MachineLearning', 'assignee': '木村雄介'}, {'team': 'Security', 'assignee': '松本剛'}, {'team': 'Security', 'assignee': '松本剛'}, {'team': 'Security', 'assignee': '橋本慎太郎'}, {'team': 'API', 'assignee': '小林直子'}, {'team': 'Security', 'assignee': '橋本慎太郎'}, {'team': 'Security', 'assignee': '橋本慎太郎'}, {'team': 'QA', 'assignee': '近藤真一'}, {'team': 'Security', 'assignee': '松本剛'}, {'team': 'Security', 'assignee': '橋本慎太郎'}, {'team': 'Security', 'assignee': '橋本慎太郎'}]
```

**回答:**

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 21.45 秒 |
| 入力トークン | 62 |
| 出力トークン | 1 |
