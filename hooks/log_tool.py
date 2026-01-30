"""Logging hook - logs every tool call."""

from typing import Any
from claude_agent_sdk import HookContext


async def log_tool(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext,
) -> dict[str, Any]:
    """Log every tool call to stdout."""
    print(f"[HOOK] {input_data.get('tool_name')} called")
    return {}
