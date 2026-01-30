from pydantic import BaseModel, Field
from utils import custom_tool


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
