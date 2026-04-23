import unittest
import sys
import types


def _install_telethon_stubs() -> None:
    telethon = types.ModuleType("telethon")
    telethon.TelegramClient = type("TelegramClient", (), {})
    sys.modules["telethon"] = telethon

    tl_module = types.ModuleType("telethon.tl")
    custom_module = types.ModuleType("telethon.tl.custom")
    message_module = types.ModuleType("telethon.tl.custom.message")
    message_module.Message = type("Message", (), {})
    sys.modules["telethon.tl"] = tl_module
    sys.modules["telethon.tl.custom"] = custom_module
    sys.modules["telethon.tl.custom.message"] = message_module


_install_telethon_stubs()

from services.agent_core.app.contracts import AgentContext
from services.agent_core.app.hooks import handle_default_mode, handle_operator_mode
from services.agent_core.app.modes import DEFAULT_MODE, OPERATOR_MODE, PARSER_MODE
from services.agent_core.app.parser import extract_parser_request, render_parser_summary
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

    def test_operator_handler_reply(self) -> None:
        decision = handle_operator_mode(AgentContext(message_text="что по парсеру", sender_id=1, chat_id=1))
        self.assertEqual(decision.mode, OPERATOR_MODE)
        self.assertIn("Режим оператора", decision.reply_text)

    def test_extract_parser_request(self) -> None:
        request = extract_parser_request("спарси 7 постов из @fit_channel")
        self.assertIsNotNone(request)
        assert request is not None
        self.assertEqual(request.peer, "@fit_channel")
        self.assertEqual(request.limit, 7)
        self.assertEqual(request.source_kind, "posts")

    def test_render_parser_summary(self) -> None:
        request = extract_parser_request("parse 3 posts from @fit_channel")
        assert request is not None
        summary = render_parser_summary(
            request,
            [{"text": "First post", "id": 1}, {"text": "Second post", "id": 2}],
        )
        self.assertIn("@fit_channel", summary)
        self.assertIn("Получено: 2", summary)
