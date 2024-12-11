import game
import string
from random import randint

class Player:
    def __init__(self, name, color, balance=1500, player_index = 0):
        self.name = name
        self.color = color
        self.balance = balance
        self.owned_companies = []   
        self.player_index = player_index
        self.in_jail_count = 0
        self.doubles_rolled = 0

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

    def landed_on_shans(self,current_cell, game):
        arr = current_cell.getArr()
        index = randint(1, len(arr) - 1)
        randomShans = arr[index]
        if randomShans.type_ == "earn":
            print(f"{randomShans.text} {self.name} earns {randomShans.amount}")
            self.balance += randomShans.amount

        elif randomShans.type_ == "pay":
            self.pay_tax(randomShans)

        elif randomShans.type_ == "move":
            destination_cell = game.board[randomShans.destination]
            print(f"{randomShans.text} {self.name} lands on {destination_cell.name}")
            if self.player_index > randomShans.destination:
                print(f"{self.name} passes START and earns 200 tenge")
                self.balance += 200
            self.player_index = randomShans.destination
            self.landed_on_company(destination_cell)

    def landed_on_random_cell(self, current_cell):
        if current_cell.type == "visit":
            return
        elif current_cell.type == "start":
            print(f"{self.name} earns bonus 100 tenge for landing on START")
            self.balance += 100
            player_index = 0
        elif current_cell.type == "prison":
            self.go_to_jail()
        elif current_cell.type == "casino":
            casino = input(f"{self.name} lands on casino! To play you have to pay 100 tenge. Do you wish to play? Type y for yes ")
            if casino == "y":
                self.balance -= 100
                guess = input("Guess the dye roll. Enter digit 1-6 ")
                while (not guess.isnumeric() or int(guess) < 1 or int(guess) > 6):
                    print("That is not a valid input. Please enter a digit 1-6")
                    guess = input("Guess the dye roll. Enter digit 1-6 ")
                dice_roll = randint(1,6)
                print(f"The dye rolls {dice_roll}")
                if guess == dice_roll:
                    print(f"Congratulations! {self.name} wins 600")
                    self.balance += 600
                else:
                    print("Unlucky, next time you will win for sure!")

    def go_to_jail(self):
        self.in_jail_count = 3
        self.player_index = 10

    
    def resign(self, game):
        print(f"{self.name} resigns!\n")
        for company in self.owned_companies:
            company.owner = None 
        new_players = list(filter(lambda x: x.name != self.name, game.players))
        game.players = new_players


    def __str__(self):
        return f"{self.name} (Balance: {self.balance}, Color: {self.color})"