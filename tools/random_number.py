from pydantic import BaseModel, Field
from utils import custom_tool


class RandomNumberInput(BaseModel):
    min_val: int = Field(default=1, ge=1, description="Minimum value")
    max_val: int = Field(default=100, ge=1, description="Maximum value")


@custom_tool
async def random_number(inp: RandomNumberInput) -> str:
    """Generate random integer in range."""
    import random
    return str(random.randint(inp.min_val, inp.max_val))
