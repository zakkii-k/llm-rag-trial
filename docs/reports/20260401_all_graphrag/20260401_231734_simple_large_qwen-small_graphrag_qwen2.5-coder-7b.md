# 実行レポート — simple_large_qwen-small

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-01 23:17:34 |
| シナリオ | simple_large_qwen-small |
| モード | graphrag |
| モデル | qwen2.5-coder:7b |
| データソース | data/large |
| クエリ数 | 5 |
| 合計回答時間 | 302.03 秒 |
| 合計トークン（入力） | 214 |
| 合計トークン（出力） | 5 |

---

## Q1. criticalなオープンバグは何件ありますか？

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {status: 'open', severity: 'critical'})
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
| 回答時間 | 31.55 秒 |
| 入力トークン | 39 |
| 出力トークン | 1 |

## Q2. highのバグを一覧で教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {severity: 'high'})
RETURN b.id, b.title, b.status, b.severity
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-002', 'b.title': '検索結果が0件になる', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-005', 'b.title': '商品画像が表示されない', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-006', 'b.title': 'カートに追加後に金額がずれる', 'b.status': 'in_progress', 'b.severity': 'high'}, {'b.id': 'BUG-009', 'b.title': '管理者がユーザー削除できない', 'b.status': 'resolved', 'b.severity': 'high'}, {'b.id': 'BUG-013', 'b.title': '決済完了メールが二重送信される', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-018', 'b.title': 'Androidアプリのメモリリーク', 'b.status': 'in_progress', 'b.severity': 'high'}, {'b.id': 'BUG-025', 'b.title': '商品レビューが投稿できない', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-026', 'b.title': 'CI/CDパイプラインが失敗する', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-028', 'b.title': 'APIのレートリミットが機能しない', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-030', 'b.title': 'ユーザー登録時にメールアドレスの重複チェックが失敗する', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-032', 'b.title': 'データウェアハウスのクエリが5分以上かかる', 'b.status': 'in_progress', 'b.severity': 'high'}, {'b.id': 'BUG-033', 'b.title': '推薦アルゴリズムが同じ商品を繰り返す', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-036', 'b.title': 'アクセスログの集計が日付をまたぐと失敗する', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-037', 'b.title': 'APIゲートウェイの認証トークン検証が遅い', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-042', 'b.title': 'XSS脆弱性がコメント投稿フォームに存在', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-044', 'b.title': 'セッションフィクセーション攻撃が可能', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-052', 'b.title': '決済APIのタイムアウト設定が短すぎる', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-055', 'b.title': '管理者のパスワード有効期限が設定されていない', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-056', 'b.title': 'データウェアハウスへのETLが冪等でない', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-060', 'b.title': 'APIゲートウェイのキャッシュが正しくパージされない', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-061', 'b.title': 'Frontend画面の初期ロードが5秒以上かかる', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-064', 'b.title': '商品の在庫数がリアルタイムに反映されない', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-069', 'b.title': '月次レポートの合計値が合わない', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-070', 'b.title': 'データパイプラインの監視アラートが機能しない', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-073', 'b.title': '脆弱性スキャナがCVEデータベースを更新しない', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-075', 'b.title': 'APIゲートウェイでリクエストが稀にドロップする', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-077', 'b.title': 'DataEngineeringチームのジョブスケジューラが重複起動する', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-078', 'b.title': '機械学習のバッチ推論が週末にスキップされる', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-080', 'b.title': 'プラットフォームチームのKubernetesポッドが頻繁に再起動する', 'b.status': 'in_progress', 'b.severity': 'high'}, {'b.id': 'BUG-081', 'b.title': 'Backendのメモリ使用量が時間で増加する', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-088', 'b.title': 'MLモデルの予測に偏り（バイアス）が検出された', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-090', 'b.title': 'プラットフォームのオートスケールが機能しない', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-092', 'b.title': '推薦APIのレスポンスタイムが2秒を超える', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-093', 'b.title': '脆弱性スキャンレポートが暗号化されていない', 'b.status': 'open', 'b.severity': 'high'}, {'b.id': 'BUG-098', 'b.title': '管理者画面の操作ログが記録されていない', 'b.status': 'open', 'b.severity': 'high'}]
```

**回答:**

以下のバグは severity が high で、なおかつ status が open または in_progress のものとして一覧されています。

1. BUG-002: 検索結果が0件になる
2. BUG-005: 商品画像が表示されない
3. BUG-006: カートに追加後に金額がずれる
4. BUG-009: 管理者がユーザー削除できない
5. BUG-013: 決済完了メールが二重送信される
6. BUG-018: Androidアプリのメモリリーク
7. BUG-025: 商品レビューが投稿できない
8. BUG-026: CI/CDパイプラインが失敗する
9. BUG-028: APIのレートリミットが機能しない
10. BUG-030: ユーザー登録時にメールアドレスの重複チェックが失敗する
11. BUG-032: データウェアハウスのクエリが5分以上かかる
12. BUG-033: 推薦アルゴリズムが同じ商品を繰り返す
13. BUG-036: アクセスログの集計が日付をまたぐと失敗する
14. BUG-037: APIゲートウェイの認証トークン検証が遅い
15. BUG-042: XSS脆弱性がコメント投稿フォームに存在
16. BUG-044: セッションフィクセーション攻撃が可能
17. BUG-052: 決済APIのタイムアウト設定が短すぎる
18. BUG-055: 管理者のパスワード有効期限が設定されていない
19. BUG-056: データウェアハウスへのETLが冪等でない
20. BUG-060: APIゲートウェイのキャッシュが正しくパージされない
21. BUG-061: Frontend画面の初期ロードが5秒以上かかる
22. BUG-064: 商品の在庫数がリアルタイムに反映されない
23. BUG-069: 月次レポートの合計値が合わない
24. BUG-070: データパイプラインの監視アラートが機能しない
25. BUG-073: 脆弱性スキャナがCVEデータベースを更新しない
26. BUG-075: APIゲートウェイでリクエストが稀にドロップする
27. BUG-077: DataEngineeringチームのジョブスケジューラが重複起動する
28. BUG-078: 機械学習のバッチ推論が週末にスキップされる
29. BUG-080: プラットフォームチームのKubernetesポッドが頻繁に再起動する
30. BUG-081: Backendのメモリ使用量が時間で増加する
31. BUG-088: MLモデルの予測に偏り（バイアス）が検出された
32. BUG-090: プラットフォームのオートスケールが機能しない
33. BUG-092: 推薦APIのレスポンスタイムが2秒を超える
34. BUG-093: 脆弱性スキャンレポートが暗号化されていない
35. BUG-098: 管理者画面の操作ログが記録されていない

| 指標 | 値 |
|------|-----|
| 回答時間 | 156.97 秒 |
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

以下の解決済み（resolved）のバグのタイトルは、以下の通りです。

1. パスワードリセットメールが届かない
2. 管理者がユーザー削除できない
3. 管理画面のページネーションが壊れている

| 指標 | 値 |
|------|-----|
| 回答時間 | 38.18 秒 |
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

山田太郎が担当しているバグのタイトルは以下の通りです：

1. 決済時に在庫チェックが行われない
2. 決済モジュールの負荷試験で10%のリクエストが失敗する
3. ユーザー登録時にメールアドレスの重複チェックが失敗する
4. クレジットカード決済がタイムアウトする
5. ログイン画面がフリーズする
6. セッションが30分で切れる

| 指標 | 値 |
|------|-----|
| 回答時間 | 44.57 秒 |
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
| 回答時間 | 30.76 秒 |
| 入力トークン | 45 |
| 出力トークン | 1 |
