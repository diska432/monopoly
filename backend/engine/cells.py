"""
Board cell types. Pure data — no I/O.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from random import randint
from typing import Optional


@dataclass
class Cell:
    name: str
    board_index: int


@dataclass
class Company(Cell):
    price: int = 0
    type: str = "company"           # "company" | "car" | "videogame"
    rent: int = 0
    fee: int = 0                    # upgrade cost per star
    color: str = ""
    count_stars: int = 0
    mortgage_count: int = -1        # -1 = not mortgaged, >0 = turns left
    initial_rent: int = 0
    owner_id: Optional[str] = None  # player id (name) or None

    def __post_init__(self) -> None:
        if self.initial_rent == 0:
            self.initial_rent = self.rent

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "board_index": self.board_index,
            "price": self.price,
            "type": self.type,
            "rent": self.rent,
            "fee": self.fee,
            "color": self.color,
            "count_stars": self.count_stars,
            "mortgage_count": self.mortgage_count,
            "initial_rent": self.initial_rent,
            "owner_id": self.owner_id,
        }


@dataclass
class ChanceCard:
    type: str               # "earn" | "pay" | "move" | "jail"
    amount: int = 0
    destination: int = 0
    text: str = ""


@dataclass
class Chance(Cell):
    cards: list[ChanceCard] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.cards:
            self.cards = _DEFAULT_CHANCE_CARDS[:]

    def draw(self) -> ChanceCard:
        return self.cards[randint(0, len(self.cards) - 1)]


@dataclass
class Tax(Cell):
    amount: int = 0


@dataclass
class SpecialCell(Cell):
    type: str = ""          # "start" | "visit" | "prison" | "casino"


_DEFAULT_CHANCE_CARDS: list[ChanceCard] = [
    ChanceCard("earn", 100, 0, "Holiday miracle!"),
    ChanceCard("earn", 150, 0, "Bank miscalculation!"),
    ChanceCard("earn", 100, 0, "You won the lottery!"),
    ChanceCard("earn", 50, 0, "Donation!"),
    ChanceCard("earn", 25, 0, "Donation!"),
    ChanceCard("earn", 20, 0, "Donation!"),
    ChanceCard("earn", 10, 0, "Donation!"),
    ChanceCard("earn", 100, 0, "Donation!"),
    ChanceCard("earn", 120, 0, "Donation!"),
    ChanceCard("earn", 40, 0, "Donation!"),
    ChanceCard("pay", 150, 0, "Tuition fees!"),
    ChanceCard("pay", 200, 0, "Mortgage!"),
    ChanceCard("pay", 100, 0, "Taxes!"),
    ChanceCard("pay", 100, 0, "Insurance!"),
    ChanceCard("pay", 25, 0, "Insurance!"),
    ChanceCard("pay", 10, 0, "Insurance!"),
    ChanceCard("pay", 50, 0, "Insurance!"),
    ChanceCard("pay", 40, 0, "Insurance!"),
    ChanceCard("pay", 140, 0, "Insurance!"),
    ChanceCard("pay", 120, 0, "Insurance!"),
    ChanceCard("move", 0, 1, "You take a casual stroll."),
    ChanceCard("move", 0, 3, "You take a casual stroll."),
    ChanceCard("move", 0, 5, "You take a casual stroll."),
    ChanceCard("move", 0, 6, "You take a casual stroll."),
    ChanceCard("move", 0, 8, "You take a casual stroll."),
    ChanceCard("move", 0, 9, "You take a casual stroll."),
    ChanceCard("move", 0, 11, "You take a casual stroll."),
    ChanceCard("move", 0, 12, "You take a casual stroll."),
    ChanceCard("move", 0, 13, "You take a casual stroll."),
    ChanceCard("move", 0, 14, "You take a casual stroll."),
    ChanceCard("move", 0, 15, "You take a casual stroll."),
    ChanceCard("move", 0, 16, "You take a casual stroll."),
    ChanceCard("move", 0, 18, "You take a casual stroll."),
    ChanceCard("move", 0, 19, "You take a casual stroll."),
    ChanceCard("move", 0, 21, "You take a casual stroll."),
    ChanceCard("move", 0, 23, "You take a casual stroll."),
    ChanceCard("move", 0, 24, "You take a casual stroll."),
    ChanceCard("move", 0, 25, "You take a casual stroll."),
    ChanceCard("move", 0, 26, "You take a casual stroll."),
    ChanceCard("move", 0, 27, "You take a casual stroll."),
    ChanceCard("move", 0, 28, "You take a casual stroll."),
    ChanceCard("move", 0, 29, "You take a casual stroll."),
    ChanceCard("move", 0, 31, "You take a casual stroll."),
    ChanceCard("move", 0, 32, "You take a casual stroll."),
    ChanceCard("move", 0, 34, "You take a casual stroll."),
    ChanceCard("move", 0, 35, "You take a casual stroll."),
    ChanceCard("move", 0, 37, "You take a casual stroll."),
    ChanceCard("move", 0, 39, "You take a casual stroll."),
    ChanceCard("jail", 0, 0, "goes straight to jail for bank heist."),
    ChanceCard("jail", 0, 0, "goes straight to jail for a heinous crime."),
]
