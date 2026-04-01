# GraphRAG vs RAG 検証レビュー

実施日: 2026-04-01
検証環境: Docker (Neo4j 5.13, Ollama)、WSL2 (27GB RAM)

---

## 1. 検証概要

### 検証目的
- GraphRAG（Neo4j + Cypher自動生成）と ベクターRAG（ChromaDB + nomic-embed-text）の精度・速度・トークン量を比較する
- クエリ複雑度（1ホップ〜3ホップ）による差異を測定する
- モデルサイズ（llama3.2 3B vs gemma2:27b）による影響を比較する

### 検証シナリオ一覧

| シナリオ | クエリ種別 | データ | モデル | モード |
|---------|-----------|--------|--------|--------|
| A | シンプル（1ホップ） | small（3バグ、3エンジニア） | llama3.2 | GraphRAG / RAG |
| B | 中程度（2ホップ） | medium（30バグ、10エンジニア） | llama3.2 | GraphRAG / RAG |
| C | マルチホップ（3+ホップ） | large（100バグ、30エンジニア） | llama3.2 | GraphRAG / RAG |
| D | マルチホップ（3+ホップ） | large（100バグ、30エンジニア） | gemma2:27b | GraphRAG / RAG |

### 正誤判定基準

| 記号 | 意味 |
|------|------|
| ✅ | 正解（事実と一致） |
| ❌ | 不正解（誤った情報、または回答不能） |
| △ | 部分正解（一部正しい要素を含むが不完全） |

---

## 2. 正誤判定（根拠付き）

### シナリオA — シンプルクエリ / small data / llama3.2

<details>
<summary>期待値の根拠（small データから導出）</summary>

```
bugs.csv: BUG-001(critical,open,ENG-001), BUG-002(high,open,ENG-002), BUG-003(medium,resolved,ENG-003)
ENG-001 = 山田太郎 / ECサイトリニューアル status = active
```
</details>

| Q | 質問 | 正解 | GraphRAG | 判定 | RAG | 判定 |
|---|------|------|----------|------|-----|------|
| 1 | criticalなオープンバグは何件？ | **1件**（BUG-001） | Cypherエラー（`WITH Bug AS (`構文） | ❌ | 0件と回答（BUG-001を見落とし） | ❌ |
| 2 | highバグ一覧 | **BUG-002** 検索結果が0件になる | BUG-002を返した（ただし英語で説明） | △ | 架空のバグを列挙（MOD-001バグ等） | ❌ |
| 3 | resolvedバグのタイトル | **パスワードリセットメールが届かない** | 正解 | ✅ | 正解 | ✅ |
| 4 | 山田太郎担当バグ | **ログイン画面がフリーズする** | Cypher内に`{id: "XXX"}`プレースホルダが残存、空結果 | ❌ | 正解 | ✅ |
| 5 | ECサイトリニューアルのstatus | **active** | Cypherは正しくactiveを取得したが回答に反映せず | ❌ | 正解 | ✅ |

**シナリオA 正解率**: GraphRAG **1/5 (20%)** ／ RAG **3/5 (60%)**

---

### シナリオB — 中程度クエリ / medium data / llama3.2

<details>
<summary>期待値の根拠（medium データから導出）</summary>

```
BackendチームTEAM-001: ENG-001(山田太郎), ENG-003(田中一郎), ENG-008(小林直子)
認証モジュールMOD-001のバグ担当: 山田太郎、田中一郎、中村大輔、小林直子
決済MOD-003のcriticalバグ担当: 山田太郎(BUG-004,021), 田中一郎(BUG-029)
REL-002(v1.1)ブロックバグ: BUG-001,004,005,006,013,017,021,025,026,029,030（11件）
Frontend(TEAM-002)バグ計6件、Backend(TEAM-001)バグ計13件
```
</details>

| Q | 質問 | 正解概要 | GraphRAG | 判定 | RAG | 判定 |
|---|------|---------|----------|------|-----|------|
| 1 | Backendチーム担当openバグ | ENG-001/003/008担当のopenバグ9件 | Engineer.nameで"Backend"を検索（チームIDを辿らず）→空 | ❌ | MOD-008（関係なし）を回答 | ❌ |
| 2 | 認証モジュールのバグ担当者 | 山田太郎・田中一郎・中村大輔・小林直子 | Cypherエラー（`WITH Bug AS b`構文） | ❌ | 「バグは存在しない」と回答 | ❌ |
| 3 | 決済モジュールcritical担当 | 山田太郎・田中一郎 | Cypherエラー（`EXISTS`構文不正） | ❌ | 渡辺恵と回答（不正解） | ❌ |
| 4 | v1.1ブロックバグと担当者 | 11件のバグと各担当 | Cypherエラー（`assignedTo->name`） | ❌ | BUG-021と001を例示（部分的に正しいが不完全） | △ |
| 5 | Frontend vs Backend バグ件数比較 | Frontend 6件 vs Backend 13件 | Cypherエラー（`GROUP BY`はCypherでは無効） | ❌ | チーム判定誤り・件数不正確 | ❌ |

**シナリオB 正解率**: GraphRAG **0/5 (0%)** ／ RAG **0/5 (0%)**、部分正解各1件

---

### シナリオC — マルチホップ / large data / llama3.2

<details>
<summary>期待値の根拠（large データから導出）</summary>

```
Engineering部署DEPT-001: Team-001(Backend),002(Frontend),003(Mobile),009(API)
REL-002(v1.1)ブロックバグ→MOD-001〜004,015→全てPROJ-001(ECサイトリニューアル)
PROJ-001モジュール×Backend担当: ENG-001,003,014,024が複数バグ担当
v1.0(REL-005)ブロックバグ担当→全員TEAM-003(Mobile): BUG-007,008,014,018,038,053,083,096
```
</details>

| Q | 質問 | 正解概要 | GraphRAG | 判定 | RAG | 判定 |
|---|------|---------|----------|------|-----|------|
| 1 | Engineering部署担当criticalオープンバグ | TEAM-001/002/003/009所属エンジニア担当の多数 | MEMBER_OF向きが逆（Engineering→Team不存在）→空 | ❌ | 架空の説明文、具体的バグ未提示 | ❌ |
| 2 | v1.1ブロックバグのモジュールのプロジェクト名 | **ECサイトリニューアル** | BLOCKSの向き逆（Release→Bug）→空 | ❌ | 推薦アルゴリズム（AIエンジン）と回答（不正解） | ❌ |
| 3 | ECサイトリニューアルのBackend担当バグ | BUG-046,052,065,001,003,004,011,021... | Cypherエラー（`[:PART_OF]*`可変長パス） | ❌ | BUG-046,065を例示（部分正解） | △ |
| 4 | criticalバグ担当エンジニアの部署別件数 | 複雑な集計（多部署にわたる） | Cypherエラー（`WITH Bug AS bug`構文） | ❌ | 「情報が不足して答えられない」 | ❌ |
| 5 | v1.0モバイルブロックバグ担当チーム | **Mobile（TEAM-003）** | ASSIGNED_TO向き逆（Engineer→Bug）→空 | ❌ | BUG-054（誤）だがチームはMobile（正） | △ |

**シナリオC 正解率**: GraphRAG **0/5 (0%)** ／ RAG **0/5 (0%)**、部分正解各2件

---

### シナリオD — マルチホップ / large data / gemma2:27b

同一クエリをgemma2:27bで実行（シナリオCと比較）

| Q | 質問 | 正解概要 | GraphRAG | 判定 | RAG | 判定 |
|---|------|---------|----------|------|-----|------|
| 1 | Engineering部署担当criticalオープンバグ | 多数 | ASSIGNED_TO向き逆→空 | ❌ | 情報不足と正直に回答（不能） | ❌ |
| 2 | v1.1ブロックバグのプロジェクト名 | **ECサイトリニューアル** | 正しいCypherで正解を取得・回答 | ✅ | 情報不足と回答（不能） | ❌ |
| 3 | ECサイトリニューアルのBackend担当バグ | 複数バグ | ASSIGNED_TO向き逆→空 | ❌ | BUG-046のみ（部分正解） | △ |
| 4 | criticalバグ担当の部署別件数 | 複雑集計 | Cypherエラー（`GROUP BY`） | ❌ | 情報不足と正直に回答（不能） | ❌ |
| 5 | v1.0モバイルブロックバグ担当チーム | **Mobile（TEAM-003）** | BELONGS_TO経由の経路は正しいがASSIGNED_TO逆→空 | ❌ | BUG-054（誤）だがTeam=Mobileを正解 | △ |

**シナリオD 正解率**: GraphRAG **1/5 (20%)** ／ RAG **0/5 (0%)**、部分正解各2件

---

## 3. パフォーマンス比較

### 回答時間（秒/クエリ・平均）

| シナリオ | GraphRAG | RAG |
|---------|---------|-----|
| A (llama3.2, simple) | 7.2s | 3.6s |
| B (llama3.2, medium) | ※エラー多数 | 6.4s |
| C (llama3.2, multihop) | ※エラー多数 | 6.5s |
| D (gemma2:27b, multihop) | **83.4s** | **38.6s** |

> GraphRAGはCypherエラー時でも3〜10秒かかる（スキーマ取得・LLM呼び出しのオーバーヘッド）

### トークン使用量（入力+出力 合計/クエリ・平均）

| シナリオ | GraphRAG | RAG |
|---------|---------|-----|
| A (llama3.2) | 41tok | 291tok |
| B (llama3.2) | 46tok | 430tok |
| C (llama3.2) | 57tok | 325tok |
| D (gemma2:27b) | 31tok | 240tok |

> GraphRAGは生成Cypherを実行するため、LLMへの入力は少ない（スキーマ + 質問のみ）。
> RAGはコンテキストドキュメントをプロンプトに含めるため入力トークンが多い。

### モデルサイズによる速度差（マルチホップクエリ）

| モデル | GraphRAG avg | RAG avg |
|--------|-------------|---------|
| llama3.2 (3B) | 9.7s | 6.5s |
| gemma2:27b (27B) | 83.4s | 38.6s |

**速度比: gemma2:27b は llama3.2 の約 8.6倍（GraphRAG）〜 5.9倍（RAG）遅い**

---

## 4. GraphRAG の失敗分析

### 4-1. Cypherエラーの分類

| エラーパターン | 例 | 発生モデル |
|-------------|----|-----------|
| 存在しないノードラベルを使用 | `(n:Issue)`, `(n:Person)`, `(n:ECサイト)` | llama3.2 |
| `WITH NodeLabel AS var` 構文 | `WITH Bug AS b, Engineer AS e` | 両モデル |
| SQLの`GROUP BY`を混用 | `GROUP BY d.name` | gemma2:27b |
| `EXISTS((a)-[:REL]->(b))`（Neo4j 5では廃止） | `AND EXISTS((...))` | llama3.2 |
| 可変長パスの誤記法 | `[:PART_OF]*` | llama3.2 |

### 4-2. リレーション方向の誤り（重大）

スキーマに明示したにもかかわらず、両モデルともに以下の向きを逆に生成することが多発した：

```
正: (Bug)-[:ASSIGNED_TO]->（Engineer）
誤: (Engineer)-[:ASSIGNED_TO]->(Bug)  ← 両モデルで頻出

正: (Bug)-[:BLOCKS]->(Release)
誤: (Release)-[:BLOCKS]->(Bug)  ← llama3.2で発生
```

gemma2:27bはBLOCKSの向きを正しく認識したクエリ（Q2）で唯一の正解を達成。
llama3.2はすべてのマルチホップでリレーション方向を誤った。

### 4-3. 結果取得後の回答失敗

シナリオA Q5: Cypherで`[{'p.status': 'active'}]`を取得したが、回答は「情報がない」
→ LLMがCypherの結果をプロンプトに埋め込まれた形式で解釈できなかった（小モデルの限界）

---

## 5. RAGの失敗分析

### 5-1. ベクター検索の限界（マルチホップ）

RAGはCSV行をフラットなテキスト文書に変換してベクター検索する。
マルチホップクエリでは「Backendチームのエンジニアが担当するバグのあるモジュールのプロジェクト」のような
複数ジョインが必要な情報を単一の類似度検索では取得できない。

### 5-2. ハルシネーション

| シナリオ | 例 |
|---------|----|
| A Q2 | 架空の「MOD-001バグ（0.1.2 - バグが修正）」を列挙（バグIDや修正履歴は存在しない） |
| B Q1 | MOD-008（レポート機能）をBackendチームのバグとして回答（チーム関係は誤り） |
| C Q1 | 自己紹介文を生成（「私はEngineeringのエンジニアです」） |
| C Q2 | AIエンジンプロジェクトを回答（REL-002とPROJ-005には接続なし） |

### 5-3. gemma2:27b は「正直な不能回答」

llama3.2は積極的にハルシネーションするのに対し、gemma2:27bは
「与えられた情報だけでは答えられない」と回答を拒否するケースが多かった。
精度としては同等だが、誤情報を出力するリスクは低い。

---

## 6. 総合評価

### 6-1. 精度サマリー

| 比較軸 | 結論 |
|--------|------|
| GraphRAG vs RAG（シンプル） | RAGが優位（GraphRAGはCypherエラー多発） |
| GraphRAG vs RAG（マルチホップ） | 両方とも低精度。GraphRAGは0〜20%、RAGも0〜20% |
| llama3.2 vs gemma2:27b（GraphRAG） | gemma2:27bがCypher品質で優位（正解1件 vs 0件） |
| llama3.2 vs gemma2:27b（RAG） | 精度同等だがgemma2:27bはハルシネーション少ない |

### 6-2. 速度・コストサマリー

| 比較軸 | 結論 |
|--------|------|
| GraphRAG vs RAG（速度） | シンプルクエリはRAGが2倍速。マルチホップではほぼ同等 |
| GraphRAG vs RAG（トークン） | GraphRAGが7〜10倍少ない（Cypher実行のためコンテキスト不要） |
| llama3.2 vs gemma2:27b | 27Bモデルは約6〜9倍遅い。精度向上は限定的 |

---

## 7. 所見と考察

### GraphRAGが機能しなかった主因

1. **Cypherを正しく生成できる能力がモデルに依存する**
   llama3.2（3B）はCypherの構文を十分に学習しておらず、SQL混じりの構文を生成することが多い。
   スキーマをプロンプトに与えてもノードラベルは改善されたが、演算子・構文の誤りは改善されなかった。

2. **リレーションの向きが最大の障壁**
   プロンプトに方向を明記しても、モデルはトレーニングデータのバイアスにより向きを逆にしやすい。
   特に`ASSIGNED_TO`は「AがBに割り当てられる」＝`A→B`か`B→A`かが文脈依存で誤りやすい。

3. **結果取得後の回答生成**
   小モデルはCypherの実行結果をプロンプトから正しく読み取れないことがある。

### GraphRAGが機能するための条件（仮説）

- Cypherを正確に生成できる大規模・専用ファインチューンモデルが必要（例: GPT-4, Claude Opus）
- または、よく使うCypherをテンプレート化し、LLMの役割をパラメータ埋め込みに限定する
- グラフのリレーション方向はFew-Shotサンプルを複数提供することで改善できる可能性がある

### RAGの限界

- 複数エンティティを結合する情報は取得できない（ベクター検索の本質的限界）
- 文書変換の質（今回：CSVを文章化）が精度に大きく影響する
- ハルシネーション率はGraphRAGより高い傾向（特に小モデル）

---

## 8. 次の検証候補

1. **Few-Shot CypherをGraphRAGプロンプトに追加**して精度改善を検証
2. **GraphRAGモデルをAPI経由のClaude/GPTに変更**してCypher品質を比較
3. **RAGのチャンクサイズ・取得件数（n_results）を変えて**精度への影響を測定
4. **Cypherのバリデーション + 自動リトライ**でエラー率を改善できるか検証
5. **データ量（small→large）の影響**：RAGのベクター検索精度はデータ量が増えると低下するか

---

## 9. レポートファイル一覧

| ファイル | 内容 |
|---------|------|
| `docs/reports/20260401_103720_A_simple_graphrag_llama3.2.md` | シナリオA GraphRAG |
| `docs/reports/20260401_103720_A_simple_rag_llama3.2.md` | シナリオA RAG |
| `docs/reports/20260401_103850_B_medium_graphrag_llama3.2.md` | シナリオB GraphRAG |
| `docs/reports/20260401_103850_B_medium_rag_llama3.2.md` | シナリオB RAG |
| `docs/reports/20260401_104024_C_multihop_graphrag_llama3.2.md` | シナリオC GraphRAG |
| `docs/reports/20260401_104024_C_multihop_rag_llama3.2.md` | シナリオC RAG |
| `docs/reports/20260401_104203_D_multihop_large_graphrag_gemma2-27b.md` | シナリオD GraphRAG |
| `docs/reports/20260401_104203_D_multihop_large_rag_gemma2-27b.md` | シナリオD RAG |
