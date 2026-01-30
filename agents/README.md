# Subagents

Subagents are specialized AI assistants that handle specific tasks. Each runs in its own isolated context window with custom system prompts, restricted tool access, and independent permissions.

## Benefits

| Benefit | Description |
|---------|-------------|
| **Context isolation** | Keep exploration/analysis out of main conversation |
| **Tool restrictions** | Limit what each subagent can do (read-only, no bash, etc.) |
| **Specialized prompts** | Domain-specific expertise without bloating main prompt |
| **Parallelization** | Run multiple subagents concurrently |
| **Cost control** | Route tasks to faster/cheaper models (haiku for exploration) |

## Creating a Subagent

```python
from claude_agent_sdk import AgentDefinition

my_agent = AgentDefinition(
    description="When Claude should use this agent",
    prompt="""System prompt defining the agent's role and behavior.

Include:
- What the agent specializes in
- How it should approach tasks
- Output format expectations""",
    tools=["Read", "Grep", "Glob"],  # Optional: restrict tool access
    model="sonnet",  # Optional: sonnet, opus, haiku, or inherit
)
```

## Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Yes | Natural language description of when to use this agent |
| `prompt` | Yes | System prompt defining role and behavior |
| `tools` | No | Allowed tools (inherits all if omitted) |
| `model` | No | Model override: `sonnet`, `opus`, `haiku`, `inherit` |

## Tool Restrictions

Common patterns:

| Use Case | Tools | Description |
|----------|-------|-------------|
| Read-only | `Read, Grep, Glob` | Can examine but not modify |
| Full access | (omit field) | Inherits all tools from parent |
| Code modification | `Read, Edit, Write, Grep, Glob` | Can edit without bash |
| Exploration | `Read, Grep, Glob, Bash` | Read + command execution |

**Important**: Subagents cannot spawn subagents. Never include `Task` in a subagent's tools.

## Register Subagent

1. Export in `agents/__init__.py`
2. Add name to `SUBAGENTS` list in agent.py

## Invocation

Claude automatically delegates based on the `description` field. You can also request explicitly:

```
"Use the code_reviewer agent to check my changes"
"Have the researcher explore how authentication works"
```

## Built-in Subagents

The SDK includes built-in subagents (Explore, Plan, general-purpose) that Claude can use automatically when `Task` is in `allowed_tools`.
