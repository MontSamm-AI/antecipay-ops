#!/bin/bash
# AnteciPay — Install Script
# Run in WSL Ubuntu

set -e

echo "🚀 AnteciPay Setup"
echo "=================="

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt --break-system-packages 2>/dev/null || pip install -r requirements.txt

echo "🎭 Installing Playwright Chromium..."
python -m playwright install chromium 2>/dev/null || echo "⚠️  Playwright install may require: playwright install-deps"

WORKSPACE="$HOME/.openclaw/workspace-antecipay"
echo "📁 Creating workspace: $WORKSPACE"
mkdir -p "$WORKSPACE/state"
mkdir -p "$WORKSPACE/artifacts/proposals"
mkdir -p "$WORKSPACE/logs"
mkdir -p "$WORKSPACE/templates/proposal"
mkdir -p "$WORKSPACE/templates/messages"

if [ ! -f "$WORKSPACE/MEMORY.md" ]; then
    cp system/config/workspace-antecipay-template/MEMORY.md "$WORKSPACE/"
    echo "✅ MEMORY.md copied"
fi

if [ ! -f "$WORKSPACE/TOOLS.md" ]; then
    cp system/config/workspace-antecipay-template/TOOLS.md "$WORKSPACE/"
    echo "✅ TOOLS.md copied"
fi

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "📝 .env created — EDIT WITH YOUR API KEYS"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your API keys"
echo "2. Run: python scripts/skills/whatsapp_sender.py status"
echo "3. Run: python scripts/skills/database_manager.py init"
echo "4. Run: python scripts/skills/proposal_generator.py --value 150000 --rate 0.72"
