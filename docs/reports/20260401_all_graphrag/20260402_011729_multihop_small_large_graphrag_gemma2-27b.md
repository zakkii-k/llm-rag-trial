# 実行レポート — multihop_small_large

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-02 01:17:29 |
| シナリオ | multihop_small_large |
| モード | graphrag |
| モデル | gemma2:27b |
| データソース | data/small |
| クエリ数 | 5 |
| 合計回答時間 | 711.46 秒 |
| 合計トークン（入力） | 152 |
| 合計トークン（出力） | 5 |

---

## Q1. Engineering部署のエンジニアが担当しているcriticalなオープンバグを全て教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {status: 'open', severity: 'critical'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)-[:BELONGS_TO]->(d:Department {name: 'Engineering'})
RETURN b.id, b.title, b.severity, e.name
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-094', 'b.title': 'APIゲートウェイのSSL証明書の有効期限が切れそう', 'b.severity': 'critical', 'e.name': '藤田恵美'}, {'b.id': 'BUG-043', 'b.title': 'APIキーがログに平文で出力される', 'b.severity': 'critical', 'e.name': '藤田恵美'}, {'b.id': 'BUG-038', 'b.title': '通知サービスでiOS/Android両方に二重送信される', 'b.severity': 'critical', 'e.name': '山本香織'}, {'b.id': 'BUG-083', 'b.title': 'MobileチームのCI環境でコードサインのキーがExpireしている', 'b.severity': 'critical', 'e.name': '坂本竜一'}, {'b.id': 'BUG-096', 'b.title': 'Androidのアプリ内購入フローが失敗する', 'b.severity': 'critical', 'e.name': '加藤誠'}, {'b.id': 'BUG-007', 'b.title': 'iOSアプリが起動時にクラッシュする', 'b.severity': 'critical', 'e.name': '佐藤美咲'}, {'b.id': 'BUG-029', 'b.title': 'データベース接続プールが枯渇する', 'b.severity': 'critical', 'e.name': '田中一郎'}, {'b.id': 'BUG-021', 'b.title': '決済時に在庫チェックが行われない', 'b.severity': 'critical', 'e.name': '山田太郎'}, {'b.id': 'BUG-100', 'b.title': '決済モジュールの負荷試験で10%のリクエストが失敗する', 'b.severity': 'critical', 'e.name': '山田太郎'}, {'b.id': 'BUG-004', 'b.title': 'クレジットカード決済がタイムアウトする', 'b.severity': 'critical', 'e.name': '山田太郎'}, {'b.id': 'BUG-001', 'b.title': 'ログイン画面がフリーズする', 'b.severity': 'critical', 'e.name': '山田太郎'}]
```

**回答:**

* BUG-094: APIゲートウェイのSSL証明書の有効期限が切れそう (担当: 藤田恵美)
* BUG-043: APIキーがログに平文で出力される (担当: 藤田恵美)

| 指標 | 値 |
|------|-----|
| 回答時間 | 160.00 秒 |
| 入力トークン | 27 |
| 出力トークン | 1 |

## Q2. v1.1リリースをブロックしているバグが属するモジュールのプロジェクト名を教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.1'})-[:BELONGS_TO]->(p:Project)
WITH b, p
MATCH (b)-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p)
RETURN p.name AS projectName
```

**Cypher実行結果:**

```
[{'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}, {'projectName': 'ECサイトリニューアル'}]
```

**回答:**

該当するデータが見つかりませんでした

| 指標 | 値 |
|------|-----|
| 回答時間 | 123.36 秒 |
| 入力トークン | 30 |
| 出力トークン | 1 |

## Q3. ECサイトリニューアルプロジェクトのモジュールで発見されたバグのうち、Backendチームが担当しているものを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p:Project {name: 'ECサイトリニューアル'})
MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Backend'})
RETURN b.id, b.title, b.severity, e.name AS engineer
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-011', 'b.title': 'セッションが30分で切れる', 'b.severity': 'low', 'engineer': '山田太郎'}, {'b.id': 'BUG-003', 'b.title': 'パスワードリセットメールが届かない', 'b.severity': 'medium', 'engineer': '田中一郎'}, {'b.id': 'BUG-001', 'b.title': 'ログイン画面がフリーズする', 'b.severity': 'critical', 'engineer': '山田太郎'}, {'b.id': 'BUG-030', 'b.title': 'ユーザー登録時にメールアドレスの重複チェックが失敗する', 'b.severity': 'high', 'engineer': '山田太郎'}, {'b.id': 'BUG-046', 'b.title': 'Backendチームのビルド時間が10分を超える', 'b.severity': 'medium', 'engineer': '村田さくら'}, {'b.id': 'BUG-064', 'b.title': '商品の在庫数がリアルタイムに反映されない', 'b.severity': 'high', 'engineer': '田中一郎'}, {'b.id': 'BUG-047', 'b.title': 'ユニットテストのカバレッジが60%を下回る', 'b.severity': 'medium', 'engineer': '林美里'}, {'b.id': 'BUG-013', 'b.title': '決済完了メールが二重送信される', 'b.severity': 'high', 'engineer': '田中一郎'}, {'b.id': 'BUG-081', 'b.title': 'Backendのメモリ使用量が時間で増加する', 'b.severity': 'high', 'engineer': '林美里'}, {'b.id': 'BUG-021', 'b.title': '決済時に在庫チェックが行われない', 'b.severity': 'critical', 'engineer': '山田太郎'}, {'b.id': 'BUG-004', 'b.title': 'クレジットカード決済がタイムアウトする', 'b.severity': 'critical', 'engineer': '山田太郎'}, {'b.id': 'BUG-029', 'b.title': 'データベース接続プールが枯渇する', 'b.severity': 'critical', 'engineer': '田中一郎'}, {'b.id': 'BUG-065', 'b.title': '決済後のカート内容が残る', 'b.severity': 'medium', 'engineer': '村田さくら'}, {'b.id': 'BUG-052', 'b.title': '決済APIのタイムアウト設定が短すぎる', 'b.severity': 'high', 'engineer': '村田さくら'}, {'b.id': 'BUG-006', 'b.title': 'カートに追加後に金額がずれる', 'b.severity': 'high', 'engineer': '田中一郎'}, {'b.id': 'BUG-100', 'b.title': '決済モジュールの負荷試験で10%のリクエストが失敗する', 'b.severity': 'critical', 'engineer': '山田太郎'}]
```

**回答:**

Backendチームが担当しているバグは以下の通りです。

* BUG-046: Backendチームのビルド時間が10分を超える
* BUG-081: Backendのメモリ使用量が時間で増加する

| 指標 | 値 |
|------|-----|
| 回答時間 | 174.73 秒 |
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
| 回答時間 | 123.11 秒 |
| 入力トークン | 28 |
| 出力トークン | 1 |

## Q5. モバイルアプリ開発プロジェクトのv1.0リリースをブロックしているバグの担当エンジニアが所属するチームを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.0'})-[:BELONGS_TO]->(p:Project {name: 'モバイルアプリ開発'})
OPTIONAL MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
RETURN t.name AS team, e.name AS engineer
```

**Cypher実行結果:**

```
[{'team': 'Mobile', 'engineer': '加藤誠'}, {'team': 'Mobile', 'engineer': '加藤誠'}, {'team': 'DevOps', 'engineer': '中村大輔'}, {'team': 'Mobile', 'engineer': '坂本竜一'}, {'team': 'Mobile', 'engineer': '佐藤美咲'}, {'team': 'Mobile', 'engineer': '坂本竜一'}, {'team': 'Mobile', 'engineer': '加藤誠'}, {'team': 'Mobile', 'engineer': '山本香織'}, {'team': 'Mobile', 'engineer': '佐藤美咲'}]
```

**回答:**

モバイルアプリ開発プロジェクトのv1.0リリースをブロックしているバグの担当エンジニアが所属するチームは**Mobile**です。

| 指標 | 値 |
|------|-----|
| 回答時間 | 130.26 秒 |
| 入力トークン | 35 |
| 出力トークン | 1 |
