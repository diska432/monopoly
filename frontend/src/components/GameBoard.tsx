import React from "react";
import { GameState } from "../types/game";
import { BOARD_POSITIONS } from "../types/boardLayout";
import BoardCellComponent from "./BoardCell";

interface Props {
  gameState: GameState;
}

const GameBoard: React.FC<Props> = ({ gameState }) => {
  return (
    <div className="board-grid">
      {gameState.board.map((cell, i) => (
        <BoardCellComponent
          key={i}
          cell={cell}
          pos={BOARD_POSITIONS[i]}
          players={gameState.players}
        />
      ))}
      <div className="board-center" style={{ gridRow: "2/11", gridColumn: "2/11" }}>
        <h1 className="board-title">MONOPOLY</h1>
        <p className="board-subtitle">KZ Edition</p>
      </div>
    </div>
  );
};

export default GameBoard;
