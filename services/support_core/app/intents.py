def normalized(text: str) -> str:
    return " ".join(text.strip().lower().split())


def normalized_simple_phrase(text: str) -> str:
    return normalized(text).strip(".,!?;:()[]{}\"'")


RU_GREETINGS = {
    "привет",
    "здравствуйте",
    "добрый день",
    "добрый вечер",
    "доброе утро",
    "салют",
}

EN_GREETINGS = {
    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon",
    "good evening",
}


def contains_any(text: str, tokens: tuple[str, ...]) -> bool:
    return any(token in text for token in tokens)


def is_payment_issue(text: str, language: str) -> bool:
    if language == "en":
        return contains_any(
            text,
            (
                "payment failed",
                "could not pay",
                "can't pay",
                "cannot pay",
                "payment did not go through",
                "card declined",
                "declined",
            ),
        )
    return contains_any(
        text,
        (
            "оплата не прошла",
            "оплата не проходит",
            "не могу оплатить",
            "не получается оплатить",
            "платеж не прошел",
            "платёж не прошёл",
            "карта отклонена",
            "не проходит оплата",
        ),
    )


def is_refund_request(text: str, language: str) -> bool:
    if language == "en":
        return contains_any(text, ("refund", "money back", "return my money", "cancel and refund"))
    return contains_any(text, ("возврат", "верните деньги", "хочу вернуть деньги", "оформить возврат"))


def is_subscription_question(text: str, language: str) -> bool:
    if language == "en":
        return contains_any(
            text,
            (
                "subscription",
                "premium",
                "paid but",
                "access",
                "limit did not update",
                "is premium active",
                "subscription status",
            ),
        )
    return contains_any(
        text,
        (
            "подписка",
            "премиум",
            "premium",
            "доступ",
            "лимит",
            "не обновился",
            "активна ли подписка",
            "статус подписки",
        ),
    )


def is_human_support_request(text: str, language: str) -> bool:
    if language == "en":
        return contains_any(text, ("human support", "talk to a person", "real person", "operator", "manager"))
    return contains_any(text, ("оператор", "живой человек", "свяжите с поддержкой", "менеджер"))


def is_thanks(text: str, language: str) -> bool:
    simple = normalized_simple_phrase(text)
    if language == "en":
        return simple in {"thanks", "thank you", "thx"}
    return simple in {"спасибо", "благодарю", "спс"}


def is_goodbye(text: str, language: str) -> bool:
    simple = normalized_simple_phrase(text)
    if language == "en":
        return simple in {"bye", "goodbye", "see you"}
    return simple in {"пока", "до свидания", "всего доброго"}


def is_greeting(text: str, language: str) -> bool:
    simple = normalized_simple_phrase(text)
    if language == "en":
        return simple in EN_GREETINGS
    return simple in RU_GREETINGS


def is_operator_summary_request(text: str) -> bool:
    text = normalized(text)
    return contains_any(
        text,
        (
            "сколько человек",
            "сколько сегодня",
            "кто написал",
            "сводка",
            "summary",
            "support today",
            "today support",
            "сегодня написало",
            "что по поддержке",
            "как дела у поддержки",
        ),
    )


def is_operator_manual_review_request(text: str) -> bool:
    text = normalized(text)
    return contains_any(
        text,
        (
            "manual review",
            "ручная проверка",
            "что требует ручной проверки",
            "неразобранные кейсы",
            "unresolved support",
        ),
    )


def is_operator_candidate_request(text: str) -> bool:
    text = normalized(text)
    return contains_any(
        text,
        (
            "candidate",
            "candidates",
            "кандидат",
            "кандидаты",
            "pending candidates",
            "knowledge-кандидат",
        ),
    )


def is_operator_request(text: str) -> bool:
    return any(
        checker(text)
        for checker in (
            is_operator_summary_request,
            is_operator_manual_review_request,
            is_operator_candidate_request,
        )
    )


def is_support_like_request(text: str, language: str) -> bool:
    normalized_text = normalized(text)
    return any(
        (
            is_payment_issue(normalized_text, language),
            is_refund_request(normalized_text, language),
            is_subscription_question(normalized_text, language),
            is_human_support_request(normalized_text, language),
        )
    )
