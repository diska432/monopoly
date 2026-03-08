# Monopoly KZ Edition — Browser Multiplayer

A real-time multiplayer Monopoly game with a Python (FastAPI) backend and React (TypeScript) frontend, connected via WebSockets. Authenticated via Supabase (email/password + Google SSO).

## Architecture

```
backend/
  engine/           Pure game engine (zero I/O state machine)
    cells.py        Board cell type definitions
    board.py        40-cell board factory
    player.py       Player state dataclass
    rent_tables.py  Data-driven rent/upgrade tables
    game_engine.py  Core state machine — actions in, events out
  auth.py           JWT verification for Supabase tokens
  config.py         Environment variable loading
  server.py         FastAPI WebSocket server with lobby management

frontend/           React + TypeScript SPA
  src/
    lib/supabase.ts Supabase client initialization
    types/          TypeScript interfaces mirroring backend state
    hooks/
      useAuth.tsx   Auth context (login, register, Google SSO, session)
      useGameSocket.ts  WebSocket connection hook (sends JWT)
    components/
      AuthScreen.tsx  Login / Register / Google sign-in UI
      Lobby, GameBoard, BoardCell, PlayerPanel, PlayersBar, EventLog
```

## Prerequisites

### 1. Supabase Project Setup

1. Create a project at [supabase.com](https://supabase.com)
2. Go to **Settings > API** and note:
   - `Project URL` (e.g. `https://xxxxx.supabase.co`)
   - `anon/public` key
   - `JWT Secret` (under **JWT Settings**)

### 2. Enable Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create an **OAuth 2.0 Client ID** (Web application)
3. Set **Authorized redirect URI** to: `https://<your-project>.supabase.co/auth/v1/callback`
4. In Supabase: **Authentication > Providers > Google** — enable it and paste your Google Client ID and Client Secret

### 3. Configure Environment Variables

Backend (`.env` in project root):
```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_JWT_SECRET=your-jwt-secret
FRONTEND_URL=http://localhost:3000
```

Frontend (`.env` in `frontend/`):
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
REACT_APP_SUPABASE_URL=https://xxxxx.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your-anon-key
```

## Quick Start

### Backend

```bash
pip install -r backend/requirements.txt
python -m uvicorn backend.server:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm start
```

Open http://localhost:3000 in your browser.

## How to Play

1. Sign in with email/password or Google
2. Click **Create Game** or enter a lobby code and click **Join**
3. Share the 6-character lobby code with friends
4. Once 2+ players are in the lobby, click **Start Game**
5. Take turns rolling dice, buying properties, upgrading, trading, and bankrupting opponents

## Features

- **Authentication**: Email/password registration + Google SSO via Supabase Auth
- Real-time multiplayer via WebSockets (all players see updates instantly)
- JWT-protected API endpoints and WebSocket connections
- Full Monopoly mechanics: buying, rent, color-set monopolies, star upgrades (1-5), mortgages, trading, jail, chance cards, casino, auctions
- Data-driven rent tables (no hardcoded values)
- Pure state-machine game engine (testable, framework-agnostic)
- Modern dark-themed UI with responsive board layout

## Database Notes

Supabase provides managed PostgreSQL. For connecting:
- **Supavisor pooler** (transaction mode, port 6543): supports IPv4 — recommended for most deployments
- **Direct connection** (port 5432): IPv6 only unless you have the IPv4 add-on
- For serverless/edge environments, always use the pooler connection string
