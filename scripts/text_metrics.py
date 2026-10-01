#!/usr/bin/env python3
"""Deterministic length metrics for writing-boost drafts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = json.loads((ROOT / "runtime-contract.json").read_text(encoding="utf-8"))

HAN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
LATIN_NUMBER_TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*")
LATIN_WORD_RE = re.compile(r"[A-Za-z]+(?:['’-][A-Za-z]+)*|\d+(?:[.,]\d+)?")
FENCE_RE = re.compile(r"```.*?```|~~~.*?~~~", flags=re.DOTALL)
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")
LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
HTML_TAG_RE = re.compile(r"<[^>]+>")


def markdown_prose(text: str) -> str:
    """Approximate visible prose by removing metadata/URLs/code blocks, not prose labels."""
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end >= 0:
            text = text[end + 5 :]
    text = FENCE_RE.sub(" ", text)
    text = IMAGE_RE.sub(" ", text)
    text = LINK_RE.sub(r"\1", text)
    text = HTML_TAG_RE.sub(" ", text)
    return text


def metrics(text: str) -> dict[str, int]:
    han_chars = len(HAN_RE.findall(text))
    latin_number_tokens = len(LATIN_NUMBER_TOKEN_RE.findall(text))
    visible_chars = sum(1 for ch in text if not ch.isspace())
    words = len(LATIN_WORD_RE.findall(text))
    return {
        "zh_units": han_chars + latin_number_tokens,
        "han_chars": han_chars,
        "latin_number_tokens": latin_number_tokens,
        "visible_chars": visible_chars,
        "words": words,
    }


def resolve_band(args: argparse.Namespace) -> tuple[int | None, int | None]:
    if args.minimum is not None or args.maximum is not None:
        return args.minimum, args.maximum
    if args.target is None:
        return None, None
    tolerance = (
        args.tolerance
        if args.tolerance is not None
        else CONTRACT["defaults"]["exact_length_tolerance_ratio"]
    )
    return round(args.target * (1 - tolerance)), round(args.target * (1 + tolerance))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument(
        "--mode",
        choices=["zh_units", "visible_chars", "words"],
        default=CONTRACT["length"]["zh_default_mode"],
    )
    parser.add_argument(
        "--markdown-prose",
        action="store_true",
        help="Remove YAML frontmatter, fenced code, image syntax, link destinations, and HTML tags before counting.",
    )
    parser.add_argument("--target", type=int)
    parser.add_argument("--min", dest="minimum", type=int)
    parser.add_argument("--max", dest="maximum", type=int)
    parser.add_argument("--tolerance", type=float)
    args = parser.parse_args()

    text = args.path.read_text(encoding="utf-8")
    counted_text = markdown_prose(text) if args.markdown_prose else text
    result = metrics(counted_text)
    minimum, maximum = resolve_band(args)
    selected = result[args.mode]

    payload = {
        "path": str(args.path),
        "mode": args.mode,
        "markdown_prose": args.markdown_prose,
        "selected_count": selected,
        "metrics": result,
        "minimum": minimum,
        "maximum": maximum,
        "pass": None
        if minimum is None and maximum is None
        else (minimum is None or selected >= minimum)
        and (maximum is None or selected <= maximum),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["pass"] is not False else 2


if __name__ == "__main__":
    raise SystemExit(main())
