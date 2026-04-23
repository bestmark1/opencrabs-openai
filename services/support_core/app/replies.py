from services.support_core.app.contracts import ReplyDecision, SupportContext
from services.support_core.app.intents import (
    is_goodbye,
    is_greeting,
    is_human_support_request,
    is_payment_issue,
    is_refund_request,
    is_subscription_question,
    is_thanks,
    normalized,
)


def build_operator_reply(*, text: str, language: str) -> str:
    del text
    if language == "en":
        return "Tell me directly what to inspect: support, manual review, or candidate queue."
    return "Напишите прямо, что посмотреть: поддержку, ручную проверку или очередь кандидатов."


def build_support_reply(context: SupportContext) -> ReplyDecision:
    text = context.user_text.strip()
    normalized_text = normalized(text)
    account_context = context.account_context or {}
    diagnosis = str(account_context.get("diagnosis") or "")

    if not text:
        return ReplyDecision(reply_text="", confident=True, metadata={"status": "empty"})

    if is_greeting(text, context.language):
        if context.language == "en":
            return ReplyDecision("Hello. How can I help you today?", True)
        return ReplyDecision("Здравствуйте. Чем могу помочь?", True)

    if is_thanks(text, context.language):
        return ReplyDecision("You're welcome." if context.language == "en" else "Пожалуйста.", True)

    if is_goodbye(text, context.language):
        return ReplyDecision("Goodbye." if context.language == "en" else "Всего доброго.", True)

    if is_subscription_question(normalized_text, context.language):
        if diagnosis == "subscription_active":
            if context.language == "en":
                return ReplyDecision(
                    "I checked the account status. Paid access is active. If something still looks wrong, describe exactly what did not update.",
                    False,
                    metadata={"issue_bucket": "subscription"},
                )
            return ReplyDecision(
                "Я проверил статус аккаунта. Платный доступ уже активен. Если что-то всё ещё выглядит неправильно, напишите, что именно не обновилось.",
                False,
                metadata={"issue_bucket": "subscription"},
            )
        if diagnosis == "no_payment_found":
            if context.language == "en":
                return ReplyDecision(
                    "I checked the account status and do not yet see an active paid subscription or recorded payment. Please send the payment date, amount, and confirmation if you have it.",
                    False,
                    metadata={"issue_bucket": "subscription"},
                )
            return ReplyDecision(
                "Я проверил статус аккаунта и пока не вижу активной платной подписки или найденного платежа. Пришлите, пожалуйста, дату платежа, сумму и подтверждение оплаты, если оно у вас есть.",
                False,
                metadata={"issue_bucket": "subscription"},
            )
        if context.language == "en":
            return ReplyDecision(
                "Please describe what happened with the subscription or access. If payment is involved, send the payment date and amount.",
                False,
                metadata={"issue_bucket": "subscription"},
            )
        return ReplyDecision(
            "Опишите, пожалуйста, что произошло с подпиской или доступом. Если это связано с оплатой, сразу пришлите дату платежа и сумму.",
            False,
            metadata={"issue_bucket": "subscription"},
        )

    if is_payment_issue(normalized_text, context.language):
        if context.language == "en":
            return ReplyDecision(
                "If payment does not go through, please send the attempt date, amount, payment method, and the exact error if you saw one.",
                False,
                metadata={"issue_bucket": "payment"},
            )
        return ReplyDecision(
            "Если оплата не проходит, пришлите, пожалуйста, дату попытки оплаты, сумму, способ оплаты и точный текст ошибки, если он был.",
            False,
            metadata={"issue_bucket": "payment"},
        )

    if is_refund_request(normalized_text, context.language):
        if context.language == "en":
            return ReplyDecision(
                "Please send the payment date, amount, and the reason for the refund request. Support will review the case manually.",
                False,
                metadata={"issue_bucket": "refund"},
            )
        return ReplyDecision(
            "Пришлите, пожалуйста, дату платежа, сумму и причину запроса на возврат. Поддержка проверит кейс вручную.",
            False,
            metadata={"issue_bucket": "refund"},
        )

    if is_human_support_request(normalized_text, context.language):
        if context.language == "en":
            return ReplyDecision(
                "Understood. Please describe the issue briefly, and support will review it.",
                False,
                metadata={"issue_bucket": "human_support"},
            )
        return ReplyDecision(
            "Понял. Коротко опишите проблему, и поддержка её посмотрит.",
            False,
            metadata={"issue_bucket": "human_support"},
        )

    if context.language == "en":
        return ReplyDecision(
            "What is your question? I will try to help. If this is about payment or access, include the account and payment details right away.",
            False,
            metadata={"issue_bucket": "generic"},
        )
    return ReplyDecision(
        "Какой у вас вопрос? Постараюсь помочь. Если это про оплату или доступ, сразу укажите аккаунт и данные платежа, если они есть.",
        False,
        metadata={"issue_bucket": "generic"},
    )
