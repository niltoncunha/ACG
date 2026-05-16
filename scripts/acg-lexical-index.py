#!/usr/bin/env python3
"""ACG Lexical Index v0.4-alpha.

Small dependency-free retrieval helper. It is not RAG yet; it is a lexical
index that can later be replaced by embeddings while preserving the same
artifact shape.

Usage:
  python scripts/acg-lexical-index.py build --source ./repo --out .acg/artifacts
  python scripts/acg-lexical-index.py search --index .acg/artifacts/lexical_index.json --query "auth token validation"
"""
from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

TEXT_EXTENSIONS = {".md", ".txt", ".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".java", ".json", ".yaml", ".yml", ".toml"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", "coverage"}
MAX_FILE_BYTES = 200_000
TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{2,}")


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in TOKEN_RE.findall(text)]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def build_index(source: Path) -> dict:
    docs: dict[str, dict] = {}
    df: Counter[str] = Counter()
    for path in source.rglob("*"):
        if should_skip(path) or not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        if path.stat().st_size > MAX_FILE_BYTES:
            continue
        rel = path.relative_to(source).as_posix()
        tokens = tokenize(read_text(path))
        counts = Counter(tokens)
        docs[rel] = {
            "path": rel,
            "size": path.stat().st_size,
            "tokens": dict(counts.most_common(300)),
            "token_count": len(tokens),
        }
        for token in counts:
            df[token] += 1
    return {"doc_count": len(docs), "documents": docs, "df": dict(df)}


def score_query(index: dict, query: str, top_k: int) -> list[tuple[float, str]]:
    q_tokens = Counter(tokenize(query))
    doc_count = max(int(index.get("doc_count", 0)), 1)
    df = index.get("df", {})
    results: list[tuple[float, str]] = []
    for path, doc in index.get("documents", {}).items():
        token_counts = doc.get("tokens", {})
        score = 0.0
        for token, q_count in q_tokens.items():
            tf = float(token_counts.get(token, 0))
            if tf <= 0:
                continue
            idf = math.log((doc_count + 1) / (float(df.get(token, 0)) + 1)) + 1.0
            score += (1.0 + math.log(tf)) * idf * q_count
        if score > 0:
            results.append((score, path))
    return sorted(results, key=lambda item: (-item[0], item[1]))[:top_k]


def write_search_help(out: Path) -> None:
    (out / "lexical_index.md").write_text("""# ACG Lexical Index

This is a dependency-free lexical retrieval artifact.

It is not semantic RAG yet. It exists so ACG can later swap lexical search for
embeddings without changing the operator workflow.

Use:

```bash
python scripts/acg-lexical-index.py search --index .acg/artifacts/lexical_index.json --query "auth token validation"
```

Rules:
- Search results are candidates, not permission.
- Do not open returned files unless they are allowed by the current ACG phase or approved by the human.
- Prefer the gateway for reads when available.
""", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="ACG Lexical Index v0.4-alpha")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_build = sub.add_parser("build")
    p_build.add_argument("--source", required=True)
    p_build.add_argument("--out", default=".acg/artifacts")

    p_search = sub.add_parser("search")
    p_search.add_argument("--index", required=True)
    p_search.add_argument("--query", required=True)
    p_search.add_argument("--top-k", type=int, default=10)

    args = parser.parse_args()
    if args.cmd == "build":
        source = Path(args.source).resolve()
        out = Path(args.out).resolve()
        out.mkdir(parents=True, exist_ok=True)
        index = build_index(source)
        (out / "lexical_index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_search_help(out)
        print(f"ACG lexical index documents: {index['doc_count']}")
        print(f"Lexical index: {out / 'lexical_index.json'}")
        print(f"Lexical index help: {out / 'lexical_index.md'}")
        return 0

    index = json.loads(Path(args.index).read_text(encoding="utf-8"))
    results = score_query(index, args.query, args.top_k)
    for score, path in results:
        print(f"{score:.3f}\t{path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
