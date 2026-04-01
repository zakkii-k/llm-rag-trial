# 実行レポート — multihop_small_qwen-large

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-01 23:48:56 |
| シナリオ | multihop_small_qwen-large |
| モード | graphrag |
| モデル | qwen2.5-coder:14b |
| データソース | data/small |
| クエリ数 | 5 |
| 合計回答時間 | 550.70 秒 |
| 合計トークン（入力） | 279 |
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

Engineering部署のエンジニアが担当しているcriticalなオープンバグは以下の通りです：

1. **BUG-094**: APIゲートウェイのSSL証明書の有効期限が切れそう (担当: 藤田恵美)
2. **BUG-043**: APIキーがログに平文で出力される (担当: 藤田恵美)
3. **BUG-038**: 通知サービスでiOS/Android両方に二重送信される (担当: 山本香織)
4. **BUG-083**: MobileチームのCI環境でコードサインのキーがExpireしている (担当: 坂本竜一)
5. **BUG-096**: Androidのアプリ内購入フローが失敗する (担当: 加藤誠)
6. **BUG-007**: iOSアプリが起動時にクラッシュする (担当: 佐藤美咲)
7. **BUG-029**: データベース接続プールが枯渇する (担当: 田中一郎)
8. **BUG-021**: 決済時に在庫チェックが行われない (担当: 山田太郎)
9. **BUG-100**: 決済モジュールの負荷試験で10%のリクエストが失敗する (担当: 山田太郎)
10. **BUG-004**: クレジットカード決済がタイムアウトする (担当: 山田太郎)
11. **BUG-001**: ログイン画面がフリーズする (担当: 山田太郎)

| 指標 | 値 |
|------|-----|
| 回答時間 | 149.34 秒 |
| 入力トークン | 48 |
| 出力トークン | 1 |

## Q2. v1.1リリースをブロックしているバグが属するモジュールのプロジェクト名を教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.1'})-[:BELONGS_TO]->(p:Project)
OPTIONAL MATCH (b)-[:FOUND_IN]->(m:Module)
RETURN b.id, b.title, m.name AS module, p.name AS project
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-041', 'b.title': 'SQLインジェクションの脆弱性が検出された', 'module': '認証モジュール', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-030', 'b.title': 'ユーザー登録時にメールアドレスの重複チェックが失敗する', 'module': '認証モジュール', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-094', 'b.title': 'APIゲートウェイのSSL証明書の有効期限が切れそう', 'module': 'APIゲートウェイ', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-002', 'b.title': '検索結果が0件になる', 'module': '検索モジュール', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-005', 'b.title': '商品画像が表示されない', 'module': '商品カタログ', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-004', 'b.title': 'クレジットカード決済がタイムアウトする', 'module': '決済モジュール', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-043', 'b.title': 'APIキーがログに平文で出力される', 'module': 'APIゲートウェイ', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-052', 'b.title': '決済APIのタイムアウト設定が短すぎる', 'module': '決済モジュール', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-001', 'b.title': 'ログイン画面がフリーズする', 'module': '認証モジュール', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-013', 'b.title': '決済完了メールが二重送信される', 'module': '決済モジュール', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-081', 'b.title': 'Backendのメモリ使用量が時間で増加する', 'module': '決済モジュール', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-026', 'b.title': 'CI/CDパイプラインが失敗する', 'module': '認証モジュール', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-017', 'b.title': 'ログアウト後もセッションが残る', 'module': '認証モジュール', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-060', 'b.title': 'APIゲートウェイのキャッシュが正しくパージされない', 'module': 'APIゲートウェイ', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-075', 'b.title': 'APIゲートウェイでリクエストが稀にドロップする', 'module': 'APIゲートウェイ', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-100', 'b.title': '決済モジュールの負荷試験で10%のリクエストが失敗する', 'module': '決済モジュール', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-006', 'b.title': 'カートに追加後に金額がずれる', 'module': '決済モジュール', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-064', 'b.title': '商品の在庫数がリアルタイムに反映されない', 'module': '商品カタログ', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-021', 'b.title': '決済時に在庫チェックが行われない', 'module': '決済モジュール', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-061', 'b.title': 'Frontend画面の初期ロードが5秒以上かかる', 'module': '商品カタログ', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-025', 'b.title': '商品レビューが投稿できない', 'module': '商品カタログ', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-029', 'b.title': 'データベース接続プールが枯渇する', 'module': '決済モジュール', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-037', 'b.title': 'APIゲートウェイの認証トークン検証が遅い', 'module': 'APIゲートウェイ', 'project': 'ECサイトリニューアル'}, {'b.id': 'BUG-042', 'b.title': 'XSS脆弱性がコメント投稿フォームに存在', 'module': '商品カタログ', 'project': 'ECサイトリニューアル'}]
```

**回答:**

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 121.44 秒 |
| 入力トークン | 55 |
| 出力トークン | 1 |

## Q3. ECサイトリニューアルプロジェクトのモジュールで発見されたバグのうち、Backendチームが担当しているものを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:FOUND_IN]->(m:Module)-[:PART_OF]->(p:Project {name: 'ECサイトリニューアル'}),
      (b)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Backend'})
RETURN b.id, b.title, b.severity, e.name AS engineer
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-011', 'b.title': 'セッションが30分で切れる', 'b.severity': 'low', 'engineer': '山田太郎'}, {'b.id': 'BUG-003', 'b.title': 'パスワードリセットメールが届かない', 'b.severity': 'medium', 'engineer': '田中一郎'}, {'b.id': 'BUG-001', 'b.title': 'ログイン画面がフリーズする', 'b.severity': 'critical', 'engineer': '山田太郎'}, {'b.id': 'BUG-030', 'b.title': 'ユーザー登録時にメールアドレスの重複チェックが失敗する', 'b.severity': 'high', 'engineer': '山田太郎'}, {'b.id': 'BUG-046', 'b.title': 'Backendチームのビルド時間が10分を超える', 'b.severity': 'medium', 'engineer': '村田さくら'}, {'b.id': 'BUG-064', 'b.title': '商品の在庫数がリアルタイムに反映されない', 'b.severity': 'high', 'engineer': '田中一郎'}, {'b.id': 'BUG-047', 'b.title': 'ユニットテストのカバレッジが60%を下回る', 'b.severity': 'medium', 'engineer': '林美里'}, {'b.id': 'BUG-013', 'b.title': '決済完了メールが二重送信される', 'b.severity': 'high', 'engineer': '田中一郎'}, {'b.id': 'BUG-081', 'b.title': 'Backendのメモリ使用量が時間で増加する', 'b.severity': 'high', 'engineer': '林美里'}, {'b.id': 'BUG-021', 'b.title': '決済時に在庫チェックが行われない', 'b.severity': 'critical', 'engineer': '山田太郎'}, {'b.id': 'BUG-004', 'b.title': 'クレジットカード決済がタイムアウトする', 'b.severity': 'critical', 'engineer': '山田太郎'}, {'b.id': 'BUG-029', 'b.title': 'データベース接続プールが枯渇する', 'b.severity': 'critical', 'engineer': '田中一郎'}, {'b.id': 'BUG-065', 'b.title': '決済後のカート内容が残る', 'b.severity': 'medium', 'engineer': '村田さくら'}, {'b.id': 'BUG-052', 'b.title': '決済APIのタイムアウト設定が短すぎる', 'b.severity': 'high', 'engineer': '村田さくら'}, {'b.id': 'BUG-006', 'b.title': 'カートに追加後に金額がずれる', 'b.severity': 'high', 'engineer': '田中一郎'}, {'b.id': 'BUG-100', 'b.title': '決済モジュールの負荷試験で10%のリクエストが失敗する', 'b.severity': 'critical', 'engineer': '山田太郎'}]
```

**回答:**

Backendチームが担当しているバグは以下の通りです：

- BUG-046: Backendチームのビルド時間が10分を超える (重要度：中)
- BUG-052: 決済APIのタイムアウト設定が短すぎる (重要度：高)
- BUG-065: 決済後のカート内容が残る (重要度：中)

| 指標 | 値 |
|------|-----|
| 回答時間 | 116.67 秒 |
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

以下が、criticalバグを担当しているエンジニアが所属する部署ごとのバグ件数です：

- Engineering部署: 11件
- Data部署: 5件
- Security部署: 4件
- Infrastructure部署: 2件

この情報は、Cypherクエリの実行結果に基づいています。

| 指標 | 値 |
|------|-----|
| 回答時間 | 80.57 秒 |
| 入力トークン | 52 |
| 出力トークン | 1 |

## Q5. モバイルアプリ開発プロジェクトのv1.0リリースをブロックしているバグの担当エンジニアが所属するチームを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:BLOCKS]->(r:Release {version: 'v1.0'})-[:BELONGS_TO]->(p:Project {name: 'モバイルアプリ開発'})
OPTIONAL MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
RETURN e.name AS assignee, t.name AS team
```

**Cypher実行結果:**

```
[{'assignee': '加藤誠', 'team': 'Mobile'}, {'assignee': '加藤誠', 'team': 'Mobile'}, {'assignee': '中村大輔', 'team': 'DevOps'}, {'assignee': '坂本竜一', 'team': 'Mobile'}, {'assignee': '佐藤美咲', 'team': 'Mobile'}, {'assignee': '坂本竜一', 'team': 'Mobile'}, {'assignee': '加藤誠', 'team': 'Mobile'}, {'assignee': '山本香織', 'team': 'Mobile'}, {'assignee': '佐藤美咲', 'team': 'Mobile'}]
```

**回答:**

モバイルアプリ開発プロジェクトのv1.0リリースをブロックしているバグの担当エンジニアが所属するチームは「Mobile」です。

| 指標 | 値 |
|------|-----|
| 回答時間 | 82.68 秒 |
| 入力トークン | 64 |
| 出力トークン | 1 |
