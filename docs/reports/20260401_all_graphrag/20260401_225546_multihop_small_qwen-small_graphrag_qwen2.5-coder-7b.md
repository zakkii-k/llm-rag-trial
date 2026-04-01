# 実行レポート — multihop_small_qwen-small

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-01 22:55:46 |
| シナリオ | multihop_small_qwen-small |
| モード | graphrag |
| モデル | qwen2.5-coder:7b |
| データソース | data/small |
| クエリ数 | 5 |
| 合計回答時間 | 309.50 秒 |
| 合計トークン（入力） | 279 |
| 合計トークン（出力） | 5 |

---

## Q1. Engineering部署のエンジニアが担当しているcriticalなオープンバグを全て教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {severity: 'critical', status: 'open'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)-[:BELONGS_TO]->(d:Department {name: 'Engineering'})
RETURN b.id, b.title
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-094', 'b.title': 'APIゲートウェイのSSL証明書の有効期限が切れそう'}, {'b.id': 'BUG-043', 'b.title': 'APIキーがログに平文で出力される'}, {'b.id': 'BUG-038', 'b.title': '通知サービスでiOS/Android両方に二重送信される'}, {'b.id': 'BUG-083', 'b.title': 'MobileチームのCI環境でコードサインのキーがExpireしている'}, {'b.id': 'BUG-096', 'b.title': 'Androidのアプリ内購入フローが失敗する'}, {'b.id': 'BUG-007', 'b.title': 'iOSアプリが起動時にクラッシュする'}, {'b.id': 'BUG-029', 'b.title': 'データベース接続プールが枯渇する'}, {'b.id': 'BUG-021', 'b.title': '決済時に在庫チェックが行われない'}, {'b.id': 'BUG-100', 'b.title': '決済モジュールの負荷試験で10%のリクエストが失敗する'}, {'b.id': 'BUG-004', 'b.title': 'クレジットカード決済がタイムアウトする'}, {'b.id': 'BUG-001', 'b.title': 'ログイン画面がフリーズする'}]
```

**回答:**

Engineering部署のエンジニアが担当しているcriticalなオープンバグは以下の通りです：

1. BUG-094: APIゲートウェイのSSL証明書の有効期限が切れそう
2. BUG-043: APIキーがログに平文で出力される
3. BUG-038: 通知サービスでiOS/Android両方に二重送信される
4. BUG-083: MobileチームのCI環境でコードサインのキーがExpireしている
5. BUG-096: Androidのアプリ内購入フローが失敗する
6. BUG-007: iOSアプリが起動時にクラッシュする
7. BUG-029: データベース接続プールが枯渇する
8. BUG-021: 決済時に在庫チェックが行われない
9. BUG-100: 決済モジュールの負荷試験で10%のリクエストが失敗する
10. BUG-004: クレジットカード決済がタイムアウトする
11. BUG-001: ログイン画面がフリーズする

| 指標 | 値 |
|------|-----|
| 回答時間 | 64.32 秒 |
| 入力トークン | 48 |
| 出力トークン | 1 |

## Q2. v1.1リリースをブロックしているバグが属するモジュールのプロジェクト名を教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.1'})-[:BELONGS_TO]->(p:Project)
OPTIONAL MATCH (m:Module)-[:FOUND_IN]->(b)
RETURN p.name AS project_name, m.name AS module_name
```

**Cypher実行結果:**

```
[{'project_name': 'ECサイトリニューアル', 'module_name': None}, {'project_name': 'ECサイトリニューアル', 'module_name': None}, {'project_name': 'ECサイトリニューアル', 'module_name': None}, {'project_name': 'ECサイトリニューアル', 'module_name': None}, {'project_name': 'ECサイトリニューアル', 'module_name': None}, {'project_name': 'ECサイトリニューアル', 'module_name': None}, {'project_name': 'ECサイトリニューアル', 'module_name': None}, {'project_name': 'ECサイトリニューアル', 'module_name': None}, {'project_name': 'ECサイトリニューアル', 'module_name': None}, {'project_name': 'ECサイトリニューアル', 'module_name': None}, {'project_name': 'ECサイトリニューアル', 'module_name': None}, {'project_name': 'ECサイトリニューアル', 'module_name': None}, {'project_name': 'ECサイトリニューアル', 'module_name': None}, {'project_name': 'ECサイトリニューアル', 'module_name': None}, {'project_name': 'ECサイトリニューアル', 'module_name': None}, {'project_name': 'ECサイトリニューアル', 'module_name': None}, {'project_name': 'ECサイトリニューアル', 'module_name': None}, {'project_name': 'ECサイトリニューアル', 'module_name': None}, {'project_name': 'ECサイトリニューアル', 'module_name': None}, {'project_name': 'ECサイトリニューアル', 'module_name': None}, {'project_name': 'ECサイトリニューアル', 'module_name': None}, {'project_name': 'ECサイトリニューアル', 'module_name': None}, {'project_name': 'ECサイトリニューアル', 'module_name': None}, {'project_name': 'ECサイトリニューアル', 'module_name': None}]
```

**回答:**

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 44.13 秒 |
| 入力トークン | 55 |
| 出力トークン | 1 |

## Q3. ECサイトリニューアルプロジェクトのモジュールで発見されたバグのうち、Backendチームが担当しているものを教えてください。

**試行回数: 3回**

### 試行1（失敗）

```cypher
MATCH (b:Bug)-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p:Project {name: 'ECサイトリニューアル'})
WHERE EXISTS ((b)-[:ASSIGNED_TO]->(:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Backend'}))
RETURN b.id, b.title, b.severity, b.status, m.name AS module
```

**エラー:** {neo4j_code: Neo.ClientError.Statement.SyntaxError} {message: PatternExpressions are not allowed to introduce new variables: 't'. (line 2, column 62 (offset: 145))
"WHERE EXISTS ((b)-[:ASSIGNED_TO]->(:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Backend'}))"
                                                              ^} {gql_status: 50N42} {gql_status_description: error: general processing exception - unexpected error. PatternExpressions are not allowed to introduce new variables: 't'. (line 2, column 62 (offset: 145))
"WHERE EXISTS ((b)-[:ASSIGNED_TO]->(:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Backend'}))"
                                                              ^}

### 試行2（失敗）

```cypher
MATCH (b:Bug)-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p:Project {name: 'ECサイトリニューアル'})
WITH b, m
WHERE EXISTS ((b)-[:ASSIGNED_TO]->(:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Backend'}))
RETURN b.id, b.title, b.severity, b.status, m.name AS module
```

**エラー:** {neo4j_code: Neo.ClientError.Statement.SyntaxError} {message: PatternExpressions are not allowed to introduce new variables: 't'. (line 3, column 62 (offset: 155))
"WHERE EXISTS ((b)-[:ASSIGNED_TO]->(:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Backend'}))"
                                                              ^} {gql_status: 50N42} {gql_status_description: error: general processing exception - unexpected error. PatternExpressions are not allowed to introduce new variables: 't'. (line 3, column 62 (offset: 155))
"WHERE EXISTS ((b)-[:ASSIGNED_TO]->(:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Backend'}))"
                                                              ^}

### 試行3（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p:Project {name: 'ECサイトリニューアル'})
WITH b, m
CALL {
    WITH b, m
    MATCH path = (b)-[:ASSIGNED_TO]->(:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Backend'})
    RETURN path IS NOT NULL AS is_backend_team
}
RETURN b.id, b.title, b.severity, b.status, m.name AS module, CASE WHEN is_backend_team THEN 'Yes' ELSE 'No' END AS assigned_to_backend_team
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-011', 'b.title': 'セッションが30分で切れる', 'b.severity': 'low', 'b.status': 'open', 'module': '認証モジュール', 'assigned_to_backend_team': 'Yes'}, {'b.id': 'BUG-003', 'b.title': 'パスワードリセットメールが届かない', 'b.severity': 'medium', 'b.status': 'resolved', 'module': '認証モジュール', 'assigned_to_backend_team': 'Yes'}, {'b.id': 'BUG-001', 'b.title': 'ログイン画面がフリーズする', 'b.severity': 'critical', 'b.status': 'open', 'module': '認証モジュール', 'assigned_to_backend_team': 'Yes'}, {'b.id': 'BUG-030', 'b.title': 'ユーザー登録時にメールアドレスの重複チェックが失敗する', 'b.severity': 'high', 'b.status': 'open', 'module': '認証モジュール', 'assigned_to_backend_team': 'Yes'}, {'b.id': 'BUG-046', 'b.title': 'Backendチームのビルド時間が10分を超える', 'b.severity': 'medium', 'b.status': 'in_progress', 'module': '認証モジュール', 'assigned_to_backend_team': 'Yes'}, {'b.id': 'BUG-064', 'b.title': '商品の在庫数がリアルタイムに反映されない', 'b.severity': 'high', 'b.status': 'open', 'module': '商品カタログ', 'assigned_to_backend_team': 'Yes'}, {'b.id': 'BUG-047', 'b.title': 'ユニットテストのカバレッジが60%を下回る', 'b.severity': 'medium', 'b.status': 'open', 'module': '決済モジュール', 'assigned_to_backend_team': 'Yes'}, {'b.id': 'BUG-013', 'b.title': '決済完了メールが二重送信される', 'b.severity': 'high', 'b.status': 'open', 'module': '決済モジュール', 'assigned_to_backend_team': 'Yes'}, {'b.id': 'BUG-081', 'b.title': 'Backendのメモリ使用量が時間で増加する', 'b.severity': 'high', 'b.status': 'open', 'module': '決済モジュール', 'assigned_to_backend_team': 'Yes'}, {'b.id': 'BUG-021', 'b.title': '決済時に在庫チェックが行われない', 'b.severity': 'critical', 'b.status': 'open', 'module': '決済モジュール', 'assigned_to_backend_team': 'Yes'}, {'b.id': 'BUG-004', 'b.title': 'クレジットカード決済がタイムアウトする', 'b.severity': 'critical', 'b.status': 'open', 'module': '決済モジュール', 'assigned_to_backend_team': 'Yes'}, {'b.id': 'BUG-029', 'b.title': 'データベース接続プールが枯渇する', 'b.severity': 'critical', 'b.status': 'open', 'module': '決済モジュール', 'assigned_to_backend_team': 'Yes'}, {'b.id': 'BUG-065', 'b.title': '決済後のカート内容が残る', 'b.severity': 'medium', 'b.status': 'open', 'module': '決済モジュール', 'assigned_to_backend_team': 'Yes'}, {'b.id': 'BUG-052', 'b.title': '決済APIのタイムアウト設定が短すぎる', 'b.severity': 'high', 'b.status': 'open', 'module': '決済モジュール', 'assigned_to_backend_team': 'Yes'}, {'b.id': 'BUG-006', 'b.title': 'カートに追加後に金額がずれる', 'b.severity': 'high', 'b.status': 'in_progress', 'module': '決済モジュール', 'assigned_to_backend_team': 'Yes'}, {'b.id': 'BUG-100', 'b.title': '決済モジュールの負荷試験で10%のリクエストが失敗する', 'b.severity': 'critical', 'b.status': 'open', 'module': '決済モジュール', 'assigned_to_backend_team': 'Yes'}]
```

**回答:**

以下はECサイトリニューアルプロジェクトのモジュールで発見されたバグのうち、Backendチームが担当しているもののリストです：

1. **セッションが30分で切れる** (BUG-011)
2. **パスワードリセットメールが届かない** (BUG-003)
3. **ログイン画面がフリーズする** (BUG-001)
4. **ユーザー登録時にメールアドレスの重複チェックが失敗する** (BUG-030)
5. **Backendチームのビルド時間が10分を超える** (BUG-046)

これらのバグは全て「認証モジュール」に関連しています。

| 指標 | 値 |
|------|-----|
| 回答時間 | 110.17 秒 |
| 入力トークン | 60 |
| 出力トークン | 1 |

## Q4. criticalバグを担当しているエンジニアが所属する部署ごとのバグ件数を教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {severity: 'critical'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)-[:BELONGS_TO]->(d:Department)
RETURN d.name AS department, count(b) AS bug_count
ORDER BY bug_count DESC
```

**Cypher実行結果:**

```
[{'department': 'Engineering', 'bug_count': 11}, {'department': 'Data', 'bug_count': 5}, {'department': 'Security', 'bug_count': 4}, {'department': 'Infrastructure', 'bug_count': 2}]
```

**回答:**

criticalバグを担当しているエンジニアが所属する部署ごとのバグ件数は以下の通りです：

Engineering: 11件
Data: 5件
Security: 4件
Infrastructure: 2件

| 指標 | 値 |
|------|-----|
| 回答時間 | 40.16 秒 |
| 入力トークン | 52 |
| 出力トークン | 1 |

## Q5. モバイルアプリ開発プロジェクトのv1.0リリースをブロックしているバグの担当エンジニアが所属するチームを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.0'})-[:BELONGS_TO]->(p:Project {name: 'モバイルアプリ開発'})
OPTIONAL MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
RETURN b.id, b.title, e.name AS assignee, t.name AS team
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-008', 'b.title': 'Androidで通知が届かない', 'assignee': '加藤誠', 'team': 'Mobile'}, {'b.id': 'BUG-096', 'b.title': 'Androidのアプリ内購入フローが失敗する', 'assignee': '加藤誠', 'team': 'Mobile'}, {'b.id': 'BUG-024', 'b.title': '管理者ロールの権限チェックが不正', 'assignee': '中村大輔', 'team': 'DevOps'}, {'b.id': 'BUG-053', 'b.title': 'iOSアプリのバッテリー消費が激しい', 'assignee': '坂本竜一', 'team': 'Mobile'}, {'b.id': 'BUG-014', 'b.title': 'iOSプッシュ通知のディープリンクが動作しない', 'assignee': '佐藤美咲', 'team': 'Mobile'}, {'b.id': 'BUG-083', 'b.title': 'MobileチームのCI環境でコードサインのキーがExpireしている', 'assignee': '坂本竜一', 'team': 'Mobile'}, {'b.id': 'BUG-018', 'b.title': 'Androidアプリのメモリリーク', 'assignee': '加藤誠', 'team': 'Mobile'}, {'b.id': 'BUG-038', 'b.title': '通知サービスでiOS/Android両方に二重送信される', 'assignee': '山本香織', 'team': 'Mobile'}, {'b.id': 'BUG-007', 'b.title': 'iOSアプリが起動時にクラッシュする', 'assignee': '佐藤美咲', 'team': 'Mobile'}]
```

**回答:**

加藤誠が担当しているバグのうち、v1.0リリースをブロックしているものは「Androidで通知が届かない」（BUG-008）と「Androidアプリのメモリリーク」（BUG-018）です。

これらのバグが所属するチームは「Mobile」です。

| 指標 | 値 |
|------|-----|
| 回答時間 | 50.72 秒 |
| 入力トークン | 64 |
| 出力トークン | 1 |
