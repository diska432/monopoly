from cell import Cell, Company, Shans, Tax, RandomCell

#need to implement Shans as set of random cards with pay, earn, move logic

class Board:
    def __init__(self):
        self.board = [
            RandomCell("Start", 0, "start"),

            Company("Chanel", 1, 60, "company", 2, 50, "brown"),
            Shans(2),
            Company("Hugo Boss", 3, 60, "company", 4, 50, "brown"),
            Tax(4, 200),
            Company("Audi", 5, 200, "car", 25),
            Company("Adidas",6, 100, "company", 6, 50, "pink"),
            Shans(7),
            Company("Puma", 8, 100, "company", 6, 50, "pink"),
            Company("Lacoste", 9, 120, "company", 8, 50, "pink"),
            RandomCell("PrisonVisit", 10, "visit"),

            Company("Skype", 11, 140, "company", 10, 100, "purple"),
            Company("Rockstar", 12, 150, "videogame", 0),
            Company("Facebook", 13, 140, "company", 10, 100, "purple"),
            Company("Twitter", 14, 160, "company", 12, 100, "purple"),
            Company("Mercedes", 15, 200, "car", 25),
            Company("Coca-Cola", 16, 180, "company", 14, 100, "orange"),
            Shans(17),
            Company("Pepsi", 18, 180, "company", 14, 100, "orange"),
            Company("Fanta", 19, 200, "company", 16, 100, "orange"),
            RandomCell("Casino", 20, "casino"),

            Company("Air Astana", 21, 220, "company", 18, 150, "red"),
            Shans(22),
            Company("Fly Arystan", 23, 220, "company", 18, 150, "red"),
            Company("Scat", 24, 240, "company", 20, 150, "red"),
            Company("Ford", 25, 200, "car", 25),
            Company("Im Cafe", 26, 260, "company", 22, 150, "yellow"),
            Company("Burger King", 27, 260, "company", 24, 150, "yellow"),
            Company("Valve", 28, 150, "videogame", 0),
            Company("KFC", 29, 280, "company", 26, 150, "yellow"),
            RandomCell("Prison", 30, "prison"),

            Company("Radisson", 31, 300, "company", 28, 200, "green"),
            Company("Novotel", 32, 300, "company", 28, 200, "green"),
            Shans(33),
            Company("Hilton", 34, 320, "company", 30, 200, "green"),
            Company("Toyota", 35, 200, "car", 25),
            Tax(36, 100),
            Company("Samsung", 37, 350, "company", 35, 200, "blue"),
            Shans(38),
            Company("Apple", 39, 500, "company", 50, 200, "blue"),
        ]

    def getBoard(self) :
        return self.board