import unittest

from services.support_core.app.contracts import SupportContext
from services.support_core.app.hooks import build_support_reply, is_operator_request


class RuntimeSmokeTest(unittest.TestCase):
    def test_operator_request_detection(self) -> None:
        self.assertTrue(is_operator_request("что по поддержке"))
        self.assertFalse(is_operator_request("После оплаты Premium у меня старый лимит"))

    def test_generic_payment_reply(self) -> None:
        decision = build_support_reply(
            SupportContext(
                user_text="Оплата не проходит. Что делать?",
                sender_id=1,
                chat_id=1,
                language="ru",
            )
        )
        self.assertIn("дату попытки оплаты", decision.reply_text)
        self.assertEqual(decision.metadata.get("issue_bucket"), "payment")

    def test_subscription_active_reply_uses_account_context(self) -> None:
        decision = build_support_reply(
            SupportContext(
                user_text="После оплаты Premium лимит не обновился",
                sender_id=1,
                chat_id=1,
                language="ru",
                account_context={"diagnosis": "subscription_active"},
            )
        )
        self.assertIn("Платный доступ уже активен", decision.reply_text)
