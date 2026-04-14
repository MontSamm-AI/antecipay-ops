#!/usr/bin/env python3
"""
browser_research.py — Pesquisa de precatórios via browser CDP
AnteciPay Cadence Skills v1.0
"""
import requests
import json
import time
import os


CDP_HOST = os.getenv("CDP_HOST", "localhost")
CDP_PORT = int(os.getenv("CDP_PORT", "9222"))


def get_tabs() -> list:
    resp = requests.get(f"http://{CDP_HOST}:{CDP_PORT}/json")
    return resp.json()


def navigate_and_get_text(url: str, wait_seconds: int = 3) -> str:
    """Navega para URL e retorna texto da página"""
    tabs = get_tabs()
    if not tabs:
        return "No browser tabs available"
    
    tab_id = tabs[0]["id"]
    ws_url = tabs[0]["webSocketDebuggerUrl"]
    
    import websocket
    ws = websocket.create_connection(ws_url)
    
    ws.send(json.dumps({"id": 1, "method": "Page.navigate", "params": {"url": url}}))
    time.sleep(wait_seconds)
    
    ws.send(json.dumps({
        "id": 2,
        "method": "Runtime.evaluate",
        "params": {"expression": "document.body.innerText"}
    }))
    result = json.loads(ws.recv())
    ws.close()
    
    return result.get("result", {}).get("result", {}).get("value", "")


def search_cnj(process_number: str) -> str:
    """Pesquisa processo no CNJ"""
    url = f"https://www.cnj.jus.br/busca/?q={process_number}"
    return navigate_and_get_text(url)


def search_tjsp(process_number: str) -> str:
    """Pesquisa processo no TJSP"""
    url = f"https://esaj.tjsp.jus.br/cpopg/search.do?conversationId=&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado=&foroNumeroUnificado=&dadosConsulta.valorConsultaNuUnificado={process_number}"
    return navigate_and_get_text(url)


def research_precatorio(process_number: str, tribunal: str = "") -> dict:
    """Pesquisa abrangente sobre um precatório"""
    results = {
        "process_number": process_number,
        "tribunal": tribunal,
        "searches": []
    }
    
    try:
        cnj_result = search_cnj(process_number)
        results["searches"].append({
            "source": "CNJ",
            "text_preview": cnj_result[:500] if cnj_result else "No result"
        })
    except Exception as e:
        results["searches"].append({"source": "CNJ", "error": str(e)})
    
    if "tjsp" in tribunal.lower():
        try:
            tjsp_result = search_tjsp(process_number)
            results["searches"].append({
                "source": "TJSP",
                "text_preview": tjsp_result[:500] if tjsp_result else "No result"
            })
        except Exception as e:
            results["searches"].append({"source": "TJSP", "error": str(e)})
    
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--process", required=True)
    parser.add_argument("--tribunal", default="")
    args = parser.parse_args()
    
    result = research_precatorio(args.process, args.tribunal)
    print(json.dumps(result, indent=2, ensure_ascii=False))
