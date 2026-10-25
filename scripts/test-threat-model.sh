#!/usr/bin/env bash
# Prepare a fresh fictional project and optionally open an interactive Codex session.
set -euo pipefail

usage() {
    cat <<'EOF'
Usage: bash scripts/test-threat-model.sh [--prepare-only]

Creates a fresh temporary project with the current create-threat-model skill.
By default, opens Codex using your existing configuration and login.
Use --prepare-only to open the generated folder in your preferred assistant.
Results stay in that folder until you or the system remove it.
EOF
}

prepare_only=false
if [[ $# -gt 1 ]]; then
    usage >&2
    exit 2
fi
case "${1:-}" in
    '') ;;
    --prepare-only) prepare_only=true ;;
    --help|-h) usage; exit 0 ;;
    *) usage >&2; exit 2 ;;
esac

if [[ "$prepare_only" == false ]] && ! command -v codex >/dev/null 2>&1; then
    printf '%s\n' 'Codex CLI nicht gefunden. Nutze --prepare-only und öffne den Testordner in deiner App.' >&2
    exit 1
fi

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
skill_dir="$script_dir/../skills/create-threat-model"
if [[ ! -f "$skill_dir/SKILL.md" || ! -d "$skill_dir/references" ]]; then
    printf '%s\n' 'Der lokale create-threat-model Skill ist unvollständig.' >&2
    exit 1
fi

test_dir="$(mktemp -d "${TMPDIR:-/tmp}/threat-model-test.XXXXXXXX")"
printf 'Testprojekt: %s\n' "$test_dir"
mkdir -p -- "$test_dir/.agents/skills"
cp -R -- "$skill_dir" "$test_dir/.agents/skills/create-threat-model"

cat > "$test_dir/PROJECT.md" <<'EOF'
# Kundenportal für Anträge

Dieses fiktive, noch nicht implementierte System soll Kunden ermöglichen,
Anträge zu stellen und zugehörige Dokumente hochzuladen.

- Kunden melden sich an und sehen ihre eigenen Anträge und Dokumente.
- Sachbearbeiter prüfen die ihnen zugewiesenen Anträge und geben sie frei.
- Kunden können Dokumente bis zur Freigabe ersetzen.
- Das Portal speichert Anträge in einer Datenbank und Dokumente in einem Dateispeicher.
- Ein externer E-Mail-Dienst versendet Statusmeldungen an die Antragsteller.
- Das Produktteam verantwortet die fachlichen Regeln.

Weitere fachliche und betriebliche Details sind noch zu klären.
EOF

cat > "$test_dir/PROMPT.txt" <<'EOF'
Nutze $create-threat-model aus .agents/skills/create-threat-model/SKILL.md.
Erstelle für das in PROJECT.md beschriebene System ein Threat Model
in diesem Testprojekt. Beginne mit den vorhandenen Unterlagen.
EOF

printf '%s\n' 'Erwartete Ergebnisse: threat-model.md und SECURITY.md im Testprojekt.'
if [[ "$prepare_only" == true ]]; then
    printf '%s\n' 'Öffne den Testordner in deiner App und sende den Text aus PROMPT.txt.'
else
    printf '%s\n' 'Starte Codex. Beantworte die Rückfragen oder überspringe sie für einen weiteren Testfall.'
    exec codex -C "$test_dir" "$(cat "$test_dir/PROMPT.txt")"
fi
