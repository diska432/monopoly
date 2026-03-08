import React, { useState } from "react";
import { AuthProvider, useAuth } from "./hooks/useAuth";
import { useGameSocket } from "./hooks/useGameSocket";
import AuthScreen from "./components/AuthScreen";
import Lobby from "./components/Lobby";
import GameBoard from "./components/GameBoard";
import PlayerPanel from "./components/PlayerPanel";
import PlayersBar from "./components/PlayersBar";
import EventLog from "./components/EventLog";
import "./App.css";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

function GameApp() {
  const { user, session, displayName, signOut, getAccessToken, loading } = useAuth();
  const [screen, setScreen] = useState<"home" | "game">("home");
  const [lobbyId, setLobbyId] = useState<string | null>(null);
  const [playerName, setPlayerName] = useState<string>("");
  const [joinCode, setJoinCode] = useState("");
  const [error, setError] = useState("");

  const token = session?.access_token ?? null;
  const { gameState, events, connected, sendAction } = useGameSocket(lobbyId, playerName, token);

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

  const createLobby = async () => {
    try {
      const freshToken = await getAccessToken();
      // #region agent log
      fetch('http://127.0.0.1:7566/ingest/8db1c7ed-c122-43c4-b932-92b1335506ed',{method:'POST',headers:{'Content-Type':'application/json','X-Debug-Session-Id':'b45bcf'},body:JSON.stringify({sessionId:'b45bcf',location:'App.tsx:createLobby',message:'createLobby called',data:{hasToken:!!freshToken,tokenLen:freshToken?.length||0,userEmail:user?.email||null,hasSession:!!session},timestamp:Date.now(),hypothesisId:'H2'})}).catch(()=>{});
      // #endregion
      if (!freshToken) { setError("Session expired. Please sign in again."); return; }
      const res = await fetch(`${API_BASE}/api/create-lobby`, {
        headers: { Authorization: `Bearer ${freshToken}` },
      });
      // #region agent log
      fetch('http://127.0.0.1:7566/ingest/8db1c7ed-c122-43c4-b932-92b1335506ed',{method:'POST',headers:{'Content-Type':'application/json','X-Debug-Session-Id':'b45bcf'},body:JSON.stringify({sessionId:'b45bcf',location:'App.tsx:createLobby.response',message:'API response',data:{status:res.status,ok:res.ok},timestamp:Date.now(),hypothesisId:'H1'})}).catch(()=>{});
      // #endregion
      if (res.status === 401) { setError("Session expired. Please sign in again."); return; }
      const data = await res.json();
      setPlayerName(displayName);
      setLobbyId(data.lobby_id);
      setScreen("game");
      setError("");
    } catch {
      setError("Could not connect to server.");
    }
  };

  const joinLobby = async () => {
    if (!joinCode.trim()) { setError("Enter lobby code"); return; }
    try {
      const res = await fetch(`${API_BASE}/api/lobby/${joinCode.trim()}/exists`);
      const data = await res.json();
      if (!data.exists) { setError("Lobby not found"); return; }
      setPlayerName(displayName);
      setLobbyId(joinCode.trim());
      setScreen("game");
      setError("");
    } catch {
      setError("Could not connect to server.");
    }
  };

  if (screen === "home") {
    return (
      <div className="home-screen">
        <div className="home-card">
          <h1 className="home-title">MONOPOLY</h1>
          <p className="home-subtitle">KZ Edition</p>

          <div className="user-info">
            <span>Signed in as <strong>{displayName}</strong></span>
            <button className="link-btn" onClick={signOut}>Sign out</button>
          </div>

          <div className="home-actions">
            <button className="btn-primary" onClick={createLobby}>
              Create Game
            </button>
            <div className="divider"><span>or</span></div>
            <div className="join-row">
              <input
                value={joinCode}
                onChange={(e) => setJoinCode(e.target.value.toUpperCase())}
                placeholder="Lobby Code"
                maxLength={6}
              />
              <button className="btn-secondary" onClick={joinLobby}>
                Join
              </button>
            </div>
          </div>

          {error && <p className="error-text">{error}</p>}
        </div>
      </div>
    );
  }

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
