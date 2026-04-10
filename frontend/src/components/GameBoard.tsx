import React, { useEffect, useRef, useState } from "react";
import { GameState, BoardCell } from "../types/game";
import { BOARD_POSITIONS } from "../types/boardLayout";
import BoardCellComponent from "./BoardCell";
import PropertyCardPopup from "./PropertyCardPopup";

interface Props {
  gameState: GameState;
}

const TURN_DURATION = 60;

const GameBoard: React.FC<Props> = ({ gameState }) => {
  const [selectedCell, setSelectedCell] = useState<BoardCell | null>(null);
  const [turnSeconds, setTurnSeconds] = useState(TURN_DURATION);
  const prevPlayer = useRef(gameState.current_player);

  useEffect(() => {
    if (gameState.current_player !== prevPlayer.current) {
      prevPlayer.current = gameState.current_player;
      setTurnSeconds(TURN_DURATION);
    }
  }, [gameState.current_player]);

  useEffect(() => {
    if (gameState.state !== "active") return;
    const interval = setInterval(() => {
      setTurnSeconds((s) => (s > 0 ? s - 1 : 0));
    }, 1000);
    return () => clearInterval(interval);
  }, [gameState.state]);

  const mins = Math.floor(turnSeconds / 60);
  const secs = turnSeconds % 60;
  const timerStr = `${mins}:${secs.toString().padStart(2, "0")}`;

  return (
    <div className="board-container">
      {gameState.state === "active" && gameState.current_player && (
        <div className="turn-indicator">
          <span className="turn-indicator__name">{gameState.current_player}'s TURN</span>
          <span className="turn-indicator__timer">{timerStr}</span>
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
