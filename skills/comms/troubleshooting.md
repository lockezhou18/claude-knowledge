# Troubleshooting

| Symptom | Fix |
|---------|-----|
| Tunnel DOWN | `bash -c "ssh -f -N -L $NATS_PORT:localhost:4222 vm"` |
| NATS DOWN | Check VM: `bash -c "ssh vm 'docker ps \| grep nats'"` |
| "No responders" | VM listener not running: `bash -c "ssh vm 'tmux attach -t agentbus'"` |
| Timeout on sessions | Restart listener: `bash -c "ssh vm 'tmux send-keys -t agentbus C-c; sleep 2; tmux send-keys -t agentbus \"cd ~/agentbus && agentbus listen --agent $TARGET_AGENT --workspace ~/workspace\" Enter'"` |
| Auth expired | Kerberos: `! kinit`; Claude on VM: `! ssh -t vm 'claude auth login'` |
| Mutagen sync broken | Use `/sync fix` skill |
