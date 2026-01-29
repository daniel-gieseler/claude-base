"""Simplified tool definition pattern.

Tool definition derives from:
- name: function name
- description: docstring
- input: Pydantic model type hint
- output: just return a string (auto-wrapped)
"""

import anyio
from functools import wraps
from typing import Callable, Awaitable, get_type_hints
from pydantic import BaseModel, Field
from claude_agent_sdk import (
    ClaudeSDKClient, ClaudeAgentOptions, 
    tool as sdk_tool, create_sdk_mcp_server,
)


def custom_tool(func: Callable[[BaseModel], Awaitable[str]]):
    """Decorator that creates an MCP tool from a simple async function.
    
    - name: function.__name__
    - description: function.__doc__
    - input: first param's Pydantic type hint (validated automatically)
    - output: return string, auto-wrapped in MCP format
    """
    hints = get_type_hints(func)
    input_model = list(hints.values())[0]  # First param's type
    
    @wraps(func)
    async def handler(args: dict) -> dict:
        from pydantic import ValidationError
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


# === Example Tools ===

class CalculatorInput(BaseModel):
    expression: str = Field(description="Math expression (e.g., '2 + 2')")

@custom_tool
async def calculator(inp: CalculatorInput) -> str:
    """Evaluate mathematical expressions safely."""
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in inp.expression):
        return "Error: Invalid characters"
    return f"{inp.expression} = {eval(inp.expression)}"


class GreetInput(BaseModel):
    name: str = Field(description="Name to greet")
    formal: bool = Field(default=False, description="Use formal greeting")

@custom_tool
async def greet(inp: GreetInput) -> str:
    """Greet someone by name."""
    if inp.formal:
        return f"Good day, {inp.name}. How may I assist you?"
    return f"Hey {inp.name}!"


# === Run ===

server = create_sdk_mcp_server("simple", tools=[calculator, greet])

async def main():
    options = ClaudeAgentOptions(
        mcp_servers={"s": server},
        allowed_tools=["mcp__s__calculator", "mcp__s__greet"],
    )
    async with ClaudeSDKClient(options) as client:
        await client.query("Greet Alice formally, then calculate 7 * 8.")
        async for msg in client.receive_response():
            print(msg)

if __name__ == "__main__":
    anyio.run(main)
