"""
Player state. Pure data — no I/O.
"""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Player:
    name: str
    color: str
    balance: int = 1500
    position: int = 0
    in_jail_turns: int = 0      # 0 = free, >0 = turns remaining in jail
    doubles_rolled: int = 0
    owned_company_names: list[str] = field(default_factory=list)

    color_counts: dict[str, int] = field(default_factory=lambda: {
        "brown": 0, "pink": 0, "purple": 0, "orange": 0,
        "red": 0, "yellow": 0, "green": 0, "blue": 0,
        "cars": 0, "videogame": 0,
    })

    upgrade_used_this_turn: dict[str, bool] = field(default_factory=lambda: {
        "brown": False, "pink": False, "purple": False, "orange": False,
        "red": False, "yellow": False, "green": False, "blue": False,
    })

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "color": self.color,
            "balance": self.balance,
            "position": self.position,
            "in_jail_turns": self.in_jail_turns,
            "doubles_rolled": self.doubles_rolled,
            "owned_company_names": list(self.owned_company_names),
            "color_counts": dict(self.color_counts),
        }

    def reset_upgrade_flags(self) -> None:
        for key in self.upgrade_used_this_turn:
            self.upgrade_used_this_turn[key] = False
