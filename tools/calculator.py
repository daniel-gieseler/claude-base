from pydantic import BaseModel, Field
from utils import custom_tool


class CalculatorInput(BaseModel):
    expression: str = Field(description="Math expression (e.g., '2 + 2 * 3')")


@custom_tool
async def calculator(inp: CalculatorInput) -> str:
    """Evaluate mathematical expressions safely."""
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in inp.expression):
        return "Error: Invalid characters"
    return f"{inp.expression} = {eval(inp.expression)}"
