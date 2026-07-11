# Post-Incident Review (Lessons Learned) Template

Structured, blameless review template for the post-incident meeting — held within 1-2 weeks of incident closure while details are still fresh.

## Template

```markdown
# Post-Incident Review: [Incident Name/ID]

**Date of review:** [date]
**Attendees:** [names/roles]
**Incident timeframe:** [detection timestamp] to [closure timestamp]
**Playbook used:** [which playbook, link to it]

## Timeline Summary
[Pull directly from tooling/playbook-tracker/ export — detection,
containment, eradication, recovery timestamps and the time-to-X metrics]

## What Went Well
[Specific, not generic — "the EDR alert fired within 90 seconds of shadow
copy deletion" not "detection was good"]

## What Didn't Go Well
[Specific and blameless — describe the gap, not who caused it. "The
playbook didn't cover multi-site coordination" not "the on-call analyst
didn't know to loop in the second site."]

## Root Cause
[The specific technical/process gap that allowed this — see the DFIR
report template's Root Cause section for the same discipline: avoid vague
causes in favor of specific, actionable ones]

## Detection Gaps Identified
[Were there earlier signals that, in hindsight, should have triggered
detection sooner? This directly feeds into detection rule updates — see
siem-soar-detection-engineering]

## Playbook Gaps Identified
[Did the playbook used cover this scenario adequately? What step was
missing, unclear, or wrong? This is the direct input for updating the
playbook itself — a post-incident review that doesn't result in a playbook
edit was probably too vague]

## Action Items

| Action | Owner | Priority | Target Date |
|---|---|---|---|
| | | | |

## Metrics for This Incident
- Time to containment: [from playbook-tracker report]
- Time to eradication: [from playbook-tracker report]
- Time to recovery: [from playbook-tracker report]
- Compare against prior incidents of the same type, if available — a single
  incident's metrics mean little in isolation; trend over time is what
  shows whether response capability is actually improving
```

## Facilitation Guidance

- **Blameless means blameless — actually enforce it in the room.** The moment a review turns into identifying who made a mistake, people stop being honest about what they saw and didn't act on, which is exactly the information the review needs most.
- **Every "what didn't go well" item should map to an action item.** A review that identifies gaps without assigning owners and dates is a venting session, not process improvement.
- **Revisit prior action items at the start of the next review.** An action item that's been "in progress" across three consecutive incidents of the same type is a signal worth escalating on its own.

---
*Part of the [incident-response-playbooks](../README.md) repository.*
