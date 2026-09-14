import json
import logging
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent.parent
QUEUE_DIR = BASE_DIR / "knowledge_base" / "pipeline" / "task2_queue"
QUEUE_DIR.mkdir(parents=True, exist_ok=True)

_executor = ThreadPoolExecutor(max_workers=2)
_lock = threading.Lock()


def _now():
    return datetime.now(timezone.utc).isoformat()


def _path(job_id):
    return QUEUE_DIR / f"{job_id}.json"


def _write(job):
    with _lock:
        _path(job["id"]).write_text(json.dumps(job, indent=2), encoding="utf-8")


def get_job(job_id):
    path = _path(job_id)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _run(job_id, fn, args, kwargs):
    job = get_job(job_id) or {"id": job_id}
    job.update({"status": "processing", "started_at": _now()})
    _write(job)
    try:
        result = fn(*args, **kwargs)
        job.update({"status": "completed", "result": result, "finished_at": _now()})
    except Exception as exc:
        logger.exception("Background job failed: %s", job_id)
        job.update({"status": "failed", "error": str(exc), "finished_at": _now()})
    _write(job)


def submit(fn, *args, description="Evidence processing", **kwargs):
    job_id = f"task2_{uuid.uuid4().hex[:12]}"
    job = {
        "id": job_id,
        "status": "queued",
        "description": description,
        "created_at": _now(),
    }
    _write(job)
    _executor.submit(_run, job_id, fn, args, kwargs)
    return job


def cleanup_old_jobs(retention_hours=24):
    cutoff = time.time() - retention_hours * 3600
    for path in QUEUE_DIR.glob("*.json"):
        try:
            if path.stat().st_mtime < cutoff:
                path.unlink(missing_ok=True)
        except Exception:
            pass

def run_with_timeout(fn, *args, timeout_seconds=30, description="Background processing", **kwargs):
    job = submit(fn, *args, description=description, **kwargs)
    deadline = time.time() + float(timeout_seconds)
    while time.time() < deadline:
        current = get_job(job["id"])
        if current and current.get("status") in {"completed", "failed"}:
            return current
        time.sleep(0.2)
    current = get_job(job["id"]) or job
    current["status"] = "queued"
    current["customer_notification"] = (
        "Your file is taking longer than 30 seconds to process. "
        "It has been moved to the background queue and will continue automatically."
    )
    _write(current)
    return current
