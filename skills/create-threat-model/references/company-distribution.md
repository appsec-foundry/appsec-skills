# Company distribution and customization

Use this guide to maintain `create-threat-model` in an existing company repository with several skills under `skills/`. The company repository holds the version developers install, including your changes. Upstream remains a separate Git source.

## Repository layout

```text
company-skills/
  skills/
    create-threat-model/
      SKILL.md
      README.md
      references/
    another-skill/
      SKILL.md
  context/
    security-requirements.md
    known-threats.md
  UPSTREAM.md
```

Keep company knowledge under `context/` or in project documents. Change the skill itself when you need a different workflow. Both forms can coexist.

## Import the skill

These commands run in your company repository and require Git. Start with a clean working tree and no existing `skills/create-threat-model/` directory. If you already have a modified copy, preserve it and establish its upstream base before using the update procedure.

Add the source remote once and fetch its history:

```bash
git remote add appsec-upstream https://github.com/appsec-foundry/appsec-skills.git
git fetch appsec-upstream
```

Select a reviewed upstream commit. Replace the placeholder below with its full SHA; do not leave a moving branch name in your provenance record.

```bash
imported_upstream='FULL_UPSTREAM_COMMIT_SHA'
git restore --source="$imported_upstream" --staged --worktree -- skills/create-threat-model
git diff --cached --stat
```

This imports the complete skill directory without merging the other repository's root files or other skills. Add an entry to `UPSTREAM.md`:

```markdown
## create-threat-model

- Source: https://github.com/appsec-foundry/appsec-skills.git
- Path: skills/create-threat-model
- Commit: FULL_UPSTREAM_COMMIT_SHA
- Company release: company.1
```

Preserve any applicable license and attribution notices. Commit the import and provenance before making company changes:

```bash
git add UPSTREAM.md
git commit -m "Import create-threat-model from recorded upstream commit"
```

## Make company changes

Edit `skills/create-threat-model/SKILL.md` and its references in the company repository. Commit those changes separately from the import. Do not edit developers' installed copies; reinstall from the company repository after a change.

Keep the skill's `name` as `create-threat-model` if you want the same invocation. Give each company release a distinct `metadata.version`, such as `0.1.0-company.1`, so the opening message identifies the installed variant. Avoid installing two variants under the same name in overlapping locations.

Keep instructions, examples, README, and expected behavior consistent. For a changed workflow, use a small fictional project to check the intended behavior before distribution. README links to repository-level files may need company equivalents or explicit upstream URLs.

Autonomous integrations must enforce cumulative time, call, retry, and delegation budgets outside the model, validate and authorize tool arguments, and test cancellation and denied actions before deployment. This skill provides no such enforcement.

## Supply company context

The current skill reads explicitly selected Markdown or plain-text sources. Placing files under `context/` or copying them into the skill does not automatically select them. For example, with a local company checkout at `/work/company-skills`:

```text
Use create-threat-model for this project.
Start with docs/requirements.md and docs/architecture.md.
Include these company sources:
- /work/company-skills/context/security-requirements.md
- /work/company-skills/context/known-threats.md
```

Replace these paths with accessible locations. Give company requirements and threat patterns stable IDs and record their version. See [supported security context](security-context.md). For project-specific additions, use the README's [checklist](../README.md#adapt-the-checklist) and [abuse-pattern](../README.md#add-project-abuse-patterns) formats.

The installer copies selected skills, not the sibling `context/` directory. Make those context files available separately. A host configuration can explicitly select them; a custom default-loading workflow would be a company change to maintain and test.

## Install the company version

Use the [Skills CLI prerequisites](../README.md#quick-start). From the application project, install from the company checkout:

```bash
npx skills@1.7.2 add /work/company-skills --skill create-threat-model
```

Select the assistant when prompted. Installation is project-local by default; add `-g` for a user-wide installation. To select all skills from the company repository, use `--skill '*'`. An authenticated private Git URL can replace the checkout path; see the [CLI installation documentation](https://github.com/vercel-labs/skills/blob/v1.7.2/README.md#private-repositories).

For manual distribution, copy the complete `skills/create-threat-model/` directory to your assistant's skill location. No custom installer is required. The upstream `make install-dev` target creates a development snapshot and is not needed for this distribution.

Start a fresh assistant session and invoke `create-threat-model` on a fictional project. Check the reported company version, selected context, expected output, and your changed workflow. These are manual checks; successful file installation alone does not establish correct model behavior.

## Merge an upstream update

Start with a clean working tree and all company changes committed. Keep the current company release available for rollback.

Fetch upstream, then set the old SHA from `UPSTREAM.md` and the new reviewed SHA:

```bash
git fetch appsec-upstream
previous_upstream='FULL_PREVIOUS_UPSTREAM_COMMIT_SHA'
next_upstream='FULL_NEXT_UPSTREAM_COMMIT_SHA'
git diff --stat "$previous_upstream" "$next_upstream" -- skills/create-threat-model
```

Review that upstream diff, then apply only its changes to this skill:

```bash
upstream_patch=$(mktemp)
git diff --binary "$previous_upstream" "$next_upstream" -- skills/create-threat-model > "$upstream_patch"
git apply --3way --index "$upstream_patch"
```

Run the apply command only if diff generation succeeded and the patch contains changes. Git uses the fetched base objects to merge the upstream patch with your committed company version. This works even though the company repository has its own history. It preserves compatible local changes and reports conflicts; it does not guarantee a conflict-free update.

If Git reports conflicts, inspect `git status`, resolve them in the affected files, and stage the resolutions. Do not replace the whole directory or use an upstream-only update command to bypass the merge. Check `metadata.version` as well; choose a new company version rather than silently restoring the upstream label.

Review the resulting changes, repeat the fictional-project checks, and update `UPSTREAM.md` with the new base SHA and company release. Commit and distribute the company version again:

```bash
git add skills/create-threat-model UPSTREAM.md
git diff --cached --check
git diff --cached
git commit -m "Merge create-threat-model upstream update"
```

To abandon an uncommitted update, the following restores this skill to your committed company version. It discards edits made during the attempt, so save any resolution work you want to retain first:

```bash
git restore --source=HEAD --staged --worktree -- skills/create-threat-model
```

Also restore any provenance edits before retrying. To roll back a distributed release, reinstall the previous recorded company release, including its matching context version.

The Skills CLI handles installation from your company source. It does not merge public upstream changes into that source. Import and merge commands above are a manual procedure; this repository provides no company import/update script.
