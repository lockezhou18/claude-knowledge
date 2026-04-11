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

    # Check for completed results (top-level .json files)
    new_results = [f for f in RESULTS_DIR.glob("*.json") if f.is_file()]
    # Check for auto-mode checkpoints
    checkpoint_dirs = [d for d in RESULTS_DIR.iterdir() if d.is_dir() and d.name != "read" and d.name.endswith("_checkpoints")]

    if not new_results and not checkpoint_dirs:
        return

    READ_DIR.mkdir(parents=True, exist_ok=True)
    notifications = []

    # Completed async results
    for result_file in new_results:
        try:
            with open(result_file) as f:
                data = json.load(f)
            status = data.get("result", {}).get("status", data.get("final_status", "?"))
            request = data.get("original_request", "")[:80]
            task_id = data.get("task_id", "?")[:8]
            result_text = str(data.get("result", {}).get("result", data.get("final_result", "")))[:200]
            rounds = data.get("total_rounds")

            icon = "✓" if status == "success" else "✗"
            rounds_str = f" ({rounds} rounds)" if rounds else ""
            notifications.append(f"  {icon} [{task_id}..]{rounds_str} {request}")
            if result_text:
                notifications.append(f"    → {result_text[:150]}")

            shutil.move(str(result_file), str(READ_DIR / result_file.name))
        except Exception:
            continue

    # In-progress auto-mode checkpoints
    for cp_dir in checkpoint_dirs:
        try:
            checkpoints = sorted(cp_dir.glob("*_step*.json"))
            if not checkpoints:
                continue
            latest = checkpoints[-1]
            with open(latest) as f:
                cp = json.load(f)
            task_id = cp.get("task_id", "?")[:8]
            step = cp.get("round", "?")
            max_r = cp.get("max_rounds", "?")
            preview = cp.get("result_preview", "")[:100]
            done = cp.get("done", False)

            if done:
                notifications.append(f"  ✓ [{task_id}..] auto-task done at step {step}/{max_r}")
                # Move entire checkpoint dir to read
                shutil.move(str(cp_dir), str(READ_DIR / cp_dir.name))
            else:
                notifications.append(f"  ⏳ [{task_id}..] auto-task step {step}/{max_r}: {preview[:80]}")
        except Exception:
            continue

    if notifications:
        count = len(new_results) + len(checkpoint_dirs)
        print(f"DELEGATE_UPDATE: {count} task(s):")
        for n in notifications:
            print(n)
        print(f"  Details: ~/bin/vm-agent --results")


if __name__ == "__main__":
    check_results()
