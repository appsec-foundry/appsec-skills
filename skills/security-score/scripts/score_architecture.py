"""Readable detectors for architecture and dependency declarations.

Each detector kind is linked from rules.json and returns located observations.
Presence of a framework, ORM, or lockfile never establishes application safety.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path
import re


def document(text):
    try:
        result = json.loads(text)
        return result if isinstance(result, dict) else None
    except (ValueError, RecursionError):
        return None


def line_of(text, name):
    index = text.find(name)
    return text.count("\n", 0, index) + 1 if index >= 0 else 1


def csp_status(policy):
    directives = {}
    for part in policy.split(";"):
        tokens = part.lower().split()
        if tokens:
            directives.setdefault(tokens[0], tokens[1:])
    scripts = directives.get("script-src", directives.get("default-src"))
    if scripts is None:
        return "unclear"
    if any(
        token in {"*", "'unsafe-inline'", "'unsafe-eval'", "http:", "https:"}
        for token in scripts
    ):
        return "violated"
    if (
        not scripts
        or directives.get("object-src") != ["'none'"]
        or directives.get("base-uri") != ["'none'"]
        or not directives.get("frame-ancestors")
    ):
        return "unclear"
    return "satisfied"


def csp_observations(path, text, code):
    observations = []
    # The assignment separator must be outside a JS string/comment, so quoted
    # documentation does not become an actual configured header.
    pattern = r"""["']Content-Security-Policy["']\s*(?:\]\s*)?(?P<separator>[:,=])\s*(?P<quote>["'])(?P<policy>[^\n]*?)(?P=quote)"""
    if Path(path).suffix == ".py":
        try:
            tree = ast.parse(text)
        except (SyntaxError, ValueError, RecursionError):
            return []
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Assign)
                and isinstance(node.value, ast.Constant)
                and isinstance(node.value.value, str)
            ):
                for target in node.targets:
                    if (
                        isinstance(target, ast.Subscript)
                        and isinstance(target.slice, ast.Constant)
                        and target.slice.value == "Content-Security-Policy"
                    ):
                        observations.append((node.lineno, csp_status(node.value.value)))
            elif (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr
                in {"set_header", "setHeader", "header", "setdefault"}
                and len(node.args) >= 2
                and isinstance(node.args[0], ast.Constant)
                and node.args[0].value == "Content-Security-Policy"
            ):
                policy = node.args[1]
                observations.append(
                    (
                        node.lineno,
                        csp_status(policy.value)
                        if isinstance(policy, ast.Constant)
                        and isinstance(policy.value, str)
                        else "unclear",
                    )
                )
        return observations
    for match in re.finditer(pattern, text):
        if code[match.start("separator")].isspace():
            continue
        observations.append(
            (text.count("\n", 0, match.start()) + 1, csp_status(match["policy"]))
        )
    for match in re.finditer(
        r"""(?im)^\s*add_header\s+Content-Security-Policy\s+(["'])(.*?)\1""", text
    ):
        observations.append(
            (text.count("\n", 0, match.start()) + 1, csp_status(match[2]))
        )
    # A report-only policy is deliberately not recognized as enforcement.
    return observations


def npm_observations(kind, path, text, files):
    manifest = document(text)
    if manifest is None:
        return [(1, "unclear")]
    dependencies = {}
    for field in ("dependencies", "devDependencies", "optionalDependencies"):
        values = manifest.get(field, {})
        if not isinstance(values, dict):
            return [(1, "unclear")]
        dependencies.update(values)
    if kind == "npm-sources":
        rows = []
        for name, value in sorted(dependencies.items()):
            if not isinstance(value, str):
                status = "unclear"
            elif value.startswith(("http://", "git+http://")):
                status = "violated"
            elif value.startswith(("git+", "github:", "gitlab:")):
                status = (
                    "satisfied"
                    if re.search(r"#[0-9a-fA-F]{40}$", value)
                    else "violated"
                )
            elif value.startswith(("file:", "link:", "workspace:")):
                status = "unclear"
            else:
                status = "unclear"  # Registry ranges need resolution/lock evidence.
            rows.append((line_of(text, '"' + name + '"'), status))
        return rows
    if kind == "npm-lock":
        if not dependencies:
            return []
        parent = str(Path(path).parent)
        prefix = "" if parent == "." else parent + "/"
        for name in ("npm-shrinkwrap.json", "package-lock.json"):
            source = files.get(prefix + name)
            if not source:
                continue
            lock = document(source["text"])
            if (
                lock
                and lock.get("lockfileVersion") in {2, 3}
                and isinstance(lock.get("packages"), dict)
            ):
                root = lock["packages"].get("")
                if isinstance(root, dict) and all(
                    manifest.get(field, {}) == root.get(field, {})
                    for field in (
                        "dependencies",
                        "devDependencies",
                        "optionalDependencies",
                    )
                ):
                    return [(1, "satisfied")]
            return [(1, "unclear")]
        # External or other-manager locks may exist outside this selected scope.
        return [(1, "unclear")]
    scripts = manifest.get("scripts", {})
    if not isinstance(scripts, dict):
        return [(1, "unclear")]
    rows = []
    for name in ("preinstall", "install", "postinstall", "prepare"):
        value = scripts.get(name)
        if isinstance(value, str):
            unsafe = re.search(
                r"\b(?:curl|wget)\b[^\n]{0,1000}\|\s*(?:ba|z|k)?sh\b|\b(?:Invoke-WebRequest|iwr)\b[^\n]{0,1000}\|\s*(?:iex|Invoke-Expression)\b",
                value,
                re.I,
            )
            rows.append(
                (line_of(text, '"' + name + '"'), "violated" if unsafe else "unclear")
            )
    return rows


def observations(rule, path, text, code, files):
    kind = rule["kind"]
    if kind.startswith("npm-"):
        return npm_observations(kind, path, text, files)
    if kind == "csp":
        return csp_observations(path, text, code)
    rows = []
    original_lines = text.splitlines()
    for number, line in enumerate(code.splitlines(), 1):
        status = None
        if kind == "js-sql":
            match = re.search(r"\.(?:query|execute|\$queryRawUnsafe)\s*\(", line)
            if match:
                original = original_lines[number - 1][match.end() :].strip()
                if re.match(
                    r"[`'\"]\s*(?:SELECT|INSERT|UPDATE|DELETE|WITH|CREATE)\b",
                    original,
                    re.I,
                ):
                    status = (
                        "violated"
                        if re.search(r"\$\{|['\"]\s*\+|\+\s*['\"]", original)
                        else "satisfied"
                    )
                else:
                    status = "unclear"
        elif kind == "frontend":
            if re.search(
                r"\bdangerouslySetInnerHTML\s*=|\bbypassSecurityTrust(?:Html|Script|Url|ResourceUrl)\s*\(",
                line,
            ):
                status = "violated"
            elif re.search(
                r"<(?:div|span|p|li|label|button)\b[^>]{0,200}>\s*\{[^{}]{1,200}\}\s*</",
                line,
            ):
                status = "satisfied"
            elif path.endswith(".component.html") and re.search(
                r"\{\{[^{}]{1,200}\}\}", line
            ):
                status = "satisfied"
        elif kind == "requirements":
            value = line.strip()
            if value and not value.startswith("#"):
                if value.startswith(("-r", "-c", "--")):
                    status = "unclear"
                elif "http://" in value or not re.match(
                    r"[\w.-]+(?:\[[\w,.-]+\])?==[^\s*]+", value
                ):
                    status = "violated"
                else:
                    status = (
                        "satisfied"
                        if re.search(r"--hash=sha256:[0-9a-fA-F]{64}", value)
                        else "unclear"
                    )
        elif kind == "workflow-permissions":
            if re.match(r"\s*permissions:\s*write-all\s*(?:#.*)?$", line):
                status = "violated"
            elif re.match(r"\s*permissions:\s*read-all\s*(?:#.*)?$", line):
                status = "satisfied"
        if status:
            rows.append((number, status))
    return rows


def describe(files, budget):
    """Technology observations are context, not scored control evidence."""
    frontend, persistence = [], []
    for path, source in sorted(files.items()):
        budget.check()
        if Path(path).name == "package.json":
            manifest = document(source["text"]) or {}
            dependencies = {}
            for key in ("dependencies", "devDependencies"):
                if isinstance(manifest.get(key), dict):
                    dependencies.update(manifest[key])
            for name in ("react", "@angular/core", "vue", "preact"):
                if name in dependencies:
                    frontend.append({"technology": name, "file": path})
            for name in (
                "pg",
                "mysql2",
                "mongodb",
                "mongoose",
                "sequelize",
                "knex",
                "@prisma/client",
                "typeorm",
            ):
                if name in dependencies:
                    persistence.append({"technology": name, "file": path})
        elif Path(path).suffix == ".py":
            try:
                tree = ast.parse(source["text"])
            except (SyntaxError, ValueError, RecursionError):
                continue
            modules = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    modules.update(alias.name.split(".")[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    modules.add(node.module.split(".")[0])
            for name in sorted(
                modules
                & {"sqlalchemy", "django", "sqlite3", "psycopg", "psycopg2", "pymongo"}
            ):
                persistence.append({"technology": name, "file": path})
    return {
        "frontend": frontend,
        "persistence": persistence,
        "interpretation": "Declared technologies and imports only; their presence gives no score credit. CSP delivery, authorization, DB privileges and deployment controls require wider evidence.",
    }
