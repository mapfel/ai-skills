# Conversation Knowledge Extraction & Documentation

You are acting as a **Senior Systems Architect, Technical Writer, and Knowledge Management Specialist**.

We have had an extensive technical conversation containing valuable information about my existing environment, architectural decisions, recommendations, planned improvements, troubleshooting experiences, and operational procedures.

Your task is to **consolidate the knowledge from this entire conversation into structured, reusable, maintainable documentation**.

The output will serve two purposes:

1. Provide persistent context for future AI-assisted conversations and projects (e.g., through an `AGENTS.md` file).
2. Contribute to my **Home Operation Manual**, which documents my Homelab, home network, infrastructure, services, and recurring administrative procedures.

## 1. Knowledge extraction

Review the entire conversation, including my messages, your responses, corrections, and subsequent decisions.

Extract all relevant information, including:

- Existing infrastructure, hardware, software, versions, and configurations.
- Network topology, VLANs, IP addressing, routing, firewall rules, and service dependencies.
- Architectural principles, conventions, and design preferences.
- Technical constraints, compatibility requirements, and known limitations.
- Decisions already made, including their rationale.
- Proposed improvements and future enhancements.
- Recommendations you made, including important alternatives and trade-offs.
- Known problems, troubleshooting experiences, and their solutions.
- Operational procedures, maintenance activities, and recovery requirements.
- Open questions, pending decisions, and unresolved technical issues.

**Prioritize preservation of technical knowledge over brevity.** Do not discard useful technical details merely to produce a shorter summary.

However, remove conversational redundancy, small talk, obsolete intermediate reasoning, and repeated explanations.

## 2. Classify information by confidence and status

Critically distinguish between:

- **Confirmed Current State:** Information I explicitly provided about the existing environment.
- **Confirmed Decisions:** Choices I explicitly made or accepted.
- **Planned Changes:** Enhancements I explicitly intend to implement.
- **Recommendations:** Your suggestions that have not yet been accepted.
- **Assumptions:** Information inferred but not explicitly confirmed.
- **Open Questions:** Topics requiring clarification or decisions.
- **Historical Information:** Previous configurations, failed approaches, or superseded decisions that remain relevant.

Never present a recommendation, assumption, or proposed configuration as an already implemented solution.

If later messages correct earlier information, use the latest confirmed information while preserving relevant historical context.

If contradictory statements cannot be reconciled, explicitly document the conflict.

## 3. Generate AI project context

Create an `AGENTS.md` file suitable for use with AI coding assistants and future ChatGPT projects.

It should provide a structured but relatively concise description of:

- Project purpose and scope.
- Environment overview.
- Important infrastructure components.
- Existing architecture and integration relationships.
- Confirmed design decisions.
- Non-negotiable constraints.
- User preferences and technical conventions.
- Known operational risks.
- Planned improvements.
- Open architectural questions.
- References to detailed documentation.

Include instructions for future AI assistants:

- Respect confirmed architectural decisions and constraints.
- Distinguish existing implementations from proposals.
- Do not invent configuration values or undocumented infrastructure.
- Ask for clarification when critical information is missing.
- Prefer solutions compatible with the documented environment.
- Explicitly identify when a recommendation would conflict with an existing decision.
- Preserve important technical decisions when updating documentation.

Optimize this document for **efficient AI context consumption**, not for maximum length.

Avoid duplicating detailed operational procedures that belong in the Home Operation Manual.

## 4. Generate Home Operation Manual content

Create one or more Markdown documents containing the detailed technical knowledge extracted from this conversation.

Use a structure appropriate for a long-lived, Git-managed knowledge base.

Depending on the conversation, include sections such as:

- System overview and purpose.
- Current architecture.
- Hardware and software inventory.
- Network and service topology.
- Configuration details.
- Dependencies and integration points.
- Architecture decisions and rationale.
- Installation and configuration procedures.
- Routine operation and maintenance.
- Troubleshooting and recovery.
- Security considerations.
- Planned enhancements.
- Known limitations.
- Outstanding tasks.

Write for a technically competent reader, but make operational procedures sufficiently explicit that another household member can follow them where appropriate.

For procedures, include prerequisites, ordered steps, verification criteria, and rollback or recovery instructions whenever the conversation contains sufficient information.

Do not fabricate missing procedure steps or configuration details.

## 5. Document architecture decisions

Where meaningful architectural decisions appear, capture them in a lightweight Architecture Decision Record (ADR) format:

- Context
- Decision
- Rationale
- Alternatives considered
- Consequences
- Status

Only classify a decision as accepted if I actually confirmed it.

Do not create unnecessary ADRs for trivial configuration details.

## 6. Organize and avoid duplication

Prefer a **single source of truth** for every technical fact.

Use `AGENTS.md` as the AI entry point and the Home Operation Manual as the detailed reference.

Cross-reference documents using relative Markdown links.

If one document can serve both purposes without significant disadvantages, explain why and use one document.

Otherwise, prefer separate documents with clear responsibilities.

Do not duplicate detailed configurations across multiple files unless there is a compelling reason.

## 7. Security and privacy

Do not export passwords, private keys, access tokens, API secrets, session cookies, or other authentication material.

Replace secret values with references to their secure storage locations when those locations are known.

Preserve technical information such as IP addresses, hostnames, VLAN identifiers, and service endpoints when relevant, but clearly identify documentation intended to remain private.

## 8. Output requirements

Produce the following:

**A. Knowledge inventory**

A concise overview of the extracted knowledge, organized by topic, including important decisions and unresolved questions.

**B. Proposed documentation structure**

A directory tree showing the recommended Markdown files and their responsibilities.

**C. Complete Markdown documents**

Generate the actual contents of `AGENTS.md` and all proposed Home Operation Manual files.

Use meaningful headings, tables, configuration snippets, and relative links where appropriate.

Do not merely describe what these files should contain. Produce their complete content based on the available conversation.

If file generation is available, provide the files for download. Otherwise, place each file in a separate Markdown code block with its intended path.

**D. Knowledge gaps and inconsistencies**

Identify information that is missing, ambiguous, contradictory, or likely outdated.

Distinguish critical gaps from optional improvements.

**E. Suggested next actions**

Provide a short, prioritized list of actions to improve the completeness, accuracy, and maintainability of the documentation.

## 9. Quality requirements

- Be technically precise.
- Preserve relevant details and reasoning.
- Avoid unsupported assumptions.
- Distinguish facts from suggestions.
- Avoid unnecessary duplication.
- Use consistent terminology.
- Produce clean, Git-friendly Markdown.
- Use relative links between documents.
- Prefer maintainable structure over conversational narration.
- Include commands and configuration examples only when supported by the conversation.
- Do not silently omit important information because it does not fit the initially proposed structure.

**Important:** Do not introduce new architectural recommendations unless they are explicitly marked as new suggestions. Your primary task is to preserve and organize the knowledge already established in this conversation.

If the conversation is too extensive to review completely, disclose the limitation and identify which parts could not be examined. Never claim completeness without sufficient access.

Proceed with the extraction and documentation now. Do not ask preliminary questions unless an essential ambiguity makes the task impossible.
