"""Utility decorators for simplified tool and agent definitions."""

from functools import wraps
from typing import Callable, Awaitable, get_type_hints
from pydantic import BaseModel, ValidationError
from claude_agent_sdk import tool as sdk_tool, create_sdk_mcp_server, AgentDefinition, HookMatcher


def load_agents(agents_dir: str = ".claude/agents") -> dict[str, AgentDefinition]:
    """Load agent definitions from markdown files in agents directory.
    
    Args:
        agents_dir: Path to agents directory (default: .claude/agents)
        
    Returns:
        Dict mapping agent name to AgentDefinition
    
    Usage:
        agents = load_agents()  # loads from .claude/agents/
    """
    from pathlib import Path
    import yaml
    
    agents = {}
    for md_file in Path(agents_dir).glob("*.md"):
        content = md_file.read_text()
        if not content.startswith("---"):
            continue
        
        # Split frontmatter and body
        _, fm, body = content.split("---", 2)
        meta = yaml.safe_load(fm)
        
        # Parse tools (comma-separated string or list)
        tools = meta.get("tools")
        if isinstance(tools, str):
            tools = [t.strip() for t in tools.split(",")]
        
        agents[meta["name"]] = AgentDefinition(
            description=meta["description"],
            prompt=body.strip(),
            tools=tools,
            model=meta.get("model"),
        )
    return agents


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
