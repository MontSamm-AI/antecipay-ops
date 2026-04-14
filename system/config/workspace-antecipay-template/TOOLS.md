# AnteciPay — Tools & Infrastructure

## WhatsApp (Evolution API)
- URL: https://evolution.montsam.site
- Instância: antecipay
- Skill: whatsapp_sender.py
- Capacidades: texto, PDF, documentos, imagens

## Database (Postgres VPS)
- Host: 5.78.144.113 (Docker Swarm)
- DB: antecipay
- Skill: database_manager.py
- Tabelas: leads, interactions, proposals

## PDF Generator
- Engine: Playwright + Jinja2
- Skill: proposal_generator.py
- Templates: workspace-antecipay/templates/proposal/
- Output: workspace-antecipay/artifacts/proposals/

## Browser Research (CDP)
- Porta: 9222 (Windows Chrome)
- Skill: browser_research.py
- Uso: pesquisar processos judiciais (CNJ, tribunais), validar precatórios

## Backoffice (Telegram)
- Skill: backoffice_notifier.py / telegram_handoff.py
- Uso: handoff Stage 3, alertas urgentes, confirmações

## OpenClaw Gateway
- WS: ws://127.0.0.1:18789
- Token: (em .env)

## n8n (Orchestration)
- URL: https://n8n.montsam.site
- Uso: webhooks de entrada WhatsApp, automações
