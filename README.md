# OpenCrabs Agent Base

Reusable Telegram support-agent base extracted from a production support runtime and stripped down to a reusable core.

## Included

- Telethon transport
- listener runtime
- operator mode entrypoint
- support message routing contracts
- review/candidate hooks
- minimal project layout for reuse in another product

## Not Included

- FitMentor-specific copy
- FitMentor subscription/payment checks
- FitMentor KB content and migrations
- FitMentor-specific issue buckets

## Structure

```text
opencrabs-agent-base/
  scripts/support_listener.py
  services/telegram_adapter/app/
  services/support_core/app/
  docs/
  tests/
```

## Quick Start

1. Copy `.env.example` to `.env`.
2. Fill Telegram session settings.
3. Implement project hooks in `services/support_core/app/hooks.py`.
4. Start the listener:

```bash
python scripts/support_listener.py
```

## Extension Points

- `build_support_reply`
- `fetch_account_context`
- `build_candidate_draft`
- `is_operator_request`
- `record_support_event`

## Publish Notes

- This is the first extraction pass.
- Transport and runtime are reusable.
- Product hooks are still placeholders and should be implemented per project.
- The current local repo path is `/tmp/opencrabs-agent-base`.

## Suggested GitHub Names

- `opencrabs-agent-base`
- `opencrabs-telegram-agent`
- `opencrabs-support-runtime`
