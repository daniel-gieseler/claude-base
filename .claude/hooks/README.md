# Hooks

Intercept agent execution at key points.

## Available Events (Python SDK)

| Event | When | Can Block? |
|-------|------|------------|
| `PreToolUse` | Before tool runs | Yes |
| `PostToolUse` | After tool runs | No |
| `UserPromptSubmit` | User sends prompt | No |
| `Stop` | Agent stops | No |
| `SubagentStop` | Subagent completes | No |
| `PreCompact` | Before compaction | No |

## Hook Signature

```python
async def my_hook(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext,
) -> dict[str, Any]:
    # Return {} to allow, or hookSpecificOutput to block/modify
    return {}
```

## Blocking a Tool (PreToolUse only)

```python
return {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Reason shown to Claude",
    }
}
```

## Usage in agent.py

```python
HOOKS = {"PreToolUse": ["log_tool", "block_rm_rf"], "PostToolUse": ["log_tool"]}
hooks = load_hooks(HOOKS)
options = ClaudeAgentOptions(hooks=hooks, ...)
```
