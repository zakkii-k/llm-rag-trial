# 実行レポート — multihop_large_qwen-large

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-02 00:39:11 |
| シナリオ | multihop_large_qwen-large |
| モード | graphrag |
| モデル | qwen2.5-coder:14b |
| データソース | data/large |
| クエリ数 | 5 |
| 合計回答時間 | 494.24 秒 |
| 合計トークン（入力） | 279 |
| 合計トークン（出力） | 5 |

---

## Q1. Engineering部署のエンジニアが担当しているcriticalなオープンバグを全て教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {severity: 'critical', status: 'open'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)-[:BELONGS_TO]->(d:Department {name: 'Engineering'})
RETURN b.id, b.title, b.severity
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-094', 'b.title': 'APIゲートウェイのSSL証明書の有効期限が切れそう', 'b.severity': 'critical'}, {'b.id': 'BUG-043', 'b.title': 'APIキーがログに平文で出力される', 'b.severity': 'critical'}, {'b.id': 'BUG-038', 'b.title': '通知サービスでiOS/Android両方に二重送信される', 'b.severity': 'critical'}, {'b.id': 'BUG-083', 'b.title': 'MobileチームのCI環境でコードサインのキーがExpireしている', 'b.severity': 'critical'}, {'b.id': 'BUG-096', 'b.title': 'Androidのアプリ内購入フローが失敗する', 'b.severity': 'critical'}, {'b.id': 'BUG-007', 'b.title': 'iOSアプリが起動時にクラッシュする', 'b.severity': 'critical'}, {'b.id': 'BUG-029', 'b.title': 'データベース接続プールが枯渇する', 'b.severity': 'critical'}, {'b.id': 'BUG-021', 'b.title': '決済時に在庫チェックが行われない', 'b.severity': 'critical'}, {'b.id': 'BUG-100', 'b.title': '決済モジュールの負荷試験で10%のリクエストが失敗する', 'b.severity': 'critical'}, {'b.id': 'BUG-004', 'b.title': 'クレジットカード決済がタイムアウトする', 'b.severity': 'critical'}, {'b.id': 'BUG-001', 'b.title': 'ログイン画面がフリーズする', 'b.severity': 'critical'}]
```

**回答:**

Engineering部署のエンジニアが担当しているcriticalなオープンバグを以下に示します：

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

これらのバグはすべてcriticalの severity で、Engineering部署のエンジニアに対応することが推奨されます。

| 指標 | 値 |
|------|-----|
| 回答時間 | 136.79 秒 |
| 入力トークン | 48 |
| 出力トークン | 1 |

## Q2. v1.1リリースをブロックしているバグが属するモジュールのプロジェクト名を教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.1'})-[:BELONGS_TO]->(p:Project)
OPTIONAL MATCH (b)-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p)
RETURN p.name AS project_name, m.name AS module_name
ORDER BY project_name, module_name
```

**Cypher実行結果:**

```
[{'project_name': 'ECサイトリニューアル', 'module_name': 'APIゲートウェイ'}, {'project_name': 'ECサイトリニューアル', 'module_name': 'APIゲートウェイ'}, {'project_name': 'ECサイトリニューアル', 'module_name': 'APIゲートウェイ'}, {'project_name': 'ECサイトリニューアル', 'module_name': 'APIゲートウェイ'}, {'project_name': 'ECサイトリニューアル', 'module_name': 'APIゲートウェイ'}, {'project_name': 'ECサイトリニューアル', 'module_name': '商品カタログ'}, {'project_name': 'ECサイトリニューアル', 'module_name': '商品カタログ'}, {'project_name': 'ECサイトリニューアル', 'module_name': '商品カタログ'}, {'project_name': 'ECサイトリニューアル', 'module_name': '商品カタログ'}, {'project_name': 'ECサイトリニューアル', 'module_name': '商品カタログ'}, {'project_name': 'ECサイトリニューアル', 'module_name': '検索モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': '決済モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': '決済モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': '決済モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': '決済モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': '決済モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': '決済モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': '決済モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': '決済モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': '認証モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': '認証モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': '認証モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': '認証モジュール'}, {'project_name': 'ECサイトリニューアル', 'module_name': '認証モジュール'}]
```

**回答:**

v1.1リリースをブロックしているバグが属するモジュールのプロジェクト名は「ECサイトリニューアル」です。

| 指標 | 値 |
|------|-----|
| 回答時間 | 97.93 秒 |
| 入力トークン | 55 |
| 出力トークン | 1 |

## Q3. ECサイトリニューアルプロジェクトのモジュールで発見されたバグのうち、Backendチームが担当しているものを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p:Project {name: 'ECサイトリニューアル'}),
      (b)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Backend'})
RETURN b.id, b.title, b.severity, m.name AS module
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-011', 'b.title': 'セッションが30分で切れる', 'b.severity': 'low', 'module': '認証モジュール'}, {'b.id': 'BUG-003', 'b.title': 'パスワードリセットメールが届かない', 'b.severity': 'medium', 'module': '認証モジュール'}, {'b.id': 'BUG-001', 'b.title': 'ログイン画面がフリーズする', 'b.severity': 'critical', 'module': '認証モジュール'}, {'b.id': 'BUG-030', 'b.title': 'ユーザー登録時にメールアドレスの重複チェックが失敗する', 'b.severity': 'high', 'module': '認証モジュール'}, {'b.id': 'BUG-046', 'b.title': 'Backendチームのビルド時間が10分を超える', 'b.severity': 'medium', 'module': '認証モジュール'}, {'b.id': 'BUG-064', 'b.title': '商品の在庫数がリアルタイムに反映されない', 'b.severity': 'high', 'module': '商品カタログ'}, {'b.id': 'BUG-047', 'b.title': 'ユニットテストのカバレッジが60%を下回る', 'b.severity': 'medium', 'module': '決済モジュール'}, {'b.id': 'BUG-013', 'b.title': '決済完了メールが二重送信される', 'b.severity': 'high', 'module': '決済モジュール'}, {'b.id': 'BUG-081', 'b.title': 'Backendのメモリ使用量が時間で増加する', 'b.severity': 'high', 'module': '決済モジュール'}, {'b.id': 'BUG-021', 'b.title': '決済時に在庫チェックが行われない', 'b.severity': 'critical', 'module': '決済モジュール'}, {'b.id': 'BUG-004', 'b.title': 'クレジットカード決済がタイムアウトする', 'b.severity': 'critical', 'module': '決済モジュール'}, {'b.id': 'BUG-029', 'b.title': 'データベース接続プールが枯渇する', 'b.severity': 'critical', 'module': '決済モジュール'}, {'b.id': 'BUG-065', 'b.title': '決済後のカート内容が残る', 'b.severity': 'medium', 'module': '決済モジュール'}, {'b.id': 'BUG-052', 'b.title': '決済APIのタイムアウト設定が短すぎる', 'b.severity': 'high', 'module': '決済モジュール'}, {'b.id': 'BUG-006', 'b.title': 'カートに追加後に金額がずれる', 'b.severity': 'high', 'module': '決済モジュール'}, {'b.id': 'BUG-100', 'b.title': '決済モジュールの負荷試験で10%のリクエストが失敗する', 'b.severity': 'critical', 'module': '決済モジュール'}]
```

**回答:**

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 104.26 秒 |
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

以下が質問に対する回答です：

Engineering部署：11件
Data部署：5件
Security部署：4件
Infrastructure部署：2件

この結果は、criticalバグを担当しているエンジニアが所属する各部署ごとのバグ件数を示しています。

| 指標 | 値 |
|------|-----|
| 回答時間 | 77.49 秒 |
| 入力トークン | 52 |
| 出力トークン | 1 |

## Q5. モバイルアプリ開発プロジェクトのv1.0リリースをブロックしているバグの担当エンジニアが所属するチームを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.0'})-[:BELONGS_TO]->(p:Project {name: 'モバイルアプリ開発'}),
      (b)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
RETURN DISTINCT t.name AS team
```

**Cypher実行結果:**

```
[{'team': 'Mobile'}, {'team': 'DevOps'}]
```

**回答:**

モバイルアプリ開発プロジェクトのv1.0リリースをブロックしているバグの担当エンジニアが所属するチームは「Mobile」および「DevOps」です。

| 指標 | 値 |
|------|-----|
| 回答時間 | 77.77 秒 |
| 入力トークン | 64 |
| 出力トークン | 1 |
