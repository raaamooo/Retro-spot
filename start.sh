#!/usr/bin/env bash
# start.sh — Build and launch Retro Spot on this machine.
# Run once: bash start.sh
# After that use: pm2 restart all

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "╔══════════════════════════════════════╗"
echo "║     Retro Spot — Production Start    ║"
echo "╚══════════════════════════════════════╝"
echo ""

# ── Create log directory ──────────────────────────────────────────
mkdir -p logs

# ── Ensure PM2 is installed ────────────────────────────────────────
export PATH="$HOME/.local/bin:$PATH"
if ! command -v pm2 &>/dev/null; then
  echo "📦 Installing PM2 locally..."
  npm install -g pm2 --prefix ~/.local
fi

# ── Backend ────────────────────────────────────────────────────────
echo "🔧 Building backend..."
cd backend
npm install --silent
npx tsx prisma/seed-inventory.ts 2>/dev/null || true   # seed if not already seeded
npm run build
cd ..

# ── Frontend ───────────────────────────────────────────────────────
echo "🎨 Building frontend..."
cd frontend
npm install --silent
npm run build

# Copy public assets into standalone output (required for standalone mode)
cp -r public .next/standalone/public 2>/dev/null || true
cp -r .next/static .next/standalone/.next/static 2>/dev/null || true
cd ..

# ── Start with PM2 ────────────────────────────────────────────────
echo "🚀 Starting services with PM2..."
pm2 delete retro-backend  2>/dev/null || true
pm2 delete retro-frontend 2>/dev/null || true
pm2 start ecosystem.config.js

# ── Show status ───────────────────────────────────────────────────
echo ""
pm2 list
echo ""
echo "✅ Retro Spot is live!"
echo ""
echo "   Frontend  →  http://192.168.41.9:3000"
echo "   Backend   →  http://192.168.41.9:5000"
echo "   Admin     →  http://192.168.41.9:3000/admin/barista"
echo ""
echo "💡 To keep services running after reboot:"
echo "   pm2 save && pm2 startup"
echo ""
echo "📋 Useful commands:"
echo "   pm2 logs          — live logs"
echo "   pm2 restart all   — restart both"
echo "   pm2 stop all      — stop both"
