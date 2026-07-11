#!/usr/bin/env python3
"""
playbook_tracker.py — Track live execution of an IR playbook against a real
incident: log phase timestamps, compute time-to-containment/time-to-recovery
metrics, and export a timeline for the post-incident report.

Why this exists: playbooks are documentation until someone is actually
running one during an incident. This tool turns "we followed the ransomware
playbook" into a timestamped record of exactly when detection, containment,
eradication, and recovery each happened — which is both a stronger metric
for post-incident review and the raw material for the "Timeline of Events"
section of a report (see the DFIR toolkit's report template).

Requires: Python 3.8+, standard library only.

Usage:
    python3 playbook_tracker.py init
    python3 playbook_tracker.py start-incident --name "INC-2026-021" --playbook ransomware --description "Encryption detected on FIN-WKS-014"
    python3 playbook_tracker.py log-phase --incident-id 1 --phase containment --note "Host isolated via EDR"
    python3 playbook_tracker.py log-phase --incident-id 1 --phase eradication --note "Persistence mechanism removed"
    python3 playbook_tracker.py log-phase --incident-id 1 --phase recovery --note "Restored from verified backup"
    python3 playbook_tracker.py close-incident --incident-id 1
    python3 playbook_tracker.py report --incident-id 1
"""

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path.home() / ".ir_playbook_tracker" / "incidents.db"

VALID_PHASES = ["detection", "containment", "eradication", "recovery", "post_incident"]


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db():
    conn = get_connection()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            playbook TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'active',
            started_at TEXT NOT NULL,
            closed_at TEXT
        );

        CREATE TABLE IF NOT EXISTS phase_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_id INTEGER NOT NULL,
            phase TEXT NOT NULL,
            note TEXT,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (incident_id) REFERENCES incidents(id)
        );
        """
    )
    conn.commit()
    conn.close()
    print(f"Initialized incident tracking database at {DB_PATH}")


def now():
    return datetime.now(timezone.utc).isoformat()


def start_incident(args):
    conn = get_connection()
    ts = now()
    try:
        conn.execute(
            "INSERT INTO incidents (name, playbook, description, status, started_at) VALUES (?, ?, ?, 'active', ?)",
            (args.name, args.playbook, args.description, ts),
        )
        conn.commit()
        incident_id = conn.execute("SELECT id FROM incidents WHERE name = ?", (args.name,)).fetchone()[0]
        # Detection is implicitly logged as the start event
        conn.execute(
            "INSERT INTO phase_log (incident_id, phase, note, timestamp) VALUES (?, 'detection', ?, ?)",
            (incident_id, "Incident tracking started", ts),
        )
        conn.commit()
        print(f"Started incident '{args.name}' (playbook: {args.playbook}) with ID {incident_id}")
    except sqlite3.IntegrityError:
        print(f"Error: an incident named '{args.name}' already exists", file=sys.stderr)
        sys.exit(1)
    finally:
        conn.close()


def log_phase(args):
    if args.phase not in VALID_PHASES:
        print(f"Error: phase must be one of {VALID_PHASES}", file=sys.stderr)
        sys.exit(1)

    conn = get_connection()
    incident = conn.execute("SELECT id, name FROM incidents WHERE id = ?", (args.incident_id,)).fetchone()
    if not incident:
        print(f"Error: no incident found with ID {args.incident_id}", file=sys.stderr)
        sys.exit(1)

    conn.execute(
        "INSERT INTO phase_log (incident_id, phase, note, timestamp) VALUES (?, ?, ?, ?)",
        (args.incident_id, args.phase, args.note, now()),
    )
    conn.commit()
    conn.close()
    print(f"Logged phase '{args.phase}' for incident {args.incident_id} ({incident[1]})")


def close_incident(args):
    conn = get_connection()
    conn.execute("UPDATE incidents SET status = 'closed', closed_at = ? WHERE id = ?", (now(), args.incident_id))
    conn.commit()
    conn.close()
    print(f"Closed incident {args.incident_id}")


def list_incidents(args):
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, name, playbook, status, started_at FROM incidents ORDER BY started_at DESC"
    ).fetchall()
    conn.close()
    if not rows:
        print("No incidents found.")
        return
    for r in rows:
        print(f"[{r[0]}] {r[1]}  playbook={r[2]}  status={r[3]}  started={r[4]}")


def compute_metrics(phase_rows):
    """Compute time-to-X metrics from ordered phase log entries."""
    phase_times = {}
    for phase, ts in phase_rows:
        ts_parsed = datetime.fromisoformat(ts)
        if phase not in phase_times:  # first occurrence of each phase
            phase_times[phase] = ts_parsed

    metrics = {}
    if "detection" in phase_times and "containment" in phase_times:
        delta = phase_times["containment"] - phase_times["detection"]
        metrics["time_to_containment"] = str(delta)
    if "detection" in phase_times and "eradication" in phase_times:
        delta = phase_times["eradication"] - phase_times["detection"]
        metrics["time_to_eradication"] = str(delta)
    if "detection" in phase_times and "recovery" in phase_times:
        delta = phase_times["recovery"] - phase_times["detection"]
        metrics["time_to_recovery"] = str(delta)
    return metrics, phase_times


def report(args):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    incident = conn.execute("SELECT * FROM incidents WHERE id = ?", (args.incident_id,)).fetchone()
    if not incident:
        print(f"Error: no incident found with ID {args.incident_id}", file=sys.stderr)
        sys.exit(1)

    phases = conn.execute(
        "SELECT phase, note, timestamp FROM phase_log WHERE incident_id = ? ORDER BY timestamp",
        (args.incident_id,),
    ).fetchall()
    conn.close()

    print(f"\n=== Incident Report: {incident['name']} ===")
    print(f"Playbook: {incident['playbook']}")
    print(f"Status: {incident['status']}")
    print(f"Description: {incident['description'] or '(none)'}")

    print(f"\nPhase Timeline:")
    for p in phases:
        print(f"  [{p['timestamp']}] {p['phase']:15s} {p['note'] or ''}")

    metrics, _ = compute_metrics([(p["phase"], p["timestamp"]) for p in phases])
    print(f"\nMetrics:")
    if metrics:
        for k, v in metrics.items():
            print(f"  {k}: {v}")
    else:
        print("  (insufficient phase data to compute metrics yet)")

    if args.output:
        export = {
            "incident": dict(incident),
            "phases": [dict(p) for p in phases],
            "metrics": metrics,
        }
        with open(args.output, "w") as f:
            json.dump(export, f, indent=2)
        print(f"\nExported full report to {args.output}")


def build_parser():
    parser = argparse.ArgumentParser(description="IR playbook execution tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Initialize the local database").set_defaults(func=lambda a: init_db())

    p = sub.add_parser("start-incident", help="Start tracking a new incident")
    p.add_argument("--name", required=True)
    p.add_argument("--playbook", required=True, help="e.g. ransomware, phishing-bec, cloud-compromise")
    p.add_argument("--description", default="")
    p.set_defaults(func=start_incident)

    p = sub.add_parser("log-phase", help=f"Log a phase transition ({', '.join(VALID_PHASES)})")
    p.add_argument("--incident-id", type=int, required=True)
    p.add_argument("--phase", required=True)
    p.add_argument("--note", default="")
    p.set_defaults(func=log_phase)

    p = sub.add_parser("close-incident", help="Mark an incident as closed")
    p.add_argument("--incident-id", type=int, required=True)
    p.set_defaults(func=close_incident)

    sub.add_parser("list-incidents", help="List all tracked incidents").set_defaults(func=list_incidents)

    p = sub.add_parser("report", help="Print timeline and time-to-X metrics for an incident")
    p.add_argument("--incident-id", type=int, required=True)
    p.add_argument("--output", help="Optional path to export full JSON report")
    p.set_defaults(func=report)

    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
