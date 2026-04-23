from services.support_core.app.contracts import ReplyDecision, SupportContext
from services.support_core.app.intents import is_goodbye, is_greeting, is_thanks


def should_create_candidate(context: SupportContext, decision: ReplyDecision) -> bool:
    text = context.user_text.strip()
    if not text or decision.confident:
        return False
    if is_greeting(text, context.language) or is_thanks(text, context.language) or is_goodbye(text, context.language):
        return False
    if len(text) < 20:
        return False
    return decision.metadata.get("issue_bucket") == "generic"


def build_candidate_draft(context: SupportContext, decision: ReplyDecision) -> dict | None:
    if not should_create_candidate(context, decision):
        return None
    return {
        "status": "pending",
        "suggested_title": "New unsupported support scenario",
        "suggested_content": (
            "User asked a question that did not match an approved support pattern. "
            "Review the wording and decide whether this should become a reusable knowledge card."
        ),
        "evidence": {
            "user_text": context.user_text,
            "draft_reply": decision.reply_text,
            "language": context.language,
        },
    }
