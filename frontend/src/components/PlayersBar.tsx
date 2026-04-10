import React, { useMemo } from "react";
import { GameState, Character } from "../types/game";

interface Props {
  gameState: GameState;
  playerName: string;
}

const PlayersBar: React.FC<Props> = ({ gameState, playerName }) => {
  const charMap = useMemo(() => {
    const m: Record<string, Character> = {};
    for (const c of gameState.characters || []) m[c.id] = c;
    return m;
  }, [gameState.characters]);

  return (
    <div className="players-sidebar">
      {gameState.players.map((p) => {
        const char = p.character_id ? charMap[p.character_id] : null;
        return (
          <div
            key={p.name}
            className={`ps-card ${p.name === gameState.current_player ? "ps-card--active" : ""} ${p.name === playerName ? "ps-card--me" : ""}`}
          >
            <div className="ps-avatar">
              {char ? (
                <img src={char.avatar_url} alt={char.name} className="ps-avatar-img" />
              ) : (
                <span className="ps-avatar-initial">{p.name.charAt(0).toUpperCase()}</span>
              )}
            </div>
            <div className="ps-info">
              <span className="ps-name">
                {p.name}
                {p.name === gameState.current_player && <span className="ps-turn-arrow"> ◀</span>}
              </span>
              <span className="ps-balance">${p.balance.toLocaleString()}</span>
            </div>
            {p.in_jail_turns > 0 && <span className="ps-jail">JAIL</span>}
          </div>
        );
      })}
    </div>
  );
};

export default PlayersBar;
