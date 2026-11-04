#!/usr/bin/env python3
"""Deterministic checks for the dialogue of a create-threat-model run.

Usage: check_transcript.py ROLLOUT.jsonl [--no-code] [--scenario-bound]
                           [--max-questions 3] [--max-words 40] [--json]

Reads a Codex rollout transcript (~/.codex/sessions/.../rollout-*.jsonl),
extracts the question rounds, assistant messages, and writes to the model
file, and checks the interview rules of the skill. The checks cover form,
not whether a question was sensible. Exit code 1 when an error was found.
"""

import argparse
import json
import re
import sys
from pathlib import Path

SCENARIO_OR_ITEM = re.compile(r"\b(T|C|P|PAC|AC)-\d{2,3}\b")
PERMISSION_START = re.compile(r"^\s*(may i|should i|which file|do you want|darf ich|soll ich|welche datei)\b", re.IGNORECASE)
AUDIENCE_HINT = re.compile(r"read this threat model|who should be able to read|lesen (darf|soll|dürfen)|public", re.IGNORECASE)
READING_HINT = re.compile(r"(read|lesen).{0,60}(code|quellcode|source)", re.IGNORECASE)
OPEN_ANSWER_HINT = re.compile(r"unknown|short answer|unbekannt|kurze antwort|one sentence|ein satz", re.IGNORECASE)
MODEL_WRITE = re.compile(r"\*\*\* (Add|Update) File: .*threat-model\.md")
VERSION_BANNER = re.compile(r"Version \d+\.\d+")


def load_events(path):
    """Return the ordered list of (kind, data) events relevant to the checks."""
    events = []
    with path.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            payload = record.get("payload") or {}
            kind = payload.get("type")
            if kind == "function_call" and "request_user_input" in (payload.get("name") or ""):
                try:
                    arguments = json.loads(payload.get("arguments") or "{}")
                except json.JSONDecodeError:
                    continue
                questions = arguments.get("questions") or []
                if questions:
                    events.append(("round", questions))
            elif kind == "message" and payload.get("role") == "assistant":
                text = "\n".join(
                    part.get("text", "") for part in payload.get("content", []) if isinstance(part, dict)
                )
                events.append(("message", text))
            elif kind in ("custom_tool_call", "function_call"):
                blob = payload.get("input") or payload.get("arguments") or ""
                if MODEL_WRITE.search(blob.replace("\\n", "\n")):
                    events.append(("write", payload.get("name")))
    return events


def question_text(question):
    return (question.get("title") or question.get("question") or "").strip()


def check_transcript(events, no_code=False, scenario_bound=False, max_questions=3, max_words=40):
    findings = []

    def add(level, code, message):
        findings.append({"level": level, "code": code, "message": message})

    rounds = 0
    seen_titles = {}
    audience_rounds = 0
    candidates_shown = False
    first_message_checked = False
    writes = 0
    questions_after_write = 0
    questions_before_candidates = 0
    total_questions = 0

    for kind, data in events:
        if kind == "message":
            if not first_message_checked and data.strip():
                first_message_checked = True
                if not VERSION_BANNER.search(data):
                    add("error", "Q09", "first assistant message does not show the skill name and version (REQ-16)")
            if len(set(re.findall(r"\bT-\d{3}\b", data))) >= 2:
                candidates_shown = True
            continue
        if kind == "write":
            writes += 1
            continue

        rounds += 1
        total_questions += len(data)
        if writes:
            questions_after_write += len(data)
        if not candidates_shown:
            questions_before_candidates += len(data)
        if len(data) > max_questions:
            add("error", "Q01", f"round {rounds} has {len(data)} questions (limit {max_questions})")
        for question in data:
            title = question_text(question)
            options = [str(o) for o in (question.get("options") or [])]
            label = f"round {rounds}: '{title[:70]}'"
            count = len(re.findall(r"\S+", title))
            if count > max_words:
                add("error", "Q02", f"{label} has {count} words (limit {max_words})")
            if title.count("?") > 1:
                add("warning", "Q11", f"{label} asks more than one question")
            if not options and not OPEN_ANSWER_HINT.search(title):
                add("warning", "Q03", f"{label} has no options and does not say that a short or unknown answer suffices")
            key = re.sub(r"\s+", " ", title.lower())
            if key in seen_titles:
                add("error", "Q04", f"{label} repeats the question from round {seen_titles[key]}")
            else:
                seen_titles[key] = rounds
            if AUDIENCE_HINT.search(title) or any(re.match(r"public\b", o, re.IGNORECASE) for o in options):
                audience_rounds += 1
                if audience_rounds > 1:
                    add("error", "Q05", f"{label} asks about the audience again")
            if no_code and READING_HINT.search(title):
                add("error", "Q06", f"{label} asks for code-reading permission although the target has no code")
            if scenario_bound and candidates_shown:
                if not SCENARIO_OR_ITEM.search(title) and not PERMISSION_START.match(title):
                    add("error", "Q07", f"{label} is not bound to a scenario or checklist item")

    summary = {
        "rounds": rounds,
        "questions": total_questions,
        "questions_before_candidates": questions_before_candidates,
        "model_writes": writes,
        "questions_after_first_write": questions_after_write,
    }
    return findings, summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("transcript", type=Path)
    parser.add_argument("--no-code", action="store_true", help="the target has no implementation")
    parser.add_argument("--scenario-bound", action="store_true",
                        help="after threat candidates were shown, every question must name a T-, C-, or P- ID")
    parser.add_argument("--max-questions", type=int, default=3)
    parser.add_argument("--max-words", type=int, default=40)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if not args.transcript.is_file():
        parser.error(f"{args.transcript} is not a file")
    events = load_events(args.transcript)
    findings, summary = check_transcript(events, args.no_code, args.scenario_bound,
                                         args.max_questions, args.max_words)
    errors = [f for f in findings if f["level"] == "error"]
    if args.json:
        print(json.dumps({"findings": findings, "summary": summary}, indent=2))
    else:
        for finding in findings:
            print(f"{finding['level'].upper()} {finding['code']} {finding['message']}")
        print(", ".join(f"{k} {v}" for k, v in summary.items()))
        print(f"{len(errors)} errors, {len(findings) - len(errors)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
