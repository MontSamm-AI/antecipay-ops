# Backoffice & Human Handoff

## When to Hand Off

The agent hands off to human backoffice when:
1. Lead reaches Stage 3 (closing ready)
2. Lead has objections agent cannot resolve
3. Legal/compliance questions arise
4. Document validation needed

## Telegram Handoff

The agent sends a structured Telegram message to the backoffice bot.

### Handoff Message Format

```
🔔 HANDOFF AnteciPay — Stage 3

👤 Lead: João da Silva
📱 WhatsApp: +55 11 99999-9999
💰 Precatório: R$ 200.000,00
📋 Processo: 0001234-56.2018.8.26.0001
🏛️ Tribunal: TJSP

📝 Resumo: Lead qualificado, proposta aceita (R$140k / 70%). 
Aguardando coleta de documentos.

⚡ Ação necessária: Iniciar processo de formalização
```

## Backoffice Actions

1. Review lead in Postgres (leads table)
2. Contact lead for document collection
3. Forward to legal team for contract prep
4. Update lead stage in DB
5. Confirm transfer via bank
