import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def write_unfollow_log(username: str, items: List[Dict[str, Any]], dry_run: bool):
    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    doc = {
        "timestamp_utc": ts,
        "actor": username,
        "dry_run": dry_run,
        "count": len(items),
        "items": items,
    }
    path = LOG_DIR / f"unfollow-{ts}.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    return str(path)
