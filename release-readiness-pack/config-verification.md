# Configuration Verification

## Expected Configuration

| Setting | Source | Expected value/state | Verification |
|---|---|---|---|
| `LOG_LEVEL` | `k8s/configmap.yaml` | `info` | Present in the ConfigMap; application logging reads it. |
| `PORT` | `k8s/configmap.yaml` | `5000` | Matches the container port and Gunicorn bind port. Keep these values aligned; Gunicorn currently binds to 5000 directly. |
| `DATABASE_URL` | Kubernetes Secret `checkout-api-secrets` | Required, non-empty PostgreSQL connection string | The Deployment now imports it from the Secret. Secret existence, key presence, value correctness, and connectivity were not verified because the target cluster is unavailable. |
| `REDIS_URL` | Kubernetes Secret `checkout-api-secrets` | Required, non-empty Redis connection string | The Deployment now imports it from the Secret. Secret existence, key presence, value correctness, and connectivity were not verified because the target cluster is unavailable. |

No credentials belong in a ConfigMap or this repository. Provision the Secret in namespace `checkout-system` through the approved secret-management process. It must contain keys named `DATABASE_URL` and `REDIS_URL` before deployment; the Deployment's non-optional `secretRef` deliberately prevents a pod from starting with the Secret absent.

## Application and Probe Behavior

- `/health` is a process liveness endpoint. It remains HTTP 200 when dependency configuration is missing and reports `missing_config`; it does not claim that configured URLs are reachable.
- `/ready` returns HTTP 503 until both required variables are present, and HTTP 200 once both are present. This proves configuration presence only, not database/cache connectivity.
- Kubernetes uses `/health` for liveness and `/ready` for readiness. The readiness gate keeps a pod out of Service endpoints when required configuration is missing.
- The app currently does not open PostgreSQL or Redis connections. A successful `/ready` response is not an end-to-end dependency check.

## Release Gate

**Status: BLOCKED.** Verify the Secret's existence and key names without printing its values, confirm the URLs and credentials with the target environment owner, and run authenticated connectivity/smoke checks from the deployed application before approval. None of those production checks could be performed from this workstation.