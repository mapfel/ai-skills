# Homelab

## Considerations

For your Homelab project, I would use a two-layer documentation approach:

1. AGENTS.md — AI-oriented project context: architecture, constraints, decisions, conventions, current state, and unresolved questions.
2. Home Operation Manual — Human-oriented documentation: system architecture, configuration, maintenance procedures, troubleshooting, and operational instructions.

This offers an important benefit: the Home Operation Manual becomes the authoritative knowledge base, while AGENTS.md acts as the AI-facing entry point.

For example, instead of duplicating your Sophos XG VLAN configuration inside AGENTS.md, you could simply reference docs/architecture/network.md. Similarly, an established constraint such as keeping your existing Zigbee2MQTT installation unchanged should be visible in AGENTS.md, while its technical details belong in the services documentation.

**Additional recommendations:**

1. Maintain an explicit distinction between knowledge and instructions. AGENTS.md is not merely a place to store facts; it can also tell AI assistants how to work with your Homelab. Your manual, by contrast, should remain useful without an AI assistant.

2. Support incremental knowledge integration. After the initial extraction, a future prompt should be able to take another conversation and update existing Markdown files rather than replacing them. It should compare new findings against established information, detect contradictions, propose changes, and preserve unrelated content. I would strongly recommend making this your second reusable prompt.

3. Make the extraction auditable. For particularly long or important conversations, consider adding source references such as Source: Conversation about Sophos PKI, November 2026 and recording when information was last confirmed. This is especially useful for configurations and decisions that may change over time.

**Overall recommendation:**

- Establish a workflow of Conversation → Knowledge Extraction → Documentation Update → Git Commit.  
  Over time, your Git repository becomes the persistent, version-controlled source of truth for both your Home Operation Manual and future AI conversations.

## Structure

```text
homelab/
├── AGENTS.md              # AI context and instructions
├── README.md              # Human entry point
└── docs/
    ├── architecture/      # Topology, networks, service dependencies
    ├── infrastructure/    # Devices, hypervisors, storage
    ├── services/          # MQTT, Zigbee2MQTT, HomeMatic, etc.
    ├── operations/        # Runbooks, maintenance, troubleshooting
    ├── decisions/         # Architecture Decision Records (ADRs)
    └── projects/          # Planned and ongoing improvements
```
