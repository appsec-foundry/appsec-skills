#!/usr/bin/env python3
"""Deterministic structure checks for a threat model written by create-threat-model.

Usage: check_threat_model.py MODEL.md [--repo DIR] [--no-code] [--json]

The checks cover form, not meaning: identifiers, links, required sections,
status tables, and length bands. They run without model calls. Exit code 1
when an error was found, 0 otherwise. Warnings never fail the run.
"""

import argparse
import collections
import json
import re
import sys
from pathlib import Path

SCENARIO_ID = re.compile(r"\bT-\d{3}\b")
CHECKLIST_ID = re.compile(r"\b[CP]-\d{2}\b")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
LOCAL_LINK = re.compile(r"\[([^\]]*)\]\(#([^)\s]+)\)")
STATUS_WORDS = ("clarified", "open", "not applicable", "not examined")
ORIGIN_MARKERS = ("intended", "observed", "assumed")
SCENARIO_WORDS_WARN = 180
SCENARIO_WORDS_ERROR = 320


def slug(text):
    """GitHub-style heading anchor."""
    text = re.sub(r"[`*_\[\]()]", "", text).strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s", "-", text)


class Report:
    def __init__(self):
        self.findings = []

    def add(self, level, code, line, message):
        self.findings.append({"level": level, "code": code, "line": line, "message": message})

    def error(self, code, line, message):
        self.add("error", code, line, message)

    def warning(self, code, line, message):
        self.add("warning", code, line, message)

    @property
    def errors(self):
        return [f for f in self.findings if f["level"] == "error"]


def parse_headings(lines):
    headings = []
    in_fence = False
    for number, line in enumerate(lines, start=1):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING.match(line)
        if match:
            headings.append({"line": number, "level": len(match.group(1)), "text": match.group(2)})
    anchors = collections.Counter()
    for heading in headings:
        base = slug(heading["text"])
        heading["anchor"] = base if anchors[base] == 0 else f"{base}-{anchors[base]}"
        anchors[base] += 1
    return headings


def sections(lines, headings):
    """Yield (heading, body_lines, start_line) for each heading."""
    for index, heading in enumerate(headings):
        start = heading["line"]
        end = len(lines) + 1
        for later in headings[index + 1:]:
            if later["level"] <= heading["level"]:
                end = later["line"]
                break
        yield heading, lines[start:end - 1], start + 1


def find_section(lines, headings, pattern):
    for heading, body, start in sections(lines, headings):
        if re.search(pattern, heading["text"], re.IGNORECASE):
            return heading, body, start
    return None, [], 0


def words(text):
    return len(re.findall(r"\S+", text))


def check_model(path, repo=None, no_code=False):
    report = Report()
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    headings = parse_headings(lines)
    anchors = {h["anchor"] for h in headings}

    # M01 title and audience notice
    title = next((h for h in headings if h["level"] == 1), None)
    if not title:
        report.error("M01", 1, "no level-1 title")
    else:
        after = [l for l in lines[title["line"]:title["line"] + 3] if l.strip()]
        if not after or not re.match(r"^>\s*\*\*[A-Z][^a-z]*\*\*", after[0]):
            report.error("M01", title["line"] + 1,
                         "audience notice missing: expected a blockquote with a bold uppercase heading directly below the title")

    # M02 scenario headings unique
    scenario_headings = [h for h in headings if SCENARIO_ID.match(h["text"])]
    seen = collections.Counter(SCENARIO_ID.match(h["text"]).group(0) for h in scenario_headings)
    for scenario_id, count in seen.items():
        if count > 1:
            report.error("M02", 0, f"{scenario_id} has {count} scenario headings")
    if not scenario_headings:
        report.error("M02", 0, "no scenario headings of the form '### T-001 ...'")
    defined = set(seen)

    # M03 referenced IDs exist
    referenced = collections.defaultdict(list)
    in_fence = False
    for number, line in enumerate(lines, start=1):
        if line.startswith("```"):
            in_fence = not in_fence
        if in_fence:
            continue
        for scenario_id in SCENARIO_ID.findall(line):
            referenced[scenario_id].append(number)
    for scenario_id, where in referenced.items():
        if scenario_id not in defined:
            report.error("M03", where[0], f"{scenario_id} is referenced but has no scenario heading")

    # M04 local links resolve
    for number, line in enumerate(lines, start=1):
        for _, anchor in LOCAL_LINK.findall(line):
            if anchor not in anchors:
                report.error("M04", number, f"local link '#{anchor}' does not resolve to a heading")

    # M05 evidence link per scenario, M06 length, M09 verified claims
    verified = re.compile(r"(?<!un)(?<!not )(?<!not-)\bverified\b", re.IGNORECASE)
    for heading, body, start in sections(lines, headings):
        match = SCENARIO_ID.match(heading["text"])
        if not match:
            continue
        scenario_id = match.group(0)
        body_text = "\n".join(body)
        evidence_links = [
            (label, anchor) for label, anchor in LOCAL_LINK.findall(body_text)
            if scenario_id.lower() in anchor
        ]
        if not evidence_links:
            report.error("M05", heading["line"], f"{scenario_id} has no evidence link to an appendix entry for the same ID")
        else:
            label, anchor = evidence_links[-1]
            main_text = body_text.split(f"[{label}](#{anchor})")[0]
            count = words(re.sub(r"\*\*|__", "", main_text))
            if count > SCENARIO_WORDS_ERROR:
                report.error("M06", heading["line"], f"{scenario_id} main text has {count} words (limit {SCENARIO_WORDS_ERROR})")
            elif count > SCENARIO_WORDS_WARN:
                report.warning("M06", heading["line"], f"{scenario_id} main text has {count} words (guide: about 80-140)")
        for offset, line in enumerate(body):
            if verified.search(line) and not LOCAL_LINK.search(line) and "](" not in line:
                report.warning("M09", start + offset,
                               f"{scenario_id}: 'verified' without a link to evidence in the same paragraph")

    # M07 required sections
    for pattern, code in ((r"^overview|^übersicht|^zusammenfassung", "M07"),
                          (r"open decisions|offene entscheidungen", "M07"),
                          (r"evidence|verification|nachweis", "M07")):
        if not any(re.search(pattern, h["text"], re.IGNORECASE) for h in headings):
            report.warning(code, 0, f"no section matching '{pattern}'")

    # M08 checklist statuses
    checklist_rows = [(n, l) for n, l in enumerate(lines, start=1)
                      if l.startswith("|") and CHECKLIST_ID.search(l.split("|")[1] if "|" in l[1:] else "")]
    for number, line in checklist_rows:
        cells = [c.strip().lower() for c in line.strip("|").split("|")]
        if len(cells) < 2 or not any(cells[1].startswith(s) for s in STATUS_WORDS):
            report.error("M08", number, "checklist row without a status in its second column "
                                        "(clarified, open, not applicable, not examined)")
    if not checklist_rows and not re.search(r"not listed .{0,40}clarified", text, re.IGNORECASE):
        report.warning("M08", 0, "no checklist status table and no statement that unlisted items are clarified")

    # M10 diagram, M14 origin markers
    system_heading, system_body, system_start = find_section(lines, headings, r"system|architektur")
    system_text = "\n".join(system_body)
    if system_heading is None:
        report.warning("M10", 0, "no system section found")
    else:
        if "```mermaid" not in system_text and "```text" not in system_text:
            report.warning("M10", system_heading["line"], "system section has no fenced diagram")
        present = [m for m in ORIGIN_MARKERS if re.search(rf"\b{m}\b", system_text, re.IGNORECASE)]
        if not present:
            report.warning("M14", system_heading["line"],
                           "system section does not mark element origin (intended, observed, assumed)")
        if no_code and re.search(r"\bobserved\b", system_text, re.IGNORECASE):
            report.warning("M13", system_heading["line"],
                           "'observed' used although the target has no code")

    # M11 repeated sentences
    sentences = collections.Counter()
    for line in lines:
        if line.startswith(("|", "#", ">", "```")):
            continue
        for sentence in re.split(r"(?<=[.!?])\s+", line.strip()):
            cleaned = re.sub(r"\s+", " ", sentence).strip()
            if words(cleaned) >= 8:
                sentences[cleaned] += 1
    for sentence, count in sentences.items():
        if count > 1:
            report.warning("M11", 0, f"sentence repeated {count} times: '{sentence[:80]}'")

    # M12 security document link
    if repo:
        repo = Path(repo)
        security = next((repo / n for n in ("SECURITY.md", "security.md") if (repo / n).is_file()), None)
        if security is None:
            report.error("M12", 0, "no SECURITY.md or security.md in the repository")
        else:
            links = re.findall(r"\]\(([^)]+)\)", security.read_text(encoding="utf-8"))
            resolved = [(security.parent / l.split("#")[0]).resolve() for l in links if not l.startswith(("http", "mailto"))]
            if path.resolve() not in resolved:
                report.error("M12", 0, f"{security.name} has no link that resolves to {path.name}")

    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("model", type=Path)
    parser.add_argument("--repo", type=Path, help="repository root; enables the security-document link check")
    parser.add_argument("--no-code", action="store_true", help="the target has no implementation")
    parser.add_argument("--json", action="store_true", help="print findings as JSON")
    args = parser.parse_args(argv)
    if not args.model.is_file():
        parser.error(f"{args.model} is not a file")
    report = check_model(args.model, args.repo, args.no_code)
    if args.json:
        print(json.dumps(report.findings, indent=2))
    else:
        for finding in report.findings:
            where = f"line {finding['line']}: " if finding["line"] else ""
            print(f"{finding['level'].upper()} {finding['code']} {where}{finding['message']}")
        print(f"{len(report.errors)} errors, {len(report.findings) - len(report.errors)} warnings")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
