"""
Board factory — builds the 40-cell Monopoly board. Pure data, no I/O.
"""

from .cells import Cell, Company, Chance, Tax, SpecialCell


def create_board() -> list[Cell]:
    return [
        SpecialCell("Start", 0, type="start"),

        Company("Chanel", 1, price=60, type="company", rent=2, fee=50, color="brown"),
        Chance("Chance", 2),
        Company("Givenchy", 3, price=60, type="company", rent=4, fee=50, color="brown"),
        Tax("Tax", 4, amount=200),
        Company("Audi", 5, price=200, type="car", rent=25),
        Company("Adidas", 6, price=100, type="company", rent=6, fee=50, color="pink"),
        Chance("Chance", 7),
        Company("Puma", 8, price=100, type="company", rent=6, fee=50, color="pink"),
        Company("Lacoste", 9, price=120, type="company", rent=8, fee=50, color="pink"),
        SpecialCell("PrisonVisit", 10, type="visit"),

        Company("Skype", 11, price=140, type="company", rent=10, fee=100, color="purple"),
        Company("Rockstar", 12, price=150, type="videogame", rent=0),
        Company("Facebook", 13, price=140, type="company", rent=10, fee=100, color="purple"),
        Company("Twitter", 14, price=160, type="company", rent=12, fee=100, color="purple"),
        Company("Mercedes", 15, price=200, type="car", rent=25),
        Company("Coca-Cola", 16, price=180, type="company", rent=14, fee=100, color="orange"),
        Chance("Chance", 17),
        Company("Pepsi", 18, price=180, type="company", rent=14, fee=100, color="orange"),
        Company("Fanta", 19, price=200, type="company", rent=16, fee=100, color="orange"),
        SpecialCell("Casino", 20, type="casino"),

        Company("Lufthansa", 21, price=220, type="company", rent=18, fee=150, color="red"),
        Chance("Chance", 22),
        Company("KLM", 23, price=220, type="company", rent=18, fee=150, color="red"),
        Company("Scat", 24, price=240, type="company", rent=20, fee=150, color="red"),
        Company("Ford", 25, price=200, type="car", rent=25),
        Company("Hardee's", 26, price=260, type="company", rent=22, fee=150, color="yellow"),
        Company("Subway", 27, price=260, type="company", rent=24, fee=150, color="yellow"),
        Company("Valve", 28, price=150, type="videogame", rent=0),
        Company("KFC", 29, price=280, type="company", rent=26, fee=150, color="yellow"),
        SpecialCell("Prison", 30, type="prison"),

        Company("Radisson", 31, price=300, type="company", rent=28, fee=200, color="green"),
        Company("Novotel", 32, price=300, type="company", rent=28, fee=200, color="green"),
        Chance("Chance", 33),
        Company("Hilton", 34, price=320, type="company", rent=30, fee=200, color="green"),
        Company("Toyota", 35, price=200, type="car", rent=25),
        Tax("Tax", 36, amount=100),
        Company("Samsung", 37, price=350, type="company", rent=35, fee=200, color="blue"),
        Chance("Chance", 38),
        Company("Apple", 39, price=500, type="company", rent=50, fee=200, color="blue"),
    ]
