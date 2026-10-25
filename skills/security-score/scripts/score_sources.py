"""Bounded, read-only local source and Git selection for the internal score."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import signal
import stat
import subprocess
import threading
import time
import unicodedata

from score_core import change_supported, supported


MAX_FILES = 3000
MAX_FILE = 524288
MAX_BYTES = 20 * 1024 * 1024
MAX_PATCH = 4 * 1024 * 1024
MAX_TOOL = 24 * 1024 * 1024
EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "target",
    "coverage",
    "__pycache__",
    ".venv",
    "venv",
}
SENSITIVE = {
    ".env",
    ".npmrc",
    ".pypirc",
    "credentials",
    "credentials.json",
    "secrets.json",
    "id_rsa",
    "id_ed25519",
}


class SourceError(ValueError):
    pass


class Budget:
    def __init__(self, seconds=15):
        self.deadline = time.monotonic() + seconds

    def check(self):
        if time.monotonic() >= self.deadline:
            raise SourceError(
                "Execution time limit reached; no complete score is available."
            )

    def remaining(self):
        self.check()
        return max(0.01, self.deadline - time.monotonic())


def label(value):
    return "".join(
        " " if unicodedata.category(c) in {"Cc", "Cf", "Cs"} else c for c in str(value)
    )[:240]


def relative(path):
    if (
        not isinstance(path, str)
        or not path
        or len(path) > 1024
        or "\\" in path
        or ":" in path
    ):
        raise SourceError("Unsupported or unsafe source path.")
    parts = PurePosixPath(path).parts
    if (
        path.startswith("/")
        or any(part in {"..", ".git"} for part in parts)
        or any(unicodedata.category(c) in {"Cc", "Cf", "Cs"} for c in path)
    ):
        raise SourceError("Unsupported or unsafe source path.")
    return PurePosixPath(*parts).as_posix()


def excluded(path):
    parts = PurePosixPath(path).parts
    name = parts[-1].lower()
    return (
        bool(set(parts) & EXCLUDED_DIRS)
        or name in SENSITIVE
        or name.startswith(".env.")
        or name.endswith((".pem", ".key", ".p12", ".pfx"))
    )


def stop(process):
    if os.name == "posix":
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    elif process.poll() is None:
        process.kill()
    process.wait()


def command(
    arguments, budget, *, cwd=None, data=None, limit=MAX_TOOL, allow_failure=False
):
    """Bound both output and time; never expose subprocess diagnostics or source."""
    budget.check()
    process = subprocess.Popen(
        arguments,
        cwd=cwd,
        stdin=subprocess.PIPE if data is not None else subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        start_new_session=os.name == "posix",
    )
    output = bytearray()
    too_large = threading.Event()

    def read():
        while True:
            chunk = process.stdout.read(16384)
            if not chunk:
                break
            if len(output) + len(chunk) > limit:
                too_large.set()
                try:
                    process.kill()
                except ProcessLookupError:
                    pass
                break
            output.extend(chunk)

    def write():
        try:
            process.stdin.write(data)
            process.stdin.close()
        except (BrokenPipeError, OSError):
            pass

    reader = threading.Thread(target=read, daemon=True)
    reader.start()
    writer = threading.Thread(target=write, daemon=True) if data is not None else None
    if writer:
        writer.start()
    try:
        process.wait(timeout=budget.remaining())
        reader.join(timeout=budget.remaining())
        if reader.is_alive():
            raise SourceError("A tool did not close its output within the time limit.")
        if too_large.is_set():
            raise SourceError("Tool output exceeded the source limit.")
        if process.returncode and not allow_failure:
            raise SourceError(
                "A source or engine command failed; check the selection and installation."
            )
        return process.returncode, bytes(output)
    except subprocess.TimeoutExpired:
        raise SourceError(
            "Execution time limit reached; no complete score is available."
        ) from None
    finally:
        stop(process)
        reader.join(timeout=1)
        if writer:
            writer.join(timeout=1)
        process.stdout.close()


def git(root, budget, *args, data=None, limit=MAX_TOOL):
    prefix = [
        "git",
        "--no-pager",
        "--literal-pathspecs",
        "-c",
        "core.hooksPath=/dev/null",
        "-c",
        "core.fsmonitor=",
        "-c",
        "diff.external=",
    ]
    # Worktree diffs can invoke clean filters even with external diffs disabled.
    cache = getattr(budget, "git_filters", {})
    identity = str(root)
    if identity not in cache:
        names = command(
            [*prefix, "config", "--list", "--name-only", "-z"],
            budget,
            cwd=root,
            limit=65536,
        )[1]
        drivers = set()
        for raw in names.split(b"\0"):
            name = raw.decode("utf-8")
            if name.startswith("filter.") and name.count(".") >= 2:
                driver = name[len("filter.") : name.rindex(".")]
                if "=" in driver or any(ord(c) < 32 for c in driver):
                    raise SourceError("Cannot neutralize repository content filters.")
                drivers.add(driver)
        cache[identity] = [
            value
            for driver in sorted(drivers)
            for key, setting in (
                ("clean", ""),
                ("smudge", ""),
                ("process", ""),
                ("required", "false"),
            )
            for value in ("-c", f"filter.{driver}.{key}={setting}")
        ]
        budget.git_filters = cache
    return command(
        [*prefix, *cache[identity], *args], budget, cwd=root, data=data, limit=limit
    )[1]


def resolve(root, revision, budget):
    if not revision or len(revision) > 256 or any(ord(c) < 32 for c in revision):
        raise SourceError("Invalid Git revision.")
    value = (
        git(
            root,
            budget,
            "rev-parse",
            "--verify",
            "--end-of-options",
            revision + "^{commit}",
        )
        .decode()
        .strip()
    )
    if not re.fullmatch(r"[0-9a-f]{40,64}", value):
        raise SourceError("Cannot resolve the selected Git revision.")
    return value


def regular_read(root, path, budget, maximum=MAX_FILE):
    """Use descriptor-relative no-follow reads to reject links and parent races."""
    budget.check()
    if not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
        raise SourceError(
            "This runtime requires descriptor-relative no-follow file access."
        )
    parts = relative(path).split("/")
    directory = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in parts[:-1]:
            child = os.open(
                part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory
            )
            os.close(directory)
            directory = child
        descriptor = os.open(
            parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory
        )
        with os.fdopen(descriptor, "rb") as handle:
            before = os.fstat(handle.fileno())
            if not stat.S_ISREG(before.st_mode):
                raise SourceError("Selected source contains a link or special file.")
            if before.st_size > maximum:
                return None, "oversized", bool(before.st_mode & 0o111)
            data = handle.read(maximum + 1)
            after = os.fstat(handle.fileno())
            if (before.st_size, before.st_mtime_ns, before.st_ino) != (
                after.st_size,
                after.st_mtime_ns,
                after.st_ino,
            ):
                raise SourceError("Selected source changed while being read.")
            if len(data) > maximum:
                return None, "oversized", bool(after.st_mode & 0o111)
            return data, None, bool(after.st_mode & 0o111)
    except OSError:
        raise SourceError(
            "Cannot read selected source without following links; no score is available."
        ) from None
    finally:
        os.close(directory)


def decode(data):
    if b"\0" in data:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeError:
        return None


def inventory(root, budget):
    # Git enumeration respects ignores without evaluating content filters.
    if (root / ".git").exists():
        values = (
            git(
                root,
                budget,
                "ls-files",
                "--cached",
                "--others",
                "--exclude-standard",
                "-z",
            )
            .decode("utf-8")
            .split("\0")
        )
    else:
        values = []
        for parent, dirs, names in os.walk(root, followlinks=False):
            budget.check()
            dirs[:] = sorted(name for name in dirs if name not in EXCLUDED_DIRS)
            # Linked directories do not silently become an inspected surface.
            if any((Path(parent) / name).is_symlink() for name in dirs):
                raise SourceError("Selected source contains a linked directory.")
            for name in names:
                values.append((Path(parent) / name).relative_to(root).as_posix())
            if len(values) > MAX_FILES:
                raise SourceError("Source inventory exceeds the file limit.")
    paths = sorted({relative(value) for value in values if value})
    if len(paths) > MAX_FILES:
        raise SourceError("Source inventory exceeds the file limit.")
    return paths


def working(root, paths, budget, context=False):
    files, exclusions = {}, []
    size = 0
    for path in paths:
        budget.check()
        if excluded(path) or not (
            change_supported(path) if context else supported(path)
        ):
            exclusions.append(
                {"file": label(path), "reason": "excluded or unsupported"}
            )
            continue
        if not os.path.lexists(root / path):
            continue  # A tracked worktree deletion.
        data, reason, executable = regular_read(root, path, budget)
        text = decode(data) if data is not None else None
        if text is None:
            exclusions.append(
                {"file": label(path), "reason": reason or "binary or non-UTF-8"}
            )
            continue
        size += len(data)
        if size > MAX_BYTES:
            raise SourceError("Selected source exceeds the aggregate byte limit.")
        files[path] = {"text": text, "executable": executable}
    return files, exclusions


def objects(root, revision, paths, budget, *, index=False, context=False):
    files, exclusions, wanted = {}, [], []
    if not paths:
        return files, exclusions
    if index:
        rows = git(root, budget, "ls-files", "--stage", "-z", "--", *paths)
    else:
        rows = git(
            root, budget, "ls-tree", "-r", "-z", "--full-tree", revision, "--", *paths
        )
    for row in rows.split(b"\0"):
        if not row:
            continue
        meta, raw_path = row.split(b"\t", 1)
        fields = meta.decode("ascii").split()
        mode, oid = fields[0], fields[1] if index else fields[2]
        path = relative(raw_path.decode("utf-8"))
        if index and fields[2] != "0":
            raise SourceError("Unmerged index entries cannot be scored.")
        if mode not in {"100644", "100755"}:
            exclusions.append({"file": label(path), "reason": "link or submodule"})
        elif excluded(path) or not (
            change_supported(path) if context else supported(path)
        ):
            exclusions.append(
                {"file": label(path), "reason": "excluded or unsupported"}
            )
        else:
            wanted.append((path, oid))
    if not wanted:
        return files, exclusions
    query = "".join(oid + "\n" for _, oid in wanted).encode("ascii")
    sizes = (
        git(root, budget, "cat-file", "--batch-check", data=query)
        .decode("ascii")
        .splitlines()
    )
    if len(sizes) != len(wanted):
        raise SourceError("Invalid Git object metadata.")
    kept = []
    total = 0
    for (path, oid), row in zip(wanted, sizes):
        fields = row.split()
        if len(fields) != 3 or fields[0] != oid or fields[1] != "blob":
            raise SourceError("Invalid Git source object.")
        size = int(fields[2])
        if size > MAX_FILE:
            exclusions.append({"file": label(path), "reason": "oversized"})
        else:
            kept.append((path, oid, size))
            total += size
    if total > MAX_BYTES:
        raise SourceError("Selected source exceeds the aggregate byte limit.")
    if not kept:
        return files, exclusions
    data = git(
        root,
        budget,
        "cat-file",
        "--batch",
        data="".join(oid + "\n" for _, oid, _ in kept).encode("ascii"),
    )
    cursor = 0
    executable_modes = {
        relative(row.split(b"\t", 1)[1].decode("utf-8")): row.startswith(b"100755 ")
        for row in rows.split(b"\0")
        if row
    }
    for path, oid, size in kept:
        end = data.find(b"\n", cursor)
        if data[cursor:end] != f"{oid} blob {size}".encode("ascii"):
            raise SourceError("Invalid Git source output.")
        content = data[end + 1 : end + 1 + size]
        if len(content) != size or data[end + 1 + size : end + 2 + size] != b"\n":
            raise SourceError("Truncated Git source output.")
        cursor = end + 2 + size
        text = decode(content)
        if text is None:
            exclusions.append({"file": label(path), "reason": "binary or non-UTF-8"})
        else:
            files[path] = {"text": text, "executable": executable_modes[path]}
    if cursor != len(data):
        raise SourceError("Unexpected Git source output.")
    return files, exclusions


def fingerprint(files):
    digest = hashlib.sha256()
    for path, source in sorted(files.items()):
        encoded = source["text"].encode("utf-8")
        digest.update(
            path.encode("utf-8") + b"\0" + len(encoded).to_bytes(8, "big") + encoded
        )
        if "executable" in source:
            digest.update(b"executable:" + str(source["executable"]).encode())
        if source.get("fragment"):
            digest.update(json.dumps(source.get("lines", {}), sort_keys=True).encode())
    return digest.hexdigest()


def patch_path(value):
    value = value.split("\t", 1)[0]
    if value == "/dev/null":
        return None
    if value.startswith('"'):
        raise SourceError(
            "Quoted patch paths need a local Git comparison or an unquoted normalized patch."
        )
    if value.startswith(("a/", "b/")):
        value = value[2:]
    return relative(value)


def parse_patch(text, budget):
    """Read unified hunks as fragments; never open a path named by a patch."""
    before, after, exclusions = {}, {}, []
    old_path = new_path = None
    old_line = new_line = 0
    old_left = new_left = 0
    in_hunk = False
    hunks = 0
    git_block_hunks = None

    def append(files, path, line, content, changed=False):
        if path is None:
            raise SourceError("Invalid addition or deletion in patch.")
        if excluded(path) or not change_supported(path):
            return
        source = files.setdefault(
            path, {"text": "", "lines": {}, "fragment": True, "fragments": []}
        )
        if not source["fragments"] or source["fragments"][-1]["hunk"] != hunks:
            source["fragments"].append(
                {"text": "", "lines": {}, "fragment": True, "hunk": hunks}
            )
        fragment = source["fragments"][-1]
        if line <= source.get("last_line", 0):
            raise SourceError("Patch hunks overlap or contain invalid line positions.")
        source["last_line"] = line
        if changed:
            source.setdefault("changed_lines", []).append(line)
        fragment["lines"][len(fragment["lines"]) + 1] = line
        fragment["text"] += content + "\n"
        number = len(source["lines"]) + 1
        source["lines"][number] = line
        source["text"] += content + "\n"
        if len(source["text"].encode()) > MAX_FILE:
            raise SourceError("Patch fragment exceeds the per-file limit.")

    for raw in text.splitlines():
        budget.check()
        if len(raw) > 16384:
            raise SourceError("Patch line exceeds the supported limit.")
        if in_hunk and (old_left or new_left):
            prefix, content = raw[:1], raw[1:]
            if prefix == "\\":
                continue
            if prefix not in {" ", "+", "-"}:
                raise SourceError("Malformed or truncated unified patch.")
            if prefix in {" ", "-"}:
                old_left -= 1
                append(before, old_path, old_line, content, prefix == "-")
                old_line += 1
            if prefix in {" ", "+"}:
                new_left -= 1
                append(after, new_path, new_line, content, prefix == "+")
                new_line += 1
            if old_left < 0 or new_left < 0:
                raise SourceError("Patch hunk counts do not match.")
            continue
        if raw.startswith("diff --git "):
            if git_block_hunks is not None and git_block_hunks == hunks:
                raise SourceError(
                    "Metadata-only patch entries need a local Git comparison."
                )
            git_block_hunks = hunks
            old_path = new_path = None
            in_hunk = False
        elif raw.startswith(
            (
                "old mode ",
                "new mode ",
                "rename from ",
                "rename to ",
                "copy from ",
                "copy to ",
            )
        ) or (
            raw.startswith(("new file mode ", "deleted file mode "))
            and raw.rsplit(" ", 1)[-1] != "100644"
        ):
            raise SourceError(
                "Permission and rename/copy patches need a local Git comparison."
            )
        elif raw.startswith("--- "):
            old_path = patch_path(raw[4:])
            new_path = None
            in_hunk = False
        elif raw.startswith("+++ "):
            new_path = patch_path(raw[4:])
            for path in (old_path, new_path):
                if path and (excluded(path) or not change_supported(path)):
                    exclusions.append(
                        {"file": label(path), "reason": "excluded or unsupported"}
                    )
        elif raw.startswith("@@"):
            match = re.fullmatch(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@.*", raw)
            if not match or (old_path is None and new_path is None):
                raise SourceError("Malformed unified patch header.")
            old_line, old_left = int(match[1]), int(match[2] or 1)
            new_line, new_left = int(match[3]), int(match[4] or 1)
            if (old_left and old_line < 1) or (new_left and new_line < 1):
                raise SourceError("Invalid patch line position.")
            hunks += 1
            in_hunk = True
        elif raw.startswith(("Binary files ", "GIT binary patch")):
            raise SourceError("Binary patches need a local Git comparison.")
        elif (
            raw.startswith(("+", "-", " "))
            and in_hunk
            and not raw.startswith(("---", "+++"))
        ):
            raise SourceError("Unexpected content after a patch hunk.")
    if git_block_hunks is not None and git_block_hunks == hunks:
        raise SourceError("Metadata-only patch entries need a local Git comparison.")
    if old_left or new_left or not hunks:
        raise SourceError("No complete unified patch hunks found.")
    if len(set(before) | set(after)) > MAX_FILES:
        raise SourceError("Patch exceeds the file limit.")
    return before, after, exclusions


def select(options, budget):
    root = Path(options.repo).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise SourceError("Select an existing repository directory.")
    if options.patch:
        patch = Path(options.patch).expanduser()
        raw, reason, _ = regular_read(
            patch.parent.resolve(strict=True), patch.name, budget, MAX_PATCH
        )
        if raw is None or len(raw) > MAX_PATCH:
            raise SourceError("Patch exceeds the input limit.")
        text = decode(raw)
        if text is None:
            raise SourceError("Patch must be UTF-8 text.")
        before, after, exclusions = parse_patch(text, budget)
        return (
            before,
            after,
            exclusions,
            {
                "kind": "change",
                "selection": "patch",
                "repository": label(root),
                "context": "fragments only",
            },
            None,
        )
    is_change = (
        options.base is not None
        or options.commit
        or options.staged
        or options.unstaged
        or options.worktree
    )
    if not is_change:
        paths = inventory(root, budget)
        after, exclusions = working(root, paths, budget)

        def verify():
            if inventory(root, budget) != paths or fingerprint(
                working(root, paths, budget)[0]
            ) != fingerprint(after):
                raise SourceError(
                    "Selected source changed during analysis; rerun against a stable source."
                )

        return (
            {},
            after,
            exclusions,
            {
                "kind": "repository",
                "selection": "working files",
                "repository": label(root),
            },
            verify,
        )
    top = git(root, budget, "rev-parse", "--show-toplevel").decode().strip()
    if root != Path(top).resolve():
        raise SourceError("Git comparisons require the selected top-level checkout.")
    if options.commit:
        head = resolve(root, options.commit, budget)
        base = resolve(root, head + "^", budget)
    elif options.base:
        base, head = (
            resolve(root, options.base, budget),
            resolve(root, options.head or "HEAD", budget),
        )
    elif options.unstaged:
        base, head = "index", "worktree"
    elif options.staged:
        base, head = resolve(root, "HEAD", budget), "index"
    else:
        base, head = resolve(root, "HEAD", budget), "worktree"
    diff = [
        "diff",
        "--no-ext-diff",
        "--no-textconv",
        "--no-renames",
        "--name-only",
        "-z",
    ]
    if options.staged:
        diff += ["--cached", base]
    elif options.unstaged:
        pass
    elif head == "worktree":
        diff += [base]
    else:
        diff += [base, head]

    def selected_paths():
        selected = {
            relative(value)
            for value in git(root, budget, *diff, "--").decode("utf-8").split("\0")
            if value
        }
        if options.worktree:
            selected.update(
                relative(value)
                for value in git(
                    root, budget, "ls-files", "--others", "--exclude-standard", "-z"
                )
                .decode("utf-8")
                .split("\0")
                if value
            )
        return sorted(selected)

    paths = selected_paths()
    if len(paths) > MAX_FILES:
        raise SourceError("Change exceeds the file limit.")
    before, old_exclusions = objects(
        root, base, paths, budget, index=base == "index", context=True
    )
    after, exclusions = (
        working(root, paths, budget, context=True)
        if head == "worktree"
        else objects(root, head, paths, budget, index=head == "index", context=True)
    )

    def verify():
        if (
            head in {"worktree", "index"} or base == "index"
        ) and selected_paths() != paths:
            raise SourceError("Selected change scope changed during analysis.")
        if head == "worktree" and fingerprint(
            working(root, paths, budget, context=True)[0]
        ) != fingerprint(after):
            raise SourceError("Working source changed during analysis.")
        if base == "index" or head == "index":
            current = objects(root, "index", paths, budget, index=True, context=True)[0]
            if fingerprint(current) != fingerprint(
                before if base == "index" else after
            ):
                raise SourceError("Index source changed during analysis.")

    return (
        before,
        after,
        [*old_exclusions, *exclusions],
        {
            "kind": "change",
            "selection": "git",
            "repository": label(root),
            "base": base,
            "head": head,
        },
        verify,
    )
