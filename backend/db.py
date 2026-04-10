"""
Supabase database client for persistence operations (save/load games, characters).
"""
from __future__ import annotations

from typing import Any
from supabase import create_client, Client

from .config import SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY

_client: Client | None = None


def get_client() -> Client | None:
    global _client
    if _client is not None:
        return _client
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        return None
    _client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    return _client


def fetch_characters() -> list[dict[str, Any]]:
    client = get_client()
    if not client:
        return _default_characters()
    try:
        resp = client.table("characters").select("*").order("display_order").execute()
        if resp.data:
            return resp.data
    except Exception:
        pass
    return _default_characters()


def save_game(
    host_user_id: str,
    name: str,
    game_state: dict,
    room_settings: dict,
    turn_count: int,
    players: list[dict],
) -> dict | None:
    client = get_client()
    if not client:
        return None
    resp = client.table("saved_games").insert({
        "host_user_id": host_user_id,
        "name": name,
        "game_state": game_state,
        "room_settings": room_settings,
        "turn_count": turn_count,
        "player_count": len(players),
    }).execute()
    if not resp.data:
        return None
    saved = resp.data[0]
    for p in players:
        client.table("saved_game_players").insert({
            "saved_game_id": saved["id"],
            "user_id": p.get("user_id"),
            "player_name": p["player_name"],
            "character_id": p.get("character_id"),
            "balance": p.get("balance", 0),
        }).execute()
    return saved


def list_saved_games(host_user_id: str) -> list[dict]:
    client = get_client()
    if not client:
        return []
    resp = (
        client.table("saved_games")
        .select("*, saved_game_players(*)")
        .eq("host_user_id", host_user_id)
        .order("updated_at", desc=True)
        .execute()
    )
    return resp.data or []


def load_saved_game(saved_game_id: str) -> dict | None:
    client = get_client()
    if not client:
        return None
    resp = (
        client.table("saved_games")
        .select("*, saved_game_players(*)")
        .eq("id", saved_game_id)
        .single()
        .execute()
    )
    return resp.data


def delete_saved_game(saved_game_id: str, host_user_id: str) -> bool:
    client = get_client()
    if not client:
        return False
    resp = (
        client.table("saved_games")
        .delete()
        .eq("id", saved_game_id)
        .eq("host_user_id", host_user_id)
        .execute()
    )
    return bool(resp.data)


def _default_characters() -> list[dict[str, Any]]:
    return [
        {"id": "rukia", "name": "Rukia", "era": "Feudal Japan", "avatar_url": "/assets/characters/rukia.svg", "trivia": "A wandering ronin from the Edo period.", "display_order": 1},
        {"id": "atlas", "name": "Atlas", "era": "Ancient Greece", "avatar_url": "/assets/characters/atlas.svg", "trivia": "A titan who holds a monopoly instead of the sky.", "display_order": 2},
        {"id": "ember", "name": "Ember", "era": "Stone Age", "avatar_url": "/assets/characters/ember.svg", "trivia": "The first to discover fire and charge for warmth.", "display_order": 3},
        {"id": "nova", "name": "Nova", "era": "Cyberpunk 2077", "avatar_url": "/assets/characters/nova.svg", "trivia": "A netrunner hacking her way to financial dominance.", "display_order": 4},
        {"id": "khan", "name": "Khan", "era": "Medieval Central Asia", "avatar_url": "/assets/characters/khan.svg", "trivia": "A steppe conqueror with an eye for property.", "display_order": 5},
        {"id": "raven", "name": "Raven", "era": "Victorian Era", "avatar_url": "/assets/characters/raven.svg", "trivia": "A mysterious aristocrat from fog-shrouded London.", "display_order": 6},
    ]
