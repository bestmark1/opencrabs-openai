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


async def telegram_resolve_peer(client: TelegramClient, payload: dict[str, Any]) -> dict[str, Any]:
    entity = await client.get_entity(payload["peer"])
    return {
        "id": getattr(entity, "id", None),
        "username": getattr(entity, "username", None),
        "title": getattr(entity, "title", None),
        "first_name": getattr(entity, "first_name", None),
        "last_name": getattr(entity, "last_name", None),
    }


async def telegram_get_messages(client: TelegramClient, payload: dict[str, Any]) -> dict[str, Any]:
    peer = payload["peer"]
    limit = int(payload.get("limit", 20))
    messages = await client.get_messages(peer, limit=limit)
    return {"items": [_message_to_dict(message) for message in messages]}


async def telegram_get_channel_posts(client: TelegramClient, payload: dict[str, Any]) -> dict[str, Any]:
    peer = payload["peer"]
    limit = int(payload.get("limit", 20))
    messages = await client.get_messages(peer, limit=limit)
    items = [item for item in messages if getattr(item, "post", False) or item.chat_id]
    return {"items": [_message_to_dict(message) for message in items]}
