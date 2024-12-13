import game
import string
from random import randint
from cell import Cell, Company

class Player:
    def __init__(self, name, color, balance=1500, player_index = 0):
        self.name = name
        self.color = color
        self.balance = balance
        self.owned_companies = []   
        self.player_index = player_index
        self.in_jail_count = 0
        self.doubles_rolled = 0
        self.countMap = {
            "countBrown": 0,
            "countPink" : 0,
            "countPurple" : 0,
            "countOrange" : 0,
            "countRed" : 0,
            "countYellow" : 0,
            "countGreen" : 0,
            "countBlue" : 0,
            "countCars" : 0,
            "countVideoGame" : 0
        }        
        self.upgradeMap = {
            "upgradeBrown": False,
            "upgradePink" : False,
            "upgradePurple" : False,
            "upgradeOrange" : False,
            "upgradeRed" : False,
            "upgradeYellow" : False,
            "upgradeGreen" : False,
            "upgradeBlue" : False
        }        

    def buy_company(self, company):
        #need to implement increment of rent for cars and video games
        if self.balance >= company.price:
            company.owner = self
            self.owned_companies.append(company)
            self.balance -= company.price

            if company.color == "brown":
                self.countMap["countBrown"] += 1
                if self.countMap["countBrown"] == 2:
                    for company in self.owned_companies:
                        if company.color == "brown":
                            company.rent *= 2
            elif company.color == "pink":
                self.countMap["countPink"] += 1
                if self.countMap["countPink"] == 3:
                    for company in self.owned_companies:
                        if company.color == "pink":
                            company.rent *= 2
            elif company.color == "purple":
                self.countMap["countPurple"] += 1
                if self.countMap["countPurple"] == 3:
                    for company in self.owned_companies:
                        if company.color == "purple":
                            company.rent *= 2
            elif company.color == "orange":
                self.countMap["countOrange"] += 1
                if self.countMap["countOrange"] == 3:
                    for company in self.owned_companies:
                        if company.color == "orange":
                            company.rent *= 2
            elif company.color == "red":
                self.countMap["countRed"] += 1
                if self.countMap["countRed"] == 3:
                    for company in self.owned_companies:
                        if company.color == "red":
                            company.rent *= 2
            elif company.color == "yellow":
                self.countMap["countYellow"] += 1
                if self.countMap["countYellow"] == 3:
                    for company in self.owned_companies:
                        if company.color == "yellow":
                            company.rent *= 2
            elif company.color == "green":
                self.countMap["countGreen"] += 1
                if self.countMap["countGreen"] == 3:
                    for company in self.owned_companies:
                        if company.color == "green":
                            company.rent *= 2
            elif company.color == "blue":
                self.countMap["countBlue"] += 1
                if self.countMap["countBlue"] == 3:
                    for company in self.owned_companies:
                        if company.color == "blue":
                            company.rent *= 2
            elif company.type == "car":
                self.countMap["countCars"] += 1
                for company in self.owned_companies:
                    if company.type == "car":
                        company.rent *= 2
            elif company.type == "videogame":
                self.countMap["countVideoGame"] += 1

            print(f"{self.name} bought {company.name} for {company.price}")
        else:
            print(f"{self.name} does not have enough balance to buy {company.name}")

    def upgrade_company(self, game):
        if len(self.owned_companies) == 0 or not (self.countMap["countBrown"] == 2 or self.countMap["countPink"] == 3 or 
        self.countMap["countPurple"] == 3 or self.countMap["countOrange"] == 3 or self.countMap["countRed"] == 3 or 
        self.countMap["countYellow"] == 3 or self.countMap["countGreen"] == 3 or self.countMap["countBlue"] == 2):
            print(f"{self.name}, you have no companies to upgrade")
            return 
        print("From the list below choose the company you want to upgrade")  
        possibleUpgrade = []
        if self.countMap["countBrown"] == 2:
            print("Chanel") 
            possibleUpgrade.append("Chanel")
            print("Hugo Boss") 
            possibleUpgrade.append("Hugo Boss")
        if self.countMap["countPink"] == 3:
            print("Adidas")
            possibleUpgrade.append("Adidas")
            print("Puma")
            possibleUpgrade.append("Puma")
            print("Lacoste")
            possibleUpgrade.append("Lacoste")
        if self.countMap["countPurple"] == 3:
            print("Skype")
            possibleUpgrade.append("Skype")
            print("Facebook")
            possibleUpgrade.append("Facebook")
            print("Twitter")
            possibleUpgrade.append("Twitter")
        if self.countMap["countOrange"] == 3:
            print("Coca-Cola")
            possibleUpgrade.append("Coca-Cola")
            print("Pepsi")
            possibleUpgrade.append("Pepsi")
            print("Fanta")
            possibleUpgrade.append("Fanta")
        if self.countMap["countRed"] == 3:
            print("Air Astana")
            possibleUpgrade.append("Air Astana")
            print("Fly Arystan")
            possibleUpgrade.append("Fly Arystan")
            print("Scat")
            possibleUpgrade.append("Scat")
        if self.countMap["countYellow"] == 3:
            print("Im Cafe")
            possibleUpgrade.append("Im Cafe")
            print("Burger King")
            possibleUpgrade.append("Burger King")
            print("KFC")
            possibleUpgrade.append("KFC")
        if self.countMap["countGreen"] == 3:
            print("Radisson")
            possibleUpgrade.append("Radisson")
            print("Novotel")
            possibleUpgrade.append("Novotel")
            print("Hilton")
            possibleUpgrade.append("Hilton")
        if self.countMap["countBlue"] == 3:
            print("Samsung")
            possibleUpgrade.append("Samsung")
            print("Apple")
            possibleUpgrade.append("Apple")
        input_company = input("Please type the name of the company: ")
        if input_company not in possibleUpgrade:
            print("Not a valid company. Please enter company name from the given list")
            return

        for cell in game.board:
            if isinstance(cell, Company) and cell.name == input_company:
                if cell.color == "brown":
                    if self.upgradeMap["upgradeBrown"]:
                        print("You can only upgrade one company set one move at a time")
                        return 1
                    elif cell.countStars == 5:
                        print("You already have 5 stars on this company")
                        return 1
                    else:
                        self.upgradeMap["upgradeBrown"] = True
                        if self.balance >= cell.fee:
                            self.balance -= cell.fee
                            print(f"{self.name} buys a star for {cell.name} for {cell.fee} tenge")
                            if cell.countStars == 0:
                                cell.countStars += 1
                                if cell.name == "Chanel":
                                    cell.rent = 10
                                elif cell.name == "Hugo Boss":
                                    cell.rent = 20
                            
                            elif cell.countStars == 1:
                                cell.countStars += 1
                                if cell.name == "Chanel":
                                    cell.rent = 30
                                elif cell.name == "Hugo Boss":
                                    cell.rent = 60
                            
                            elif cell.countStars == 2:
                                cell.countStars += 1
                                if cell.name == "Chanel":
                                    cell.rent = 90
                                elif cell.name == "Hugo Boss":
                                    cell.rent = 180
                            
                            elif cell.countStars == 3:
                                cell.countStars += 1
                                if cell.name == "Chanel":
                                    cell.rent = 160
                                elif cell.name == "Hugo Boss":
                                    cell.rent = 320
                            
                            elif cell.countStars == 4:
                                cell.countStars += 1
                                if cell.name == "Chanel":
                                    cell.rent = 250
                                elif cell.name == "Hugo Boss":
                                    cell.rent = 450
                        else:
                            print("You don't have enough money to upgrade this cell")
                            return 1

                if cell.color == "pink":
                    if self.upgradeMap["upgradePink"]:
                        print("You can only upgrade one company set one move at a time")
                        return 1
                    elif cell.countStars == 5:
                        print("You already have 5 stars on this company")
                        return 1
                    else:
                        self.upgradeMap["upgradePink"] = True
                        if self.balance >= cell.fee:
                            self.balance -= cell.fee
                            print(f"{self.name} buys a star for {cell.name} for {cell.fee} tenge")
                            if cell.countStars == 0:
                                cell.countStars += 1
                                if cell.name == "Lacoste":
                                    cell.rent = 40
                                else:
                                    cell.rent = 30
                            
                            elif cell.countStars == 1:
                                cell.countStars += 1
                                if cell.name == "Lacoste":
                                    cell.rent = 100
                                else:
                                    cell.rent = 90
                            
                            elif cell.countStars == 2:
                                cell.countStars += 1
                                if cell.name == "Lacoste":
                                    cell.rent = 300
                                else:
                                    cell.rent = 270
                            
                            elif cell.countStars == 3:
                                cell.countStars += 1
                                if cell.name == "Lacoste":
                                    cell.rent = 450
                                else:
                                    cell.rent = 400
                            
                            elif cell.countStars == 4:
                                cell.countStars += 1
                                if cell.name == "Lacoste":
                                    cell.rent = 550
                                else:
                                    cell.rent = 600
                        else:
                            print("You don't have enough money to upgrade this cell")
                            return 1 
                    
                if cell.color == "purple":
                    if self.upgradeMap["upgradePurple"]:
                        print("You can only upgrade one company set one move at a time")
                        return 1
                    elif cell.countStars == 5:
                        print("You already have 5 stars on this company")
                        return 1
                    else:
                        self.upgradeMap["upgradePurple"] = True
                        if self.balance >= cell.fee:
                            self.balance -= cell.fee
                            print(f"{self.name} buys a star for {cell.name} for {cell.fee} tenge")
                            if cell.countStars == 0:
                                cell.countStars += 1
                                if cell.name == "Twitter":
                                    cell.rent = 60
                                else:
                                    cell.rent = 50
                            
                            elif cell.countStars == 1:
                                cell.countStars += 1
                                if cell.name == "Twitter":
                                    cell.rent = 180
                                else:
                                    cell.rent = 150
                            
                            elif cell.countStars == 2:
                                cell.countStars += 1
                                if cell.name == "Twitter":
                                    cell.rent = 500
                                else:
                                    cell.rent = 450
                            
                            elif cell.countStars == 3:
                                cell.countStars += 1
                                if cell.name == "Twitter":
                                    cell.rent = 700
                                else:
                                    cell.rent = 625
                            
                            elif cell.countStars == 4:
                                cell.countStars += 1
                                if cell.name == "Twitter":
                                    cell.rent = 900
                                else:
                                    cell.rent = 750
                        else:
                            print("You don't have enough money to upgrade this cell")
                            return 1 
                    
                if cell.color == "orange":
                    if self.upgradeMap["upgradeOrange"]:
                        print("You can only upgrade one company set one move at a time")
                        return 1
                    elif cell.countStars == 5:
                        print("You already have 5 stars on this company")
                        return 1
                    else:
                        self.upgradeMap["upgradeOrange"] = True
                        if self.balance >= cell.fee:
                            self.balance -= cell.fee
                            print(f"{self.name} buys a star for {cell.name} for {cell.fee} tenge")
                            if cell.countStars == 0:
                                cell.countStars += 1
                                if cell.name == "Fanta":
                                    cell.rent = 80
                                else:
                                    cell.rent = 60
                            
                            elif cell.countStars == 1:
                                cell.countStars += 1
                                if cell.name == "Fanta":
                                    cell.rent = 220
                                else:
                                    cell.rent = 200
                            
                            elif cell.countStars == 2:
                                cell.countStars += 1
                                if cell.name == "Fanta":
                                    cell.rent = 600
                                else:
                                    cell.rent = 550
                            
                            elif cell.countStars == 3:
                                cell.countStars += 1
                                if cell.name == "Fanta":
                                    cell.rent = 800
                                else:
                                    cell.rent = 750
                            
                            elif cell.countStars == 4:
                                cell.countStars += 1
                                if cell.name == "Fanta":
                                    cell.rent = 1000
                                else:
                                    cell.rent = 950
                        else:
                            print("You don't have enough money to upgrade this cell")
                            return 1 
                    
                if cell.color == "red":
                    if self.upgradeMap["upgradeRed"]:
                        print("You can only upgrade one company set one move at a time")
                        return 1
                    elif cell.countStars == 5:
                        print("You already have 5 stars on this company")
                        return 1
                    else:
                        self.upgradeMap["upgradeRed"] = True
                        if self.balance >= cell.fee:
                            self.balance -= cell.fee
                            print(f"{self.name} buys a star for {cell.name} for {cell.fee} tenge")
                            if cell.countStars == 0:
                                cell.countStars += 1
                                if cell.name == "Scat":
                                    cell.rent = 100
                                else:
                                    cell.rent = 90
                            
                            elif cell.countStars == 1:
                                cell.countStars += 1
                                if cell.name == "Scat":
                                    cell.rent = 300
                                else:
                                    cell.rent = 250
                            
                            elif cell.countStars == 2:
                                cell.countStars += 1
                                if cell.name == "Scat":
                                    cell.rent = 750
                                else:
                                    cell.rent = 700
                            
                            elif cell.countStars == 3:
                                cell.countStars += 1
                                if cell.name == "Scat":
                                    cell.rent = 925
                                else:
                                    cell.rent = 875
                            
                            elif cell.countStars == 4:
                                cell.countStars += 1
                                if cell.name == "Scat":
                                    cell.rent = 1100
                                else:
                                    cell.rent = 1050
                        else:
                            print("You don't have enough money to upgrade this cell")
                            return 1 
                    
                if cell.color == "yellow":
                    if self.upgradeMap["upgradeYellow"]:
                        print("You can only upgrade one company set one move at a time")
                        return 1
                    elif cell.countStars == 5:
                        print("You already have 5 stars on this company")
                        return 1
                    else:
                        self.upgradeMap["upgradeYellow"] = True
                        if self.balance >= cell.fee:
                            self.balance -= cell.fee
                            print(f"{self.name} buys a star for {cell.name} for {cell.fee} tenge")
                            if cell.countStars == 0:
                                cell.countStars += 1
                                if cell.name == "KFC":
                                    cell.rent = 120
                                else:
                                    cell.rent = 110
                            
                            elif cell.countStars == 1:
                                cell.countStars += 1
                                if cell.name == "KFC":
                                    cell.rent = 360
                                else:
                                    cell.rent = 330
                            
                            elif cell.countStars == 2:
                                cell.countStars += 1
                                if cell.name == "KFC":
                                    cell.rent = 850
                                else:
                                    cell.rent = 800
                            
                            elif cell.countStars == 3:
                                cell.countStars += 1
                                if cell.name == "KFC":
                                    cell.rent = 1025
                                else:
                                    cell.rent = 975
                            
                            elif cell.countStars == 4:
                                cell.countStars += 1
                                if cell.name == "KFC":
                                    cell.rent = 1200
                                else:
                                    cell.rent = 1150
                        else:
                            print("You don't have enough money to upgrade this cell")
                            return 1 
                    
                if cell.color == "green":
                    if self.upgradeMap["upgradeGreen"]:
                        print("You can only upgrade one company set one move at a time")
                        return 1
                    elif cell.countStars == 5:
                        print("You already have 5 stars on this company")
                        return 1
                    else:
                        self.upgradeMap["upgradeGreen"] = True
                        if self.balance >= cell.fee:
                            self.balance -= cell.fee
                            print(f"{self.name} buys a star for {cell.name} for {cell.fee} tenge")
                            if cell.countStars == 0:
                                cell.countStars += 1
                                if cell.name == "Hilton":
                                    cell.rent = 150
                                else:
                                    cell.rent = 130
                            
                            elif cell.countStars == 1:
                                cell.countStars += 1
                                if cell.name == "Hilton":
                                    cell.rent = 450
                                else:
                                    cell.rent = 390
                            
                            elif cell.countStars == 2:
                                cell.countStars += 1
                                if cell.name == "Hilton":
                                    cell.rent = 1000
                                else:
                                    cell.rent = 900
                            
                            elif cell.countStars == 3:
                                cell.countStars += 1
                                if cell.name == "Hilton":
                                    cell.rent = 1200
                                else:
                                    cell.rent = 1100
                            
                            elif cell.countStars == 4:
                                cell.countStars += 1
                                if cell.name == "Hilton":
                                    cell.rent = 1400
                                else:
                                    cell.rent = 1275
                        else:
                            print("You don't have enough money to upgrade this cell")
                            return 1 

                if cell.color == "blue":
                    if self.upgradeMap["upgradeBlue"]:
                        print("You can only upgrade one company set one move at a time")
                        return 1
                    elif cell.countStars == 5:
                        print("You already have 5 stars on this company")
                        return 1
                    else:
                        self.upgradeMap["upgradeBlue"] = True
                        if self.balance >= cell.fee:
                            self.balance -= cell.fee
                            print(f"{self.name} buys a star for {cell.name} for {cell.fee} tenge")
                            if cell.countStars == 0:
                                cell.countStars += 1
                                if cell.name == "Samsung":
                                    cell.rent = 175
                                elif cell.name == "Apple":
                                    cell.rent = 200
                            
                            elif cell.countStars == 1:
                                cell.countStars += 1
                                if cell.name == "Samsung":
                                    cell.rent = 500
                                elif cell.name == "Apple":
                                    cell.rent = 600
                            
                            elif cell.countStars == 2:
                                cell.countStars += 1
                                if cell.name == "Samsung":
                                    cell.rent = 1100
                                elif cell.name == "Apple":
                                    cell.rent = 1400
                            
                            elif cell.countStars == 3:
                                cell.countStars += 1
                                if cell.name == "Samsung":
                                    cell.rent = 1300
                                elif cell.name == "Apple":
                                    cell.rent = 1700
                            
                            elif cell.countStars == 4:
                                cell.countStars += 1
                                if cell.name == "Samsung":
                                    cell.rent = 1500
                                elif cell.name == "Apple":
                                    cell.rent = 2000
                        else:
                            print("You don't have enough money to upgrade this cell")
                            return 1


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
        index = randint(0, len(arr) - 1)
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

        elif randomShans.type_ == "jail":
            print(f"{self.name}{randomShans.text}")
            self.go_to_jail()

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