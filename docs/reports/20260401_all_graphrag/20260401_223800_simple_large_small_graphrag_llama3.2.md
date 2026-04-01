# 実行レポート — simple_large_small

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-01 22:38:00 |
| シナリオ | simple_large_small |
| モード | graphrag |
| モデル | llama3.2 |
| データソース | data/large |
| クエリ数 | 5 |
| 合計回答時間 | 157.59 秒 |
| 合計トークン（入力） | 203 |
| 合計トークン（出力） | 5 |

---

## Q1. criticalなオープンバグは何件ありますか？

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {status: 'open', severity: 'critical'})
RETURN count(*) AS cnt
```

**Cypher実行結果:**

```
[{'cnt': 22}]
```

**回答:**

この Cypher実行結果は、オープンバグの数を取得するためのクエリですが、結果には数字が示されていないため、結果は空になります。

したがって、答えは:"該当するデータが見つかりませんでした"です。

| 指標 | 値 |
|------|-----|
| 回答時間 | 16.40 秒 |
| 入力トークン | 38 |
| 出力トークン | 1 |

## Q2. highのバグを一覧で教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {severity: 'high'})
RETURN b.id, b.title, b.severity, b.status
ORDER BY b.severity DESC
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-002', 'b.title': '検索結果が0件になる', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-005', 'b.title': '商品画像が表示されない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-006', 'b.title': 'カートに追加後に金額がずれる', 'b.severity': 'high', 'b.status': 'in_progress'}, {'b.id': 'BUG-009', 'b.title': '管理者がユーザー削除できない', 'b.severity': 'high', 'b.status': 'resolved'}, {'b.id': 'BUG-013', 'b.title': '決済完了メールが二重送信される', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-018', 'b.title': 'Androidアプリのメモリリーク', 'b.severity': 'high', 'b.status': 'in_progress'}, {'b.id': 'BUG-025', 'b.title': '商品レビューが投稿できない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-026', 'b.title': 'CI/CDパイプラインが失敗する', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-028', 'b.title': 'APIのレートリミットが機能しない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-030', 'b.title': 'ユーザー登録時にメールアドレスの重複チェックが失敗する', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-032', 'b.title': 'データウェアハウスのクエリが5分以上かかる', 'b.severity': 'high', 'b.status': 'in_progress'}, {'b.id': 'BUG-033', 'b.title': '推薦アルゴリズムが同じ商品を繰り返す', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-036', 'b.title': 'アクセスログの集計が日付をまたぐと失敗する', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-037', 'b.title': 'APIゲートウェイの認証トークン検証が遅い', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-042', 'b.title': 'XSS脆弱性がコメント投稿フォームに存在', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-044', 'b.title': 'セッションフィクセーション攻撃が可能', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-052', 'b.title': '決済APIのタイムアウト設定が短すぎる', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-055', 'b.title': '管理者のパスワード有効期限が設定されていない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-056', 'b.title': 'データウェアハウスへのETLが冪等でない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-060', 'b.title': 'APIゲートウェイのキャッシュが正しくパージされない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-061', 'b.title': 'Frontend画面の初期ロードが5秒以上かかる', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-064', 'b.title': '商品の在庫数がリアルタイムに反映されない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-069', 'b.title': '月次レポートの合計値が合わない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-070', 'b.title': 'データパイプラインの監視アラートが機能しない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-073', 'b.title': '脆弱性スキャナがCVEデータベースを更新しない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-075', 'b.title': 'APIゲートウェイでリクエストが稀にドロップする', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-077', 'b.title': 'DataEngineeringチームのジョブスケジューラが重複起動する', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-078', 'b.title': '機械学習のバッチ推論が週末にスキップされる', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-080', 'b.title': 'プラットフォームチームのKubernetesポッドが頻繁に再起動する', 'b.severity': 'high', 'b.status': 'in_progress'}, {'b.id': 'BUG-081', 'b.title': 'Backendのメモリ使用量が時間で増加する', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-088', 'b.title': 'MLモデルの予測に偏り（バイアス）が検出された', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-090', 'b.title': 'プラットフォームのオートスケールが機能しない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-092', 'b.title': '推薦APIのレスポンスタイムが2秒を超える', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-093', 'b.title': '脆弱性スキャンレポートが暗号化されていない', 'b.severity': 'high', 'b.status': 'open'}, {'b.id': 'BUG-098', 'b.title': '管理者画面の操作ログが記録されていない', 'b.severity': 'high', 'b.status': 'open'}]
```

**回答:**

以下は「高優先度のバグ」の一覧です。

1. 検索結果が0件になる（BUG-002）
2. 商品画像が表示されない（BUG-005）
3. カートに追加後に金額がずれる（BUG-006）
4.管理者がユーザー削除できない（BUG-009）
5.決済完了メールが二重送信される（BUG-013）
6.Androidアプリのメモリリーク（BUG-018）
7.商品レビューが投稿できない（BUG-025）
8.CI/CDパイプラインが失敗する（BUG-026）
9.APIのレートリミットが機能しない（BUG-028）
10.ユーザー登録時にメールアドレスの重複チェックが失敗する（BUG-030）
11.データウェアハウスのクエリが5分以上かかる（BUG-032）
12.추천アルゴリズムが同じ商品を繰り返す（BUG-033）
13.アクセスログの集計が日付をまたぐと失敗する（BUG-036）
14.APIゲートウェイの認証トークン検証が遅い（BUG-037）
15.XSS脆弱性がコメント投稿フォームに存在（BUG-042）
16.セッションフィクセーション攻撃が可能（BUG-044）
17.決済APIのタイムアウト設定が短すぎる（BUG-052）
18.管理者のパスワード有効期限が設定されていない（BUG-055）
19.データウェアハウスへのETLが冪等でない（BUG-056）
20.APIゲートウェイのキャッシュが正しくパージされない（BUG-060）
21.Frontend画面の初期ロードが5秒以上かかる（BUG-061）
22.商品の在庫数がリアルタイムに反映されない（BUG-064）
23.月次レポートの合計値が合わない（BUG-069）
24.データパイプラインの監視アラートが機能しない（BUG-070）
25.脆弱性スキャナがCVEデータベースを更新しない（BUG-073）
26.APIゲートウェイでリクエストが稀にドロップする（BUG-075）
27.DataEngineeringチームのジョブスケジューラが重複起動する（BUG-077）
28.機械学習のバッチ推論が週末にスキップされる（BUG-078）
29.プラットフォームチームのKubernetesポッドが頻繁に再起動する（BUG-080）
30.Backendのメモリ使用量が時間で増加する（BUG-081）
31.MLモデルの予測に偏り（バイアス）が検出された（BUG-088）
32.プラットフォームのオートスケールが機能しない（BUG-090）
33.推薦APIのレスポンスタイムが2秒を超える（BUG-092）
34.脆弱性スキャンレポートが暗号化されていない（BUG-093）
35.管理者画面の操作ログが記録されていない（BUG-098）

| 指標 | 値 |
|------|-----|
| 回答時間 | 79.62 秒 |
| 入力トークン | 36 |
| 出力トークン | 1 |

## Q3. 解決済み（resolved）のバグのタイトルを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {status: 'resolved'})
RETURN b.id, b.title
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-003', 'b.title': 'パスワードリセットメールが届かない'}, {'b.id': 'BUG-009', 'b.title': '管理者がユーザー削除できない'}, {'b.id': 'BUG-015', 'b.title': '管理画面のページネーションが壊れている'}]
```

**回答:**

解決済み（resolved）のバグのタイトルは以下のとおりです。

- BUG-003：パスワードリセットメールが届かない
- BUG-009：管理者がユーザー削除できない
- BUG-015：管理画面のページネーションが壊れている

| 指標 | 値 |
|------|-----|
| 回答時間 | 19.24 秒 |
| 入力トークン | 43 |
| 出力トークン | 1 |

## Q4. 山田太郎が担当しているバグのタイトルを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug)-[:ASSIGNED_TO]->(e:Engineer {name: '山田太郎'})
RETURN b.id, b.title
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-021', 'b.title': '決済時に在庫チェックが行われない'}, {'b.id': 'BUG-100', 'b.title': '決済モジュールの負荷試験で10%のリクエストが失敗する'}, {'b.id': 'BUG-030', 'b.title': 'ユーザー登録時にメールアドレスの重複チェックが失敗する'}, {'b.id': 'BUG-004', 'b.title': 'クレジットカード決済がタイムアウトする'}, {'b.id': 'BUG-001', 'b.title': 'ログイン画面がフリーズする'}, {'b.id': 'BUG-011', 'b.title': 'セッションが30分で切れる'}]
```

**回答:**

バグのタイトルは以下の通りです。

- BUG-021：決済時に在庫チェックが行われない
- BUG-100：決済モジュールの負荷試験で10%のリクエストが失敗する
- BUG-030：ユーザー登録時にメールアドレスの重複チェックが失敗する
- BUG-004：クレジットカード決済がタイムアウトする
- BUG-001：ログイン画面がフリーズする
- BUG-011：セッションが30分で切れる

| 指標 | 値 |
|------|-----|
| 回答時間 | 21.24 秒 |
| 入力トークン | 42 |
| 出力トークン | 1 |

## Q5. ECサイトリニューアルプロジェクトのステータスを教えてください。

**試行回数: 1回**

### 試行1（成功）

**生成Cypherクエリ:**

```cypher
MATCH (p:Project {name: 'ECサイトリニューアル'})-[:BELONGS_TO]->(r:Release)
RETURN r.status
```

**Cypher実行結果:**

```
[]
```

**回答:**

該当するデータが見つかりません。

| 指標 | 値 |
|------|-----|
| 回答時間 | 21.09 秒 |
| 入力トークン | 44 |
| 出力トークン | 1 |
