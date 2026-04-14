# AnteciPay — Sistema de Aquisição de Precatórios com IA

> Automatiza o ciclo completo de aquisição de precatórios — desde a qualificação de leads via WhatsApp (Stage 0) até a formalização (Stage 3).

## O que é um Precatório?

Um **precatório** é uma dívida formal do governo (federal, estadual ou municipal) com um indivíduo ou empresa, resultante de decisão judicial. Os titulares frequentemente esperam **anos** pelo pagamento — a AnteciPay oferece **liquidez imediata**, comprando esses créditos com desconto.

## Como Funciona

1. **Stage 0**: Prospecção via WhatsApp — identificamos potenciais cedentes
2. **Stage 1**: Coleta de dados — número do processo, valor, tribunal
3. **Stage 2**: Proposta — análise de viabilidade, geração de proposta em PDF
4. **Stage 3**: Fechamento — coleta de documentos, assinatura, transferência

## Rodando o Sistema

```bash
pip install -r requirements.txt
python scripts/skills/whatsapp_sender.py
```
