import React, { useMemo } from "react";
import { BoardCell as BCType, PlayerState, Character, isCompanyCell } from "../types/game";
import { BoardPosition } from "../types/boardLayout";

interface Props {
  cell: BCType;
  pos: BoardPosition;
  players: PlayerState[];
  characters?: Character[];
  onCellClick?: (cell: BCType) => void;
}

const COLOR_MAP: Record<string, string> = {
  brown: "#8B4513", pink: "#FF69B4", purple: "#9370DB", orange: "#FF8C00",
  red: "#DC143C", yellow: "#FFD700", green: "#228B22", blue: "#1E90FF",
};

const PLAYER_COLORS: Record<string, string> = {
  red: "#e74c3c", green: "#2ecc71", blue: "#3498db",
  black: "#2c3e50", yellow: "#f1c40f", purple: "#9b59b6", orange: "#e67e22",
};

const BoardCellComponent: React.FC<Props> = ({ cell, pos, players, characters, onCellClick }) => {
  const playersHere = players.filter((p) => p.position === cell.board_index);
  const isProperty = isCompanyCell(cell);
  const colorBar = isProperty && cell.color ? COLOR_MAP[cell.color] : undefined;
  const isCorner = pos.side === "corner";

  const charMap = useMemo(() => {
    const m: Record<string, Character> = {};
    for (const c of characters || []) m[c.id] = c;
    return m;
  }, [characters]);

  return (
    <div
      className={`board-cell ${pos.side} ${isCorner ? "corner" : ""} ${isProperty && cell.owner_id ? "owned" : ""}`}
      style={{ gridRow: pos.row + 1, gridColumn: pos.col + 1 }}
      onClick={() => isProperty && onCellClick?.(cell)}
    >
      {colorBar && <div className="color-bar" style={{ background: colorBar }} />}
      <div className="cell-name">{cell.name}</div>
      {isProperty && cell.owner_id && (
        <div className="owner-dot" style={{
          background: PLAYER_COLORS[players.find(p => p.name === cell.owner_id)?.color.toLowerCase() || ""] || "#999"
        }} />
      )}
      {isProperty && cell.count_stars > 0 && (
        <div className="stars">{"★".repeat(cell.count_stars)}</div>
      )}
      {!isProperty && cell.type === "tax" && <div className="cell-info">💰{(cell as any).amount}</div>}
      {!isProperty && cell.type === "chance" && <div className="cell-info">?</div>}
      {playersHere.length > 0 && (
        <div className="player-tokens">
          {playersHere.map((p) => {
            const char = p.character_id ? charMap[p.character_id] : null;
            return char ? (
              <img
                key={p.name}
                className="token-avatar"
                src={char.avatar_url}
                alt={p.name}
                title={p.name}
              />
            ) : (
              <div
                key={p.name}
                className="token"
                title={p.name}
                style={{ background: PLAYER_COLORS[p.color.toLowerCase()] || "#999" }}
              />
            );
          })}
        </div>
      )}
    </div>
  );
};

export default BoardCellComponent;
