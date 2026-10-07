# Deployment Ownership

The role boundaries below are defined, but no individual names, contact details, or deploy-window confirmations were provided. Role descriptions do not count as assignment; all named-owner fields remain open and block approval.

| Role | Accountability | Assigned person/contact | Status |
|---|---|---|---|
| Release Owner | Owns the go/no-go, confirms gates, coordinates the window, and records the decision. | **UNASSIGNED** | Blocking |
| SRE / Operational Lead | Confirms target configuration, image availability, rollout/rollback plan, and production monitoring. | **UNASSIGNED** | Blocking |
| On-Call Support | Watches the deployment, acknowledges alerts, validates service health, and can execute rollback. | **UNASSIGNED** | Blocking |
| Application Owner | Owns app behavior, dependency integration, test results, and remediation of regressions. | **UNASSIGNED** | Blocking |
| Authorized Approver | Reviews the evidence and records approval or rejection independently of deployment execution. | **UNASSIGNED** | Blocking |

## Required Before the Window

- Record each person's name, team, and reachable contact/paging path; confirm availability for the entire deploy and rollback window.
- Name a backup for the On-Call Support and SRE / Operational Lead roles.
- Publish the deployment window, monitoring dashboard/alerts, incident channel, and escalation contacts.
- Have the Release Owner record a dated decision and link the exact commit, image digest, CI run, and readiness report.

## Escalation

On-Call Support responds first and pages the SRE / Operational Lead for rollout or infrastructure issues. The SRE lead escalates customer-impacting incidents to the Release Owner and incident commander, who coordinate rollback and stakeholder updates. Actual names and paging destinations must be filled in before this path is usable; none are asserted here.