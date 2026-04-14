# WhatsApp Setup — Evolution API

## Overview

We use Evolution API v2 to send/receive WhatsApp messages via a dedicated business number.

## Instance Setup

### 1. Access Evolution API

- URL: https://evolution.montsam.site
- Auth: API key in header `apikey`

### 2. Create Instance (if not exists)

```bash
curl -X POST https://evolution.montsam.site/instance/create \
  -H "apikey: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "instanceName": "antecipay",
    "qrcode": true,
    "integration": "WHATSAPP-BAILEYS"
  }'
```

### 3. Connect WhatsApp (scan QR)

```bash
curl https://evolution.montsam.site/instance/connect/antecipay \
  -H "apikey: YOUR_KEY"
```

Response includes QR code URL — open in browser, scan with phone.

### 4. Check Status

```python
from scripts.skills.whatsapp_sender import get_instance_status
print(get_instance_status())
```

## Webhook (for inbound messages)

Configure n8n webhook to receive messages:
- Webhook URL: https://n8n.montsam.site/webhook/antecipay-inbound
- Events: MESSAGES_UPSERT

## Message Types

| Type | Use |
|------|-----|
| Text | Stage 0-2 conversations |
| Document (PDF) | Stage 2 proposals |
| Image | Document collection (Stage 3) |
| Template | Regulated outbound campaigns |
