from observer import EventObserver
from player import Player
from board import Board
from random import randint
from cell import Cell, Company, Shans, ShansCard, Tax, RandomCell
from input_handler import InputHandler

class Game(EventObserver):
    def __init__(self, lobby_id):
        self.lobby_id = lobby_id
        self.players = []
        self.colors = ["Red", "Green", "Blue", "Black", "Yellow", "Purple", "Yellow"]
        new_board = Board()
        self.board = Board.getBoard(new_board)
        self.state = "lobby"
        self.current_player_index = 0

    def add_player(self, player):
        if self.state == "lobby":
            self.players.append(player)
            print(f"{player.name} joined the game.")
        else:
            print("You can only add players when setting up a game in the lobby.\n")
            return

    def start_game(self):
        if len(self.players) < 2:
            print("Need at least 2 players to start.")
            return
        self.state = "active"
        print("Game started!")


    def roll_dice(self):
        return randint(1, 6)

    def play_turn(self):
        current_player = self.players[self.current_player_index]
        current_player.update_mortgage()
        self.make_move(current_player)     
        if current_player.doubles_rolled > 0 and current_player.in_jail_count > 0:
            current_player.in_jail_count = 0
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
        if not current_player.doubles_rolled > 0:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
           
            
    def make_move(self, current_player):
        #reset upgradeMap every time a player moves
        for key in current_player.upgradeMap.keys():
            current_player.upgradeMap[key] = False
        # dice_roll1 = self.roll_dice()
        dice_roll1 = 5
        # dice_roll2 = self.roll_dice()
        dice_roll2 = 2
        if current_player.in_jail_count > 0:
            wish = input(f"{current_player.name}, do you want to pay 50 tenge to get out of jail? Type y for yes ")
            if wish == "y":
                current_player.balance -= 50
                current_player.in_jail_count = 0
            else:
                if dice_roll1 == dice_roll2:
                    print(f"{current_player.name} rolls a double and gets out of jail")
                    current_player.in_jail_count = 0
                else:
                    current_player.in_jail_count -= 1
                    print(f"{current_player.name} can't roll a double to get out of jail")
                    if current_player.in_jail_count == 0:
                        fee = input("You need to pay 50 tenge to get out of jail. Type y for yes ")
                        while not fee == "y" :
                            fee = input("You need to pay 50 tenge to get out of jail. Type y for yes ")
                        current_player.balance -= 50
                    else:
                        return
        
        # dice_roll = dice_roll1 + dice_roll2
        dice_roll = 4
        print(f"{current_player.name} rolls {dice_roll}")
        if dice_roll1 == dice_roll2:
            print(f"{current_player.name} rolls a double")
            current_player.doubles_rolled += 1
            if current_player.doubles_rolled == 3:
                print(f"{current_player.name} goes to jail for rolling 3 doubles in a row")
                current_player.go_to_jail()
                current_player.doubles_rolled = 0
                return
        else:
            current_player.doubles_rolled = 0

        destination = current_player.player_index + dice_roll
        if destination >= 40:
            print(f"{current_player.name} passes START and earns 200 tenge")
            destination %= 40

        current_player.player_index = destination
        current_cell = self.board[current_player.player_index]
        print(f"{current_player.name} lands on {current_cell.name}!")
        
        if isinstance(current_cell, Company):
            current_player.landed_on_company(current_cell, dice_roll)

        elif isinstance(current_cell, Tax):
            current_player.pay_tax(current_cell)

        elif isinstance(current_cell, Shans):
            current_player.landed_on_shans(current_cell, self)

        elif isinstance(current_cell, RandomCell):
            current_player.landed_on_random_cell(current_cell)
        
    
    def play(self):
        handler = InputHandler()
        while True:
            res =  handler.handleInput(self)
            if res == 2:
                print("We have a winner!")
                return

    def notify(self, event):
        print(f"Event: {event}")