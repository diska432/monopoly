"""
FastAPI WebSocket server with lobby/room management and Supabase JWT auth.
"""
from __future__ import annotations
import hashlib
import json
import random
import string
from dataclasses import dataclass
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .config import FRONTEND_URL, SUPABASE_JWT_SECRET
from .auth import JWTBearer, verify_ws_token
from .engine.game_engine import GameEngine
from . import db

app = FastAPI(title="Monopoly Server")
FRONTEND_BUILD_DIR = Path(__file__).resolve().parents[1] / "frontend" / "build"

origins = [o.strip() for o in FRONTEND_URL.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jwt_scheme = JWTBearer()


class CreateLobbyRequest(BaseModel):
    max_players: int = Field(default=6, ge=2, le=6)
    casino: bool = False
    teams: bool = False
    timer: bool = False
    is_private: bool = False
    password: str = Field(default="", max_length=64)


class JoinLobbyRequest(BaseModel):
    password: str = Field(default="", max_length=64)


@dataclass
class LobbyRoom:
    lobby_id: str
    host_name: str
    name: str
    visibility: str
    password_hash: str | None
    max_players: int
    casino: bool
    teams: bool
    timer: bool
    game: GameEngine

    def to_summary(self) -> dict:
        return {
            "id": self.lobby_id,
            "name": self.name,
            "host_name": self.host_name,
            "visibility": self.visibility,
            "max_players": self.max_players,
            "casino": self.casino,
            "teams": self.teams,
            "timer": self.timer,
            "state": self.game.state,
            "player_count": len(self.game.players),
            "players": [p.name for p in self.game.players],
        }


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class ConnectionManager:
    def __init__(self):
        self.rooms: dict[str, LobbyRoom] = {}
        self.connections: dict[str, dict[str, WebSocket]] = {}

    def create_lobby(
        self,
        *,
        host_name: str,
        max_players: int = 6,
        casino: bool = False,
        teams: bool = False,
        timer: bool = False,
        is_private: bool = False,
        password: str = "",
    ) -> LobbyRoom:
        lobby_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        while lobby_id in self.rooms:
            lobby_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        room = LobbyRoom(
            lobby_id=lobby_id,
            host_name=host_name,
            name=f"{host_name.upper()}'S LOBBY",
            visibility="private" if is_private else "public",
            password_hash=_hash_password(password) if is_private and password else None,
            max_players=max_players,
            casino=casino,
            teams=teams,
            timer=timer,
            game=GameEngine(lobby_id),
        )
        room.game.characters = db.fetch_characters()
        self.rooms[lobby_id] = room
        self.connections[lobby_id] = {}
        return room

    def get_game(self, lobby_id: str) -> GameEngine | None:
        room = self.rooms.get(lobby_id)
        return room.game if room else None

    def get_room(self, lobby_id: str) -> LobbyRoom | None:
        return self.rooms.get(lobby_id)

    def list_rooms(self, visibility: str | None = None) -> list[dict]:
        rooms = []
        for room in self.rooms.values():
            if room.game.state != "lobby":
                continue
            if len(room.game.players) >= room.max_players:
                continue
            if visibility and room.visibility != visibility:
                continue
            rooms.append(room.to_summary())
        return rooms

    def can_join_room(self, room: LobbyRoom, password: str = "") -> tuple[bool, str | None]:
        if room.game.state != "lobby":
            return False, "Game already started."
        if len(room.game.players) >= room.max_players:
            return False, "Room is full."
        if room.visibility == "private":
            if not room.password_hash:
                return False, "Room password is not configured."
            if _hash_password(password or "") != room.password_hash:
                return False, "Incorrect password."
        return True, None

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


def _serialize_state(room: LobbyRoom) -> dict:
    state = room.game.get_full_state()
    state["room"] = room.to_summary()
    return state


# ---- Protected HTTP endpoints ----

@app.get("/api/me")
async def get_me(payload: dict = Depends(jwt_scheme)):
    return {
        "user_id": payload.get("sub"),
        "email": payload.get("email"),
        "display_name": _extract_display_name(payload),
    }


@app.post("/api/lobbies")
async def create_lobby(body: CreateLobbyRequest, payload: dict = Depends(jwt_scheme)):
    host_name = _extract_display_name(payload)
    if body.is_private and not body.password.strip():
        raise HTTPException(status_code=400, detail="Password is required for private rooms.")
    room = manager.create_lobby(
        host_name=host_name,
        max_players=body.max_players,
        casino=body.casino,
        teams=body.teams,
        timer=body.timer,
        is_private=body.is_private,
        password=body.password.strip(),
    )
    return {"room": room.to_summary()}


@app.get("/api/create-lobby")
async def create_lobby_legacy(payload: dict = Depends(jwt_scheme)):
    room = manager.create_lobby(host_name=_extract_display_name(payload))
    return {"lobby_id": room.lobby_id, "room": room.to_summary()}


@app.get("/api/lobbies")
async def list_lobbies(visibility: str | None = Query(default=None)):
    if visibility not in (None, "public", "private"):
        raise HTTPException(status_code=400, detail="Invalid visibility.")
    return {"rooms": manager.list_rooms(visibility)}


@app.post("/api/lobbies/{lobby_id}/join")
async def join_lobby(lobby_id: str, body: JoinLobbyRequest, payload: dict = Depends(jwt_scheme)):
    room = manager.get_room(lobby_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found.")
    can_join, reason = manager.can_join_room(room, body.password.strip())
    if not can_join:
        raise HTTPException(status_code=403, detail=reason or "Cannot join room.")
    return {"room": room.to_summary(), "player_name": _extract_display_name(payload)}


@app.get("/api/lobby/{lobby_id}/exists")
async def lobby_exists(lobby_id: str):
    room = manager.get_room(lobby_id)
    if room:
        return {"exists": True, "state": room.game.state, "players": [p.name for p in room.game.players]}
    return {"exists": False}


# ---- Save / Load Game Endpoints ----

class SaveGameRequest(BaseModel):
    room_id: str


class LoadGameRequest(BaseModel):
    saved_game_id: str


@app.post("/api/games/save")
async def save_game_endpoint(body: SaveGameRequest, payload: dict = Depends(jwt_scheme)):
    user_id = payload.get("sub", "")
    host_name = _extract_display_name(payload)
    room = manager.get_room(body.room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found.")
    if room.host_name != host_name:
        raise HTTPException(status_code=403, detail="Only the host can save the game.")
    if room.game.state not in ("active", "lobby"):
        raise HTTPException(status_code=400, detail="Cannot save a finished game.")

    game_state = room.game.to_save_dict()
    room_settings = {
        "max_players": room.max_players,
        "casino": room.casino,
        "teams": room.teams,
        "timer": room.timer,
        "visibility": room.visibility,
    }
    players = [
        {
            "player_name": p.name,
            "character_id": p.character_id,
            "balance": p.balance,
            "user_id": None,
        }
        for p in room.game.players
    ]
    turn_count = game_state.get("current_player_index", 0)

    saved = db.save_game(
        host_user_id=user_id,
        name=room.name,
        game_state=game_state,
        room_settings=room_settings,
        turn_count=turn_count,
        players=players,
    )
    if not saved:
        raise HTTPException(status_code=500, detail="Could not save game. Check database configuration.")
    return {"saved_game": saved}


@app.get("/api/games/saved")
async def list_saved_games_endpoint(payload: dict = Depends(jwt_scheme)):
    user_id = payload.get("sub", "")
    games = db.list_saved_games(user_id)
    return {"saved_games": games}


@app.post("/api/games/load")
async def load_game_endpoint(body: LoadGameRequest, payload: dict = Depends(jwt_scheme)):
    user_id = payload.get("sub", "")
    host_name = _extract_display_name(payload)
    saved = db.load_saved_game(body.saved_game_id)
    if not saved:
        raise HTTPException(status_code=404, detail="Saved game not found.")
    if saved.get("host_user_id") != user_id:
        raise HTTPException(status_code=403, detail="You are not the host of this saved game.")

    restored_engine = GameEngine.from_save_dict(saved["game_state"])
    restored_engine.characters = db.fetch_characters()
    restored_engine.state = "lobby"
    for p in restored_engine.players:
        p.ready = False

    room_settings = saved.get("room_settings", {})
    room = manager.create_lobby(
        host_name=host_name,
        max_players=room_settings.get("max_players", 6),
        casino=room_settings.get("casino", False),
        teams=room_settings.get("teams", False),
        timer=room_settings.get("timer", False),
        is_private=room_settings.get("visibility") == "private",
    )
    room.game = restored_engine
    restored_engine.lobby_id = room.lobby_id

    return {"room": room.to_summary()}


@app.delete("/api/games/{saved_game_id}")
async def delete_saved_game_endpoint(saved_game_id: str, payload: dict = Depends(jwt_scheme)):
    user_id = payload.get("sub", "")
    success = db.delete_saved_game(saved_game_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Saved game not found or not your game.")
    return {"deleted": True}


# ---- WebSocket with JWT auth ----

@app.websocket("/ws/{lobby_id}/{player_name}")
async def websocket_endpoint(
    websocket: WebSocket,
    lobby_id: str,
    player_name: str,
    token: str = Query(default=""),
    room_password: str = Query(default=""),
):
    await websocket.accept()

    if SUPABASE_JWT_SECRET:
        payload = await verify_ws_token(websocket, token)
        if not payload:
            await websocket.close(code=4001, reason="Authentication failed")
            return
        user_id = payload.get("sub", "")
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

    room = manager.get_room(lobby_id)
    if not room:
        await websocket.close(code=4004, reason="Lobby not found")
        return
    game = room.game

    existing_player = game._get_player(player_name)
    if not existing_player:
        can_join, reason = manager.can_join_room(room, room_password)
        if not can_join:
            await websocket.close(code=4005, reason=reason or "Cannot join room")
            return

    if payload:
        websocket._user_id = payload.get("sub", "")

    manager.add_connection(lobby_id, player_name, websocket)

    if game.state == "lobby" and not game._get_player(player_name):
        events = game.handle_action(player_name, "add_player", {"name": player_name})
        await manager.broadcast(lobby_id, {"type": "events", "events": events, "state": _serialize_state(room)})

    await websocket.send_json({"type": "full_state", "state": _serialize_state(room)})

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

            response = {"type": "events", "events": events, "state": _serialize_state(room)}
            await manager.broadcast(lobby_id, response)

    except WebSocketDisconnect:
        manager.remove_connection(lobby_id, player_name)
        await manager.broadcast(lobby_id, {
            "type": "player_disconnected",
            "player": player_name,
            "state": _serialize_state(room),
        })


if FRONTEND_BUILD_DIR.exists():
    static_dir = FRONTEND_BUILD_DIR / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=static_dir), name="frontend-static")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API route not found.")
        candidate = FRONTEND_BUILD_DIR / full_path
        if full_path and candidate.exists() and candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(FRONTEND_BUILD_DIR / "index.html")
