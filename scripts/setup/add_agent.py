#!/usr/bin/env python3
import json
import sys
from pathlib import Path

openclaw_path = Path.home() / '.openclaw' / 'openclaw.json'

with open(openclaw_path) as f:
    config = json.load(f)

new_agent = {
    'id': 'cadence-antecipay',
    'displayName': 'Cadence AnteciPay',
    'workspace': '/home/monts/.openclaw/workspace-antecipay',
    'model': 'openai-codex/gpt-5.4',
    'channels': ['whatsapp', 'telegram'],
    'description': 'Agente de prospecção e qualificação de cessão de precatórios — Stages 0-3',
    'identity': {
        'name': 'AnteciPay',
        'theme': 'ocean',
        'emoji': '💰'
    },
    'tools': {
        'profile': 'full',
        'alsoAllow': ['browser', 'canvas', 'message', 'gateway', 'nodes', 'agents_list', 'tts']
    }
}

agent_ids = [a['id'] for a in config['agents']['list']]
if 'cadence-antecipay' not in agent_ids:
    config['agents']['list'].append(new_agent)
    with open(openclaw_path, 'w') as f:
        json.dump(config, f, indent=2)
    print('Agent cadence-antecipay added to openclaw.json')
    sys.exit(0)
else:
    print('Agent cadence-antecipay already exists')
    sys.exit(0)
