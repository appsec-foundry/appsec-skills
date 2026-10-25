"""Deterministic, source-only checks. No imports or execution from the target."""

from __future__ import annotations

import ast
from collections import Counter, defaultdict
import hashlib
from pathlib import Path
import re
import textwrap

from score_calculation import (
    CATALOG_BYTES,
    POLICY,
    VERSION,
    WEIGHTS,
    calculate as calculate,
    grade as grade,
    validate_scoring,
)


ROOT = Path(__file__).resolve().parent.parent
RULE_VERSION = POLICY["rule_version"]
RULES = POLICY["rules"]


def validate_policy():
    kinds = {
        "py-exec",
        "py-shell",
        "py-sql",
        "py-tls",
        "py-yaml",
        "py-pickle",
        "py-hash",
        "py-debug",
        "js-eval",
        "js-shell",
        "js-random",
        "js-html",
        "js-tls",
        "actions",
        "image",
        "user",
        "js-sql",
        "frontend",
        "csp",
        "npm-sources",
        "npm-lock",
        "npm-install",
        "requirements",
        "workflow-permissions",
        "host",
    }
    if (
        type(VERSION) is not int
        or VERSION < 1
        or not isinstance(RULES, list)
        or not RULES
    ):
        raise ValueError("Invalid rule catalog version or rule list.")
    validate_scoring()
    identifiers = set()
    for rule in RULES:
        if (
            not isinstance(rule, dict)
            or not re.fullmatch(r"[A-Z][A-Z0-9-]{0,79}", rule.get("id", ""))
            or rule["id"] in identifiers
        ):
            raise ValueError("Rule IDs must be unique and stable.")
        identifiers.add(rule["id"])
        if rule.get("kind") not in kinds or rule.get("severity") not in WEIGHTS:
            raise ValueError("Unknown detector or severity in rule catalog.")
        for field in ("area", "title", "criteria", "next_action"):
            if not isinstance(rule.get(field), str) or not rule[field].strip():
                raise ValueError(
                    "Each rule needs area, title, criteria and next action."
                )
        if not isinstance(rule.get("examples"), list) or not rule["examples"]:
            raise ValueError("Every rule needs verifiable examples.")
    relevance = POLICY["change_relevance"]
    if (
        type(RULE_VERSION) is not int
        or RULE_VERSION < 1
        or type(relevance["version"]) is not int
        or relevance["version"] < 1
    ):
        raise ValueError("Rule and relevance versions must be positive integers.")
    relevance_rules = [
        *relevance["path_rules"],
        *relevance["code_rules"],
        *relevance["area_rules"].values(),
        relevance["documentation_rule"],
        relevance["executable_rule"],
    ]
    for rule in relevance_rules:
        if rule["id"] in identifiers or not re.fullmatch(
            r"[A-Z][A-Z0-9-]{0,79}", rule["id"]
        ):
            raise ValueError("Relevance rule IDs must be unique and stable.")
        identifiers.add(rule["id"])
        if (
            rule["level"] not in {"high", "medium"}
            or not rule["reason"]
            or not rule["aspect"]
        ):
            raise ValueError(
                "Positive relevance signals need a level, aspect and reason."
            )
        if "pattern" in rule:
            re.compile(rule["pattern"])
    if not relevance["examples"] or not all(
        example["expected_relevance"] in {"high", "medium", "low", "unclear"}
        for example in relevance["examples"]
    ):
        raise ValueError("Relevance examples need expected outcomes.")


validate_policy()
CATALOG_HASH = hashlib.sha256(CATALOG_BYTES).hexdigest()
IMPLEMENTATION_HASH = hashlib.sha256(
    b"".join(
        (ROOT / "scripts" / name).read_bytes()
        for name in (
            "score_core.py",
            "score_calculation.py",
            "score_sources.py",
            "score_remote.py",
            "score_architecture.py",
            "score_relevance.py",
            "score.py",
        )
    )
).hexdigest()
JS_EXTENSIONS = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}
SOURCE_EXTENSIONS = JS_EXTENSIONS | {
    ".py",
    ".yaml",
    ".yml",
    ".json",
    ".html",
    ".conf",
    ".config",
}


class ScanLimit(ValueError):
    pass


def supported(path):
    return (
        Path(path).suffix.lower() in SOURCE_EXTENSIONS
        or Path(path).name == "Dockerfile"
        or (Path(path).name.startswith("requirements") and Path(path).suffix == ".txt")
    )


def change_supported(path):
    """Read selected context for relevance without expanding repository scoring."""
    return (
        supported(path)
        or Path(path).suffix.lower()
        in {
            ".md",
            ".rst",
            ".adoc",
            ".txt",
            ".java",
            ".kt",
            ".scala",
            ".go",
            ".rs",
            ".cs",
            ".php",
            ".rb",
            ".sql",
            ".vue",
            ".svelte",
            ".xml",
            ".toml",
            ".ini",
            ".properties",
            ".sh",
            ".bash",
            ".ps1",
            ".tf",
            ".lock",
            ".gradle",
            ".kts",
            ".svg",
        }
        or Path(path).name in {"Gemfile", "Jenkinsfile", "CODEOWNERS"}
    )


def qualified(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return qualified(node.value) + "." + node.attr
    return ""


def literal(node, value):
    return (
        isinstance(node, ast.Constant)
        and type(node.value) is type(value)
        and node.value == value
    )


def python_observations(rule, text, tree=None):
    """Return (line, status) for recognized calls; unrecognized aliases stay uncovered."""
    try:
        tree = tree if tree is not None else ast.parse(text)
    except (SyntaxError, ValueError, RecursionError):
        return [], True
    observations = []
    kind = rule["kind"]
    lines = text.splitlines()
    for call in ast.walk(tree):
        if not isinstance(call, ast.Call):
            continue
        name = qualified(call.func)
        args = call.args
        options = {kw.arg: kw.value for kw in call.keywords}
        status = None
        if kind == "py-exec" and name in {"eval", "exec", "ast.literal_eval"}:
            status = "satisfied" if name == "ast.literal_eval" else "violated"
        elif kind == "py-shell" and name in {
            "subprocess.run",
            "subprocess.call",
            "subprocess.check_call",
            "subprocess.check_output",
            "subprocess.Popen",
        }:
            shell = options.get("shell", ast.Constant(False))
            if literal(shell, True):
                status = "violated"
            elif (
                literal(shell, False)
                and args
                and isinstance(args[0], (ast.List, ast.Tuple))
            ):
                status = "satisfied"
            else:
                status = "unclear"
        elif (
            kind == "py-sql"
            and name.rsplit(".", 1)[-1] in {"execute", "executemany"}
            and args
        ):
            query = args[0]
            if isinstance(query, (ast.JoinedStr, ast.BinOp)) or (
                isinstance(query, ast.Call)
                and isinstance(query.func, ast.Attribute)
                and query.func.attr == "format"
            ):
                status = "violated"
            elif isinstance(query, ast.Constant) and isinstance(query.value, str):
                status = "satisfied"
            else:
                status = "unclear"
        elif kind == "py-tls" and name in {
            "requests." + verb
            for verb in ("get", "post", "put", "patch", "delete", "head", "request")
        }:
            verify = options.get("verify", ast.Constant(True))
            status = (
                "violated"
                if literal(verify, False)
                else "satisfied"
                if literal(verify, True)
                else "unclear"
            )
        elif kind == "py-yaml" and name in {"yaml.load", "yaml.safe_load"}:
            loader = qualified(options.get("Loader"))
            status = (
                "satisfied"
                if name == "yaml.safe_load"
                or loader in {"yaml.SafeLoader", "yaml.CSafeLoader"}
                else "violated"
                if loader
                in {
                    "yaml.Loader",
                    "yaml.UnsafeLoader",
                    "yaml.CLoader",
                    "yaml.CUnsafeLoader",
                }
                else "unclear"
            )
        elif kind == "py-pickle" and name in {"pickle.load", "pickle.loads"}:
            status = "violated"
        elif kind == "py-hash" and name.startswith("hashlib."):
            # A broken primitive is relevant here only with a named security purpose.
            line = lines[call.lineno - 1]
            if re.search(
                r"\b(?:signature|token|password|credential|secret|hmac)\w*\b",
                line,
                re.I,
            ):
                status = (
                    "violated" if name in {"hashlib.md5", "hashlib.sha1"} else "unclear"
                )
        elif kind == "py-debug" and name == "app.run" and "debug" in options:
            status = (
                "violated"
                if literal(options["debug"], True)
                else "satisfied"
                if literal(options["debug"], False)
                else "unclear"
            )
        if status:
            observations.append((call.lineno, status))
    return observations, False


def javascript_code(text):
    """Mask comments and literal contents, preserving offsets and line numbers.

    This is a lexer for narrow patterns, not a JavaScript parser. Template
    interpolation and regular-expression literals are not analyzed.
    """
    out = list(text)
    state = None
    quote = None
    escaped = False
    index = 0
    while index < len(text):
        char = text[index]
        pair = text[index : index + 2]
        if state == "line":
            if char == "\n":
                state = None
            else:
                out[index] = " "
        elif state == "block":
            if pair == "*/":
                out[index : index + 2] = "  "
                index += 1
                state = None
            elif char != "\n":
                out[index] = " "
        elif state == "string":
            if char != "\n":
                out[index] = " "
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                state = None
        elif pair in {"//", "/*"}:
            state = "line" if pair == "//" else "block"
            out[index : index + 2] = "  "
            index += 1
        elif char in {"'", '"', "`"}:
            state, quote = "string", char
            out[index] = " "
        index += 1
    if state in {"string", "block"}:
        raise SyntaxError("Incomplete JavaScript lexical context")
    return "".join(out)


def other_observations(rule, text, code=None):
    kind = rule["kind"]
    code = (
        code
        if code is not None
        else javascript_code(text)
        if kind.startswith("js-")
        else text
    )
    observations = []
    for number, line in enumerate(code.splitlines(), 1):
        status = None
        if kind == "js-eval":
            if re.search(r"\b(?:eval|Function)\s*\(", line):
                status = "violated"
            elif re.search(r"\bJSON\.parse\s*\(", line):
                status = "satisfied"
        elif kind == "js-shell":
            if re.search(r"\b(?:child_process\.)?exec(?:Sync)?\s*\(", line):
                status = "violated"
            elif re.search(r"\b(?:child_process\.)?execFile(?:Sync)?\s*\(", line):
                status = (
                    "unclear"  # shell options and executable identity need context.
                )
        elif kind == "js-random" and re.search(
            r"\b(?:token|secret|otp|nonce|sessionId|resetToken)\b", line
        ):
            if re.search(r"\bMath\.random\s*\(", line):
                status = "violated"
            elif re.search(
                r"\bcrypto\.(?:randomBytes|randomUUID|getRandomValues)\s*\(", line
            ):
                status = "satisfied"
        elif kind == "js-html":
            if re.search(r"\.innerHTML\s*=(?!=)", line):
                status = "violated"
            elif re.search(r"\.textContent\s*=(?!=)", line):
                status = "satisfied"
        elif kind == "js-tls":
            match = re.search(r"\brejectUnauthorized\s*:\s*(\w+)", line)
            if match:
                status = {"false": "violated", "true": "satisfied"}.get(
                    match[1], "unclear"
                )
        elif kind == "actions":
            match = re.match(r"\s*(?:-\s*)?uses:\s*['\"]?([^\s'\"#]+)", line)
            if match and not match[1].startswith("./"):
                value = match[1]
                if value.startswith("docker://"):
                    status = (
                        "satisfied"
                        if re.search(r"@sha256:[0-9a-fA-F]{64}$", value)
                        else "violated"
                    )
                elif re.fullmatch(r"[\w.-]+/[\w./-]+@[\w.-]+", value):
                    status = (
                        "satisfied"
                        if re.search(r"@[0-9a-fA-F]{40}$", value)
                        else "violated"
                    )
                else:
                    status = "unclear"
        elif kind == "image":
            match = re.match(r"(?i)\s*FROM\s+(?:--platform=\S+\s+)?(\S+)", line)
            if match and match[1].lower() != "scratch":
                value = match[1]
                status = (
                    "satisfied"
                    if re.search(r"@sha256:[0-9a-fA-F]{64}$", value)
                    else "unclear"
                    if "$" in value
                    else "violated"
                )
        elif kind == "user":
            match = re.match(r"(?i)\s*USER\s+(\S+)", line)
            if match:
                user = match[1].split(":", 1)[0]
                status = (
                    "violated"
                    if user in {"root", "0"}
                    else "unclear"
                    if "$" in user
                    else "satisfied"
                )
        if status:
            observations.append((number, status))
    return observations, False


def applies(rule, path):
    kind = rule["kind"]
    suffix = Path(path).suffix.lower()
    if kind.startswith("py-"):
        return suffix == ".py"
    if kind.startswith("js-"):
        return suffix in JS_EXTENSIONS
    if kind == "actions":
        return path.startswith(".github/workflows/") and suffix in {".yml", ".yaml"}
    if kind == "workflow-permissions":
        return path.startswith(".github/workflows/") and suffix in {".yml", ".yaml"}
    if kind.startswith("npm-"):
        return Path(path).name == "package.json"
    if kind == "requirements":
        return Path(path).name.startswith("requirements") and suffix == ".txt"
    if kind == "js-sql":
        return suffix in JS_EXTENSIONS
    if kind == "frontend":
        return suffix in JS_EXTENSIONS or path.endswith(".component.html")
    if kind == "csp":
        return suffix in JS_EXTENSIONS | {".py", ".json", ".conf", ".config"}
    if kind == "host":
        return False
    return Path(path).name == "Dockerfile"


def scan(files, budget, findings=None, checks=None):
    findings = [] if findings is None else findings
    checks = [] if checks is None else checks
    for path, original in sorted(files.items()):
        for source in original.get("fragments", [original]):
            scan_source(path, source, budget, findings, checks, files)
    return findings, checks


def scan_source(path, source, budget, findings, checks, files):
    from score_architecture import observations

    budget.check()
    text = textwrap.dedent(source["text"]) if source.get("fragment") else source["text"]
    tree, parse_error = None, False
    if Path(path).suffix.lower() == ".py":
        try:
            tree = ast.parse(text)
        except (SyntaxError, ValueError, RecursionError):
            parse_error = True
    try:
        code = (
            javascript_code(text)
            if Path(path).suffix.lower() in JS_EXTENSIONS
            else text
        )
    except SyntaxError:
        code, parse_error = "", True
    code_lines = code.splitlines()
    signatures = {}
    signatures_ready = False
    if tree is not None:

        class Signatures(ast.NodeVisitor):
            def __init__(self):
                self.context = []

            def visit_FunctionDef(self, node):
                self.context.append(node.name)
                self.generic_visit(node)
                self.context.pop()

            visit_AsyncFunctionDef = visit_FunctionDef
            visit_ClassDef = visit_FunctionDef

            def visit_Call(self, node):
                signatures.setdefault(node.lineno, []).append(
                    (tuple(self.context), ast.dump(node, include_attributes=False))
                )
                self.generic_visit(node)

    for rule in RULES:
        if not applies(rule, path):
            continue
        budget.check()
        if parse_error:
            observed = []
        elif rule["kind"].startswith("py-"):
            observed = [] if parse_error else python_observations(rule, text, tree)[0]
        elif rule["kind"] in {
            "js-sql",
            "frontend",
            "csp",
            "npm-sources",
            "npm-lock",
            "npm-install",
            "requirements",
            "workflow-permissions",
        }:
            observed = observations(rule, path, text, code, files)
        else:
            observed = other_observations(rule, text, code)[0]
        states = Counter(status for _, status in observed)
        status = (
            "violated"
            if states["violated"]
            else "unclear"
            if states["unclear"] or parse_error
            else "satisfied"
            if states["satisfied"]
            else "not_applicable"
        )
        checks.append(
            {
                "rule": rule["id"],
                "area": rule["area"],
                "file": path,
                "status": status,
                "locations": [
                    {"line": source.get("lines", {}).get(line, line), "status": outcome}
                    for line, outcome in observed
                ],
            }
        )
        if parse_error:
            checks[-1]["error"] = (
                "Source syntax or lexical context could not be read reliably."
            )
        for line, outcome in observed:
            if outcome != "violated":
                continue
            if len(findings) >= 5000:
                raise ScanLimit("Finding limit reached; the result is incomplete.")
            actual_line = source.get("lines", {}).get(line, line)
            if tree is not None and not signatures_ready:
                Signatures().visit(tree)
                signatures_ready = True
            observation = signatures.get(line) or re.sub(
                r"\s+", "", code_lines[line - 1]
            )
            identity = hashlib.sha256(repr(observation).encode()).hexdigest()
            # Raw source and literal values never enter the result.
            findings.append(
                {
                    "rule": rule["id"],
                    "area": rule["area"],
                    "severity": rule["severity"],
                    "title": rule["title"],
                    "file": path,
                    "line": actual_line,
                    "evidence": "Static pattern at the referenced location; exploitability unverified.",
                    "next_action": rule["next_action"],
                    "_identity": identity,
                }
            )


def compare(before, after):
    """Compare instances by rule and file, not unstable source line numbers.

    More occurrences of an existing check are 'worsened'; fewer are 'resolved'.
    Equal counts cannot establish that an individual flow stayed unchanged.
    """
    groups = defaultdict(lambda: [[], []])
    for side, findings in enumerate((before, after)):
        for finding in findings:
            groups[(finding["file"], finding["rule"])][side].append(finding)
    output = []
    for key in sorted(groups):
        old, new = groups[key]
        remaining = Counter(finding.get("_identity") for finding in old)
        for finding in new:
            identity = finding.get("_identity")
            if remaining[identity]:
                remaining[identity] -= 1
                status = "pre_existing"
            else:
                status = "worsened" if old and len(new) > len(old) else "introduced"
            output.append({**finding, "change": status, "side": "proposed"})
        for finding in old:
            identity = finding.get("_identity")
            if remaining[identity]:
                remaining[identity] -= 1
                output.append({**finding, "change": "resolved", "side": "baseline"})
    return output
