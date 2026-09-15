import logging
import time
from pathlib import Path

from src.config import TASK2_CONFIG

logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent.parent
CONVERSATIONS_DIR = BASE_DIR / "knowledge_base" / "conversations"


def _expired(uploaded_at: str, retention_hours: int) -> bool:
    try:
        from datetime import datetime, timezone
        value = str(uploaded_at or "").replace("Z", "+00:00")
        created = datetime.fromisoformat(value)
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - created).total_seconds() >= retention_hours * 3600
    except Exception:
        return False


def cleanup_expired_files(retention_hours=None):
    retention_hours = int(retention_hours or TASK2_CONFIG.get("retention_hours", 24))
    deleted = []
    if not CONVERSATIONS_DIR.exists():
        return deleted
    for manifest_path in CONVERSATIONS_DIR.glob("*/manifest.json"):
        try:
            import json
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            changed = False
            chat_dir = manifest_path.parent
            files_dir = chat_dir / "files"
            for file_id, record in list(manifest.items()):
                if not _expired(record.get("uploaded_at"), retention_hours):
                    continue
                filename = record.get("file_name")
                if filename:
                    (files_dir / filename).unlink(missing_ok=True)
                manifest.pop(file_id, None)
                deleted.append({"chat_id": chat_dir.name, "file_id": file_id, "file_name": filename})
                changed = True
            if changed:
                manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        except Exception as exc:
            logger.warning("Retention cleanup failed for %s: %s", manifest_path, exc)
    return deleted
