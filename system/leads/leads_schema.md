# AnteciPay — Lead Data Schema

## leads table

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Internal ID |
| phone | VARCHAR(20) | WhatsApp number (5511999999999) |
| name | VARCHAR(200) | Full name |
| cpf | VARCHAR(14) | Brazilian tax ID |
| stage | INTEGER | Current stage (0-3) |
| precatorio_number | VARCHAR(100) | Process number |
| precatorio_value | DECIMAL(15,2) | Face value R$ |
| precatorio_type | VARCHAR(20) | federal/estadual/municipal |
| tribunal | VARCHAR(100) | Issuing court |
| status | VARCHAR(50) | active/paused/closed/lost |
| notes | TEXT | Agent notes |
| created_at | TIMESTAMP | First contact |
| updated_at | TIMESTAMP | Last update |

## interactions table

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Internal ID |
| lead_id | INTEGER | FK to leads |
| channel | VARCHAR(50) | whatsapp/telegram |
| direction | VARCHAR(10) | inbound/outbound |
| message | TEXT | Message content |
| timestamp | TIMESTAMP | When sent/received |

## proposals table

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Internal ID |
| lead_id | INTEGER | FK to leads |
| proposal_id | VARCHAR(50) | PROP-YYYYMMDDHHMMSS |
| precatorio_value | DECIMAL(15,2) | Face value |
| rate | DECIMAL(5,4) | Rate (0.7200 = 72%) |
| antecipated_value | DECIMAL(15,2) | What lead receives |
| status | VARCHAR(50) | pending/accepted/rejected |
| pdf_path | VARCHAR(500) | Path to PDF file |
| created_at | TIMESTAMP | Proposal date |
