"""Deterministic change relevance, separate from weakness severity and scores."""

from __future__ import annotations

import ast
from bisect import bisect_left, bisect_right
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
MAX_CONTEXT_LINES = 200
MAX_CONTEXT_FILE_LINES = 10000
BRACE_LANGUAGES = JS_EXTENSIONS | {".java", ".kt", ".cs", ".go", ".rs", ".php"}
FUNCTION_HEADER = re.compile(
    r"(?:\bfunction\s*(?:\w+)?\s*\([^{};]*\)"
    r"|\bfunc\s+(?:\([^{};]*\)\s*)?\w+\s*\([^{};]*\)[^{};]*"
    r"|\b(?P<method>[A-Za-z_$][\w$]*)\s*\([^{};]*\)"
    r"(?:\s*(?::|->)\s*[^{};=]+)?(?:\s+throws\s+[\w., ]+)?"
    r"|(?:\([^{};]*\)|\b\w+)\s*=>)\s*$"
)


def function_spans(path, text, active, budget):
    """Return bounded-source function extents, without importing target code."""
    if Path(path).suffix.lower() == ".py":
        try:
            tree = ast.parse(text)
        except (SyntaxError, ValueError, RecursionError):
            return []
        spans = []
        for node in ast.walk(tree):
            budget.check()
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                start = min(
                    [node.lineno, *(item.lineno for item in node.decorator_list)]
                )
                spans.append((start - 1, node.end_lineno - 1, node.body[0].lineno - 2))
        return spans
    if Path(path).suffix.lower() not in BRACE_LANGUAGES:
        return []
    # Strings/comments have already been masked. Only balanced function bodies
    # qualify; an if/for/class block must not become a function context.
    code = "\n".join(active)
    line_starts = [0, *(match.end() for match in re.finditer("\n", code))]
    stack, spans = [], []
    previous = 0
    for match in re.finditer(r"[{};]", code):
        budget.check()
        token, offset = match[0], match.start()
        if token == "{":
            header_start = max(previous, offset - 1000)
            header = code[header_start:offset]
            signature = FUNCTION_HEADER.search(header)
            is_function = signature and signature.group("method") not in {
                "if",
                "for",
                "while",
                "switch",
                "catch",
                "with",
                "synchronized",
            }
            if is_function:
                start = bisect_right(line_starts, header_start + signature.start()) - 1
                # Include adjacent annotations/attributes such as @GetMapping or
                # [Authorize], while staying inside this declaration's header.
                first_header_line = bisect_right(line_starts, header_start) - 1
                while start > first_header_line and active[
                    start - 1
                ].lstrip().startswith(("@", "[")):
                    start -= 1
                stack.append((start, bisect_right(line_starts, offset) - 1))
            else:
                stack.append(None)
        elif token == "}" and stack:
            scope = stack.pop()
            if scope is not None:
                start, header_end = scope
                spans.append((start, bisect_right(line_starts, offset) - 1, header_end))
        previous = match.end()
    return spans


def code_context(path, source, changed_indices, budget):
    """Select changed/nearby lines and enclosing functions; keep hunks isolated.

    Function bodies over 200 lines contribute their header only, in addition to
    changed/nearby lines. Partial patches never invent a containing function.
    """
    actual = source.get("lines", {})
    changed_lines = {actual.get(index + 1, index + 1) for index in changed_indices}
    selected, locations = [], set()
    limited = False
    for segment in source.get("fragments", [source]):
        budget.check()
        text = segment["text"]
        active = active_lines(path, text)
        mapping = segment.get("lines", {})
        changed = [
            index
            for index in range(len(active))
            if mapping.get(index + 1, index + 1) in changed_lines
        ]
        spans = []
        if not segment.get("fragment") and len(active) <= MAX_CONTEXT_FILE_LINES:
            spans = function_spans(path, text, active, budget)
        elif len(active) > MAX_CONTEXT_FILE_LINES:
            limited = True
        # Choose the innermost function for each changed line. A nearby sibling
        # function is not evidence about the changed function.
        owners = {}
        for start, end, header_end in spans:
            budget.check()
            for index in changed[
                bisect_left(changed, start) : bisect_right(changed, end)
            ]:
                if (
                    index not in owners
                    or end - start < owners[index][1] - owners[index][0]
                ):
                    owners[index] = (start, end, header_end)
        context = {}
        for index in changed:
            start, end, _ = owners.get(index, (0, len(active) - 1, 0))
            for neighbor in range(max(start, index - 2), min(end + 1, index + 3)):
                context[neighbor] = "near changed lines"
        for start, end, header_end in set(owners.values()):
            if end - start + 1 > MAX_CONTEXT_LINES:
                limited = True
                end = min(header_end, start + 19)
            for index in range(start, end + 1):
                context.setdefault(index, "in changed function")
        for index in changed:
            context[index] = "changed"
        for index, relation in sorted(context.items()):
            line = mapping.get(index + 1, index + 1)
            selected.append((line, active[index], relation))
            locations.add(line)
    return selected, locations, limited


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
    context_limited = []
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
            if is_document:
                selected = [
                    (
                        source.get("lines", {}).get(index + 1, index + 1),
                        lines[side_index][index],
                        "changed",
                    )
                    for index in sorted(changed[side_index])
                ]
            else:
                selected, contexts[side][path], limited = code_context(
                    path, source, changed[side_index], budget
                )
                if limited:
                    context_limited.append(path)
            for actual_line, content, relation in selected:
                budget.check()
                if is_document:
                    if DOC_PATTERN.search(content):
                        add(CONFIG["documentation_rule"], path, side, actual_line)
                else:
                    for rule, pattern in CODE_RULES:
                        if pattern.search(content):
                            add(
                                rule,
                                path,
                                side,
                                actual_line,
                                relation,
                            )
        for check in checks_by_file[path]:
            side = check.get("side", "proposed")
            for location in check.get("locations", []):
                if (
                    location["line"] in contexts[side].get(path, set())
                    and check["area"] in CONFIG["area_rules"]
                ):
                    rule = CONFIG["area_rules"][check["area"]]
                    add(
                        rule, path, side, location["line"], "in affected change context"
                    )
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
            "context_limited_files": sorted(set(context_limited)),
            "basis": "Indication from changed lines, bounded enclosing-function context and security-related paths/configuration. Unrecognized behavior remains unclear; signals do not establish a defect or verified security impact.",
        },
    }
