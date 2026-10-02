from __future__ import annotations
import json
import os
from datetime import datetime, timezone
from pathlib import Path

class Audit:
    def __init__(self, path: str | None = None):
        path = path or os.getenv("JARVIS_AUDIT_LOG", str(Path.home() / ".local" / "share" / "jarvis" / "audit.jsonl"))
        self.path = Path(path).expanduser()
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, **event):
        event["ts"] = datetime.now(timezone.utc).isoformat()
        self.path.open("a", encoding="utf-8").write(json.dumps(event, ensure_ascii=False) + "\n")
