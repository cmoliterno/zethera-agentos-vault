#!/usr/bin/env python3
"""Small local lexical RAG for an AgentOS Vault.

Uses SQLite FTS5 from the Python standard library. No API keys.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_SUFFIXES = {".md", ".txt", ".yaml", ".yml", ".json"}
EXCLUDED_DIRS = {".git", ".agentos", "node_modules", "__pycache__"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in DEFAULT_SUFFIXES:
            yield path


def chunks(text: str, size: int = 1800, overlap: int = 250):
    text = text.replace("\r\n", "\n")
    if len(text) <= size:
        yield text
        return
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        yield text[start:end]
        if end == len(text):
            break
        start = max(0, end - overlap)


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute("drop table if exists documents")
    conn.execute("drop table if exists documents_fts")
    conn.execute(
        "create table documents (id integer primary key, path text, title text, chunk_index integer, content text)"
    )
    conn.execute(
        "create virtual table documents_fts using fts5(title, path, content, content='documents', content_rowid='id')"
    )


def ingest(root: Path, db: Path) -> dict:
    root = root.resolve()
    db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db)
    init_db(conn)
    count_files = 0
    count_chunks = 0
    for path in iter_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = path.relative_to(root).as_posix()
        title = path.stem
        count_files += 1
        for index, chunk in enumerate(chunks(text)):
            cur = conn.execute(
                "insert into documents(path, title, chunk_index, content) values (?, ?, ?, ?)",
                (rel, title, index, chunk),
            )
            rowid = cur.lastrowid
            conn.execute(
                "insert into documents_fts(rowid, title, path, content) values (?, ?, ?, ?)",
                (rowid, title, rel, chunk),
            )
            count_chunks += 1
    conn.commit()
    conn.close()
    return {"root": str(root), "db": str(db), "files": count_files, "chunks": count_chunks, "generated_at": now_iso()}


def query(db: Path, text: str, limit: int) -> dict:
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        select d.path, d.title, d.chunk_index,
               snippet(documents_fts, 2, '[', ']', ' ... ', 30) as snippet,
               bm25(documents_fts) as score
        from documents_fts
        join documents d on d.id = documents_fts.rowid
        where documents_fts match ?
        order by bm25(documents_fts)
        limit ?
        """,
        (text, limit),
    ).fetchall()
    conn.close()
    evidences = []
    for index, row in enumerate(rows, start=1):
        evidences.append(
            {
                "rank": index,
                "title": row["title"],
                "path": row["path"],
                "chunk_index": row["chunk_index"],
                "score": row["score"],
                "snippet": row["snippet"],
            }
        )
    return {"query": text, "generated_at": now_iso(), "retrieval_mode": "sqlite_fts5_local", "evidence_count": len(evidences), "evidences": evidences}


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    ingest_parser = sub.add_parser("ingest")
    ingest_parser.add_argument("--root", type=Path, required=True)
    ingest_parser.add_argument("--db", type=Path, required=True)

    query_parser = sub.add_parser("query")
    query_parser.add_argument("--db", type=Path, required=True)
    query_parser.add_argument("--query", required=True)
    query_parser.add_argument("--limit", type=int, default=8)

    args = parser.parse_args()
    if args.command == "ingest":
        print(json.dumps(ingest(args.root, args.db), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(query(args.db, args.query, args.limit), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

