# データ概要

## グラフ構造

```
(Department)
    ↑ BELONGS_TO
(Team)
    ↑ MEMBER_OF
(Engineer)
    ↑ ASSIGNED_TO
(Bug) ──FOUND_IN──► (Module) ──PART_OF──► (Project)
  └──BLOCKS────────► (Release) ──BELONGS_TO──► (Project)
```

### ノードタイプ

| ノード | 主なプロパティ |
|--------|--------------|
| Department | id, name |
| Team | id, name |
| Engineer | id, name, email |
| Project | id, name, status |
| Module | id, name |
| Release | id, version, status |
| Bug | id, title, severity, status |

### リレーションタイプ

| リレーション | from → to | 意味 |
|------------|-----------|------|
| MEMBER_OF | Engineer → Team | エンジニアがチームに所属 |
| BELONGS_TO | Team → Department | チームが部署に所属 |
| ASSIGNED_TO | Bug → Engineer | バグの担当者 |
| FOUND_IN | Bug → Module | バグが発見されたモジュール |
| PART_OF | Module → Project | モジュールがプロジェクトに属する |
| BLOCKS | Bug → Release | バグがリリースをブロック |
| BELONGS_TO | Release → Project | リリースがプロジェクトに属する |

---

## データセット統計

### small — 1〜2ホップ検証向け

| ノード | 件数 |
|--------|------|
| Department | 2 |
| Team | 2 |
| Engineer | 3 |
| Project | 1 |
| Module | 2 |
| Release | 2 |
| Bug | 3 |

| Severity | 件数 |
|----------|------|
| critical | 1 |
| medium | 1 |
| high | 1 |

| Status | 件数 |
|--------|------|
| open | 2 |
| resolved | 1 |

---

### medium — 2〜3ホップ検証向け

| ノード | 件数 |
|--------|------|
| Department | 4 |
| Team | 5 |
| Engineer | 10 |
| Project | 3 |
| Module | 8 |
| Release | 6 |
| Bug | 30 |

| Severity | 件数 |
|----------|------|
| critical | 7 |
| high | 13 |
| medium | 8 |
| low | 2 |

| Status | 件数 |
|--------|------|
| open | 21 |
| in_progress | 5 |
| resolved | 4 |

**チーム構成:**

| Team | Department | エンジニア数 |
|------|-----------|------------|
| Backend | Engineering | 2 |
| Frontend | Engineering | 2 |
| Mobile | Engineering | 2 |
| QA | QA | 2 |
| DevOps | Infrastructure | 1 |

---

### large — 3ホップ以上の複雑クエリ向け

| ノード | 件数 |
|--------|------|
| Department | 6 |
| Team | 10 |
| Engineer | 30 |
| Project | 6 |
| Module | 16 |
| Release | 10 |
| Bug | 100 |

| Severity | 件数 |
|----------|------|
| critical | 26 |
| high | 41 |
| medium | 27 |
| low | 6 |

| Status | 件数 |
|--------|------|
| open | 76 |
| in_progress | 11 |
| resolved | 13 |

**チーム構成:**

| Team | Department | エンジニア数 |
|------|-----------|------------|
| Backend | Engineering | 4 |
| Frontend | Engineering | 4 |
| Mobile | Engineering | 4 |
| QA | QA | 4 |
| DevOps | Infrastructure | 3 |
| Security | Security | 3 |
| DataEngineering | Data | 3 |
| MachineLearning | Data | 3 |
| API | Engineering | 3 |
| Platform | Infrastructure | 2 |

**プロジェクト構成:**

| Project | モジュール数 | リリース数 |
|---------|-----------|---------|
| ECサイトリニューアル | 6 | 3 |
| モバイルアプリ開発 | 3 | 2 |
| 管理画面改善 | 2 | 1 |
| データ基盤構築 | 2 | 1 |
| AI推薦エンジン | 2 | 2 |
| セキュリティ強化 | 2 | 1 |

---

## 検証クエリのホップ数分類

### 1ホップ（`prompts/simple.txt`）
単一ノードまたは直接の関係のみで答えられる。

例: `criticalなバグは何件？` → Bug のプロパティを参照するだけ

### 2ホップ（`prompts/medium.txt`）
2つのノードをたどる必要がある。

例: `Backendチームのエンジニアが担当するバグ` → Bug→Engineer→Team

### 3+ホップ（`prompts/multihop.txt`）
3つ以上のノードをたどる複雑な経路。RAGとGraphRAGの差が最も出やすい。

例: `v1.1をブロックするバグが属するモジュールのプロジェクト名` → Bug→Release, Bug→Module→Project
