import string
import random
import game
from player import Player

class InputHandler:
    def handleInput(self, game):
        current_player = None
        if len(game.players) > 0 and game.state == "active" :
            current_player = game.players[game.current_player_index]
            print(f"{current_player.name}, it is your turn! ")
        op1 = input("Type a command:\n start = start the game\n resign = resign from the game\n move = roll a dice and move\n add = add a  player to the lobby\n lobby = create a new lobby\n dp = display current player\n dc = display companies owned by player\n upgrade = upgrade company\n sell = sell a star of company\n mortgage = mortgage company to the bank\n lift = lift mortgage of a company\n")
        if op1 == "start":
            if game.state == "active":
                print("You are already in a game. Please finish the current game before starting a new one.\n")
                return 1
            elif game.state == "game over":
                print("You need to create a new lobby to start a game.\n")
                return 1
            else:
                game.start_game()
        
        elif op1 == "add":
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
        
        elif op1 == "lobby":
            if game.state == "active":
                print("You are already in a game. Please finish the current game before creating a new lobby.\n")
                return 1
            elif game.state == "lobby":
                print("You are already in a lobby.\n")
            else:
                N = 10
                lobby_id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation, k=N))
                game = lobby_manager.create_lobby(lobby_id)
        elif op1 == "move":
            if game.state == "gameover" or game.state == "lobby":
                print("The game has not started. Please start the game first.\n")
                return 1
            game.play_turn()
        elif op1 == "resign":
            if game.state == "gameover" or game.state == "lobby":
                print("The game has not started. Please start the game first.\n")
                return 1
            if len(game.players) == 0:
                print("No players in the game. Current player cannot resign.\n")
                return 1
            current_player.resign(game)
        elif op1 == "dp":
            if game.state == "gameover" or game.state == "lobby":
                print("The game has not started. Please start the game first.\n")
                return 1
            if len(game.players) == 0:
                print("No players in the game. Cannot display current player.\n")
                return 1
            print(f"Name: {current_player.name}")
            print(f"Color: {current_player.color}")
            print(f"Balance: {current_player.balance}")
        elif op1 == "dc":
            if game.state == "gameover" or game.state == "lobby":
                print("The game has not started. Please start the game first.\n")
                return 1
            if len(game.players) == 0:
                print("No players in the game. Cannot display current player's companies.\n")
                return 1
            for c in current_player.owned_companies:
                print(f"{c.name}, mortgage: {c.mortgage_count}, fee: {c.fee}, rent: {c.rent}")
        elif op1 == "upgrade":
            if game.state == "gameover" or game.state == "lobby":
                print("The game has not started. Please start the game first.\n")
                return 1
            if len(game.players) == 0:
                print("No players in the game. Cannot upgrade company.\n")
                return 1
            current_player.upgrade_company(game)
        elif op1 == "sell":
            if game.state == "gameover" or game.state == "lobby":
                print("The game has not started. Please start the game first.\n")
                return 1
            if len(game.players) == 0:
                print("No players in the game. Cannot downgrade company.\n")
                return 1
            current_player.downgrade_company()                          
        elif op1 == "mortgage":
            if game.state == "gameover" or game.state == "lobby":
                print("The game has not started. Please start the game first.\n")
                return 1
            if len(game.players) == 0:
                print("No players in the game. Cannot mortgage company.\n")
                return 1
            current_player.mortgage_company()                          
        elif op1 == "lift":
            if len(game.players) == 0:
                print("No players in the game. Cannot lift mortgage.\n")
                return 1
            if game.state == "gameover" or game.state == "lobby":
                print("The game has not started. Please start the game first.\n")
                return 1
            current_player.lift_mortgage()
        else:
            print("Please enter a valid command\n")
            return
        