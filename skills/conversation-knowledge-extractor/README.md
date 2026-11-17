# Conversation Knowledge Extractor

Long AI conversations often contain valuable technical information, architectural decisions, recommendations, and operational knowledge that would otherwise remain buried in chat history.

The **Conversation Knowledge Extractor** transforms these discussions into maintainable documentation.

Its intended capabilities include:

- Extracting facts, decisions, recommendations, and unresolved questions.
- Distinguishing confirmed information from assumptions and proposals.
- Producing structured Markdown documentation.
- Creating AI project context files such as `AGENTS.md`.
- Generating architecture decision records (ADRs) where appropriate.
- Integrating new knowledge into existing documentation.
- Identifying inconsistencies, missing information, and outdated assumptions.

The skill is designed to support both AI-oriented project context and human-readable knowledge bases, including technical documentation and operational manuals.

## Operating Modes

The Conversation Knowledge Extractor supports four operating modes that cover different stages of the knowledge management lifecycle.

| Mode        | Purpose                                        | Output                                               |
|-------------|------------------------------------------------|------------------------------------------------------|
| `extract`   | Preserve knowledge from a conversation         | Structured Markdown knowledge export                 |
| `bootstrap` | Initialize a new documentation project         | `AGENTS.md`, documentation structure, detailed files |
| `merge`     | Incorporate knowledge into an existing project | Proposed changes to existing files                   |
| `audit`     | Check consistency and missing information      | Contradictions, outdated facts, knowledge gaps       |

**Default mode:** `extract`

The modes can be used independently or combined into a workflow:

1. **Extract** knowledge from an AI conversation.
2. **Bootstrap** a documentation repository if none exists.
3. **Merge** newly extracted knowledge into existing documentation.
4. **Audit** documentation for inconsistencies and missing information.

**Example Usage:**

- **Extract knowledge from the current conversation:**

  > Use the conversation-knowledge-extractor skill in extract mode
  > to preserve the technical knowledge from this conversation.

- **Initialize a new knowledge base:**

  > Use the conversation-knowledge-extractor skill in bootstrap mode
  > to create a documentation structure for my Homelab project.

- **Update existing documentation:**

  > Use the conversation-knowledge-extractor skill in merge mode
  > to integrate the extracted knowledge into my existing documentation.

- **Audit existing documentation:**

  > Use the conversation-knowledge-extractor skill in audit mode
  > to identify inconsistencies, outdated information, and knowledge gaps.


## Outlook

In the longer term, additional artifacts may become available:

```text
ai-skills/
├── README.md
├── .gitignore
├── skills/
│   └── conversation-knowledge-extractor/
│       ├── SKILL.md
│       ├── references/
│       │   ├── knowledge-classification.md
│       │   └── documentation-strategy.md
│       └── assets/
│           ├── agents-template.md
│           └── adr-template.md
└── docs/
    └── installation.md
```
