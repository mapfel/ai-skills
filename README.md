# AI Skills

A collection of reusable, provider-independent AI agent skills designed to turn recurring tasks and complex workflows into structured, reliable, and repeatable processes.

The goal of this repository is to develop, maintain, and share practical skills that can be used across different AI assistants, including **ChatGPT, Claude, and compatible AI coding agents**.

## Philosophy

AI assistants are powerful general-purpose tools, but recurring tasks often benefit from explicit instructions, consistent workflows, and clearly defined outcomes.

This repository follows a few guiding principles:

- **Provider-independent** — Maintain skills in a portable format rather than tying them to a particular AI platform.
- **Reusable** — Design skills to work across different projects and contexts.
- **Modular** — Keep each skill self-contained, with its own instructions and supporting resources.
- **Maintainable** — Treat skills as version-controlled artifacts that can be reviewed, tested, and improved.
- **Transparent** — Favor explicit instructions, clear assumptions, and verifiable results.
- **Practical** — Focus on real-world tasks and workflows rather than experimental demonstrations.

## Available Skills

| Skill                                                                        | Description                                                                                                 | Status |
|------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|:------:|
| [Conversation Knowledge Extractor](skills/conversation-knowledge-extractor/) | Extracts and consolidates valuable knowledge from AI conversations into structured, reusable documentation. |  WIP   |


### Conversation Knowledge Extractor

Transforms valuable information from AI conversations into structured, reusable, and maintainable documentation.

Supports four operating modes:

- `extract` — Preserve conversation knowledge.
- `bootstrap` — Initialize documentation projects.
- `merge` — Integrate knowledge into existing documentation.
- `audit` — Identify inconsistencies and knowledge gaps.

See the [skill documentation](skills/conversation-knowledge-extractor/README.md)
for detailed usage instructions and examples.


## Repository Structure

```text
ai-skills/
├── README.md
├── LICENSE
└── skills/
    └── conversation-knowledge-extractor/
        ├── SKILL.md
        ├── references/
        └── assets/
```

Each skill resides in its own directory and contains a `SKILL.md` file describing its purpose, usage conditions, instructions, and expected behavior.

Additional resources, such as reference documents, templates, or scripts, may be included when useful.

## Compatibility

Skills follow the open [Agent Skills specification](https://agentskills.io/), using Markdown files with YAML frontmatter.

The intention is to maintain **one canonical definition per skill**, regardless of which AI assistant executes it.

The repository targets AI environments such as:

- **Claude Code and Claude.ai**
- **OpenAI Codex and supported ChatGPT environments**
- **Other agents supporting the Agent Skills format**

Actual support, installation procedures, and capabilities depend on the respective platform.

Skills may require adaptations or manual invocation in environments without native Agent Skills support.

## Installation and Usage

Clone the repository:

```bash
git clone https://github.com/mapfel/ai-skills.git
```

Each skill can then be installed or referenced according to the instructions of the target AI environment.

For agents supporting the Agent Skills specification, the skill directory typically serves as the unit of installation.

For environments without native support, the instructions in `SKILL.md` may be used as a conventional prompt.

Refer to the documentation of your AI assistant for supported installation locations and activation mechanisms.

## Development Guidelines

Skills in this repository should follow a consistent design philosophy.

- **1. Separate generic workflows from project-specific knowledge.**

  A skill defines *how* a task should be performed. Project-specific context, configurations, and constraints should remain in the respective project repository.

- **2. Prefer explicit, verifiable behavior.**

  Skills should clearly distinguish established facts from assumptions, recommendations, and incomplete information.

- **3. Preserve existing work.**

  Whenever a skill updates documents or other artifacts, it should respect existing structure, terminology, and decisions. Destructive changes should not be made silently.

- **4. Keep instructions focused.**

  Avoid unnecessary complexity and duplication. Use supporting reference files when a skill grows beyond a manageable size.

- **5. Design for portability.**

  Avoid provider-specific features unless they are necessary. Document any platform-specific dependencies or limitations.

- **6. Validate with realistic scenarios.**

  Skills should be tested against representative tasks, including edge cases, incomplete information, and contradictory inputs.

## Contributing

Suggestions, bug reports, improvements, and contributions are welcome.

When proposing changes, please aim to preserve the repository's guiding principles: portability, clarity, maintainability, and practical usefulness.

For new skills, include a clear description of their purpose, usage conditions, expected outputs, and any external dependencies.

## License

This project is licensed under the [MIT License](LICENSE).

You are free to use, modify, and redistribute the skills, including for commercial purposes, subject to the license terms.

## Disclaimer

These skills provide instructions for AI assistants. Their execution and results depend on the capabilities, available context, permissions, and behavior of the underlying AI system.

Skills do not guarantee complete or correct results. Generated content and proposed changes should be reviewed, particularly when they involve security-sensitive configurations, infrastructure, or operational procedures.
