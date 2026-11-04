# Threat Model — Broken Example

## Overview

This example breaks several rules on purpose. The portal is used by customers and case workers to handle applications. The portal is used by customers and case workers to handle applications.

| Scenario | Priority | First proposed action |
| --- | --- | --- |
| [T-001](#t-001-document-changes-after-review) | High | Reopen the review |
| [T-009](#t-009-missing) | High | Does not exist |

## System and protection needs

Customers submit applications. Case workers approve them.

## Threat scenarios

### T-001 Document changes after review

**Attack and harm.** A customer replaces a document after review. The ownership check has been verified.

[Evidence and verification for T-001](#evidence-and-verification-for-t-001)

### T-001 Duplicate identifier

**Attack and harm.** This heading reuses an identifier.

[Evidence and verification for T-001](#evidence-and-verification-for-t-001)

### T-002 Scenario without evidence link

**Attack and harm.** A customer reads another customer's documents.

## Open decisions

None.

## Appendix: evidence and verification

### Evidence and verification for T-001

`PROJECT.md` allows replacement until approval.

| Item | Status | Missing fact |
| --- | --- | --- |
| C-03 Valuable data | Document categories unknown | |
