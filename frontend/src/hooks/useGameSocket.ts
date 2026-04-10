import { useCallback, useEffect, useRef, useState } from "react";
import { GameState, GameEvent, ServerMessage } from "../types/game";

const WS_BASE = process.env.REACT_APP_WS_URL || "ws://localhost:8000";

export type WsErrorKind =
  | "room_not_found"
  | "password_required"
  | "auth_failed"
  | "already_connected"
  | "connection_failed";

function closeCodeToError(code: number, reason: string): WsErrorKind | null {
  switch (code) {
    case 4001:
      return "auth_failed";
    case 4003:
      return "already_connected";
    case 4004:
      return "room_not_found";
    case 4005:
      return reason?.toLowerCase().includes("password")
        ? "password_required"
        : "connection_failed";
    default:
      return code >= 4000 ? "connection_failed" : null;
  }
}

export function useGameSocket(
  lobbyId: string | null,
  playerName: string | null,
  token: string | null,
  roomPassword: string | null = null
) {
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [events, setEvents] = useState<GameEvent[]>([]);
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState<WsErrorKind | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!lobbyId || !playerName) return;

    setError(null);

    const params = new URLSearchParams();
    if (token) params.set("token", token);
    if (roomPassword) params.set("room_password", roomPassword);
    const query = params.toString();
    const ws = new WebSocket(`${WS_BASE}/ws/${lobbyId}/${playerName}${query ? `?${query}` : ""}`);
    wsRef.current = ws;

    ws.onopen = () => {
      setConnected(true);
      setError(null);
    };

    ws.onmessage = (ev) => {
      const msg: ServerMessage = JSON.parse(ev.data);
      if (msg.state) setGameState(msg.state);
      if (msg.events) setEvents((prev) => [...prev, ...msg.events!]);
      if (msg.type === "player_disconnected" && msg.state) {
        setGameState(msg.state);
      }
    };

    ws.onclose = (ev) => {
      setConnected(false);
      const kind = closeCodeToError(ev.code, ev.reason);
      if (kind) setError(kind);
    };

    ws.onerror = () => {
      setConnected(false);
    };

    return () => {
      ws.close();
      wsRef.current = null;
    };
  }, [lobbyId, playerName, token, roomPassword]);

  const sendAction = useCallback(
    (action: string, data: Record<string, any> = {}) => {
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({ action, data }));
      }
    },
    []
  );

  return { gameState, events, connected, error, sendAction };
}
