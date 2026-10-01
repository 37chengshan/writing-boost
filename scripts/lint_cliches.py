#!/usr/bin/env python3
"""Locate high-risk Chinese nonfiction cliches without rewriting the text."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERN_FILE = ROOT / "references" / "cliche-patterns-zh.json"


def line_info(text: str, offset: int) -> tuple[int, str]:
    number = text.count("\n", 0, offset) + 1
    lines = text.splitlines()
    line = lines[number - 1] if number - 1 < len(lines) else ""
    return number, line


def looks_quoted(line: str, phrase: str) -> bool:
    stripped = line.lstrip()
    if stripped.startswith(">"):
        return True
    quoted_forms = [
        f"“{phrase}”",
        f"‘{phrase}’",
        f'"{phrase}"',
        f"'{phrase}'",
        f"`{phrase}`",
    ]
    return any(form in line for form in quoted_forms)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero for unquoted high-risk hits. Quotes remain review triggers but do not fail strict mode.",
    )
    args = parser.parse_args()

    text = args.path.read_text(encoding="utf-8")
    pattern_doc = json.loads(PATTERN_FILE.read_text(encoding="utf-8"))
    hits = []

    for item in pattern_doc["patterns"]:
        phrase = item["phrase"]
        start = 0
        while True:
            offset = text.find(phrase, start)
            if offset < 0:
                break
            line_no, line = line_info(text, offset)
            hits.append(
                {
                    "id": item["id"],
                    "phrase": phrase,
                    "severity": item["severity"],
                    "line": line_no,
                    "quoted_hint": looks_quoted(line, phrase),
                    "line_preview": line.strip()[:220],
                }
            )
            start = offset + len(phrase)

    strict_hits = [
        h for h in hits if h["severity"] == "high" and not h["quoted_hint"]
    ]
    payload = {
        "path": str(args.path),
        "hit_count": len(hits),
        "unquoted_high_risk_count": len(strict_hits),
        "hits": hits,
        "note": (
            "Hits are review triggers, not automatic deletion orders. "
            "quoted_hint is heuristic only; reviewer must preserve sourced quotes "
            "and intentional discussion."
        ),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 2 if args.strict and strict_hits else 0


if __name__ == "__main__":
    raise SystemExit(main())
