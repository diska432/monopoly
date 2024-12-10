class Player:
    def __init__(self, name, color, balance=1500, boardIndex = 0, resign = False):
        self.name = name
        self.color = color
        self.balance = balance
        self.owned_companies = []
        self.boardIndex = boardIndex
        self.resign = resign

    def buy_company(self, company):
        if self.balance >= company.price:
            company.owned = True
            self.owned_companies.append(company)
            self.balance -= company.price
            print(f"{self.name} bought {company.name} for {company.price}")
        else:
            print(f"{self.name} does not have enough balance to buy {company.name}")
    
    def pay_tax(self, tax):
        if self.balance >= tax.amount:
            self.balance -= tax.amount
            print(f"{self.name} paid {tax.amount}")
        else:
            #will implement logic with zalog in the future
            self.resign = True

    def __str__(self):
        return f"{self.name} (Balance: {self.balance}, Color: {self.color})"