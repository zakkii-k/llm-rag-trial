# 実行レポート — medium_large_large

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-02 02:21:01 |
| シナリオ | medium_large_large |
| モード | graphrag |
| モデル | gemma2:27b |
| データソース | data/large |
| クエリ数 | 5 |
| 合計回答時間 | 795.51 秒 |
| 合計トークン（入力） | 119 |
| 合計トークン（出力） | 5 |

---

## Q1. Backendチームのエンジニアが担当しているオープンなバグを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {status: 'open'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Backend'})
RETURN b.id, b.title, b.severity, e.name
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-081', 'b.title': 'Backendのメモリ使用量が時間で増加する', 'b.severity': 'high', 'e.name': '林美里'}, {'b.id': 'BUG-047', 'b.title': 'ユニットテストのカバレッジが60%を下回る', 'b.severity': 'medium', 'e.name': '林美里'}, {'b.id': 'BUG-052', 'b.title': '決済APIのタイムアウト設定が短すぎる', 'b.severity': 'high', 'e.name': '村田さくら'}, {'b.id': 'BUG-065', 'b.title': '決済後のカート内容が残る', 'b.severity': 'medium', 'e.name': '村田さくら'}, {'b.id': 'BUG-029', 'b.title': 'データベース接続プールが枯渇する', 'b.severity': 'critical', 'e.name': '田中一郎'}, {'b.id': 'BUG-013', 'b.title': '決済完了メールが二重送信される', 'b.severity': 'high', 'e.name': '田中一郎'}, {'b.id': 'BUG-064', 'b.title': '商品の在庫数がリアルタイムに反映されない', 'b.severity': 'high', 'e.name': '田中一郎'}, {'b.id': 'BUG-021', 'b.title': '決済時に在庫チェックが行われない', 'b.severity': 'critical', 'e.name': '山田太郎'}, {'b.id': 'BUG-100', 'b.title': '決済モジュールの負荷試験で10%のリクエストが失敗する', 'b.severity': 'critical', 'e.name': '山田太郎'}, {'b.id': 'BUG-030', 'b.title': 'ユーザー登録時にメールアドレスの重複チェックが失敗する', 'b.severity': 'high', 'e.name': '山田太郎'}, {'b.id': 'BUG-004', 'b.title': 'クレジットカード決済がタイムアウトする', 'b.severity': 'critical', 'e.name': '山田太郎'}, {'b.id': 'BUG-001', 'b.title': 'ログイン画面がフリーズする', 'b.severity': 'critical', 'e.name': '山田太郎'}, {'b.id': 'BUG-011', 'b.title': 'セッションが30分で切れる', 'b.severity': 'low', 'e.name': '山田太郎'}]
```

**回答:**

Backendチームのエンジニアが担当しているオープンなバグは以下の通りです。

* **BUG-081:** Backendのメモリ使用量が時間で増加する (担当: 林美里)

| 指標 | 値 |
|------|-----|
| 回答時間 | 153.65 秒 |
| 入力トークン | 24 |
| 出力トークン | 1 |

## Q2. 認証モジュールで発見されたバグの担当者名を教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:FOUND_IN]->(m:Module {name: '認証'})-[:PART_OF]->(p:Project)
OPTIONAL MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)
RETURN b.id, b.title, e.name AS engineer
```

**Cypher実行結果:**

```
[]
```

**回答:**

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 105.78 秒 |
| 入力トークン | 24 |
| 出力トークン | 1 |

## Q3. 決済モジュールに関連するcriticalバグは誰が担当していますか？

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {severity: 'critical'})-[:FOUND_IN]->(m:Module {name: '決済'})-[:ASSIGNED_TO]->(e:Engineer)
RETURN b.id, b.title, e.name AS engineer
```

**Cypher実行結果:**

```
[]
```

**回答:**

該当するデータが見つかりませんでした

| 指標 | 値 |
|------|-----|
| 回答時間 | 101.87 秒 |
| 入力トークン | 24 |
| 出力トークン | 1 |

## Q4. v1.1リリースをブロックしているバグの一覧と担当者を教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.1'})-[:BELONGS_TO]->(p:Project)
OPTIONAL MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)
RETURN b.id, b.title, e.name AS assignee
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-041', 'b.title': 'SQLインジェクションの脆弱性が検出された', 'assignee': '松本剛'}, {'b.id': 'BUG-030', 'b.title': 'ユーザー登録時にメールアドレスの重複チェックが失敗する', 'assignee': '山田太郎'}, {'b.id': 'BUG-094', 'b.title': 'APIゲートウェイのSSL証明書の有効期限が切れそう', 'assignee': '藤田恵美'}, {'b.id': 'BUG-002', 'b.title': '検索結果が0件になる', 'assignee': '鈴木花子'}, {'b.id': 'BUG-005', 'b.title': '商品画像が表示されない', 'assignee': '渡辺恵'}, {'b.id': 'BUG-004', 'b.title': 'クレジットカード決済がタイムアウトする', 'assignee': '山田太郎'}, {'b.id': 'BUG-043', 'b.title': 'APIキーがログに平文で出力される', 'assignee': '藤田恵美'}, {'b.id': 'BUG-052', 'b.title': '決済APIのタイムアウト設定が短すぎる', 'assignee': '村田さくら'}, {'b.id': 'BUG-001', 'b.title': 'ログイン画面がフリーズする', 'assignee': '山田太郎'}, {'b.id': 'BUG-013', 'b.title': '決済完了メールが二重送信される', 'assignee': '田中一郎'}, {'b.id': 'BUG-081', 'b.title': 'Backendのメモリ使用量が時間で増加する', 'assignee': '林美里'}, {'b.id': 'BUG-026', 'b.title': 'CI/CDパイプラインが失敗する', 'assignee': '中村大輔'}, {'b.id': 'BUG-017', 'b.title': 'ログアウト後もセッションが残る', 'assignee': '中村大輔'}, {'b.id': 'BUG-060', 'b.title': 'APIゲートウェイのキャッシュが正しくパージされない', 'assignee': '前田麗'}, {'b.id': 'BUG-075', 'b.title': 'APIゲートウェイでリクエストが稀にドロップする', 'assignee': '藤田恵美'}, {'b.id': 'BUG-100', 'b.title': '決済モジュールの負荷試験で10%のリクエストが失敗する', 'assignee': '山田太郎'}, {'b.id': 'BUG-006', 'b.title': 'カートに追加後に金額がずれる', 'assignee': '田中一郎'}, {'b.id': 'BUG-064', 'b.title': '商品の在庫数がリアルタイムに反映されない', 'assignee': '田中一郎'}, {'b.id': 'BUG-021', 'b.title': '決済時に在庫チェックが行われない', 'assignee': '山田太郎'}, {'b.id': 'BUG-061', 'b.title': 'Frontend画面の初期ロードが5秒以上かかる', 'assignee': '長谷川翼'}, {'b.id': 'BUG-025', 'b.title': '商品レビューが投稿できない', 'assignee': '渡辺恵'}, {'b.id': 'BUG-029', 'b.title': 'データベース接続プールが枯渇する', 'assignee': '田中一郎'}, {'b.id': 'BUG-037', 'b.title': 'APIゲートウェイの認証トークン検証が遅い', 'assignee': '藤田恵美'}, {'b.id': 'BUG-042', 'b.title': 'XSS脆弱性がコメント投稿フォームに存在', 'assignee': '橋本慎太郎'}]
```

**回答:**

v1.1リリースをブロックしているバグは以下の通りです。

* **BUG-041**: SQLインジェクションの脆弱性が検出された (担当: 松本剛)
* **BUG-030**: ユーザー登録時にメールアドレスの重複チェックが失敗する (担当: 山田太郎)
* **BUG-094**: APIゲートウェイのSSL証明書の有効期限が切れそう (担当: 藤田恵美)

| 指標 | 値 |
|------|-----|
| 回答時間 | 196.23 秒 |
| 入力トークン | 26 |
| 出力トークン | 1 |

## Q5. FrontendチームとBackendチームのバグ件数を比較してください。

**試行回数: 3回**

### 試行1（失敗）

```cypher
MATCH (b:Bug)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
WITH t.name AS team, b
RETURN team, count(b) AS bug_count
ORDER BY bug_count DESC

MATCH (b:Bug)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team {name:'Frontend'})
RETURN count(b) AS frontend_bug_count

MATCH (b:Bug)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team {name:'Backend'})
RETURN count(b) AS backend_bug_count
```

**エラー:** {neo4j_code: Neo.ClientError.Statement.SyntaxError} {message: RETURN can only be used at the end of the query (line 3, column 1 (offset: 89))
"RETURN team, count(b) AS bug_count"
 ^} {gql_status: 50N42} {gql_status_description: error: general processing exception - unexpected error. RETURN can only be used at the end of the query (line 3, column 1 (offset: 89))
"RETURN team, count(b) AS bug_count"
 ^}

### 試行2（失敗）

```cypher
MATCH (b:Bug)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Frontend'})
RETURN count(b) AS frontend_bug_count

MATCH (b:Bug)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Backend'})
RETURN count(b) AS backend_bug_count
```

**エラー:** {neo4j_code: Neo.ClientError.Statement.SyntaxError} {message: RETURN can only be used at the end of the query (line 2, column 1 (offset: 85))
"RETURN count(b) AS frontend_bug_count"
 ^} {gql_status: 50N42} {gql_status_description: error: general processing exception - unexpected error. RETURN can only be used at the end of the query (line 2, column 1 (offset: 85))
"RETURN count(b) AS frontend_bug_count"
 ^}

### 試行3（失敗）

```cypher
MATCH (b:Bug)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Frontend'})
WITH b, t
RETURN count(b) AS frontend_bug_count

MATCH (b:Bug)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Backend'})
WITH b, t
RETURN count(b) AS backend_bug_count
```

**エラー:** {neo4j_code: Neo.ClientError.Statement.SyntaxError} {message: RETURN can only be used at the end of the query (line 3, column 1 (offset: 95))
"RETURN count(b) AS frontend_bug_count"
 ^} {gql_status: 50N42} {gql_status_description: error: general processing exception - unexpected error. RETURN can only be used at the end of the query (line 3, column 1 (offset: 95))
"RETURN count(b) AS frontend_bug_count"
 ^}

**回答:**

Cypherクエリの生成・実行に失敗しました。

| 指標 | 値 |
|------|-----|
| 回答時間 | 237.98 秒 |
| 入力トークン | 21 |
| 出力トークン | 1 |
