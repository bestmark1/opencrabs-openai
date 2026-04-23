import unittest

from services.agent_core.app.contracts import AgentContext
from services.agent_core.app.hooks import handle_default_mode, handle_operator_mode, handle_parser_mode
from services.agent_core.app.modes import DEFAULT_MODE, OPERATOR_MODE, PARSER_MODE
from services.agent_core.app.router import is_operator_request, is_parser_request, pick_mode


class AgentRuntimeSmokeTest(unittest.TestCase):
    def test_operator_request_detection(self) -> None:
        self.assertTrue(is_operator_request("что по парсеру"))
        self.assertFalse(is_operator_request("собери посты из канала"))

    def test_parser_request_detection(self) -> None:
        self.assertTrue(is_parser_request("собери посты из канала"))
        self.assertFalse(is_parser_request("привет"))

    def test_mode_picker_prefers_operator_for_owner(self) -> None:
        mode = pick_mode(text="что по парсеру", is_owner=True, as_user_mode=False)
        self.assertEqual(mode, OPERATOR_MODE)

    def test_mode_picker_uses_parser_mode(self) -> None:
        mode = pick_mode(text="спарси каналы по фитнесу", is_owner=False, as_user_mode=False)
        self.assertEqual(mode, PARSER_MODE)

    def test_default_handler_reply(self) -> None:
        decision = handle_default_mode(AgentContext(message_text="привет", sender_id=1, chat_id=1))
        self.assertEqual(decision.mode, DEFAULT_MODE)
        self.assertIn("спарсить", decision.reply_text)

    def test_parser_handler_reply(self) -> None:
        decision = handle_parser_mode(AgentContext(message_text="собери посты", sender_id=1, chat_id=1))
        self.assertEqual(decision.mode, PARSER_MODE)
        self.assertIn("Запрос на парсинг принят", decision.reply_text)

    def test_operator_handler_reply(self) -> None:
        decision = handle_operator_mode(AgentContext(message_text="что по парсеру", sender_id=1, chat_id=1))
        self.assertEqual(decision.mode, OPERATOR_MODE)
        self.assertIn("Режим оператора", decision.reply_text)
