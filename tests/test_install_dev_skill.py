"""Exercise dev installation in disposable projects, without touching user skills."""

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/install-dev-skill.py"
spec = importlib.util.spec_from_file_location("dev_installer", SCRIPT)
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class DevInstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="appsec-dev-test-")
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        self.destination = self.project / ".agents/skills" / installer.DEV_NAME
        self.files, self.revision = installer.snapshot(installer.SOURCE)

    def test_both_hosts_and_regular_skill_coexist(self):
        original = self.destination.parent / "create-threat-model"
        original.mkdir(parents=True)
        (original / "SKILL.md").write_text("existing production skill")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "both", "--project", str(self.project)],
            capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        for location in installer.LOCATIONS.values():
            target = self.project / location / installer.DEV_NAME
            installed = installer.read_tree(target)
            self.assertEqual(installed, self.files)
            self.assertIn(b"name: create-threat-model-dev\n", installed["SKILL.md"])
            self.assertIn(self.revision.encode(), installed["SKILL.md"])
        self.assertEqual((original / "SKILL.md").read_text(), "existing production skill")

    def test_refresh_replaces_snapshot_and_removes_obsolete_files(self):
        installer.install(self.files, self.destination)
        source = self.project / "source"
        source.mkdir()
        for name, data in installer.read_tree(installer.SOURCE).items():
            path = source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        (source / "README.md").unlink()
        reference = source / "references/checklist.md"
        reference.write_text(reference.read_text() + "\nDevelopment change.\n")
        updated, revision = installer.snapshot(source)
        self.assertNotEqual(revision, self.revision)
        installer.install(updated, self.destination)
        self.assertEqual(installer.read_tree(self.destination), updated)

    def test_modified_install_is_preserved(self):
        installer.install(self.files, self.destination)
        path = self.destination / "SKILL.md"
        path.write_text("local edit")
        with self.assertRaisesRegex(ValueError, "verändert"):
            installer.install(self.files, self.destination)
        self.assertEqual(path.read_text(), "local edit")

    def test_unmanaged_and_linked_targets_are_preserved(self):
        self.destination.mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "gehört nicht"):
            installer.install(self.files, self.destination)
        self.destination.rmdir()
        outside = self.project / "outside"
        outside.mkdir()
        (outside / "keep").write_text("preserve")
        self.destination.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            installer.install(self.files, self.destination)
        self.assertEqual((outside / "keep").read_text(), "preserve")

    def test_source_link_is_rejected(self):
        source = self.project / "source"
        source.mkdir()
        (source / "SKILL.md").symlink_to(installer.SOURCE / "SKILL.md")
        with self.assertRaisesRegex(ValueError, "Links"):
            installer.snapshot(source)

    def test_failed_replacement_restores_previous_install(self):
        installer.install(self.files, self.destination)
        original_rename = Path.rename

        def fail_stage(path, target):
            if path.name == "new":
                raise OSError("simulated failure")
            return original_rename(path, target)

        with patch.object(Path, "rename", fail_stage):
            with self.assertRaises(OSError):
                installer.install(self.files, self.destination)
        self.assertEqual(installer.read_tree(self.destination), self.files)


if __name__ == "__main__":
    unittest.main()
