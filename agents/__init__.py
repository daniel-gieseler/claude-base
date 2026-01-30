"""Subagents collection for task delegation."""

from .code_reviewer import code_reviewer
from .debugger import debugger
from .researcher import researcher

ALL_AGENTS = {"code_reviewer": code_reviewer, "debugger": debugger, "researcher": researcher}
