import re

from services.agent_core.app.contracts import ParserRequest, ParserRun
from services.agent_core.app.router import normalized


def extract_parser_request(text: str) -> ParserRequest | None:
    raw = text.strip()
    if not raw:
        return None

    peer_match = re.search(r"@([A-Za-z0-9_]{4,})", raw)
    if not peer_match:
        return None

    limit_match = re.search(r"\b(\d{1,2})\b", raw)
    limit = 10
    if limit_match:
        limit = max(1, min(50, int(limit_match.group(1))))

    source_kind = "messages"
    lowered = normalized(raw)
    if any(token in lowered for token in ("post", "posts", "пост", "посты")):
        source_kind = "posts"

    return ParserRequest(peer=f"@{peer_match.group(1)}", limit=limit, source_kind=source_kind)


def render_parser_summary(run: ParserRun) -> str:
    if not run.items:
        return (
            f"Не удалось получить данные из {run.source.peer}."
            if run.source.source_kind == "messages"
            else f"Не удалось получить посты из {run.source.peer}."
        )

    lines = [
        f"Источник: {run.source.peer}",
        f"Тип: {'posts' if run.source.source_kind == 'posts' else 'messages'}",
        f"Получено: {run.item_count}",
        "Последние элементы:",
    ]
    for item in run.items[:5]:
        snippet = str(item.text or "").strip().replace("\n", " ")
        if len(snippet) > 120:
            snippet = snippet[:117] + "..."
        lines.append(f"- {snippet or '[empty]'}")
    return "\n".join(lines)
