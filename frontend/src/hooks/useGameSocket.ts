import { useCallback, useEffect, useRef, useState } from "react";
import { GameState, GameEvent, ServerMessage } from "../types/game";

const WS_BASE = process.env.REACT_APP_WS_URL || "ws://localhost:8000";

export function useGameSocket(lobbyId: string | null, playerName: string | null, token: string | null) {
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [events, setEvents] = useState<GameEvent[]>([]);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!lobbyId || !playerName) return;

    const tokenParam = token ? `?token=${encodeURIComponent(token)}` : "";
    const ws = new WebSocket(`${WS_BASE}/ws/${lobbyId}/${playerName}${tokenParam}`);
    wsRef.current = ws;

    ws.onopen = () => setConnected(true);

    ws.onmessage = (ev) => {
      const msg: ServerMessage = JSON.parse(ev.data);
      if (msg.state) setGameState(msg.state);
      if (msg.events) setEvents((prev) => [...prev, ...msg.events!]);
      if (msg.type === "player_disconnected" && msg.state) {
        setGameState(msg.state);
      }
    };

    ws.onclose = () => setConnected(false);
    ws.onerror = () => setConnected(false);

    return () => {
      ws.close();
      wsRef.current = null;
    };
  }, [lobbyId, playerName, token]);

  const sendAction = useCallback(
    (action: string, data: Record<string, any> = {}) => {
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({ action, data }));
      }
    },
    []
  );

  return { gameState, events, connected, sendAction };
}
