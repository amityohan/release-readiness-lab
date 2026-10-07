# Risk Analysis

Severity is based on operational impact; likelihood is the best current estimate, not a measured production rate. Any open High risk blocks release regardless of the number of passing checks.

| Risk | Severity | Likelihood | Mitigation / exit criterion | Owner | State |
|---|---|---|---|---|---|
| Production `checkout-api-secrets` and its PostgreSQL/Redis values are unverified. | High | High until checked | Provision through the approved secret manager; verify key names and connectivity in the target namespace without exposing values. | SRE / Platform owner (unassigned) | Open; blocks release |
| `/ready` confirms environment-variable presence but the app does not establish real PostgreSQL or Redis connections. | High | Medium | Implement or confirm real dependency integration and test failure/recovery behavior; update readiness checks to reflect actual dependency health. | Application owner (unassigned) | Open; blocks release |
| No successful Python 3.11 CI or Docker image build evidence is attached. | High | Medium | Run the pull-request workflow, require its tests and image build to pass, and attach the run URL/logs. | CI / Release owner (unassigned) | Open; blocks release |
| Stable `v2.3` image availability and rollback execution are unverified. | High | Medium | Verify registry digest/pull access and rehearse rollback in a representative cluster; record timings and post-rollback checks. | SRE / Operational Lead (unassigned) | Open; blocks release |
| No named on-call responder or authorized approver is recorded. | High | Medium | Assign named people, deploy window, contact/paging route, escalation backup, and an approval record. | Release owner (unassigned) | Open; blocks release |
| Local checks used Python 3.13.14, not the documented Python 3.11 runtime. | Medium | Medium | Obtain a green CI run using Python 3.11 and retain the evidence. | CI owner (unassigned) | Open |
| Direct requirements are pinned, but transitive dependencies are not hash-locked. | Medium | Medium | Adopt a reviewed lock/hash strategy if reproducible builds are required; scan the exact resolved set on every release. | Application owner (unassigned) | Open |

## Gate

There are multiple unresolved High risks. The release is **No-Go** until every High item is closed with evidence and an accountable person signs the readiness report.