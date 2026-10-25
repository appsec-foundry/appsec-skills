"""Deterministic change relevance, separate from weakness severity and scores."""

from __future__ import annotations

import ast
from collections import Counter, defaultdict
import difflib
import io
import json
from pathlib import Path
import re
import tokenize

from score_core import JS_EXTENSIONS, POLICY, javascript_code


CONFIG = POLICY["change_relevance"]
VERSION = CONFIG["version"]
PATH_RULES = [(rule, re.compile(rule["pattern"])) for rule in CONFIG["path_rules"]]
CODE_RULES = [(rule, re.compile(rule["pattern"])) for rule in CONFIG["code_rules"]]
DOC_PATTERN = re.compile(CONFIG["documentation_rule"]["pattern"])
LEVELS = {"high": 0, "medium": 1, "low": 2, "unclear": 3}


def same_program(path, old, new):
    """Only make a non-functional claim where a parser supports that claim."""
    if old.get("fragment") or new.get("fragment"):
        return False
    if old["text"] == new["text"]:
        return True
    try:
        if Path(path).suffix.lower() == ".py":
            return ast.dump(
                ast.parse(old["text"]), include_attributes=False
            ) == ast.dump(ast.parse(new["text"]), include_attributes=False)
        if Path(path).suffix.lower() == ".json":
            # Preserve duplicate keys, ordering and number representation types.
            options = {"object_pairs_hook": lambda pairs: ("object", pairs)}
            return repr(json.loads(old["text"], **options)) == repr(
                json.loads(new["text"], **options)
            )
    except (SyntaxError, ValueError, RecursionError):
        pass
    return False


def active_lines(path, text):
    if Path(path).suffix.lower() in JS_EXTENSIONS | {
        ".java",
        ".kt",
        ".cs",
        ".go",
        ".rs",
        ".php",
    }:
        try:
            return javascript_code(text).splitlines()
        except SyntaxError:
            return []
    if Path(path).suffix.lower() == ".py":
        lines = text.splitlines()
        try:
            for token in tokenize.generate_tokens(io.StringIO(text).readline):
                if token.type == tokenize.COMMENT:
                    row, column = token.start
                    lines[row - 1] = lines[row - 1][:column]
        except (tokenize.TokenError, IndentationError, SyntaxError):
            pass
        return lines
    return text.splitlines()


def delta(old, new, budget):
    sources = (old or {"text": ""}, new or {"text": ""})
    lines = [source["text"].splitlines() for source in sources]
    changed = [set(), set()]
    uncertain = False
    if any(source.get("fragment") for source in sources):
        for side, source in enumerate(sources):
            selected = set(source.get("changed_lines", []))
            changed[side] = {
                index
                for index in range(len(lines[side]))
                if source.get("lines", {}).get(index + 1, index + 1) in selected
            }
    elif max(map(len, lines), default=0) > 10000:
        changed = [set(range(len(rows))) for rows in lines]
        uncertain = True
    else:
        budget.check()
        for tag, start_old, end_old, start_new, end_new in difflib.SequenceMatcher(
            None, *lines, autojunk=True
        ).get_opcodes():
            if tag != "equal":
                changed[0].update(range(start_old, end_old))
                changed[1].update(range(start_new, end_new))
        budget.check()
    contexts = []
    for rows, indices, source in zip(lines, changed, sources):
        context = set()
        for index in indices:
            context.update(range(max(0, index - 2), min(len(rows), index + 3)))
        contexts.append(
            {source.get("lines", {}).get(index + 1, index + 1) for index in context}
        )
    return lines, changed, contexts, uncertain


def analyze(before, after, checks, findings, exclusions, budget, *, complete=True):
    signals, seen = [], set()
    strongest = None
    truncated = False
    contexts = {"baseline": {}, "proposed": {}}
    nonfunctional = []
    unclassified = []
    changed_files = []
    uncertain_paths = {row["file"] for row in exclusions}
    checks_by_file = defaultdict(list)
    for check in checks:
        checks_by_file[check["file"]].append(check)

    def add(rule, path, side="metadata", line=0, relation="changed"):
        nonlocal strongest, truncated
        key = rule["id"], path, side
        stronger = strongest is None or LEVELS[rule["level"]] < LEVELS[strongest]
        if stronger:
            strongest = rule["level"]
        if key in seen:
            return
        seen.add(key)
        if len(signals) >= 1000:
            truncated = True
            if not stronger:
                return
            # Always retain evidence explaining the headline level.
            signals.pop()
        signals.append(
            {
                "rule": rule["id"],
                "level": rule["level"],
                "aspect": rule["aspect"],
                "reason": rule["reason"],
                "file": path,
                "line": line,
                "side": side,
                "relation": relation,
            }
        )

    paths = sorted(set(before) | set(after) | uncertain_paths)
    for path in paths:
        budget.check()
        old, new = before.get(path), after.get(path)
        if (
            old is not None
            and new is not None
            and old["text"] == new["text"]
            and old.get("executable") == new.get("executable")
            and not old.get("fragment")
        ):
            continue
        changed_files.append(path)
        metadata_changed = (
            old is not None
            and new is not None
            and old.get("executable") != new.get("executable")
        )
        if metadata_changed:
            add(CONFIG["executable_rule"], path)
        if old is not None and new is not None and same_program(path, old, new):
            if not metadata_changed:
                nonfunctional.append(path)
            continue
        for rule, pattern in PATH_RULES:
            if pattern.search(path):
                add(rule, path)
        if path in uncertain_paths:
            unclassified.append(path)
        if old is None and new is None:
            continue
        lines, changed, context, complex_diff = delta(old, new, budget)
        for side, selected in zip(("baseline", "proposed"), context):
            contexts[side][path] = selected
        if complex_diff:
            unclassified.append(path)
        is_document = Path(path).suffix.lower() in CONFIG["documentation_extensions"]
        before_signal_count = len(seen)
        for side_index, (side, source) in enumerate(
            (("baseline", old), ("proposed", new))
        ):
            if source is None:
                continue
            active = (
                lines[side_index] if is_document else active_lines(path, source["text"])
            )
            selected_indices = (
                changed[side_index]
                if is_document
                else {
                    index
                    for index in range(len(active))
                    if source.get("lines", {}).get(index + 1, index + 1)
                    in context[side_index]
                }
            )
            for index in sorted(selected_indices):
                budget.check()
                if index >= len(active):
                    continue
                actual_line = source.get("lines", {}).get(index + 1, index + 1)
                if is_document:
                    if DOC_PATTERN.search(active[index]):
                        add(CONFIG["documentation_rule"], path, side, actual_line)
                else:
                    for rule, pattern in CODE_RULES:
                        if pattern.search(active[index]):
                            add(
                                rule,
                                path,
                                side,
                                actual_line,
                                "changed"
                                if index in changed[side_index]
                                else "near changed lines",
                            )
        for check in checks_by_file[path]:
            side = check.get("side", "proposed")
            for location in check.get("locations", []):
                if (
                    location["line"] in contexts[side].get(path, set())
                    and check["area"] in CONFIG["area_rules"]
                ):
                    rule = CONFIG["area_rules"][check["area"]]
                    add(rule, path, side, location["line"], "in or near changed lines")
        if is_document and path not in uncertain_paths:
            nonfunctional.append(path)
        elif not metadata_changed and len(seen) == before_signal_count:
            unclassified.append(path)
    if strongest is not None:
        relevance = strongest
    elif complete and not unclassified and not uncertain_paths:
        relevance = "low"
    else:
        relevance = "unclear"
    visible_findings = [
        finding
        for finding in findings
        if finding.get("change") != "pre_existing"
        or finding["line"]
        in contexts[finding.get("side", "proposed")].get(finding["file"], set())
    ]
    outcomes = Counter(row["status"] for row in checks)
    counts = Counter(
        finding.get("change", "unresolved") for finding in visible_findings
    )
    return {
        "analysis": "change-relevance",
        "relevance_version": VERSION,
        "verdict": "complete" if complete else "incomplete",
        "relevance": relevance,
        "signals": signals,
        "findings": visible_findings,
        "finding_changes": dict(sorted(counts.items())),
        "aspects": sorted({signal["aspect"] for signal in signals}),
        "coverage": {
            "check_outcomes": dict(sorted(outcomes.items())),
            "changed_files": changed_files,
            "nonfunctional_or_documentation": sorted(set(nonfunctional)),
            "unclassified_files": sorted(set(unclassified)),
            "signals_truncated": truncated,
            "basis": "Changed lines, bounded nearby control observations and known sensitive file types. Unrecognized behavior remains unclear.",
        },
    }
