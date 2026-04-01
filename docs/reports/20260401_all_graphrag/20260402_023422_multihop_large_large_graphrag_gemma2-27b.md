# 実行レポート — multihop_large_large

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-02 02:34:22 |
| シナリオ | multihop_large_large |
| モード | graphrag |
| モデル | gemma2:27b |
| データソース | data/large |
| クエリ数 | 5 |
| 合計回答時間 | 620.00 秒 |
| 合計トークン（入力） | 152 |
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


提供されたCypher実行結果には、Engineering部署のエンジニアが担当しているcriticalなオープンバグに関する情報は含まれていません。

| 指標 | 値 |
|------|-----|
| 回答時間 | 136.29 秒 |
| 入力トークン | 27 |
| 出力トークン | 1 |

## Q2. v1.1リリースをブロックしているバグが属するモジュールのプロジェクト名を教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.1'})-[:BELONGS_TO]->(p:Project)
WITH b, p
MATCH (b)-[:FOUND_IN]->(m:Module)
RETURN p.name AS projectName
```

**Cypher実行結果:**

```
[{'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}]
```

**回答:**

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 119.01 秒 |
| 入力トークン | 30 |
| 出力トークン | 1 |

## Q3. ECサイトリニューアルプロジェクトのモジュールで発見されたバグのうち、Backendチームが担当しているものを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p:Project {name: 'ECサイトリニューアル'})
MATCH (b)<-[:ASSIGNED_TO]-(e:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Backend'})
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
| 回答時間 | 110.74 秒 |
| 入力トークン | 32 |
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

部署ごとのcriticalバグ件数は以下の通りです。

* Engineering: 11件
* Data: 5件
* Security: 4件
* Infrastructure: 2件

| 指標 | 値 |
|------|-----|
| 回答時間 | 121.73 秒 |
| 入力トークン | 28 |
| 出力トークン | 1 |

## Q5. モバイルアプリ開発プロジェクトのv1.0リリースをブロックしているバグの担当エンジニアが所属するチームを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.0'})-[:BELONGS_TO]->(p:Project {name: 'モバイルアプリ開発'})
OPTIONAL MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
RETURN t.name AS team, e.name AS engineer, b.title AS bug_title
```

**Cypher実行結果:**

```
[{'team': 'Mobile', 'engineer': '加藤誠', 'bug_title': 'Androidで通知が届かない'}, {'team': 'Mobile', 'engineer': '加藤誠', 'bug_title': 'Androidのアプリ内購入フローが失敗する'}, {'team': 'DevOps', 'engineer': '中村大輔', 'bug_title': '管理者ロールの権限チェックが不正'}, {'team': 'Mobile', 'engineer': '坂本竜一', 'bug_title': 'iOSアプリのバッテリー消費が激しい'}, {'team': 'Mobile', 'engineer': '佐藤美咲', 'bug_title': 'iOSプッシュ通知のディープリンクが動作しない'}, {'team': 'Mobile', 'engineer': '坂本竜一', 'bug_title': 'MobileチームのCI環境でコードサインのキーがExpireしている'}, {'team': 'Mobile', 'engineer': '加藤誠', 'bug_title': 'Androidアプリのメモリリーク'}, {'team': 'Mobile', 'engineer': '山本香織', 'bug_title': '通知サービスでiOS/Android両方に二重送信される'}, {'team': 'Mobile', 'engineer': '佐藤美咲', 'bug_title': 'iOSアプリが起動時にクラッシュする'}]
```

**回答:**

Mobileチームです。

| 指標 | 値 |
|------|-----|
| 回答時間 | 132.23 秒 |
| 入力トークン | 35 |
| 出力トークン | 1 |
