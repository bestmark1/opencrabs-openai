from services.agent_core.app.modes import DEFAULT_MODE, OPERATOR_MODE, PARSER_MODE


def normalized(text: str) -> str:
    return " ".join(text.strip().lower().split())


def detect_language(text: str) -> str:
    lowered = (text or "").lower()
    if any(token in lowered for token in ("hello", "channel", "parse", "messages", "posts")):
        return "en"
    return "ru"


def extract_as_user_mode(text: str) -> tuple[bool, str]:
    stripped = text.strip()
    prefixes = ("/as_user", "/parse_test")
    for prefix in prefixes:
        if stripped.startswith(prefix):
            return True, stripped[len(prefix):].strip()
    return False, text


def is_operator_request(text: str) -> bool:
    text = normalized(text)
    return any(
        token in text
        for token in (
            "status",
            "summary",
            "что по парсеру",
            "что по агенту",
            "покажи статус",
            "operator",
            "сводка",
        )
    )


def is_parser_request(text: str) -> bool:
    text = normalized(text)
    return any(
        token in text
        for token in (
            "parse",
            "parser",
            "спарси",
            "собери посты",
            "собери сообщения",
            "канал",
            "каналы",
            "чат",
            "чаты",
            "posts",
            "messages",
        )
    )


def pick_mode(*, text: str, is_owner: bool, as_user_mode: bool) -> str:
    if is_owner and not as_user_mode and is_operator_request(text):
        return OPERATOR_MODE
    if is_parser_request(text):
        return PARSER_MODE
    return DEFAULT_MODE
