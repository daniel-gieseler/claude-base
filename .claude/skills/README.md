# Agent Skills

Skills extend Claude with specialized capabilities that are automatically invoked when relevant.

## Structure

Each skill is a directory containing a `SKILL.md` file:

```
.claude/skills/
├── code-review/
│   └── SKILL.md
├── git-commits/
│   └── SKILL.md
└── data-analysis/
    └── SKILL.md
```

## SKILL.md Format

```yaml
---
name: skill-name          # lowercase, hyphens only, max 64 chars
description: What the skill does and when to use it.  # max 1024 chars
---

# Skill Name

## Instructions
[Clear, step-by-step guidance for Claude]

## Examples
[Concrete examples of using this skill]
```

## SDK Integration

Skills are auto-discovered when `setting_sources=["project"]` is configured:

```python
options = ClaudeAgentOptions(
    cwd="/path/to/project",
    setting_sources=["user", "project"],  # Load skills from filesystem
    allowed_tools=["Skill", "Read", "Write", "Bash"],  # Enable Skill tool
)
```

## Best Practices

1. **Be concise** - Claude is already smart, only add context it doesn't have
2. **Write descriptions in third person** - "Generates commit messages..." not "I can generate..."
3. **Include trigger context** - Describe both what it does AND when to use it
4. **Keep SKILL.md under 500 lines** - Use progressive disclosure for more
5. **Use consistent terminology** - Pick one term and stick with it

## Progressive Disclosure

For complex skills, split into multiple files:

```
complex-skill/
├── SKILL.md           # Overview (loaded when triggered)
├── REFERENCE.md       # Details (loaded as needed)
└── scripts/
    └── helper.py      # Utility (executed, not loaded into context)
```

Claude reads additional files only when needed, keeping context efficient.
