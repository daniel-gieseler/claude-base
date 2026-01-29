import anyio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, tool, create_sdk_mcp_server
from pydantic import BaseModel, Field
from typing import Any, Literal


# === Tool Definitions ===

class CalculatorInput(BaseModel):
    expression: str = Field(description="Mathematical expression (e.g., '2 + 2 * 3')")

@tool(
    "calculator",
    "Evaluate mathematical expressions safely",
    CalculatorInput.model_json_schema()
)
async def calculator(args: dict[str, Any]) -> dict[str, Any]:
    try:
        allowed = set("0123456789+-*/.() ")
        expr = args["expression"]
        if not all(c in allowed for c in expr):
            return {"content": [{"type": "text", "text": "Error: Invalid characters"}]}
        result = eval(expr)
        return {"content": [{"type": "text", "text": f"{expr} = {result}"}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error: {e}"}], "is_error": True}


class CurrentTimeInput(BaseModel):
    timezone: str = Field(default="UTC", description="Timezone (e.g., 'UTC', 'US/Eastern')")

@tool(
    "current_time",
    "Get current date and time",
    CurrentTimeInput.model_json_schema()
)
async def current_time(args: dict[str, Any]) -> dict[str, Any]:
    from datetime import datetime, timezone as tz
    try:
        import zoneinfo
        zone = zoneinfo.ZoneInfo(args.get("timezone", "UTC"))
        now = datetime.now(zone)
    except Exception:
        now = datetime.now(tz.utc)
    return {"content": [{"type": "text", "text": now.strftime("%Y-%m-%d %H:%M:%S %Z")}]}


class RandomNumberInput(BaseModel):
    min_val: int = Field(default=1, ge=1, description="Minimum value")
    max_val: int = Field(default=100, ge=1, description="Maximum value")

@tool(
    "random_number",
    "Generate random integer in range",
    RandomNumberInput.model_json_schema()
)
async def random_number(args: dict[str, Any]) -> dict[str, Any]:
    import random
    result = random.randint(args.get("min_val", 1), args.get("max_val", 100))
    return {"content": [{"type": "text", "text": str(result)}]}


class Customer(BaseModel):
    name: str = Field(min_length=1)
    email: str

class OrderItem(BaseModel):
    product: str
    quantity: int = Field(ge=1)
    price: float = Field(ge=0)

class OrderInput(BaseModel):
    customer: Customer
    items: list[OrderItem] = Field(min_length=1)
    priority: Literal["low", "normal", "high", "urgent"]
    notes: str | None = None

@tool(
    "create_order",
    "Create order with customer, items, priority",
    OrderInput.model_json_schema()
)
async def create_order(args: dict[str, Any]) -> dict[str, Any]:
    customer = args["customer"]
    items = args["items"]
    priority = args["priority"]
    total = sum(item["quantity"] * item["price"] for item in items)
    summary = (
        f"Order for {customer['name']} ({customer['email']})\n"
        f"Priority: {priority.upper()}\n"
        f"Items: {len(items)}, Total: ${total:.2f}"
    )
    if notes := args.get("notes"):
        summary += f"\nNotes: {notes}"
    return {"content": [{"type": "text", "text": summary}]}


# === MCP Server & Config ===

custom_server = create_sdk_mcp_server(
    name="custom-tools",
    version="1.0.0",
    tools=[calculator, current_time, random_number, create_order],
)

BUILTIN_TOOLS = ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]
CUSTOM_TOOLS = [
    "mcp__custom__calculator",
    "mcp__custom__current_time",
    "mcp__custom__random_number",
    "mcp__custom__create_order",
]


async def main():
    options = ClaudeAgentOptions(
        mcp_servers={"custom": custom_server},
        allowed_tools=BUILTIN_TOOLS + CUSTOM_TOOLS,
    )
    async with ClaudeSDKClient(options) as client:
        await client.query("Create an order for John Doe (john@example.com) with 2 laptops at $999 each and 1 mouse at $29, priority high.")
        async for message in client.receive_response():
            print(message)

if __name__ == "__main__":
    anyio.run(main)
