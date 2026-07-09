# Incident Response Playbooks

Standardized, NIST SP 800-61r2-aligned incident response playbooks for SOC and DFIR teams, built for repeatable execution under pressure rather than as reference documentation nobody reads during a real incident.

## Why This Exists

Most published IR playbooks are either generic checklists that don't survive contact with a real incident, or dense compliance documents nobody reads during an active response. These playbooks are written the way an experienced DFIR responder actually works an incident: fast triage decisions first, then structured containment/eradication/recovery steps, with clear escalation and evidence-preservation checkpoints throughout.

## Framework

Every playbook follows the NIST SP 800-61r2 incident response lifecycle:

1. **Preparation** — what needs to be in place before an incident happens
2. **Detection & Analysis** — triage criteria, severity classification, initial scoping
3. **Containment, Eradication & Recovery** — short-term containment, evidence preservation, root-cause eradication, staged recovery
4. **Post-Incident Activity** — lessons-learned review, playbook update triggers

## What's Inside

| Playbook | Scope |
|---|---|
| `playbooks/ransomware-incident-response-playbook.md` | Detection through recovery for ransomware/encryption events, including decision points on isolation vs. shutdown and backup validation before restore |
| `playbooks/` *(expanding)* | Additional playbooks (phishing/BEC, insider threat, cloud account compromise) added as they're built out |

## Who This Is For

SOC analysts and incident responders needing executable runbooks, DFIR teams standardizing response procedures across shifts, and security leaders building tabletop exercises around realistic scenarios.

## Status

Actively maintained — playbooks are added and refined based on current threat patterns.

## About the Author

Maintained by Shakil Md. Rezwanul Bari, Cyber Security Engineer with 17+ years of experience in DFIR, SIEM/SOAR, and enterprise incident response across financial-sector and critical infrastructure environments. Connect on [LinkedIn](https://www.linkedin.com/in/rezwanulbari/).

## License

MIT — see [LICENSE](LICENSE).
