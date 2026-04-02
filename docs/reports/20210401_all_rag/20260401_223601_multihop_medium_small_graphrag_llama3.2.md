# 実行レポート — multihop_medium_small

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-01 22:36:01 |
| シナリオ | multihop_medium_small |
| モード | graphrag |
| モデル | llama3.2 |
| データソース | data/medium |
| クエリ数 | 5 |
| 合計回答時間 | 115.61 秒 |
| 合計トークン（入力） | 273 |
| 合計トークン（出力） | 5 |

---

## Q1. Engineering部署のエンジニアが担当しているcriticalなオープンバグを全て教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {status: 'open', severity: 'critical'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)-[:BELONGS_TO]->(d:Department {name: 'Engineering'})
RETURN b.id, b.title
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-094', 'b.title': 'APIゲートウェイのSSL証明書の有効期限が切れそう'}, {'b.id': 'BUG-043', 'b.title': 'APIキーがログに平文で出力される'}, {'b.id': 'BUG-038', 'b.title': '通知サービスでiOS/Android両方に二重送信される'}, {'b.id': 'BUG-083', 'b.title': 'MobileチームのCI環境でコードサインのキーがExpireしている'}, {'b.id': 'BUG-096', 'b.title': 'Androidのアプリ内購入フローが失敗する'}, {'b.id': 'BUG-007', 'b.title': 'iOSアプリが起動時にクラッシュする'}, {'b.id': 'BUG-029', 'b.title': 'データベース接続プールが枯渇する'}, {'b.id': 'BUG-021', 'b.title': '決済時に在庫チェックが行われない'}, {'b.id': 'BUG-100', 'b.title': '決済モジュールの負荷試験で10%のリクエストが失敗する'}, {'b.id': 'BUG-004', 'b.title': 'クレジットカード決済がタイムアウトする'}, {'b.id': 'BUG-001', 'b.title': 'ログイン画面がフリーズする'}]
```

**回答:**

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 18.61 秒 |
| 入力トークン | 48 |
| 出力トークン | 1 |

## Q2. v1.1リリースをブロックしているバグが属するモジュールのプロジェクト名を教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.1'})-[:BELONGS_TO]->(p:Project)
RETURN p.id, p.name AS project_name
```

**Cypher実行結果:**

```
[{'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}, {'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}, {'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}, {'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}, {'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}, {'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}, {'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}, {'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}, {'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}, {'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}, {'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}, {'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}, {'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}, {'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}, {'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}, {'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}, {'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}, {'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}, {'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}, {'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}, {'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}, {'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}, {'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}, {'p.id': 'PROJ-001', 'project_name': 'ECサイトリニューアル'}]
```

**回答:**

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 20.30 秒 |
| 入力トークン | 54 |
| 出力トークン | 1 |

## Q3. ECサイトリニューアルプロジェクトのモジュールで発見されたバグのうち、Backendチームが担当しているものを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p:Project {name: 'ECサイトリニューアル'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Backend'})
RETURN b.id, b.title, e.name AS assignee
```

**Cypher実行結果:**

```
[]
```

**回答:**

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 17.96 秒 |
| 入力トークン | 59 |
| 出力トークン | 1 |

## Q4. criticalバグを担当しているエンジニアが所属する部署ごとのバグ件数を教えてください。

**試行回数: 2回**

### 試行1（失敗）

```cypher
MATCH (b:Bug {severity: 'critical'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
RETURN t.id AS team_id, t.name AS department
ORDER BY count(b) DESC
```

**エラー:** {neo4j_code: Neo.ClientError.Statement.SyntaxError} {message: Cannot use aggregation in ORDER BY if there are no aggregate expressions in the preceding RETURN (line 2, column 1 (offset: 89))
"RETURN t.id AS team_id, t.name AS department"
 ^} {gql_status: 50N42} {gql_status_description: error: general processing exception - unexpected error. Cannot use aggregation in ORDER BY if there are no aggregate expressions in the preceding RETURN (line 2, column 1 (offset: 89))
"RETURN t.id AS team_id, t.name AS department"
 ^}

### 試行2（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {severity: 'critical'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
RETURN e.id AS engineer_id, t.id AS team_id, count(b) AS bug_count
ORDER BY bug_count DESC
```

**Cypher実行結果:**

```
[{'engineer_id': 'ENG-001', 'team_id': 'TEAM-001', 'bug_count': 4}, {'engineer_id': 'ENG-007', 'team_id': 'TEAM-005', 'bug_count': 2}, {'engineer_id': 'ENG-012', 'team_id': 'TEAM-007', 'bug_count': 2}, {'engineer_id': 'ENG-011', 'team_id': 'TEAM-006', 'bug_count': 2}, {'engineer_id': 'ENG-022', 'team_id': 'TEAM-009', 'bug_count': 2}, {'engineer_id': 'ENG-019', 'team_id': 'TEAM-006', 'bug_count': 2}, {'engineer_id': 'ENG-004', 'team_id': 'TEAM-003', 'bug_count': 1}, {'engineer_id': 'ENG-003', 'team_id': 'TEAM-001', 'bug_count': 1}, {'engineer_id': 'ENG-016', 'team_id': 'TEAM-003', 'bug_count': 1}, {'engineer_id': 'ENG-013', 'team_id': 'TEAM-008', 'bug_count': 1}, {'engineer_id': 'ENG-021', 'team_id': 'TEAM-008', 'bug_count': 1}, {'engineer_id': 'ENG-026', 'team_id': 'TEAM-003', 'bug_count': 1}, {'engineer_id': 'ENG-020', 'team_id': 'TEAM-007', 'bug_count': 1}, {'engineer_id': 'ENG-009', 'team_id': 'TEAM-003', 'bug_count': 1}]
```

**回答:**

そのようなデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 32.97 秒 |
| 入力トークン | 50 |
| 出力トークン | 1 |

## Q5. モバイルアプリ開発プロジェクトのv1.0リリースをブロックしているバグの担当エンジニアが所属するチームを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.0'})-[:BELONGS_TO]->(p:Project)
OPTIONAL MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
RETURN e.name AS assignee, t.name AS team, p.name AS project
```

**Cypher実行結果:**

```
[{'assignee': '加藤誠', 'team': 'Mobile', 'project': 'モバイルアプリ開発'}, {'assignee': '加藤誠', 'team': 'Mobile', 'project': 'モバイルアプリ開発'}, {'assignee': '中村大輔', 'team': 'DevOps', 'project': 'モバイルアプリ開発'}, {'assignee': '坂本竜一', 'team': 'Mobile', 'project': 'モバイルアプリ開発'}, {'assignee': '佐藤美咲', 'team': 'Mobile', 'project': 'モバイルアプリ開発'}, {'assignee': '坂本竜一', 'team': 'Mobile', 'project': 'モバイルアプリ開発'}, {'assignee': '加藤誠', 'team': 'Mobile', 'project': 'モバイルアプリ開発'}, {'assignee': '山本香織', 'team': 'Mobile', 'project': 'モバイルアプリ開発'}, {'assignee': '佐藤美咲', 'team': 'Mobile', 'project': 'モバイルアプリ開発'}, {'assignee': '井上真由', 'team': 'DataEngineering', 'project': 'データ基盤構築'}, {'assignee': '藤原大樹', 'team': 'Platform', 'project': 'データ基盤構築'}, {'assignee': '石川莉奈', 'team': 'DataEngineering', 'project': 'データ基盤構築'}, {'assignee': '井上真由', 'team': 'DataEngineering', 'project': 'データ基盤構築'}, {'assignee': '石川莉奈', 'team': 'DataEngineering', 'project': 'データ基盤構築'}, {'assignee': '石川莉奈', 'team': 'DataEngineering', 'project': 'データ基盤構築'}, {'assignee': '岡田和也', 'team': 'Platform', 'project': 'データ基盤構築'}, {'assignee': '石川莉奈', 'team': 'DataEngineering', 'project': 'データ基盤構築'}, {'assignee': '井上真由', 'team': 'DataEngineering', 'project': 'データ基盤構築'}, {'assignee': '上田健', 'team': 'MachineLearning', 'project': 'AI推薦エンジン'}, {'assignee': '木村雄介', 'team': 'MachineLearning', 'project': 'AI推薦エンジン'}, {'assignee': '木村雄介', 'team': 'MachineLearning', 'project': 'AI推薦エンジン'}, {'assignee': '上田健', 'team': 'MachineLearning', 'project': 'AI推薦エンジン'}, {'assignee': '上田健', 'team': 'MachineLearning', 'project': 'AI推薦エンジン'}, {'assignee': '木村雄介', 'team': 'MachineLearning', 'project': 'AI推薦エンジン'}, {'assignee': '松本剛', 'team': 'Security', 'project': 'セキュリティ強化'}, {'assignee': '松本剛', 'team': 'Security', 'project': 'セキュリティ強化'}, {'assignee': '橋本慎太郎', 'team': 'Security', 'project': 'セキュリティ強化'}, {'assignee': '小林直子', 'team': 'API', 'project': 'セキュリティ強化'}, {'assignee': '橋本慎太郎', 'team': 'Security', 'project': 'セキュリティ強化'}, {'assignee': '橋本慎太郎', 'team': 'Security', 'project': 'セキュリティ強化'}, {'assignee': '近藤真一', 'team': 'QA', 'project': 'セキュリティ強化'}, {'assignee': '松本剛', 'team': 'Security', 'project': 'セキュリティ強化'}, {'assignee': '橋本慎太郎', 'team': 'Security', 'project': 'セキュリティ強化'}, {'assignee': '橋本慎太郎', 'team': 'Security', 'project': 'セキュリティ強化'}]
```

**回答:**

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 25.77 秒 |
| 入力トークン | 62 |
| 出力トークン | 1 |
