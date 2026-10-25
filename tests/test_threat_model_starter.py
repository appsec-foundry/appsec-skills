"""Test local preparation and CLI handoff without making model calls."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
STARTER = ROOT / "scripts/test-threat-model.sh"


class ThreatModelStarterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="threat-model-starter-tests-")
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.env = {**os.environ, "TMPDIR": str(self.work)}

    def run_starter(self, *args):
        return subprocess.run(
            ["/bin/bash", str(STARTER), *args],
            cwd=self.work,
            env=self.env,
            capture_output=True,
            text=True,
            timeout=10,
        )

    def test_prepare_copies_current_skill_and_keeps_runs_separate(self):
        for _ in range(2):
            result = self.run_starter("--prepare-only")
            self.assertEqual(result.returncode, 0, result.stderr)
        projects = list(self.work.glob("threat-model-test.*"))
        self.assertEqual(len(projects), 2)
        source = ROOT / "skills/create-threat-model"
        for project in projects:
            copy = project / ".agents/skills/create-threat-model"
            self.assertFalse(copy.is_symlink())
            for original in source.rglob("*"):
                if original.is_file():
                    self.assertEqual(
                        original.read_bytes(),
                        (copy / original.relative_to(source)).read_bytes(),
                    )
            self.assertTrue((project / "PROJECT.md").is_file())
            self.assertTrue((project / "PROMPT.txt").is_file())
            self.assertFalse((project / "threat-model.md").exists())

    def test_launch_passes_exact_workspace_and_prompt(self):
        # Spaces and shell syntax in the directory must remain literal arguments.
        temp_parent = self.work / "space ; touch SHOULD_NOT_EXIST"
        temp_parent.mkdir()
        self.env["TMPDIR"] = str(temp_parent)
        bin_dir = self.work / "bin"
        bin_dir.mkdir()
        fake_codex = bin_dir / "codex"
        fake_codex.write_text(
            '#!/bin/bash\nprintf "%s\\0" "$@" > "$STARTER_TEST_CAPTURE"\n'
        )
        fake_codex.chmod(0o700)
        capture = self.work / "arguments"
        self.env["PATH"] = str(bin_dir) + os.pathsep + os.environ["PATH"]
        self.env["STARTER_TEST_CAPTURE"] = str(capture)
        result = self.run_starter()
        self.assertEqual(result.returncode, 0, result.stderr)
        project, = temp_parent.glob("threat-model-test.*")
        arguments = capture.read_bytes().split(b"\0")[:-1]
        self.assertEqual(arguments, [
            b"-C",
            os.fsencode(project),
            (project / "PROMPT.txt").read_bytes().rstrip(b"\n"),
        ])
        self.assertFalse((self.work / "SHOULD_NOT_EXIST").exists())

    def test_invalid_arguments_create_nothing(self):
        for arguments in (("--unknown",), ("--prepare-only", "extra")):
            result = self.run_starter(*arguments)
            self.assertEqual(result.returncode, 2)
        self.assertEqual(list(self.work.iterdir()), [])

    def test_missing_codex_exits_before_creating_project(self):
        self.env["PATH"] = str(self.work)
        result = self.run_starter()
        self.assertEqual(result.returncode, 1)
        self.assertIn("--prepare-only", result.stderr)
        self.assertEqual(list(self.work.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
