"""
Pure state-machine game engine. Zero I/O.
Accepts actions, returns event lists. All bugs from original codebase fixed.
"""
from __future__ import annotations
import math
from random import randint
from typing import Any

from .cells import Cell, Company, Chance, Tax, SpecialCell
from .player import Player
from .board import create_board
from .rent_tables import RENT_TABLE, CAR_RENT_BY_COUNT, COLOR_SET_SIZE

COLORS = ["Red", "Green", "Blue", "Black", "Yellow", "Purple", "Orange"]


class GameEngine:
    def __init__(self, lobby_id: str):
        self.lobby_id = lobby_id
        self.players: list[Player] = []
        self.board: list[Cell] = create_board()
        self.state = "lobby"  # lobby | active | gameover
        self.current_player_index = 0
        self._pending_action: str | None = None
        self._pending_player: str | None = None
        self._pending_company: str | None = None
        self._pending_was_double: bool = False
        self._auction: dict | None = None
        self.characters: list[dict] = []

    # ---- Serialization ----
    def get_full_state(self) -> dict:
        board_data = []
        for cell in self.board:
            if isinstance(cell, Company):
                board_data.append(cell.to_dict())
            elif isinstance(cell, Tax):
                board_data.append({"name": cell.name, "board_index": cell.board_index, "type": "tax", "amount": cell.amount})
            elif isinstance(cell, Chance):
                board_data.append({"name": cell.name, "board_index": cell.board_index, "type": "chance"})
            elif isinstance(cell, SpecialCell):
                board_data.append({"name": cell.name, "board_index": cell.board_index, "type": cell.type})
        auction_data = None
        if self._auction:
            a = self._auction
            auction_data = {
                "company": a["company"],
                "current_price": a["price"],
                "current_bidder": a["participants"][a["bidder_idx"]] if a["participants"] else None,
                "highest_bidder": a["highest_bidder"],
                "participants": a["participants"],
            }
        selected_ids = {p.character_id for p in self.players if p.character_id}
        available = [c["id"] for c in self.characters if c["id"] not in selected_ids]
        return {
            "lobby_id": self.lobby_id,
            "state": self.state,
            "current_player_index": self.current_player_index,
            "current_player": self.players[self.current_player_index].name if self.players and self.state == "active" else None,
            "players": [p.to_dict() for p in self.players],
            "board": board_data,
            "pending_action": self._pending_action,
            "pending_player": self._pending_player,
            "pending_company": self._pending_company,
            "auction": auction_data,
            "characters": self.characters,
            "available_characters": available,
        }

    def to_save_dict(self) -> dict:
        """Full serialization for persisting a game snapshot (includes internal state)."""
        board_data = []
        for cell in self.board:
            if isinstance(cell, Company):
                d = cell.to_dict()
                board_data.append(d)
            elif isinstance(cell, Tax):
                board_data.append({"name": cell.name, "board_index": cell.board_index, "type": "tax", "amount": cell.amount})
            elif isinstance(cell, Chance):
                board_data.append({"name": cell.name, "board_index": cell.board_index, "type": "chance"})
            elif isinstance(cell, SpecialCell):
                board_data.append({"name": cell.name, "board_index": cell.board_index, "type": cell.type})

        players_data = []
        for p in self.players:
            pd = p.to_dict()
            pd["upgrade_used_this_turn"] = dict(p.upgrade_used_this_turn)
            players_data.append(pd)

        auction_data = None
        if self._auction:
            auction_data = dict(self._auction)

        return {
            "lobby_id": self.lobby_id,
            "state": self.state,
            "current_player_index": self.current_player_index,
            "players": players_data,
            "board": board_data,
            "pending_action": self._pending_action,
            "pending_player": self._pending_player,
            "pending_company": self._pending_company,
            "pending_was_double": self._pending_was_double,
            "auction": auction_data,
        }

    @classmethod
    def from_save_dict(cls, data: dict) -> "GameEngine":
        """Reconstruct a GameEngine from a save dict."""
        engine = cls(data.get("lobby_id", "restored"))
        engine.state = data.get("state", "lobby")
        engine.current_player_index = data.get("current_player_index", 0)
        engine._pending_action = data.get("pending_action")
        engine._pending_player = data.get("pending_player")
        engine._pending_company = data.get("pending_company")
        engine._pending_was_double = data.get("pending_was_double", False)
        engine._auction = data.get("auction")

        for pd in data.get("players", []):
            p = Player(
                name=pd["name"],
                color=pd["color"],
                balance=pd.get("balance", 1500),
                position=pd.get("position", 0),
                in_jail_turns=pd.get("in_jail_turns", 0),
                doubles_rolled=pd.get("doubles_rolled", 0),
                character_id=pd.get("character_id"),
                ready=pd.get("ready", False),
                owned_company_names=list(pd.get("owned_company_names", [])),
            )
            p.color_counts = dict(pd.get("color_counts", p.color_counts))
            p.upgrade_used_this_turn = dict(pd.get("upgrade_used_this_turn", p.upgrade_used_this_turn))
            engine.players.append(p)

        saved_board = data.get("board", [])
        if saved_board:
            for saved_cell in saved_board:
                idx = saved_cell.get("board_index")
                if idx is None or idx >= len(engine.board):
                    continue
                cell = engine.board[idx]
                if isinstance(cell, Company) and "price" in saved_cell:
                    cell.owner_id = saved_cell.get("owner_id")
                    cell.count_stars = saved_cell.get("count_stars", 0)
                    cell.mortgage_count = saved_cell.get("mortgage_count", -1)
                    cell.rent = saved_cell.get("rent", cell.initial_rent)

        return engine

    # ---- Helpers ----
    def _get_player(self, name: str) -> Player | None:
        for p in self.players:
            if p.name == name:
                return p
        return None

    def _get_company(self, name: str) -> Company | None:
        for cell in self.board:
            if isinstance(cell, Company) and cell.name == name:
                return cell
        return None

    def _current_player(self) -> Player:
        return self.players[self.current_player_index]

    def _has_monopoly(self, player: Player, color: str) -> bool:
        needed = COLOR_SET_SIZE.get(color, 0)
        return needed > 0 and player.color_counts.get(color, 0) >= needed

    def _recalc_rent(self, company: Company) -> None:
        if company.type != "company" or not company.owner_id:
            return
        owner = self._get_player(company.owner_id)
        if not owner:
            return
        if company.mortgage_count >= 0:
            company.rent = 0
            return
        base = RENT_TABLE[company.name][company.count_stars]
        if company.count_stars == 0 and self._has_monopoly(owner, company.color):
            base *= 2
        company.rent = base

    def _recalc_car_rents(self, owner: Player) -> None:
        count = owner.color_counts.get("cars", 0)
        rent_val = CAR_RENT_BY_COUNT.get(count, 25)
        for cell in self.board:
            if isinstance(cell, Company) and cell.type == "car" and cell.owner_id == owner.name:
                cell.rent = rent_val

    # ---- Public action dispatcher ----
    def handle_action(self, player_name: str, action: str, data: dict | None = None) -> list[dict]:
        data = data or {}
        if action == "add_player":
            return self._add_player(data.get("name", ""), data.get("color"))
        if action == "select_character":
            return self._select_character(player_name, data.get("character_id", ""))
        if action == "ready_up":
            return self._ready_up(player_name)
        if action == "unready":
            return self._unready(player_name)
        if action == "start_game":
            return self._start_game()
        if self.state != "active":
            return [{"type": "error", "message": "Game is not active."}]

        # Auction actions can come from any participant
        if self._pending_action == "auction":
            if action == "auction_bid":
                return self._auction_bid(player_name)
            if action == "auction_pass":
                return self._auction_pass(player_name)
            return [{"type": "error", "message": "Auction in progress. Bid or pass."}]

        # Buy/casino pending: only the pending player can act
        if self._pending_action in ("buy_decision", "casino_decision"):
            if player_name != self._pending_player:
                return [{"type": "error", "message": "Waiting for another player's decision."}]
            if self._pending_action == "buy_decision":
                if action == "buy_property":
                    return self._buy_property(player_name, data.get("accept", False))
                return [{"type": "error", "message": "You must buy or pass."}]
            if self._pending_action == "casino_decision":
                if action == "casino_play":
                    return self._casino_play(player_name, data.get("guess", 0))
                if action == "casino_skip":
                    return self._casino_skip(player_name)
                return [{"type": "error", "message": "You must play or skip casino."}]

        cp = self._current_player()
        if player_name != cp.name:
            return [{"type": "error", "message": "Not your turn."}]

        if action == "roll_dice":
            return self._roll_dice(cp)
        if action == "jail_pay":
            return self._jail_pay(cp)
        if action == "upgrade":
            return self._upgrade(cp, data.get("company_name", ""))
        if action == "sell_star":
            return self._sell_star(cp, data.get("company_name", ""))
        if action == "mortgage":
            return self._mortgage(cp, data.get("company_name", ""))
        if action == "lift_mortgage":
            return self._lift_mortgage(cp, data.get("company_name", ""))
        if action == "negotiate":
            return self._negotiate(cp, data)
        if action == "resign":
            return self._resign(cp)
        return [{"type": "error", "message": f"Unknown action: {action}"}]

    # ---- Lobby actions ----
    def _add_player(self, name: str, color: str | None = None) -> list[dict]:
        if self.state != "lobby":
            return [{"type": "error", "message": "Can only add players in lobby."}]
        if not name:
            return [{"type": "error", "message": "Name is required."}]
        if self._get_player(name):
            return [{"type": "error", "message": "Name already taken."}]
        if len(self.players) >= 6:
            return [{"type": "error", "message": "Max 6 players."}]
        c = color or COLORS[len(self.players) % len(COLORS)]
        self.players.append(Player(name=name, color=c))
        return [{"type": "player_joined", "player": name, "color": c}]

    def _select_character(self, player_name: str, character_id: str) -> list[dict]:
        if self.state != "lobby":
            return [{"type": "error", "message": "Can only select characters in lobby."}]
        player = self._get_player(player_name)
        if not player:
            return [{"type": "error", "message": "Player not found."}]
        if not character_id:
            return [{"type": "error", "message": "Character ID is required."}]
        valid_ids = {c["id"] for c in self.characters}
        if valid_ids and character_id not in valid_ids:
            return [{"type": "error", "message": "Invalid character."}]
        for p in self.players:
            if p.character_id == character_id and p.name != player_name:
                return [{"type": "error", "message": "Character already taken."}]
        player.character_id = character_id
        player.ready = False
        return [{"type": "character_selected", "player": player_name, "character_id": character_id}]

    def _ready_up(self, player_name: str) -> list[dict]:
        if self.state != "lobby":
            return [{"type": "error", "message": "Can only ready up in lobby."}]
        player = self._get_player(player_name)
        if not player:
            return [{"type": "error", "message": "Player not found."}]
        if not player.character_id:
            return [{"type": "error", "message": "Select a character first."}]
        player.ready = True
        return [{"type": "player_ready", "player": player_name}]

    def _unready(self, player_name: str) -> list[dict]:
        if self.state != "lobby":
            return [{"type": "error", "message": "Can only unready in lobby."}]
        player = self._get_player(player_name)
        if not player:
            return [{"type": "error", "message": "Player not found."}]
        player.ready = False
        return [{"type": "player_unready", "player": player_name}]

    def _start_game(self) -> list[dict]:
        if self.state == "active":
            return [{"type": "error", "message": "Game already active."}]
        if len(self.players) < 2:
            return [{"type": "error", "message": "Need at least 2 players."}]
        for p in self.players:
            if not p.character_id:
                return [{"type": "error", "message": f"{p.name} has not selected a character."}]
            if not p.ready:
                return [{"type": "error", "message": f"{p.name} is not ready."}]
        self.state = "active"
        self.current_player_index = 0
        return [{"type": "game_started", "current_player": self._current_player().name}]

    # ---- Turn actions ----
    def _roll_dice(self, player: Player) -> list[dict]:
        self._update_mortgages(player)
        player.reset_upgrade_flags()

        d1 = randint(1, 6)
        d2 = randint(1, 6)
        events: list[dict] = [{"type": "dice_rolled", "player": player.name, "d1": d1, "d2": d2}]
        is_double = d1 == d2

        if player.in_jail_turns > 0:
            if is_double:
                player.in_jail_turns = 0
                player.doubles_rolled = 0
                events.append({"type": "jail_free_doubles", "player": player.name})
            else:
                player.in_jail_turns -= 1
                if player.in_jail_turns == 0:
                    player.balance -= 50
                    events.append({"type": "jail_expired", "player": player.name, "message": "Forced to pay 50 after 3 turns."})
                else:
                    events.append({"type": "jail_stay", "player": player.name, "turns_left": player.in_jail_turns})
                    self._advance_turn()
                    return events
            total = d1 + d2
            events.extend(self._move_player(player, total, d1 + d2))
            if not self._pending_action:
                self._advance_turn()
            return events

        if is_double:
            player.doubles_rolled += 1
            events.append({"type": "doubles", "player": player.name, "count": player.doubles_rolled})
            if player.doubles_rolled >= 3:
                self._go_to_jail(player)
                player.doubles_rolled = 0
                events.append({"type": "jail", "player": player.name, "reason": "Rolled 3 doubles in a row."})
                self._advance_turn()
                return events
        else:
            player.doubles_rolled = 0

        total = d1 + d2
        events.extend(self._move_player(player, total, d1 + d2))

        if self._pending_action:
            self._pending_was_double = is_double
        elif not is_double:
            self._advance_turn()
        return events

    def _jail_pay(self, player: Player) -> list[dict]:
        if player.in_jail_turns <= 0:
            return [{"type": "error", "message": "Not in jail."}]
        player.balance -= 50
        player.in_jail_turns = 0
        events: list[dict] = [{"type": "jail_paid", "player": player.name}]
        return events

    def _move_player(self, player: Player, steps: int, dice_total: int) -> list[dict]:
        events: list[dict] = []
        old_pos = player.position
        new_pos = old_pos + steps
        if new_pos >= 40:
            player.balance += 200
            events.append({"type": "passed_start", "player": player.name, "bonus": 200})
            new_pos %= 40
        player.position = new_pos
        cell = self.board[new_pos]
        events.append({"type": "moved", "player": player.name, "position": new_pos, "cell": cell.name})
        events.extend(self._land_on_cell(player, cell, dice_total))
        return events

    def _land_on_cell(self, player: Player, cell: Cell, dice_total: int) -> list[dict]:
        if isinstance(cell, Company):
            return self._land_on_company(player, cell, dice_total)
        elif isinstance(cell, Tax):
            return self._land_on_tax(player, cell)
        elif isinstance(cell, Chance):
            return self._land_on_chance(player, cell, dice_total)
        elif isinstance(cell, SpecialCell):
            return self._land_on_special(player, cell)
        return []

    def _land_on_company(self, player: Player, company: Company, dice_total: int) -> list[dict]:
        if company.owner_id is None:
            self._pending_action = "buy_decision"
            self._pending_player = player.name
            self._pending_company = company.name
            return [{"type": "buy_option", "player": player.name, "company": company.name, "price": company.price}]
        if company.owner_id == player.name or company.mortgage_count >= 0:
            return []
        owner = self._get_player(company.owner_id)
        if not owner:
            return []
        if company.type == "videogame":
            vg_count = owner.color_counts.get("videogame", 0)
            rent = dice_total * (4 if vg_count == 1 else 10)
        else:
            rent = company.rent
        player.balance -= rent
        owner.balance += rent
        return [{"type": "rent_paid", "player": player.name, "owner": owner.name, "amount": rent, "company": company.name}]

    def _land_on_tax(self, player: Player, tax: Tax) -> list[dict]:
        player.balance -= tax.amount
        return [{"type": "tax_paid", "player": player.name, "amount": tax.amount}]

    def _land_on_chance(self, player: Player, chance: Chance, dice_total: int) -> list[dict]:
        card = chance.draw()
        events: list[dict] = [{"type": "chance_card", "player": player.name, "card_type": card.type, "text": card.text, "amount": card.amount}]
        if card.type == "earn":
            player.balance += card.amount
        elif card.type == "pay":
            player.balance -= card.amount
        elif card.type == "move":
            if player.position > card.destination:
                player.balance += 200
                events.append({"type": "passed_start", "player": player.name, "bonus": 200})
            player.position = card.destination
            dest_cell = self.board[card.destination]
            events.append({"type": "moved", "player": player.name, "position": card.destination, "cell": dest_cell.name})
            if isinstance(dest_cell, Company):
                events.extend(self._land_on_company(player, dest_cell, dice_total))
        elif card.type == "jail":
            self._go_to_jail(player)
            events.append({"type": "jail", "player": player.name, "reason": card.text})
        return events

    def _land_on_special(self, player: Player, cell: SpecialCell) -> list[dict]:
        if cell.type == "start":
            player.balance += 100
            return [{"type": "start_bonus", "player": player.name, "bonus": 100}]
        if cell.type == "prison":
            self._go_to_jail(player)
            return [{"type": "jail", "player": player.name, "reason": "Landed on Prison."}]
        if cell.type == "casino":
            self._pending_action = "casino_decision"
            self._pending_player = player.name
            return [{"type": "casino_option", "player": player.name, "cost": 100}]
        return []

    def _casino_play(self, player_name: str, guess: int) -> list[dict]:
        if self._pending_action != "casino_decision":
            return [{"type": "error", "message": "No casino pending."}]
        player = self._get_player(player_name)
        if not player:
            return [{"type": "error", "message": "Player not found."}]
        self._clear_pending()
        if guess < 1 or guess > 6:
            return [{"type": "error", "message": "Guess must be 1-6."}]
        player.balance -= 100
        roll = randint(1, 6)
        events: list[dict] = [{"type": "casino_result", "player": player.name, "guess": guess, "roll": roll}]
        if guess == roll:
            player.balance += 600
            events.append({"type": "casino_win", "player": player.name, "amount": 600})
        else:
            events.append({"type": "casino_loss", "player": player.name})
        events.extend(self._finish_pending_turn(player))
        return events

    def _casino_skip(self, player_name: str) -> list[dict]:
        player = self._get_player(player_name)
        if not player:
            return [{"type": "error", "message": "Player not found."}]
        self._clear_pending()
        events: list[dict] = [{"type": "casino_skipped", "player": player.name}]
        events.extend(self._finish_pending_turn(player))
        return events

    # ---- Property management ----
    def _buy_property(self, player_name: str, accept: bool) -> list[dict]:
        if self._pending_action != "buy_decision":
            return [{"type": "error", "message": "No buy pending."}]
        player = self._get_player(player_name)
        company = self._get_company(self._pending_company or "")
        if not player or not company:
            self._clear_pending()
            return [{"type": "error", "message": "Invalid state."}]

        if not accept:
            self._clear_pending()
            events: list[dict] = [{"type": "buy_declined", "player": player.name, "company": company.name}]
            events.extend(self._start_auction(company, player.name))
            return events

        if player.balance < company.price:
            return [{"type": "error", "message": "Not enough money."}]

        was_double = self._pending_was_double
        self._clear_pending()
        player.balance -= company.price
        company.owner_id = player.name
        player.owned_company_names.append(company.name)
        if company.type == "company":
            player.color_counts[company.color] = player.color_counts.get(company.color, 0) + 1
            self._recalc_color_rents(player, company.color)
        elif company.type == "car":
            player.color_counts["cars"] = player.color_counts.get("cars", 0) + 1
            self._recalc_car_rents(player)
        elif company.type == "videogame":
            player.color_counts["videogame"] = player.color_counts.get("videogame", 0) + 1
        events = [{"type": "property_bought", "player": player.name, "company": company.name, "price": company.price}]
        if not was_double:
            self._advance_turn()
        return events

    def _recalc_color_rents(self, owner: Player, color: str) -> None:
        for cell in self.board:
            if isinstance(cell, Company) and cell.color == color and cell.owner_id == owner.name:
                self._recalc_rent(cell)

    def _upgrade(self, player: Player, company_name: str) -> list[dict]:
        company = self._get_company(company_name)
        if not company or company.owner_id != player.name:
            return [{"type": "error", "message": "You don't own this property."}]
        if company.type != "company":
            return [{"type": "error", "message": "Can only upgrade regular properties."}]
        if not self._has_monopoly(player, company.color):
            return [{"type": "error", "message": "Need complete color set."}]
        if player.upgrade_used_this_turn.get(company.color, False):
            return [{"type": "error", "message": "Already upgraded this color set this turn."}]
        if company.count_stars >= 5:
            return [{"type": "error", "message": "Max 5 stars."}]
        if player.balance < company.fee:
            return [{"type": "error", "message": "Not enough money."}]
        player.balance -= company.fee
        company.count_stars += 1
        player.upgrade_used_this_turn[company.color] = True
        self._recalc_rent(company)
        return [{"type": "upgraded", "player": player.name, "company": company_name, "stars": company.count_stars, "new_rent": company.rent}]

    def _sell_star(self, player: Player, company_name: str) -> list[dict]:
        company = self._get_company(company_name)
        if not company or company.owner_id != player.name:
            return [{"type": "error", "message": "You don't own this property."}]
        if company.count_stars <= 0:
            return [{"type": "error", "message": "No stars to sell."}]
        company.count_stars -= 1
        player.balance += company.fee
        self._recalc_rent(company)
        return [{"type": "star_sold", "player": player.name, "company": company_name, "stars": company.count_stars, "refund": company.fee}]

    def _mortgage(self, player: Player, company_name: str) -> list[dict]:
        company = self._get_company(company_name)
        if not company or company.owner_id != player.name:
            return [{"type": "error", "message": "You don't own this."}]
        if company.mortgage_count >= 0:
            return [{"type": "error", "message": "Already mortgaged."}]
        for cell in self.board:
            if isinstance(cell, Company) and cell.color == company.color and cell.owner_id == player.name and cell.count_stars > 0:
                return [{"type": "error", "message": "Sell all stars in color set first."}]
        company.mortgage_count = 15
        company.rent = 0
        payout = company.price // 2
        player.balance += payout
        return [{"type": "mortgaged", "player": player.name, "company": company_name, "payout": payout}]

    def _lift_mortgage(self, player: Player, company_name: str) -> list[dict]:
        company = self._get_company(company_name)
        if not company or company.owner_id != player.name:
            return [{"type": "error", "message": "You don't own this."}]
        if company.mortgage_count < 0:
            return [{"type": "error", "message": "Not mortgaged."}]
        cost = math.ceil((company.price / 2) * 1.1)
        if player.balance < cost:
            return [{"type": "error", "message": "Not enough money."}]
        player.balance -= cost
        company.mortgage_count = -1
        self._recalc_rent(company)
        return [{"type": "mortgage_lifted", "player": player.name, "company": company_name, "cost": cost}]

    def _negotiate(self, player: Player, data: dict) -> list[dict]:
        target = self._get_player(data.get("target", ""))
        if not target or target.name == player.name:
            return [{"type": "error", "message": "Invalid target."}]
        offer_cash = int(data.get("offer_cash", 0))
        want_cash = int(data.get("want_cash", 0))
        offer_companies = data.get("offer_companies", [])
        want_companies = data.get("want_companies", [])
        if offer_cash < 0 or want_cash < 0:
            return [{"type": "error", "message": "Cash cannot be negative."}]
        if offer_cash > player.balance or want_cash > target.balance:
            return [{"type": "error", "message": "Not enough balance."}]
        accepted = data.get("accepted", False)
        if not accepted:
            return [{"type": "trade_proposed", "from": player.name, "to": target.name,
                      "offer_cash": offer_cash, "want_cash": want_cash,
                      "offer_companies": offer_companies, "want_companies": want_companies}]
        player.balance += want_cash - offer_cash
        target.balance += offer_cash - want_cash
        for cn in want_companies:
            self._transfer_company(target, player, cn)
        for cn in offer_companies:
            self._transfer_company(player, target, cn)
        return [{"type": "trade_completed", "from": player.name, "to": target.name}]

    def _transfer_company(self, from_p: Player, to_p: Player, company_name: str) -> None:
        company = self._get_company(company_name)
        if not company:
            return
        from_p.owned_company_names.remove(company_name)
        if company.type == "company":
            from_p.color_counts[company.color] -= 1
            self._recalc_color_rents(from_p, company.color)
        elif company.type == "car":
            from_p.color_counts["cars"] -= 1
            self._recalc_car_rents(from_p)
        elif company.type == "videogame":
            from_p.color_counts["videogame"] -= 1

        company.owner_id = to_p.name
        to_p.owned_company_names.append(company_name)
        if company.type == "company":
            to_p.color_counts[company.color] = to_p.color_counts.get(company.color, 0) + 1
            self._recalc_color_rents(to_p, company.color)
        elif company.type == "car":
            to_p.color_counts["cars"] = to_p.color_counts.get("cars", 0) + 1
            self._recalc_car_rents(to_p)
        elif company.type == "videogame":
            to_p.color_counts["videogame"] = to_p.color_counts.get("videogame", 0) + 1

    def _resign(self, player: Player) -> list[dict]:
        for cn in list(player.owned_company_names):
            comp = self._get_company(cn)
            if comp:
                comp.owner_id = None
                comp.rent = comp.initial_rent
                comp.count_stars = 0
                comp.mortgage_count = -1
        self.players.remove(player)
        if self.current_player_index >= len(self.players):
            self.current_player_index = 0
        events: list[dict] = [{"type": "player_resigned", "player": player.name}]
        events.extend(self._check_winner())
        return events

    # ---- Internal helpers ----
    def _clear_pending(self) -> None:
        was = self._pending_action
        self._pending_action = None
        self._pending_player = None
        self._pending_company = None

    def _finish_pending_turn(self, player: Player) -> list[dict]:
        was_double = self._pending_was_double
        self._pending_was_double = False
        if not was_double:
            self._advance_turn()
        return self._check_winner()

    # ---- Auction ----
    def _start_auction(self, company: Company, decliner_name: str) -> list[dict]:
        participants = [p.name for p in self.players if p.name != decliner_name]
        if not participants:
            events = self._finish_pending_turn(self._get_player(decliner_name) or self.players[0])
            return [{"type": "auction_skipped", "company": company.name, "reason": "No other players."}] + events
        self._pending_action = "auction"
        self._auction = {
            "company": company.name,
            "price": company.price + 10,
            "bidder_idx": 0,
            "participants": participants,
            "highest_bidder": None,
            "decliner": decliner_name,
        }
        return [{"type": "auction_started", "company": company.name, "starting_price": company.price + 10,
                 "participants": participants, "current_bidder": participants[0]}]

    def _auction_bid(self, player_name: str) -> list[dict]:
        a = self._auction
        if not a:
            return [{"type": "error", "message": "No auction."}]
        if a["participants"][a["bidder_idx"]] != player_name:
            return [{"type": "error", "message": "Not your turn to bid."}]
        bidder = self._get_player(player_name)
        if not bidder or bidder.balance < a["price"]:
            return self._auction_pass(player_name)
        a["highest_bidder"] = player_name
        events: list[dict] = [{"type": "auction_bid", "player": player_name, "amount": a["price"]}]
        a["price"] += 10
        a["bidder_idx"] = (a["bidder_idx"] + 1) % len(a["participants"])
        if len(a["participants"]) == 1:
            events.extend(self._resolve_auction())
            return events
        return events + [{"type": "auction_next", "current_bidder": a["participants"][a["bidder_idx"]],
                          "current_price": a["price"]}]

    def _auction_pass(self, player_name: str) -> list[dict]:
        a = self._auction
        if not a:
            return [{"type": "error", "message": "No auction."}]
        if a["participants"][a["bidder_idx"]] != player_name:
            return [{"type": "error", "message": "Not your turn to bid."}]
        events: list[dict] = [{"type": "auction_pass", "player": player_name}]
        a["participants"].remove(player_name)
        if not a["participants"]:
            events.extend(self._resolve_auction())
            return events
        if a["bidder_idx"] >= len(a["participants"]):
            a["bidder_idx"] = 0
        if len(a["participants"]) == 1 and a["highest_bidder"]:
            events.extend(self._resolve_auction())
            return events
        events.append({"type": "auction_next", "current_bidder": a["participants"][a["bidder_idx"]],
                        "current_price": a["price"]})
        return events

    def _resolve_auction(self) -> list[dict]:
        a = self._auction
        if not a:
            return []
        company = self._get_company(a["company"])
        winner_name = a["highest_bidder"]
        decliner_name = a["decliner"]
        self._auction = None
        self._pending_action = None
        decliner = self._get_player(decliner_name)

        if not winner_name or not company:
            events: list[dict] = [{"type": "auction_no_winner", "company": a["company"]}]
            if decliner:
                events.extend(self._finish_pending_turn(decliner))
            return events

        winner = self._get_player(winner_name)
        if not winner:
            events = [{"type": "auction_no_winner", "company": a["company"]}]
            if decliner:
                events.extend(self._finish_pending_turn(decliner))
            return events

        final_price = a["price"] - 10
        winner.balance -= final_price
        company.owner_id = winner.name
        winner.owned_company_names.append(company.name)
        if company.type == "company":
            winner.color_counts[company.color] = winner.color_counts.get(company.color, 0) + 1
            self._recalc_color_rents(winner, company.color)
        elif company.type == "car":
            winner.color_counts["cars"] = winner.color_counts.get("cars", 0) + 1
            self._recalc_car_rents(winner)
        elif company.type == "videogame":
            winner.color_counts["videogame"] = winner.color_counts.get("videogame", 0) + 1

        events = [{"type": "auction_won", "player": winner.name, "company": company.name, "price": final_price}]
        if decliner:
            events.extend(self._finish_pending_turn(decliner))
        return events

    def _go_to_jail(self, player: Player) -> None:
        player.in_jail_turns = 3
        player.position = 10

    def _advance_turn(self) -> None:
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def _check_winner(self) -> list[dict]:
        if len(self.players) == 1:
            self.state = "gameover"
            return [{"type": "game_over", "winner": self.players[0].name}]
        if len(self.players) == 0:
            self.state = "gameover"
            return [{"type": "game_over", "winner": None}]
        return []

    def _update_mortgages(self, player: Player) -> None:
        to_remove = []
        for cn in player.owned_company_names:
            comp = self._get_company(cn)
            if not comp:
                continue
            if comp.mortgage_count == 0:
                to_remove.append(cn)
            elif comp.mortgage_count > 0:
                comp.mortgage_count -= 1
        for cn in to_remove:
            comp = self._get_company(cn)
            if comp:
                comp.owner_id = None
                comp.rent = comp.initial_rent
                comp.count_stars = 0
                comp.mortgage_count = -1
                player.owned_company_names.remove(cn)
                if comp.type == "company":
                    player.color_counts[comp.color] -= 1
