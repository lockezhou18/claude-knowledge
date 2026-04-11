#!/usr/bin/env python3
"""UserPromptSubmit hook: check for new async delegate results.

Looks for unread result files in ~/workspace/.agentbus/results/.
If found, prints a notification so Claude can inform the user.
Marks results as read by moving to results/read/ subdirectory.
"""

import json
import os
import shutil
import sys
from pathlib import Path

RESULTS_DIR = Path.home() / "workspace" / ".agentbus" / "results"
READ_DIR = RESULTS_DIR / "read"


def check_results():
    if not RESULTS_DIR.exists():
        return

    new_results = list(RESULTS_DIR.glob("*.json"))
    if not new_results:
        return

    READ_DIR.mkdir(parents=True, exist_ok=True)

    notifications = []
    for result_file in new_results:
        try:
            with open(result_file) as f:
                data = json.load(f)
            status = data.get("result", {}).get("status", "?")
            request = data.get("original_request", "")[:80]
            task_id = data.get("task_id", "?")[:8]
            result_text = data.get("result", {}).get("result", "")[:200]

            icon = "✓" if status == "success" else "✗"
            notifications.append(f"  {icon} [{task_id}..] {request}")
            if result_text:
                notifications.append(f"    → {result_text[:150]}")

            # Move to read
            shutil.move(str(result_file), str(READ_DIR / result_file.name))
        except Exception:
            continue

    if notifications:
        print(f"ASYNC_RESULTS: {len(new_results)} delegate task(s) completed:")
        for n in notifications:
            print(n)
        print(f"  Full details: ~/bin/vm-agent --results")


if __name__ == "__main__":
    check_results()
