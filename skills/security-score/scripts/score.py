#!/usr/bin/env python3
"""Standalone security score. Requires only Python 3.10+; Git for comparisons."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import threading
from urllib.parse import urlsplit

try:
    from score_core import (
        CATALOG_HASH,
        IMPLEMENTATION_HASH,
        POLICY,
        RULES,
        RULE_VERSION,
        ScanLimit,
        VERSION,
        calculate,
        compare,
        grade,
        scan,
    )
except (
    OSError,
    ValueError,
    KeyError,
    TypeError,
    AttributeError,
    RecursionError,
    re.error,
):
    print(
        "Invalid bundled rule catalog. Check rules.json and the scoring policy before running again.",
        file=sys.stderr,
    )
    raise SystemExit(1) from None
from score_sources import Budget, SourceError, command, fingerprint, select
from score_architecture import describe
from score_relevance import VERSION as RELEVANCE_VERSION, analyze as analyze_relevance
from score_remote import (
    host_settings,
    read_token,
    repository_url,
    select_remote,
    settings_checks,
)


class Progress:
    """Keep quick runs quiet; show a single progress line for longer work."""

    def __enter__(self):
        self.timer = threading.Timer(
            1.0,
            lambda: print(
                "Security checks are running...", file=sys.stderr, flush=True
            ),
        )
        self.timer.daemon = True
        self.timer.start()
        return self

    def __exit__(self, *args):
        self.timer.cancel()
        self.timer.join()


def parser():
    result = argparse.ArgumentParser(
        description="Repository scores (0–100/A–F) or change security relevance; no model calls."
    )
    result.add_argument(
        "repository",
        nargs="?",
        help="Local source directory or HTTPS GitHub/GitLab URL; defaults to the current directory",
    )
    result.add_argument("--repo", help="Alternative local repository selection")
    result.add_argument(
        "--details",
        action="store_true",
        help="Explain findings, coverage, architecture and relevance or score calculation",
    )
    result.add_argument(
        "--token-env",
        help="Environment variable holding an operator-selected read-only GitHub/GitLab API token; URL requests only",
    )
    result.add_argument(
        "--list-rules",
        action="store_true",
        help="Show the rule catalog without scanning",
    )
    result.add_argument(
        "--engine", choices=("internal", "analyzer"), default="internal"
    )
    result.add_argument(
        "--analyzer", help="Trusted operator-selected absolute Analyzer executable"
    )
    selection = result.add_mutually_exclusive_group()
    selection.add_argument(
        "--patch",
        "--diff",
        dest="patch",
        help="UTF-8 unified patch; paths are never opened",
    )
    selection.add_argument("--base", help="Base revision for a local Git comparison")
    selection.add_argument("--commit", help="Compare a commit with its first parent")
    selection.add_argument("--staged", action="store_true")
    selection.add_argument("--unstaged", action="store_true")
    selection.add_argument(
        "--worktree",
        action="store_true",
        help="HEAD versus working files, including untracked files",
    )
    result.add_argument(
        "--head", help="Proposed revision with --base; defaults to HEAD"
    )
    remote = result.add_mutually_exclusive_group()
    remote.add_argument(
        "--pr",
        help="Selected GitHub PR URL; supply its patch or local base/head comparison",
    )
    remote.add_argument(
        "--mr",
        help="Selected GitLab MR URL; supply its patch or local base/head comparison",
    )
    formatting = result.add_mutually_exclusive_group()
    formatting.add_argument("--json", action="store_true")
    formatting.add_argument("--yaml", action="store_true")
    result.add_argument(
        "--timeout",
        type=float,
        default=15,
        help="Total execution budget in seconds, 0.1–120 (default: 15)",
    )
    result.add_argument(
        "--verify-rules",
        action="store_true",
        help="Run the bundled positive/negative rule examples without scanning",
    )
    return result


def remote_identity(options):
    value = options.pr or options.mr
    if not value:
        return None
    parsed = urlsplit(value)
    host = "github.com" if options.pr else "gitlab.com"
    pattern = (
        r"/[\w.-]+/[\w.-]+/pull/[1-9]\d*"
        if options.pr
        else r"/(?:[\w.-]+/)+[\w.-]+/-/merge_requests/[1-9]\d*"
    )
    if (
        parsed.scheme != "https"
        or parsed.netloc != host
        or parsed.query
        or parsed.fragment
        or not re.fullmatch(pattern, parsed.path)
    ):
        raise SourceError(
            "Select a canonical HTTPS GitHub PR or GitLab MR URL without credentials or query parameters."
        )
    if not options.patch and not options.base:
        raise SourceError(
            "Retrieve the selected PR/MR through an authorized host tool and supply --patch or --base/--head. No implicit network retrieval is performed."
        )
    return value


def yaml_text(value, indent=0):
    """JSON-quoted scalars form a safe YAML 1.2 subset without dependencies."""
    space = " " * indent
    if isinstance(value, dict) and value:
        rows = []
        for key, child in value.items():
            name = json.dumps(str(key), ensure_ascii=True)
            if isinstance(child, (dict, list)) and child:
                rows.append(f"{space}{name}:\n{yaml_text(child, indent + 2)}")
            else:
                rows.append(
                    f"{space}{name}: {json.dumps(child, ensure_ascii=True, allow_nan=False)}"
                )
        return "\n".join(rows)
    if isinstance(value, list) and value:
        return "\n".join(
            f"{space}-\n{yaml_text(child, indent + 2)}"
            if isinstance(child, (dict, list)) and child
            else f"{space}- {json.dumps(child, ensure_ascii=True, allow_nan=False)}"
            for child in value
        )
    return space + json.dumps(value, ensure_ascii=True, allow_nan=False)


def render(result, details=False):
    if result.get("analysis") == "change-relevance":
        return render_change(result, details)
    if not details:
        return (
            f"{result['score']}/100 ({result['grade']})"
            if result["score"] is not None
            else result["verdict"]
        )
    lines = [
        f"Security score · {result['engine']} · version {result['scoring_version']}",
        f"{result['score']} / 100 · grade {result['grade']}"
        if result["score"] is not None
        else result["verdict"],
        "Limited scanner indication; no security approval or verified exploitability.",
    ]
    if result["engine"] == "analyzer":
        for entry in result.get("host_settings", []):
            lines.append(
                f"Host {entry['setting']}: {entry['status']} · {entry['reason']}"
            )
        lines += [
            "Analyzer result (separate scoring policy):",
            json.dumps(result["analyzer_result"], indent=2, ensure_ascii=True),
        ]
        return "\n".join(lines)
    scope = result["scope"]
    lines += [
        f"Scope: {scope['kind']} · {scope['selection']} · {scope['repository']}",
        "Check outcomes: "
        + json.dumps(result["coverage"]["check_outcomes"], sort_keys=True),
        f"Findings affecting this score: {result['coverage']['scored_findings']}",
    ]
    for area in result["areas"]:
        lines.append(
            f"  {area['area']}: {area['score'] if area['score'] is not None else 'unscored'}"
        )
    for finding in result["findings"]:
        change = (
            f" · {finding['change']} ({finding['side']})" if "change" in finding else ""
        )
        lines += [
            f"{finding['severity'].upper()} · {finding['rule']} · {finding['file']}:{finding['line']}{change}",
            f"  {finding['title']}",
            f"  Next: {finding['next_action']}",
        ]
    for area in result["areas"]:
        lines.append(f"Calculation {area['area']}:")
        for entry in area["breakdown"]:
            lines.append(
                f"  {entry['rule']} ({entry['severity']}): "
                f"{entry['instances']} x {entry['points_per_instance']} = {entry['deduction']} points"
            )
        lines.append(
            f"  100 - {area['deduction']} = {100 - area['deduction']}; "
            f"cap={area['severity_cap']}; floor=0; "
            f"score={area['score'] if area['score'] is not None else 'withheld'}"
        )
    if result["score"] is not None:
        scores = ", ".join(
            str(area["score"]) for area in result["areas"] if area["score"] is not None
        )
        lines.append(
            f"Overall: lowest assessed area = min({scores}) = {result['score']}"
        )
    architecture = result.get("architecture", {})
    for key in ("frontend", "persistence"):
        names = sorted({entry["technology"] for entry in architecture.get(key, [])})
        lines.append(
            f"Architecture {key}: {', '.join(names) if names else 'not established'}"
        )
    for entry in result.get("host_settings", []):
        lines.append(f"Host {entry['setting']}: {entry['status']} · {entry['reason']}")
    for warning in result["warnings"]:
        lines.append("Limit: " + warning)
    lines.append(
        f"Excluded or unsupported entries: {len(result['exclusions'])}; see JSON/YAML for paths and reasons."
    )
    return "\n".join(lines)


def render_change(result, details=False):
    counts = result["finding_changes"]
    status = "incomplete · " if result["verdict"] == "incomplete" else ""
    summary = f"{status}Security relevance: {result['relevance']} · {counts.get('introduced', 0)} introduced, {counts.get('worsened', 0)} worsened findings"
    if not details:
        return summary
    scope = result["scope"]
    lines = [
        summary,
        f"Rule version: {result['rule_version']} · relevance version: {result['relevance_version']}",
        f"Scope: {scope['selection']} · {scope['repository']}",
        "Security relevance identifies review needs; finding severity is reported separately.",
    ]
    if "base" in scope:
        lines.append(f"Comparison: {scope['base']} -> {scope['head']}")
    if "remote_selection" in scope:
        lines.append(f"PR/MR: {scope['remote_selection']}")
        lines.append(f"Context: {scope['remote_validation']}")
    for signal in result["signals"]:
        lines.append(
            f"{signal['level'].upper()} · {signal['rule']} · {signal['file']}:{signal['line']} ({signal['side']}, {signal['relation']})\n  {signal['reason']}"
        )
    for finding in result["findings"]:
        lines.append(
            f"{finding['severity'].upper()} · {finding['change']} · {finding['rule']} · {finding['file']}:{finding['line']}\n  {finding['title']}\n  Next: {finding['next_action']}"
        )
    lines.append(
        "Coverage: " + json.dumps(result["coverage"], ensure_ascii=True, sort_keys=True)
    )
    lines.extend("Limit: " + warning for warning in result["warnings"])
    return "\n".join(lines)


def analyzer_score(options, budget):
    if any(
        (
            options.patch,
            options.base,
            options.head,
            options.commit,
            options.staged,
            options.unstaged,
            options.worktree,
            options.pr,
            options.mr,
        )
    ):
        raise SourceError(
            "The Analyzer variant supports repository scoring only; use the internal variant for changes."
        )
    is_url = options.repo.startswith("https://")
    if is_url:
        host, project = repository_url(options.repo)
        root = None
        target = "https://" + host + "/" + project + ".git"
    else:
        root = Path(options.repo).expanduser().resolve(strict=True)
        target = str(root)
        if options.token_env:
            raise SourceError("--token-env requires an explicitly selected Git URL.")
    executable = Path(options.analyzer or shutil.which("appsec-analyzer") or "")
    if (
        not executable.is_absolute()
        or not executable.is_file()
        or not os.access(executable, os.X_OK)
    ):
        raise SourceError(
            "Select an installed compatible Analyzer; it is optional and never installed automatically."
        )
    executable = executable.resolve()
    if root is not None and executable.is_relative_to(root):
        raise SourceError(
            "An analyzed repository cannot supply the Analyzer executable."
        )
    for operation in ("version", "capabilities"):
        _, raw = command([str(executable), operation], budget, limit=65536)
        document = json.loads(raw)
        if not isinstance(document, dict) or document.get("interface_version") != 1:
            raise SourceError("Analyzer public interface 1 is required.")
        if operation == "capabilities":
            capability = document.get("score", {})
            if (
                not isinstance(capability, dict)
                or capability.get("available") is not True
                or capability.get("model_calls") is not False
                or capability.get("scoring_version") != 2
            ):
                raise SourceError(
                    "Analyzer scoring version 2 without model calls is required."
                )
    if options.details:
        print("Running the selected Analyzer variant...", file=sys.stderr, flush=True)
    settings = (
        host_settings(host, project, budget, read_token(options.token_env))[0]
        if is_url
        else []
    )
    status, raw = command(
        [str(executable), "score", target, "--json"], budget, allow_failure=True
    )
    document = json.loads(raw)
    if not isinstance(document, dict):
        raise SourceError("Analyzer returned an invalid result.")
    verdict, score = document.get("verdict"), document.get("score")
    if verdict not in {"scored", "incomplete", "undetermined"}:
        raise SourceError("Analyzer did not return a supported result status.")
    if verdict == "scored":
        if type(score) is not int or not 0 <= score <= 100 or status != 0:
            raise SourceError("Analyzer returned an invalid numeric score.")
    elif score is not None or status != (2 if verdict == "undetermined" else 1):
        raise SourceError("Analyzer status and result disagree.")
    identity = document.get("comparability")
    if not isinstance(identity, dict) or identity.get("scoring_version") != 2:
        raise SourceError("Analyzer score identity is missing or incompatible.")
    return {
        "engine": "analyzer",
        "scoring_version": 2,
        "verdict": verdict,
        "score": score,
        "grade": grade(score),
        "analyzer_result": document,
        "host_settings": settings,
    }, status


def verify_rules():
    cases = 0
    for rule in RULES:
        for example in rule["examples"]:
            if rule["kind"] == "host":
                findings, checks = settings_checks(
                    [{**example, "reason": "Isolated example."}]
                )
            else:
                files = {
                    path: {"text": text}
                    for path, text in example.get("files", {}).items()
                }
                files[example["file"]] = {"text": example["source"]}
                findings, checks = scan(files, Budget())
            row = next(item for item in checks if item["rule"] == rule["id"])
            if row["status"] != example["outcome"]:
                raise SourceError(
                    f"Rule example failed: {rule['id']} / {example['outcome']}."
                )
            effect = calculate(
                [finding for finding in findings if finding["rule"] == rule["id"]],
                [row],
            )
            if (
                effect["score"] != example["expected_score"]
                or effect["grade"] != example["expected_grade"]
            ):
                raise SourceError(f"Rule score example failed: {rule['id']}.")
            cases += 1
    for example in POLICY["change_relevance"]["examples"]:
        filename = example["file"]
        before = {
            filename: {
                "text": example["before"],
                "executable": example.get("before_executable", False),
            }
        }
        after = {
            filename: {
                "text": example["after"],
                "executable": example.get("after_executable", False),
            }
        }
        old_findings, old_checks = scan(before, Budget())
        findings, checks = scan(after, Budget())
        checks = [
            {**row, "side": side}
            for side, rows in (("baseline", old_checks), ("proposed", checks))
            for row in rows
        ]
        assessment = analyze_relevance(
            before, after, checks, compare(old_findings, findings), [], Budget()
        )
        if assessment["relevance"] != example["expected_relevance"]:
            raise SourceError(f"Relevance example failed for {filename}.")
    return {
        "engine": "internal",
        "scoring_version": VERSION,
        "rule_version": RULE_VERSION,
        "relevance_version": RELEVANCE_VERSION,
        "rules_verified": len(RULES),
        "examples_verified": cases,
        "catalog_fingerprint": CATALOG_HASH,
        "relevance_examples_verified": len(POLICY["change_relevance"]["examples"]),
    }


def run(options):
    budget = Budget(options.timeout)
    if options.verify_rules:
        return verify_rules(), 0
    if options.list_rules:
        return {
            "scoring_version": VERSION,
            "rule_version": RULE_VERSION,
            "change_relevance": POLICY["change_relevance"],
            "scoring": POLICY["scoring"],
            "rules": RULES,
        }, 0
    if options.engine == "analyzer":
        return analyzer_score(options, budget)
    if options.analyzer:
        raise SourceError("--analyzer requires --engine analyzer.")
    remote = remote_identity(options)
    if options.details:
        print("Reading selected sources...", file=sys.stderr, flush=True)
    settings = []
    if options.repo.startswith("https://"):
        before, after, exclusions, scope, verify, settings = select_remote(
            options, budget
        )
    else:
        if options.token_env:
            raise SourceError("--token-env requires an explicitly selected Git URL.")
        before, after, exclusions, scope, verify = select(options, budget)
    if options.details:
        print("Checking source patterns...", file=sys.stderr, flush=True)
    old_findings, old_checks, findings, checks = [], [], [], []
    scan_error = None
    architecture = None
    try:
        scan(before, budget, old_findings, old_checks)
        scan(after, budget, findings, checks)
        architecture = describe(after, budget)
    except (SourceError, ScanLimit) as error:
        scan_error = str(error)
    change = scope["kind"] == "change"
    comparable = (
        scan_error is None
        and not any(row.get("error") for row in [*old_checks, *checks])
        and not any(
            row["reason"] in {"oversized", "link or submodule", "binary or non-UTF-8"}
            for row in exclusions
        )
    )
    if change:
        findings = (
            compare(old_findings, findings)
            if comparable
            else [
                {**finding, "change": "unresolved", "side": side}
                for side, rows in (("baseline", old_findings), ("proposed", findings))
                for finding in rows
            ]
        )
        checks = [
            {**row, "side": side}
            for side, rows in (("baseline", old_checks), ("proposed", checks))
            for row in rows
        ]
    complete = (
        scan_error is None
        and not any(row.get("error") for row in checks)
        and not any(
            row["reason"] in {"oversized", "link or submodule", "binary or non-UTF-8"}
            for row in exclusions
        )
    )
    host_findings, host_checks = settings_checks(settings)
    findings.extend(host_findings)
    for finding in findings:
        finding.pop("_identity", None)
    checks.extend(host_checks)
    architecture = architecture or {
        "frontend": [],
        "persistence": [],
        "interpretation": "Architecture observation did not complete.",
    }
    if (
        architecture["frontend"]
        or any(
            row["rule"] == "FRONTEND-BINDING" and row["status"] != "not_applicable"
            for row in checks
        )
    ) and not any(
        row["rule"] == "WEB-CSP" and row["status"] != "not_applicable" for row in checks
    ):
        checks.append(
            {
                "rule": "WEB-CSP",
                "area": "frontend-policy",
                "file": "frontend-scope",
                "status": "unclear",
            }
        )
    if verify and scan_error is None:
        if options.details:
            print("Verifying source consistency...", file=sys.stderr, flush=True)
        try:
            verify()
        except SourceError as error:
            complete = False
            scan_error = str(error)
    if change:
        try:
            result = analyze_relevance(
                before, after, checks, findings, exclusions, budget, complete=complete
            )
        except SourceError as error:
            scan_error = str(error)
            complete = False
            result = {
                "analysis": "change-relevance",
                "relevance_version": RELEVANCE_VERSION,
                "verdict": "incomplete",
                "relevance": "unclear",
                "signals": [],
                "findings": findings,
                "finding_changes": dict(
                    Counter(finding.get("change", "unresolved") for finding in findings)
                ),
                "aspects": [],
                "coverage": {
                    "check_outcomes": dict(Counter(row["status"] for row in checks)),
                    "basis": "Relevance analysis did not finish.",
                },
            }
    else:
        result = calculate(findings, checks, complete=complete, require_source=True)
        result["analysis"] = "repository-score"
    if remote:
        scope["remote_selection"] = remote
        scope["remote_validation"] = (
            "Host-supplied source; no independent remote retrieval or freshness check."
        )
    coverage_identity = sorted(
        {(row["rule"], row["status"] != "not_applicable") for row in checks}
    )
    result.update(
        {
            "engine": "internal",
            "rule_version": RULE_VERSION,
            **({} if change else {"scoring_version": VERSION}),
            "scope": scope,
            "architecture": architecture,
            "host_settings": settings,
            "checks": checks,
            "exclusions": exclusions,
            "comparability": {
                "rule_version": RULE_VERSION,
                **(
                    {"relevance_version": RELEVANCE_VERSION}
                    if change
                    else {"scoring_version": VERSION}
                ),
                "catalog_fingerprint": CATALOG_HASH,
                "implementation_fingerprint": IMPLEMENTATION_HASH,
                "coverage_fingerprint": hashlib.sha256(
                    json.dumps(coverage_identity).encode()
                ).hexdigest(),
                "source_policy": "skill-bounded-static-v2",
                "subject_kind": scope["kind"],
                "host_settings_fingerprint": hashlib.sha256(
                    json.dumps(settings, sort_keys=True).encode()
                ).hexdigest(),
            },
            "sources": {
                "baseline_sha256": fingerprint(before),
                "proposed_sha256": fingerprint(after),
            },
            "warnings": [
                "Coverage is limited to the bundled rule catalog; authorization, business logic, runtime exposure and dependency vulnerabilities are not comprehensively assessed."
            ],
        }
    )
    if not change:
        result["findings"] = findings
    if change:
        result["warnings"].append(
            "Relevance and finding severity are independent. Signals are deterministic indicators, not a full semantic review. Unrecognized behavior remains unclear; low relevance is not security approval."
        )
    if options.patch:
        result["warnings"].append(
            "Patch fragments omit surrounding context. Unparseable Python fragments stay unclear; unchanged findings outside the patch cannot be assessed."
        )
    if scan_error:
        result["warnings"].append(scan_error)
    return result, (0 if complete else 1) if change else {
        "scored": 0,
        "undetermined": 2,
        "incomplete": 1,
    }[result["verdict"]]


def main(argv=None):
    arguments = parser()
    options = arguments.parse_args(argv)
    if options.repository and options.repo:
        arguments.error("Choose a positional repository or --repo, not both.")
    options.repo = options.repo or options.repository or os.getcwd()
    if not 0.1 <= options.timeout <= 120:
        arguments.error("--timeout must be between 0.1 and 120 seconds.")
    if options.head and not options.base:
        arguments.error("--head requires --base.")
    try:
        with Progress():
            result, status = run(options)
        if options.json:
            output = json.dumps(result, indent=2, ensure_ascii=True, allow_nan=False)
        elif options.yaml:
            output = yaml_text(result)
        elif options.verify_rules:
            output = f"Verified {result['rules_verified']} scanner rules, {result['examples_verified']} examples and {result['relevance_examples_verified']} relevance examples."
        elif options.list_rules:
            output = "\n\n".join(
                f"{rule['id']} · {rule['severity']} · {rule['title']}\n{rule['criteria']}"
                for rule in RULES
            )
            relevance_rules = [
                *POLICY["change_relevance"]["path_rules"],
                *POLICY["change_relevance"]["code_rules"],
                *POLICY["change_relevance"]["area_rules"].values(),
                POLICY["change_relevance"]["documentation_rule"],
                POLICY["change_relevance"]["executable_rule"],
            ]
            output += "\n\n" + "\n\n".join(
                f"{rule['id']} · relevance {rule['level']} · {rule['aspect']}\n{rule['reason']}"
                for rule in relevance_rules
            )
        else:
            output = render(result, options.details)
        print(output)
        return status
    except KeyboardInterrupt:
        print(
            "Security score cancelled; no complete result published.", file=sys.stderr
        )
        return 130
    except SourceError as error:
        print(str(error), file=sys.stderr)
        return 1
    except BrokenPipeError:
        return 1
    except (OSError, ValueError, KeyError, TypeError, RecursionError):
        print(
            "Security score could not complete. Check the selected sources and runtime installation.",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
