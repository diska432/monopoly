import React, { useState } from "react";
import { GameState, BoardCell } from "../types/game";
import { BOARD_POSITIONS } from "../types/boardLayout";
import BoardCellComponent from "./BoardCell";
import PropertyCardPopup from "./PropertyCardPopup";

interface Props {
  gameState: GameState;
}

const GameBoard: React.FC<Props> = ({ gameState }) => {
  const [selectedCell, setSelectedCell] = useState<BoardCell | null>(null);

  return (
    <div className="board-container">
      {gameState.state === "active" && gameState.current_player && (
        <div className="turn-indicator">
          <span className="turn-indicator__name">{gameState.current_player}'s TURN</span>
        </div>
      )}
      <div className="board-grid">
        {gameState.board.map((cell, i) => (
          <BoardCellComponent
            key={i}
            cell={cell}
            pos={BOARD_POSITIONS[i]}
            players={gameState.players}
            characters={gameState.characters}
            onCellClick={setSelectedCell}
          />
        ))}
        <div className="board-center" style={{ gridRow: "2/11", gridColumn: "2/11" }}>
          <h1 className="board-title">LEIX IV</h1>
          <p className="board-subtitle">MONOPOLY</p>
        </div>
      </div>
      {selectedCell && (
        <PropertyCardPopup cell={selectedCell} onClose={() => setSelectedCell(null)} />
      )}
    </div>
  );
};

export default GameBoard;
