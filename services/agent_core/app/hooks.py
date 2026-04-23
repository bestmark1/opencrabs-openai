from typing import Any

from services.agent_core.app.contracts import AgentContext, AgentDecision
from services.agent_core.app.modes import DEFAULT_MODE, OPERATOR_MODE, PARSER_MODE
from services.agent_core.app.parser import extract_parser_request, render_parser_summary
from services.telegram_adapter.app.commands import telegram_get_channel_posts, telegram_get_messages, telegram_resolve_peer


async def fetch_account_context(*, sender_id: int | None) -> dict | None:
    del sender_id
    return None


def handle_default_mode(context: AgentContext) -> AgentDecision:
    if context.language == "en":
        return AgentDecision(
            mode=DEFAULT_MODE,
            reply_text="Write what you want to parse or inspect. For example: parse channels about nutrition or collect recent posts.",
            confident=False,
        )
    return AgentDecision(
        mode=DEFAULT_MODE,
        reply_text="Напишите, что именно нужно спарсить или посмотреть. Например: спарси каналы по питанию или собери последние посты.",
        confident=False,
    )


def handle_operator_mode(context: AgentContext) -> AgentDecision:
    del context
    return AgentDecision(
        mode=OPERATOR_MODE,
        reply_text="Режим оператора: можно запросить статус, сводку или очередь задач парсера.",
        confident=True,
    )


async def handle_parser_mode(client: Any, context: AgentContext) -> AgentDecision:
    request = extract_parser_request(context.message_text)
    if request is None:
        if context.language == "en":
            return AgentDecision(
                mode=PARSER_MODE,
                reply_text="Specify a Telegram target, for example: parse 10 posts from @channel_name.",
                confident=False,
            )
        return AgentDecision(
            mode=PARSER_MODE,
            reply_text="Укажите Telegram-цель, например: спарси 10 постов из @channel_name.",
            confident=False,
        )

    resolved = await telegram_resolve_peer(client, {"peer": request.peer})
    if request.source_kind == "posts":
        result = await telegram_get_channel_posts(client, {"peer": request.peer, "limit": request.limit})
    else:
        result = await telegram_get_messages(client, {"peer": request.peer, "limit": request.limit})

    items = list(result.get("items") or [])
    return AgentDecision(
        mode=PARSER_MODE,
        reply_text=render_parser_summary(request, items),
        confident=True,
        metadata={
            "action": "parse_request",
            "request": {
                "peer": request.peer,
                "limit": request.limit,
                "source_kind": request.source_kind,
            },
            "resolved_peer": resolved,
            "items": items,
        },
    )
