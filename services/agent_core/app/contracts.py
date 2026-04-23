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
