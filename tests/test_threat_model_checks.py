"""Tests for the deterministic threat-model checks. No model calls."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/threat-model-checks"
MODEL_CHECK = ROOT / "scripts/check_threat_model.py"
TRANSCRIPT_CHECK = ROOT / "scripts/check_transcript.py"


def run(script, *args):
    result = subprocess.run(
        [sys.executable, "-I", str(script), *args, "--json"],
        capture_output=True, text=True, timeout=30,
    )
    return result.returncode, json.loads(result.stdout)


class ModelCheckTests(unittest.TestCase):
    def test_good_model_has_no_errors(self):
        with tempfile.TemporaryDirectory() as repo:
            model = Path(repo) / "threat-model.md"
            model.write_text((FIXTURES / "model-good.md").read_text())
            (Path(repo) / "SECURITY.md").write_text("# Security\n\nSee the [threat model](threat-model.md).\n")
            code, findings = run(MODEL_CHECK, str(model), "--repo", repo, "--no-code")
        self.assertEqual(code, 0, findings)
        self.assertEqual([f for f in findings if f["level"] == "error"], [])

    def test_bad_model_reports_each_violation(self):
        with tempfile.TemporaryDirectory() as repo:
            model = Path(repo) / "threat-model.md"
            model.write_text((FIXTURES / "model-bad.md").read_text())
            code, findings = run(MODEL_CHECK, str(model), "--repo", repo)
        self.assertEqual(code, 1)
        codes = {f["code"] for f in findings}
        expected = {
            "M01",  # no audience notice
            "M02",  # duplicate T-001
            "M03",  # T-009 referenced but undefined
            "M04",  # broken anchor
            "M05",  # T-002 without evidence link
            "M08",  # checklist row without status
            "M09",  # 'verified' without evidence link
            "M10",  # no diagram
            "M11",  # repeated sentence
            "M12",  # no SECURITY.md
            "M14",  # no origin markers
        }
        self.assertTrue(expected <= codes, f"missing: {expected - codes}; findings: {findings}")

    def test_security_link_must_resolve_to_the_model(self):
        with tempfile.TemporaryDirectory() as repo:
            model = Path(repo) / "threat-model.md"
            model.write_text((FIXTURES / "model-good.md").read_text())
            (Path(repo) / "SECURITY.md").write_text("See [the model](docs/other.md).\n")
            code, findings = run(MODEL_CHECK, str(model), "--repo", repo)
        self.assertEqual(code, 1)
        self.assertIn("M12", {f["code"] for f in findings if f["level"] == "error"})


def event(payload):
    return json.dumps({"payload": payload})


def message(text):
    return event({"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": text}]})


def questions(*titles, options=("Yes", "No", "Unknown")):
    items = [{"title": t, "options": list(options)} for t in titles]
    return event({"type": "function_call", "name": "request_user_input_async",
                  "arguments": json.dumps({"questions": items})})


def write_model():
    return event({"type": "custom_tool_call", "name": "exec",
                  "input": 'apply_patch("*** Begin Patch\\n*** Add File: /repo/threat-model.md\\n+# Threat Model")'})


class TranscriptCheckTests(unittest.TestCase):
    def run_transcript(self, lines, *flags):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "rollout.jsonl"
            path.write_text("\n".join(lines) + "\n")
            return run(TRANSCRIPT_CHECK, str(path), *flags)

    def test_scenario_bound_dialogue_passes(self):
        code, result = self.run_transcript([
            message("create-threat-model · Version 0.2.0\n\nI will read PROJECT.md first."),
            questions("Who should be able to read this threat model?",
                      options=("Internal", "Public", "Not decided yet")),
            message("Candidates: T-001 document changes after review; T-002 cross-customer document access."),
            questions("T-001: Does replacing a document reopen the review?"),
            message("→ T-001 stays high. Question 2 of about 2 · T-002 Cross-customer document access"),
            questions("T-002: Do uploaded documents contain bank or health data?"),
            write_model(),
            questions("T-001: Must customers be able to correct a document after approval?"),
        ], "--scenario-bound", "--no-code")
        self.assertEqual(code, 0, result)
        self.assertEqual(result["summary"]["rounds"], 4)
        self.assertEqual(result["summary"]["questions_before_candidates"], 1)
        self.assertEqual(result["summary"]["questions_after_first_write"], 1)

    def test_violations_are_reported(self):
        long_title = "Could you please describe in as much detail as possible " * 5 + "?"
        code, result = self.run_transcript([
            message("I will start without showing the version."),
            questions("Who should be able to read this threat model?",
                      "What is the purpose?", "Which data is sensitive?", "What is the worst case?",
                      options=("Internal", "Public", "Not decided yet")),
            message("Candidates: T-001 and T-002."),
            questions("Who should be able to read this threat model?",
                      long_title,
                      "May I read more of the source code to trace data flows?"),
            questions("What is the worst outcome? And who would notice it?", options=()),
            questions("T-001: Does replacing a document reopen the review?",
                      "T-002: Do uploaded documents contain bank or health data?"),
        ], "--scenario-bound", "--no-code")
        self.assertEqual(code, 1)
        codes = {f["code"] for f in result["findings"]}
        self.assertTrue({"Q01", "Q02", "Q03", "Q04", "Q05", "Q06", "Q07", "Q09", "Q11", "Q12"} <= codes,
                        result["findings"])


if __name__ == "__main__":
    unittest.main()
