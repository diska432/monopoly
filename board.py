from cell import Cell, Company, Shans, Tax, RandomCell

#need to implement Shans as set of random cards with pay, earn, move logic

class Board:
    def __init__(self):
        self.board = [
            RandomCell("Start", "start"),

            Company("Chanel", 60, "company"),
            Shans(),
            Company("Hugo Boss", 60, "company"),
            Tax(200),
            Company("Audi", 200, "car"),
            Company("Adidas", 100, "company"),
            Shans(),
            Company("Puma", 100, "company"),
            Company("Lacoste", 120, "company"),
            RandomCell("PrisonVisit", "visit"),

            Company("Skype", 140, "company"),
            Company("Rockstar", 150, "videogame"),
            Company("Facebook", 140, "company"),
            Company("Twitter", 160, "company"),
            Company("Mercedes", 200, "car"),
            Company("Coca-Cola", 180, "company"),
            Shans(),
            Company("Pepsi", 180, "company"),
            Company("Fanta", 200, "company"),
            RandomCell("Casino", "casino"),

            Company("Air Astana", 220, "company"),
            Shans(),
            Company("Fly Arystan", 220, "company"),
            Company("Scat", 240, "company"),
            Company("Ford", 200, "car"),
            Company("Im Cafe", 260, "company"),
            Company("Burger King", 260, "company"),
            Company("Valve", 150, "videogame"),
            Company("KFC", 280, "company"),
            RandomCell("Prison", "prison"),

            Company("Radisson", 300, "company"),
            Company("Novotel", 300, "company"),
            Shans(),
            Company("Hilton", 320, "company"),
            Company("Toyota", 200, "car"),
            Tax(100),
            Company("Samsung", 350, "company"),
            Shans(),
            Company("Apple", 500, "company"),
        ]

    def getBoard(self) :
        return self.board