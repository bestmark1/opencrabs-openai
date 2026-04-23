from typing import Any

from telethon import TelegramClient
from telethon.tl.custom.message import Message

from services.support_core.app.contracts import SupportContext
from services.support_core.app.intents import is_support_like_request
from services.support_core.app.hooks import (
    build_candidate_draft,
    build_operator_reply,
    build_support_reply,
    fetch_account_context,
    is_operator_request,
)
from services.telegram_adapter.app.commands import telegram_reply
from services.telegram_adapter.app.config import get_telegram_settings


def _normalized(text: str) -> str:
    return " ".join(text.strip().lower().split())


def detect_language(text: str) -> str:
    lowered = (text or "").lower()
    if any(token in lowered for token in ("hello", "payment", "refund", "support", "access")):
        return "en"
    return "ru"


def extract_owner_support_test(text: str) -> tuple[bool, str]:
    stripped = text.strip()
    prefixes = ("/support_test", "/as_user")
    for prefix in prefixes:
        if stripped.startswith(prefix):
            return True, stripped[len(prefix):].strip()
    return False, text


def _message_peer(message: Message) -> str | int:
    username = getattr(message.chat, "username", None) if getattr(message, "chat", None) else None
    if username:
        return str(username)
    sender_id = getattr(message, "sender_id", None)
    if sender_id is not None:
        return int(sender_id)
    chat_id = getattr(message, "chat_id", None)
    if chat_id is not None:
        return int(chat_id)
    return "me"


async def _send_reply_for_message(
    tg_client: TelegramClient,
    message: Message,
    *,
    reply_text: str,
) -> dict[str, Any]:
    return await telegram_reply(
        tg_client,
        {
            "peer": _message_peer(message),
            "reply_to_msg_id": int(message.id),
            "text": reply_text,
        },
    )


async def process_support_message(
    tg_client: TelegramClient,
    message: Message,
) -> dict[str, Any]:
    settings = get_telegram_settings()
    message_text = message.message or ""
    if not message_text.strip():
        return {"ok": True, "status": "empty_message_ignored", "message_id": message.id}

    sender_id = getattr(message, "sender_id", None)
    chat_id = getattr(message, "chat_id", None)
    is_owner = settings.is_trusted_operator(sender_id)
    support_test_mode, effective_text = extract_owner_support_test(message_text)
    language = detect_language(effective_text or message_text)
    is_test = bool(support_test_mode or settings.is_test_user(sender_id))
    owner_support_like = bool(
        is_owner
        and not support_test_mode
        and is_support_like_request(effective_text or message_text, language)
    )

    if is_owner and not support_test_mode and not owner_support_like and is_operator_request(message_text):
        reply_text = build_operator_reply(text=message_text, language=language)
        sent = await _send_reply_for_message(tg_client, message, reply_text=reply_text)
        return {
            "ok": True,
            "mode": "operator_mode",
            "message_id": message.id,
            "reply_text": reply_text,
            "sent": True,
            "sent_message": sent,
        }

    user_text = effective_text.strip()
    account_context = await fetch_account_context(sender_id=sender_id)
    context = SupportContext(
        user_text=user_text,
        sender_id=sender_id,
        chat_id=chat_id,
        language=language,
        is_owner=is_owner,
        is_test=is_test,
        account_context=account_context,
    )
    decision = build_support_reply(context)
    candidate = build_candidate_draft(context, decision)
    sent = await _send_reply_for_message(tg_client, message, reply_text=decision.reply_text)
    return {
        "ok": True,
        "mode": "support_test" if support_test_mode else "support",
        "message_id": message.id,
        "is_test": is_test,
        "reply_text": decision.reply_text,
        "confident": decision.confident,
        "candidate_update": candidate,
        "sent": True,
        "sent_message": sent,
    }
