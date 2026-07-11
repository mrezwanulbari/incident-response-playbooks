# Incident Response Playbooks

Standardized, NIST SP 800-61r2-aligned incident response playbooks and working execution tooling for SOC and DFIR teams — built for repeatable execution under pressure, not as reference documentation nobody reads during a real incident.

## What's Inside

### Playbooks
| Playbook | Scope |
|---|---|
| `playbooks/ransomware-incident-response-playbook.md` | Detection through recovery for ransomware/encryption events, including decision points on isolation vs. shutdown and backup validation before restore |
| `playbooks/phishing-bec-response-playbook.md` | Phishing campaigns and business email compromise — account takeover, invoice fraud, executive impersonation, including time-critical wire-recall guidance for financial fraud cases |
| `playbooks/cloud-account-compromise-playbook.md` | Compromised cloud identity (AWS IAM, Azure AD/Entra ID) — access keys, over-privileged role abuse, fast identity-disable containment specific to cloud environments |

Every playbook follows the same NIST SP 800-61r2 structure (Detection & Triage → Containment → Eradication → Recovery → Post-Incident Activity) so responders trained on one can immediately navigate another.

### Working Tooling
| Tool | Description | Testing Status |
|---|---|---|
| `tooling/playbook-tracker/` | SQLite-backed CLI: logs phase timestamps against a live incident, computes time-to-containment/eradication/recovery metrics automatically | **Tested end-to-end** — full incident lifecycle verified, metrics confirmed accurate |
| `tooling/severity-triage/` | Structured 60-second severity scoring tool — consistent classification instead of a gut call that varies by who's on shift | **Tested** — verified against both a minimal low-severity case and a ransomware-like critical scenario, both classified correctly |

### Templates
| Template | Use |
|---|---|
| `templates/executive-notification-template.md` | First notification to leadership during an active incident — plain-language, status-first, no jargon |
| `templates/post-incident-review-template.md` | Blameless post-incident review structure — every finding maps to an owned action item |

### Schema
| File | Description |
|---|---|
| `schema/incident-export-schema.json` | Formal JSON Schema for the playbook tracker's export format. **Validated** against a real export produced by `playbook_tracker.py` |

## How the Pieces Connect

1. **Severity triage** runs first — 60 seconds to get a defensible initial classification
2. **Playbook tracker** starts logging as soon as response begins, timestamping each phase as the relevant **playbook** guides the response
3. **Executive notification template** goes out early, using the plain-language status — not the technical detail
4. Once closed, the tracker's exported timeline feeds directly into the **post-incident review**, and (for full forensic writeups) the [DFIR toolkit's report template](https://github.com/mrezwanulbari/digital-forensics-dfir-toolkit/blob/main/templates/dfir-report-template.md)

## Who This Is For

SOC analysts and incident responders needing executable runbooks and tooling that actually runs, DFIR teams standardizing response procedures and metrics across shifts, and security leaders building tabletop exercises or tracking IR program maturity over time.

## Status

Actively maintained — playbooks, tooling, and templates are added and refined based on current threat patterns and real response experience.

## About the Author

Maintained by Shakil Md. Rezwanul Bari, Cyber Security Engineer with 17+ years of experience in DFIR, SIEM/SOAR, and enterprise incident response across financial-sector and critical infrastructure environments. Connect on [LinkedIn](https://www.linkedin.com/in/rezwanulbari/).

## License

MIT — see [LICENSE](LICENSE).
