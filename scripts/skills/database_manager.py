#!/usr/bin/env python3
"""
database_manager.py — Gerenciamento de leads e operações AnteciPay no Postgres
AnteciPay Cadence Skills v1.0
"""
import os
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URL = os.getenv("ANTECIPAY_DB_URL", "")
LOCAL_LEADS_FILE = Path.home() / ".openclaw" / "workspace-antecipay" / "state" / "leads.json"


def get_conn():
    import psycopg2
    if not POSTGRES_URL:
        raise ValueError("ANTECIPAY_DB_URL not set in environment")
    return psycopg2.connect(POSTGRES_URL)


def init_schema():
    """Cria schema inicial se não existir"""
    sql = """
    CREATE TABLE IF NOT EXISTS leads (
        id SERIAL PRIMARY KEY,
        phone VARCHAR(20) UNIQUE NOT NULL,
        name VARCHAR(200),
        cpf VARCHAR(14),
        stage INTEGER DEFAULT 0,
        precatorio_number VARCHAR(100),
        precatorio_value DECIMAL(15,2),
        precatorio_type VARCHAR(20),
        tribunal VARCHAR(100),
        status VARCHAR(50) DEFAULT 'active',
        notes TEXT,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS interactions (
        id SERIAL PRIMARY KEY,
        lead_id INTEGER REFERENCES leads(id),
        channel VARCHAR(50),
        direction VARCHAR(10),
        message TEXT,
        timestamp TIMESTAMP DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS proposals (
        id SERIAL PRIMARY KEY,
        lead_id INTEGER REFERENCES leads(id),
        proposal_id VARCHAR(50) UNIQUE,
        precatorio_value DECIMAL(15,2),
        rate DECIMAL(5,4),
        antecipated_value DECIMAL(15,2),
        status VARCHAR(50) DEFAULT 'pending',
        pdf_path VARCHAR(500),
        created_at TIMESTAMP DEFAULT NOW()
    );
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
    print("✅ Schema inicializado com sucesso")


def upsert_lead(phone: str, **kwargs) -> dict:
    """Cria ou atualiza lead. Retorna dados do lead."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO leads (phone) VALUES (%s) ON CONFLICT (phone) DO UPDATE SET updated_at = NOW() RETURNING id",
                (phone,)
            )
            lead_id = cur.fetchone()[0]
            if kwargs:
                kwargs['updated_at'] = datetime.now()
                valid_cols = ['name', 'cpf', 'stage', 'precatorio_number', 'precatorio_value',
                              'precatorio_type', 'tribunal', 'status', 'notes', 'updated_at']
                filtered = {k: v for k, v in kwargs.items() if k in valid_cols}
                if filtered:
                    set_clause = ", ".join(f"{k} = %s" for k in filtered)
                    cur.execute(f"UPDATE leads SET {set_clause} WHERE id = %s",
                               list(filtered.values()) + [lead_id])
    _sync_to_local()
    return get_lead(phone)


def get_lead(phone: str) -> dict:
    """Busca lead pelo número de telefone"""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM leads WHERE phone = %s", (phone,))
            row = cur.fetchone()
            if row:
                cols = [d[0] for d in cur.description]
                return dict(zip(cols, row))
    return {}


def advance_stage(phone: str) -> dict:
    """Avança o lead para o próximo stage"""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE leads SET stage = stage + 1, updated_at = NOW() WHERE phone = %s RETURNING stage",
                (phone,)
            )
            result = cur.fetchone()
            new_stage = result[0] if result else -1
    print(f"📈 Lead {phone} → Stage {new_stage}")
    _sync_to_local()
    return get_lead(phone)


def list_leads(stage: int = None, status: str = 'active') -> list:
    """Lista leads, opcionalmente filtrado por stage"""
    with get_conn() as conn:
        with conn.cursor() as cur:
            if stage is not None:
                cur.execute("SELECT * FROM leads WHERE stage = %s AND status = %s ORDER BY updated_at DESC", (stage, status))
            else:
                cur.execute("SELECT * FROM leads WHERE status = %s ORDER BY updated_at DESC", (status,))
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]


def log_interaction(phone: str, channel: str, direction: str, message: str):
    """Registra interação com lead"""
    lead = get_lead(phone)
    if not lead:
        return
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO interactions (lead_id, channel, direction, message) VALUES (%s, %s, %s, %s)",
                (lead['id'], channel, direction, message)
            )


def _sync_to_local():
    """Sincroniza leads do Postgres para JSON local (fallback para agente)"""
    try:
        leads = list_leads(status=None)
        LOCAL_LEADS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOCAL_LEADS_FILE, "w") as f:
            json.dump(leads, f, indent=2, default=str)
    except Exception as e:
        print(f"⚠️  Sync local falhou: {e}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        print("Inicializando schema AnteciPay...")
        init_schema()
    else:
        print("Testando conexão...")
        try:
            with get_conn() as conn:
                print(f"✅ Conexão OK: {POSTGRES_URL[:40]}...")
        except Exception as e:
            print(f"❌ Erro: {e}")
