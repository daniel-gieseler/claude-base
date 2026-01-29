"""Same tools as agent_tools_custom.py but using the simplified decorator."""

import anyio
from pydantic import BaseModel, Field
from typing import Literal
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, create_sdk_mcp_server
from utils import custom_tool


# === Tools ===

class CalculatorInput(BaseModel):
    expression: str = Field(description="Math expression (e.g., '2 + 2 * 3')")

@custom_tool
async def calculator(inp: CalculatorInput) -> str:
    """Evaluate mathematical expressions safely."""
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in inp.expression):
        return "Error: Invalid characters"
    return f"{inp.expression} = {eval(inp.expression)}"


class CurrentTimeInput(BaseModel):
    timezone: str = Field(default="UTC", description="Timezone (e.g., 'UTC', 'US/Eastern')")

@custom_tool
async def current_time(inp: CurrentTimeInput) -> str:
    """Get current date and time."""
    from datetime import datetime, timezone as tz
    try:
        import zoneinfo
        zone = zoneinfo.ZoneInfo(inp.timezone)
        now = datetime.now(zone)
    except Exception:
        now = datetime.now(tz.utc)
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")


class RandomNumberInput(BaseModel):
    min_val: int = Field(default=1, ge=1, description="Minimum value")
    max_val: int = Field(default=100, ge=1, description="Maximum value")

@custom_tool
async def random_number(inp: RandomNumberInput) -> str:
    """Generate random integer in range."""
    import random
    return str(random.randint(inp.min_val, inp.max_val))


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

@custom_tool
async def create_order(inp: OrderInput) -> str:
    """Create order with customer, items, priority."""
    total = sum(item.quantity * item.price for item in inp.items)
    result = (
        f"Order for {inp.customer.name} ({inp.customer.email})\n"
        f"Priority: {inp.priority.upper()}\n"
        f"Items: {len(inp.items)}, Total: ${total:.2f}"
    )
    if inp.notes:
        result += f"\nNotes: {inp.notes}"
    return result


# === Server & Config ===

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
