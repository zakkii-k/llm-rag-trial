# 実行レポート — multihop_medium_qwen-small

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-01 23:13:01 |
| シナリオ | multihop_medium_qwen-small |
| モード | graphrag |
| モデル | qwen2.5-coder:7b |
| データソース | data/medium |
| クエリ数 | 5 |
| 合計回答時間 | 268.67 秒 |
| 合計トークン（入力） | 279 |
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
| 回答時間 | 66.74 秒 |
| 入力トークン | 48 |
| 出力トークン | 1 |

## Q2. v1.1リリースをブロックしているバグが属するモジュールのプロジェクト名を教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.1'})-[:BELONGS_TO]->(p:Project)
RETURN p.name AS project_name
```

**Cypher実行結果:**

```
[{'project_name': 'ECサイトリニューアル'}, {'project_name': 'ECサイトリニューアル'}, {'project_name': 'ECサイトリニューアル'}, {'project_name': 'ECサイトリニューアル'}, {'project_name': 'ECサイトリニューアル'}, {'project_name': 'ECサイトリニューアル'}, {'project_name': 'ECサイトリニューアル'}, {'project_name': 'ECサイトリニューアル'}, {'project_name': 'ECサイトリニューアル'}, {'project_name': 'ECサイトリニューアル'}, {'project_name': 'ECサイトリニューアル'}, {'project_name': 'ECサイトリニューアル'}, {'project_name': 'ECサイトリニューアル'}, {'project_name': 'ECサイトリニューアル'}, {'project_name': 'ECサイトリニューアル'}, {'project_name': 'ECサイトリニューアル'}, {'project_name': 'ECサイトリニューアル'}, {'project_name': 'ECサイトリニューアル'}, {'project_name': 'ECサイトリニューアル'}, {'project_name': 'ECサイトリニューアル'}, {'project_name': 'ECサイトリニューアル'}, {'project_name': 'ECサイトリニューアル'}, {'project_name': 'ECサイトリニューアル'}, {'project_name': 'ECサイトリニューアル'}]
```

**回答:**

v1.1リリースをブロックしているバグが属するモジュールのプロジェクト名は「ECサイトリニューアル」です。

| 指標 | 値 |
|------|-----|
| 回答時間 | 42.32 秒 |
| 入力トークン | 55 |
| 出力トークン | 1 |

## Q3. ECサイトリニューアルプロジェクトのモジュールで発見されたバグのうち、Backendチームが担当しているものを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p:Project {name: 'ECサイトリニューアル'})
WITH b, m, p
MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Backend'})
RETURN b.id, b.title, b.severity, e.name AS engineer, m.name AS module
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-011', 'b.title': 'セッションが30分で切れる', 'b.severity': 'low', 'engineer': '山田太郎', 'module': '認証モジュール'}, {'b.id': 'BUG-003', 'b.title': 'パスワードリセットメールが届かない', 'b.severity': 'medium', 'engineer': '田中一郎', 'module': '認証モジュール'}, {'b.id': 'BUG-001', 'b.title': 'ログイン画面がフリーズする', 'b.severity': 'critical', 'engineer': '山田太郎', 'module': '認証モジュール'}, {'b.id': 'BUG-030', 'b.title': 'ユーザー登録時にメールアドレスの重複チェックが失敗する', 'b.severity': 'high', 'engineer': '山田太郎', 'module': '認証モジュール'}, {'b.id': 'BUG-046', 'b.title': 'Backendチームのビルド時間が10分を超える', 'b.severity': 'medium', 'engineer': '村田さくら', 'module': '認証モジュール'}, {'b.id': 'BUG-064', 'b.title': '商品の在庫数がリアルタイムに反映されない', 'b.severity': 'high', 'engineer': '田中一郎', 'module': '商品カタログ'}, {'b.id': 'BUG-047', 'b.title': 'ユニットテストのカバレッジが60%を下回る', 'b.severity': 'medium', 'engineer': '林美里', 'module': '決済モジュール'}, {'b.id': 'BUG-013', 'b.title': '決済完了メールが二重送信される', 'b.severity': 'high', 'engineer': '田中一郎', 'module': '決済モジュール'}, {'b.id': 'BUG-081', 'b.title': 'Backendのメモリ使用量が時間で増加する', 'b.severity': 'high', 'engineer': '林美里', 'module': '決済モジュール'}, {'b.id': 'BUG-021', 'b.title': '決済時に在庫チェックが行われない', 'b.severity': 'critical', 'engineer': '山田太郎', 'module': '決済モジュール'}, {'b.id': 'BUG-004', 'b.title': 'クレジットカード決済がタイムアウトする', 'b.severity': 'critical', 'engineer': '山田太郎', 'module': '決済モジュール'}, {'b.id': 'BUG-029', 'b.title': 'データベース接続プールが枯渇する', 'b.severity': 'critical', 'engineer': '田中一郎', 'module': '決済モジュール'}, {'b.id': 'BUG-065', 'b.title': '決済後のカート内容が残る', 'b.severity': 'medium', 'engineer': '村田さくら', 'module': '決済モジュール'}, {'b.id': 'BUG-052', 'b.title': '決済APIのタイムアウト設定が短すぎる', 'b.severity': 'high', 'engineer': '村田さくら', 'module': '決済モジュール'}, {'b.id': 'BUG-006', 'b.title': 'カートに追加後に金額がずれる', 'b.severity': 'high', 'engineer': '田中一郎', 'module': '決済モジュール'}, {'b.id': 'BUG-100', 'b.title': '決済モジュールの負荷試験で10%のリクエストが失敗する', 'b.severity': 'critical', 'engineer': '山田太郎', 'module': '決済モジュール'}]
```

**回答:**

Backendチームが担当しているバグは以下の通りです：

1. **BUG-046: Backendチームのビルド時間が10分を超える**
   - モジュール：認証モジュール
   - 重要度：中程度

2. **BUG-081: Backendのメモリ使用量が時間で増加する**
   - モジュール：決済モジュール
   - 重要度：高め

| 指標 | 値 |
|------|-----|
| 回答時間 | 67.52 秒 |
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

各部署ごとのcriticalバグ件数は以下の通りです。

- Engineering: 11個
- Data: 5個
- Security: 4個
- Infrastructure: 2個

| 指標 | 値 |
|------|-----|
| 回答時間 | 38.29 秒 |
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

加藤誠が担当しているバグのうち、モバイルアプリ開発プロジェクトのv1.0リリースをブロックしていると推測されます。これらのバグは「Mobile」チームに所属しています。

したがって、モバイルアプリ開発プロジェクトのv1.0リリースをブロックしているバグの担当エンジニアが所属するチームは「Mobile」です。

| 指標 | 値 |
|------|-----|
| 回答時間 | 53.80 秒 |
| 入力トークン | 64 |
| 出力トークン | 1 |
