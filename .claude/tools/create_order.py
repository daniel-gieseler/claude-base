from pydantic import BaseModel, Field
from typing import Literal
from utils import custom_tool


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
