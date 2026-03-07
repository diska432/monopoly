export interface BoardPosition {
  row: number;
  col: number;
  side: "bottom" | "left" | "top" | "right" | "corner";
}

// Classic Monopoly board layout: indices 0-39 mapped to grid positions
// Bottom row: 0(corner) 1-9 10(corner)  -> row 10
// Left col:   11-19                      -> col 0
// Top row:    20(corner) 21-29 30(corner)-> row 0
// Right col:  31-39                      -> col 10

export const BOARD_POSITIONS: BoardPosition[] = [
  // Bottom row (right to left): indices 0-10
  { row: 10, col: 10, side: "corner" }, // 0: Start
  { row: 10, col: 9, side: "bottom" },  // 1
  { row: 10, col: 8, side: "bottom" },  // 2
  { row: 10, col: 7, side: "bottom" },  // 3
  { row: 10, col: 6, side: "bottom" },  // 4
  { row: 10, col: 5, side: "bottom" },  // 5
  { row: 10, col: 4, side: "bottom" },  // 6
  { row: 10, col: 3, side: "bottom" },  // 7
  { row: 10, col: 2, side: "bottom" },  // 8
  { row: 10, col: 1, side: "bottom" },  // 9
  { row: 10, col: 0, side: "corner" },  // 10: Prison Visit

  // Left column (bottom to top): indices 11-20
  { row: 9, col: 0, side: "left" },     // 11
  { row: 8, col: 0, side: "left" },     // 12
  { row: 7, col: 0, side: "left" },     // 13
  { row: 6, col: 0, side: "left" },     // 14
  { row: 5, col: 0, side: "left" },     // 15
  { row: 4, col: 0, side: "left" },     // 16
  { row: 3, col: 0, side: "left" },     // 17
  { row: 2, col: 0, side: "left" },     // 18
  { row: 1, col: 0, side: "left" },     // 19
  { row: 0, col: 0, side: "corner" },   // 20: Casino

  // Top row (left to right): indices 21-30
  { row: 0, col: 1, side: "top" },      // 21
  { row: 0, col: 2, side: "top" },      // 22
  { row: 0, col: 3, side: "top" },      // 23
  { row: 0, col: 4, side: "top" },      // 24
  { row: 0, col: 5, side: "top" },      // 25
  { row: 0, col: 6, side: "top" },      // 26
  { row: 0, col: 7, side: "top" },      // 27
  { row: 0, col: 8, side: "top" },      // 28
  { row: 0, col: 9, side: "top" },      // 29
  { row: 0, col: 10, side: "corner" },  // 30: Prison

  // Right column (top to bottom): indices 31-39
  { row: 1, col: 10, side: "right" },   // 31
  { row: 2, col: 10, side: "right" },   // 32
  { row: 3, col: 10, side: "right" },   // 33
  { row: 4, col: 10, side: "right" },   // 34
  { row: 5, col: 10, side: "right" },   // 35
  { row: 6, col: 10, side: "right" },   // 36
  { row: 7, col: 10, side: "right" },   // 37
  { row: 8, col: 10, side: "right" },   // 38
  { row: 9, col: 10, side: "right" },   // 39
];
