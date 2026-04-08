---
name: k8s-ops
description: Common Kubernetes operations for LinkedIn KSAP services — pod management, deployment, debugging, scaling
inputs: ["app", "fabric"]
chain_to: investigate
chain_when: "CrashLoopBackOff or OOMKilled detected"
project: null
---

## Steps

All commands use `kubectl-in` (LinkedIn's kubectl wrapper). Replace `{{app}}` and `{{fabric}}` with your service and target fabric.

### 1. View pods and deployment status

```bash
# List all pods
kubectl in get pods -p {{app}} -a {{app}} -f {{fabric}}

# With cluster and namespace info (needed for port-forward)
kubectl in get pods -p {{app}} -a {{app}} -f {{fabric}} --show-cluster --show-namespace

# Deployment status with version info
go-status -f {{fabric}} {{app}} --show-tags --config-version

# Get LiDeployment details
kubectl in get lideployment -p {{app}} -f {{fabric}}

# Detailed status
kubectl in status lideployment -p {{app}} -f {{fabric}}
```

### 2. Logs and debugging

```bash
# Stream logs
kubectl in logs {{POD_NAME}} -p {{app}} -f {{fabric}} --stdout

# Previous container logs (after crash)
kubectl in logs {{POD_NAME}} -p {{app}} -f {{fabric}} --previous

# Describe pod (events, conditions, resource usage)
kubectl in describe pod {{POD_NAME}} -p {{app}} -f {{fabric}}

# Shell into pod
kubectl in exec {{POD_NAME}} -p {{app}} -f {{fabric}} -- bash

# Read-only debug container (for pods that won't start)
kubectl in debug {{POD_NAME}} -p {{app}} -f {{fabric}}
# Then exec into the debug container as shown in output
```

### 3. Pod management

```bash
# Restart all pods (rolling restart)
kubectl in rollout restart lideployment -p {{app}} -f {{fabric}}

# Restart specific product tag
kubectl in rollout restart lideployment -p {{app}} -f {{fabric}} -t {{app}}.{{tag}}

# Delete a specific pod (will be recreated by controller)
kubectl in delete pod {{POD_NAME}} -p {{app}} -a {{app}} -f {{fabric}}
```

### 4. Scaling

```bash
# Scale replicas (causes drift — update values.yaml after)
kubectl in update lideployment -p {{app}} -f {{fabric}} --replicas={{N}}

# Scale specific LiDeployment with version pinning
kubectl in update lideployment {{LIDEPLOYMENT_NAME}} -a {{app}} -f {{fabric}} \
  --application-version={{VERSION}} --config-version={{CONFIG_VERSION}} --replicas={{N}}

# Check Auto Rightsizing status
# Omit 'replicas' in values.yaml to enable AR
```

### 5. Deploy specific version

```bash
# Deploy specific app + config version
kubectl in update lideployment -p {{app}} -f {{fabric}} \
  --application-version={{APP_VERSION}} --config-version={{CONFIG_VERSION}}
```

### 6. Drift management

```bash
# Show drift (mismatch between live and IaC)
kubectl in drift show -p {{app}} -f {{fabric}}

# Resolve drift (align live with IaC)
kubectl in drift resolve -p {{app}} -f {{fabric}}
```

### 7. JMX access (port-forward)

```bash
# Step 1: Get pod with cluster and namespace
kubectl in get pods -p {{app}} -a {{app}} -f {{fabric}} --show-cluster --show-namespace

# Step 2: Port-forward (use raw kubectl, not kubectl-in)
kubectl port-forward pod/{{POD_NAME}} 9000:1949 --namespace {{NAMESPACE}} --context {{CLUSTER}}

# Step 3: Access JMX
open http://localhost:9000/{{app}}/jmx
```

### 8. ArgoCD UI

```
https://k8s-argocd.prod.linkedin.com/{{FABRIC}}-k8s-1/applications/{{app}}
```

## Expected Output

Each command should return data. If you see:
- `No resources found` → check product/app/fabric names
- `RBAC` error → run `kubectl in rbac-update --tenant ksap`
- Pod in `Pending` → check quota: `nimbus quota show <id> -f <fabric>`

## On Failure

- **CrashLoopBackOff** → check `kubectl in logs --previous`, chain to `/investigate`
- **OOMKilled (exit 137)** → increase memory in values.yaml
- **Drift detected on deploy** → run `kubectl in drift resolve` or update values.yaml
- **No permission** → engage #ask-nimbus on Slack
