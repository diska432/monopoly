import React from "react";
import { GameState } from "../types/game";

interface Props {
  gameState: GameState;
  playerName: string;
}

const PLAYER_COLORS: Record<string, string> = {
  red: "#e74c3c", green: "#2ecc71", blue: "#3498db",
  black: "#2c3e50", yellow: "#f1c40f", purple: "#9b59b6", orange: "#e67e22",
};

const PlayersBar: React.FC<Props> = ({ gameState, playerName }) => {
  return (
    <div className="players-bar">
      {gameState.players.map((p) => (
        <div
          key={p.name}
          className={`player-card ${p.name === gameState.current_player ? "active" : ""} ${p.name === playerName ? "is-me" : ""}`}
          style={{ borderColor: PLAYER_COLORS[p.color.toLowerCase()] || "#888" }}
        >
          <div className="pc-header">
            <span className="pc-dot" style={{ background: PLAYER_COLORS[p.color.toLowerCase()] || "#888" }} />
            <span className="pc-name">{p.name}</span>
            {p.name === gameState.current_player && <span className="pc-turn">◀</span>}
          </div>
          <div className="pc-balance">{p.balance} ₸</div>
          <div className="pc-props">{p.owned_company_names.length} properties</div>
          {p.in_jail_turns > 0 && <div className="pc-jail">Jail ({p.in_jail_turns})</div>}
        </div>
      ))}
    </div>
  );
};

export default PlayersBar;
