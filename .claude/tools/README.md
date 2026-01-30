# Custom Tools

## Creating a New Tool

```python
from pydantic import BaseModel, Field
from utils import custom_tool


class MyToolInput(BaseModel):
    param: str = Field(description="Description for Claude")
    count: int = Field(default=10, ge=0)


@custom_tool
async def my_tool(inp: MyToolInput) -> str:
    """Short description shown to Claude."""
    try:
        result = do_something(inp.param, inp.count)
        return f"Success: processed {inp.count} items"
    except ValueError as e:
        return f"Error: {e}"
```

## Rules

| Aspect | Requirement |
|--------|-------------|
| **Name** | Function name = tool name |
| **Description** | Docstring = tool description |
| **Input** | Pydantic model as type hint |
| **Output** | Return a string (auto-wrapped) |
| **Errors** | Return error message as string, don't raise |
| **Validation** | Handled by `@custom_tool` decorator |

## Register Tool

1. Export in `tools/__init__.py`
2. Add name to `CUSTOM_TOOLS` list in agent
