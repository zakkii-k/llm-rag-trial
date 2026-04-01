# 実行レポート — medium_small_qwen-large

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-01 23:40:29 |
| シナリオ | medium_small_qwen-large |
| モード | graphrag |
| モデル | qwen2.5-coder:14b |
| データソース | data/small |
| クエリ数 | 5 |
| 合計回答時間 | 500.84 秒 |
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

Backendチームのエンジニアが担当しているオープンなバグは以下の通りです：

- ID: BUG-081, タイトル: Backendのメモリ使用量が時間で増加する, 優先度: 高
- ID: BUG-047, タイトル: ユニットテストのカバレッジが60%を下回る, 優先度: 中

これらのバグは林美里エンジニアが担当しています。

| 指標 | 値 |
|------|-----|
| 回答時間 | 108.53 秒 |
| 入力トークン | 46 |
| 出力トークン | 1 |

## Q2. 認証モジュールで発見されたバグの担当者名を教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:FOUND_IN]->(m:Module {name: '認証モジュール'})-[:PART_OF]->(p:Project)
OPTIONAL MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)
RETURN b.id, b.title, e.name AS assignee
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-011', 'b.title': 'セッションが30分で切れる', 'assignee': '山田太郎'}, {'b.id': 'BUG-003', 'b.title': 'パスワードリセットメールが届かない', 'assignee': '田中一郎'}, {'b.id': 'BUG-044', 'b.title': 'セッションフィクセーション攻撃が可能', 'assignee': '松本剛'}, {'b.id': 'BUG-063', 'b.title': 'ユーザープロフィール画像のアップロードが失敗する', 'assignee': '渡辺恵'}, {'b.id': 'BUG-017', 'b.title': 'ログアウト後もセッションが残る', 'assignee': '中村大輔'}, {'b.id': 'BUG-001', 'b.title': 'ログイン画面がフリーズする', 'assignee': '山田太郎'}, {'b.id': 'BUG-041', 'b.title': 'SQLインジェクションの脆弱性が検出された', 'assignee': '松本剛'}, {'b.id': 'BUG-026', 'b.title': 'CI/CDパイプラインが失敗する', 'assignee': '中村大輔'}, {'b.id': 'BUG-019', 'b.title': 'パスワード変更後に自動ログアウトしない', 'assignee': '小林直子'}, {'b.id': 'BUG-030', 'b.title': 'ユーザー登録時にメールアドレスの重複チェックが失敗する', 'assignee': '山田太郎'}, {'b.id': 'BUG-046', 'b.title': 'Backendチームのビルド時間が10分を超える', 'assignee': '村田さくら'}]
```

**回答:**

以下のバグが認証モジュールに関連しています：

1. セッションが30分で切れる (担当者: 山田太郎)
2. パスワードリセットメールが届かない (担当者: 田中一郎)
3. セッションフィクセーション攻撃が可能 (担当者: 松本剛)
4. ログアウト後もセッションが残る (担当者: 中村大輔)
5. ログイン画面がフリーズする (担当者: 山田太郎)
6. SQLインジェクションの脆弱性が検出された (担当者: 松本剛)

これらのバグは認証モジュールに関連していると思われます。

| 指標 | 値 |
|------|-----|
| 回答時間 | 111.21 秒 |
| 入力トークン | 50 |
| 出力トークン | 1 |

## Q3. 決済モジュールに関連するcriticalバグは誰が担当していますか？

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {severity: 'critical'})-[:FOUND_IN]->(m:Module {name: '決済'})
OPTIONAL MATCH (b)-[:ASSIGNED_TO]->(e:Engineer)
RETURN b.id, b.title, e.name AS assignee
```

**Cypher実行結果:**

```
[]
```

**回答:**

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 65.63 秒 |
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

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 135.10 秒 |
| 入力トークン | 52 |
| 出力トークン | 1 |

## Q5. FrontendチームとBackendチームのバグ件数を比較してください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Frontend'})
RETURN 'Frontend' AS team, count(b) AS bug_count

UNION ALL

MATCH (b:Bug)-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team {name: 'Backend'})
RETURN 'Backend' AS team, count(b) AS bug_count
```

**Cypher実行結果:**

```
[{'team': 'Frontend', 'bug_count': 11}, {'team': 'Backend', 'bug_count': 16}]
```

**回答:**

バックエンドチームの方がフロントエンドチームよりもバグ件数が多いです。バックエンドチームのバグ件数は16件、フロントエンドチームのバグ件数は11件です。

| 指標 | 値 |
|------|-----|
| 回答時間 | 80.37 秒 |
| 入力トークン | 44 |
| 出力トークン | 1 |
