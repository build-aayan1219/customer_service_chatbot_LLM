"""Unattended runner for the Task 1 knowledge-base production pipeline.

Schedule this script from Windows Task Scheduler/cron. The pipeline itself
enforces the configured schedule, maintenance window, quality gates and retries.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.knowledge_base import run_scheduled_knowledge_base_pipeline


if __name__ == "__main__":
    result = run_scheduled_knowledge_base_pipeline()
    print(result)
