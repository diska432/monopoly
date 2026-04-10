import React, { useMemo, useState } from "react";
import { GameState, Character } from "../types/game";

interface LobbyProps {
  gameState: GameState;
  playerName: string;
  sendAction: (action: string, data?: Record<string, any>) => void;
}

const Lobby: React.FC<LobbyProps> = ({ gameState, playerName, sendAction }) => {
  const [hoveredChar, setHoveredChar] = useState<string | null>(null);
  const roomName = gameState.room?.name || "GAME LOBBY";
  const roomMaxPlayers = gameState.room?.max_players || 6;
  const characters = useMemo(() => gameState.characters || [], [gameState.characters]);
  const availableIds = new Set(gameState.available_characters || []);

  const me = gameState.players.find((p) => p.name === playerName);
  const myCharId = me?.character_id ?? null;
  const myReady = me?.ready ?? false;
  const isHost = gameState.room?.host_name === playerName;
  const allReady = gameState.players.length >= 2 && gameState.players.every((p) => p.ready);

  const charMap = useMemo(() => {
    const m: Record<string, Character> = {};
    for (const c of characters) m[c.id] = c;
    return m;
  }, [characters]);

  const displayedChar: Character | null =
    (hoveredChar && charMap[hoveredChar]) ||
    (myCharId && charMap[myCharId]) ||
    null;

  const handleSelectCharacter = (charId: string) => {
    if (!availableIds.has(charId) && charId !== myCharId) return;
    sendAction("select_character", { character_id: charId });
    setHoveredChar(null);
  };

  const handleReadyToggle = () => {
    sendAction(myReady ? "unready" : "ready_up");
  };

  const handleStartGame = () => {
    sendAction("start_game");
  };

  const getPlayerStatus = (p: typeof gameState.players[0]) => {
    if (p.name === playerName) return "[ YOU ]";
    if (p.ready) return "[ READY ]";
    if (p.character_id) return "[ SELECT ]";
    return "[ JOINING ]";
  };

  return (
    <div className="char-select">
      {/* Top bar: player slots */}
      <div className="char-select__topbar">
        {gameState.players.map((p) => {
          const char = p.character_id ? charMap[p.character_id] : null;
          return (
            <div key={p.name} className={`char-select__player-slot ${p.ready ? "char-select__player-slot--ready" : ""}`}>
              <div className="char-select__avatar">
                {char ? (
                  <img src={char.avatar_url} alt={char.name} className="char-select__avatar-img" />
                ) : (
                  <span className="char-select__avatar-letter">?</span>
                )}
              </div>
              <span className="char-select__player-name">{p.name}</span>
              <span
                className="char-select__player-status"
                style={{ color: p.name === playerName ? "#ff008c" : p.ready ? "#66bb6a" : "#6a6a6a" }}
              >
                {getPlayerStatus(p)}
              </span>
            </div>
          );
        })}
        {Array.from({ length: Math.max(0, roomMaxPlayers - gameState.players.length) }).map((_, i) => (
          <div key={`empty-${i}`} className="char-select__player-slot char-select__player-slot--empty">
            <div className="char-select__avatar char-select__avatar--empty">
              <span className="char-select__avatar-letter">?</span>
            </div>
            <span className="char-select__player-name char-select__player-name--empty">Waiting...</span>
            <span className="char-select__player-status">[ OPEN ]</span>
          </div>
        ))}
      </div>

      {/* Main area */}
      <div className="char-select__main">
        {/* Left: character grid */}
        <div className="char-select__left">
          <h2 className="char-select__heading">CHOOSE YOUR SURVIVOR</h2>
          <div className="char-select__grid">
            {characters.map((c) => {
              const taken = !availableIds.has(c.id) && c.id !== myCharId;
              const selected = c.id === myCharId;
              return (
                <div key={c.id} className="char-select__grid-wrapper">
                  <button
                    className={`char-select__grid-cell ${selected ? "char-select__grid-cell--selected" : ""} ${taken ? "char-select__grid-cell--taken" : ""}`}
                    onClick={() => !taken && handleSelectCharacter(c.id)}
                    onMouseEnter={() => setHoveredChar(c.id)}
                    onMouseLeave={() => setHoveredChar(null)}
                    disabled={taken}
                  >
                    <img src={c.avatar_url} alt={c.name} className="char-select__grid-img" />
                    {taken && <div className="char-select__grid-taken">TAKEN</div>}
                    {selected && <div className="char-select__grid-check">&#10003;</div>}
                  </button>
                  <span className="char-select__grid-name">{c.name}</span>
                </div>
              );
            })}
          </div>

          <div className="char-select__players-list">
            <h3 className="char-select__players-title">
              Players ({gameState.players.length}/{roomMaxPlayers})
            </h3>
            {gameState.players.map((p) => {
              const char = p.character_id ? charMap[p.character_id] : null;
              return (
                <div
                  key={p.name}
                  className={`char-select__player-row ${p.name === playerName ? "char-select__player-row--me" : ""}`}
                >
                  {char ? (
                    <img src={char.avatar_url} alt={char.name} className="char-select__player-row-avatar" />
                  ) : (
                    <span className="char-select__player-dot" />
                  )}
                  <span className="char-select__player-row-name">{p.name}</span>
                  {p.ready && <span className="char-select__ready-tag">READY</span>}
                  {p.name === playerName && <span className="you-badge">You</span>}
                </div>
              );
            })}
          </div>
        </div>

        {/* Right: character info panel */}
        <div className="char-select__right">
          <div className="char-select__info-panel">
            {displayedChar ? (
              <>
                <div className="char-select__info-avatar">
                  <img src={displayedChar.full_art_url || displayedChar.avatar_url} alt={displayedChar.name} />
                </div>
                <p className="char-select__info-label">NAME</p>
                <h3 className="char-select__info-name">{displayedChar.name}</h3>
                <p className="char-select__info-label">MOTHERTIME</p>
                <p className="char-select__info-era">{displayedChar.era}</p>
                <p className="char-select__info-label">TRIVIA</p>
                <p className="char-select__info-trivia">{displayedChar.trivia}</p>
              </>
            ) : (
              <>
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
                  <span>{allReady ? "All Ready" : "Selecting..."}</span>
                </div>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Bottom: ready / start button */}
      <div className="char-select__bottom">
        {isHost && allReady ? (
          <button className="char-select__ready-btn" onClick={handleStartGame}>
            START GAME
          </button>
        ) : myCharId ? (
          <button
            className={`char-select__ready-btn ${myReady ? "char-select__ready-btn--waiting" : ""}`}
            onClick={handleReadyToggle}
          >
            {myReady ? "WAITING..." : "READY UP!"}
          </button>
        ) : (
          <div className="char-select__waiting-btn">
            Select a character...
          </div>
        )}
      </div>
    </div>
  );
};

export default Lobby;
