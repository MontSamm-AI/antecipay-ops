# AnteciPay System Overview

## What We Do

AnteciPay acquires precatórios (court-ordered government debts) from holders who prefer immediate liquidity over waiting for the government to pay. We pay a discounted amount upfront and collect the full value later.

## Business Model

- Holder has: R$200,000 precatório (government owes them)
- Holder receives: R$140,000 from AnteciPay NOW
- AnteciPay collects: R$200,000 from government (over time)
- AnteciPay profit: R$60,000 (30% spread)

## AI Agent Role

The `cadence-antecipay` OpenClaw agent handles:
1. **Outbound prospecting** — identifies and contacts potential cedentes via WhatsApp
2. **Inbound qualification** — responds to interested parties, collects data
3. **Proposal generation** — calculates offers, generates PDF, sends via WhatsApp
4. **Stage tracking** — maintains lead status in Postgres CRM
5. **Handoff** — notifies human backoffice via Telegram when Stage 3 reached

## Infrastructure

- **VPS (5.78.144.113)**: Docker Swarm with all services
- **WSL (Ubuntu)**: OpenClaw agent runtime
- **Windows Chrome**: CDP browser for research
- **GitHub**: Code and documentation

## Security

- API keys in .env (never committed)
- SSH key authentication for VPS
- Postgres with dedicated antecipay user
