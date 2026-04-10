import React, { useEffect, useState } from "react";
import { SavedGame } from "../types/game";

interface NewLobbyScreenProps {
  onCreateLobby: (settings: LobbySettings) => void;
  onLoadGame: (savedGameId: string) => void;
  onDeleteGame: (savedGameId: string) => void;
  onBack: () => void;
  error: string;
  creating: boolean;
  savedGames: SavedGame[];
}

export interface LobbySettings {
  maxPlayers: number;
  casino: boolean;
  teams: boolean;
  timer: boolean;
  isPrivate: boolean;
  password: string;
}

const NewLobbyScreen: React.FC<NewLobbyScreenProps> = ({
  onCreateLobby, onLoadGame, onDeleteGame, onBack, error, creating, savedGames,
}) => {
  const [selectedSaveId, setSelectedSaveId] = useState<string | null>(null);
  const [maxPlayers, setMaxPlayers] = useState(() => {
    const draft = sessionStorage.getItem("new-lobby-draft");
    return draft ? JSON.parse(draft).maxPlayers ?? 6 : 6;
  });
  const [casino, setCasino] = useState(() => {
    const draft = sessionStorage.getItem("new-lobby-draft");
    return draft ? JSON.parse(draft).casino ?? false : false;
  });
  const [teams, setTeams] = useState(() => {
    const draft = sessionStorage.getItem("new-lobby-draft");
    return draft ? JSON.parse(draft).teams ?? false : false;
  });
  const [timer, setTimer] = useState(() => {
    const draft = sessionStorage.getItem("new-lobby-draft");
    return draft ? JSON.parse(draft).timer ?? false : false;
  });
  const [isPrivate, setIsPrivate] = useState(() => {
    const draft = sessionStorage.getItem("new-lobby-draft");
    return draft ? JSON.parse(draft).isPrivate ?? false : false;
  });
  const [password, setPassword] = useState(() => {
    const draft = sessionStorage.getItem("new-lobby-draft");
    return draft ? JSON.parse(draft).password ?? "" : "";
  });

  useEffect(() => {
    sessionStorage.setItem(
      "new-lobby-draft",
      JSON.stringify({ maxPlayers, casino, teams, timer, isPrivate, password })
    );
  }, [maxPlayers, casino, teams, timer, isPrivate, password]);

  const handleCreate = () => {
    if (isPrivate && !password.trim()) return;
    sessionStorage.removeItem("new-lobby-draft");
    onCreateLobby({ maxPlayers, casino, teams, timer, isPrivate, password });
  };

  const selectedSave = savedGames.find((g) => g.id === selectedSaveId) ?? null;

  const formatDate = (iso: string) => {
    try {
      return new Date(iso).toLocaleDateString(undefined, {
        month: "2-digit", day: "2-digit", year: "2-digit",
        hour: "2-digit", minute: "2-digit",
      });
    } catch { return iso; }
  };

  return (
    <div className="new-lobby-screen">
      <button className="go-back" onClick={onBack}>[ Go Back ]</button>

      <div className="new-lobby-screen__layout">
        {/* Left panel: New Game + Saved Games list */}
        <div className="new-lobby-screen__left">
          <p className="new-lobby-screen__section-label">Fresh Start:</p>
          <button
            className={`new-lobby-screen__new-game ${selectedSaveId === null ? "new-lobby-screen__new-game--active" : ""}`}
            onClick={() => setSelectedSaveId(null)}
          >
            <span className="new-lobby-screen__new-highlight" />
            <span className="new-lobby-screen__new-label">New Game</span>
          </button>

          {savedGames.length > 0 && (
            <>
              <p className="new-lobby-screen__section-label new-lobby-screen__section-label--saves">
                Saved Games:
              </p>
              <div className="saved-games-list">
                {savedGames.map((g) => (
                  <button
                    key={g.id}
                    className={`saved-game-row ${selectedSaveId === g.id ? "saved-game-row--active" : ""}`}
                    onClick={() => setSelectedSaveId(g.id)}
                  >
                    <span className="saved-game-row__name">{g.name}</span>
                    <span className="saved-game-row__meta">
                      {formatDate(g.updated_at)} &middot; TURN: {g.turn_count} | PLAYERS: {g.player_count}
                    </span>
                  </button>
                ))}
              </div>
            </>
          )}
        </div>

        {/* Right panel: Game Info or Saved Game Details */}
        <div className="new-lobby-screen__panel">
          {selectedSave ? (
            <div className="new-lobby-screen__panel-inner">
              <h3 className="new-lobby-screen__panel-title">{selectedSave.name}</h3>

              {selectedSave.saved_game_players && selectedSave.saved_game_players.length > 0 && (
                <div className="saved-game-players">
                  {selectedSave.saved_game_players.map((p) => (
                    <div key={p.id} className="saved-game-player-row">
                      <span className="saved-game-player-row__name">{p.player_name}</span>
                      <span className="saved-game-player-row__balance">${p.balance.toLocaleString()}</span>
                    </div>
                  ))}
                </div>
              )}

              <div className="new-lobby-screen__row">
                <span className="new-lobby-screen__row-label">Turn</span>
                <span className="new-lobby-screen__row-value">{selectedSave.turn_count}</span>
              </div>
              <div className="new-lobby-screen__row">
                <span className="new-lobby-screen__row-label">Players</span>
                <span className="new-lobby-screen__row-value">{selectedSave.player_count}</span>
              </div>
              {selectedSave.room_settings && (
                <>
                  <div className="new-lobby-screen__row">
                    <span className="new-lobby-screen__row-label">Casino</span>
                    <span className="new-lobby-screen__row-value">{selectedSave.room_settings.casino ? "ON" : "OFF"}</span>
                  </div>
                  <div className="new-lobby-screen__row">
                    <span className="new-lobby-screen__row-label">Teams</span>
                    <span className="new-lobby-screen__row-value">{selectedSave.room_settings.teams ? "ON" : "OFF"}</span>
                  </div>
                  <div className="new-lobby-screen__row">
                    <span className="new-lobby-screen__row-label">Timer</span>
                    <span className="new-lobby-screen__row-value">{selectedSave.room_settings.timer ? "ON" : "OFF"}</span>
                  </div>
                </>
              )}

              <div className="saved-game-actions">
                <button
                  className="btn-primary"
                  onClick={() => onLoadGame(selectedSave.id)}
                  disabled={creating}
                >
                  {creating ? "Loading..." : "LOAD FILE"}
                </button>
                <button
                  className="btn-danger"
                  onClick={() => {
                    onDeleteGame(selectedSave.id);
                    setSelectedSaveId(null);
                  }}
                >
                  TERMINATE
                </button>
              </div>
            </div>
          ) : (
            <div className="new-lobby-screen__panel-inner">
              <h3 className="new-lobby-screen__panel-title">Game Info</h3>

              <div className="new-lobby-screen__row">
                <span className="new-lobby-screen__row-label">Players</span>
                <div className="new-lobby-screen__row-control">
                  <button
                    className="new-lobby-screen__stepper"
                    onClick={() => setMaxPlayers(Math.max(2, maxPlayers - 1))}
                  >-</button>
                  <span className="new-lobby-screen__row-value">{maxPlayers}</span>
                  <button
                    className="new-lobby-screen__stepper"
                    onClick={() => setMaxPlayers(Math.min(6, maxPlayers + 1))}
                  >+</button>
                </div>
              </div>

              <div className="new-lobby-screen__row">
                <span className="new-lobby-screen__row-label">Casino</span>
                <button
                  className={`new-lobby-screen__toggle ${casino ? "active" : ""}`}
                  onClick={() => setCasino(!casino)}
                >{casino ? "ON" : "OFF"}</button>
              </div>

              <div className="new-lobby-screen__row">
                <span className="new-lobby-screen__row-label">Teams</span>
                <button
                  className={`new-lobby-screen__toggle ${teams ? "active" : ""}`}
                  onClick={() => setTeams(!teams)}
                >{teams ? "ON" : "OFF"}</button>
              </div>

              <div className="new-lobby-screen__row">
                <span className="new-lobby-screen__row-label">Timer</span>
                <button
                  className={`new-lobby-screen__toggle ${timer ? "active" : ""}`}
                  onClick={() => setTimer(!timer)}
                >{timer ? "ON" : "OFF"}</button>
              </div>

              <div className="new-lobby-screen__row">
                <span className="new-lobby-screen__row-label">Lobby</span>
                <button
                  className={`new-lobby-screen__toggle ${isPrivate ? "" : "active"}`}
                  onClick={() => setIsPrivate(!isPrivate)}
                >{isPrivate ? "PRIVATE" : "PUBLIC"}</button>
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
          )}
        </div>
      </div>

      {error && <p className="error-text">{error}</p>}

      {!selectedSave && (
        <button
          className="new-lobby-screen__create"
          onClick={handleCreate}
          disabled={creating || (isPrivate && !password.trim())}
        >
          {creating ? "Creating..." : "Create New Lobby"}
        </button>
      )}
    </div>
  );
};

export default NewLobbyScreen;
