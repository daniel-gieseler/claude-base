"""Utility decorators for simplified tool and agent definitions."""

from functools import wraps
from typing import Callable, Awaitable, get_type_hints
from pydantic import BaseModel, ValidationError
from claude_agent_sdk import tool as sdk_tool, create_sdk_mcp_server, AgentDefinition, HookMatcher


def load_agents(agent_names: list[str]) -> dict[str, AgentDefinition]:
    """Load agent definitions by name from the agents module.
    
    Args:
        agent_names: List of agent names (e.g., ["code_reviewer", "debugger"])
        
    Returns:
        Dict mapping agent name to AgentDefinition
    
    Usage:
        SUBAGENTS = ["code_reviewer", "debugger", "researcher"]
        agents = load_agents(SUBAGENTS)
    """
    import agents as agents_module
    return {name: getattr(agents_module, name) for name in agent_names}


def load_hooks(config: dict[str, list[str]]) -> dict[str, list[HookMatcher]]:
    """Load hooks by event type and hook names.
    
    Args:
        config: Dict mapping event to hook names, e.g.:
            {"PreToolUse": ["log_tool", "block_rm_rf"], "PostToolUse": ["log_tool"]}
    
    Returns:
        Dict for ClaudeAgentOptions.hooks
    """
    import hooks as hooks_module
    result = {}
    for event, names in config.items():
        callbacks = [getattr(hooks_module, n) for n in names]
        result[event] = [HookMatcher(hooks=callbacks)]
    return result


def create_tools_server(tool_names: list[str]) -> tuple[dict, list[str]]:
    """Create MCP server and allowed_tools list from tool names.
    
    Args:
        tool_names: List of tool names (e.g., ["calculator", "current_time"])
        
    Returns:
        (mcp_servers dict, allowed_tools list)
    
    Usage:
        CUSTOM_TOOLS = ["calculator", "current_time", "random_number"]
        mcp_servers, allowed_tools = create_tools_server(CUSTOM_TOOLS)
    """
    import tools as tools_module
    tool_funcs = [getattr(tools_module, name) for name in tool_names]
    server = create_sdk_mcp_server(name="custom", version="1.0.0", tools=tool_funcs)
    allowed = [f"mcp__custom__{name}" for name in tool_names]
    return {"custom": server}, allowed


def custom_tool(func: Callable[[BaseModel], Awaitable[str]]):
    """Decorator that creates an MCP tool from a simple async function.
    
    Extracts:
    - name: function.__name__
    - description: function.__doc__
    - schema: first param's Pydantic type hint (.model_json_schema())
    
    Provides:
    - Auto-parsing of args dict into Pydantic model
    - Validation error handling
    - Auto-wrapping of string output into MCP format
    """
    hints = get_type_hints(func)
    input_model = list(hints.values())[0]
    
    @wraps(func)
    async def handler(args: dict) -> dict:
        try:
            inp = input_model(**args)
        except ValidationError as e:
            return {"content": [{"type": "text", "text": f"Validation error: {e}"}], "is_error": True}
        
        result = await func(inp)
        return {"content": [{"type": "text", "text": result}]}
    
    return sdk_tool(
        func.__name__,
        func.__doc__ or "",
        input_model.model_json_schema(),
    )(handler)
