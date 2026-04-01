# 実行レポート — multihop_medium_large

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-02 01:56:55 |
| シナリオ | multihop_medium_large |
| モード | graphrag |
| モデル | gemma2:27b |
| データソース | data/medium |
| クエリ数 | 5 |
| 合計回答時間 | 663.10 秒 |
| 合計トークン（入力） | 152 |
| 合計トークン（出力） | 5 |

---

## Q1. Engineering部署のエンジニアが担当しているcriticalなオープンバグを全て教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {status: 'open', severity: 'critical'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)-[:BELONGS_TO]->(d:Department {name: 'Engineering'})
RETURN b.id, b.title, e.name
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-094', 'b.title': 'APIゲートウェイのSSL証明書の有効期限が切れそう', 'e.name': '藤田恵美'}, {'b.id': 'BUG-043', 'b.title': 'APIキーがログに平文で出力される', 'e.name': '藤田恵美'}, {'b.id': 'BUG-038', 'b.title': '通知サービスでiOS/Android両方に二重送信される', 'e.name': '山本香織'}, {'b.id': 'BUG-083', 'b.title': 'MobileチームのCI環境でコードサインのキーがExpireしている', 'e.name': '坂本竜一'}, {'b.id': 'BUG-096', 'b.title': 'Androidのアプリ内購入フローが失敗する', 'e.name': '加藤誠'}, {'b.id': 'BUG-007', 'b.title': 'iOSアプリが起動時にクラッシュする', 'e.name': '佐藤美咲'}, {'b.id': 'BUG-029', 'b.title': 'データベース接続プールが枯渇する', 'e.name': '田中一郎'}, {'b.id': 'BUG-021', 'b.title': '決済時に在庫チェックが行われない', 'e.name': '山田太郎'}, {'b.id': 'BUG-100', 'b.title': '決済モジュールの負荷試験で10%のリクエストが失敗する', 'e.name': '山田太郎'}, {'b.id': 'BUG-004', 'b.title': 'クレジットカード決済がタイムアウトする', 'e.name': '山田太郎'}, {'b.id': 'BUG-001', 'b.title': 'ログイン画面がフリーズする', 'e.name': '山田太郎'}]
```

**回答:**

Engineering部署のエンジニアが担当しているcriticalなオープンバグは以下の通りです。

* BUG-094: APIゲートウェイのSSL証明書の有効期限が切れそう (担当: 藤田恵美)
* BUG-043: APIキーがログに平文で出力される (担当: 藤田恵美)

| 指標 | 値 |
|------|-----|
| 回答時間 | 156.76 秒 |
| 入力トークン | 27 |
| 出力トークン | 1 |

## Q2. v1.1リリースをブロックしているバグが属するモジュールのプロジェクト名を教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.1'})-[:BELONGS_TO]->(p:Project)
OPTIONAL MATCH (b)-[:FOUND_IN]->(m:Module) 
RETURN p.name AS project_name, m.name AS module_name
```

**Cypher実行結果:**

```
[{'project_name': 'ECサイトリニューアル', 'module_name': '認証モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': '認証モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': 'APIゲートウェイ'}, {'project_name': 'ECサイトリニューアル', 'module_name': '検索モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': '商品カタログ'}, {'project_name': 'ECサイトリニューアル', 'module_name': '決済モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': 'APIゲートウェイ'}, {'project_name': 'ECサイトリニューアル', 'module_name': '決済モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': '認証モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': '決済モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': '決済モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': '認証モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': '認証モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': 'APIゲートウェイ'}, {'project_name': 'ECサイトリニューアル', 'module_name': 'APIゲートウェイ'}, {'project_name': 'ECサイトリニューアル', 'module_name': '決済モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': '決済モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': '商品カタログ'}, {'project_name': 'ECサイトリニューアル', 'module_name': '決済モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': '商品カタログ'}, {'project_name': 'ECサイトリニューアル', 'module_name': '商品カタログ'}, {'project_name': 'ECサイトリニューアル', 'module_name': '決済モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': 'APIゲートウェイ'}, {'project_name': 'ECサイトリニューアル', 'module_name': '商品カタログ'}]
```

**回答:**

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 141.32 秒 |
| 入力トークン | 30 |
| 出力トークン | 1 |

## Q3. ECサイトリニューアルプロジェクトのモジュールで発見されたバグのうち、Backendチームが担当しているものを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p:Project {name: 'ECサイトリニューアル'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Backend'})
RETURN b.id, b.title, b.severity, b.status, m.name AS module, e.name AS engineer
```

**Cypher実行結果:**

```
[]
```

**回答:**

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 115.38 秒 |
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
| 回答時間 | 121.36 秒 |
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
| 回答時間 | 128.28 秒 |
| 入力トークン | 35 |
| 出力トークン | 1 |
