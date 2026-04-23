from typing import Any

from telethon import TelegramClient
from telethon.tl.custom.message import Message

from services.agent_core.app.contracts import AgentContext
from services.agent_core.app.hooks import (
    fetch_account_context,
    handle_default_mode,
    handle_operator_mode,
    handle_parser_mode,
)
from services.agent_core.app.modes import DEFAULT_MODE, OPERATOR_MODE, PARSER_MODE
from services.agent_core.app.router import detect_language, extract_as_user_mode, pick_mode
from services.telegram_adapter.app.commands import telegram_reply
from services.telegram_adapter.app.config import get_telegram_settings


def message_peer(message: Message) -> str | int:
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


async def send_reply_for_message(
    tg_client: TelegramClient,
    message: Message,
    *,
    reply_text: str,
) -> dict[str, Any]:
    return await telegram_reply(
        tg_client,
        {
            "peer": message_peer(message),
            "reply_to_msg_id": int(message.id),
            "text": reply_text,
        },
    )


async def process_message(
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
    as_user_mode, effective_text = extract_as_user_mode(message_text)
    language = detect_language(effective_text or message_text)
    is_test = bool(as_user_mode or settings.is_test_user(sender_id))
    mode = pick_mode(text=effective_text, is_owner=is_owner, as_user_mode=as_user_mode)
    account_context = await fetch_account_context(sender_id=sender_id)
    context = AgentContext(
        message_text=effective_text.strip(),
        sender_id=sender_id,
        chat_id=chat_id,
        language=language,
        is_owner=is_owner,
        is_test=is_test,
        account_context=account_context,
    )

    if mode == OPERATOR_MODE:
        decision = handle_operator_mode(context)
    elif mode == PARSER_MODE:
        decision = handle_parser_mode(context)
    else:
        decision = handle_default_mode(context)

    sent = await send_reply_for_message(tg_client, message, reply_text=decision.reply_text)
    return {
        "ok": True,
        "mode": decision.mode,
        "message_id": message.id,
        "is_test": is_test,
        "reply_text": decision.reply_text,
        "confident": decision.confident,
        "metadata": decision.metadata,
        "sent": True,
        "sent_message": sent,
    }
