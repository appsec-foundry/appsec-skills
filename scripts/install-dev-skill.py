#!/usr/bin/env python3
"""Install a named development snapshot of create-threat-model locally."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import tempfile


SOURCE = Path(__file__).resolve().parents[1] / "skills/create-threat-model"
DEV_NAME = "create-threat-model-dev"
MARKER = ".appsec-skills-dev.json"
LOCATIONS = {"codex": ".agents/skills", "claude": ".claude/skills"}


def read_tree(root):
    """Read regular files only; never import or replace linked content."""
    if root.is_symlink() or not root.is_dir():
        raise ValueError("Skill-Verzeichnis fehlt oder ist ein symbolischer Link.")
    files = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError("Symbolische Links im Skill werden nicht übernommen.")
        if path.is_file():
            files[path.relative_to(root).as_posix()] = path.read_bytes()
        elif not path.is_dir():
            raise ValueError("Der Skill enthält einen nicht unterstützten Dateityp.")
    return files


def hashes(files):
    return {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}


def snapshot(source):
    files = read_tree(source)
    if "SKILL.md" not in files or not any(n.startswith("references/") for n in files):
        raise ValueError("Der lokale Skill ist unvollständig.")
    revision = hashlib.sha256(
        json.dumps(hashes(files), sort_keys=True).encode()
    ).hexdigest()[:12]
    text = files["SKILL.md"].decode("utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise ValueError("SKILL.md hat kein unterstütztes Frontmatter.")
    header = match.group(1)
    header, count = re.subn(
        r"^name: create-threat-model$", f"name: {DEV_NAME}", header, flags=re.M
    )
    if count != 1:
        raise ValueError("Unerwarteter Skill-Name; keine Installation durchgeführt.")
    header, count = re.subn(
        r'^  version: "([0-9]+\.[0-9]+\.[0-9]+)"$',
        lambda m: f'  version: "{m[1]}-dev.{revision}"',
        header, flags=re.M,
    )
    if count != 1:
        raise ValueError("Unerwartetes Versionsformat; keine Installation durchgeführt.")
    header, count = re.subn(
        r"^description: ", "description: Local development snapshot. ",
        header, flags=re.M,
    )
    if count != 1:
        raise ValueError("Unerwartetes Beschreibungsformat.")
    files["SKILL.md"] = ("---\n" + header + "\n---\n" + text[match.end():]).encode()
    files[MARKER] = json.dumps(
        {"installer": "appsec-skills-dev-v1", "files": hashes(files)},
        sort_keys=True, indent=2,
    ).encode() + b"\n"
    return files, revision


def check_destination(destination):
    if not destination.exists() and not destination.is_symlink():
        return
    files = read_tree(destination)
    marker = files.pop(MARKER, None)
    if marker is None:
        raise ValueError("Das Dev-Ziel existiert bereits und gehört nicht diesem Installer.")
    try:
        recorded = json.loads(marker)
    except (ValueError, UnicodeDecodeError):
        raise ValueError("Die Installationskennung ist ungültig.") from None
    if not isinstance(recorded, dict) or recorded.get("installer") != "appsec-skills-dev-v1":
        raise ValueError("Die Installationskennung ist unbekannt.")
    if recorded.get("files") != hashes(files):
        raise ValueError(
            "Die installierte Dev-Kopie wurde verändert. Änderungen zuerst sichern "
            "und den Dev-Ordner umbenennen; anschließend erneut installieren."
        )


def install(files, destination):
    check_destination(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".appsec-dev-", dir=destination.parent) as temp:
        stage = Path(temp) / "new"
        stage.mkdir()
        for name, data in files.items():
            path = stage / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        # Check again immediately before replacement, preserving intervening edits.
        check_destination(destination)
        backup = Path(temp) / "old"
        if destination.exists():
            destination.rename(backup)
        try:
            stage.rename(destination)
        except OSError:
            if backup.exists():
                backup.rename(destination)
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("agent", choices=[*LOCATIONS, "both"])
    parser.add_argument(
        "--project", type=Path,
        help="Nur in diesem bestehenden Projekt installieren (Standard: Benutzerinstallation).",
    )
    args = parser.parse_args()
    root = args.project.expanduser().resolve() if args.project else Path.home()
    try:
        if not root.is_dir():
            raise ValueError("Das Projektverzeichnis existiert nicht.")
        files, revision = snapshot(SOURCE)
        agents = list(LOCATIONS) if args.agent == "both" else [args.agent]
        destinations = [(agent, root / LOCATIONS[agent] / DEV_NAME) for agent in agents]
        # Detect conflicts for both hosts before changing either installation.
        for _, destination in destinations:
            check_destination(destination)
        for agent, destination in destinations:
            install(files, destination)
            print(f"{agent}: {destination}")
        print(f"Dev-Stand: {revision}. Zum Aktualisieren denselben Befehl erneut ausführen.")
        print("In einer frischen Sitzung aufrufen:")
        for agent in agents:
            prefix = "$" if agent == "codex" else "/"
            print(f"  {agent}: {prefix}{DEV_NAME}")
    except (OSError, ValueError) as error:
        detail = str(error) if isinstance(error, ValueError) else error.strerror
        parser.exit(1, f"Installation fehlgeschlagen: {detail}\n")


if __name__ == "__main__":
    main()
