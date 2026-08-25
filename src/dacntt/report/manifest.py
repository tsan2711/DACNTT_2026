"""Tool-lock file so later numbers can be compared."""

from __future__ import annotations

import json
from datetime import date, datetime, timezone
from importlib import metadata
from pathlib import Path
from typing import Any


def write_manifest(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def build_manifest(
    *,
    presets: list[str],
    n: int,
    limit: int | None,
    datasets: list[str],
    gold_urls: dict[str, str],
) -> dict[str, Any]:
    return {
        "date": date.today().isoformat(),
        "utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "n": n,
        "limit": limit,
        "datasets": datasets,
        "presets": presets,
        "math_verify_version": _pkg_version("math-verify"),
        "antlr4_version": _pkg_version("antlr4-python3-runtime"),
        "gold_urls": gold_urls,
    }


def _pkg_version(name: str) -> str:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return "not-installed"
