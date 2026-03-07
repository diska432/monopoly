# Monopoly KZ Edition — Browser Multiplayer

A real-time multiplayer Monopoly game with a Python (FastAPI) backend and React (TypeScript) frontend, connected via WebSockets.

## Architecture

```
backend/
  engine/           Pure game engine (zero I/O state machine)
    cells.py        Board cell type definitions
    board.py        40-cell board factory
    player.py       Player state dataclass
    rent_tables.py  Data-driven rent/upgrade tables
    game_engine.py  Core state machine — actions in, events out
  server.py         FastAPI WebSocket server with lobby management
  requirements.txt

frontend/           React + TypeScript SPA
  src/
    types/          TypeScript interfaces mirroring backend state
    hooks/          useGameSocket — WebSocket connection hook
    components/     Lobby, GameBoard, BoardCell, PlayerPanel, PlayersBar, EventLog
```

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
cd ..
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

1. Enter your name and click **Create Game**
2. Share the 6-character lobby code with friends
3. Other players enter the code and click **Join**
4. Once 2+ players are in the lobby, click **Start Game**
5. Take turns rolling dice, buying properties, upgrading, trading, and bankrupting opponents

## Features

- Real-time multiplayer via WebSockets (all players see updates instantly)
- Full Monopoly mechanics: buying, rent, color-set monopolies, star upgrades (1-5), mortgages, trading, jail, chance cards, casino
- Data-driven rent tables (no hardcoded values)
- Pure state-machine game engine (testable, framework-agnostic)
- Modern dark-themed UI with responsive board layout
