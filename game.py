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
        self.make_move(current_player)     
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
           
            
    def make_move(self, current_player):
        # dice_roll = self.roll_dice() + self.roll_dice()
        dice_roll = 5
        print(f"{current_player.name} rolls {dice_roll}")

        current_player.player_index += dice_roll
        current_cell = self.board[current_player.player_index]
        print(f"{current_player.name} lands on {current_cell.name}!")
        
        if isinstance(current_cell, Company):
            current_player.landed_on_company(current_cell)

        elif isinstance(current_cell, Tax):
            current_player.pay_tax(current_cell)

        elif isinstance(current_cell, Shans):
            arr = current_cell.getArr()
            index = randint(1, len(arr) - 1)
            randomShans = arr[index]
            if randomShans.type_ == "earn":
                print(f"{randomShans.text} {current_player.name} earns {randomShans.amount}")
                current_player.balance += randomShans.amount

            elif randomShans.type_ == "pay":
                current_player.pay_tax(randomShans)

            elif randomShans.type_ == "move":
                destination_cell = self.board[randomShans.destination]
                print(f"{randomShans.text} {current_player.name} lands on {destination_cell.name}")
                if current_player.player_index > randomShans.destination:
                    print(f"{current_player.name} passes START and earns 200")
                    current_player.balance += 200
                current_player.player_index = randomShans.destination
                current_player.landed_on_company(destination_cell)
    
    def play(self):
        handler = InputHandler()
        while True:
            res =  handler.handleInput(self)

    def notify(self, event):
        print(f"Event: {event}")