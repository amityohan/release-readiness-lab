# Dependency Checks

## Declared Direct Dependencies

| Package | Pinned version | Purpose |
|---|---:|---|
| Flask | 3.1.3 | HTTP application |
| Gunicorn | 22.0.0 | Production WSGI server |
| pytest | 9.0.3 | Test runner |

The application runtime documented in `docs/architecture.md` is Python 3.11. The requirements are exact-version pins, and the framework version in the architecture record has been aligned with the updated requirement. The local test and audit environment used Python 3.13.14, so the documented Python 3.11 CI run remains required.

## Vulnerability Audit

- Tool: `pip-audit`
- Input: the complete resolved package/version list installed from `app/requirements.txt` in a clean temporary environment
- Result: `No known vulnerabilities found`
- The first scan identified advisories for Flask 3.0.2 and pytest 8.0.2. The direct pins were upgraded to Flask 3.1.3 and pytest 9.0.3, then the full resolved package set was scanned again successfully.
- The audit checked versions against the available vulnerability data; it did not verify package hashes or provenance.

## Remaining Dependency Risks

- There is no committed lock file or hash-locked dependency set. Transitive versions may change on a future install even while direct requirements remain pinned.
- `app/requirements.txt` does not include PostgreSQL or Redis client libraries, and `app/app.py` does not connect to either service. The current code only reports whether their environment variables are configured. Confirm whether real integrations are intentionally outside this demo's release scope; do not treat the configuration check as dependency connectivity validation.
- Repeat the audit at release time and preserve its output with the CI run for the exact image being promoted.