
from __future__ import annotations
from pathlib import Path
import json
from typing import Any

def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text())

def dump_json(data: Any, path: str | Path) -> None:
    Path(path).write_text(json.dumps(data, indent=2))

def load_jsonl(path: str | Path) -> list[dict]:
    rows = []
    with Path(path).open() as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows
