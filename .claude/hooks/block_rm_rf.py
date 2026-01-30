"""Security hook - blocks dangerous rm -rf commands."""

from typing import Any
from claude_agent_sdk import HookContext


async def block_rm_rf(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext,
) -> dict[str, Any]:
    """Block rm -rf / commands."""
    if input_data.get("hook_event_name") != "PreToolUse":
        return {}
    
    command = input_data.get("tool_input", {}).get("command", "")
    if "rm -rf /" in command:
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "Dangerous command blocked",
            }
        }
    return {}
