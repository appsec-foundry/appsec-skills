"""Opt-in public Analyzer preview checks using fictional, disposable sources.

Set APPSEC_ANALYZER_TEST_EXECUTABLE to a trusted absolute executable path.
The default suite requires no Analyzer. These tests never request paid analysis.
"""

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ENGINE = os.environ.get("APPSEC_ANALYZER_TEST_EXECUTABLE")


@unittest.skipUnless(ENGINE, "optional Analyzer preview tests not selected")
class AnalyzeThreatsPreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        executable = Path(ENGINE)
        if not executable.is_absolute() or not executable.is_file():
            raise ValueError("Select a trusted absolute Analyzer executable path")
        result = subprocess.run(
            [ENGINE, "capabilities"], capture_output=True, text=True, timeout=20
        )
        if result.returncode:
            raise AssertionError(result.stderr)
        capabilities = json.loads(result.stdout)
        if capabilities.get("interface_version") != 1:
            raise AssertionError("Analyzer interface 1 is required for these cases")
        analysis = capabilities.get("analyze_threats", {})
        if not analysis.get("available") or analysis.get("preview_model_calls") is not False:
            raise AssertionError("A public preview without model calls is required")

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="analyze-threats-preview-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "tenant portal"
        self.repo.mkdir()
        (self.repo / "docs").mkdir()
        self.design = self.repo / "docs/export.md"
        self.design.write_text(
            "# Export design\nTenant members export their own invoices.\n"
            "A queued worker processes jobs. Downloads require the recipient to sign in.\n"
        )
        (self.repo / "threat-model.md").write_text(
            "# Tenant portal threat model\n\n"
            "## T-003: Cross-tenant export\n"
            "Worker authorization is planned, not verified.\n\n"
            "## T-008: Unexpected recipient\n"
            "Assumption: downloads require the recipient to sign in.\n"
        )
        (self.repo / "SECURITY.md").write_text(
            "# Security\nSee [threat model](threat-model.md).\n"
        )
        self.git("init", "-b", "main")
        self.commit("Baseline design")
        self.base = self.git("rev-parse", "HEAD")
        self.design.write_text(
            "# Export design\nTenant members export their own invoices.\n"
            "A queued worker processes jobs. External auditors can use shareable links.\n"
        )
        self.commit("Shareable downloads")
        self.head = self.git("rev-parse", "HEAD")

    def git(self, *arguments):
        result = subprocess.run(
            [
                "git", "-C", str(self.repo),
                "-c", "core.hooksPath=/dev/null",
                "-c", "user.name=Preview fixture",
                "-c", "user.email=fixture@example.invalid",
                *arguments,
            ],
            capture_output=True, text=True, timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def commit(self, message):
        self.git("add", ".")
        self.git("commit", "--no-gpg-sign", "-m", message)

    def snapshot(self):
        return {
            path.relative_to(self.repo): path.read_bytes()
            for path in self.repo.rglob("*")
            if path.is_file() and ".git" not in path.relative_to(self.repo).parts
        }

    def preview(self, *selection, expected_exit=0):
        before = self.snapshot()
        status = self.git("status", "--porcelain")
        result = subprocess.run(
            [
                ENGINE, "analyze-threats",
                "Analyze the export feature and compare relevant model scenarios.",
                "--repo", str(self.repo), *selection,
                "--preview", "--non-interactive",
            ],
            cwd=self.root,
            env={**os.environ, "XDG_STATE_HOME": str(self.root / "state")},
            capture_output=True, text=True, timeout=20,
        )
        self.assertEqual(result.returncode, expected_exit, result.stderr)
        self.assertEqual(self.snapshot(), before, "Preview changed source documents")
        self.assertEqual(self.git("status", "--porcelain"), status)
        return result.stdout + result.stderr

    def test_design_discovers_markdown_model(self):
        output = self.preview("--design-file", str(self.design))
        self.assertIn("threat-model.md @ worktree (delivered)", output)

    def test_explicit_markdown_model(self):
        output = self.preview(
            "--design-file", str(self.design), "--threat-model", "threat-model.md"
        )
        self.assertIn("threat-model.md @ worktree (delivered)", output)

    def test_comparison_captures_both_context_versions(self):
        output = self.preview(
            "--base", self.base, "--head", self.head,
            "--context", "docs/export.md",
        )
        for side, revision in (("baseline", self.base), ("proposed", self.head)):
            for document in ("docs/export.md", "threat-model.md"):
                self.assertIn(f"{side}:{document} @ {revision} (delivered)", output)

    def test_missing_model_does_not_block_design_preview(self):
        (self.repo / "threat-model.md").unlink()
        output = self.preview("--design-file", str(self.design))
        self.assertNotIn("threat-model.md @ worktree (delivered)", output)

    def test_missing_explicit_model_fails(self):
        self.preview(
            "--design-file", str(self.design),
            "--threat-model", "absent-model.md", expected_exit=2,
        )

    def test_automatic_context_can_be_excluded(self):
        for option in ("--no-context", "--isolated"):
            with self.subTest(option=option):
                output = self.preview("--design-file", str(self.design), option)
                self.assertNotIn("threat-model.md @ worktree (delivered)", output)

    def test_no_context_still_allows_explicit_model(self):
        output = self.preview(
            "--design-file", str(self.design), "--no-context",
            "--threat-model", "threat-model.md",
        )
        self.assertIn("threat-model.md @ worktree (delivered)", output)


if __name__ == "__main__":
    unittest.main()
