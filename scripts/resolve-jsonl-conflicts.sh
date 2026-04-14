#!/bin/bash
# Auto-resolve merge conflicts in JSONL files (append-only logs)
# Both sides are valid — keep all lines, deduplicate
cd ~/claude-knowledge
for f in $(git diff --name-only --diff-filter=U 2>/dev/null); do
    if [[ "$f" == *.jsonl ]]; then
        python3 -c "
import re, sys
with open(\"\") as fh:
    content = fh.read()
cleaned = re.sub(r\"<<<<<<<.*\\n\", \"\", content)
cleaned = re.sub(r\"=======\\n\", \"\", cleaned)
cleaned = re.sub(r\">>>>>>>.*\\n\", \"\", cleaned)
lines = list(dict.fromkeys(l for l in cleaned.strip().split(\"\\n\") if l.strip()))
with open(\"\", \"w\") as fh:
    fh.write(\"\\n\".join(lines) + \"\\n\")
" 2>/dev/null && git add "$f" && echo "Resolved: $f"
    fi
done
