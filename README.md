# OpenCrabs Agent Base

Reusable Telegram support-agent base extracted from the FitMentor support runtime.

## What is included

- Telethon transport
- listener runtime
- operator mode entrypoint
- support message routing contracts
- review/candidate hooks
- minimal project layout for reuse in another product

## What is intentionally not included

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

## Quick start

1. Copy `.env.example` to `.env`.
2. Fill Telegram session settings.
3. Implement project hooks in `services/support_core/app/hooks.py`.
4. Start the listener:

```bash
python scripts/support_listener.py
```

## Extension points

- `build_support_reply`
- `fetch_account_context`
- `build_candidate_draft`
- `is_operator_request`
- `record_support_event`

## Status

This is the first extraction pass: transport and runtime are already reusable, while product hooks are still placeholder interfaces.
