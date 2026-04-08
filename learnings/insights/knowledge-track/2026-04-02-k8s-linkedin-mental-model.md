---
id: know-016
track: knowledge
type: semantic
repos: ["*"]
tags: ["k8s", "kubernetes", "ksap", "nimbus", "lideployment", "infrastructure", "deployment", "kubectl-in"]
severity: high
created: "2026-04-02"
last_verified: "2026-04-02"
use_count: 0
outcome_score: 0
rot_rate: slow
status: active
---

## Kubernetes at LinkedIn — Mental Model

**When** working with k8s at LinkedIn, understand that LinkedIn does NOT use vanilla k8s. They built Nimbus/KSAP on top.

### General k8s → LinkedIn Mapping

| K8s Concept | LinkedIn Equivalent | Key Difference |
|-------------|-------------------|----------------|
| Deployment | **LiDeployment** (CRD) | Custom resource with canary, quotas, AR |
| Service | **D2** (ZooKeeper) | No k8s Services — D2 for Java, Envoy/INDIS for non-Java |
| Ingress | **D2 routing** | No k8s Ingress |
| HPA | **Auto Rightsizing** | Omit `replicas` in values.yaml to enable |
| ConfigMap | **Cfg2** | LinkedIn config system |
| Secret | **KMS** | LinkedIn key management |
| kubectl | **kubectl-in** | Enhanced wrapper with `-f fabric -p product` context |
| Helm | `.linkedin/kube/` IaC | Helm-based with LinkedIn chart libs |

### Three Platforms

| Platform | For | When to use |
|----------|-----|-------------|
| **KSAP** | Stateless (APIs, mid-tier) | hp-ats-integration-mt, mcm-mt, ts-api |
| **NSS** | Stateful (DBs, caches) | Espresso nodes, need persistent storage |
| **KJP** | Batch (Spark, ML, ETL) | Offline processing |

### Deployment Flow

```
IaC in .linkedin/kube/ (Chart.yaml + values.yaml per fabric)
  → PR merge → LCD pipeline (Airflow)
  → KSAP operator → LiDeployment → Pods
  → Canary analysis (EKG) → Full rollout
```

### Key Gotchas

1. **No SSH** — cannot SSH into KSAP hosts. Use `kubectl in exec` or `kubectl in debug`
2. **CLI changes cause drift** — manual `kubectl in update` creates mismatch with IaC. Always update values.yaml after
3. **First deploy needs replicas** — must set explicitly, AR takes over after
4. **maxUnavailable ≤ 15%** — CRT blocks prod deploy if exceeded
5. **LARE auto-integrations** — certs (Grestin), config (Cfg2), discovery (Topology), secrets (KMS) are auto-injected
6. **Legacy → KSAP migration deadline: FY26H2** — all RAIN apps must migrate

### Essential Commands

```bash
kubectl in get pods -p APP -f FABRIC          # list pods
kubectl in logs POD -p APP -f FABRIC --stdout  # stream logs
kubectl in exec POD -p APP -f FABRIC -- bash   # shell in
kubectl in debug POD -p APP -f FABRIC          # debug container
kubectl in rollout restart lideployment -p APP -f FABRIC  # restart
kubectl in drift show -p APP -f FABRIC         # check drift
go-status -f FABRIC APP --show-tags            # version info
```

### Ownership
- Nimbus/KSAP: #nimbus, #ksap
- KJP: #kjp
- LCD: #lcd
- Support: #ask-nimbus

### For Personal Infra (Takeaways)
- **k3s** for lightweight self-hosted k8s
- **ArgoCD** for GitOps (LinkedIn's drift concept)
- **Prometheus + Grafana** for monitoring
- **Cert-Manager** for TLS
- **Traefik** for ingress
- Store all manifests in git, deploy via CI/CD
