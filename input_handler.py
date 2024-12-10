import string
import random
import game
from player import Player

class InputHandler:
    def handleInput(self, game):
        if len(game.players) > 0 and game.state == "active" :
            current_player = game.players[game.current_player_index]
            print(f"{current_player.name}, it is your turn! \n")
        op1 = input("Type s for start, r for resign, m for move, a to add player, l to create new lobby: ")
        if op1 == "s":
            if game.state == "active":
                print("You are already in a game. Please finish the current game before starting a new one.\n")
                return
            elif game.state == "game over":
                print("You need to create a new lobby to start a game.\n")
                return
            else:
                game.start_game()
        
        elif op1 == "a":
            if game.state == "active" or game.state == "game over":
                print("You can only add players when setting up a game in the lobby.\n")
                return
            else:
                player_name = input("Please enter your name: ")
                new_player = Player(player_name, game.colors[len(game.players)], 1500, 0)
                game.add_player(new_player)
        
        elif op1 == "l":
            if game.state == "active":
                print("You are already in a game. Please finish the current game before creating a new lobby.\n")
                return
            elif game.state == "lobby":
                print("You are already in a lobby.\n")
            else:
                N = 10
                lobby_id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation, k=N))
                game = lobby_manager.create_lobby(lobby_id)
        elif op1 == "m":
            if game.state == "gameover" or game.state == "lobby":
                print("The game has not started. Please start the game first.\n")
                return
            game.play_turn()
        elif op1 == "r":
            if game.state == "gameover" or game.state == "lobby":
                print("The game has not started. Please start the game first.\n")
                return
            if len(game.players) == 0:
                print("No players in the game. Current player cannot resign.\n")
                return
            current_player = self.players[self.current_player_index]
            current_player.resign(game)
        