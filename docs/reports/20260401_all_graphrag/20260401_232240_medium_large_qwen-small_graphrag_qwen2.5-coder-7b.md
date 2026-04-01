# 実行レポート — medium_large_qwen-small

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-01 23:22:40 |
| シナリオ | medium_large_qwen-small |
| モード | graphrag |
| モデル | qwen2.5-coder:7b |
| データソース | data/large |
| クエリ数 | 5 |
| 合計回答時間 | 307.93 秒 |
| 合計トークン（入力） | 240 |
| 合計トークン（出力） | 5 |

---

## Q1. Backendチームのエンジニアが担当しているオープンなバグを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {status: 'open'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Backend'})
RETURN b.id, b.title, b.severity, e.name AS engineer
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-081', 'b.title': 'Backendのメモリ使用量が時間で増加する', 'b.severity': 'high', 'engineer': '林美里'}, {'b.id': 'BUG-047', 'b.title': 'ユニットテストのカバレッジが60%を下回る', 'b.severity': 'medium', 'engineer': '林美里'}, {'b.id': 'BUG-052', 'b.title': '決済APIのタイムアウト設定が短すぎる', 'b.severity': 'high', 'engineer': '村田さくら'}, {'b.id': 'BUG-065', 'b.title': '決済後のカート内容が残る', 'b.severity': 'medium', 'engineer': '村田さくら'}, {'b.id': 'BUG-029', 'b.title': 'データベース接続プールが枯渇する', 'b.severity': 'critical', 'engineer': '田中一郎'}, {'b.id': 'BUG-013', 'b.title': '決済完了メールが二重送信される', 'b.severity': 'high', 'engineer': '田中一郎'}, {'b.id': 'BUG-064', 'b.title': '商品の在庫数がリアルタイムに反映されない', 'b.severity': 'high', 'engineer': '田中一郎'}, {'b.id': 'BUG-021', 'b.title': '決済時に在庫チェックが行われない', 'b.severity': 'critical', 'engineer': '山田太郎'}, {'b.id': 'BUG-100', 'b.title': '決済モジュールの負荷試験で10%のリクエストが失敗する', 'b.severity': 'critical', 'engineer': '山田太郎'}, {'b.id': 'BUG-030', 'b.title': 'ユーザー登録時にメールアドレスの重複チェックが失敗する', 'b.severity': 'high', 'engineer': '山田太郎'}, {'b.id': 'BUG-004', 'b.title': 'クレジットカード決済がタイムアウトする', 'b.severity': 'critical', 'engineer': '山田太郎'}, {'b.id': 'BUG-001', 'b.title': 'ログイン画面がフリーズする', 'b.severity': 'critical', 'engineer': '山田太郎'}, {'b.id': 'BUG-011', 'b.title': 'セッションが30分で切れる', 'b.severity': 'low', 'engineer': '山田太郎'}]
```

**回答:**

Backendチームのエンジニアが担当しているオープンなバグを以下にまとめます：

1. **BUG-081**: バックエンドのメモリ使用量が時間で増加する (優先度: 高)
2. **BUG-047**: ユニットテストのカバレッジが60%を下回る (優先度: 中)
3. **BUG-052**: 決済APIのタイムアウト設定が短すぎる (優先度: 高)
4. **BUG-065**: 決済後のカート内容が残る (優先度: 中)
5. **BUG-029**: データベース接続プールが枯渇する (優先度: 緊急)
6. **BUG-013**: 決済完了メールが二重送信される (優先度: 高)
7. **BUG-064**: 商品の在庫数がリアルタイムに反映されない (優先度: 高)
8. **BUG-021**: 決済時に在庫チェックが行われない (優先度: 緊急)
9. **BUG-100**: 決済モジュールの負荷試験で10%のリクエストが失敗する (優先度: 練急)
10. **BUG-030**: ユーザー登録時にメールアドレスの重複チェックが失敗する (優先度: 高)
11. **BUG-004**: クレジットカード決済がタイムアウトする (優先度: 練急)
12. **BUG-001**: ログイン画面がフリーズする (優先度: 練急)
13. **BUG-011**: セッションが30分で切れる (優先度: 低)

これらのバグはBackendチームのエンジニアが担当しており、一部は緊急性が高いです。

| 指標 | 値 |
|------|-----|
| 回答時間 | 91.16 秒 |
| 入力トークン | 46 |
| 出力トークン | 1 |

## Q2. 認証モジュールで発見されたバグの担当者名を教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:FOUND_IN]->(m:Module {name: '認証モジュール'})-[:ASSIGNED_TO]->(e:Engineer)
RETURN e.name AS assignee
```

**Cypher実行結果:**

```
[]
```

**回答:**

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 31.58 秒 |
| 入力トークン | 50 |
| 出力トークン | 1 |

## Q3. 決済モジュールに関連するcriticalバグは誰が担当していますか？

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {severity: 'critical'})-[:FOUND_IN]->(m:Module {name: '決済モジュール'})
RETURN b.id, b.title, b.severity, b.status, m.name AS module
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-021', 'b.title': '決済時に在庫チェックが行われない', 'b.severity': 'critical', 'b.status': 'open', 'module': '決済モジュール'}, {'b.id': 'BUG-004', 'b.title': 'クレジットカード決済がタイムアウトする', 'b.severity': 'critical', 'b.status': 'open', 'module': '決済モジュール'}, {'b.id': 'BUG-029', 'b.title': 'データベース接続プールが枯渇する', 'b.severity': 'critical', 'b.status': 'open', 'module': '決済モジュール'}, {'b.id': 'BUG-100', 'b.title': '決済モジュールの負荷試験で10%のリクエストが失敗する', 'b.severity': 'critical', 'b.status': 'open', 'module': '決済モジュール'}]
```

**回答:**

担当者が見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 36.73 秒 |
| 入力トークン | 48 |
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

v1.1リリースをブロックしているバグの一覧と担当者如下です：

1. **BUG-041**: SQLインジェクションの脆弱性が検出された - 松本剛 (Security)
2. **BUG-030**: ユーザー登録時にメールアドレスの重複チェックが失敗する - 山田太郎 (Backend)
3. **BUG-094**: APIゲートウェイのSSL証明書の有効期限が切れそう - 藤田恵美 (API)
4. **BUG-026**: CI/CDパイプラインが失敗する - 中村大輔 (DevOps)
5. **BUG-100**: 決済モジュールの負荷試験で10%のリクエストが失敗する - 山田太郎 (Backend)

これらのバグはv1.1リリースをブロックしている可能性があります。

| 指標 | 値 |
|------|-----|
| 回答時間 | 93.97 秒 |
| 入力トークン | 52 |
| 出力トークン | 1 |

## Q5. FrontendチームとBackendチームのバグ件数を比較してください。

**試行回数: 2回**

### 試行1（失敗）

```cypher
MATCH (b:Bug)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team {name IN ['Frontend', 'Backend']})
RETURN t.name AS team, count(b) AS bug_count
ORDER BY bug_count DESC
```

**エラー:** {neo4j_code: Neo.ClientError.Statement.SyntaxError} {message: Invalid input '{': expected a parameter (line 1, column 66 (offset: 65))
"MATCH (b:Bug)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team {name IN ['Frontend', 'Backend']})"
                                                                  ^} {gql_status: 50N42} {gql_status_description: error: general processing exception - unexpected error. Invalid input '{': expected a parameter (line 1, column 66 (offset: 65))
"MATCH (b:Bug)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team {name IN ['Frontend', 'Backend']})"
                                                                  ^}

### 試行2（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)
WHERE t.name IN ['Frontend', 'Backend']
RETURN t.name AS team, count(b) AS bug_count
ORDER BY bug_count DESC
```

**Cypher実行結果:**

```
[{'team': 'Backend', 'bug_count': 16}, {'team': 'Frontend', 'bug_count': 11}]
```

**回答:**

Frontendチームは11件、Backendチームは16件のバグがあります。 Backendチームの方がFrontendチームよりも多くのバグを抱えています。

| 指標 | 値 |
|------|-----|
| 回答時間 | 54.49 秒 |
| 入力トークン | 44 |
| 出力トークン | 1 |
