# PDF Proposal Generation

## Overview

Proposals are generated as HTML (Jinja2 template) then printed to PDF using Playwright headless Chromium.

## Template

Location: `templates/proposal/proposal_template.html.j2`

Variables:
- `lead` — lead data dict
- `precatorio_value` — face value
- `antecipation_rate` — rate (0.72 = 72%)
- `antecipated_value` — what lead receives
- `discount` — difference
- `proposal_date` — date string
- `proposal_id` — unique ID
- `valid_until` — validity string

## Usage

```bash
# Generate proposal
python scripts/skills/proposal_generator.py \
  --lead-id PHONE_NUMBER \
  --value 150000 \
  --rate 0.72 \
  --output /tmp/proposal_test.pdf

# Send via WhatsApp
python scripts/skills/whatsapp_sender.py send-doc \
  --phone 5511999999999 \
  --file /tmp/proposal_test.pdf \
  --caption "Segue a proposta da AnteciPay para o seu precatório"
```

## Output Location

`~/.openclaw/workspace-antecipay/artifacts/proposals/PROP-YYYYMMDDHHMMSS.pdf`
