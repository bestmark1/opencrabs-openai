from typing import Any

from services.support_core.app.contracts import ReplyDecision, SupportContext


async def fetch_account_context(*, sender_id: int | None) -> dict[str, Any] | None:
    del sender_id
    return None


def build_support_reply(context: SupportContext) -> ReplyDecision:
    text = context.user_text.strip()
    if not text:
        return ReplyDecision(reply_text="", confident=True, metadata={"status": "empty"})
    return ReplyDecision(
        reply_text="Какой у вас вопрос? Постараюсь помочь.",
        confident=False,
    )


def build_operator_reply(*, text: str, language: str) -> str:
    if language == "en":
        return "Tell me directly what to inspect: support, manual review, payments, or candidates."
    return "Напишите прямо, что посмотреть: поддержку, ручную проверку, оплаты или кандидатов."


def build_candidate_draft(context: SupportContext, decision: ReplyDecision) -> dict[str, Any] | None:
    del context, decision
    return None


def is_operator_request(text: str) -> bool:
    normalized = " ".join(text.strip().lower().split())
    triggers = (
        "что по поддержке",
        "сводка",
        "manual review",
        "pending candidates",
        "кандидаты",
        "ручная проверка",
    )
    return any(token in normalized for token in triggers)
