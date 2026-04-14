#!/usr/bin/env python3
"""
lead_qualifier.py — Lógica de qualificação de leads Stage 0 e Stage 1
AnteciPay Cadence Skills v1.0
"""
from dataclasses import dataclass, field
from typing import Optional
import re


@dataclass
class LeadQualification:
    phone: str
    raw_response: str
    
    # Stage 0
    has_precatorio: Optional[bool] = None
    approximate_value: Optional[float] = None
    precatorio_type: Optional[str] = None
    
    # Stage 1
    full_name: Optional[str] = None
    cpf: Optional[str] = None
    process_number: Optional[str] = None
    tribunal: Optional[str] = None
    
    # Scoring
    qualification_score: int = 0
    disqualified: bool = False
    disqualification_reason: str = ""


def qualify_stage0(response: str, phone: str) -> LeadQualification:
    """Qualifica lead no Stage 0 baseado na resposta inicial"""
    q = LeadQualification(phone=phone, raw_response=response)
    text = response.lower()
    
    positive_signals = ['sim', 'tenho', 'possuo', 'tenho sim', 'claro', 'quero saber']
    negative_signals = ['não', 'nao', 'nunca', 'não tenho', 'nao tenho']
    
    if any(s in text for s in positive_signals):
        q.has_precatorio = True
        q.qualification_score += 30
    elif any(s in text for s in negative_signals):
        q.has_precatorio = False
        q.disqualified = True
        q.disqualification_reason = "Lead informou não ter precatório"
        return q
    
    value_match = re.search(r'R?\$?\s*(\d+[\.,]?\d*)\s*(mil|k|reais|milhão|milhao)?', text)
    if value_match:
        val_str = value_match.group(1).replace('.', '').replace(',', '.')
        try:
            val = float(val_str)
            multiplier = {'mil': 1000, 'k': 1000, 'milhão': 1000000, 'milhao': 1000000}.get(
                value_match.group(2), 1
            )
            q.approximate_value = val * multiplier
            if q.approximate_value >= 50000:
                q.qualification_score += 30
            elif q.approximate_value < 20000:
                q.qualification_score -= 20
        except ValueError:
            pass
    
    if 'federal' in text:
        q.precatorio_type = 'federal'
        q.qualification_score += 20
    elif 'estadual' in text or 'estado' in text:
        q.precatorio_type = 'estadual'
        q.qualification_score += 15
    elif 'municipal' in text or 'prefeitura' in text:
        q.precatorio_type = 'municipal'
        q.qualification_score += 10
    
    return q


def get_stage0_questions(q: LeadQualification) -> list:
    """Retorna próximas perguntas para Stage 0"""
    questions = []
    
    if q.has_precatorio is None:
        questions.append("Você possui um precatório? É uma dívida do governo reconhecida pelo tribunal.")
    
    if q.precatorio_type is None and q.has_precatorio:
        questions.append("Seu precatório é federal, estadual ou municipal?")
    
    if q.approximate_value is None and q.has_precatorio:
        questions.append("Qual é o valor aproximado do seu precatório?")
    
    return questions


def qualify_stage1(responses: dict, phone: str) -> LeadQualification:
    """Qualifica lead no Stage 1"""
    q = LeadQualification(phone=phone, raw_response=str(responses))
    q.has_precatorio = True
    
    if 'nome' in responses:
        q.full_name = responses['nome'].strip()
        q.qualification_score += 20
    
    if 'cpf' in responses:
        cpf_clean = re.sub(r'[^\d]', '', responses['cpf'])
        if len(cpf_clean) == 11:
            q.cpf = f"{cpf_clean[:3]}.{cpf_clean[3:6]}.{cpf_clean[6:9]}-{cpf_clean[9:]}"
            q.qualification_score += 20
    
    if 'processo' in responses:
        proc = responses['processo'].strip()
        if re.match(r'\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}', proc):
            q.process_number = proc
            q.qualification_score += 30
        else:
            q.process_number = proc
            q.qualification_score += 15
    
    if 'tribunal' in responses:
        q.tribunal = responses['tribunal'].upper().strip()
        q.qualification_score += 10
    
    return q


STAGE_MESSAGES = {
    "stage0_opener": "Olá! Somos da AnteciPay. Você possui um precatório?",
}


if __name__ == "__main__":
    test_response = "sim tenho um precatório estadual de uns 150 mil"
    q = qualify_stage0(test_response, "5511999999999")
    print(f"Has precatorio: {q.has_precatorio}")
    print(f"Type: {q.precatorio_type}")
    print(f"Value: {q.approximate_value}")
    print(f"Score: {q.qualification_score}")
