"""Agent using modular tools from tools/ folder."""

import anyio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from utils import create_tools_server


BUILTIN_TOOLS = ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]
CUSTOM_TOOLS = ["calculator", "current_time", "random_number", "create_order"]

async def main():
    mcp_servers, custom_allowed = create_tools_server(CUSTOM_TOOLS)
    options = ClaudeAgentOptions(
        mcp_servers=mcp_servers,
        allowed_tools=BUILTIN_TOOLS + custom_allowed,
    )
    async with ClaudeSDKClient(options) as client:
        await client.query("Create an order for John Doe (john@example.com) with 2 laptops at $999 each, priority high.")
        async for message in client.receive_response():
            print(message)

if __name__ == "__main__":
    anyio.run(main)
