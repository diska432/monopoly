export interface PlayerState {
  name: string;
  color: string;
  balance: number;
  position: number;
  in_jail_turns: number;
  doubles_rolled: number;
  character_id: string | null;
  ready: boolean;
  owned_company_names: string[];
  color_counts: Record<string, number>;
}

export interface Character {
  id: string;
  name: string;
  era: string;
  avatar_url: string;
  trivia: string;
  display_order: number;
}

export interface CompanyCell {
  name: string;
  board_index: number;
  price: number;
  type: "company" | "car" | "videogame";
  rent: number;
  fee: number;
  color: string;
  count_stars: number;
  mortgage_count: number;
  initial_rent: number;
  owner_id: string | null;
}

export interface TaxCell {
  name: string;
  board_index: number;
  type: "tax";
  amount: number;
}

export interface ChanceCell {
  name: string;
  board_index: number;
  type: "chance";
}

export interface SpecialCellData {
  name: string;
  board_index: number;
  type: "start" | "visit" | "prison" | "casino";
}

export type BoardCell = CompanyCell | TaxCell | ChanceCell | SpecialCellData;

export interface AuctionState {
  company: string;
  current_price: number;
  current_bidder: string | null;
  highest_bidder: string | null;
  participants: string[];
}

export interface RoomInfo {
  id: string;
  name: string;
  host_name: string;
  visibility: "public" | "private";
  max_players: number;
  casino: boolean;
  teams: boolean;
  timer: boolean;
  state: "lobby" | "active" | "gameover";
  player_count: number;
  players: string[];
}

export interface GameState {
  lobby_id: string;
  state: "lobby" | "active" | "gameover";
  current_player_index: number;
  current_player: string | null;
  players: PlayerState[];
  board: BoardCell[];
  pending_action: string | null;
  pending_player: string | null;
  pending_company: string | null;
  auction: AuctionState | null;
  room?: RoomInfo;
  characters?: Character[];
  available_characters?: string[];
}

export interface SavedGame {
  id: string;
  host_user_id: string;
  name: string;
  game_state: any;
  room_settings: any;
  turn_count: number;
  player_count: number;
  created_at: string;
  updated_at: string;
  saved_game_players?: SavedGamePlayer[];
}

export interface SavedGamePlayer {
  id: string;
  saved_game_id: string;
  user_id: string | null;
  player_name: string;
  character_id: string | null;
  balance: number;
}

export interface GameEvent {
  type: string;
  [key: string]: any;
}

export interface ServerMessage {
  type: "full_state" | "events" | "error" | "player_disconnected";
  state?: GameState;
  events?: GameEvent[];
  message?: string;
  player?: string;
}

export function isCompanyCell(cell: BoardCell): cell is CompanyCell {
  return "price" in cell;
}
