# Retro Spot — Full-Stack Platform

A premium neo-retro cafe and workspace management platform built with Next.js, Node.js, Prisma, and PostgreSQL.

## Features
- **Real-Time Dashboards**: Separate tablet-optimized interfaces for Barista, Waiter, Cashier, Inventory, and Manager.
- **Dynamic Menu**: Real-time availability synchronization based on live inventory levels.
- **Booking System**: Event and workspace bookings with automated payment verification (Instapay/Mobile Wallet).
- **Art Platform**: Weekly bidding for local artists' work.
- **Localization**: Full English and Arabic (RTL) support.
- **Responsive Design**: Mobile-first customer experience with premium animations.

---

## 🛠 Deployment Guide (Render)

This project is optimized for deployment on **Render**.

### 1. Database Setup
1. Create a **PostgreSQL** database on Render.
2. Copy the **Internal Database URL**.

### 2. Backend Deployment (Web Service)
1. Create a new **Web Service** on Render.
2. Point it to your repository.
3. **Root Directory**: `backend`
4. **Build Command**: `npm run render-build`
5. **Start Command**: `npm start`
6. **Environment Variables**:
   - `DATABASE_URL`: (Paste your PostgreSQL URL)
   - `FRONTEND_URL`: (The URL of your frontend static site once deployed)
   - `JWT_SECRET`: (Generate a secure random string)
   - `NODE_ENV`: `production`
   - `INSTAPAY_PHONE`: Your Instapay number
   - `MOBILE_WALLET_PHONE`: Your Vodafone Cash/Mobile Wallet number
   - `MAP_EMBED_URL`: Your Google Maps embed URL

### 3. Frontend Deployment (Static Site)
1. Create a new **Static Site** on Render.
2. Point it to your repository.
3. **Root Directory**: `frontend`
4. **Build Command**: `npm run build`
5. **Publish Directory**: `out` (if using Static Export) or `.next` (if using Web Service)
   - *Note: If you want real-time features on a static site, ensure the backend URL is set correctly.*
6. **Environment Variables**:
   - `NEXT_PUBLIC_API_URL`: (The URL of your deployed backend)

---

## 🚀 Local Development

### Prerequisites
- Node.js 18+
- PostgreSQL (or use SQLite for local testing by changing `provider` in `prisma/schema.prisma`)

### Backend
```bash
cd backend
npm install
npx prisma migrate dev
npm run dev
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 📂 Project Structure
- `/backend`: Express.js API, Prisma ORM, Socket.IO.
- `/frontend`: Next.js (App Router), Tailwind CSS, Framer Motion.
- `/prisma`: Database schema and seed data.

## 📄 License
Private / Proprietary.
