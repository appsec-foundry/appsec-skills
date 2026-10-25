# Developing Create Threat Model

These instructions require a clone of the full AppSec Skills repository. The Makefile and scripts are not included in an installed skill directory. Run the commands below from the repository root.

Follow [AGENTS.md](AGENTS.md) and the [skill requirements](skills/create-threat-model/requirements.md) when making changes. For installation and everyday use, see the [user guide](skills/create-threat-model/README.md).

## Load a development version into Codex or Claude Code

From the root of this checkout, install or update your current working version:

```bash
make install-dev          # Codex and Claude Code
make install-dev-codex    # Codex only
make install-dev-claude   # Claude Code only
```

This requires Make and Python 3 and installs a snapshot named **create-threat-model-dev** under `~/.agents/skills/` for Codex or `~/.claude/skills/` for Claude Code. The regular `create-threat-model` installation remains intact. Without Make, run `python3 scripts/install-dev-skill.py both` (or select `codex` or `claude`). To install only for one project, use `python3 scripts/install-dev-skill.py both --project /path/to/project`.

In a fresh session in your target project, invoke:

```text
Codex:       $create-threat-model-dev
Claude Code: /create-threat-model-dev
```

Then describe the modeling task as usual. The opening displays the dev name and a version containing a fingerprint of the local source files (REQ-16). **After editing the source skill, rerun the same installation command** to refresh the snapshot; uncommitted changes are included. Make edits in this checkout, not the installed copy. The installer preserves unrelated installations and refuses to replace a dev copy with local edits or an unmanaged folder. It installs no packages and starts no model session. These paths apply to local Codex and Claude Code, not Claude web chat or Cowork.

Anyone with a local checkout can use these targets; paths are resolved from that checkout and the current user's home directory. Run `make help` to list targets and `make test` for the local installer and test-starter checks without model calls.

See the official [Codex local skill documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) and [Claude Code skill documentation](https://code.claude.com/docs/en/skills#choose-where-skills-load).

## Optional: try a fictional project

From the root of this repository, run:

```bash
bash scripts/test-threat-model.sh
```

The starter creates a fresh temporary project, copies the current skill into it, adds a fictional customer-portal description, and opens an interactive Codex CLI session with the prompt already supplied. It requires Bash and an installed, configured Codex CLI; it uses your existing login and configuration. Each run copies your latest local changes. Results remain in the printed test directory; move them elsewhere if you need to keep them beyond temporary-directory cleanup.

To use the app instead of the CLI, run `bash scripts/test-threat-model.sh --prepare-only`, open the printed folder, and send the text from `PROMPT.txt` in a fresh conversation.

The example deliberately leaves audience, data sensitivity, and business impact unspecified. Check that the early dialogue clarifies these within the three-question limit (REQ-03, REQ-05–07, REQ-11, REQ-14), and that your answers inform the scenarios and priorities. In a fresh run, skip an answer or add "Do not ask questions" to the prompt and check that the uncertainty stays visible (REQ-04). This is a manual behavior test; the starter does not automatically evaluate the resulting model.

### Check the opening system summary (REQ-04, REQ-05, REQ-19)

Provide a fictional project overview stating that customers use a web app to view their orders, the app loads orders from a database, and email notifications are planned but not implemented. Leave the login method unspecified and make the request in German. Before the interview, expect a short German summary and a sketch readable in an ordinary console, for example:

```text
Kunden sehen ihre Bestellungen in einer Web-App.

┌─────────────┐     ┌─────────────┐     ┌─────────────────┐
│ Kunde       │────>│ Web-App     │────>│ Bestelldaten    │
│ im Browser  │     │             │     │ in Datenbank    │
└─────────────┘     └─────────────┘     └─────────────────┘

E-Mail-Benachrichtigungen sind geplant, aber noch nicht umgesetzt.
Noch offen: Die Anmeldung der Kunden ist nicht beschrieben.
Grundlage: Projektbeschreibung.
```

The unresolved audience still comes first in the interview. Accept other concise wording and layouts that convey the same source-supported state. Check box and arrow alignment in monospace, readable width, familiar labels, and a clear separation between purpose, diagram, and unknowns. When a source describes a supported optional external connection, expect a separate branch labeled optional, without implying it is enabled. Do not turn a planned feature into a supported optional connection: the assistant must neither draw the unimplemented email delivery as an existing flow nor invent a login mechanism. With only a feature idea and no implemented system, expect an explicitly planned design instead of an alleged current state. With insufficient context for a flow, expect known facts and the gap without an invented sketch. A no-questions request keeps the summary but starts no interview. These are manual behavior cases, not an automated model-session test.

### Check context confirmation (REQ-03)

Use these cases to check the dialogue before detailed scenario analysis; inspect the actual conversation, not just the finished model:

- **Training regression:** Request a new internal model for a local training application. Answer the deployment question with "isolated local training with synthetic data" and permit confidential findings for authorized repository readers. Expect a further short round proposing the supported training purpose, clarifying the sensitivity and recipients of any other relevant data, and asking which plausible worst-case consequences matter. Host compromise or lost training time may be proposals, not confirmed business impact. The two initial answers alone must not end clarification.
- **Documented context:** Supply purpose, data classifications, and harmful outcomes in project documents. Expect source-derived proposals for confirmation, not a demand to describe everything again. Explicit user statements already covering those aspects for the same scope should not be asked again.
- **Skip or no questions:** Skip worst-case confirmation or request no questions. Expect a supported draft with that context explicitly unconfirmed and affected priorities provisional; no repeated demand or invented confirmation. Silence or a timeout must not be treated as a skip.
- **Focused update:** Change one data flow in an existing model. Expect confirmation only for affected context, preserving unrelated confirmations and decisions.

These are manual behavior checks; documentation review or a passing installer test does not establish that a model session followed the dialogue.

### Check the guided interview (REQ-03, REQ-19)

Use the training example above with a German user request and an English model. Check that questions use German and the host's interactive question interface when it is available and permitted. Expect one question at a time by default; at most three short, independent questions may be grouped. For example, "Verwendest du nur erfundene Übungsdaten oder auch echte Daten?" can offer "Nur erfundene Daten," "Auch echte Daten," and "Weiß ich noch nicht." Whether an AI provider receives data needs a separate question if it remains relevant and unresolved. The system explanation must make sense without reading Mermaid syntax.

Repeat with no permitted interactive question tool: expect the same understandable interview in chat, without trying a prohibited tool or changing the host's mode. Answer "Weiß ich noch nicht" or skip a question: expect that point to stay unresolved, without an invented confirmation or the same question being asked again. With an asynchronous tool, no submitted answer must leave required confirmation pending; a preselected choice or elapsed time is not a reply. A request for no questions must still bypass the interview and preserve open context. These cases require a real host session to verify tool selection and waiting behavior.

### Check the audience question (REQ-03, REQ-11, REQ-19)

- **Audience missing:** Request a model for a local training application with made-up data, without naming the document's readers. Expect the first interview question to offer internal, public, and undecided; the deployment and data description must not silently select internal.
- **Audience inherited:** Request an update to a model with an established public audience. Expect a short statement that the existing public audience is being retained, without a redundant question.
- **Provisional audience:** Request an update or review of a model marked internal only as an unresolved fallback, with no prior skip or no-questions instruction in the current task. Expect the audience question first. The provisional heading alone must not count as an answer.
- **Skipped or undecided:** Skip the audience question or choose undecided. Expect the audience to remain unresolved and affected confidential details to remain omitted. Do not repeat the question during that task or treat the fallback as permission to disclose. An explicit no-questions request must still be honored.

### Check waiting and resumption (REQ-03, REQ-09, REQ-10, REQ-11)

Start with a fictional existing `threat-model.md` and its security-document link. Use a host with an asynchronous question tool and supported waiting, then inspect the conversation through the submitted answer:

- **Explicit update or review:** Request a focused update, or separately a read-only review. Expect the requested operation to proceed without a redundant update/review menu just because the model exists. A review must remain read-only.
- **Creation with an existing model:** Request creation without authorizing replacement or update. Expect one clarification offering a focused update, with the existing model preserved while unanswered. Delay the reply beyond a tool return or wait timeout. Expect the question to remain pending, no dependent write, and no final "No files changed; please choose" report. Independent reads may finish, but must not become filler activity.
- **Answer and continue:** Select an update and provide the change to assess. Expect the assistant to resume from that answer, preserve the existing scope unless changed explicitly, and complete the authorized update and checks. It must not stop at acknowledging the selection or ask the operation question again. Selecting review instead must lead to review observations without writes.
- **No authorization supplied:** Skip the operation choice or stop the task. Expect no inferred update permission and no overwrite of the existing model or link. A factual confirmation skipped during an already authorized update follows the supported-draft rules instead; do not confuse these cases.
- **Chat-only host:** With no supported interactive waiting, expect a concise question and a normal turn yielded for the reply. On the reply, expect continuation rather than a claimed completed task or a fresh interview. Do not fail this case merely because the chat turn ended.

These cases need a real host session to verify answer delivery and waiting behavior. Static skill validation cannot prove that an interactive question stays live.

### Check question necessity and answer interpretation (REQ-03, REQ-04, REQ-07, REQ-14, REQ-15, REQ-19)

Use a fictional training application with an optional AI integration and an older note saying an exercise compromise has no material impact. Inspect the conversation as well as the resulting model:

- **Already answered:** State that the model is internal for authorized repository readers, the instance is reachable only from the local computer, all exercise data is made-up and intended for participants, and AI is disabled. Expect those answers to be reused. There should be no repeat audience, reachability, provider-location, exercise-data, or recipient question without a concrete new gap or conflict. A missing question is correct when its information is already established.
- **Unknown operating facts:** Leave deployment and integration enablement unspecified. Expect relevant missing facts to be resolved before proposing host or provider consequences that depend on them. Once AI is disabled, provider location drops out of the pending interview. If AI is enabled but its provider is undecided, record that as unknown rather than cloud. Independent unknowns must not share one answer option.
- **Analysis concern, not a fact:** Reply "Please assess host compromise too." Expect the model to record a concern and examine prerequisites, without claiming verified host exposure or automatically replacing the older impact note. If the conflict changes priority, expect one concrete question about the affected assets or loss, not a request to certify attack feasibility.
- **Desired isolation:** Reply "Damage should be confined to the disposable exercise." Expect an intended protection objective, not a verified control or a conclusion that nothing else can be harmed. If the actual setup is unknown and material, clarify that fact separately; otherwise record the limit of the evidence.
- **Conditional real data:** After the made-up-data answer, expect no generic demand to confirm real participant-data exposure. If the supplied design includes a realistic accidental-entry path, any resulting scenario must state that condition and must not claim real data is routinely present.
- **Optional code reading:** Leave a named, consequential architecture gap unresolved by documentation. Expect the offer to explain that gap and the benefit of broader reading. With no such gap, a brief optional offer must not become another mandatory question round. Declining it preserves the gap without another request or unauthorized broader reading.
- **Stop:** Say "I don't know; continue without further questions." Expect no more questions, supported analysis, and explicit unresolved context rather than invented confirmation.

For each actual question, be able to identify the missing fact and the assessment or permitted action it changes, or the required confirmation it satisfies. Reject a round justified only by checklist completion. These are manual behavior checks; static validation does not establish that a live model follows them.

### Check the transition to measures (REQ-07, REQ-11, REQ-19)

Supply a fictional local-training model whose T-001 concerns access to unrelated work files, T-002 concerns unwanted network exposure, and T-003 concerns external requests. Request an update for direct Node.js operation. Provide proposed measures in the fixture, but leave runtime effectiveness unverified. Inspect the closing and a separately requested follow-up:

- **Actionable closing:** Expect the key harms and a recommended starting point, with a short reason for its priority. Each next step should identify a source-supported measure or a specific check and the decision it informs. "Host access needs verification; check permissions, listeners, and outbound access" is insufficient. A check might establish which unrelated directories the process account can access, informing whether its permissions need to be reduced; this must remain a planned check, not an executed result.
- **Usable continuation:** Expect a copyable request in the user's language to work through measures for the actual relevant IDs, compare meaningful alternatives, and record only explicit decisions if an update is requested. A bare instruction to "decide treatments" is insufficient. Routine source-link or ID checks must not displace the recommended actions.
- **Explain before deciding:** Send that continuation request. Expect a concrete proposal with benefit, relevant trade-offs, and needed evidence before a decision question. Do not start with unexplained risk-treatment categories or demand an owner for an undefined measure.
- **Boundaries and uncertainty:** With no requested follow-up, expect the model delivery to finish after the useful invitation, without launching another questionnaire. No example prompt or chosen plan authorizes runtime checks or application changes. Missing evidence must not turn into a confirmed weakness, and missing technical detail must not produce invented commands or settings.

These are manual behavior checks. Static validation does not establish that a real model produces useful recommendations or respects the transition in practice.

### Check readable scenarios and evidence placement (REQ-04, REQ-06, REQ-07, REQ-19)

Use a fictional image-import scenario whose source notes describe a server download and a browser fallback after download failure. Supply links to those observations, but no runtime results. Request a model, or explicitly request a readability update to a dense existing model:

- **Main text:** Expect a short explanation that both server and browser may contact destinations outside the exercise, why this matters, a proposed response covering both paths, and a concrete next action. The reader must reach the recommendation without first reading several paragraphs of file-by-file analysis. Actual destination reachability and consequence remain conditional.
- **Evidence appendix:** Expect a descriptive link from the scenario to evidence explaining both paths, with the supplied source references and their limits. Detailed proposed tests belong separately from observed facts. Moving the browser-fallback trace must not remove the browser from the main recommendation or imply server-only restrictions are sufficient.
- **Shared status and updates:** State shared limits once, while preserving material scenario-specific unknowns. During an authorized readability update, retain stable IDs, explicit decisions, source traceability, and unresolved conflicts; replace repetition rather than accumulating update history. A read-only review must propose this restructuring without changing the target model.
- **Human reading check:** Read only the overview and one scenario. It should be clear what could go wrong, under what important condition, what to do next, and what remains uncertain. Follow the evidence link to check the basis. An appendix containing only a source list without explaining which claim each source supports fails this check.

These are manual reading and behavior checks; word counts and valid Markdown alone do not establish that the explanation is understandable.

Also review all user-visible text for a developer audience (REQ-19): the opening, progress updates, questions and choices, diagram labels, model, and closing. A developer should understand what happens, why it matters, and what to answer or do without knowing security terminology. For example, prefer "Could someone read another customer's invoice?" over "Is cross-tenant confidentiality guaranteed?" Keep details that help locate or check a change; remove unexplained analysis labels, repeated caveats, and procedural commentary that does not help the reader.
