class Cell:
    def __init__(self, name, board_index):
        self.name = name
        self.board_index = board_index

class Company(Cell):
    def __init__(self, name, board_index, price, type_, rent, fee = 0, color = ""): 
        super().__init__(name, board_index)
        self.price = price

        #type can be either company or video game
        self.type = type_
        self.owner = None
        self.rent = rent
        self.fee = fee
        self.color = color
        self.countStars = 0
        self.mortgage_count = -1
        self.initial_rent = rent
        
    def __str__(self):
        return f"{self.name} (mortgage: {self.mortgage_count}, fee: {self.fee}, rent: {self.rent})"

class ShansCard:
    def __init__(self, type_, amount = 0, destination = "", text = ""):
        self.type_ = type_
        self.amount = amount
        self.destination = destination
        self.text = text

class Shans(Cell):
    def __init__(self, board_index):
        super().__init__("Shans", board_index)
        self.arr = [
            ShansCard("earn", 100, "",  "Holiday miracle!"),
            ShansCard("earn", 150, "", "Bank miscalculation!"),
            ShansCard("earn", 100, "", "You won the lottery!"),
            ShansCard("earn", 50, "", "Donation!"),
            ShansCard("earn", 25, "", "Donation!"),
            ShansCard("earn", 20, "", "Donation!"),
            ShansCard("earn", 10, "", "Donation!"),
            ShansCard("earn", 100,"", "Donation!"),
            ShansCard("earn", 120, "", "Donation!"),
            ShansCard("earn", 40, "", "Donation!"),
            ShansCard("pay", 150, "", "Tuition fees!"),
            ShansCard("pay", 200, "", "Mortgage!"),
            ShansCard("pay", 100, "", "Taxes!"),
            ShansCard("pay", 100, "", "Insurance!"),
            ShansCard("pay", 25, "", "Insurance!"),
            ShansCard("pay", 10, "", "Insurance!"),
            ShansCard("pay", 50, "", "Insurance!"),
            ShansCard("pay", 40, "", "Insurance!"),
            ShansCard("pay", 140, "", "Insurance!"),
            ShansCard("pay", 120, "", "Insurance!"),
            ShansCard("move", 0, 1, "You take a casual stroll."),
            ShansCard("move", 0, 3, "You take a casual stroll."),
            ShansCard("move", 0, 5, "You take a casual stroll."),
            ShansCard("move", 0, 6, "You take a casual stroll."),
            ShansCard("move", 0, 8, "You take a casual stroll."),
            ShansCard("move", 0, 9, "You take a casual stroll."),
            ShansCard("move", 0, 11, "You take a casual stroll."),
            ShansCard("move", 0, 12, "You take a casual stroll."),
            ShansCard("move", 0, 13, "You take a casual stroll."),
            ShansCard("move", 0, 14, "You take a casual stroll."),
            ShansCard("move", 0, 15, "You take a casual stroll."),
            ShansCard("move", 0, 16, "You take a casual stroll."),
            ShansCard("move", 0, 18, "You take a casual stroll."),
            ShansCard("move", 0, 19, "You take a casual stroll."),
            ShansCard("move", 0, 21, "You take a casual stroll."),
            ShansCard("move", 0, 23, "You take a casual stroll."),
            ShansCard("move", 0, 24, "You take a casual stroll."),
            ShansCard("move", 0, 25, "You take a casual stroll."),
            ShansCard("move", 0, 26, "You take a casual stroll."),
            ShansCard("move", 0, 27, "You take a casual stroll."),
            ShansCard("move", 0, 28, "You take a casual stroll."),
            ShansCard("move", 0, 29, "You take a casual stroll."),
            ShansCard("move", 0, 31, "You take a casual stroll."),
            ShansCard("move", 0, 32, "You take a casual stroll."),
            ShansCard("move", 0, 34, "You take a casual stroll."),
            ShansCard("move", 0, 35, "You take a casual stroll."),
            ShansCard("move", 0, 37, "You take a casual stroll."),
            ShansCard("move", 0, 39, "You take a casual stroll."),
            ShansCard("jail", 0, "", " goes straight to jail for bank heist."),
            ShansCard("jail", 0, "", " goes straight to jail for a heinous crime."),
        ]

    def getArr(self) :
        return self.arr


class Tax(Cell):
    def __init__(self, board_index, amount):
        super().__init__("Tax", board_index)
        self.amount = amount

class RandomCell(Cell):
    def __init__(self, name, board_index, type_):
        super().__init__(name, board_index)
        self.type = type_
