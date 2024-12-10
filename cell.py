class Cell:
    def __init__(self, name):
        self.name = name

class Company(Cell):
    def __init__(self, name, price, type_, owned = False): #type can be either company or video game(komunalka, vokzal)
        super().__init__(name)
        self.price = price
        self.type = type_
        self.owned = owned

class ShansCard:
    def __init__(self, type_, amount = 0, destination = "", text = ""):
        self.type_ = type_
        self.amount = amount
        self.destination = destination
        self.text = text

class Shans(Cell):
    def __init__(self):
        super().__init__("Shans")
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
            ShansCard("move", "Chanel", "You take a casual stroll!"),
            ShansCard("move", "Hugo Boss", "You take a casual stroll!"),
            ShansCard("move", "Audi", "You take a casual stroll!"),
            ShansCard("move", "Adidas", "You take a casual stroll!"),
            ShansCard("move", "Puma", "You take a casual stroll!"),
            ShansCard("move", "Lacoste", "You take a casual stroll!"),
            ShansCard("move", "Skype", "You take a casual stroll!"),
            ShansCard("move", "Rockstar", "You take a casual stroll!"),
            ShansCard("move", "Facebook", "You take a casual stroll!"),
            ShansCard("move", "Twitter", "You take a casual stroll!"),
            ShansCard("move", "Mercedes", "You take a casual stroll!"),
            ShansCard("move", "Coca-Cola", "You take a casual stroll!"),
            ShansCard("move", "Pepsi", "You take a casual stroll!"),
            ShansCard("move", "Fanta", "You take a casual stroll!"),
            ShansCard("move", "Air Astana", "You take a casual stroll!"),
            ShansCard("move", "Fly Arystan", "You take a casual stroll!"),
            ShansCard("move", "Scat", "You take a casual stroll!"),
            ShansCard("move", "Ford", "You take a casual stroll!"),
            ShansCard("move", "Im Cafe", "You take a casual stroll!"),
            ShansCard("move", "Burger King", "You take a casual stroll!"),
            ShansCard("move", "Valve", "You take a casual stroll!"),
            ShansCard("move", "KFC", "You take a casual stroll!"),
            ShansCard("move", "Radisson", "You take a casual stroll!"),
            ShansCard("move", "Novotel", "You take a casual stroll!"),
            ShansCard("move", "Hilton", "You take a casual stroll!"),
            ShansCard("move", "Toyota", "You take a casual stroll!"),
            ShansCard("move", "Samsung", "You take a casual stroll!"),
            ShansCard("move", "Apple", "You take a casual stroll!"),
        ]

    def getArr(self) :
        return self.arr


class Tax(Cell):
    def __init__(self, amount):
        super().__init__("Tax")
        self.amount = amount

class RandomCell(Cell):
    def __init__(self, name, type_):
        super().__init__(name)
        self.type = type_

# class CellFactory:
#     @staticmethod
#     def create_cell(cell_type):
#         if cell_type % 5 == 0:  # For demo purposes
#             return Company(f"Company-{cell_type}", 200 + cell_type * 10, "Blue")
#         elif cell_type % 7 == 0:
#             return Tax(100)
#         else:
#             return Shans()