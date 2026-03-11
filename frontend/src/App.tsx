import React, { useCallback, useEffect, useState } from "react";
import { AuthProvider, useAuth } from "./hooks/useAuth";
import { useGameSocket } from "./hooks/useGameSocket";
import AuthScreen from "./components/AuthScreen";
import MainMenu from "./components/MainMenu";
import HostJoinScreen from "./components/HostJoinScreen";
import NewLobbyScreen from "./components/NewLobbyScreen";
import { LobbySettings } from "./components/NewLobbyScreen";
import JoinLobbyScreen from "./components/JoinLobbyScreen";
import Lobby from "./components/Lobby";
import GameBoard from "./components/GameBoard";
import PlayerPanel from "./components/PlayerPanel";
import PlayersBar from "./components/PlayersBar";
import EventLog from "./components/EventLog";
import { RoomInfo } from "./types/game";
import "./App.css";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

type Screen = "main-menu" | "host-join" | "new-lobby" | "join-lobby" | "game";

function GameApp() {
  const { user, session, displayName, signOut, getAccessToken, loading } = useAuth();
  const [screen, setScreen] = useState<Screen>("main-menu");
  const [lobbyId, setLobbyId] = useState<string | null>(null);
  const [playerName, setPlayerName] = useState<string>("");
  const [roomPassword, setRoomPassword] = useState<string>("");
  const [rooms, setRooms] = useState<RoomInfo[]>([]);
  const [error, setError] = useState("");
  const [creating, setCreating] = useState(false);
  const [joining, setJoining] = useState(false);

  const token = session?.access_token ?? null;
  const { gameState, events, connected, sendAction } = useGameSocket(lobbyId, playerName, token, roomPassword);

  const fetchRooms = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/api/lobbies`);
      const data = await res.json();
      setRooms(data.rooms ?? []);
    } catch {
      setError("Could not load rooms.");
    }
  }, []);

  useEffect(() => {
    if (screen === "join-lobby" && user) {
      fetchRooms();
    }
  }, [screen, user, fetchRooms]);

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner" />
        <p>Loading...</p>
      </div>
    );
  }

  if (!user) {
    return <AuthScreen />;
  }

  const goBack = (to: Screen) => {
    setError("");
    setScreen(to);
  };

  const handleCreateLobby = async (settings: LobbySettings) => {
    setCreating(true);
    setError("");
    try {
      const freshToken = await getAccessToken();
      if (!freshToken) {
        setError("Session expired. Please sign in again.");
        setCreating(false);
        return;
      }
      const res = await fetch(`${API_BASE}/api/lobbies`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${freshToken}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          max_players: settings.maxPlayers,
          casino: settings.casino,
          teams: settings.teams,
          timer: settings.timer,
          is_private: settings.isPrivate,
          password: settings.password,
        }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail || "Could not create room.");
        setCreating(false);
        return;
      }
      setPlayerName(displayName);
      setRoomPassword(settings.isPrivate ? settings.password : "");
      setLobbyId(data.room.id);
      setScreen("game");
    } catch {
      setError("Could not connect to server.");
    }
    setCreating(false);
  };

  const handleJoinLobby = async (room: RoomInfo, password = "") => {
    setJoining(true);
    setError("");
    try {
      const freshToken = await getAccessToken();
      if (!freshToken) {
        setError("Session expired. Please sign in again.");
        setJoining(false);
        return;
      }
      const res = await fetch(`${API_BASE}/api/lobbies/${room.id}/join`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${freshToken}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ password }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail || "Could not join room.");
        setJoining(false);
        return;
      }
      setPlayerName(data.player_name || displayName);
      setRoomPassword(password);
      setLobbyId(room.id);
      setScreen("game");
    } catch {
      setError("Could not connect to server.");
    }
    setJoining(false);
  };

  if (screen === "main-menu") {
    return (
      <MainMenu
        displayName={displayName}
        onStartGame={() => { setError(""); setScreen("host-join"); }}
        onLeave={signOut}
      />
    );
  }

  if (screen === "host-join") {
    return (
      <HostJoinScreen
        onHost={() => { setError(""); setScreen("new-lobby"); }}
        onJoin={() => { setError(""); setScreen("join-lobby"); }}
        onBack={() => goBack("main-menu")}
      />
    );
  }

  if (screen === "new-lobby") {
    return (
      <NewLobbyScreen
        onCreateLobby={handleCreateLobby}
        onBack={() => goBack("host-join")}
        error={error}
        creating={creating}
      />
    );
  }

  if (screen === "join-lobby") {
    return (
      <JoinLobbyScreen
        rooms={rooms}
        onJoin={handleJoinLobby}
        onRefresh={fetchRooms}
        onBack={() => goBack("host-join")}
        error={error}
        joining={joining}
      />
    );
  }

  // screen === "game"
  if (!gameState) {
    return (
      <div className="loading-screen">
        <div className="spinner" />
        <p>{connected ? "Loading game..." : "Connecting..."}</p>
      </div>
    );
  }

  if (gameState.state === "lobby") {
    return <Lobby gameState={gameState} playerName={playerName} sendAction={sendAction} />;
  }

  return (
    <div className="game-screen">
      <PlayersBar gameState={gameState} playerName={playerName} />
      <div className="game-main">
        <GameBoard gameState={gameState} />
        <div className="game-sidebar">
          <PlayerPanel gameState={gameState} playerName={playerName} sendAction={sendAction} />
          <EventLog events={events} />
        </div>
      </div>
      {gameState.state === "gameover" && (
        <div className="gameover-overlay">
          <div className="gameover-card">
            <h2>Game Over!</h2>
            <p>Winner: {gameState.players[0]?.name || "Nobody"}</p>
            <button className="btn-primary" onClick={() => window.location.reload()}>
              New Game
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <GameApp />
    </AuthProvider>
  );
}

export default App;
