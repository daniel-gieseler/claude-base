# Subagents

Subagents are specialized AI assistants defined as markdown files. Each runs in its own isolated context window with custom system prompts and restricted tool access.

## Creating a Subagent

Create a `.md` file in this folder with YAML frontmatter:

```markdown
---
name: my-agent
description: When Claude should use this agent
tools: Read, Grep, Glob
model: sonnet
---

System prompt defining the agent's role and behavior.
```

## Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (kebab-case) |
| `description` | Yes | When to delegate to this agent |
| `tools` | No | Comma-separated tools (inherits all if omitted) |
| `model` | No | `sonnet`, `opus`, `haiku`, or `inherit` |

## Tool Restrictions

| Use Case | Tools |
|----------|-------|
| Read-only | `Read, Grep, Glob` |
| Full access | (omit field) |
| Code modification | `Read, Edit, Write, Grep, Glob` |
| Exploration | `Read, Grep, Glob, Bash` |

**Note**: Never include `Task` - subagents cannot spawn subagents.

## Invocation

Claude auto-delegates based on `description`. Or request explicitly:

```
"Use the code-reviewer agent to check my changes"
```

## Registration

Agents are auto-discovered from `.claude/agents/*.md` - no manual registration needed.
