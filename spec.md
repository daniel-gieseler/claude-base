# General Config
https://platform.claude.com/docs/en/agent-sdk/python#claude-sdk-client
https://platform.claude.com/docs/en/agent-sdk/python#types
## Tools (built-in)
https://platform.claude.com/docs/en/agent-sdk/python#tool-input-output-types

# Tools (custom)
https://platform.claude.com/docs/en/agent-sdk/custom-tools
https://platform.claude.com/docs/en/agent-sdk/mcp
https://platform.claude.com/docs/en/agent-sdk/python#using-custom-tools-with-claude-sdk-client

# (Sub)agents
https://platform.claude.com/docs/en/agent-sdk/subagents

# Skills
https://platform.claude.com/docs/en/agent-sdk/skills

# Hooks
https://platform.claude.com/docs/en/agent-sdk/python#hook-types
https://platform.claude.com/docs/en/agent-sdk/hooks
https://platform.claude.com/docs/en/agent-sdk/python#using-hooks-for-behavior-modification

# Retrieval
Notice that tools, subagents and skills are also callable.
Can be either loaded by default or when requested.
We need to understand how to set this distinction.
Also understand how to retrieve them efficiently and precisely.
I remember reading somehitng in the docs about a search feature that uses regex or bm25...


---

Always do the minimal implementation to illustrate and educate the utilization of it.

[X] build a minimalistic client call with the built=in tools listed and documented in the script, we will select some of them.

[X] create a few custom tools to complete the current built-in tools
