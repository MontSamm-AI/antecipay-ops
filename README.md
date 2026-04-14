# AnteciPay — AI-Powered Precatorio Acquisition System

> Automates the full lifecycle of precatorio acquisition deals — from WhatsApp lead qualification (Stage 0) through proposal generation and backoffice handoff (Stage 3).

[![Stage 0](https://img.shields.io/badge/Stage%200-WhatsApp%20Prospecting-green)](docs/STAGES.md)
[![Stage 1](https://img.shields.io/badge/Stage%201-Data%20Collection-blue)](docs/STAGES.md)
[![Stage 2](https://img.shields.io/badge/Stage%202-Proposal%20PDF-orange)](docs/STAGES.md)
[![Stage 3](https://img.shields.io/badge/Stage%203-Closing-red)](docs/STAGES.md)

## What Is a Precatório?

A **precatório** is a formal court-ordered debt owed by the Brazilian government (federal, state, or municipal) to individuals or companies. Holders often wait **years** for payment — AnteciPay offers **immediate liquidity** by purchasing these credits at a negotiated discount.

**Example:** João has a R$200,000 court judgment against the São Paulo state government. Instead of waiting 5-10 years, AnteciPay pays him R$140,000 today (70% of face value) and collects the full amount from the government later.

## System Architecture

```
WhatsApp Lead
      │
      ▼
[Stage 0: cadence-antecipay]
  Opener message + qualification
      │
      ▼
[Stage 1: Data Collection]
  Precatorio number, value, tribunal
      │
      ▼
[Stage 2: Proposal]
  PDF generation + send via WhatsApp
      │
      ▼
[Stage 3: Closing]
  Human backoffice (Telegram handoff)
  Document collection + formalization
```

## Stages

| Stage | Name | Agent | Key Actions |
|-------|------|-------|-------------|
| 0 | Prospecting | cadence-antecipay | WhatsApp opener, basic qualification |
| 1 | Data Collection | cadence-antecipay | Precatorio details, tribunal, value |
| 2 | Proposal | cadence-antecipay | Value analysis, PDF proposal via WhatsApp |
| 3 | Closing | Human + Agent | Document collection, contract, formalization |

## Tech Stack

| Component | Technology |
|-----------|-----------|
| AI Agent | OpenClaw (cadence-antecipay) |
| WhatsApp | Evolution API v2 |
| Database | PostgreSQL (VPS Docker Swarm) |
| PDF Engine | Playwright + Jinja2 |
| Backoffice | Telegram Bot notifications |
| Orchestration | n8n (VPS) |
| Research | Chrome CDP automation |

## Quick Start

```bash
# 1. Clone
git clone https://github.com/MontSamm-AI/antecipay-ops
cd antecipay-ops

# 2. Install deps
pip install -r requirements.txt

# 3. Configure
cp system/config/openclaw-antecipay.example.json ~/.openclaw/workspace-antecipay/config.json
# Edit with your API keys

# 4. Test WhatsApp connection
python scripts/skills/whatsapp_sender.py

# 5. Generate test proposal
python scripts/skills/proposal_generator.py --value 150000 --rate 0.72
```

## Built By

**Sami Monteleone** — AI automation engineer  
GitHub: [@MontSamm-AI](https://github.com/MontSamm-AI)
