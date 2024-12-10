class Cell:
    def __init__(self, name):
        self.name = name

class Company(Cell):
    def __init__(self, name, price, type_, owned = False): #type can be either company or video game(komunalka, vokzal)
        super().__init__(name)
        self.price = price
        self.type = type_
        self.owned = owned

class Shans(Cell):
    def __init__(self):
        super().__init__("Shans")
        self.arr = [
            {type_: "earn", amount: 100, text: "Holiday miracle!"},
            {type_: "earn", amount: 150, text: "Bank miscalculation!"},
            {type_: "earn", amount: 200, text: "You won the lottery!"},
            {type_: "earn", amount: 50, text: "Donation!"},
            {type_: "earn", amount: 25, text: "Donation!"},
            {type_: "earn", amount: 20, text: "Donation!"},
            {type_: "earn", amount: 10, text: "Donation!"},
            {type_: "earn", amount: 100, text: "Donation!"},
            {type_: "earn", amount: 120, text: "Donation!"},
            {type_: "earn", amount: 40, text: "Donation!"},
            {type_: "pay", amount: 150, text: "You need to pay tuition!"},
            {type_: "pay", amount: 200, text: "You need to pay mortgage!"},
            {type_: "pay", amount: 100, text: "You need to pay more taxes!"},
            {type_: "pay", amount: 120, text: "You need to pay for insurance!"},
            {type_: "pay", amount: 100, text: "You need to pay for insurance!"},
            {type_: "pay", amount: 25, text: "You need to pay for insurance!"},
            {type_: "pay", amount: 10, text: "You need to pay for insurance!"},
            {type_: "pay", amount: 50, text: "You need to pay for insurance!"},
            {type_: "pay", amount: 40, text: "You need to pay for insurance!"},
            {type_: "pay", amount: 20, text: "You need to pay for insurance!"},
            {type_: "pay", amount: 140, text: "You need to pay for insurance!"},
            {type_: "move", destination: "Chanel", text: "You take a casual stroll"},
            {type_: "move", destination: "Hugo Boss", text: "You take a casual stroll"},
            {type_: "move", destination: "Audi", text: "You take a casual stroll"},
            {type_: "move", destination: "Adidas", text: "You take a casual stroll"},
            {type_: "move", destination: "Puma", text: "You take a casual stroll"},
            {type_: "move", destination: "Lacoste", text: "You take a casual stroll"},
            {type_: "move", destination: "Skype", text: "You take a casual stroll"},
            {type_: "move", destination: "Rockstar", text: "You take a casual stroll"},
            {type_: "move", destination: "Facebook", text: "You take a casual stroll"},
            {type_: "move", destination: "Twitter", text: "You take a casual stroll"},
            {type_: "move", destination: "Mercedes", text: "You take a casual stroll"},
            {type_: "move", destination: "Coca-Cola", text: "You take a casual stroll"},
            {type_: "move", destination: "Pepsi", text: "You take a casual stroll"},
            {type_: "move", destination: "Fanta", text: "You take a casual stroll"},
            {type_: "move", destination: "Air Astana", text: "You take a casual stroll"},
            {type_: "move", destination: "Fly Arystan", text: "You take a casual stroll"},
            {type_: "move", destination: "Scat", text: "You take a casual stroll"},
            {type_: "move", destination: "Ford", text: "You take a casual stroll"},
            {type_: "move", destination: "Im Cafe", text: "You take a casual stroll"},
            {type_: "move", destination: "Burger King", text: "You take a casual stroll"},
            {type_: "move", destination: "Valve", text: "You take a casual stroll"},
            {type_: "move", destination: "KFC", text: "You take a casual stroll"},
            {type_: "move", destination: "Radisson", text: "You take a casual stroll"},
            {type_: "move", destination: "Novotel", text: "You take a casual stroll"},
            {type_: "move", destination: "Hilton", text: "You take a casual stroll"},
            {type_: "move", destination: "Toyota", text: "You take a casual stroll"},
            {type_: "move", destination: "Samsung", text: "You take a casual stroll"},
            {type_: "move", destination: "Apple", text: "You take a casual stroll"},
        ]

    def getArr() :
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