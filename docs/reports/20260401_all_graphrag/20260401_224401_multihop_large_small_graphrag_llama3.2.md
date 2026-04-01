# 実行レポート — multihop_large_small

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-01 22:44:01 |
| シナリオ | multihop_large_small |
| モード | graphrag |
| モデル | llama3.2 |
| データソース | data/large |
| クエリ数 | 5 |
| 合計回答時間 | 152.81 秒 |
| 合計トークン（入力） | 273 |
| 合計トークン（出力） | 5 |

---

## Q1. Engineering部署のエンジニアが担当しているcriticalなオープンバグを全て教えてください。

**試行回数: 3回**

### 試行1（失敗）

```cypher
MATCH (b:Bug {severity: 'critical'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
RETURN b.id, b.title, e.name AS assignee, t.name AS team

### 2. Departmentの名前とCriticalバグ件数を集計する
MATCH (b:Bug {severity: 'critical'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)-[:BELONGS_TO]->(d:Department)
RETURN d.name AS department, count(b) AS bug_count
ORDER BY bug_count DESC
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
  <EOF> (line 4, column 1 (offset: 147))
"### 2. Departmentの名前とCriticalバグ件数を集計する"
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
  <EOF> (line 4, column 1 (offset: 147))
"### 2. Departmentの名前とCriticalバグ件数を集計する"
 ^}

### 試行2（失敗）

```cypher
MATCH (b:Bug {severity: 'critical'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
RETURN b.id, b.title, e.name AS assignee, t.name AS team

UNWIND [d IN COLLECT(DISTINCT (b)-[:BELONGS_TO]->(dep:Department))] AS dep
WITH d.dep AS department
RETURN department, count(b) AS bug_count
ORDER BY bug_count DESC;
```

**エラー:** {neo4j_code: Neo.ClientError.Statement.SyntaxError} {message: PatternExpressions are not allowed to introduce new variables: 'b'. (line 4, column 32 (offset: 178))
"UNWIND [d IN COLLECT(DISTINCT (b)-[:BELONGS_TO]->(dep:Department))] AS dep"
                                ^} {gql_status: 50N42} {gql_status_description: error: general processing exception - unexpected error. PatternExpressions are not allowed to introduce new variables: 'b'. (line 4, column 32 (offset: 178))
"UNWIND [d IN COLLECT(DISTINCT (b)-[:BELONGS_TO]->(dep:Department))] AS dep"
                                ^}

### 試行3（成功）

**生成Cypherクエリ:**

```cypher
MATCH (e:Engineer {name: 'Engineering Department'})-[:ASSIGNED_TO]->(b:Bug)-[:BLOCKS]->(:Release)
WITH b, COLLECT(DISTINCT e) AS engineers
RETURN b.id, b.title, engineers[0].name AS assignee
```

**Cypher実行結果:**

```
[]
```

**回答:**

該当するデータが見つかりません。

| 指標 | 値 |
|------|-----|
| 回答時間 | 48.94 秒 |
| 入力トークン | 48 |
| 出力トークン | 1 |

## Q2. v1.1リリースをブロックしているバグが属するモジュールのプロジェクト名を教えてください。

**試行回数: 2回**

### 試行1（失敗）

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.1'})-[:BELONGS_TO]->(p:Project)
RETURN p.name AS project_name, TYPE(p) AS node_type
```

**エラー:** {neo4j_code: Neo.ClientError.Statement.SyntaxError} {message: Type mismatch: expected Relationship but was Node (line 2, column 37 (offset: 118))
"RETURN p.name AS project_name, TYPE(p) AS node_type"
                                     ^} {gql_status: 50N42} {gql_status_description: error: general processing exception - unexpected error. Type mismatch: expected Relationship but was Node (line 2, column 37 (offset: 118))
"RETURN p.name AS project_name, TYPE(p) AS node_type"
                                     ^}

### 試行2（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.1'})-[:BELONGS_TO]->(p:Project)
RETURN p.name AS project_name, COUNT(DISTINCT r) AS cnt
```

**Cypher実行結果:**

```
[{'project_name': 'ECサイトリニューアル', 'cnt': 1}]
```

**回答:**

v1.1 リリースをブロックしているバグが属するモジュールのプロジェクト名は、"ECサイトリニューアル" です。

| 指標 | 値 |
|------|-----|
| 回答時間 | 42.23 秒 |
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
| 回答時間 | 16.75 秒 |
| 入力トークン | 59 |
| 出力トークン | 1 |

## Q4. criticalバグを担当しているエンジニアが所属する部署ごとのバグ件数を教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {severity: 'critical'})
OPTIONAL MATCH (e:Engineer)-[:ASSIGNED_TO]->(b)
OPTIONAL MATCH (t:Team)-[:MEMBER_OF]->(e)
OPTIONAL MATCH (d:Department)-[:BELONGS_TO]->(t)
RETURN d.name AS department, count(DISTINCT e) AS engineer_count
ORDER BY engineer_count DESC
```

**Cypher実行結果:**

```
[{'department': None, 'engineer_count': 0}]
```

**回答:**

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 26.84 秒 |
| 入力トークン | 50 |
| 出力トークン | 1 |

## Q5. モバイルアプリ開発プロジェクトのv1.0リリースをブロックしているバグの担当エンジニアが所属するチームを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.0'})-[:BELONGS_TO]->(p:Project)
OPTIONAL MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
RETURN t.name AS team
```

**Cypher実行結果:**

```
[{'team': 'Mobile'}, {'team': 'Mobile'}, {'team': 'DevOps'}, {'team': 'Mobile'}, {'team': 'Mobile'}, {'team': 'Mobile'}, {'team': 'Mobile'}, {'team': 'Mobile'}, {'team': 'Mobile'}, {'team': 'DataEngineering'}, {'team': 'Platform'}, {'team': 'DataEngineering'}, {'team': 'DataEngineering'}, {'team': 'DataEngineering'}, {'team': 'DataEngineering'}, {'team': 'Platform'}, {'team': 'DataEngineering'}, {'team': 'DataEngineering'}, {'team': 'MachineLearning'}, {'team': 'MachineLearning'}, {'team': 'MachineLearning'}, {'team': 'MachineLearning'}, {'team': 'MachineLearning'}, {'team': 'MachineLearning'}, {'team': 'Security'}, {'team': 'Security'}, {'team': 'Security'}, {'team': 'API'}, {'team': 'Security'}, {'team': 'Security'}, {'team': 'QA'}, {'team': 'Security'}, {'team': 'Security'}, {'team': 'Security'}]
```

**回答:**

バグの担当エンジニアが所属するチームは、Mobile のみです。

| 指標 | 値 |
|------|-----|
| 回答時間 | 18.05 秒 |
| 入力トークン | 62 |
| 出力トークン | 1 |
