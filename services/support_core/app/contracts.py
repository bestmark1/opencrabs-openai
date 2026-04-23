from dataclasses import dataclass, field
from typing import Any


@dataclass
class SupportContext:
    user_text: str
    sender_id: int | None
    chat_id: int | None
    language: str = "ru"
    is_owner: bool = False
    is_test: bool = False
    account_context: dict[str, Any] | None = None


@dataclass
class ReplyDecision:
    reply_text: str
    confident: bool
    mode: str = "support"
    metadata: dict[str, Any] = field(default_factory=dict)
