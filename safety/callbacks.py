"""
CinemaNexus - Security & Safety Callbacks
=========================================
Multi-layered ADK callbacks:
- before_model_callback -> blocks prompt injection before inference
- after_model_callback  -> redacts PII before output reaches the user
- before_tool_callback  -> sanitizes and validates tool arguments
"""

import logging
from typing import Any, Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types

try:
    from ..schemas import GuardrailResult
except (ImportError, ValueError):
    from schemas import GuardrailResult

from .filters import (
    INJECTION_PATTERNS,
    MAX_TITLE_LENGTH,
    MAX_WATCHLIST_SIZE,
    PII_PATTERNS,
)

logger = logging.getLogger(__name__)


def _extract_last_user_text(llm_request: LlmRequest) -> str:
    """Pull the text of the most recent user message from the LLM request."""
    if llm_request.contents and llm_request.contents[-1].role == "user":
        parts = llm_request.contents[-1].parts or []
        return " ".join(p.text for p in parts if getattr(p, "text", None))
    return ""


def input_guardrail(
    callback_context: CallbackContext,
    llm_request: LlmRequest,
) -> Optional[LlmResponse]:
    """Block prompt-injection attempts before they reach the LLM.

    Returns an LlmResponse to short-circuit the call when a threat is
    detected, or None to let the request proceed normally.
    """
    text = _extract_last_user_text(llm_request)
    matched = [p.pattern for p in INJECTION_PATTERNS if p.search(text)]

    if matched:
        result = GuardrailResult(
            passed=False, reason="prompt_injection", patterns_matched=matched
        )
        logger.warning("Input guardrail BLOCKED: %s", result.model_dump_json())
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[
                    types.Part(
                        text=(
                            "I can't process that request. "
                            "If you have a question about movies or TV shows, I'm happy to help."
                        )
                    )
                ],
            )
        )
    return None


def output_guardrail(
    callback_context: CallbackContext,
    llm_response: LlmResponse,
) -> Optional[LlmResponse]:
    """Redact PII from the model's response before it reaches the user."""
    if not llm_response.content or not llm_response.content.parts:
        return None

    modified = False
    new_parts: list[types.Part] = []

    for part in llm_response.content.parts:
        text = part.text
        if not text:
            new_parts.append(part)
            continue
        for replacement, pattern in PII_PATTERNS.items():
            if pattern.search(text):
                text = pattern.sub(replacement, text)
                modified = True
        new_parts.append(types.Part(text=text))

    if modified:
        logger.info("Output guardrail - PII redacted from response")
        return LlmResponse(content=types.Content(role="model", parts=new_parts))
    return None


def watchlist_tool_guardrail(
    tool: BaseTool,
    args: dict[str, Any],
    tool_context: ToolContext,
) -> Optional[dict]:
    """Validate watchlist tool arguments before execution.

    - Enforces max title length and watchlist size limits.
    - Sanitizes title input (strip whitespace).
    - Returns a dict to skip the tool call if validation fails;
      returns None to proceed normally.
    """
    if tool.name != "manage_watchlist":
        return None

    title = args.get("title", "")
    action = args.get("action", "")

    # Sanitize title - strip whitespace
    if title:
        args["title"] = title.strip()

    # Title length check
    if title and len(title) > MAX_TITLE_LENGTH:
        logger.warning("Tool guardrail – title too long: %d chars", len(title))
        return {
            "status": "error",
            "message": f"Title must be under {MAX_TITLE_LENGTH} characters.",
        }

    # Watchlist size check on add
    if action == "add":
        current = tool_context.state.get("user_watchlist", [])
        if len(current) >= MAX_WATCHLIST_SIZE:
            logger.warning("Tool guardrail – watchlist full: %d items", len(current))
            return {
                "status": "error",
                "message": f"Watchlist is full ({MAX_WATCHLIST_SIZE} movies max). Remove one first.",
            }

    logger.debug("Tool guardrail – passed for %s(%s)", tool.name, action)
    return None
