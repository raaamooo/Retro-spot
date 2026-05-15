#!/usr/bin/env bash
# stop.sh — Gracefully stop all Retro Spot services.

echo "🛑 Stopping Retro Spot services..."
pm2 stop retro-backend retro-frontend 2>/dev/null || pm2 stop all 2>/dev/null || true
echo "✅ Services stopped. Run 'bash start.sh' to restart."
