import React, { useState } from "react";
import { useGameSocket } from "./hooks/useGameSocket";
import Lobby from "./components/Lobby";
import GameBoard from "./components/GameBoard";
import PlayerPanel from "./components/PlayerPanel";
import PlayersBar from "./components/PlayersBar";
import EventLog from "./components/EventLog";
import "./App.css";

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

function App() {
  const [screen, setScreen] = useState<"home" | "game">("home");
  const [lobbyId, setLobbyId] = useState<string | null>(null);
  const [playerName, setPlayerName] = useState<string>("");
  const [nameInput, setNameInput] = useState("");
  const [joinCode, setJoinCode] = useState("");
  const [error, setError] = useState("");

  const { gameState, events, connected, sendAction } = useGameSocket(lobbyId, playerName);

  const createLobby = async () => {
    if (!nameInput.trim()) { setError("Enter your name"); return; }
    try {
      const res = await fetch(`${API_BASE}/api/create-lobby`);
      const data = await res.json();
      setPlayerName(nameInput.trim());
      setLobbyId(data.lobby_id);
      setScreen("game");
      setError("");
    } catch {
      setError("Could not connect to server.");
    }
  };

  const joinLobby = async () => {
    if (!nameInput.trim()) { setError("Enter your name"); return; }
    if (!joinCode.trim()) { setError("Enter lobby code"); return; }
    try {
      const res = await fetch(`${API_BASE}/api/lobby/${joinCode.trim()}/exists`);
      const data = await res.json();
      if (!data.exists) { setError("Lobby not found"); return; }
      setPlayerName(nameInput.trim());
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

          <div className="form-group">
            <label>Your Name</label>
            <input
              value={nameInput}
              onChange={(e) => setNameInput(e.target.value)}
              placeholder="Enter nickname..."
              maxLength={20}
            />
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

export default App;
