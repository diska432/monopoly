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
            "count_brown": 0,
            "count_pink" : 0,
            "count_purple" : 0,
            "count_orange" : 0,
            "count_red" : 0,
            "count_yellow" : 0,
            "count_green" : 0,
            "count_blue" : 0,
            "count_cars" : 0,
            "count_video_game" : 0
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
        if self.balance >= company.price:
            company.owner = self
            self.owned_companies.append(company)
            self.balance -= company.price

            count_string = "count_" + company.color
            if company.color == "brown" or company.color == "blue":
                self.countMap[count_string] += 1
                if self.countMap[count_string] == 2:
                    for c in self.owned_companies:
                        if c.color == company.color:
                            c.rent *= 2
            else:
                self.countMap[count_string] += 1
                if self.countMap[count_string] == 3:
                    for c in self.owned_companies:
                        if c.color == company.color:
                            c.rent *= 2
            if company.type == "car":
                self.countMap["count_cars"] += 1
                for c in self.owned_companies:
                    if c.type == "car":
                        c.rent *= 2
            elif company.type == "videogame":
                self.countMap["count_video_game"] += 1

            print(f"{self.name} bought {company.name} for {company.price}")
        else:
            print(f"{self.name} does not have enough balance to buy {company.name}")

    def possible_company_monopoly_list(self):
        possibleUpgrade = []
        if self.countMap["count_brown"] == 2:
            print("Chanel") 
            possibleUpgrade.append("Chanel")
            print("Hugo Boss") 
            possibleUpgrade.append("Hugo Boss")
        if self.countMap["count_pink"] == 3:
            print("Adidas")
            possibleUpgrade.append("Adidas")
            print("Puma")
            possibleUpgrade.append("Puma")
            print("Lacoste")
            possibleUpgrade.append("Lacoste")
        if self.countMap["count_purple"] == 3:
            print("Skype")
            possibleUpgrade.append("Skype")
            print("Facebook")
            possibleUpgrade.append("Facebook")
            print("Twitter")
            possibleUpgrade.append("Twitter")
        if self.countMap["count_orange"] == 3:
            print("Coca-Cola")
            possibleUpgrade.append("Coca-Cola")
            print("Pepsi")
            possibleUpgrade.append("Pepsi")
            print("Fanta")
            possibleUpgrade.append("Fanta")
        if self.countMap["count_red"] == 3:
            print("Air Astana")
            possibleUpgrade.append("Air Astana")
            print("Fly Arystan")
            possibleUpgrade.append("Fly Arystan")
            print("Scat")
            possibleUpgrade.append("Scat")
        if self.countMap["count_yellow"] == 3:
            print("Im Cafe")
            possibleUpgrade.append("Im Cafe")
            print("Burger King")
            possibleUpgrade.append("Burger King")
            print("KFC")
            possibleUpgrade.append("KFC")
        if self.countMap["count_green"] == 3:
            print("Radisson")
            possibleUpgrade.append("Radisson")
            print("Novotel")
            possibleUpgrade.append("Novotel")
            print("Hilton")
            possibleUpgrade.append("Hilton")
        if self.countMap["count_blue"] == 3:
            print("Samsung")
            possibleUpgrade.append("Samsung")
            print("Apple")
            possibleUpgrade.append("Apple")
        return possibleUpgrade

    def upgrade_company(self, game):
        if len(self.owned_companies) == 0 or not (self.countMap["count_brown"] == 2 or self.countMap["count_pink"] == 3 or 
        self.countMap["count_purple"] == 3 or self.countMap["count_orange"] == 3 or self.countMap["count_red"] == 3 or 
        self.countMap["count_yellow"] == 3 or self.countMap["count_green"] == 3 or self.countMap["count_blue"] == 2):
            print(f"{self.name}, you have no companies to upgrade")
            return 
        print("From the list below choose the company you want to upgrade")  
        possibleUpgrade = self.possible_company_monopoly_list()
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

    def downgrade_company(self):
        input_company = input("Please enter the company name you want to sell: ")
        for company in self.owned_companies:
            if input_company == company.name:
                if company.countStars > 0:
                    company.countStars -= 1
                    if company.color == "brown":
                        if company.name == "Chanel":
                            if company.countStars == 4:
                                company.rent = 160
                            elif company.countStars == 3:
                                company.rent = 90
                            elif company.countStars == 2:
                                company.rent = 30
                            elif company.countStars == 1:
                                company.rent = 10
                            elif company.countStars == 0:
                                company.rent = 4
                        elif company.name == "Hugo Boss":
                            if company.countStars == 4:
                                company.rent = 320
                            elif company.countStars == 3:
                                company.rent = 180
                            elif company.countStars == 2:
                                company.rent = 60
                            elif company.countStars == 1:
                                company.rent = 20
                            elif company.countStars == 0:
                                company.rent = 8
                    elif company.color == "pink":
                        if company.name == "Lacoste":
                            if company.countStars == 4:
                                company.rent = 450
                            elif company.countStars == 3:
                                company.rent = 300
                            elif company.countStars == 2:
                                company.rent = 100
                            elif company.countStars == 1:
                                company.rent = 40
                            elif company.countStars == 0:
                                company.rent = 16
                        else:
                            if company.countStars == 4:
                                company.rent = 400
                            elif company.countStars == 3:
                                company.rent = 270
                            elif company.countStars == 2:
                                company.rent = 90
                            elif company.countStars == 1:
                                company.rent = 30
                            elif company.countStars == 0:
                                company.rent = 12
                    elif company.color == "purple":
                        if company.name == "Twitter":
                            if company.countStars == 4:
                                company.rent = 700
                            elif company.countStars == 3:
                                company.rent = 500
                            elif company.countStars == 2:
                                company.rent = 180
                            elif company.countStars == 1:
                                company.rent = 60
                            elif company.countStars == 0:
                                company.rent = 24
                        else:
                            if company.countStars == 4:
                                company.rent = 625
                            elif company.countStars == 3:
                                company.rent = 450
                            elif company.countStars == 2:
                                company.rent = 150
                            elif company.countStars == 1:
                                company.rent = 50
                            elif company.countStars == 0:
                                company.rent = 20
                    elif company.color == "orange":
                        if company.name == "Fanta":
                            if company.countStars == 4:
                                company.rent = 800
                            elif company.countStars == 3:
                                company.rent = 600
                            elif company.countStars == 2:
                                company.rent = 220
                            elif company.countStars == 1:
                                company.rent = 80
                            elif company.countStars == 0:
                                company.rent = 32
                        else:
                            if company.countStars == 4:
                                company.rent = 750
                            elif company.countStars == 3:
                                company.rent = 550
                            elif company.countStars == 2:
                                company.rent = 200
                            elif company.countStars == 1:
                                company.rent = 60
                            elif company.countStars == 0:
                                company.rent = 28
                    elif company.color == "red":
                        if company.name == "Scat":
                            if company.countStars == 4:
                                company.rent = 925
                            elif company.countStars == 3:
                                company.rent = 750
                            elif company.countStars == 2:
                                company.rent = 300
                            elif company.countStars == 1:
                                company.rent = 100
                            elif company.countStars == 0:
                                company.rent = 40
                        else:
                            if company.countStars == 4:
                                company.rent = 875
                            elif company.countStars == 3:
                                company.rent = 700
                            elif company.countStars == 2:
                                company.rent = 250
                            elif company.countStars == 1:
                                company.rent = 90
                            elif company.countStars == 0:
                                company.rent = 36
                    elif company.color == "yellow":
                        if company.name == "KFC":
                            if company.countStars == 4:
                                company.rent = 1025
                            elif company.countStars == 3:
                                company.rent = 850
                            elif company.countStars == 2:
                                company.rent = 360
                            elif company.countStars == 1:
                                company.rent = 120
                            elif company.countStars == 0:
                                company.rent = 48
                        else:
                            if company.countStars == 4:
                                company.rent = 975
                            elif company.countStars == 3:
                                company.rent = 800
                            elif company.countStars == 2:
                                company.rent = 330
                            elif company.countStars == 1:
                                company.rent = 110
                            elif company.countStars == 0:
                                company.rent = 44
                    elif company.color == "green":
                        if company.name == "Hilton":
                            if company.countStars == 4:
                                company.rent = 1200
                            elif company.countStars == 3:
                                company.rent = 1000
                            elif company.countStars == 2:
                                company.rent = 450
                            elif company.countStars == 1:
                                company.rent = 150
                            elif company.countStars == 0:
                                company.rent = 56
                        else:
                            if company.countStars == 4:
                                company.rent = 1100
                            elif company.countStars == 3:
                                company.rent = 900
                            elif company.countStars == 2:
                                company.rent = 390
                            elif company.countStars == 1:
                                company.rent = 130
                            elif company.countStars == 0:
                                company.rent = 52
                    elif company.color == "blue":
                        if company.name == "Apple":
                            if company.countStars == 4:
                                company.rent = 1700
                            elif company.countStars == 3:
                                company.rent = 1400
                            elif company.countStars == 2:
                                company.rent = 600
                            elif company.countStars == 1:
                                company.rent = 200
                            elif company.countStars == 0:
                                company.rent = 100
                        else:
                            if company.countStars == 4:
                                company.rent = 1300
                            elif company.countStars == 3:
                                company.rent = 1100
                            elif company.countStars == 2:
                                company.rent = 500
                            elif company.countStars == 1:
                                company.rent = 175
                            elif company.countStars == 0:
                                company.rent = 70
                    print(f"{self.name} earns {company.fee} by selling a star from {company.name}")
                    self.balance += company.fee
                    return 1
                else:
                    print("This company does not have any stars. Please choose a valid company that has stars.")
                    return 1
        print("Invalid input")

    def can_mortgage_company(self, color):
        possibleMortgage = [x for x in self.owned_companies if x.color == color]
        for x in possibleMortgage:
            if x.countStars > 0:
                print("Cannot mortgage company. You need to sell all stars first")
                return 1
        return 2
    

    def mortgage_company(self):
        input_company = input("Please enter the company name you want to mortgage: ")
        for company in self.owned_companies:
            if input_company == company.name:
                if company.mortgage_count > 0:
                    print("The company is already mortgaged.")
                    return 1
                if company.color == "brown" or company.color == "blue":
                    count_string = "count_" + company.color 
                    if self.countMap[count_string] == 2:
                        can_mortgage = self.can_mortgage_company(color)
                        if can_mortgage == 1:
                            return 1
                    company.mortgage_count = 15
                    company.rent = 0
                    self.balance += company.price
                else:
                    count_string = "count_" + company.color 
                    if self.countMap[count_string] == 3:
                        can_mortgage = self.can_mortgage_company(color)
                        if can_mortgage == 1:
                            return 1
                    company.mortgage_count = 15
                    company.rent = 0
                    self.balance += company.price / 2    

    def update_mortgage(self):
        for company in self.owned_companies:
            if company.mortgage_count == 0:
                #if mortgage gets to 0 then company goes back to bank
                count_string = "count_" + company.color
                self.countMap[count_string] -= 1
                if company.color == "brown" or company.color == "blue":
                    if self.countMap[count_string] == 1:
                        self.decrease_rent_after_mortgage_ends(company.color)
                else:
                    if self.countMap[count_string] == 2:
                        self.decrease_rent_after_mortgage_ends(company.color)
                        
                company.owner = None
                company.rent = company.initial_rent
                companies_after_removal = list(filter(lambda x: x.name != company.name, self.owned_companies))
                self.owned_companies = companies_after_removal

            if company.mortgage_count >= 0:
                company.mortgage_count -= 1

    def decrease_rent_after_mortgage_ends(self, color):
        companies = [x for x in self.owned_companies if x.color == color]
        for c in companies:
            c.rent /= 2

    def lift_mortgage(self):
        input_name = input("Please enter the name of the company for which you want to lift the mortgage: ")
        for company in self.owned_companies:
            if company.name == input_name:
                if company.mortgage_count == -1:
                    print("Invalid input")
                    return 1
                lift_mortgage_price = ceil((company.price / 2) * 1.1)
                if self.balance >= lift_mortgage_price:
                    self.balance -= lift_mortgage_price
                    company.mortgage_count = -1
                    company.rent = comapny.initial_rent
                    count_string = "count_" + company.color
                    if company.color == "brown" or company.color == "blue":
                        if self.countMap[count_string] == 2:
                            company.rent *= 2
                    else:
                        if self.countMap[count_string] == 3:
                            company.rent *= 2
                    return 1
                else:
                    print("Not enough money to lift mortgage")
                    return 1 
        print("Invalid input")
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