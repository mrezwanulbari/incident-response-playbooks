# Executive Incident Notification Template

Structured template for the first notification to executive leadership during an active incident — written for speed under pressure (fill-in-the-blank) and for a non-technical audience.

## Template

```markdown
Subject: [SEVERITY] Security Incident Notification — [Incident Name/ID]

**Status as of [timestamp]:**

**What happened:**
[1-2 sentences, plain language, no jargon. E.g., "We detected ransomware
activity on [N] systems in [department/location] at approximately [time]."]

**Current impact:**
[What's affected right now — systems down, data at risk, business
operations impacted. Be honest about what's NOT yet known, don't guess.]

**What we've done so far:**
[Containment actions taken, in plain language]

**What happens next:**
[Immediate next steps and rough timeline for the next update]

**What we need from you:**
[Specific asks — approval for an action, resource authorization,
customer/regulatory notification decision, etc. Only include this if
there's an actual decision needed now; don't pad with informational-only
content.]

**Next update:** [Specific time, not "soon" — e.g., "within 2 hours" or "by 5pm ET"]

**Point of contact:** [Name, how to reach you]
```

## Writing Guidance

- **Lead with status, not narrative.** Executives reading this mid-crisis want "are we okay right now" before "how did this happen."
- **Never speculate as fact.** "We believe this may be ransomware, pending confirmation" is honest; "This is ransomware" when it's not yet confirmed creates a false narrative that's hard to walk back later.
- **Commit to a specific next-update time, every time.** An open-ended "we'll update you when we know more" leaves leadership without a way to plan around the incident — a specific time, even if the update is "still investigating, next update in 2 hours," is far more useful than silence or vagueness.
- **Keep the technical detail out of this notification.** Full technical detail belongs in the [DFIR report](https://github.com/mrezwanulbari/digital-forensics-dfir-toolkit/blob/main/templates/dfir-report-template.md) written after the incident, not in a live status update.

---
*Part of the [incident-response-playbooks](../README.md) repository.*
