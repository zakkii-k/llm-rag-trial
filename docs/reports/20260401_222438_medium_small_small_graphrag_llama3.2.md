# 実行レポート — medium_small_small

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-01 22:24:38 |
| シナリオ | medium_small_small |
| モード | graphrag |
| モデル | llama3.2 |
| データソース | data/small |
| クエリ数 | 5 |
| 合計回答時間 | 239.67 秒 |
| 合計トークン（入力） | 222 |
| 合計トークン（出力） | 5 |

---

## Q1. Backendチームのエンジニアが担当しているオープンなバグを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {status: 'open'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)-[:BELONGS_TO]->(d:Department {name: 'Backend'})
RETURN b.id, b.title, b.severity, e.name
```

**Cypher実行結果:**

```
[]
```

**回答:**

該当するデータが見つかりません。

| 指標 | 値 |
|------|-----|
| 回答時間 | 15.19 秒 |
| 入力トークン | 45 |
| 出力トークン | 1 |

## Q2. 認証モジュールで発見されたバグの担当者名を教えてください。

**試行回数: 2回**

### 試行1（失敗）

```cypher
MATCH (b:Bug {status: 'open'})-[:FOUND_IN]->(m:Module)-[:PART_OF]->(:Project)-[:BELONGS_TO]->(:Department)
OPTIONAL MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
RETURN b.id, b.title, e.name AS assignee, t.name AS team

### 例2: 認証モジュールで発見されたバグの担当者（GROUP BYは使わない）

Cypher:
MATCH (b:Bug {status: 'open'})-[:FOUND_IN]->(m:Module)-[:PART_OF]->(:Project)-[:BELONGS_TO]->(:Department)
RETURN m.name AS module, count(DISTINCT b) AS bug_count
ORDER BY bug_count DESC

### 例3: 認証モジュールで発見されたバグの担当者（ASSIGNED_TO方向に注意）

Cypher:
MATCH (b:Bug {status: 'open'})-[:FOUND_IN]->(m:Module)-[:PART_OF]->(:Project)
OPTIONAL MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
RETURN b.id, b.title, e.name AS assignee, t.name AS team

### 例4: 認証モジュールで発見されたバグの担当者（モジュール→プロジェクト経由）

Cypher:
MATCH (b:Bug {status: 'open'})-[:FOUND_IN]->(m:Module)-[:PART_OF]->(:Project)
RETURN m.name AS module, b.id, b.title, b.severity
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
  <EOF> (line 5, column 1 (offset: 236))
"### 例2: 認証モジュールで発見されたバグの担当者（GROUP BYは使わない）"
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
  <EOF> (line 5, column 1 (offset: 236))
"### 例2: 認証モジュールで発見されたバグの担当者（GROUP BYは使わない）"
 ^}

### 試行2（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {status: 'open'})-[:FOUND_IN]->(m:Module)-[:PART_OF]->(:Project)-[:BELONGS_TO]->(:Department)
OPTIONAL MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
RETURN b.id, b.title, e.name AS assignee, t.name AS team
```

**Cypher実行結果:**

```
[]
```

**回答:**

該当するデータが見つかりません。

| 指標 | 値 |
|------|-----|
| 回答時間 | 48.13 秒 |
| 入力トークン | 45 |
| 出力トークン | 1 |

## Q3. 決済モジュールに関連するcriticalバグは誰が担当していますか？

**試行回数: 3回**

### 試行1（失敗）

```cypher
MATCH (b:Bug {severity: 'critical'})-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p:Project {name: '決済モジュール'})
 OPTIONAL MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)
 RETURN e.name AS assignee

### 説明：
決済モジュールに関連するcriticalバグは、特定のモジュールが属しているプロジェクト内で発見されたバグのみを検索します。assigneeの値は、バグをアサインしたエンジニアの名前になります。assigneeが存在しない場合は、NULLになります。
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
  <EOF> (line 5, column 1 (offset: 180))
"### 説明："
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
  <EOF> (line 5, column 1 (offset: 180))
"### 説明："
 ^}

### 試行2（失敗）

```cypher
MATCH (b:Bug {severity: 'critical'})-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p:Project {name: '決済モジュール'})
WITH b, COLLECT(DISTINCT e.name AS assignee) AS assigns
RETURN assigns[0] AS assignee
```

**エラー:** {neo4j_code: Neo.ClientError.Statement.SyntaxError} {message: Invalid input 'AS': expected
  "!="
  "%"
  ")"
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
  "CONTAINS"
  "ENDS"
  "IN"
  "IS"
  "OR"
  "STARTS"
  "XOR"
  "^" (line 2, column 33 (offset: 135))
"WITH b, COLLECT(DISTINCT e.name AS assignee) AS assigns"
                                 ^} {gql_status: 50N42} {gql_status_description: error: general processing exception - unexpected error. Invalid input 'AS': expected
  "!="
  "%"
  ")"
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
  "CONTAINS"
  "ENDS"
  "IN"
  "IS"
  "OR"
  "STARTS"
  "XOR"
  "^" (line 2, column 33 (offset: 135))
"WITH b, COLLECT(DISTINCT e.name AS assignee) AS assigns"
                                 ^}

### 試行3（失敗）

```cypher
MATCH (b:Bug {severity: 'critical'})-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p:Project {name: '決済モジュール'})
WITH b, COLLECT(DISTINCT e.name) AS assigns
RETURN assigns[0] AS assignee
```

**エラー:** {neo4j_code: Neo.ClientError.Statement.SyntaxError} {message: Variable `e` not defined (line 2, column 26 (offset: 128))
"WITH b, COLLECT(DISTINCT e.name) AS assigns"
                          ^} {gql_status: 50N42} {gql_status_description: error: general processing exception - unexpected error. Variable `e` not defined (line 2, column 26 (offset: 128))
"WITH b, COLLECT(DISTINCT e.name) AS assigns"
                          ^}

**回答:**

Cypherクエリの生成・実行に失敗しました。

| 指標 | 値 |
|------|-----|
| 回答時間 | 50.65 秒 |
| 入力トークン | 43 |
| 出力トークン | 1 |

## Q4. v1.1リリースをブロックしているバグの一覧と担当者を教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.1'})-[:BELONGS_TO]->(p:Project)
OPTIONAL MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
RETURN b.id, b.title, e.name AS assignee, t.name AS team, p.name AS project
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-041', 'b.title': 'SQLインジェクションの脆弱性が検出された', 'assignee': '松本剛', 'team': 'Security', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-030', 'b.title': 'ユーザー登録時にメールアドレスの重複チェックが失敗する', 'assignee': '山田太郎', 'team': 'Backend', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-094', 'b.title': 'APIゲートウェイのSSL証明書の有効期限が切れそう', 'assignee': '藤田恵美', 'team': 'API', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-002', 'b.title': '検索結果が0件になる', 'assignee': '鈴木花子', 'team': 'Frontend', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-005', 'b.title': '商品画像が表示されない', 'assignee': '渡辺恵', 'team': 'Frontend', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-004', 'b.title': 'クレジットカード決済がタイムアウトする', 'assignee': '山田太郎', 'team': 'Backend', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-043', 'b.title': 'APIキーがログに平文で出力される', 'assignee': '藤田恵美', 'team': 'API', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-052', 'b.title': '決済APIのタイムアウト設定が短すぎる', 'assignee': '村田さくら', 'team': 'Backend', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-001', 'b.title': 'ログイン画面がフリーズする', 'assignee': '山田太郎', 'team': 'Backend', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-013', 'b.title': '決済完了メールが二重送信される', 'assignee': '田中一郎', 'team': 'Backend', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-081', 'b.title': 'Backendのメモリ使用量が時間で増加する', 'assignee': '林美里', 'team': 'Backend', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-026', 'b.title': 'CI/CDパイプラインが失敗する', 'assignee': '中村大輔', 'team': 'DevOps', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-017', 'b.title': 'ログアウト後もセッションが残る', 'assignee': '中村大輔', 'team': 'DevOps', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-060', 'b.title': 'APIゲートウェイのキャッシュが正しくパージされない', 'assignee': '前田麗', 'team': 'API', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-075', 'b.title': 'APIゲートウェイでリクエストが稀にドロップする', 'assignee': '藤田恵美', 'team': 'API', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-100', 'b.title': '決済モジュールの負荷試験で10%のリクエストが失敗する', 'assignee': '山田太郎', 'team': 'Backend', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-006', 'b.title': 'カートに追加後に金額がずれる', 'assignee': '田中一郎', 'team': 'Backend', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-064', 'b.title': '商品の在庫数がリアルタイムに反映されない', 'assignee': '田中一郎', 'team': 'Backend', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-021', 'b.title': '決済時に在庫チェックが行われない', 'assignee': '山田太郎', 'team': 'Backend', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-061', 'b.title': 'Frontend画面の初期ロードが5秒以上かかる', 'assignee': '長谷川翼', 'team': 'Frontend', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-025', 'b.title': '商品レビューが投稿できない', 'assignee': '渡辺恵', 'team': 'Frontend', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-029', 'b.title': 'データベース接続プールが枯渇する', 'assignee': '田中一郎', 'team': 'Backend', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-037', 'b.title': 'APIゲートウェイの認証トークン検証が遅い', 'assignee': '藤田恵美', 'team': 'API', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-042', 'b.title': 'XSS脆弱性がコメント投稿フォームに存在', 'assignee': '橋本慎太郎', 'team': 'Security', 'project': 'ECサイトリニューアル'}]
```

**回答:**

v1.1リリースをブロックしているバグの一覧と担当者は以下の通りです。

1. BUG-041: SQLインジェクションの脆弱性が検出された -(assignee: 松本剛)
2. BUG-030: ユーザー登録時にメールアドレスの重複チェックが失敗する - (assignee: 山田太郎)
3. BUG-094: APIゲートウェイのSSL証明書の有効期限が切れそう - (assignee: 藤田恵美)
4. BUG-002: 検索結果が0件になる - (assignee: 鈴木花子)
5. BUG-005: 商品画像が表示されない - (assignee: 渡辺恵)
6. BUG-004: クレジットカード決済がタイムアウトする - (assignee: 山田太郎)
7. BUG-043: APIキーがログに平文で出力される - (assignee: 藤田恵美)
8. BUG-052: 決済APIのタイムアウト設定が短すぎる - (assignee: 村田さくら)
9. BUG-001: ログイン画面がフリーズする - (assignee: 山田太郎)
10. BUG-013: 決済完了メールが二重送信される - (assignee: 田中一郎)
11. BUG-081: Behindendのメモリ使用量が時間で増加する - (assignee: 林美里)
12. BUG-026: CI/CDパイプラインが失敗する - (assignee: 中村大輔)
13. BUG-017: ログアウト後もセッションが残る - (assignee: 中村大輔)
14. BUG-060: APIゲートウェイのキャッシュが正しくパージされない - (assignee: 前田麗)
15. BUG-075: APIゲートウェイでリクエストが稀にドロップする - (assignee: 藤田恵美)
16. BUG-100: 決済モジュールの負荷試験で10%のリクエストが失敗する - (assignee: 山田太郎)
17. BUG-006: カートに追加後に金額がずれる - (assignee: 田中一郎)
18. BUG-064: 商品の在庫数がリアルタイムに反映されない - (assignee: 田中一郎)
19. BUG-021: 決済時に在庫チェックが行われない - (assignee: 山田太郎)
20. BUG-061: Frontend画面の初期ロードが5秒以上かかる - (assignee: 長谷川翼)
21. BUG-025: 商品レビューが投稿できない - (assignee: 渡辺恵)
22. BUG-029: データベース接続プールが枯渇する - (assignee: 田中一郎)
23. BUG-037: APIゲートウェイの認証トークン検証が遅い - (assignee: 藤田恵美)
24. BUG-042: XSS脆弱性がコメント投稿フォームに存在 - (assignee: 橋本慎太郎)

特定のバグについては、各項の(assignee:)を参照してください。

| 指標 | 値 |
|------|-----|
| 回答時間 | 65.51 秒 |
| 入力トークン | 48 |
| 出力トークン | 1 |

## Q5. FrontendチームとBackendチームのバグ件数を比較してください。

**試行回数: 3回**

### 試行1（失敗）

```cypher
MATCH (b:Bug {status: 'open'})
WITH b, COLLECT(DISTINCT t.name) AS team_names
UNWIND team_names AS team_name
RETURN team_name, COUNT(b) AS bug_count
ORDER BY bug_count DESC;
```

**エラー:** {neo4j_code: Neo.ClientError.Statement.SyntaxError} {message: Variable `t` not defined (line 2, column 26 (offset: 56))
"WITH b, COLLECT(DISTINCT t.name) AS team_names"
                          ^} {gql_status: 50N42} {gql_status_description: error: general processing exception - unexpected error. Variable `t` not defined (line 2, column 26 (offset: 56))
"WITH b, COLLECT(DISTINCT t.name) AS team_names"
                          ^}

### 試行2（失敗）

```cypher
MATCH (b:Bug {status: 'open'})
RETURN 'Frontend' AS team_name, COUNT(b) AS bug_count
UNION ALL
RETURN 'Backend' AS team_name, COUNT(DISTINCT b) AS bug_count
ORDER BY bug_count DESC;
```

**エラー:** {neo4j_code: Neo.ClientError.Statement.SyntaxError} {message: Variable `b` not defined (line 4, column 47 (offset: 141))
"RETURN 'Backend' AS team_name, COUNT(DISTINCT b) AS bug_count"
                                               ^} {gql_status: 50N42} {gql_status_description: error: general processing exception - unexpected error. Variable `b` not defined (line 4, column 47 (offset: 141))
"RETURN 'Backend' AS team_name, COUNT(DISTINCT b) AS bug_count"
                                               ^}

### 試行3（失敗）

```cypher
MATCH (b:Bug {status: 'open'})
WITH b, CASE WHEN type(b) = 'Frontend' THEN 'Frontend' ELSE 'Backend' END AS team_name
RETURN team_name, COUNT(*) AS bug_count
UNION ALL
RETURN 'Frontend' AS team_name, COUNT(*) AS bug_count
ORDER BY bug_count DESC;
```

**エラー:** {neo4j_code: Neo.ClientError.Statement.SyntaxError} {message: Type mismatch: expected Relationship but was Node (line 2, column 24 (offset: 54))
"WITH b, CASE WHEN type(b) = 'Frontend' THEN 'Frontend' ELSE 'Backend' END AS team_name"
                        ^} {gql_status: 50N42} {gql_status_description: error: general processing exception - unexpected error. Type mismatch: expected Relationship but was Node (line 2, column 24 (offset: 54))
"WITH b, CASE WHEN type(b) = 'Frontend' THEN 'Frontend' ELSE 'Backend' END AS team_name"
                        ^}

**回答:**

Cypherクエリの生成・実行に失敗しました。

| 指標 | 値 |
|------|-----|
| 回答時間 | 60.19 秒 |
| 入力トークン | 41 |
| 出力トークン | 1 |
