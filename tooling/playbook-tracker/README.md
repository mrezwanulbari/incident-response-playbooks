# Playbook Execution Tracker

A stdlib-only Python CLI for tracking live execution of an IR playbook against a real incident — logs phase timestamps (detection, containment, eradication, recovery) and computes time-to-containment/eradication/recovery metrics automatically.

## Why This Exists

A playbook is documentation until someone runs it during a real incident. This tool turns "we followed the ransomware playbook" into a timestamped, exportable record — which is both a stronger input for post-incident review and the raw material for the "Timeline of Events" section of a full report.

## Usage

```bash
python3 playbook_tracker.py init

python3 playbook_tracker.py start-incident --name "INC-2026-021" --playbook ransomware --description "Encryption detected on FIN-WKS-014"

python3 playbook_tracker.py log-phase --incident-id 1 --phase containment --note "Host isolated via EDR"
python3 playbook_tracker.py log-phase --incident-id 1 --phase eradication --note "Persistence mechanism removed"
python3 playbook_tracker.py log-phase --incident-id 1 --phase recovery --note "Restored from verified backup"

python3 playbook_tracker.py list-incidents
python3 playbook_tracker.py report --incident-id 1 --output incident_1_report.json
```

## Metrics Computed

- **Time to containment** — from detection (incident start) to first containment log
- **Time to eradication** — from detection to first eradication log
- **Time to recovery** — from detection to first recovery log

These are the standard metrics used to track IR program maturity over time — trending them across incidents (not just looking at one in isolation) is what shows whether response capability is actually improving.

## Data Export

`report --output` produces a JSON export validated against [`schema/incident-export-schema.json`](../../schema/incident-export-schema.json).

## Tested

Verified end-to-end: incident creation, phase logging across all four phases, metrics computation, and JSON export — all confirmed producing correct output including accurate elapsed-time calculations.

---
*Part of the [incident-response-playbooks](../../README.md) repository.*
