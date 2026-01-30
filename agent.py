"""Agent using modular tools and skills."""

import anyio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from utils import create_tools_server


# === Configuration ===
BUILTIN_TOOLS = ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Skill"]
CUSTOM_TOOLS = ["calculator", "current_time", "random_number", "create_order"]

# Skills are auto-discovered from .claude/skills/ when setting_sources includes "project"
# See .claude/skills/README.md for how to create custom skills


async def main():
    mcp_servers, custom_allowed = create_tools_server(CUSTOM_TOOLS)
    
    options = ClaudeAgentOptions(
        mcp_servers=mcp_servers,
        allowed_tools=BUILTIN_TOOLS + custom_allowed,
        setting_sources=["project"],  # Load skills from .claude/skills/
    )
    
    async with ClaudeSDKClient(options) as client:
        await client.query("Review this code for issues: def add(a, b): return a + b")
        async for message in client.receive_response():
            print(message)


if __name__ == "__main__":
    anyio.run(main)
