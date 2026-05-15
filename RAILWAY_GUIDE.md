# 🚂 Deploying Retro Spot to Railway

This guide covers how to deploy your full-stack application to Railway using the configuration files provided.

---

## 1. Create a New Project
1. Log in to [Railway.app](https://railway.app/).
2. Click **+ New Project**.
3. Select **Deploy from GitHub repo**.
4. Choose your repository (`raaamooo/Retro-spot`).

## 2. Provision the Database
1. In your new project, click **+ Add Service**.
2. Select **Database** -> **Add PostgreSQL**.
3. Once created, Railway will automatically provide a `DATABASE_URL` environment variable.

## 3. Set Up the Backend Service
1. Click **+ Add Service** -> **GitHub Repo**.
2. Select your repository again.
3. Name this service `backend`.
4. Go to **Settings** -> **General**:
   - **Root Directory**: `backend`
5. Go to **Variables**:
   - Add `DATABASE_URL` (Reference the Postgres service: `${{Postgres.DATABASE_URL}}`).
   - Add `NODE_ENV`: `production`
   - Add `JWT_SECRET`: (A secure random string)
   - Add `FRONTEND_URL`: (The URL of your frontend service, e.g., `https://frontend-production-xxxx.up.railway.app`)
   - Add any other secrets (`INSTAPAY_PHONE`, `MOBILE_WALLET_PHONE`, etc.).

## 4. Set Up the Frontend Service
1. Click **+ Add Service** -> **GitHub Repo**.
2. Select your repository again.
3. Name this service `frontend`.
4. Go to **Settings** -> **General**:
   - **Root Directory**: `frontend`
5. Go to **Variables**:
   - Add `NEXT_PUBLIC_API_URL`: (The URL of your backend service, e.g., `https://backend-production-xxxx.up.railway.app`)
   - Add `NEXT_PUBLIC_SOCKET_URL`: (Same as above)
   - Add `NODE_ENV`: `production`

---

## 💡 Key Configurations Included
- **Auto-Migrations**: The `backend/railway.toml` automatically runs `prisma migrate deploy` and seeds the database on every build.
- **Watch Paths**: Changes in the `frontend/` folder only trigger a frontend rebuild, and changes in `backend/` only trigger a backend rebuild.
- **Nixpacks**: We use Railway's Nixpacks builder for high-performance builds.

## 🧪 Verification
Once both services are "Active" and "Healthy":
1. Visit the Frontend URL.
2. Check if the menu items load (this verifies Frontend -> Backend connection).
3. Try placing a test order to verify Database connectivity.
