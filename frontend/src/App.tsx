import React, { useCallback, useEffect, useState } from "react";
import { Navigate, Route, Routes, useLocation, useNavigate, useParams } from "react-router-dom";
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
import Toast from "./components/Toast";
import LoadingScreen from "./components/LoadingScreen";
import { RoomInfo, SavedGame } from "./types/game";
import "./App.css";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

function getStoredRoomPassword(roomId: string): string {
  return sessionStorage.getItem(`room-password:${roomId}`) ?? "";
}

function setStoredRoomPassword(roomId: string, password: string) {
  if (password.trim()) {
    sessionStorage.setItem(`room-password:${roomId}`, password);
  } else {
    sessionStorage.removeItem(`room-password:${roomId}`);
  }
}

function RoomPage({ displayName, token }: { displayName: string; token: string | null }) {
  const navigate = useNavigate();
  const { roomId } = useParams<{ roomId: string }>();
  const [roomPassword, setRoomPassword] = useState(() =>
    roomId ? getStoredRoomPassword(roomId) : ""
  );
  const [passwordInput, setPasswordInput] = useState("");
  const [showSettings, setShowSettings] = useState(false);
  const [saving, setSaving] = useState(false);
  const { getAccessToken } = useAuth();
  const { gameState, events, connected, error, sendAction } = useGameSocket(
    roomId ?? null,
    displayName,
    token,
    roomPassword
  );

  useEffect(() => {
    if (error === "room_not_found") {
      sessionStorage.setItem("toast", "Room no longer exists.");
      navigate("/", { replace: true });
    } else if (error === "auth_failed") {
      sessionStorage.setItem("toast", "Session expired. Please sign in again.");
      navigate("/auth/login", { replace: true });
    } else if (error === "already_connected") {
      sessionStorage.setItem("toast", "You are already connected to this room.");
      navigate("/", { replace: true });
    }
  }, [error, navigate]);

  if (!roomId) {
    return <Navigate to="/" replace />;
  }

  if (error === "password_required") {
    return (
      <div className="error-screen">
        <div className="error-card">
          <h2>Private Room</h2>
          <p>This room requires a password to join.</p>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              if (passwordInput.trim()) {
                setStoredRoomPassword(roomId, passwordInput.trim());
                setRoomPassword(passwordInput.trim());
              }
            }}
          >
            <input
              className="error-card__input"
              type="password"
              value={passwordInput}
              onChange={(e) => setPasswordInput(e.target.value)}
              placeholder="Room password..."
              autoFocus
            />
            <button type="submit" className="btn-primary" disabled={!passwordInput.trim()}>
              Join Room
            </button>
          </form>
          <button className="btn-secondary error-card__back" onClick={() => navigate("/", { replace: true })}>
            Back to Menu
          </button>
        </div>
      </div>
    );
  }

  if (error === "connection_failed") {
    return (
      <div className="error-screen">
        <div className="error-card">
          <h2>Connection Failed</h2>
          <p>Could not connect to the game room. It may have been closed.</p>
          <button className="btn-primary" onClick={() => navigate("/", { replace: true })}>
            Back to Menu
          </button>
        </div>
      </div>
    );
  }

  if (!gameState) {
    return <LoadingScreen message={connected ? "Loading game..." : "Connecting..."} />;
  }

  if (gameState.state === "lobby") {
    return <Lobby gameState={gameState} playerName={displayName} sendAction={sendAction} />;
  }

  const isHost = gameState.room?.host_name === displayName;

  const handleSaveGame = async () => {
    if (!roomId) return;
    setSaving(true);
    try {
      const freshToken = await getAccessToken();
      if (!freshToken) return;
      const res = await fetch(`${API_BASE}/api/games/save`, {
        method: "POST",
        headers: { Authorization: `Bearer ${freshToken}`, "Content-Type": "application/json" },
        body: JSON.stringify({ room_id: roomId }),
      });
      if (res.ok) {
        sessionStorage.setItem("toast", "Game saved successfully!");
        navigate("/", { replace: true });
      }
    } catch { /* ignore */ }
    setSaving(false);
  };

  return (
    <div className="game-screen">
      <div className="game-left">
        <PlayersBar gameState={gameState} playerName={displayName} />
        <EventLog events={events} />
      </div>
      <div className="game-board-area">
        <GameBoard gameState={gameState} />
      </div>
      <div className="game-sidebar">
        <PlayerPanel gameState={gameState} playerName={displayName} sendAction={sendAction} />
        {isHost && (
          <button className="btn-secondary settings-btn" onClick={() => setShowSettings(!showSettings)}>
            Settings
          </button>
        )}
      </div>
      {showSettings && isHost && (
        <div className="settings-overlay" onClick={() => setShowSettings(false)}>
          <div className="settings-panel" onClick={(e) => e.stopPropagation()}>
            <h3 className="settings-panel__title">GAME SETTINGS</h3>
            <button className="btn-primary" onClick={handleSaveGame} disabled={saving}>
              {saving ? "Saving..." : "SAVE GAME"}
            </button>
            <button className="btn-secondary" onClick={() => setShowSettings(false)}>
              CLOSE
            </button>
          </div>
        </div>
      )}
      {gameState.state === "gameover" && (
        <div className="gameover-overlay">
          <div className="gameover-card">
            <h2>Game Over!</h2>
            <p>Winner: {gameState.players[0]?.name || "Nobody"}</p>
            <button className="btn-primary" onClick={() => navigate("/", { replace: true })}>
              New Game
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

function GameApp() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, session, displayName, signOut, getAccessToken, loading } = useAuth();
  const [rooms, setRooms] = useState<RoomInfo[]>([]);
  const [savedGames, setSavedGames] = useState<SavedGame[]>([]);
  const [error, setError] = useState("");
  const [creating, setCreating] = useState(false);
  const [joining, setJoining] = useState(false);

  const token = session?.access_token ?? null;

  const fetchRooms = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/api/lobbies`);
      const data = await res.json();
      setRooms(data.rooms ?? []);
    } catch {
      setError("Could not load rooms.");
    }
  }, []);

  const fetchSavedGames = useCallback(async () => {
    try {
      const freshToken = await getAccessToken();
      if (!freshToken) return;
      const res = await fetch(`${API_BASE}/api/games/saved`, {
        headers: { Authorization: `Bearer ${freshToken}` },
      });
      const data = await res.json();
      setSavedGames(data.saved_games ?? []);
    } catch { /* ignore */ }
  }, [getAccessToken]);

  useEffect(() => {
    if (user && location.pathname === "/play/join") {
      fetchRooms();
    }
    if (user && location.pathname === "/play/host") {
      fetchSavedGames();
    }
  }, [user, location.pathname, fetchRooms, fetchSavedGames]);

  if (loading) {
    return <LoadingScreen />;
  }

  if (!user) {
    return (
      <Routes>
        <Route path="/auth/login" element={<AuthScreen />} />
        <Route path="/auth/register" element={<AuthScreen />} />
        <Route path="*" element={<Navigate to="/auth/login" replace />} />
      </Routes>
    );
  }

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
      setStoredRoomPassword(data.room.id, settings.isPrivate ? settings.password : "");
      navigate(`/rooms/${data.room.id}`, { replace: true });
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
      setStoredRoomPassword(room.id, password);
      navigate(`/rooms/${room.id}`, { replace: true });
    } catch {
      setError("Could not connect to server.");
    }
    setJoining(false);
  };

  const handleLoadGame = async (savedGameId: string) => {
    setCreating(true);
    setError("");
    try {
      const freshToken = await getAccessToken();
      if (!freshToken) {
        setError("Session expired. Please sign in again.");
        setCreating(false);
        return;
      }
      const res = await fetch(`${API_BASE}/api/games/load`, {
        method: "POST",
        headers: { Authorization: `Bearer ${freshToken}`, "Content-Type": "application/json" },
        body: JSON.stringify({ saved_game_id: savedGameId }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail || "Could not load game.");
        setCreating(false);
        return;
      }
      navigate(`/rooms/${data.room.id}`, { replace: true });
    } catch {
      setError("Could not connect to server.");
    }
    setCreating(false);
  };

  const handleDeleteGame = async (savedGameId: string) => {
    try {
      const freshToken = await getAccessToken();
      if (!freshToken) return;
      await fetch(`${API_BASE}/api/games/${savedGameId}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${freshToken}` },
      });
      setSavedGames((prev) => prev.filter((g) => g.id !== savedGameId));
    } catch { /* ignore */ }
  };

  return (
    <Routes>
      <Route path="/auth/*" element={<Navigate to="/" replace />} />
      <Route
        path="/"
        element={
          <>
            <Toast />
            <MainMenu
            displayName={displayName}
            onStartGame={() => {
              setError("");
              navigate("/play");
            }}
            onLeave={async () => {
              await signOut();
              navigate("/auth/login", { replace: true });
            }}
          />
          </>
        }
      />
      <Route
        path="/play"
        element={
          <HostJoinScreen
            onHost={() => {
              setError("");
              navigate("/play/host");
            }}
            onJoin={() => {
              setError("");
              navigate("/play/join?tab=public");
            }}
            onBack={() => navigate("/")}
          />
        }
      />
      <Route
        path="/play/host"
        element={
          <NewLobbyScreen
            onCreateLobby={handleCreateLobby}
            onLoadGame={handleLoadGame}
            onDeleteGame={handleDeleteGame}
            onBack={() => navigate("/play")}
            error={error}
            creating={creating}
            savedGames={savedGames}
          />
        }
      />
      <Route
        path="/play/join"
        element={
          <JoinLobbyScreen
            rooms={rooms}
            onJoin={handleJoinLobby}
            onRefresh={fetchRooms}
            onBack={() => navigate("/play")}
            error={error}
            joining={joining}
          />
        }
      />
      <Route path="/rooms/:roomId" element={<RoomPage displayName={displayName} token={token} />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
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
