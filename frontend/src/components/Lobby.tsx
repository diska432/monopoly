import React, { useState } from "react";
import { GameState } from "../types/game";

interface LobbyProps {
  gameState: GameState;
  playerName: string;
  sendAction: (action: string, data?: Record<string, any>) => void;
}

const PLAYER_COLORS: Record<string, string> = {
  red: "#ef5350",
  blue: "#42a5f5",
  green: "#66bb6a",
  yellow: "#ffca28",
  purple: "#ab47bc",
  orange: "#ffa726",
};

const Lobby: React.FC<LobbyProps> = ({ gameState, playerName, sendAction }) => {
  const [copied, setCopied] = useState(false);
  const roomName = gameState.room?.name || "GAME LOBBY";
  const roomVisibility = gameState.room?.visibility || "public";
  const roomMaxPlayers = gameState.room?.max_players || 6;

  const copyCode = () => {
    navigator.clipboard.writeText(roomName);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const isMe = (name: string) => name === playerName;
  const canStart = gameState.players.length >= 2;

  return (
    <div className="char-select">
      <div className="char-select__topbar">
        {gameState.players.map((p) => {
          const color = PLAYER_COLORS[p.color.toLowerCase()] || p.color;
          return (
            <div key={p.name} className="char-select__player-slot">
              <div
                className="char-select__avatar"
                style={{ borderColor: color, background: `${color}22` }}
              >
                <span className="char-select__avatar-letter" style={{ color }}>
                  {p.name.charAt(0).toUpperCase()}
                </span>
              </div>
              <span className="char-select__player-name">{p.name}</span>
              <span className="char-select__player-status" style={{ color: isMe(p.name) ? "#ff008c" : "#6a6a6a" }}>
                {isMe(p.name) ? "[ YOU ]" : "[ READY ]"}
              </span>
            </div>
          );
        })}
        {Array.from({ length: Math.max(0, 6 - gameState.players.length) }).map((_, i) => (
          <div key={`empty-${i}`} className="char-select__player-slot char-select__player-slot--empty">
            <div className="char-select__avatar char-select__avatar--empty">
              <span className="char-select__avatar-letter">?</span>
            </div>
            <span className="char-select__player-name char-select__player-name--empty">Waiting...</span>
            <span className="char-select__player-status">[ OPEN ]</span>
          </div>
        ))}
      </div>

      <div className="char-select__main">
        <div className="char-select__left">
          <h2 className="char-select__heading">{roomName}</h2>

          <div className="char-select__code-area">
            <p className="char-select__code-label">Room Type:</p>
            <div className="char-select__code-row">
              <span className="char-select__code">{roomVisibility}</span>
              <button onClick={copyCode} className="btn-small">
                {copied ? "Copied!" : "Copy Name"}
              </button>
            </div>
          </div>

          <div className="char-select__players-list">
            <h3 className="char-select__players-title">
              Players ({gameState.players.length}/{roomMaxPlayers})
            </h3>
            {gameState.players.map((p) => {
              const color = PLAYER_COLORS[p.color.toLowerCase()] || p.color;
              return (
                <div
                  key={p.name}
                  className={`char-select__player-row ${isMe(p.name) ? "char-select__player-row--me" : ""}`}
                  style={{ borderLeftColor: color }}
                >
                  <span className="char-select__player-dot" style={{ background: color }} />
                  <span className="char-select__player-row-name">{p.name}</span>
                  {isMe(p.name) && <span className="you-badge">You</span>}
                </div>
              );
            })}
          </div>
        </div>

        <div className="char-select__right">
          <div className="char-select__info-panel">
            <h3 className="char-select__info-title">Game Info</h3>
            <div className="char-select__info-row">
              <span>Room</span>
              <span>{roomName}</span>
            </div>
            <div className="char-select__info-row">
              <span>Players</span>
              <span>{gameState.players.length} / {roomMaxPlayers}</span>
            </div>
            <div className="char-select__info-row">
              <span>Status</span>
              <span>{canStart ? "Ready" : "Waiting"}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="char-select__bottom">
        {canStart ? (
          <button className="char-select__ready-btn" onClick={() => sendAction("start_game")}>
            Start Game!
          </button>
        ) : (
          <div className="char-select__waiting-btn">
            Waiting for players...
          </div>
        )}
      </div>
    </div>
  );
};

export default Lobby;
