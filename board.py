from cell import Cell, Company, Shans, Tax, RandomCell

#need to implement Shans as set of random cards with pay, earn, move logic

class Board:
    def __init__(self):
        self.board = [
            RandomCell("Start", 0, "start"),

            Company("Chanel", 1, 60, "company"),
            Shans(2),
            Company("Hugo Boss", 3, 60, "company"),
            Tax(4, 200),
            Company("Audi", 5, 200, "car"),
            Company("Adidas",6, 100, "company"),
            Shans(7),
            Company("Puma", 8, 100, "company"),
            Company("Lacoste", 9, 120, "company"),
            RandomCell("PrisonVisit", 10, "visit"),

            Company("Skype", 11, 140, "company"),
            Company("Rockstar", 12, 150, "videogame"),
            Company("Facebook", 13, 140, "company"),
            Company("Twitter", 14, 160, "company"),
            Company("Mercedes", 15, 200, "car"),
            Company("Coca-Cola", 16, 180, "company"),
            Shans(17),
            Company("Pepsi", 18, 180, "company"),
            Company("Fanta", 19, 200, "company"),
            RandomCell("Casino", 20, "casino"),

            Company("Air Astana", 21, 220, "company"),
            Shans(22),
            Company("Fly Arystan", 23, 220, "company"),
            Company("Scat", 24, 240, "company"),
            Company("Ford", 25, 200, "car"),
            Company("Im Cafe", 26, 260, "company"),
            Company("Burger King", 27, 260, "company"),
            Company("Valve", 28, 150, "videogame"),
            Company("KFC", 29, 280, "company"),
            RandomCell("Prison", 30, "prison"),

            Company("Radisson", 31, 300, "company"),
            Company("Novotel", 32, 300, "company"),
            Shans(33),
            Company("Hilton", 34, 320, "company"),
            Company("Toyota", 35, 200, "car"),
            Tax(36, 100),
            Company("Samsung", 37, 350, "company"),
            Shans(38),
            Company("Apple", 39, 500, "company"),
        ]

    def getBoard(self) :
        return self.board