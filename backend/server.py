"""
FastAPI WebSocket server with lobby/room management and Supabase JWT auth.
"""
from __future__ import annotations
import json
import random
import string
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Query
from fastapi.middleware.cors import CORSMiddleware

from .config import FRONTEND_URL, SUPABASE_JWT_SECRET
from .auth import JWTBearer, verify_token, verify_ws_token
from .engine.game_engine import GameEngine

app = FastAPI(title="Monopoly Server")

origins = [o.strip() for o in FRONTEND_URL.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jwt_scheme = JWTBearer()


class ConnectionManager:
    def __init__(self):
        self.games: dict[str, GameEngine] = {}
        self.connections: dict[str, dict[str, WebSocket]] = {}

    def create_lobby(self) -> str:
        lobby_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        while lobby_id in self.games:
            lobby_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.games[lobby_id] = GameEngine(lobby_id)
        self.connections[lobby_id] = {}
        return lobby_id

    def get_game(self, lobby_id: str) -> GameEngine | None:
        return self.games.get(lobby_id)

    def add_connection(self, lobby_id: str, player_name: str, ws: WebSocket):
        if lobby_id not in self.connections:
            self.connections[lobby_id] = {}
        self.connections[lobby_id][player_name] = ws

    def remove_connection(self, lobby_id: str, player_name: str):
        if lobby_id in self.connections:
            self.connections[lobby_id].pop(player_name, None)

    async def broadcast(self, lobby_id: str, message: dict):
        conns = self.connections.get(lobby_id, {})
        dead = []
        for name, ws in conns.items():
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(name)
        for name in dead:
            conns.pop(name, None)

    async def send_to(self, lobby_id: str, player_name: str, message: dict):
        ws = self.connections.get(lobby_id, {}).get(player_name)
        if ws:
            try:
                await ws.send_json(message)
            except Exception:
                pass


manager = ConnectionManager()


def _extract_display_name(payload: dict) -> str:
    """Get a display name from the JWT payload's user_metadata or email."""
    meta = payload.get("user_metadata", {})
    name = meta.get("full_name") or meta.get("name") or ""
    if name:
        return name
    email = payload.get("email", "")
    if email:
        return email.split("@")[0]
    return payload.get("sub", "Player")[:16]


# ---- Protected HTTP endpoints ----

@app.get("/api/me")
async def get_me(payload: dict = Depends(jwt_scheme)):
    return {
        "user_id": payload.get("sub"),
        "email": payload.get("email"),
        "display_name": _extract_display_name(payload),
    }


@app.get("/api/create-lobby")
async def create_lobby(payload: dict = Depends(jwt_scheme)):
    lobby_id = manager.create_lobby()
    return {"lobby_id": lobby_id}


@app.get("/api/lobby/{lobby_id}/exists")
async def lobby_exists(lobby_id: str):
    game = manager.get_game(lobby_id)
    if game:
        return {"exists": True, "state": game.state, "players": [p.name for p in game.players]}
    return {"exists": False}


# ---- WebSocket with JWT auth ----

@app.websocket("/ws/{lobby_id}/{player_name}")
async def websocket_endpoint(
    websocket: WebSocket,
    lobby_id: str,
    player_name: str,
    token: str = Query(default=""),
):
    if SUPABASE_JWT_SECRET:
        payload = await verify_ws_token(websocket, token)
        if not payload:
            await websocket.close(code=4001, reason="Authentication failed")
            return
        user_id = payload.get("sub", "")
        existing_conn_name = None
        conns = manager.connections.get(lobby_id, {})
        game = manager.get_game(lobby_id)
        if game:
            for p in game.players:
                ws_for_p = conns.get(p.name)
                if ws_for_p and hasattr(ws_for_p, '_user_id') and ws_for_p._user_id == user_id and p.name != player_name:
                    await websocket.close(code=4003, reason="Already connected with a different name")
                    return
    else:
        payload = None

    game = manager.get_game(lobby_id)
    if not game:
        await websocket.close(code=4004, reason="Lobby not found")
        return

    await websocket.accept()

    if payload:
        websocket._user_id = payload.get("sub", "")

    manager.add_connection(lobby_id, player_name, websocket)

    if game.state == "lobby" and not game._get_player(player_name):
        events = game.handle_action(player_name, "add_player", {"name": player_name})
        await manager.broadcast(lobby_id, {"type": "events", "events": events, "state": game.get_full_state()})

    await websocket.send_json({"type": "full_state", "state": game.get_full_state()})

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                await websocket.send_json({"type": "error", "message": "Invalid JSON"})
                continue

            action = msg.get("action", "")
            data = msg.get("data", {})
            events = game.handle_action(player_name, action, data)

            response = {"type": "events", "events": events, "state": game.get_full_state()}
            await manager.broadcast(lobby_id, response)

    except WebSocketDisconnect:
        manager.remove_connection(lobby_id, player_name)
        await manager.broadcast(lobby_id, {
            "type": "player_disconnected",
            "player": player_name,
            "state": game.get_full_state(),
        })
