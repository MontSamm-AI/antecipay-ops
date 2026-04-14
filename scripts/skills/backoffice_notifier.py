#!/usr/bin/env python3
"""
backoffice_notifier.py — Notificações Telegram para backoffice AnteciPay
AnteciPay Cadence Skills v1.0
"""
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")


def send_handoff(lead: dict, notes: str = "") -> dict:
    """Envia notificação de handoff Stage 3 para backoffice"""
    value_str = f"R$ {lead.get('precatorio_value', 0):,.2f}" if lead.get('precatorio_value') else "A confirmar"
    
    message = f"""🔔 *HANDOFF AnteciPay — Stage 3*

👤 *Lead:* {lead.get('name', 'N/A')}
📱 *WhatsApp:* +{lead.get('phone', 'N/A')}
💰 *Precatório:* {value_str}
📋 *Processo:* {lead.get('precatorio_number', 'N/A')}
🏛️ *Tribunal:* {lead.get('tribunal', 'N/A')}
📊 *Tipo:* {lead.get('precatorio_type', 'N/A')}

📝 *Notas:* {notes or 'Lead qualificado e proposta apresentada.'}

⚡ *Ação necessária:* Iniciar processo de formalização
🔗 Stage: {lead.get('stage', '?')} | Status: {lead.get('status', 'active')}"""

    return _send_message(message, parse_mode="Markdown")


def send_alert(title: str, message: str, urgent: bool = False) -> dict:
    """Envia alerta genérico ao backoffice"""
    emoji = "🚨" if urgent else "📢"
    full_message = f"{emoji} *{title}*\n\n{message}"
    return _send_message(full_message, parse_mode="Markdown")


def send_daily_summary(stats: dict) -> dict:
    """Envia resumo diário de operações"""
    message = f"""📊 *AnteciPay — Resumo do Dia*

👥 Leads Ativos: {stats.get('total_active', 0)}
🆕 Stage 0 (Prospecção): {stats.get('stage_0', 0)}
📋 Stage 1 (Coleta): {stats.get('stage_1', 0)}
📄 Stage 2 (Proposta): {stats.get('stage_2', 0)}
🤝 Stage 3 (Fechamento): {stats.get('stage_3', 0)}
✅ Fechados hoje: {stats.get('closed_today', 0)}"""
    
    return _send_message(message, parse_mode="Markdown")


def _send_message(text: str, parse_mode: str = "Markdown") -> dict:
    if not BOT_TOKEN or not CHAT_ID:
        print(f"⚠️  Telegram não configurado. Mensagem:\n{text}")
        return {"ok": False, "error": "Not configured"}
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": parse_mode}
    resp = requests.post(url, json=payload)
    return resp.json()


if __name__ == "__main__":
    test_lead = {
        "name": "Maria Santos (TESTE)",
        "phone": "5511987654321",
        "precatorio_value": 180000.00,
        "precatorio_number": "0001234-56.2018.8.26.0001",
        "tribunal": "TJSP",
        "precatorio_type": "estadual",
        "stage": 3,
        "status": "active"
    }
    result = send_handoff(test_lead, "Lead chegou por indicação. Muito interessada.")
    print(json.dumps(result, indent=2))
