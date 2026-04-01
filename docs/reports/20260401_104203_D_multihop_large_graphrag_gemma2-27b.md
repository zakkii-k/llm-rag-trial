# 実行レポート — D_multihop_large

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-01 10:42:03 |
| シナリオ | D_multihop_large |
| モード | graphrag |
| モデル | gemma2:27b |
| データソース | data/large |
| クエリ数 | 5 |
| 合計回答時間 | 406.80 秒 |
| 合計トークン（入力） | 124 |
| 合計トークン（出力） | 4 |

---

## Q1. Engineering部署のエンジニアが担当しているcriticalなオープンバグを全て教えてください。

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {severity: 'critical', status: 'open'})<-[:ASSIGNED_TO]-(e:Engineer)-[:MEMBER_OF]->(t:Team)-[:BELONGS_TO]->(d:Department {name: 'Engineering'})
RETURN b.id, b.title
```

**Cypher実行結果:**

```
[]
```

**回答:**

I don't know the answer.

| 指標 | 値 |
|------|-----|
| 回答時間 | 175.91 秒 |
| 入力トークン | 27 |
| 出力トークン | 1 |

## Q2. v1.1リリースをブロックしているバグが属するモジュールのプロジェクト名を教えてください。

**生成Cypherクエリ:**

```cypher
MATCH (r:Release {version:'v1.1'})<-[:BLOCKS]-(b:Bug)-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p:Project)
RETURN p.name
```

**Cypher実行結果:**

```
[{'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}]
```

**回答:**

ECサイトリニューアル

| 指標 | 値 |
|------|-----|
| 回答時間 | 71.04 秒 |
| 入力トークン | 30 |
| 出力トークン | 1 |

## Q3. ECサイトリニューアルプロジェクトのモジュールで発見されたバグのうち、Backendチームが担当しているものを教えてください。

**生成Cypherクエリ:**

```cypher
MATCH (p:Project {name: "ECサイトリニューアル"})<-[:PART_OF]-(m:Module)<-[:FOUND_IN]-(b:Bug)
WHERE b.status = 'open'
WITH b, m
MATCH (t:Team {name: "Backend"})<-[:MEMBER_OF]-(e:Engineer)-[:ASSIGNED_TO]->(b)
RETURN b.title, e.name
```

**Cypher実行結果:**

```
[]
```

**回答:**

申し訳ありませんが、その情報はありません。

| 指標 | 値 |
|------|-----|
| 回答時間 | 81.65 秒 |
| 入力トークン | 32 |
| 出力トークン | 1 |

## Q4. criticalバグを担当しているエンジニアが所属する部署ごとのバグ件数を教えてください。

**エラー:** {neo4j_code: Neo.ClientError.Statement.SyntaxError} {message: Invalid input 'GROUP': expected
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
  <EOF> (line 3, column 1 (offset: 155))
"GROUP BY d.name"
 ^} {gql_status: 50N42} {gql_status_description: error: general processing exception - unexpected error. Invalid input 'GROUP': expected
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
  <EOF> (line 3, column 1 (offset: 155))
"GROUP BY d.name"
 ^}

## Q5. モバイルアプリ開発プロジェクトのv1.0リリースをブロックしているバグの担当エンジニアが所属するチームを教えてください。

**生成Cypherクエリ:**

```cypher
MATCH (p:Project {name: "モバイルアプリ開発"})<-[:BELONGS_TO]-(r:Release {version: "v1.0"})<-[:BLOCKS]-(b:Bug)<-[:ASSIGNED_TO]-(e:Engineer)-[:MEMBER_OF]->(t:Team)
RETURN t.name
```

**Cypher実行結果:**

```
[]
```

**回答:**

この質問に対する情報がないため、答えられません。

| 指標 | 値 |
|------|-----|
| 回答時間 | 78.20 秒 |
| 入力トークン | 35 |
| 出力トークン | 1 |
