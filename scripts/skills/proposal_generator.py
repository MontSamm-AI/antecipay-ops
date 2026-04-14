#!/usr/bin/env python3
"""
proposal_generator.py — Gera proposta PDF para cessão de precatário
AnteciPay Cadence Skills v1.0
"""
import argparse
import json
import os
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

WORKSPACE_DIR = Path.home() / ".openclaw" / "workspace-antecipay"
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates" / "proposal"
OUTPUT_DIR = WORKSPACE_DIR / "artifacts" / "proposals"


def load_lead(lead_id: str) -> dict:
    leads_file = WORKSPACE_DIR / "state" / "leads.json"
    if leads_file.exists():
        with open(leads_file) as f:
            leads = json.load(f)
        return next((l for l in leads if str(l.get("id")) == lead_id or l.get("phone") == lead_id), {})
    return {}


def generate_proposal(lead: dict, value: float, rate: float, output_path: str = None) -> str:
    antecipated_value = value * rate
    discount = value - antecipated_value
    proposal_id = f"PROP-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    context = {
        "lead": lead,
        "precatorio_value": value,
        "antecipation_rate": rate,
        "antecipated_value": antecipated_value,
        "discount": discount,
        "proposal_date": datetime.now().strftime("%d/%m/%Y"),
        "proposal_id": proposal_id,
        "valid_until": "30 dias",
    }

    html_content = _basic_html(context)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    html_path = OUTPUT_DIR / f"{proposal_id}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    pdf_path = output_path or str(OUTPUT_DIR / f"{proposal_id}.pdf")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"file://{html_path}")
            page.pdf(path=pdf_path, format="A4", print_background=True)
            browser.close()
        print(f"✅ PDF gerado: {pdf_path}")
        return pdf_path
    except Exception as e:
        print(f"⚠️  Playwright não disponível ({e}). HTML salvo: {html_path}")
        return str(html_path)


def _basic_html(ctx: dict) -> str:
    lead_name = ctx['lead'].get('name', 'Prezado(a) cedente')
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Proposta AnteciPay {ctx['proposal_id']}</title>
<style>
  body {{ font-family: Arial, sans-serif; background: #f8f9fa; color: #333; }}
  .wrapper {{ max-width: 800px; margin: 0 auto; background: white; }}
  .header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; padding: 40px; }}
  .header h1 {{ font-size: 32px; letter-spacing: 3px; margin: 0; }}
  .content {{ padding: 40px; }}
  .section {{ margin: 30px 0; }}
  .section h2 {{ color: #e94560; border-bottom: 2px solid #e94560; padding-bottom: 8px; }}
  .values-box {{ background: #f8f9fa; border-radius: 8px; padding: 25px; border-left: 4px solid #e94560; }}
  .value-row {{ display: flex; justify-content: space-between; padding: 10px 0; }}
  .footer {{ background: #1a1a2e; color: #a0a0b8; padding: 25px 40px; font-size: 12px; }}
</style>
</head>
<body>
<div class="wrapper">
  <div class="header">
    <h1>ANTECIPAY</h1>
    <div>Antecipação de Precatórios — Liquidez Imediata</div>
  </div>
  <div class="content">
    <p>Olá, <strong>{lead_name}</strong>!</p>
    <p>Preparamos uma proposta exclusiva para a antecipação do seu precatório.</p>
    <div class="section">
      <h2>Sua Proposta de Antecipação</h2>
      <div class="values-box">
        <div class="value-row">
          <span>Valor total do precatório</span>
          <span>R$ {ctx['precatorio_value']:,.2f}</span>
        </div>
        <div class="value-row">
          <span>Taxa de antecipação</span>
          <span>{ctx['antecipation_rate']*100:.1f}%</span>
        </div>
        <div class="value-row">
          <span>Desconto</span>
          <span>R$ {ctx['discount']:,.2f}</span>
        </div>
        <div class="value-row" style="background: #1a1a2e; color: white; padding: 10px; border-radius: 4px;">
          <span><strong>VOCÊ RECEBE AGORA</strong></span>
          <span style="color: #e94560; font-size: 18px;"><strong>R$ {ctx['antecipated_value']:,.2f}</strong></span>
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <p>AnteciPay — Soluções em Antecipação de Precatórios</p>
    <p>Proposta {ctx['proposal_id']} | Válida por {ctx['valid_until']} | {ctx['proposal_date']}</p>
  </div>
</div>
</body>
</html>"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AnteciPay Proposal Generator")
    parser.add_argument("--lead-id", default="TEST")
    parser.add_argument("--value", type=float, required=True)
    parser.add_argument("--rate", type=float, default=0.72)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    if args.lead_id == "TEST":
        lead = {"id": "TEST", "name": "João da Silva", "phone": "5511999999999"}
    else:
        lead = load_lead(args.lead_id)
        if not lead:
            lead = {"id": args.lead_id, "name": "Cedente", "phone": args.lead_id}

    result = generate_proposal(lead, args.value, args.rate, args.output)
    print(f"Proposta: {result}")
