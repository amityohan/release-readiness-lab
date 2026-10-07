# Rollback Plan

## Target

The release history in `docs/architecture.md` identifies `v2.3` as the currently deployed stable release. The candidate image is `kalvium/checkout-api:v2.4`; rollback target: `kalvium/checkout-api:v2.3` in namespace `checkout-system`.

Before the change window, the SRE must confirm that the `v2.3` image exists in the production registry, that production can pull it, and that the required Secret/configuration is compatible. Those facts and a live rollback rehearsal have not been verified here. Do not start deployment until they are confirmed.

## Rollback Trigger and Owner

Initiate rollback for failed readiness/health checks, elevated checkout errors, unacceptable latency, or a customer-impacting regression. The named On-Call Engineer executes the rollback with the SRE/Operational Lead; both roles are currently unassigned in [ownership.md](ownership.md).

## Procedure

1. Record the incident start time, current image, and failing signal. Stop further rollout or promotion.
2. Pin the Deployment to the documented stable image:

   ```sh
   kubectl set image deployment/checkout-api checkout-api=kalvium/checkout-api:v2.3 -n checkout-system
   ```

3. Wait for completion and inspect the resulting image and pods:

   ```sh
   kubectl rollout status deployment/checkout-api -n checkout-system --timeout=5m
   kubectl get deployment checkout-api -n checkout-system -o=jsonpath='{.spec.template.spec.containers[?(@.name=="checkout-api")].image}{"\n"}'
   kubectl get pods -n checkout-system -l app=checkout-api -o wide
   ```

   Confirm the Deployment reports `kalvium/checkout-api:v2.3` and all expected replicas are available. If rollout fails, page the SRE lead and follow the incident escalation path; do not repeatedly retry without diagnosis.

4. Verify the service from an approved network location. For a controlled port-forward, run:

   ```sh
   kubectl port-forward service/checkout-api-service 8080:80 -n checkout-system
   ```

   In a second terminal, request `/health` and confirm HTTP 200 and the expected version. Check customer-facing checkout signals and dependency health using approved production telemetry; `/health` alone is not proof of PostgreSQL/Redis connectivity.
5. Record the outcome, timestamps, image digest if available, and follow-up owner in the incident record. Keep the candidate paused until its defect is fixed and the readiness pack is re-approved.

## Verification Status

This is a documented procedure, not a tested production rollback. The Kubernetes API was unreachable from this workstation, and image availability was not confirmed. Rollback rehearsal is a **No-Go** gate until performed in a representative environment and the evidence is attached.