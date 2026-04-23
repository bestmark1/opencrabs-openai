from services.agent_core.app.contracts import AgentContext, AgentDecision
from services.agent_core.app.modes import DEFAULT_MODE, OPERATOR_MODE, PARSER_MODE


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


def handle_parser_mode(context: AgentContext) -> AgentDecision:
    text = context.message_text.strip()
    if context.language == "en":
        return AgentDecision(
            mode=PARSER_MODE,
            reply_text=f"Parser mode accepted: {text}",
            confident=True,
            metadata={"action": "parse_request"},
        )
    return AgentDecision(
        mode=PARSER_MODE,
        reply_text=f"Запрос на парсинг принят: {text}",
        confident=True,
        metadata={"action": "parse_request"},
    )
