from typing import Any

from telethon import TelegramClient
from telethon.tl.custom.message import Message


def _message_to_dict(message: Message) -> dict[str, Any]:
    return {
        "id": message.id,
        "chat_id": message.chat_id,
        "sender_id": getattr(message, "sender_id", None),
        "text": message.message or "",
        "date": message.date.isoformat() if message.date else None,
        "reply_to_msg_id": message.reply_to_msg_id,
        "out": bool(message.out),
    }


async def telegram_reply(client: TelegramClient, payload: dict[str, Any]) -> dict[str, Any]:
    message = await client.send_message(
        payload["peer"],
        payload["text"],
        reply_to=int(payload["reply_to_msg_id"]),
    )
    return _message_to_dict(message)
