# OpenCrabs Agent Base

Reusable Telegram parser-agent base with a small runtime core and project hooks.

## Included

- Telethon transport
- listener runtime
- parser mode entrypoint
- operator mode entrypoint
- generic message routing contracts
- project hooks
- minimal project layout for reuse in another product

## Not Included

- FitMentor support logic
- payment/subscription flows
- KB candidate review flows
- product-specific parsing rules

## Structure

```text
opencrabs-agent-base/
  scripts/listener.py
  services/telegram_adapter/app/
  services/agent_core/app/
  docs/
  tests/
```

## Quick Start

1. Copy `.env.example` to `.env`.
2. Fill Telegram session settings.
3. Implement project hooks in `services/agent_core/app/hooks.py`.
4. Start the listener:

```bash
python scripts/listener.py
```

## Extension Points

- `handle_default_mode`
- `handle_parser_mode`
- `handle_operator_mode`
- `fetch_account_context`
- `is_operator_request`
- `is_parser_request`

## Publish Notes

- This is the first extraction pass.
- Transport and runtime are reusable.
- Product hooks are still placeholders and should be implemented per project.
- The current local repo path is `/tmp/opencrabs-agent-base`.

## Suggested GitHub Names

- `opencrabs-agent-base`
- `opencrabs-telegram-agent`
- `opencrabs-parser-runtime`
