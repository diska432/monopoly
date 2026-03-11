import React, { useState } from "react";

interface NewLobbyScreenProps {
  onCreateLobby: (settings: LobbySettings) => void;
  onBack: () => void;
  error: string;
  creating: boolean;
}

export interface LobbySettings {
  maxPlayers: number;
  casino: boolean;
  teams: boolean;
  timer: boolean;
  isPrivate: boolean;
  password: string;
}

const NewLobbyScreen: React.FC<NewLobbyScreenProps> = ({ onCreateLobby, onBack, error, creating }) => {
  const [maxPlayers, setMaxPlayers] = useState(6);
  const [casino, setCasino] = useState(false);
  const [teams, setTeams] = useState(false);
  const [timer, setTimer] = useState(false);
  const [isPrivate, setIsPrivate] = useState(false);
  const [password, setPassword] = useState("");

  const handleCreate = () => {
    if (isPrivate && !password.trim()) return;
    onCreateLobby({ maxPlayers, casino, teams, timer, isPrivate, password });
  };

  return (
    <div className="new-lobby-screen">
      <button className="go-back" onClick={onBack}>[ Go Back ]</button>

      <div className="new-lobby-screen__layout">
        <div className="new-lobby-screen__left">
          <p className="new-lobby-screen__section-label">Fresh Start:</p>
          <div className="new-lobby-screen__new-game">
            <span className="new-lobby-screen__new-highlight" />
            <span className="new-lobby-screen__new-label">New Game</span>
          </div>
        </div>

        <div className="new-lobby-screen__panel">
          <div className="new-lobby-screen__panel-inner">
            <h3 className="new-lobby-screen__panel-title">Game Info</h3>

            <div className="new-lobby-screen__row">
              <span className="new-lobby-screen__row-label">Players</span>
              <div className="new-lobby-screen__row-control">
                <button
                  className="new-lobby-screen__stepper"
                  onClick={() => setMaxPlayers(Math.max(2, maxPlayers - 1))}
                >
                  -
                </button>
                <span className="new-lobby-screen__row-value">{maxPlayers}</span>
                <button
                  className="new-lobby-screen__stepper"
                  onClick={() => setMaxPlayers(Math.min(6, maxPlayers + 1))}
                >
                  +
                </button>
              </div>
            </div>

            <div className="new-lobby-screen__row">
              <span className="new-lobby-screen__row-label">Casino</span>
              <button
                className={`new-lobby-screen__toggle ${casino ? "active" : ""}`}
                onClick={() => setCasino(!casino)}
              >
                {casino ? "ON" : "OFF"}
              </button>
            </div>

            <div className="new-lobby-screen__row">
              <span className="new-lobby-screen__row-label">Teams</span>
              <button
                className={`new-lobby-screen__toggle ${teams ? "active" : ""}`}
                onClick={() => setTeams(!teams)}
              >
                {teams ? "ON" : "OFF"}
              </button>
            </div>

            <div className="new-lobby-screen__row">
              <span className="new-lobby-screen__row-label">Timer</span>
              <button
                className={`new-lobby-screen__toggle ${timer ? "active" : ""}`}
                onClick={() => setTimer(!timer)}
              >
                {timer ? "ON" : "OFF"}
              </button>
            </div>

            <div className="new-lobby-screen__row">
              <span className="new-lobby-screen__row-label">Lobby</span>
              <button
                className={`new-lobby-screen__toggle ${isPrivate ? "" : "active"}`}
                onClick={() => setIsPrivate(!isPrivate)}
              >
                {isPrivate ? "PRIVATE" : "PUBLIC"}
              </button>
            </div>

            {isPrivate && (
              <div className="new-lobby-screen__row">
                <span className="new-lobby-screen__row-label">Password</span>
                <input
                  className="new-lobby-screen__password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="[ 1234 ]"
                  maxLength={16}
                />
              </div>
            )}
          </div>
        </div>
      </div>

      {error && <p className="error-text">{error}</p>}

      <button
        className="new-lobby-screen__create"
        onClick={handleCreate}
        disabled={creating || (isPrivate && !password.trim())}
      >
        {creating ? "Creating..." : "Create New Lobby"}
      </button>
    </div>
  );
};

export default NewLobbyScreen;
