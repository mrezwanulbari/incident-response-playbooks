# Ransomware Incident Response Playbook

**Scope:** Detection through recovery for ransomware and mass-encryption events.
**Framework:** NIST SP 800-61r2

## 1. Detection & Triage (Target: within 15 minutes of first alert)

**Initial indicators:**
- EDR/AV alerts for known ransomware behavior (mass file modification, shadow copy deletion, unusual encryption process activity)
- Helpdesk reports of inaccessible files or ransom notes
- SIEM correlation alerts on abnormal file I/O volume from a single host

**Triage decisions:**
- [ ] Confirm this is ransomware, not a false positive (check for ransom note, file extension changes, `vssadmin delete shadows` or equivalent commands in EDR telemetry)
- [ ] Identify patient zero and scope: how many hosts are affected right now, and is the count growing?
- [ ] Classify severity: single endpoint vs. spreading laterally vs. domain controller/critical server involved

**Severity classification:**
| Level | Criteria | Response |
|---|---|---|
| Low | Single non-critical endpoint, contained | Standard IR process |
| Medium | Multiple endpoints, no critical servers | Escalate to IR lead, activate war room |
| Critical | Domain controllers, backup infrastructure, or critical business systems affected | Executive notification, consider full network isolation |

## 2. Containment (Target: within 30-60 minutes of confirmation)

**Short-term containment — do this first, decide isolation method based on scope:**
- [ ] Isolate affected host(s) from the network (network-level isolation via EDR preferred over shutdown — shutdown can trigger destructive payloads and always destroys volatile memory evidence)
- [ ] Disable affected user accounts if credential compromise is suspected as the vector
- [ ] Block identified C2 indicators at the firewall/proxy
- [ ] **Critical decision point:** Do NOT power off affected systems unless actively directed by DFIR — memory forensics require a live system. Network isolation, not shutdown, is the default containment action.

**Evidence preservation (parallel to containment, not after):**
- [ ] Capture memory image from at least one representative affected host before any remediation
- [ ] Preserve relevant SIEM logs, EDR telemetry, and network flow data before retention windows roll them off
- [ ] Photograph ransom notes and record ransomware variant identifiers (file extension, note filename, any embedded contact/payment info) — do NOT interact with attacker-provided links or contacts without legal/executive sign-off

## 3. Eradication

- [ ] Identify and confirm the initial access vector (phishing, exposed RDP, exploited vulnerability, compromised credentials)
- [ ] Remove persistence mechanisms (scheduled tasks, registry run keys, new service installations, unauthorized accounts)
- [ ] Patch or close the exploited vector before reconnecting any system to the network
- [ ] Rotate credentials for all accounts with any plausible exposure — start with domain admin and service accounts

## 4. Recovery

- [ ] **Validate backup integrity before restoring** — restoring from a compromised or already-encrypted backup reintroduces the incident. Check backup timestamps against the earliest known compromise indicator.
- [ ] Restore systems in priority order: authentication infrastructure and security tooling first, then business-critical systems, then general endpoints
- [ ] Monitor restored systems closely for 72 hours minimum for signs of reinfection
- [ ] Confirm eradication was complete before declaring recovery finished — a single missed persistence mechanism means round two

## 5. Post-Incident Activity

- [ ] Conduct a blameless lessons-learned review within 1-2 weeks
- [ ] Update detection rules based on the specific TTPs observed (map to MITRE ATT&CK)
- [ ] Update this playbook if any step was unclear, missing, or wrong during the real response
- [ ] Assess whether regulatory/breach notification obligations apply (varies by sector and data involved — involve legal/compliance early, not after this step)

## Escalation Contacts

*Customize this section with your organization's actual escalation chain — IR lead, legal, executive sponsor, cyber insurance carrier, and (if applicable) law enforcement/CISA contact.*

---
*Part of the [incident-response-playbooks](../README.md) repository.*
