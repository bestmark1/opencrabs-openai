# Architecture

## Layers

1. `telegram_adapter`
Transport and listener runtime around Telethon.

2. `support_core`
Generic routing, operator-mode separation, reply contracts, and product hooks.

3. `product hooks`
Project-specific logic: payments, subscription checks, KB integration, copy, and issue buckets.

## Design rule

The base repo should know how to:

- receive Telegram messages,
- separate operator traffic from support traffic,
- call project hooks,
- send replies,
- expose stable extension points.

The base repo should not know:

- what Premium means,
- what product tiers exist,
- where the product stores subscription data,
- what exact support copy is used.
