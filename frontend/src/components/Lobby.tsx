import React, { useState } from "react";
import { GameState } from "../types/game";

interface LobbyProps {
  gameState: GameState;
  playerName: string;
  sendAction: (action: string, data?: Record<string, any>) => void;
}

const Lobby: React.FC<LobbyProps> = ({ gameState, playerName, sendAction }) => {
  const [copied, setCopied] = useState(false);

  const copyCode = () => {
    navigator.clipboard.writeText(gameState.lobby_id);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="lobby">
      <div className="lobby-header">
        <h2>Game Lobby</h2>
        <div className="lobby-code">
          <span>Code: <strong>{gameState.lobby_id}</strong></span>
          <button onClick={copyCode} className="btn-small">
            {copied ? "Copied!" : "Copy"}
          </button>
        </div>
      </div>

      <div className="lobby-players">
        <h3>Players ({gameState.players.length}/6)</h3>
        <div className="player-list">
          {gameState.players.map((p) => (
            <div key={p.name} className="lobby-player" style={{ borderLeftColor: p.color.toLowerCase() }}>
              <span className="player-dot" style={{ background: p.color.toLowerCase() }} />
              <span>{p.name}</span>
              {p.name === playerName && <span className="you-badge">You</span>}
            </div>
          ))}
        </div>
      </div>

      <div className="lobby-actions">
        {gameState.players.length >= 2 ? (
          <button className="btn-primary" onClick={() => sendAction("start_game")}>
            Start Game
          </button>
        ) : (
          <p className="waiting-text">Waiting for more players to join...</p>
        )}
      </div>
    </div>
  );
};

export default Lobby;
