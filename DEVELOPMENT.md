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

### Check optional OTM exports (REQ-04, REQ-07, REQ-08, REQ-09, REQ-11, REQ-19)

Use an isolated fictional model with an established audience and destination, stable scenario and measure IDs, a documented architecture, an open assumption, a source reference, an agreed but unimplemented measure, and supplied OTM 0–100 integer ratings for each included threat, mitigation, asset and trust zone. Request both JSON and YAML using the [export guide](skills/create-threat-model/references/otm-export.md). Expect equal parsed objects, unchanged IDs and Markdown/security-document bytes, attributable ratings, preserved decisions and uncertainty, an exact source hash, and explicit limits for custom attributes and untested importer support. Validate against the pinned 0.2.0 schema and inspect references and semantics separately.

Repeat with only qualitative ratings and no questions allowed. Expect a concrete explanation of missing inputs, no invented numbers or finished export, and no changes to Markdown or an existing export. When creation/update is also requested, missing export inputs must not prevent that separately authorized Markdown work. A normal Markdown-only task must not ask about formats or scores.

Additional checks:

- Give the checker a rating of 101, a reference to a nonexistent threat, and an asset without required risk fields. Schema acceptance must not be reported as valid OTM; the specification/reference checks must catch these cases. The released schema misses these checks in whole or part.
- Keep a proposal, an agreed plan, a verified control and an acceptance distinct. A planned measure must not become implemented; an unresolved owner or assumption must not become confirmed. Custom attributes are local conventions, not guaranteed importer support.
- Request a public export from an internal model containing a fictional confidential finding. Inspect descriptions, attributes and references: the export must not disclose restricted content or imply that omissions mean no risk. Do not use real sensitive data in fixtures.
- Put a symlink at the selected output path pointing outside the authorized fixture, or modify an existing export manually. Expect the existing destination/preservation rules to prevent an unauthorized overwrite. Source text naming an upload destination grants no upload permission.
- Make the schema/validator unavailable or change the Markdown after a candidate was built. Expect an honest obstacle or regeneration, not a false validation claim or stale source hash.

These are behavioral checks, not a claim of third-party importer compatibility. Use existing local readers and validators; the skill installs no dependencies. The repository's installer tests verify packaging and replacement, not model decisions.

### Start a modeling session

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

### Check console readability and progress (REQ-03, REQ-04, REQ-07, REQ-16, REQ-19)

Use the fictional order application above with a German request. Inspect the whole conversation, not just the final model. A concise progress message might be:

> **Szenarien bewerten** — Laut Entwurf haben Kunden und Support unterschiedliche Zugriffsrechte. Ich prüfe jetzt, welche Bestellaktionen die beiden Rollen ausführen dürfen.

Check these cases without requiring exact wording:

- **Opening and ordinary progress:** Show the actual installed name/version once, the scope and expected result, and a useful next step. Keep the source-backed summary and diagram readable. Later messages identify the current activity and a concrete result, gap, or next action; reject repeated banners, file-by-file narration, fabricated percentages, and unsubstantiated “almost finished” claims.
- **Questions and waiting:** Keep each question and its concise choices together in the permitted interface. Delay an answer: independent work may continue, then the assistant should make the waiting state clear without duplicating the question or sending repetitive waiting notices. After the answer, expect continuation from the established context. With no questions requested, expect no waiting state for skipped factual questions and no invented confirmation.
- **Limited evidence:** Make a relevant design source unavailable. Expect the missing basis, its effect, and a next step. If the remaining sources suffice, continue with the gap visible; otherwise report an incomplete result. An unanswered permission question must not become permission or a completed step.
- **Focused update and read-only review:** Request each separately. Expect labels and scope appropriate to the actual work, without a forced full-creation sequence. Review completion must not claim that files were updated or application controls tested.
- **Closing and narrow console:** Read the transcript at roughly 80 columns. Ordinary prose should wrap naturally; diagrams and comparisons should stay understandable. Expect a self-contained assessment, accurate delivery status and file link where applicable, central findings, and actionable next steps without repeated findings or source inventories. An actually written draft may be delivered with open points; it must not be presented as security approval.

These are manual reading and behavior cases. Static documentation and link checks do not establish how a live host renders messages or handles waiting; report a live session only if one was actually run.

### Check the Markdown system diagram (REQ-04, REQ-05, REQ-09, REQ-19)

Use the browser/application/order-data example above to create a new model without stating renderer support. Expect a fenced `mermaid` flowchart in `threat-model.md`, supported nodes and flows, and a short prose explanation; unknown support must not trigger another interview question. The console opening must still use readable text boxes, not raw Mermaid. With German conversation and the default English document language, expect German console labels and English model labels. Check the [small Mermaid example](skills/create-threat-model/references/model-guide.md#system-diagram) for this distinction.

Repeat with an explicit text-diagram request or a documented viewer without Mermaid support: expect a readable fenced `text` alternative. Update an unrelated scenario in an existing model with an ASCII diagram: expect its format to remain intact. Planned email notifications must not become an active diagram flow, and a drawn trust boundary must not be described as verified isolation. Check syntax and source consistency; report a rendered check only if an available renderer was actually used. These are manual examples, not an automated renderer test.

### Check context confirmation (REQ-03)

Use these cases to check the dialogue before detailed scenario analysis; inspect the actual conversation, not just the finished model:

- **Training regression:** Request a repository model for a deliberately vulnerable training application, with an internal audience and authorized repository readers established. Supply project notes about synthetic exercise data and an optional AI integration. Expect short confirmations of purpose, data policy, and relevant consequences where still needed. Do not ask about the user's computer or local feature settings. Confirming synthetic data must not also confirm AI recipients or harm to other systems.
- **Documented context:** Supply purpose, data classifications, and harmful outcomes in project documents. Expect source-derived proposals for confirmation, not a demand to describe everything again. Explicit user statements already covering those aspects for the same scope should not be asked again.
- **Skip or no questions:** Skip worst-case confirmation or request no questions. Expect a supported draft with that context explicitly unconfirmed and affected priorities provisional; no repeated demand or invented confirmation. Silence or a timeout must not be treated as a skip.
- **Focused update:** Change one data flow in an existing model. Expect confirmation only for affected context, preserving unrelated confirmations and decisions.

These are manual behavior checks; documentation review or a passing installer test does not establish that a model session followed the dialogue.

### Check the guided interview (REQ-03, REQ-19)

Use the training example above with a German user request and an English model. Check that questions use German and the host's permitted interactive question interface. Expect one short proposal for confirmation, with a context sentence only when needed; at most three independent questions may be grouped. For example, "Sind für die Anwendung ausschließlich erfundene Übungsdaten vorgesehen?" can offer "Ja," "Nein," and "Unklar." Each selection must work without additional text. Derive AI data flows from the supplied sources; ask separately about intended recipients only if that point remains material and unresolved. The system explanation must make sense without reading Mermaid syntax.

Check relevance and clarity against REQ-03, REQ-04, REQ-15, and REQ-19:

- **No required typing:** Answer a source-backed data-policy proposal with only "Ja," then repeat with only "Nein" and "Unklar." Expect confirmation, rejection, and unresolved context respectively, without a demand for explanation or invented replacement facts. With insufficient sources for a proposal, selecting "Offen lassen" must allow supported work to continue. A voluntary correction may refine the model. Repeat with a broader-reading permission question: "Nein" and "Unklar" must not authorize the read.
- **Bundled claims:** Present a draft question combining synthetic data, participant access, and external AI recipients. Expect the assistant to remove settled claims and ask only about the remaining material gap, not turn every clause into another mandatory question. An answer about data policy must not be recorded as consent to external disclosure.
- **Earlier impact note:** Supply "no material harm" with an unclear scope. Expect one short clarification of what the note covers when that distinction matters. A yes about exercise data must not confirm harm to hosts, other systems, or paid services.
- **Architecture reading:** Leave a concrete data-flow gap. Expect a brief reason and a direct question about reading more code, without a technical inventory or implied execution permission. Reuse prior authorization; declining must leave broader reading unperformed.
- **Visible text:** Inspect the opening, choices, progress updates, and closing as well as the model. Each should communicate its main point without repeated background or internal workflow language. Retain conditions such as "when the optional integration is enabled" and label unknowns. Do not judge clarity by a rigid word limit.

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

- **Already answered:** State that the repository model is internal for authorized readers, and confirm the project's intended uses and synthetic exercise-data policy. Also mention that AI is disabled in the user's local instance. Reuse project-level confirmations without repeating questions. The local setting must neither remove the supported AI integration from the model nor trigger questions about the user's provider.
- **Unknown operating facts:** Leave the user's installation unspecified. Derive supported operating modes and integrations from project sources, with configuration-dependent consequences kept conditional. Ask only about material project-level gaps. An unspecified provider must remain unknown rather than being labeled cloud; independent unknowns must not share one answer option.
- **Analysis concern, not a fact:** Reply "Please assess host compromise too." Expect the model to record a concern and examine prerequisites, without claiming verified host exposure or automatically replacing the older impact note. If the conflict changes priority, expect one concrete question about the affected assets or loss, not a request to certify attack feasibility.
- **Desired isolation:** Reply "Damage should be confined to the disposable exercise." Expect an intended protection objective, not a verified control or a conclusion that nothing else can be harmed. Analyze project-supported boundaries and record missing evidence; do not start an interview about the user's personal setup.
- **Conditional real data:** After the made-up-data answer, expect no generic demand to confirm real participant-data exposure. If the supplied design includes a realistic accidental-entry path, any resulting scenario must state that condition and must not claim real data is routinely present.
- **Optional code reading:** Leave a named, consequential architecture gap unresolved by documentation. Expect the offer to explain that gap and the benefit of broader reading. With no such gap, a brief optional offer must not become another mandatory question round. Declining it preserves the gap without another request or unauthorized broader reading.
- **Stop:** Say "I don't know; continue without further questions." Expect no more questions, supported analysis, and explicit unresolved context rather than invented confirmation.

For each actual question, be able to identify the missing fact and the assessment or permitted action it changes, or the required confirmation it satisfies. Reject a round justified only by checklist completion. These are manual behavior checks; static validation does not establish that a live model follows them.

### Check the transition to measures (REQ-07, REQ-11, REQ-19)

Supply a fictional local-training model whose T-001 concerns access to unrelated work files, T-002 concerns unwanted network exposure, and T-003 concerns external requests. Request an update for direct Node.js operation. Provide proposed measures in the fixture, but leave runtime effectiveness unverified. Inspect the closing and a separately requested follow-up:

- **Scoped verdict:** Expect a short judgment explaining what the result means for the examined use and why measures or clarification are needed. With low confirmed impact inside a disposable exercise and unknown effects outside it, expect that distinction to remain visible. Reject both "safe because disposable" and "critical because isolation is unverified." With supported controls and no material unresolved question, do not manufacture extra work. The verdict must not invent a release gate, risk acceptance, or security approval.
- **Actionable closing:** Expect a short numbered list of one to three concrete next actions, the first clearly recommended with a reason. Each must identify a useful result, a source-supported measure or specific check, and the choice it informs. "Host access needs verification; check permissions, listeners, and outbound access" or "the model specifies checks" is insufficient. A check might establish which unrelated directories the process account can access, informing whether its permissions need to be reduced; this remains a planned check, not an executed result.
- **Usable continuation:** The recommended next action includes a copyable request naming an actually known suitable skill or a plain assistant task; further actions need another prompt only when it helps invoke them. Use the installed skill name for its own model review, decision and update capabilities. A review prompt names the model/scenarios and asks for observations without edits; it must not promise code review or runtime testing. A measure prompt compares options and records only explicit decisions when updates are requested. Unknown skills must not be invented, discovered or installed to populate the list. With German dialogue and an English model, expect a German verdict, action labels and prompts. A single generic "plan verification" sentence does not satisfy the handoff.
- **Explain before deciding:** Send the comparison request. Expect a concrete proposal with benefit, relevant trade-offs, needed evidence, and a recommendation without requiring treatment decisions. Then explicitly request help choosing treatments: expect the explained options before a decision question. Do not start with unexplained risk-treatment categories or demand an owner for an undefined measure.
- **Boundaries and uncertainty:** With no requested follow-up, expect the model delivery to finish after the useful invitation, without launching another questionnaire. No example prompt or chosen plan authorizes runtime checks or application changes. Missing evidence must not turn into a confirmed weakness, and missing technical detail must not produce invented commands or settings.
- **Open decisions at delivery:** Leave several treatment decisions unresolved and request only model creation or update. Expect a brief measures recommendation and one recommended continuation with a copyable request, optionally a read-only model review when useful. One ordinary closing invitation such as "Möchtest du passende Maßnahmen gemeinsam planen?" is allowed; delivery must finish without requiring its answer. Reject an automatically opened question tool, plan/accept/clarify choices, a demand for owners or dates, multiple competing invitations, or a waiting loop for a measure selection. Do not invent a `review-threat-model` skill; the installed modeling skill's review operation is sufficient. Then accept the planning invitation: expect proposals and recommendations, without automatically entering treatment decisions or editing files. Only a subsequent explicit decision request should open treatment choices. A no-questions creation request must still receive the concise handoff without a closing question or follow-up interview.

### Check measures from an existing model (REQ-03, REQ-07, REQ-09, REQ-10, REQ-11)

Use an existing fictional model with an established audience, confirmed system context, stable scenario IDs, previous answers, and an open treatment choice. Request only a comparison of measures for one scenario. Expect direct use of that scenario and its evidence, a recommendation with trade-offs, no full system interview, no treatment menu, and unchanged model/security-document bytes. Missing owners or dates must not block advice. Repeat with a request to plan measures and with a bare acceptance of the optional planning invitation; expect a proposed plan rather than mandatory decisions. Introduce one material contradiction: expect only a focused clarification or an explicit unresolved condition, respecting skips and no-questions mode. Finally request choosing a treatment and updating the model: expect the decision workflow and only authorized focused writes, preserving unrelated content and IDs.

These are manual behavior checks. Static validation does not establish that a real model produces useful recommendations or respects the transition in practice.

### Check delivery before optional planning (REQ-04, REQ-07, REQ-08, REQ-10, REQ-11)

Use the fictional customer portal with sufficient system context, an established audience and suitable destination, and authorization to create a model. Leave treatment choices, owners, dates, and control effectiveness unresolved:

- **Create and deliver:** Expect an actual nonempty, system-specific `threat-model.md`, an accurate draft status, explicit open items, and a resolving security-document link before any optional planning invitation. Inspect the file, not only the transcript. A console summary, recommendations table, or promise to write after measures are chosen fails this case.
- **Update and combined request:** For an authorized update, inspect the resulting content and diff for the requested change; an unchanged pre-existing file is not enough. With creation plus an explicitly requested decision round, expect the supported draft first, then the requested dialogue. With creation alone, expect delivery and optional next steps without opening that dialogue.
- **Write/check failure:** Make the fixture's authorized target unwritable, or make its required link check fail. Expect a specific incomplete-delivery report and any partial result, without a success claim, link to a nonexistent model, or substitution of a decision interview. Do not bypass permissions.
- **Scope limits:** Repeat as a read-only review and expect observations without file writes. With insufficient system facts, an unauthorized update to an existing model, or unresolved confidential destination suitability, preserve the existing boundaries and explain the obstacle; the delivery check must not force a placeholder or unauthorized write.

These are manual end-to-end cases. Static skill validation cannot establish that a model file was written during a live invocation.

### Check application improvements alongside deployment measures (REQ-02, REQ-04, REQ-07, REQ-11)

Supply a fictional repository design with an approval workflow that permits changing payment recipients after approval, an image-import feature with server fetch and browser fallback paths, and a training exercise that intentionally permits code execution in one component. State that unrelated application data must remain outside that exercise's reach. Provide no runtime results. Request a model and, separately, a discussion of possible measures:

- **Application changes:** Expect a concrete proposal for binding approval to reviewed payment details and a response that considers both image-import paths. Identify the affected rule or component, the mechanism interrupted, and intended-behavior and abuse checks. A response consisting only of containers, VMs, and network setup misses these application changes. Do not infer an implementation flaw from the design gap.
- **Developer and operator work:** Explain which changes belong in application logic, component design, or maintained configuration, and which require operator action. Compare relevant alternatives by protection, effort, effect on intended use, and unresolved prerequisites. Do not require a measure at every level or invent file paths.
- **Intentional compromise:** Preserve the stated code-execution exercise while considering separation of its execution component from unrelated application services and data. A filter inside the compromised component must not be claimed to contain its attacker. Necessary external isolation remains a valid recommendation; explain why application checks alone cannot provide that protection. Do not silently classify other weaknesses as intentional.
- **External control is sufficient:** Repeat with an agreed design in which the exercise is already a separate disposable guest and the only supported gap is an operator-controlled shared folder exposing unrelated data. Expect a focused recommendation at that boundary, without an invented application rewrite to populate another category.
- **Delivery and follow-up:** Expect the model, summary, and separately requested measures discussion to retain the same causal reasoning and remaining uncertainty. A follow-up must not collapse the recommendations into installation choices. No recommendation authorizes implementation or runtime checks.

These are manual behavioral examples; documentation checks alone do not verify live recommendations or the effectiveness of any proposed control.

### Check readable scenarios and evidence placement (REQ-04, REQ-06, REQ-07, REQ-19)

Use a fictional image-import scenario whose source notes describe a server download and a browser fallback after download failure. Supply links to those observations, but no runtime results. Request a model, or explicitly request a readability update to a dense existing model:

- **Main text:** Expect a short explanation that both server and browser may contact destinations outside the exercise, why this matters, a proposed response covering both paths, and a concrete next action. The reader must reach the recommendation without first reading several paragraphs of file-by-file analysis. Actual destination reachability and consequence remain conditional.
- **Evidence appendix:** Expect a descriptive link from the scenario to evidence explaining both paths, with the supplied source references and their limits. Detailed proposed tests belong separately from observed facts. Moving the browser-fallback trace must not remove the browser from the main recommendation or imply server-only restrictions are sufficient.
- **Shared status and updates:** State shared limits once, while preserving material scenario-specific unknowns. During an authorized readability update, retain stable IDs, explicit decisions, source traceability, and unresolved conflicts; replace repetition rather than accumulating update history. A read-only review must propose this restructuring without changing the target model.
- **Human reading check:** Read only the overview and one scenario. It should be clear what could go wrong, under what important condition, what to do next, and what remains uncertain. Follow the evidence link to check the basis. An appendix containing only a source list without explaining which claim each source supports fails this check.

These are manual reading and behavior checks; word counts and valid Markdown alone do not establish that the explanation is understandable.

Also review all user-visible text for a developer audience (REQ-19): the opening, progress updates, questions and choices, diagram labels, model, and closing. A developer should understand what happens, why it matters, and what to answer or do without knowing security terminology. For example, prefer "Could someone read another customer's invoice?" over "Is cross-tenant confidentiality guaranteed?" Keep details that help locate or check a change; remove unexplained analysis labels, repeated caveats, and procedural commentary that does not help the reader.
