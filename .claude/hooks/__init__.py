"""Hooks collection."""

from .log_tool import log_tool
from .block_rm_rf import block_rm_rf

ALL_HOOKS = {"log_tool": log_tool, "block_rm_rf": block_rm_rf}
