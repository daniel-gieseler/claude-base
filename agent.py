import anyio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

# All built-in tools available in Claude Agent SDK
BUILTIN_TOOLS = [
    # === Core ===
    "Read",           # read file contents (supports images, PDFs)
    "Write",          # write/create files
    "Edit",           # string replacement edits in files
    "Glob",           # find files by pattern
    "Grep",           # search file contents with regex
    "Bash",           # execute shell commands
    
    # === Shell ===
    #"BashOutput",     # get output from background shells
    #"KillBash",       # kill background bash process
    
    # === Web ===
    #"WebFetch",       # fetch URL and process content
    #"WebSearch",      # search the web
    
    # === Subagents ===
    #"Task",           # launch subagent for complex tasks
    #"TaskOutput",     # (internal) output from subagents
    #"TaskStop",       # stop a running subagent
    
    # === User Interaction ===
    #"AskUserQuestion", # ask user clarifying questions
    #"EnterPlanMode",  # enter read-only planning mode
    #"ExitPlanMode",   # exit plan mode with a plan
    
    # === MCP Resources ===
    #"ListMcpResources", # list available MCP resources
    #"ReadMcpResource",  # read MCP resource content
    
    # === Other ===
    #"TodoWrite",      # manage task/todo lists
    #"Skill",          # load skills from .claude/skills/
    #"ToolSearch",     # search for available tools
    #"NotebookEdit",   # edit Jupyter notebook cells
]


async def main():
    options = ClaudeAgentOptions(
        allowed_tools=BUILTIN_TOOLS,
    )
    async with ClaudeSDKClient(options) as client:
        await client.query("What is 2 + 2?")
        async for message in client.receive_response():
            print(message)

if __name__ == "__main__":
    anyio.run(main)
