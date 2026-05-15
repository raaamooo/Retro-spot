#!/bin/bash
# deploy.sh — Build and restart the full Retro Spot stack
set -e

echo "🔨 Building backend..."
cd backend
npm run build
cd ..

echo "🔨 Building frontend..."
cd frontend
npm run build

echo "📦 Copying static assets to standalone..."
cp -r .next/static .next/standalone/.next/static
cp -r public .next/standalone/public
cd ..

echo "🚀 Restarting PM2 processes..."
pm2 restart all

echo "✅ Deploy complete!"
pm2 status
