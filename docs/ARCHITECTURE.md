# Architecture

## Layers

1. `telegram_adapter`
Transport and listener runtime around Telethon.

2. `agent_core`
Generic routing, parser-mode separation, operator-mode separation, reply contracts, and project hooks.

3. `product hooks`
Project-specific logic: parsing rules, extraction targets, persistence, scoring, and post-processing.

## Design rule

The base repo should know how to:

- receive Telegram messages,
- separate operator traffic from parser traffic,
- call project hooks,
- send replies,
- expose stable extension points.

The base repo should not know:

- what product-specific entities are being parsed,
- where parsed results are stored,
- what scoring or enrichment pipeline a project uses.
