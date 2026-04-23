import unittest

from services.support_core.app.hooks import is_operator_request


class RuntimeSmokeTest(unittest.TestCase):
    def test_operator_request_detection(self) -> None:
        self.assertTrue(is_operator_request("что по поддержке"))
        self.assertFalse(is_operator_request("После оплаты Premium у меня старый лимит"))
