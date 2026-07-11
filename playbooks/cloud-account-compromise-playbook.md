# Cloud Account Compromise Response Playbook

**Scope:** Detection through recovery for compromised cloud identity/accounts (AWS IAM, Azure AD/Entra ID, or SaaS admin accounts), including compromised access keys and over-privileged role abuse.
**Framework:** NIST SP 800-61r2

## 1. Detection & Triage (Target: within 15 minutes of first alert)

**Initial indicators:**
- Impossible-travel or anomalous sign-in alerts from the identity provider (see [azure-security Sentinel analytics rule](https://github.com/mrezwanulbari/azure-security) for a working example)
- CloudTrail/Activity Log alerts on unusual API calls (e.g., new IAM user creation, permission escalation, security group changes from an unfamiliar principal)
- Unexpected billing spike (frequently the first visible sign of compromised compute/API keys being used for cryptomining or resource abuse)
- Static access key detected in a public location (GitHub, paste site) via secret-scanning alert

**Triage decisions:**
- [ ] Identify the compromised principal type: human user account, service account, or access key/token
- [ ] Determine current activity status: is the compromised credential still being actively used right now, or was this a past event now detected?
- [ ] Scope check: what permissions did/does this principal have? A compromised read-only account is a very different severity than a compromised account with IAM admin rights

**Severity classification:**
| Level | Criteria | Response |
|---|---|---|
| Low | Low-privilege account, no evidence of actual malicious API activity beyond the anomalous sign-in itself | Standard containment, monitor |
| Medium | Privileged account or evidence of reconnaissance-level API activity (listing resources, describing configurations) | Escalate to IR lead, full activity audit |
| Critical | Admin/root-equivalent account compromised, OR evidence of data exfiltration/resource abuse/persistence mechanism creation | Executive notification, consider cloud provider's incident response support channel |

## 2. Containment (Target: within 20 minutes of confirmation — cloud environments allow much faster containment than on-prem, use that speed)

- [ ] **Disable the compromised principal immediately** — disable the IAM user/role or revoke the access key. In cloud environments, this is a fast, low-collateral-damage action (unlike network isolation of a physical host), so the bar for acting should be lower
- [ ] Revoke all active sessions/tokens for the affected identity, not just credential rotation — an active session can persist after a password change until tokens are explicitly revoked
- [ ] **Critical decision point — do NOT delete the account/role yet.** Disable and preserve for forensic review of CloudTrail/Activity Log history; deletion can complicate the ability to fully audit what the compromised identity did
- [ ] Review and temporarily suspend any newly-created IAM users, roles, or access keys created during the suspected compromise window — attackers with IAM write access frequently create backup access before the primary compromised credential gets caught

## 3. Evidence Preservation

- [ ] Export the full CloudTrail/Activity Log history for the compromised principal covering the full suspected dwell time (default retention windows vary by provider/configuration — pull this before it ages out)
- [ ] Snapshot any compute resources the compromised identity had access to, if resource-level compromise (not just identity) is suspected
- [ ] Document the exact permission set the compromised identity held at time of compromise — IAM policies can change after the fact, so capture this early

## 4. Eradication

- [ ] Confirm and close the initial access vector: leaked key in a public repo, phished credentials, weak/no MFA on the account, or over-permissioned trust relationship that was abused
- [ ] Audit for and remove any persistence: new IAM users/roles/keys, modified trust policies, new federated identity providers, backdoor Lambda/Function resources
- [ ] Rotate any secrets/credentials the compromised identity had access to (not just the compromised identity's own credentials) — assume anything it could read, it did read

## 5. Recovery

- [ ] Re-provision access for the legitimate user with new credentials and MFA re-enrollment
- [ ] Apply least-privilege review to the restored access — this is a natural checkpoint to ask whether the original permission set was broader than necessary (see [aws-security least-privilege policy example](https://github.com/mrezwanulbari/aws-security))
- [ ] Monitor the restored identity closely for 1-2 weeks

## 6. Post-Incident Activity

- [ ] Lessons-learned review — how was the credential compromised, and does this indicate a broader gap (no MFA enforcement, overly broad IAM policies, secret-scanning gaps)?
- [ ] Update detection rules and billing-anomaly alerting thresholds based on what was observed
- [ ] Consider whether this incident indicates a need for [Zero Trust](https://github.com/mrezwanulbari/zero-trust-architecture) identity-layer improvements (conditional access policies, JIT elevation) rather than just the immediate fix

## Escalation Contacts

*Customize with your organization's actual chain — IR lead, cloud platform team, legal, cloud provider's security/incident response support channel if available under your support tier.*

---
*Part of the [incident-response-playbooks](../README.md) repository.*
