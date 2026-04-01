# 実行レポート — medium_medium_small

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-01 22:33:25 |
| シナリオ | medium_medium_small |
| モード | graphrag |
| モデル | llama3.2 |
| データソース | data/medium |
| クエリ数 | 5 |
| 合計回答時間 | 153.47 秒 |
| 合計トークン（入力） | 222 |
| 合計トークン（出力） | 5 |

---

## Q1. Backendチームのエンジニアが担当しているオープンなバグを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {status: 'open'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)-[:BELONGS_TO]->(d:Department {name: 'Backend'})
RETURN b.id, b.title, b.severity, e.name
```

**Cypher実行結果:**

```
[]
```

**回答:**

該当するデータが見つかりません。

| 指標 | 値 |
|------|-----|
| 回答時間 | 15.19 秒 |
| 入力トークン | 45 |
| 出力トークン | 1 |

## Q2. 認証モジュールで発見されたバグの担当者名を教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {FOUND_IN: '認証モジュール'})-[:ASSIGNED_TO]->(e:Engineer)
RETURN e.name AS assignee
```

**Cypher実行結果:**

```
[]
```

**回答:**

対応するデータが見つられませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 17.35 秒 |
| 入力トークン | 45 |
| 出力トークン | 1 |

## Q3. 決済モジュールに関連するcriticalバグは誰が担当していますか？

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {severity: 'critical'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)-[:BELONGS_TO]->(d:Department)
WHERE d.name = 'Payment' OR t.name = 'Payment'
RETURN e.id AS engineer_id, e.name AS assignee
```

**Cypher実行結果:**

```
[]
```

**回答:**

該当するデータが見つられませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 25.73 秒 |
| 入力トークン | 43 |
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

v1.1リリースをブロックしているバグの一覧と担当者は、以下のようになっています。

* BUG-041: 松本剛（セキュアティチーム）
* BUG-030: 山田太郎（バックエンドチーム）
* BUG-094:藤田恵美（APIチーム）
* BUG-002:鈴木花子（フロントエンドチーム）
* BUG-005:渡辺恵（フロントエンドチーム）
* BUG-004:山田太郎（バックエンドチーム）
* BUG-043:藤田恵美（APIチーム）
* BUG-052:村田さくら（バックエンドチーム）
* BUG-001:山田太郎（バックエンドチーム）
* BUG-013:田中一郎（バックエンドチーム）
* BUG-081:林美里（バックエンドチーム）
* BUG-026:中村大輔（デボップスチーム）
* BUG-017:中村大輔（デボップスチーム）
* BUG-060:前田麗（APIチーム）
* BUG-075:藤田恵美（APIチーム）
* BUG-100:山田太郎（バックエンドチーム）
* BUG-006:田中一郎（バックエンドチーム）
* BUG-064:田中一郎（バックエンドチーム）
* BUG-021:山田太郎（バックエンドチーム）
* BUG-061:長谷川翼（フロントエンドチーム）
* BUG-025:渡辺恵（フロントエンドチーム）
* BUG-029:田中一郎（バックエンドチーム）
* BUG-037:藤田恵美（APIチーム）
* BUG-042:橋本慎太郎（セキュアティチーム）

ただし、v1.1リリースをブロックしているバグが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 50.33 秒 |
| 入力トークン | 48 |
| 出力トークン | 1 |

## Q5. FrontendチームとBackendチームのバグ件数を比較してください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {status: 'open'})-[:ASSIGNED_TO]->(e:Engineer)-[:MEMBER_OF]->(t:Team)-[:BELONGS_TO]->(d:Department {name: 'Frontend'})
RETURN b.id, b.title, b.severity, e.name
```

**Cypher実行結果:**

```
[]
```

**回答:**

該当するデータが見つかりませんでした。

| 指標 | 値 |
|------|-----|
| 回答時間 | 44.87 秒 |
| 入力トークン | 41 |
| 出力トークン | 1 |
