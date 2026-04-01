# 実行レポート — medium_large_small

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-01 22:40:40 |
| シナリオ | medium_large_small |
| モード | graphrag |
| モデル | llama3.2 |
| データソース | data/large |
| クエリ数 | 5 |
| 合計回答時間 | 199.15 秒 |
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

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 15.37 秒 |
| 入力トークン | 45 |
| 出力トークン | 1 |

## Q2. 認証モジュールで発見されたバグの担当者名を教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:FOUND_IN]->(m:Module {name: '認証'})-[:PART_OF]->(p:Project)
OPTIONAL MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
RETURN e.name AS assignee
```

**Cypher実行結果:**

```
[]
```

**回答:**

該当するデータが見つかりません。

| 指標 | 値 |
|------|-----|
| 回答時間 | 16.32 秒 |
| 入力トークン | 45 |
| 出力トークン | 1 |

## Q3. 決済モジュールに関連するcriticalバグは誰が担当していますか？

**試行回数: 3回**

### 試行1（失敗）

```cypher
MATCH (b:Bug {severity: 'critical'})-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p:Project {name: '決済モジュール'})
OPTIONAL MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
RETURN e.name AS assignee, t.name AS team

### 2. 決済モジュールに関連するcriticalバグの担当者情報と、与えられたプロジェクトがどれくらいのバグに影響しているかを調べます。

Cypher:
MATCH (b:Bug {severity: 'critical'})-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p:Project {name: '決済モジュール'})
OPTIONAL MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
MATCH p <-[:BELONGS_TO]-(r:Release) RETURN r.version, r.status
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
  <EOF> (line 5, column 1 (offset: 217))
"### 2. 決済モジュールに関連するcriticalバグの担当者情報と、与えられたプロジェクトがどれくらいのバグに影響しているかを調べます。"
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
  <EOF> (line 5, column 1 (offset: 217))
"### 2. 決済モジュールに関連するcriticalバグの担当者情報と、与えられたプロジェクトがどれくらいのバグに影響しているかを調べます。"
 ^}

### 試行2（失敗）

```cypher
MATCH (b:Bug {severity: 'critical'})-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p:Project {name: '決済モジュール'})
WITH b, p, COLLECT(DISTINCT e) AS engineers, COLLECT(DISTINCT t) AS teams
RETURN e.name AS assignee, t.name AS team, COUNT(b) AS bug_count

MATCH p <-[:BELONGS_TO]-(r:Release)
WHERE r.version = (SELECT MIN(version) FROM Release WHERE project = '決済モジュール')
RETURN r.version, r.status
```

**エラー:** 構文エラー（静的チェック）: SELECT は使えません。MATCH ... RETURN を使ってください。 検出パターン: \bSELECT\b

### 試行3（失敗）

```cypher
MATCH (b:Bug {severity: 'critical'})-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p:Project {name: '決済モジュール'})
WITH b, p, COLLECT(DISTINCT e) AS engineers, COLLECT(DISTINCT t) AS teams
RETURN e.name AS assignee, t.name AS team, COUNT(b) AS bug_count

MATCH (r:Release)-[:BELONGS_TO]->(p:Project {name: '決済モジュール'})
WHERE r.version = (SELECT MIN(version) FROM Release WHERE project = '決済モジュール')
RETURN r.version, r.status
```

**エラー:** 構文エラー（静的チェック）: SELECT は使えません。MATCH ... RETURN を使ってください。 検出パターン: \bSELECT\b

**回答:**

Cypherクエリの生成・実行に失敗しました。

| 指標 | 値 |
|------|-----|
| 回答時間 | 55.82 秒 |
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

v1.1リリースをブロックしているバグの一覧と担当者は次の通りです。

- BUG-041：松本剛（セキュアティ）
- BUG-030：山田太郎（バックエンド）
- BUG-094：藤田恵美（API）
- BUG-002：鈴木花子（フロントエンド）
- BUG-005：渡辺恵（フロントエンド）
- BUG-004：山田太郎（バックエンド）
- BUG-043：藤田恵美（API）
- BUG-052：村田さくら（バックエンド）
- BUG-001：山田太郎（バックエンド）
- BUG-013：田中一郎（バックエンド）
- BUG-081：林美里（バックエンド）
- BUG-026：中村大輔（デボップス）
- BUG-017：中村大輔（デボップス）
- BUG-060：前田麗（API）
- BUG-075：藤田恵美（API）
- BUG-100：山田太郎（バックエンド）
- BUG-006：田中一郎（バックエンド）
- BUG-064：田中一郎（バックエンド）
- BUG-021：山田太郎（バックエンド）
- BUG-061：長谷川翼（フロントエンド）
- BUG-025：渡辺恵（フロントエンド）
- BUG-029：田中一郎（バックエンド）
- BUG-037：藤田恵美（API）
- BUG-042：橋本慎太郎（セキュアティ）

| 指標 | 値 |
|------|-----|
| 回答時間 | 54.85 秒 |
| 入力トークン | 48 |
| 出力トークン | 1 |

## Q5. FrontendチームとBackendチームのバグ件数を比較してください。

**試行回数: 3回**

### 試行1（失敗）

```cypher
MATCH (b:Bug)
WITH collect(DISTINCT b) as bugs
RETURN 
  'Frontend' AS team,
  count(filter(b.severity = 'critical', b.-[:MEMBER_OF]->(t:Team {name: 'Frontend'}))) AS frontend_bug_count,
  'Backend' AS team,
  count(filter(b.severity = 'critical', b.-[:MEMBER_OF]->(t:Team {name: 'Backend'}))) AS backend_bug_count
ORDER BY backend_bug_count DESC
```

**エラー:** {neo4j_code: Neo.ClientError.Statement.SyntaxError} {message: Invalid input '-': expected "TYPED" or an identifier (line 5, column 43 (offset: 119))
"  count(filter(b.severity = 'critical', b.-[:MEMBER_OF]->(t:Team {name: 'Frontend'}))) AS frontend_bug_count,"
                                           ^} {gql_status: 50N42} {gql_status_description: error: general processing exception - unexpected error. Invalid input '-': expected "TYPED" or an identifier (line 5, column 43 (offset: 119))
"  count(filter(b.severity = 'critical', b.-[:MEMBER_OF]->(t:Team {name: 'Frontend'}))) AS frontend_bug_count,"
                                           ^}

### 試行2（失敗）

```cypher
MATCH (b:Bug)
WITH collect(DISTINCT b) as bugs
RETURN 
  'Frontend' AS team,
  size(filter(b.severity = 'critical', b)-[:MEMBER_OF]->(t:Team {name: 'Frontend'})) AS frontend_bug_count,
  'Backend' AS team,
  size(filter(b.severity = 'critical', b)-[:MEMBER_OF]->(t:Team {name: 'Backend'})) AS backend_bug_count
ORDER BY backend_bug_count DESC
```

**エラー:** {neo4j_code: Neo.ClientError.Statement.SyntaxError} {message: Invalid input '[': expected "+" or "-" (line 5, column 43 (offset: 119))
"  size(filter(b.severity = 'critical', b)-[:MEMBER_OF]->(t:Team {name: 'Frontend'})) AS frontend_bug_count,"
                                           ^} {gql_status: 50N42} {gql_status_description: error: general processing exception - unexpected error. Invalid input '[': expected "+" or "-" (line 5, column 43 (offset: 119))
"  size(filter(b.severity = 'critical', b)-[:MEMBER_OF]->(t:Team {name: 'Frontend'})) AS frontend_bug_count,"
                                           ^}

### 試行3（失敗）

```cypher
MATCH (b:Bug)
WITH collect(DISTINCT b) as bugs
RETURN 
  'Frontend' AS team,
  size(filter((b)-[:MEMBER_OF]->(t:Team {name: 'Frontend'})) AND b.severity = 'critical') AS frontend_bug_count,
  'Backend' AS team,
  size(filter((b)-[:MEMBER_OF]->(t:Team {name: 'Backend'})) AND b.severity = 'critical') AS backend_bug_count
ORDER BY backend_bug_count DESC;
```

**エラー:** {neo4j_code: Neo.ClientError.Statement.SyntaxError} {message: PatternExpressions are not allowed to introduce new variables: 'b'. (line 5, column 16 (offset: 92))
"  size(filter((b)-[:MEMBER_OF]->(t:Team {name: 'Frontend'})) AND b.severity = 'critical') AS frontend_bug_count,"
                ^} {gql_status: 50N42} {gql_status_description: error: general processing exception - unexpected error. PatternExpressions are not allowed to introduce new variables: 'b'. (line 5, column 16 (offset: 92))
"  size(filter((b)-[:MEMBER_OF]->(t:Team {name: 'Frontend'})) AND b.severity = 'critical') AS frontend_bug_count,"
                ^}

**回答:**

Cypherクエリの生成・実行に失敗しました。

| 指標 | 値 |
|------|-----|
| 回答時間 | 56.79 秒 |
| 入力トークン | 41 |
| 出力トークン | 1 |
