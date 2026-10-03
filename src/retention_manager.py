import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from src.config import TASK2_CONFIG

logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent.parent
CONVERSATIONS_DIR = BASE_DIR / "knowledge_base" / "conversations"


def _expired(uploaded_at: str, retention_hours: int) -> bool:
    try:
        value = str(uploaded_at or "").replace("Z", "+00:00")
        created = datetime.fromisoformat(value)
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - created).total_seconds() >= retention_hours * 3600
    except Exception:
        return False


def _normalise_manifest(data):
    if isinstance(data, dict):
        return data
    if isinstance(data, list):
        manifest = {}
        for index, record in enumerate(data):
            if not isinstance(record, dict):
                continue
            file_id = str(record.get("id") or record.get("file_id") or f"legacy_{index}")
            record = dict(record)
            record.pop("id", None)
            record.pop("file_id", None)
            manifest[file_id] = record
        return manifest
    return {}


def cleanup_expired_files(retention_hours=None):
    retention_hours = int(retention_hours or TASK2_CONFIG.get("retention_hours", 24))
    deleted = []
    if not CONVERSATIONS_DIR.exists():
        return deleted

    for manifest_path in CONVERSATIONS_DIR.glob("*/manifest.json"):
        chat_dir = manifest_path.parent
        files_dir = chat_dir / "files"
        changed = False
        try:
            manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest = _normalise_manifest(manifest_data)

            for file_id, record in list(manifest.items()):
                if not isinstance(record, dict):
                    continue
                if not _expired(record.get("uploaded_at"), retention_hours):
                    continue

                filename = record.get("file_name")
                if filename:
                    (files_dir / Path(str(filename)).name).unlink(missing_ok=True)

                manifest.pop(file_id, None)
                deleted.append({
                    "chat_id": chat_dir.name,
                    "file_id": file_id,
                    "file_name": filename,
                })
                changed = True

            if changed or not isinstance(manifest_data, dict):
                manifest_path.write_text(
                    json.dumps(manifest, indent=2, ensure_ascii=False),
                    encoding="utf-8",
                )

                try:
                    from src.conversation_files import rebuild_conversation_index
                    rebuild_conversation_index(chat_dir.name)
                except Exception as index_error:
                    logger.warning(
                        "Could not rebuild conversation index after retention cleanup for %s: %s",
                        chat_dir.name,
                        index_error,
                    )

        except Exception as exc:
            logger.warning("Retention cleanup failed for %s: %s", manifest_path, exc)

    return deleted
