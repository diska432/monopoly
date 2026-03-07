"""
Data-driven rent tables for all properties.

Each entry maps company_name -> list of rents indexed by star count [0..5].
Index 0 = base rent (no monopoly), index 1 = 1 star, ..., index 5 = 5 stars.
The monopoly (doubled) base rent is computed dynamically and not stored here.
"""

RENT_TABLE: dict[str, list[int]] = {
    # Brown (2 to complete set)
    "Chanel":    [2, 10, 30, 90, 160, 250],
    "Givenchy":  [4, 20, 60, 180, 320, 450],

    # Pink (3 to complete set)
    "Adidas":    [6, 30, 90, 270, 400, 600],
    "Puma":      [6, 30, 90, 270, 400, 600],
    "Lacoste":   [8, 40, 100, 300, 450, 550],

    # Purple (3 to complete set)
    "Skype":     [10, 50, 150, 450, 625, 750],
    "Facebook":  [10, 50, 150, 450, 625, 750],
    "Twitter":   [12, 60, 180, 500, 700, 900],

    # Orange (3 to complete set)
    "Coca-Cola": [14, 60, 200, 550, 750, 950],
    "Pepsi":     [14, 60, 200, 550, 750, 950],
    "Fanta":     [16, 80, 220, 600, 800, 1000],

    # Red (3 to complete set)
    "Lufthansa": [18, 90, 250, 700, 875, 1050],
    "KLM":       [18, 90, 250, 700, 875, 1050],
    "Scat":      [20, 100, 300, 750, 925, 1100],

    # Yellow (3 to complete set)
    "Hardee's":  [22, 110, 330, 800, 975, 1150],
    "Subway":    [24, 110, 330, 800, 975, 1150],
    "KFC":       [26, 120, 360, 850, 1025, 1200],

    # Green (3 to complete set)
    "Radisson":  [28, 130, 390, 900, 1100, 1275],
    "Novotel":   [28, 130, 390, 900, 1100, 1275],
    "Hilton":    [30, 150, 450, 1000, 1200, 1400],

    # Blue (2 to complete set)
    "Samsung":   [35, 175, 500, 1100, 1300, 1500],
    "Apple":     [50, 200, 600, 1400, 1700, 2000],
}

CAR_RENT_BY_COUNT: dict[int, int] = {1: 25, 2: 50, 3: 100, 4: 200}

COLOR_SET_SIZE: dict[str, int] = {
    "brown": 2, "pink": 3, "purple": 3, "orange": 3,
    "red": 3, "yellow": 3, "green": 3, "blue": 2,
}

COLOR_PROPERTIES: dict[str, list[str]] = {
    "brown": ["Chanel", "Givenchy"],
    "pink": ["Adidas", "Puma", "Lacoste"],
    "purple": ["Skype", "Facebook", "Twitter"],
    "orange": ["Coca-Cola", "Pepsi", "Fanta"],
    "red": ["Lufthansa", "KLM", "Scat"],
    "yellow": ["Hardee's", "Subway", "KFC"],
    "green": ["Radisson", "Novotel", "Hilton"],
    "blue": ["Samsung", "Apple"],
}


def get_rent(company_name: str, stars: int) -> int:
    return RENT_TABLE[company_name][stars]
