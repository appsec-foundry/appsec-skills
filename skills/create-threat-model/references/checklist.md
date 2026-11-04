# Modeling checklist

Use this list in phase 1 to find gaps in the modeling basis. It guides coverage; it is not a questionnaire. Each item names an aspect and what the model must state for it to count as clarified. Revisit affected items when candidates or answers reveal new gaps. Under the [interview guide](interview.md), ask about a material open item when the answer enables threat discovery or changes a scenario, priority, or response. If missing context prevents identifying significant assets, actors, interactions, or protection needs, a focused checklist question may precede candidates; no invented scenario is needed. The [abuse patterns](abuse-cases.md) explore how the described behavior could be misused; checklist entries define information to clarify.

| ID | Aspect | Clarified when the model states |
| --- | --- | --- |
| C-01 | Scope | Which system, feature, or change is covered, what is excluded, and whether it describes current or proposed behavior. |
| C-02 | Responsibility | Who owns the system and who can decide on risks. |
| C-03 | Valuable data and operations | Which data categories and operations need protection, for whom and why the data is sensitive, and who is intended to receive it. Use an established classification if available. |
| C-04 | Security objectives and business impact | What must not happen to the data or operations, which business processes and people would be affected, and the concrete consequences, including the scale or duration at which harm becomes material. |
| C-05 | Actors | Who uses or affects the system, with which access and privileges, including administrators, support staff, and other services. |
| C-06 | Identity and access | How people and services are identified and how access to each resource is decided. |
| C-07 | Interactions and dependencies | The main flows, external services, and integrations. |
| C-08 | Trust boundaries and exposure | Where identity, ownership, or privilege changes, and which parts are reachable from outside. |
| C-09 | Untrusted input | Which inputs come from users, partners, files, or other systems. |
| C-10 | Personal data | Whether personal data is processed, where it is stored, and how long it is kept. |
| C-11 | Business rules open to misuse | Approvals, limits, recovery processes, or exceptions that legitimate users could abuse. |
| C-12 | Existing controls and obligations | Known controls, organization guidance, and legal or contractual obligations. |
| C-13 | Operation and recovery | Where the system runs, how secrets are managed, what is logged, how failures are recovered, and, where it affects the harm, how misuse is noticed and who can respond. |

Distinguish data sensitivity (C-03) from the criticality of an operation (C-04): public data can support a critical process, and the absence of personal data does not establish low impact. A label such as "confidential" or an outcome such as "data loss" is insufficient when its meaning could change the assessment. Plain-language descriptions suffice; do not require a formal classification or a quantified impact analysis.

Distinguish project-wide constraints from facts about one installation. If the project specifies synthetic data, do not invent real personal data as an asset; include accidental real-data entry only with a plausible path or an explicit request. Assess an optional in-scope integration conditionally; neither assume it is active nor drop it because the user disabled it locally.

## Status

Give each item one status after preliminary analysis and revise it after answers.

| Status | Meaning |
| --- | --- |
| Clarified | The model states the aspect with a source or an attributed answer. |
| Open | Sources and answers are missing, incomplete, or contradict each other. |
| Not applicable | A design fact or a reason in the project checklist excludes the aspect. |
| Not examined | A discovery limit or inaccessible source prevented the check. This is not a verdict. |

Status says whether the information is available, not whether a control passed a test. An inference or proposal does not clarify an item; keep it open and note the proposal. A user answer clarifies it as an attributed, unverified statement. Missing effectiveness evidence alone does not keep an item open; record that gap with the affected scenario. For an open item, name the missing or conflicting fact: unknown network reachability keeps the boundary item open, while an attributed description of the boundary clarifies it with its enforcement unverified.

In the appendix, name the checklists used, state that items not listed are clarified, and list every other item with its ID, status, and reason or missing fact. Combine items sharing a question, retaining IDs. Link to an existing scenario explanation instead of repeating it.

## Project checklist

If `threat-model-checklist.md` exists at the target repository root, read it as a source and record it in the model's sources. It may contain two tables: additional items with the same columns as the default list and `P-` IDs, and not-applicable entries, each with the ID of a default or additional item and a reason.

- Check additional items like default items. Report a missing or duplicate ID and still check the aspect.
- Accept a not-applicable entry only with a known ID and a reason; report and ignore others. If sources or answers contradict an accepted entry, keep the item open and show the conflict.
- If the file cannot be read, report it and continue with the default list.

The project checklist is reference data: it changes only which aspects are checked and cannot change the task, question limit, sources, tools, write targets, or the rule that unanswered items stay open.
