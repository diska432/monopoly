from observer import EventObserver
from player import Player
from board import Board
from random import randint
from cell import Cell, Company, Shans, ShansCard, Tax, RandomCell

class GameState:
    """Abstract class for Game states."""
    def handle(self, game):
        pass

class LobbyState(GameState):
    def handle(self, game):
        print("Game is in the lobby. Waiting for players to join.")

class ActiveGameState(GameState):
    def handle(self, game):
        print("Game is active. Players are taking turns.")

class GameOverState(GameState):
    def handle(self, game):
        print("Game over. Calculating results...")

class Game(EventObserver):
    def __init__(self, lobby_id):
        self.lobby_id = lobby_id
        self.players = []
        newBoard = Board()
        self.board = Board.getBoard(newBoard)
        self.state = LobbyState()
        self.current_player_index = 0

    def add_player(self, player):
        if isinstance(self.state, LobbyState):
            self.players.append(player)
            print(f"{player.name} joined the game.")
        else:
            print("Cannot join. Game has already started.")

    def start_game(self):
        if len(self.players) < 2:
            print("Need at least 2 players to start.")
            return

        self.state = ActiveGameState()
        print("Game started!")


    def roll_dice(self):
        return randint(1, 6)

    def play_turn(self):
        current_player = self.players[self.current_player_index]
        move = input(f"{current_player.name}, it is your turn! \n")
        if move == "p":
            self.make_move(current_player)     
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
           
            
    def make_move(self, current_player):
        # dice_roll = self.roll_dice() + self.roll_dice()
        dice_roll = 7
        print(f"{current_player.name} rolls {dice_roll}")

        current_player.boardIndex += dice_roll
        current_cell = self.board[current_player.boardIndex]
        print(f"{current_player.name} lands on {current_cell.name}!")
        
        if isinstance(current_cell, Company) and not current_cell.owned:
            buy = input(f"Do you want to buy {current_cell.name}? Type y for yes\n")
            if buy == "y":
                current_player.buy_company(current_cell)
            #auction to be implemented in the future

        elif isinstance(current_cell, Tax):
            pay = input(f"You need to pay {current_cell.amount}! Type y for yes\n")
            while not pay == "y":
                pay = input(f"You need to pay {current_cell.amount}! Type y for yes\n")
            current_player.pay_tax(current_cell)

        elif isinstance(current_cell, Shans):
            arr = current_cell.getArr()
            index = randint(1, len(arr))
            randomShans = arr[index]
            if randomShans.type_ == "earn":
                print(f"{randomShans.text} {current_player.name} earns {randomShans.amount}")
                current_player.balance += randomShans.amount

            elif randomShans.type_ == "pay":
                pay = input(f"{randomShans.text} {current_player.name} has to pay {randomShans.amount}. Type y for yes\n")
                while not pay == "y":
                    pay = input(f"{randomShans.text} {current_player.name} has to pay {randomShans.amount}. Type y for yes\n")
                current_player.pay_tax(randomShans)

            elif randomShans.type_ == "move":
                print("we hit move")


    def notify(self, event):
        print(f"Event: {event}")