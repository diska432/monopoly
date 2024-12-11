import game

class Player:
    def __init__(self, name, color, balance=1500, player_index = 0):
        self.name = name
        self.color = color
        self.balance = balance
        self.owned_companies = []   
        self.player_index = player_index

    def buy_company(self, company):
        if self.balance >= company.price:
            company.owner = self
            self.owned_companies.append(company)
            self.balance -= company.price
            print(f"{self.name} bought {company.name} for {company.price}")
        else:
            print(f"{self.name} does not have enough balance to buy {company.name}")

    def landed_on_company(self, company):
        if company.owner is None:
            buy = input(f"Do you want to buy {company.name}? Type y for yes\n")
            if buy == "y":
                self.buy_company(company)
            #auction to be implemented in the future
        else:
            rent = input(f"You need to pay rent in the amount of {company.rent}! Type y for yes\n")
            while not rent == "y":
                rent = input(f"You need to pay rent in the amount of {company.rent}! Type y for yes\n")
            company.owner.balance += company.rent
            self.balance -= company.rent
    
    def pay_tax(self, tax):
        pay = input(f"You need to pay {tax.amount}! Type y for yes\n")
        while not pay == "y":
            pay = input(f"You need to pay {tax.amount}! Type y for yes\n")
        if self.balance >= tax.amount:
            self.balance -= tax.amount
            print(f"{self.name} paid {tax.amount}")
        # else:
            #need to add logic for players to choose if they want to resign or sell company
            # self.resign()
    
    def resign(self, game):
        print(f"{self.name} resigns!\n")
        for company in self.owned_companies:
            company.owner = None 
        new_players = list(filter(lambda x: x.name != self.name, game.players))
        game.players = new_players


    def __str__(self):
        return f"{self.name} (Balance: {self.balance}, Color: {self.color})"