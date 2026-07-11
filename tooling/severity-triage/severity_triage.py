#!/usr/bin/env python3
"""
severity_triage.py — Structured initial severity scoring for a new incident.

Why this exists: severity classification under pressure tends to default to
either "everything is critical" (alert fatigue for leadership) or
"everything is low until proven otherwise" (dangerous under-response). A
short structured scoring pass takes 60 seconds and produces a defensible,
consistent classification instead of a gut call that varies by who's on
shift.

This intentionally does NOT try to be a full risk model — it's a fast
first-pass triage aid, meant to be run in the first few minutes of an
incident and revisited as more information comes in (see playbook_tracker.py
for tracking the response once triage is done).

Usage (interactive):
    python3 severity_triage.py

Usage (scripted, e.g. from a SOAR playbook):
    python3 severity_triage.py --systems-affected 3 --data-sensitivity high \\
        --business-criticality high --spreading true --privileged-access true \\
        --output triage_result.json
"""

import argparse
import json
import sys

# Each factor contributes points; total maps to a severity band.
# Weights reflect that privileged access and active spread are the two
# strongest predictors of an incident escalating quickly if not contained
# fast, so they're weighted higher than static scope factors.
WEIGHTS = {
    "systems_affected": {1: 0, "2-5": 2, "6+": 4},
    "data_sensitivity": {"none": 0, "internal": 1, "confidential": 3, "regulated": 5},
    "business_criticality": {"low": 0, "medium": 2, "high": 4},
    "spreading": {False: 0, True: 5},
    "privileged_access": {False: 0, True: 5},
    "public_facing": {False: 0, True: 2},
}

SEVERITY_BANDS = [
    (0, 3, "Low", "Standard IR process, no escalation required"),
    (4, 8, "Medium", "Escalate to IR lead, activate war room if not already"),
    (9, 14, "High", "Executive notification, all-hands response"),
    (15, 999, "Critical", "Executive + legal notification, consider external IR support / law enforcement"),
]


def score_systems_affected(n):
    if n <= 1:
        return WEIGHTS["systems_affected"][1]
    elif n <= 5:
        return WEIGHTS["systems_affected"]["2-5"]
    else:
        return WEIGHTS["systems_affected"]["6+"]


def classify(total):
    for low, high, label, guidance in SEVERITY_BANDS:
        if low <= total <= high:
            return label, guidance
    return "Unknown", "Score out of expected range — review manually"


def compute(systems_affected, data_sensitivity, business_criticality, spreading, privileged_access, public_facing):
    breakdown = {
        "systems_affected": score_systems_affected(systems_affected),
        "data_sensitivity": WEIGHTS["data_sensitivity"][data_sensitivity],
        "business_criticality": WEIGHTS["business_criticality"][business_criticality],
        "spreading": WEIGHTS["spreading"][spreading],
        "privileged_access": WEIGHTS["privileged_access"][privileged_access],
        "public_facing": WEIGHTS["public_facing"][public_facing],
    }
    total = sum(breakdown.values())
    label, guidance = classify(total)
    return {
        "inputs": {
            "systems_affected": systems_affected,
            "data_sensitivity": data_sensitivity,
            "business_criticality": business_criticality,
            "spreading": spreading,
            "privileged_access": privileged_access,
            "public_facing": public_facing,
        },
        "score_breakdown": breakdown,
        "total_score": total,
        "severity": label,
        "guidance": guidance,
    }


def interactive():
    print("=== Incident Severity Triage ===\n")
    systems_affected = int(input("How many systems are affected? [number]: ").strip())
    data_sensitivity = input("Data sensitivity involved? [none/internal/confidential/regulated]: ").strip().lower()
    business_criticality = input("Business criticality of affected systems? [low/medium/high]: ").strip().lower()
    spreading = input("Is it actively spreading right now? [y/n]: ").strip().lower().startswith("y")
    privileged_access = input("Does the attacker/malware have privileged access (admin/domain admin/root)? [y/n]: ").strip().lower().startswith("y")
    public_facing = input("Are public-facing systems involved? [y/n]: ").strip().lower().startswith("y")
    return compute(systems_affected, data_sensitivity, business_criticality, spreading, privileged_access, public_facing)


def print_result(result):
    print("\n=== Triage Result ===")
    print(f"Total score: {result['total_score']}")
    print(f"Severity: {result['severity']}")
    print(f"Guidance: {result['guidance']}")
    print("\nScore breakdown:")
    for k, v in result["score_breakdown"].items():
        print(f"  {k}: {v}")


def main():
    parser = argparse.ArgumentParser(description="Structured initial severity scoring for a new incident")
    parser.add_argument("--systems-affected", type=int)
    parser.add_argument("--data-sensitivity", choices=["none", "internal", "confidential", "regulated"])
    parser.add_argument("--business-criticality", choices=["low", "medium", "high"])
    parser.add_argument("--spreading", type=lambda x: x.lower() == "true")
    parser.add_argument("--privileged-access", type=lambda x: x.lower() == "true")
    parser.add_argument("--public-facing", type=lambda x: x.lower() == "true", default=False)
    parser.add_argument("--output", help="Optional path to write JSON result")
    args = parser.parse_args()

    if args.systems_affected is not None:
        result = compute(
            args.systems_affected,
            args.data_sensitivity,
            args.business_criticality,
            args.spreading,
            args.privileged_access,
            args.public_facing,
        )
    else:
        result = interactive()

    print_result(result)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\nResult written to {args.output}")


if __name__ == "__main__":
    main()
