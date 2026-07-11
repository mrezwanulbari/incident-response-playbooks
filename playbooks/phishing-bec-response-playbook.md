# Phishing & Business Email Compromise (BEC) Response Playbook

**Scope:** Detection through recovery for phishing campaigns and business email compromise (account takeover, invoice fraud, executive impersonation).
**Framework:** NIST SP 800-61r2

## 1. Detection & Triage (Target: within 15 minutes of first report)

**Initial indicators:**
- User-reported suspicious email (report button or forward to security)
- Email security gateway alert on a known-bad indicator
- Finance/AP team flags an unusual payment or vendor-change request
- Unusual mailbox rule creation or login anomaly from identity provider alerting

**Triage decisions:**
- [ ] Determine type: mass phishing campaign vs. targeted spear-phishing vs. BEC (account takeover or impersonation without compromise)
- [ ] For BEC specifically: has any account actually been compromised (credential entry, MFA fatigue approval), or is this impersonation-only (spoofed/lookalike domain, no account access)?
- [ ] Identify blast radius: how many users received this, has anyone clicked/entered credentials/replied with sensitive info or authorized a payment?

**Severity classification:**
| Level | Criteria | Response |
|---|---|---|
| Low | Mass phishing, no credential entry, low click rate | Standard containment, no escalation |
| Medium | Targeted spear-phishing, some credential entry suspected, no confirmed financial loss | Escalate to IR lead, activate account containment procedures |
| Critical | Confirmed account compromise on a privileged/executive account, OR a fraudulent payment was authorized/sent | Executive notification, involve finance/legal immediately, consider law enforcement for financial fraud |

## 2. Containment (Target: within 30 minutes of confirmation)

**For confirmed or suspected account compromise:**
- [ ] Force password reset and revoke all active sessions/tokens for the affected account
- [ ] Re-challenge MFA and, if MFA fatigue/push-bombing is suspected as the vector, temporarily require number-matching or hardware key MFA for the account
- [ ] Review and remove any unauthorized mailbox rules (auto-forwarding, auto-delete rules are a common BEC persistence technique — attackers create rules to hide their activity and exfiltrate ongoing mail)
- [ ] Check for unauthorized OAuth app grants / third-party app access tied to the account — a common persistence method that survives a password reset alone

**For BEC-driven financial fraud (payment already sent or in progress):**
- [ ] **Time-critical:** Contact your bank's fraud department immediately to attempt a wire recall — the window for successful recall is typically hours, not days
- [ ] Do not rely on email alone to verify any pending payment change request — verify via a known-good phone number, not one provided in the suspicious email
- [ ] Loop in finance/AP leadership and legal in parallel with the technical response, not after

**Campaign-wide containment (regardless of individual account status):**
- [ ] Block sender domain/URL/indicators at the email security gateway
- [ ] Purge the phishing email from all mailboxes it reached, not just the reporter's
- [ ] If a credential-harvesting page is involved, submit for takedown/blocklisting where possible

## 3. Eradication

- [ ] Confirm the initial access vector is closed (was it a lookalike domain, a compromised vendor account sending from a legitimate-but-compromised source, or a technical email security gap?)
- [ ] For account compromise: audit the account's recent activity thoroughly for the full suspected dwell time, not just the triggering event — attackers who gain mailbox access often read extensively before acting
- [ ] Remove any persistence mechanisms found during containment (mailbox rules, OAuth grants)

## 4. Recovery

- [ ] Restore normal account access once containment is verified complete
- [ ] Monitor the account closely for reinfection/repeat compromise attempts for at least 1-2 weeks
- [ ] For financial fraud cases, coordinate with finance on recovery status (bank recall outcome, insurance claim if applicable)

## 5. Post-Incident Activity

- [ ] Lessons-learned review — was this preventable with earlier MFA enforcement, mailbox rule alerting, or payment verification process changes?
- [ ] Update detection rules based on the specific indicators observed (sender patterns, lookalike domains, mailbox rule creation alerting)
- [ ] If this was a targeted spear-phish, consider whether the targeting suggests broader reconnaissance against the organization worth investigating further
- [ ] Update user security awareness training content with the real (sanitized) example if appropriate — a real internal example is far more effective than generic training content

## Escalation Contacts

*Customize with your organization's actual chain — IR lead, finance/AP leadership (for BEC financial fraud), legal, bank fraud department contact, cyber insurance carrier.*

---
*Part of the [incident-response-playbooks](../README.md) repository.*
