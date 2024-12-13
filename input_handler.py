import string
import random
import game
from player import Player

class InputHandler:
    def handleInput(self, game):
        if len(game.players) > 0 and game.state == "active" :
            current_player = game.players[game.current_player_index]
            print(f"{current_player.name}, it is your turn! ")
        op1 = input("Type s for start\n r for resign\n m for move\n a to add player\n l to create new lobby\n d to display current player\n u to upgrade company\n")
        if op1 == "s":
            if game.state == "active":
                print("You are already in a game. Please finish the current game before starting a new one.\n")
                return 1
            elif game.state == "game over":
                print("You need to create a new lobby to start a game.\n")
                return 1
            else:
                game.start_game()
        
        elif op1 == "a":
            if game.state == "active" or game.state == "game over":
                print("You can only add players when setting up a game in the lobby.\n")
                return 1

            player_name = input("Please enter your nickname: ")
            for p in game.players:
                if p.name == player_name:
                    print("This name is already taken. Please enter a different name.\n")
                    return 1

            new_player = Player(player_name, game.colors[len(game.players)], 1500, 0)
            game.add_player(new_player)
        
        elif op1 == "l":
            if game.state == "active":
                print("You are already in a game. Please finish the current game before creating a new lobby.\n")
                return 1
            elif game.state == "lobby":
                print("You are already in a lobby.\n")
            else:
                N = 10
                lobby_id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation, k=N))
                game = lobby_manager.create_lobby(lobby_id)
        elif op1 == "m":
            if game.state == "gameover" or game.state == "lobby":
                print("The game has not started. Please start the game first.\n")
                return 1
            game.play_turn()
        elif op1 == "r":
            if game.state == "gameover" or game.state == "lobby":
                print("The game has not started. Please start the game first.\n")
                return 1
            if len(game.players) == 0:
                print("No players in the game. Current player cannot resign.\n")
                return 1
            current_player = game.players[game.current_player_index]
            current_player.resign(game)
        elif op1 == "d":
            if game.state == "gameover" or game.state == "lobby":
                print("The game has not started. Please start the game first.\n")
                return 1
            current_player = game.players[game.current_player_index]
            print(f"Name: {current_player.name}")
            print(f"Color: {current_player.color}")
            print(f"Balance: {current_player.balance}")
        elif op1 == "u":
            if game.state == "gameover" or game.state == "lobby":
                print("The game has not started. Please start the game first.\n")
                return 1
            current_player = game.players[game.current_player_index]
            current_player.upgrade_company(game)                             
            
        else:
            print("Please enter a valid command\n")
            return
        