#!/usr/bin/env python3
"""
whatsapp_sender.py — Envio de mensagens WhatsApp via Evolution API
AnteciPay Cadence Skills v1.0
"""
import requests
import json
import os
import base64
import argparse
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

EVOLUTION_BASE = os.getenv("EVOLUTION_URL", "https://evolution.montsam.site")
EVOLUTION_KEY = os.getenv("EVOLUTION_KEY", "")
INSTANCE_NAME = os.getenv("WHATSAPP_INSTANCE", "antecipay")


def get_headers():
    return {"apikey": EVOLUTION_KEY, "Content-Type": "application/json"}


def send_text(phone: str, message: str) -> dict:
    """Envia mensagem de texto. phone: '5511999999999'"""
    url = f"{EVOLUTION_BASE}/message/sendText/{INSTANCE_NAME}"
    payload = {"number": phone, "text": message}
    resp = requests.post(url, json=payload, headers=get_headers())
    return resp.json()


def send_document(phone: str, file_path: str, caption: str = "") -> dict:
    """Envia documento (PDF, etc) via base64"""
    url = f"{EVOLUTION_BASE}/message/sendMedia/{INSTANCE_NAME}"
    with open(file_path, "rb") as f:
        file_b64 = base64.b64encode(f.read()).decode()

    filename = Path(file_path).name
    ext = filename.rsplit(".", 1)[-1].lower()
    mimetypes = {"pdf": "application/pdf", "png": "image/png", "jpg": "image/jpeg"}
    mimetype = mimetypes.get(ext, "application/octet-stream")

    payload = {
        "number": phone,
        "mediatype": "document",
        "mimetype": mimetype,
        "caption": caption,
        "fileName": filename,
        "media": file_b64,
    }
    resp = requests.post(url, json=payload, headers=get_headers())
    return resp.json()


def send_image(phone: str, image_path: str, caption: str = "") -> dict:
    """Envia imagem"""
    url = f"{EVOLUTION_BASE}/message/sendMedia/{INSTANCE_NAME}"
    with open(image_path, "rb") as f:
        file_b64 = base64.b64encode(f.read()).decode()

    payload = {
        "number": phone,
        "mediatype": "image",
        "mimetype": "image/jpeg",
        "caption": caption,
        "media": file_b64,
    }
    resp = requests.post(url, json=payload, headers=get_headers())
    return resp.json()


def get_instance_status() -> dict:
    """Verifica status da instância WhatsApp"""
    url = f"{EVOLUTION_BASE}/instance/connectionState/{INSTANCE_NAME}"
    resp = requests.get(url, headers={"apikey": EVOLUTION_KEY})
    return resp.json()


def list_instances() -> list:
    """Lista todas as instâncias"""
    url = f"{EVOLUTION_BASE}/instance/fetchInstances"
    resp = requests.get(url, headers={"apikey": EVOLUTION_KEY})
    return resp.json()


def create_instance() -> dict:
    """Cria instância antecipay se não existir"""
    url = f"{EVOLUTION_BASE}/instance/create"
    payload = {
        "instanceName": INSTANCE_NAME,
        "qrcode": True,
        "integration": "WHATSAPP-BAILEYS",
    }
    resp = requests.post(url, json=payload, headers=get_headers())
    return resp.json()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AnteciPay WhatsApp Sender")
    subparsers = parser.add_subparsers(dest="command")

    # status
    subparsers.add_parser("status", help="Check instance status")

    # list
    subparsers.add_parser("list", help="List all instances")

    # send-text
    p_text = subparsers.add_parser("send-text", help="Send text message")
    p_text.add_argument("--phone", required=True)
    p_text.add_argument("--message", required=True)

    # send-doc
    p_doc = subparsers.add_parser("send-doc", help="Send document/PDF")
    p_doc.add_argument("--phone", required=True)
    p_doc.add_argument("--file", required=True)
    p_doc.add_argument("--caption", default="")

    args = parser.parse_args()

    if args.command == "status" or args.command is None:
        status = get_instance_status()
        print(f"WhatsApp Instance Status ({INSTANCE_NAME}):")
        print(json.dumps(status, indent=2))
    elif args.command == "list":
        instances = list_instances()
        print(json.dumps(instances, indent=2))
    elif args.command == "send-text":
        result = send_text(args.phone, args.message)
        print(json.dumps(result, indent=2))
    elif args.command == "send-doc":
        result = send_document(args.phone, args.file, args.caption)
        print(json.dumps(result, indent=2))
