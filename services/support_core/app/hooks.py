from typing import Any

from services.support_core.app.candidates import build_candidate_draft as default_build_candidate_draft
from services.support_core.app.contracts import ReplyDecision, SupportContext
from services.support_core.app.intents import is_operator_request as default_is_operator_request
from services.support_core.app.replies import (
    build_operator_reply as default_build_operator_reply,
    build_support_reply as default_build_support_reply,
)


async def fetch_account_context(*, sender_id: int | None) -> dict[str, Any] | None:
    del sender_id
    return None


def build_support_reply(context: SupportContext) -> ReplyDecision:
    return default_build_support_reply(context)


def build_operator_reply(*, text: str, language: str) -> str:
    return default_build_operator_reply(text=text, language=language)


def build_candidate_draft(context: SupportContext, decision: ReplyDecision) -> dict[str, Any] | None:
    return default_build_candidate_draft(context, decision)


def is_operator_request(text: str) -> bool:
    return default_is_operator_request(text)
