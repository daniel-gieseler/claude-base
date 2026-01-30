BUILTIN_TOOLS = [
    # === Core ===
    "Read",           # read file contents (supports images, PDFs)
    "Write",          # write/create files
    "Edit",           # string replacement edits in files
    "Glob",           # find files by pattern
    "Grep",           # search file contents with regex
    "Bash",           # execute shell commands
    
    # === Skills ===
    "Skill",          # load skills from .claude/skills/ (requires setting_sources=["project"])
    
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
    #"ToolSearch",     # search for available tools
    #"NotebookEdit",   # edit Jupyter notebook cells
]