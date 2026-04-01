# 実行レポート — A_simple

| 項目 | 値 |
|------|-----|
| 実行日時 | 2026-04-01 10:37:20 |
| シナリオ | A_simple |
| モード | graphrag |
| モデル | llama3.2 |
| データソース | data/small |
| クエリ数 | 5 |
| 合計回答時間 | 35.41 秒 |
| 合計トークン（入力） | 165 |
| 合計トークン（出力） | 4 |

---

## Q1. criticalなオープンバグは何件ありますか？

**エラー:** {neo4j_code: Neo.ClientError.Statement.SyntaxError} {message: Invalid input '(': expected an identifier (line 1, column 13 (offset: 12))
"WITH Bug AS ("
             ^} {gql_status: 50N42} {gql_status_description: error: general processing exception - unexpected error. Invalid input '(': expected an identifier (line 1, column 13 (offset: 12))
"WITH Bug AS ("
             ^}

## Q2. highのバグを一覧で教えてください。

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {severity: 'high'})
RETURN b.id, b.title, b.severity
```

**Cypher実行結果:**

```
[{'b.id': 'BUG-002', 'b.title': '検索結果が0件になる', 'b.severity': 'high'}]
```

**回答:**

Searching for bugs with severity 'high' results in 1 issue.

{'b.id': 'BUG-002', 'b.title': '検索結果が0件になる', 'b.severity': 'high'}

| 指標 | 値 |
|------|-----|
| 回答時間 | 9.69 秒 |
| 入力トークン | 36 |
| 出力トークン | 1 |

## Q3. 解決済み（resolved）のバグのタイトルを教えてください。

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {status: 'resolved'})
RETURN b.title
```

**Cypher実行結果:**

```
[{'b.title': 'パスワードリセットメールが届かない'}]
```

**回答:**

パスワードリセットメールが届かない

| 指標 | 値 |
|------|-----|
| 回答時間 | 8.05 秒 |
| 入力トークン | 43 |
| 出力トークン | 1 |

## Q4. 山田太郎が担当しているバグのタイトルを教えてください。

**生成Cypherクエリ:**

```cypher
MATCH (b:Bug {id: "XXX"})-[:ASSIGNED_TO]->(e:Engineer)
WHERE e.name = "山田太郎"
RETURN b.title
```

**Cypher実行結果:**

```
[]
```

**回答:**

I don't have any information about the bug titles that 山田太郎 (Taro Yamada) is handling.

| 指標 | 値 |
|------|-----|
| 回答時間 | 9.08 秒 |
| 入力トークン | 42 |
| 出力トークン | 1 |

## Q5. ECサイトリニューアルプロジェクトのステータスを教えてください。

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

I don't have any additional information about ECサイトリニューアルプロジェクト's status.

| 指標 | 値 |
|------|-----|
| 回答時間 | 8.59 秒 |
| 入力トークン | 44 |
| 出力トークン | 1 |
