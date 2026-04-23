from datetime import datetime, timezone

from services.agent_core.app.contracts import ParserItem, ParserRun, ParserSource


def normalize_parser_items(raw_items: list[dict]) -> list[ParserItem]:
    items: list[ParserItem] = []
    for raw in raw_items:
        items.append(
            ParserItem(
                id=raw.get("id"),
                chat_id=raw.get("chat_id"),
                sender_id=raw.get("sender_id"),
                text=str(raw.get("text") or ""),
                date=raw.get("date"),
                reply_to_msg_id=raw.get("reply_to_msg_id"),
                out=bool(raw.get("out")),
            )
        )
    return items


def build_parser_run(*, peer: str, source_kind: str, limit: int, resolved_peer: dict, raw_items: list[dict]) -> ParserRun:
    items = normalize_parser_items(raw_items)
    return ParserRun(
        source=ParserSource(
            peer=peer,
            source_kind=source_kind,
            limit=limit,
            resolved_peer=resolved_peer,
        ),
        item_count=len(items),
        items=items,
        collected_at=datetime.now(timezone.utc).isoformat(),
    )
