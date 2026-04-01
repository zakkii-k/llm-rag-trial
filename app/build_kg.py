"""
build_kg.py — Neo4j にナレッジグラフを構築するスクリプト

使い方:
    python app/build_kg.py --data-dir data/small
    python app/build_kg.py --data-dir data/medium
    python app/build_kg.py --data-dir data/large
"""

import argparse
import csv
import os
from typing import Optional

from neo4j import GraphDatabase


class KnowledgeGraphBuilder:
    def __init__(self, uri: str, auth: Optional[tuple] = None):
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def close(self):
        self.driver.close()

    # ──────────────────────────────────────────
    # ノード投入
    # ──────────────────────────────────────────

    def _load_csv(self, path: str) -> list[dict]:
        with open(path, encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def load_departments(self, csv_path: str):
        rows = self._load_csv(csv_path)
        with self.driver.session() as session:
            session.execute_write(self._batch_create_departments, rows)
        print(f"  {len(rows)} 件の Department を投入しました")

    @staticmethod
    def _batch_create_departments(tx, rows):
        tx.run("""
        UNWIND $rows AS r
        MERGE (d:Department {id: r.id})
        ON CREATE SET d.name = r.name, d.createdAt = datetime()
        ON MATCH SET  d.name = r.name, d.updatedAt = datetime()
        """, rows=rows)

    def load_teams(self, csv_path: str):
        rows = self._load_csv(csv_path)
        with self.driver.session() as session:
            session.execute_write(self._batch_create_teams, rows)
        print(f"  {len(rows)} 件の Team を投入しました")

    @staticmethod
    def _batch_create_teams(tx, rows):
        tx.run("""
        UNWIND $rows AS r
        MERGE (t:Team {id: r.id})
        ON CREATE SET t.name = r.name, t.createdAt = datetime()
        ON MATCH SET  t.name = r.name, t.updatedAt = datetime()
        WITH t, r
        WHERE r.department_id <> ""
        MATCH (d:Department {id: r.department_id})
        MERGE (t)-[:BELONGS_TO]->(d)
        """, rows=rows)

    def load_engineers(self, csv_path: str):
        rows = self._load_csv(csv_path)
        with self.driver.session() as session:
            session.execute_write(self._batch_create_engineers, rows)
        print(f"  {len(rows)} 人の Engineer を投入しました")

    @staticmethod
    def _batch_create_engineers(tx, rows):
        tx.run("""
        UNWIND $rows AS r
        MERGE (e:Engineer {id: r.id})
        ON CREATE SET e.name = r.name, e.email = r.email, e.createdAt = datetime()
        ON MATCH SET  e.name = r.name, e.email = r.email, e.updatedAt = datetime()
        WITH e, r
        WHERE r.team_id <> ""
        MATCH (t:Team {id: r.team_id})
        MERGE (e)-[:MEMBER_OF]->(t)
        """, rows=rows)

    def load_projects(self, csv_path: str):
        rows = self._load_csv(csv_path)
        with self.driver.session() as session:
            session.execute_write(self._batch_create_projects, rows)
        print(f"  {len(rows)} 件の Project を投入しました")

    @staticmethod
    def _batch_create_projects(tx, rows):
        tx.run("""
        UNWIND $rows AS r
        MERGE (p:Project {id: r.id})
        ON CREATE SET p.name = r.name, p.status = r.status, p.createdAt = datetime()
        ON MATCH SET  p.name = r.name, p.status = r.status, p.updatedAt = datetime()
        """, rows=rows)

    def load_modules(self, csv_path: str):
        rows = self._load_csv(csv_path)
        with self.driver.session() as session:
            session.execute_write(self._batch_create_modules, rows)
        print(f"  {len(rows)} 件の Module を投入しました")

    @staticmethod
    def _batch_create_modules(tx, rows):
        tx.run("""
        UNWIND $rows AS r
        MERGE (m:Module {id: r.id})
        ON CREATE SET m.name = r.name, m.createdAt = datetime()
        ON MATCH SET  m.name = r.name, m.updatedAt = datetime()
        WITH m, r
        WHERE r.project_id <> ""
        MATCH (p:Project {id: r.project_id})
        MERGE (m)-[:PART_OF]->(p)
        """, rows=rows)

    def load_releases(self, csv_path: str):
        rows = self._load_csv(csv_path)
        with self.driver.session() as session:
            session.execute_write(self._batch_create_releases, rows)
        print(f"  {len(rows)} 件の Release を投入しました")

    @staticmethod
    def _batch_create_releases(tx, rows):
        tx.run("""
        UNWIND $rows AS r
        MERGE (rel:Release {id: r.id})
        ON CREATE SET rel.version = r.version, rel.status = r.status, rel.createdAt = datetime()
        ON MATCH SET  rel.version = r.version, rel.status = r.status, rel.updatedAt = datetime()
        WITH rel, r
        WHERE r.project_id <> ""
        MATCH (p:Project {id: r.project_id})
        MERGE (rel)-[:BELONGS_TO]->(p)
        """, rows=rows)

    def load_bugs(self, csv_path: str):
        rows = self._load_csv(csv_path)
        with self.driver.session() as session:
            session.execute_write(self._batch_create_bugs, rows)
        print(f"  {len(rows)} 件の Bug を投入しました")

    @staticmethod
    def _batch_create_bugs(tx, rows):
        # Bug ノード作成
        tx.run("""
        UNWIND $rows AS r
        MERGE (b:Bug {id: r.id})
        ON CREATE SET b.title = r.title, b.severity = r.severity,
                      b.status = r.status, b.createdAt = datetime()
        ON MATCH SET  b.status = r.status, b.updatedAt = datetime()
        """, rows=rows)
        # ASSIGNED_TO (Bug -> Engineer)
        tx.run("""
        UNWIND $rows AS r
        WITH r WHERE r.assignee_id <> ""
        MATCH (b:Bug {id: r.id}), (e:Engineer {id: r.assignee_id})
        MERGE (b)-[:ASSIGNED_TO]->(e)
        """, rows=rows)
        # FOUND_IN (Bug -> Module)
        tx.run("""
        UNWIND $rows AS r
        WITH r WHERE r.module_id <> ""
        MATCH (b:Bug {id: r.id}), (m:Module {id: r.module_id})
        MERGE (b)-[:FOUND_IN]->(m)
        """, rows=rows)
        # BLOCKS (Bug -> Release)
        tx.run("""
        UNWIND $rows AS r
        WITH r WHERE r.blocks_release_id <> ""
        MATCH (b:Bug {id: r.id}), (rel:Release {id: r.blocks_release_id})
        MERGE (b)-[:BLOCKS]->(rel)
        """, rows=rows)

    # ──────────────────────────────────────────
    # インデックス
    # ──────────────────────────────────────────

    def create_indexes(self):
        indexes = [
            "CREATE INDEX engineer_id   IF NOT EXISTS FOR (e:Engineer)   ON (e.id)",
            "CREATE INDEX bug_id        IF NOT EXISTS FOR (b:Bug)        ON (b.id)",
            "CREATE INDEX bug_severity  IF NOT EXISTS FOR (b:Bug)        ON (b.severity)",
            "CREATE INDEX bug_status    IF NOT EXISTS FOR (b:Bug)        ON (b.status)",
            "CREATE INDEX team_id       IF NOT EXISTS FOR (t:Team)       ON (t.id)",
            "CREATE INDEX project_id    IF NOT EXISTS FOR (p:Project)    ON (p.id)",
            "CREATE INDEX module_id     IF NOT EXISTS FOR (m:Module)     ON (m.id)",
            "CREATE INDEX release_id    IF NOT EXISTS FOR (r:Release)    ON (r.id)",
            "CREATE INDEX department_id IF NOT EXISTS FOR (d:Department) ON (d.id)",
        ]
        with self.driver.session() as session:
            for q in indexes:
                session.run(q)
        print("  インデックスを作成しました")

    def clear_graph(self):
        """既存データを全削除してからロードし直す"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        print("  既存グラフを削除しました")


def main():
    from dotenv import load_dotenv
    load_dotenv()

    parser = argparse.ArgumentParser(description="Neo4j にナレッジグラフを構築する")
    parser.add_argument(
        "--data-dir", default="data/small",
        help="CSVファイルのあるディレクトリ (例: data/small, data/medium, data/large)"
    )
    parser.add_argument(
        "--clear", action="store_true",
        help="投入前にグラフを全削除する"
    )
    args = parser.parse_args()

    data_dir = args.data_dir

    builder = KnowledgeGraphBuilder(
        uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        auth=(
            os.getenv("NEO4J_USER", "neo4j"),
            os.getenv("NEO4J_PASSWORD"),
        ),
    )

    try:
        if args.clear:
            builder.clear_graph()

        builder.create_indexes()

        # 投入順序は外部キー依存を考慮する
        _load_if_exists(builder.load_departments, data_dir, "departments.csv")
        _load_if_exists(builder.load_teams,       data_dir, "teams.csv")
        _load_if_exists(builder.load_engineers,   data_dir, "engineers.csv")
        _load_if_exists(builder.load_projects,    data_dir, "projects.csv")
        _load_if_exists(builder.load_modules,     data_dir, "modules.csv")
        _load_if_exists(builder.load_releases,    data_dir, "releases.csv")
        _load_if_exists(builder.load_bugs,        data_dir, "bugs.csv")

        print(f"\nKG構築完了 (データソース: {data_dir})")
    finally:
        builder.close()


def _load_if_exists(load_fn, data_dir: str, filename: str):
    path = os.path.join(data_dir, filename)
    if os.path.exists(path):
        load_fn(path)
    else:
        print(f"  スキップ: {path} が存在しません")


if __name__ == "__main__":
    main()
