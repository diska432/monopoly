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
        {"id": "edmund", "name": "Edmund", "era": "Medieval Britain", "avatar_url": "/assets/characters/edmund.png", "full_art_url": "/assets/characters/full/edmund-full.png", "trivia": "A cunning gentleman inventor who rose from the London fog to build an empire of steam and steel.", "display_order": 1},
        {"id": "sareena", "name": "Sareena", "era": "Central Asia", "avatar_url": "/assets/characters/sareena.png", "full_art_url": "/assets/characters/full/sareena-full.png", "trivia": "A fearless warrior-queen of the Silk Road, commanding trade routes from the steppes to the mountains.", "display_order": 2},
        {"id": "mei-lynn", "name": "Mei Lynn", "era": "Cyberpunk Japan", "avatar_url": "/assets/characters/mei-lynn.png", "full_art_url": "/assets/characters/full/mei-lynn-full.png", "trivia": "A netrunner and corporate saboteur who plays the market from the neon-lit streets of Neo-Tokyo.", "display_order": 3},
        {"id": "oleksiy", "name": "Oleksiy", "era": "Cossack Ukraine", "avatar_url": "/assets/characters/oleksiy.png", "full_art_url": "/assets/characters/full/oleksiy-full.png", "trivia": "A resourceful Cossack engineer who turns every challenge into an opportunity for profit.", "display_order": 4},
        {"id": "decimus", "name": "Decimus", "era": "Ancient Rome", "avatar_url": "/assets/characters/decimus.png", "full_art_url": "/assets/characters/full/decimus-full.png", "trivia": "A battle-hardened centurion who conquered lands and then bought them at auction.", "display_order": 5},
        {"id": "stacy", "name": "Stacy", "era": "80s America", "avatar_url": "/assets/characters/stacy.png", "full_art_url": "/assets/characters/full/stacy-full.png", "trivia": "A high-energy aerobics instructor who flipped properties between workout sessions.", "display_order": 6},
    ]
