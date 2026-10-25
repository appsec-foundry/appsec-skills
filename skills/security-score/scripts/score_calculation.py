"""Repository score arithmetic; editable values live at the top of rules.json.

Each finding deducts its severity's weight. Add deductions within each area,
apply the strictest severity cap, and use the lowest assessed area score.
Control recognition and source scanning belong to score_core, not this module.
"""

from collections import Counter
import json
import math
from pathlib import Path


CATALOG_BYTES = (Path(__file__).resolve().parent.parent / "rules.json").read_bytes()
POLICY = json.loads(CATALOG_BYTES)
VERSION = POLICY["scoring_version"]
WEIGHTS = POLICY["scoring"]["weights"]
CAPS = POLICY["scoring"]["severity_caps"]


def validate_scoring():
    if set(WEIGHTS) != {"critical", "high", "medium", "low"} or set(CAPS) != set(
        WEIGHTS
    ):
        raise ValueError("Invalid scoring severity policy.")
    if any(
        type(value) is not int or not 1 <= value <= 100 for value in WEIGHTS.values()
    ):
        raise ValueError("Weights must be whole points in 1–100.")
    if any(type(value) is not int or not 0 <= value <= 100 for value in CAPS.values()):
        raise ValueError("Severity caps must be integers in 0–100.")
    if POLICY["scoring"]["grade_bands"] != [
        [90, "A"],
        [80, "B"],
        [70, "C"],
        [60, "D"],
        [50, "E"],
        [0, "F"],
    ]:
        raise ValueError("Grade bands must match REQ-03.")
    if (
        POLICY["scoring"]["aggregation"] != "weakest assessed area"
        or POLICY["scoring"]["repetitions"] != "weight * instances"
    ):
        raise ValueError(
            "Unsupported score formula; update score_calculation.py to change it."
        )


def grade(score):
    if score is None:
        return None
    if (
        type(score) not in {int, float}
        or not math.isfinite(score)
        or not 0 <= score <= 100
    ):
        raise ValueError("score outside 0–100")
    for minimum, letter in POLICY["scoring"]["grade_bands"]:
        if score >= minimum:
            return letter
    raise ValueError("score outside 0–100")


def calculate_area(area, findings, *, assessed):
    """Keep the arithmetic and its published explanation on the same path."""
    counts = Counter((finding["rule"], finding["severity"]) for finding in findings)
    breakdown = [
        {
            "rule": rule,
            "severity": severity,
            "instances": count,
            "points_per_instance": WEIGHTS[severity],
            "deduction": count * WEIGHTS[severity],
            "severity_cap": CAPS[severity],
        }
        for (rule, severity), count in sorted(counts.items())
    ]
    deduction = sum(row["deduction"] for row in breakdown)
    cap = min((row["severity_cap"] for row in breakdown), default=100)
    score = max(0, min(100 - deduction, cap))
    return {
        "area": area,
        "score": score if assessed else None,
        "deduction": deduction,
        "severity_cap": cap,
        "breakdown": breakdown,
    }


def calculate(findings, checks, *, complete=True, require_source=False):
    """Score recognized evidence only; retain coverage gates independently of points."""
    statuses = Counter(row["status"] for row in checks)
    areas = sorted(
        {row["area"] for row in checks if row["status"] != "not_applicable"}
        | {finding["area"] for finding in findings}
    )
    assessed = {
        row["area"] for row in checks if row["status"] in {"satisfied", "violated"}
    } | {finding["area"] for finding in findings}
    rows = [
        calculate_area(
            area,
            [finding for finding in findings if finding["area"] == area],
            assessed=area in assessed,
        )
        for area in areas
    ]
    known = sum(
        row["status"] in {"satisfied", "violated"}
        and (not require_source or row["area"] != "repository-host")
        for row in checks
    )
    verdict = "incomplete" if not complete else "scored" if known else "undetermined"
    score = (
        min((row["score"] for row in rows if row["score"] is not None), default=None)
        if verdict == "scored"
        else None
    )
    if verdict != "scored":
        for row in rows:
            row["score"] = None
    return {
        "verdict": verdict,
        "score": score,
        "grade": grade(score),
        "areas": rows,
        "coverage": {
            "check_outcomes": dict(sorted(statuses.items())),
            "scored_findings": len(findings),
            "basis": "Recognized operations only; aliases and wider application controls may be uncovered.",
        },
    }
