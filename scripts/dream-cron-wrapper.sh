#!/bin/bash
LOG=~/claude-knowledge/learnings/logs/dream-cron.log
echo "=== Dream cron started: $(date) ===" >> $LOG

echo "Step 1: git pull" >> $LOG
cd ~/claude-knowledge && git pull --no-rebase 2>&1 >> $LOG || echo "git pull failed (continuing)" >> $LOG

echo "Step 2: resolve conflicts" >> $LOG
bash ~/claude-knowledge/scripts/resolve-jsonl-conflicts.sh 2>&1 >> $LOG || true

echo "Step 3: dream.py" >> $LOG
python3 ~/projects/compound-learning-ecosystem/memory-migration/scripts/dream.py 2>&1 >> $LOG

echo "Step 4: commit + push" >> $LOG
cd ~/claude-knowledge && git add -A
if ! git diff --cached --quiet; then
    git commit -m "dream: vm $(date +%Y-%m-%d)" 2>&1 >> $LOG
    git push origin HEAD:main 2>&1 >> $LOG || echo "push failed" >> $LOG
else
    echo "nothing to commit" >> $LOG
fi

echo "=== Dream cron finished: $(date) ===" >> $LOG
