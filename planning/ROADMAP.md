# AnteciPay — Roadmap

## ✅ v0.1 — Foundation (Current)

- [x] GitHub repository created
- [x] System architecture defined
- [x] Stage 0-3 documentation
- [x] WhatsApp sender script
- [x] Proposal generator (PDF)
- [x] Database manager (Postgres)
- [x] Backoffice notifier (Telegram)
- [x] Lead qualifier logic
- [x] Message templates (all stages)
- [x] OpenClaw workspace config

## 🚧 v0.2 — Integration (Next)

- [ ] WhatsApp instance "antecipay" created & connected
- [ ] Postgres "antecipay" database created & schema applied
- [ ] cadence-antecipay agent added to openclaw.json
- [ ] n8n webhook configured (inbound WhatsApp → agent)
- [ ] Test proposal PDF generated successfully
- [ ] End-to-end Stage 0 test with real WhatsApp number

## 🎯 v0.3 — Stage 0 Production

- [ ] Outbound campaign: first 10 leads contacted
- [ ] Inbound handling: agent responds automatically
- [ ] Stage advancement: automatic based on qualification
- [ ] Metrics: leads per stage tracked in Postgres

## 🚀 v1.0 — Full Pipeline

- [ ] Stages 0-3 fully automated (except human Stage 3 approval)
- [ ] PDF proposals sent automatically via WhatsApp
- [ ] Backoffice Telegram bot fully functional
- [ ] Dashboard (n8n or custom) showing pipeline
- [ ] First 5 deals closed

## Future Ideas

- Browser automation for precatorio validation (CNJ lookup)
- Integration with electronic signature platform
- Automated document validation
- CRM dashboard web interface
