# 実行レポート — multihop_large_gemini-pro

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-03 12:32:49 |
| シナリオ | multihop_large_gemini-pro |
| モード | graphrag |
| モデル | gemini-3-flash-preview |
| データソース | data/large |
| クエリ数 | 5 |
| 合計回答時間 | 175.80 秒 |
| 合計トークン（入力） | 3884 |
| 合計トークン（出力） | 1208 |

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

Engineering部署のエンジニアが担当しているcriticalなオープンバグは以下の通りです。

- BUG-094: APIゲートウェイのSSL証明書の有効期限が切れそう（担当者：藤田恵美）
- BUG-043: APIキーがログに平文で出力される（担当者：藤田恵美）
- BUG-038: 通知サービスでiOS/Android両方に二重送信される（担当者：山本香織）
- BUG-083: MobileチームのCI環境でコードサインのキーがExpireしている（担当者：坂本竜一）
- BUG-096: Androidのアプリ内購入フローが失敗する（担当者：加藤誠）
- BUG-007: iOSアプリが起動時にクラッシュする（担当者：佐藤美咲）
- BUG-029: データベース接続プールが枯渇する（担当者：田中一郎）
- BUG-021: 決済時に在庫チェックが行われない（担当者：山田太郎）
- BUG-100: 決済モジュールの負荷試験で10%のリクエストが失敗する（担当者：山田太郎）
- BUG-004: クレジットカード決済がタイムアウトする（担当者：山田太郎）
- BUG-001: ログイン画面がフリーズする（担当者：山田太郎）

| 指標 | 値 |
|------|-----|
| 回答時間 | 10.72 秒 |
| 入力トークン | 844 |
| 出力トークン | 304 |

## Q2. v1.1リリースをブロックしているバグが属するモジュールのプロジェクト名を教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.1'})
MATCH (b)-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p:Project)
RETURN p.name
```

**Cypher実行結果:**

```
[{'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}, {'p.name': 'ECサイトリニューアル'}]
```

**回答:**

v1.1リリースをブロックしているバグが属するモジュールのプロジェクト名は以下の通りです。

- ECサイトリニューアル

| 指標 | 値 |
|------|-----|
| 回答時間 | 35.74 秒 |
| 入力トークン | 625 |
| 出力トークン | 29 |

## Q3. ECサイトリニューアルプロジェクトのモジュールで発見されたバグのうち、Backendチームが担当しているものを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p:Project {name: 'ECサイトリニューアル'})
MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Backend'})
RETURN b.id, b.title, b.severity, b.status, m.name AS module, e.name AS engineer
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-011', 'b.title': 'セッションが30分で切れる', 'b.severity': 'low', 'b.status': 'open', 'module': '認証モジュール', 'engineer': '山田太郎'}, {'b.id': 'BUG-003', 'b.title': 'パスワードリセットメールが届かない', 'b.severity': 'medium', 'b.status': 'resolved', 'module': '認証モジュール', 'engineer': '田中一郎'}, {'b.id': 'BUG-001', 'b.title': 'ログイン画面がフリーズする', 'b.severity': 'critical', 'b.status': 'open', 'module': '認証モジュール', 'engineer': '山田太郎'}, {'b.id': 'BUG-030', 'b.title': 'ユーザー登録時にメールアドレスの重複チェックが失敗する', 'b.severity': 'high', 'b.status': 'open', 'module': '認証モジュール', 'engineer': '山田太郎'}, {'b.id': 'BUG-046', 'b.title': 'Backendチームのビルド時間が10分を超える', 'b.severity': 'medium', 'b.status': 'in_progress', 'module': '認証モジュール', 'engineer': '村田さくら'}, {'b.id': 'BUG-064', 'b.title': '商品の在庫数がリアルタイムに反映されない', 'b.severity': 'high', 'b.status': 'open', 'module': '商品カタログ', 'engineer': '田中一郎'}, {'b.id': 'BUG-047', 'b.title': 'ユニットテストのカバレッジが60%を下回る', 'b.severity': 'medium', 'b.status': 'open', 'module': '決済モジュール', 'engineer': '林美里'}, {'b.id': 'BUG-013', 'b.title': '決済完了メールが二重送信される', 'b.severity': 'high', 'b.status': 'open', 'module': '決済モジュール', 'engineer': '田中一郎'}, {'b.id': 'BUG-081', 'b.title': 'Backendのメモリ使用量が時間で増加する', 'b.severity': 'high', 'b.status': 'open', 'module': '決済モジュール', 'engineer': '林美里'}, {'b.id': 'BUG-021', 'b.title': '決済時に在庫チェックが行われない', 'b.severity': 'critical', 'b.status': 'open', 'module': '決済モジュール', 'engineer': '山田太郎'}, {'b.id': 'BUG-004', 'b.title': 'クレジットカード決済がタイムアウトする', 'b.severity': 'critical', 'b.status': 'open', 'module': '決済モジュール', 'engineer': '山田太郎'}, {'b.id': 'BUG-029', 'b.title': 'データベース接続プールが枯渇する', 'b.severity': 'critical', 'b.status': 'open', 'module': '決済モジュール', 'engineer': '田中一郎'}, {'b.id': 'BUG-065', 'b.title': '決済後のカート内容が残る', 'b.severity': 'medium', 'b.status': 'open', 'module': '決済モジュール', 'engineer': '村田さくら'}, {'b.id': 'BUG-052', 'b.title': '決済APIのタイムアウト設定が短すぎる', 'b.severity': 'high', 'b.status': 'open', 'module': '決済モジュール', 'engineer': '村田さくら'}, {'b.id': 'BUG-006', 'b.title': 'カートに追加後に金額がずれる', 'b.severity': 'high', 'b.status': 'in_progress', 'module': '決済モジュール', 'engineer': '田中一郎'}, {'b.id': 'BUG-100', 'b.title': '決済モジュールの負荷試験で10%のリクエストが失敗する', 'b.severity': 'critical', 'b.status': 'open', 'module': '決済モジュール', 'engineer': '山田太郎'}]
```

**回答:**

ECサイトリニューアルプロジェクトのモジュールにおいて、Backendチームが担当しているバグは以下の通りです。

- BUG-011「セッションが30分で切れる」（モジュール：認証モジュール、担当者：山田太郎）
- BUG-003「パスワードリセットメールが届かない」（モジュール：認証モジュール、担当者：田中一郎）
- BUG-001「ログイン画面がフリーズする」（モジュール：認証モジュール、担当者：山田太郎）
- BUG-030「ユーザー登録時にメールアドレスの重複チェックが失敗する」（モジュール：認証モジュール、担当者：山田太郎）
- BUG-046「Backendチームのビルド時間が10分を超える」（モジュール：認証モジュール、担当者：村田さくら）
- BUG-064「商品の在庫数がリアルタイムに反映されない」（モジュール：商品カタログ、担当者：田中一郎）
- BUG-047「ユニットテストのカバレッジが60%を下回る」（モジュール：決済モジュール、担当者：林美里）
- BUG-013「決済完了メールが二重送信される」（モジュール：決済モジュール、担当者：田中一郎）
- BUG-081「Backendのメモリ使用量が時間で増加する」（モジュール：決済モジュール、担当者：林美里）
- BUG-021「決済時に在庫チェックが行われない」（モジュール：決済モジュール、担当者：山田太郎）
- BUG-004「クレジットカード決済がタイムアウトする」（モジュール：決済モジュール、担当者：山田太郎）
- BUG-029「データベース接続プールが枯渇する」（モジュール：決済モジュール、担当者：田中一郎）
- BUG-065「決済後のカート内容が残る」（モジュール：決済モジュール、担当者：村田さくら）
- BUG-052「決済APIのタイムアウト設定が短すぎる」（モジュール：決済モジュール、担当者：村田さくら）
- BUG-006「カートに追加後に金額がずれる」（モジュール：決済モジュール、担当者：田中一郎）
- BUG-100「決済モジュールの負荷試験で10%のリクエストが失敗する」（モジュール：決済モジュール、担当者：山田太郎）

| 指標 | 値 |
|------|-----|
| 回答時間 | 34.31 秒 |
| 入力トークン | 1291 |
| 出力トークン | 521 |

## Q4. criticalバグを担当しているエンジニアが所属する部署ごとのバグ件数を教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {severity: 'critical'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)-[:BELONGS_TO]->(d:Department)
RETURN d.name, count(b) AS bug_count
```

**Cypher実行結果:**

```
[{'d.name': 'Engineering', 'bug_count': 11}, {'d.name': 'Infrastructure', 'bug_count': 2}, {'d.name': 'Data', 'bug_count': 5}, {'d.name': 'Security', 'bug_count': 4}]
```

**回答:**

criticalバグを担当しているエンジニアが所属する部署ごとのバグ件数は以下の通りです。

- Engineering：11件
- Infrastructure：2件
- Data：5件
- Security：4件

| 指標 | 値 |
|------|-----|
| 回答時間 | 51.13 秒 |
| 入力トークン | 400 |
| 出力トークン | 46 |

## Q5. モバイルアプリ開発プロジェクトのv1.0リリースをブロックしているバグの担当エンジニアが所属するチームを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.0'})-[:BELONGS_TO]->(p:Project {name: 'モバイルアプリ開発'})
MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
RETURN b.id, b.title, e.name AS engineer, t.name AS team
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-008', 'b.title': 'Androidで通知が届かない', 'engineer': '加藤誠', 'team': 'Mobile'}, {'b.id': 'BUG-096', 'b.title': 'Androidのアプリ内購入フローが失敗する', 'engineer': '加藤誠', 'team': 'Mobile'}, {'b.id': 'BUG-024', 'b.title': '管理者ロールの権限チェックが不正', 'engineer': '中村大輔', 'team': 'DevOps'}, {'b.id': 'BUG-053', 'b.title': 'iOSアプリのバッテリー消費が激しい', 'engineer': '坂本竜一', 'team': 'Mobile'}, {'b.id': 'BUG-014', 'b.title': 'iOSプッシュ通知のディープリンクが動作しない', 'engineer': '佐藤美咲', 'team': 'Mobile'}, {'b.id': 'BUG-083', 'b.title': 'MobileチームのCI環境でコードサインのキーがExpireしている', 'engineer': '坂本竜一', 'team': 'Mobile'}, {'b.id': 'BUG-018', 'b.title': 'Androidアプリのメモリリーク', 'engineer': '加藤誠', 'team': 'Mobile'}, {'b.id': 'BUG-038', 'b.title': '通知サービスでiOS/Android両方に二重送信される', 'engineer': '山本香織', 'team': 'Mobile'}, {'b.id': 'BUG-007', 'b.title': 'iOSアプリが起動時にクラッシュする', 'engineer': '佐藤美咲', 'team': 'Mobile'}]
```

**回答:**

モバイルアプリ開発プロジェクトのv1.0リリースをブロックしているバグの担当エンジニアと、その所属チームは以下の通りです。

- バグ BUG-008「Androidで通知が届かない」：担当者 加藤誠（Mobileチーム）
- バグ BUG-096「Androidのアプリ内購入フローが失敗する」：担当者 加藤誠（Mobileチーム）
- バグ BUG-024「管理者ロールの権限チェックが不正」：担当者 中村大輔（DevOpsチーム）
- バグ BUG-053「iOSアプリのバッテリー消費が激しい」：担当者 坂本竜一（Mobileチーム）
- バグ BUG-014「iOSプッシュ通知의ディープリンクが動作しない」：担当者 佐藤美咲（Mobileチーム）
- バグ BUG-083「MobileチームのCI環境でコードサインのキーがExpireしている」：担当者 坂本竜一（Mobileチーム）
- バグ BUG-018「Androidアプリのメモリリーク」：担当者 加藤誠（Mobileチーム）
- バグ BUG-038「通知サービスでiOS/Android両方に二重送信される」：担当者 山本香織（Mobileチーム）
- バグ BUG-007「iOSアプリが起動時にクラッシュする」：担当者 佐藤美咲（Mobileチーム）

| 指標 | 値 |
|------|-----|
| 回答時間 | 43.90 秒 |
| 入力トークン | 724 |
| 出力トークン | 308 |
