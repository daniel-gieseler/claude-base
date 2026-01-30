"""Agent using modular tools, skills, and subagents."""

import anyio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from utils import create_tools_server, load_agents, load_hooks


# === Configuration ===
BUILTIN_TOOLS = ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Skill", "Task"]
CUSTOM_TOOLS = ["calculator", "current_time", "random_number", "create_order"]
SUBAGENTS = ["code_reviewer", "debugger", "researcher"]
HOOKS = {"PreToolUse": ["log_tool", "block_rm_rf"], "PostToolUse": ["log_tool"]}

# Skills are auto-discovered from .claude/skills/ when setting_sources includes "project"
# See .claude/skills/README.md for skills, agents/README.md for subagents, hooks/ for hooks


async def main():
    mcp_servers, custom_allowed = create_tools_server(CUSTOM_TOOLS)
    agents = load_agents(SUBAGENTS)
    hooks = load_hooks(HOOKS)
    
    options = ClaudeAgentOptions(
        mcp_servers=mcp_servers,
        allowed_tools=BUILTIN_TOOLS + custom_allowed,
        setting_sources=["project"],  # Load skills from .claude/skills/
        agents=agents,  # Subagents for task delegation
        hooks=hooks,  # Intercept tool calls (logging, security, etc.)
    )
    
    async with ClaudeSDKClient(options) as client:
        await client.query("""
1. Create a file called /tmp/test_hooks.txt with content "hello"
2. Then try to run: rm -rf /
""")
        async for message in client.receive_response():
            print(message)


if __name__ == "__main__":
    anyio.run(main)
