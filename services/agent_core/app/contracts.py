from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentContext:
    message_text: str
    sender_id: int | None
    chat_id: int | None
    language: str = "ru"
    is_owner: bool = False
    is_test: bool = False
    account_context: dict[str, Any] | None = None


@dataclass
class AgentDecision:
    mode: str
    reply_text: str = ""
    confident: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ParserRequest:
    peer: str
    limit: int = 10
    source_kind: str = "messages"


@dataclass
class ParserItem:
    id: int | None
    chat_id: int | None
    sender_id: int | None
    text: str
    date: str | None
    reply_to_msg_id: int | None
    out: bool
