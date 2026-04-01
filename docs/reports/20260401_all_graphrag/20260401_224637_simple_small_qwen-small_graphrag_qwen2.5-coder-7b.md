# 実行レポート — simple_small_qwen-small

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-01 22:46:37 |
| シナリオ | simple_small_qwen-small |
| モード | graphrag |
| モデル | qwen2.5-coder:7b |
| データソース | data/small |
| クエリ数 | 5 |
| 合計回答時間 | 263.99 秒 |
| 合計トークン（入力） | 214 |
| 合計トークン（出力） | 5 |

---

## Q1. criticalなオープンバグは何件ありますか？

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {severity: 'critical', status: 'open'})
RETURN count(b) AS critical_open_bug_count
```

**Cypher実行結果:**

```
[{'critical_open_bug_count': 22}]
```

**回答:**

22件のcriticalなオープンバグがあります。

| 指標 | 値 |
|------|-----|
| 回答時間 | 38.64 秒 |
| 入力トークン | 39 |
| 出力トークン | 1 |

## Q2. highのバグを一覧で教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {severity: 'high'})
RETURN b.id, b.title, b.status, b.assigned_to_name AS assigned_to
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-002', 'b.title': '検索結果が0件になる', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-005', 'b.title': '商品画像が表示されない', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-006', 'b.title': 'カートに追加後に金額がずれる', 'b.status': 'in_progress', 'assigned_to': None}, {'b.id': 'BUG-009', 'b.title': '管理者がユーザー削除できない', 'b.status': 'resolved', 'assigned_to': None}, {'b.id': 'BUG-013', 'b.title': '決済完了メールが二重送信される', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-018', 'b.title': 'Androidアプリのメモリリーク', 'b.status': 'in_progress', 'assigned_to': None}, {'b.id': 'BUG-025', 'b.title': '商品レビューが投稿できない', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-026', 'b.title': 'CI/CDパイプラインが失敗する', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-028', 'b.title': 'APIのレートリミットが機能しない', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-030', 'b.title': 'ユーザー登録時にメールアドレスの重複チェックが失敗する', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-032', 'b.title': 'データウェアハウスのクエリが5分以上かかる', 'b.status': 'in_progress', 'assigned_to': None}, {'b.id': 'BUG-033', 'b.title': '推薦アルゴリズムが同じ商品を繰り返す', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-036', 'b.title': 'アクセスログの集計が日付をまたぐと失敗する', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-037', 'b.title': 'APIゲートウェイの認証トークン検証が遅い', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-042', 'b.title': 'XSS脆弱性がコメント投稿フォームに存在', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-044', 'b.title': 'セッションフィクセーション攻撃が可能', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-052', 'b.title': '決済APIのタイムアウト設定が短すぎる', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-055', 'b.title': '管理者のパスワード有効期限が設定されていない', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-056', 'b.title': 'データウェアハウスへのETLが冪等でない', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-060', 'b.title': 'APIゲートウェイのキャッシュが正しくパージされない', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-061', 'b.title': 'Frontend画面の初期ロードが5秒以上かかる', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-064', 'b.title': '商品の在庫数がリアルタイムに反映されない', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-069', 'b.title': '月次レポートの合計値が合わない', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-070', 'b.title': 'データパイプラインの監視アラートが機能しない', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-073', 'b.title': '脆弱性スキャナがCVEデータベースを更新しない', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-075', 'b.title': 'APIゲートウェイでリクエストが稀にドロップする', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-077', 'b.title': 'DataEngineeringチームのジョブスケジューラが重複起動する', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-078', 'b.title': '機械学習のバッチ推論が週末にスキップされる', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-080', 'b.title': 'プラットフォームチームのKubernetesポッドが頻繁に再起動する', 'b.status': 'in_progress', 'assigned_to': None}, {'b.id': 'BUG-081', 'b.title': 'Backendのメモリ使用量が時間で増加する', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-088', 'b.title': 'MLモデルの予測に偏り（バイアス）が検出された', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-090', 'b.title': 'プラットフォームのオートスケールが機能しない', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-092', 'b.title': '推薦APIのレスポンスタイムが2秒を超える', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-093', 'b.title': '脆弱性スキャンレポートが暗号化されていない', 'b.status': 'open', 'assigned_to': None}, {'b.id': 'BUG-098', 'b.title': '管理者画面の操作ログが記録されていない', 'b.status': 'open', 'assigned_to': None}]
```

**回答:**

highのバグを一覧で教えてください。

結果が空の場合は「該当するデータが見つかりませんでした」と答えてください。

回答：

以下のhighのバグがあります。

1. BUG-002: 検索結果が0件になる
2. BUG-005: 商品画像が表示されない
3. BUG-006: カートに追加後に金額がずれる
4. BUG-013: 決済完了メールが二重送信される
5. BUG-018: Androidアプリのメモリリーク
6. BUG-022: ユーザーのパスワード有効期限が設定されていない
7. BUG-024: セッションフィクセーション攻撃が可能
8. BUG-031: APIのレートリミットが機能しない
9. BUG-036: アクセスログの集計が日付をまたぐと失敗する
10. BUG-042: XSS脆弱性がコメント投稿フォームに存在
11. BUG-050: 決済APIのタイムアウト設定が短すぎる
12. BUG-053: 管理者のパスワード有効期限が設定されていない
13. BUG-067: Frontend画面の初期ロードが5秒以上かかる
14. BUG-079: データパイプラインの監視アラートが機能しない
15. BUG-082: 機械学習のバッチ推論が週末にスキップされる
16. BUG-083: Backendのメモリ使用量が時間で増加する
17. BUG-089: MLモデルの予測に偏り（バイアス）が検出された
18. BUG-090: プラットフォームのオートスケールが機能しない
19. BUG-092: 推荐APIのレスポンスタイムが2秒を超える
20. BUG-095: 管理者画面の操作ログが記録されていない

| 指標 | 値 |
|------|-----|
| 回答時間 | 114.71 秒 |
| 入力トークン | 41 |
| 出力トークン | 1 |

## Q3. 解決済み（resolved）のバグのタイトルを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {status: 'resolved'})
RETURN b.title
```

**Cypher実行結果:**

```
[{'b.title': 'パスワードリセットメールが届かない'}, {'b.title': '管理者がユーザー削除できない'}, {'b.title': '管理画面のページネーションが壊れている'}]
```

**回答:**

解決済みのバグのタイトルは以下の通りです：

1. パスワードリセットメールが届かない
2. 管理者がユーザー削除できない
3. 管理画面のページネーションが壊れている

| 指標 | 値 |
|------|-----|
| 回答時間 | 34.04 秒 |
| 入力トークン | 45 |
| 出力トークン | 1 |

## Q4. 山田太郎が担当しているバグのタイトルを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:ASSIGNED_TO]->(e:Engineer {name: '山田太郎'})
RETURN b.title
```

**Cypher実行結果:**

```
[{'b.title': '決済時に在庫チェックが行われない'}, {'b.title': '決済モジュールの負荷試験で10%のリクエストが失敗する'}, {'b.title': 'ユーザー登録時にメールアドレスの重複チェックが失敗する'}, {'b.title': 'クレジットカード決済がタイムアウトする'}, {'b.title': 'ログイン画面がフリーズする'}, {'b.title': 'セッションが30分で切れる'}]
```

**回答:**

山田太郎が担当しているバグのタイトルは以下の通りです。

1. 決済時に在庫チェックが行われない
2. 決済モジュールの負荷試験で10%のリクエストが失敗する
3. ユーザー登録時にメールアドレスの重複チェックが失敗する
4. クレジットカード決済がタイムアウトする
5. ログイン画面がフリーズする
6. セッションが30分で切れる

| 指標 | 値 |
|------|-----|
| 回答時間 | 44.49 秒 |
| 入力トークン | 44 |
| 出力トークン | 1 |

## Q5. ECサイトリニューアルプロジェクトのステータスを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (p:Project {name: 'ECサイトリニューアル'})
RETURN p.status
```

**Cypher実行結果:**

```
[{'p.status': 'active'}]
```

**回答:**

ECサイトリニューアルプロジェクトのステータスは「active」です。

| 指標 | 値 |
|------|-----|
| 回答時間 | 32.11 秒 |
| 入力トークン | 45 |
| 出力トークン | 1 |
