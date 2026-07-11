# Severity Triage Scorer

A fast, structured severity scoring tool for the first minutes of an incident — produces a consistent, defensible classification instead of a gut call that varies by who's on shift.

## Why This Exists

Severity classification under pressure tends to default to either "everything is critical" (alert fatigue for leadership) or "assume low until proven otherwise" (dangerous under-response). A 60-second structured scoring pass fixes both failure modes.

## Usage

Interactive:
```bash
python3 severity_triage.py
```

Scripted (e.g. called from a SOAR playbook or another tool):
```bash
python3 severity_triage.py \
    --systems-affected 12 \
    --data-sensitivity regulated \
    --business-criticality high \
    --spreading true \
    --privileged-access true \
    --public-facing false \
    --output triage_result.json
```

## Scoring Factors

| Factor | Why It's Weighted This Way |
|---|---|
| Systems affected | Scope indicator, but weighted lower than the dynamic factors below — a wide but static/contained incident is less urgent than a small but actively spreading one |
| Data sensitivity | Regulated data involvement drives notification/legal obligations regardless of technical severity |
| Business criticality | Impact to operations, independent of technical scope |
| **Actively spreading** | Highest weight — this is the strongest predictor of an incident escalating quickly if not contained now |
| **Privileged access compromised** | Equally high weight — privileged access changes the blast radius of every other factor |
| Public-facing systems involved | Reputational/external-exposure multiplier |

## Severity Bands

| Score | Severity | Guidance |
|---|---|---|
| 0-3 | Low | Standard IR process |
| 4-8 | Medium | Escalate to IR lead, activate war room |
| 9-14 | High | Executive notification, all-hands response |
| 15+ | Critical | Executive + legal notification, consider external IR support |

## Tested

Verified against two scenarios: a minimal low-severity case (score 0) and a ransomware-like scenario with active spread, privileged access, and regulated data (score 23, correctly classified Critical).

## Scope Note

This is a fast first-pass triage aid, not a comprehensive risk model — re-assess as more information comes in during the response, using the [playbook tracker](../playbook-tracker/) to log how the incident actually evolves.

---
*Part of the [incident-response-playbooks](../../README.md) repository.*
