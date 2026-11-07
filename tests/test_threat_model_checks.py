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
    def check_variant(self, text):
        with tempfile.TemporaryDirectory() as repo:
            model = Path(repo) / "threat-model.md"
            model.write_text(text)
            (Path(repo) / "SECURITY.md").write_text("[Threat model](threat-model.md)\n")
            return run(MODEL_CHECK, str(model), "--repo", repo)

    def test_evidence_must_be_a_separate_populated_section_for_the_same_scenario(self):
        original = (FIXTURES / "model-good.md").read_text()
        evidence_link = "](#evidence-and-verification-for-t-001)"
        start = original.index("### Evidence and verification for T-001")
        end = original.index("### Evidence and verification for T-002")
        variants = {
            "self-reference": original.replace(evidence_link, "](#t-001-document-changes-after-review)"),
            "wrong scenario": original.replace(evidence_link, "](#evidence-and-verification-for-t-002)"),
            "missing section": original[:start] + original[end:],
            "empty section": original[:start] + "### Evidence and verification for T-001\n\n" + original[end:],
            "scenario subsection": original[:start] + original[end:],
        }
        variants["scenario subsection"] = variants["scenario subsection"].replace(
            "### T-002 Customer reads another customer's documents",
            "#### Evidence and verification for T-001\n\nNot an appendix entry.\n\n"
            "### T-002 Customer reads another customer's documents",
        )
        for name, text in variants.items():
            with self.subTest(name=name):
                code, findings = self.check_variant(text)
                self.assertEqual(code, 1, findings)
                self.assertIn("M05", {f["code"] for f in findings if f["level"] == "error"})

    def test_german_statuses_and_evidence_headings_are_valid(self):
        original = (FIXTURES / "model-good.md").read_text()
        translated = original.replace("Evidence and verification for", "Nachweise und Prüfung für")
        translated = translated.replace("evidence-and-verification-for", "nachweise-und-prüfung-für")
        for status in ("Geklärt", "Offen", "Nicht anwendbar", "Nicht untersucht"):
            with self.subTest(status=status):
                code, findings = self.check_variant(
                    translated.replace("| Open |", f"| {status} |")
                    .replace("| Not examined |", f"| {status} |")
                )
                self.assertEqual(code, 0, findings)

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

    def test_single_candidate_also_requires_bound_questions(self):
        code, result = self.run_transcript([
            message("create-threat-model · Version 0.3.3"),
            message("Candidates: T-001 document changes after review."),
            questions("Which colour should the portal use?"),
        ], "--scenario-bound")
        self.assertEqual(code, 1, result)
        self.assertIn("Q07", {f["code"] for f in result["findings"]})
        self.assertEqual(result["summary"]["questions_before_candidates"], 0)

    def test_version_may_follow_one_initial_skill_announcement(self):
        announcement = message("Ich nutze create-threat-model und lese seine Anweisungen.")
        banner = message("create-threat-model · Version 0.3.4\nReview · GrantDesk")
        cases = [
            ([announcement, banner], 0),
            ([announcement], 1),
            ([announcement, questions("Who may read the model?"), banner], 1),
            ([announcement, write_model(), banner], 1),
            ([announcement, message("Here is the assessment."), banner], 1),
            ([message("Version 0.3.4")], 1),
        ]
        for events, expected in cases:
            with self.subTest(events=events):
                code, result = self.run_transcript(events)
                self.assertEqual(code, expected, result)
                self.assertEqual("Q09" in {f["code"] for f in result["findings"]}, expected == 1)

    def test_chat_questions_and_waiting_are_explicitly_unchecked(self):
        code, result = self.run_transcript([
            message("create-threat-model · Version 0.3.3"),
            message("T-001: Who approves? T-001: Which documents? T-001: What happens next?"),
            questions("T-001: Does replacement reopen the review?"),
            write_model(),
        ], "--scenario-bound")
        self.assertEqual(code, 0, result)
        self.assertEqual(result["summary"]["questions"], 1)
        self.assertIn("chat_questions", result["coverage"]["not_checked"])
        self.assertIn("answers_and_waiting", result["coverage"]["not_checked"])
        self.assertIn("semantic_quality", result["coverage"]["not_checked"])

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
