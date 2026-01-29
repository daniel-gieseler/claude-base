"""Utility decorators for simplified tool definitions."""

from functools import wraps
from typing import Callable, Awaitable, get_type_hints
from pydantic import BaseModel, ValidationError
from claude_agent_sdk import tool as sdk_tool, create_sdk_mcp_server


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
