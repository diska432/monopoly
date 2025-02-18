import game
from player import Player

class InputHandler:
    def handleInput(self, game):
        current_player = None
        if len(game.players) > 0 and game.state == "active" :
            current_player = game.players[game.current_player_index]
            print(f"{current_player.name}, it is your turn! ")
        if len(game.players) == 1 and game.state == "active" :
            current_player = game.players[0]
            print(f"We have a winner! It is {current_player.name}!")
            back_to_lounge = input("Please enter any key to continue ")
            game.state = "empty"
            return 2
        op1 = input("\nType a command:\n start = start the game\n resign = resign from the game\n move = roll a dice and move\n add = add a  player to the lobby\n exit = exit lobby (only from lobby state) \n dp = display current player\n dc = display companies owned by player\n upgrade = upgrade company\n sell = sell a star of company\n mortgage = mortgage company to the bank\n lift = lift mortgage of a company\n negotiate = enter negotiations with a player\n")
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
        
        elif op1 == "exit":
            if game.state == "active" :
                print("You are already in a game. Please resign or finish the game first\n")
                return 1
            if game.state == "lobby":
                return

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
            current_player.display_player()

        elif op1 == "dc":
            if game.state == "gameover" or game.state == "lobby":
                print("The game has not started. Please start the game first.\n")
                return 1
            if len(game.players) == 0:
                print("No players in the game. Cannot display current player's companies.\n")
                return 1
            current_player.display_companies()

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
            if game.state == "gameover" or game.state == "lobby":
                print("The game has not started. Please start the game first.\n")
                return 1
            if len(game.players) == 0:
                print("No players in the game. Cannot lift mortgage.\n")
                return 1
            current_player.lift_mortgage()

        elif op1 == "negotiate":
            if game.state == "gameover" or game.state == "lobby":
                print("The game has not started. Please start the game first.\n")
                return 1
            current_player.negotiate(game)
        
        else:
            print("Please enter a valid command\n")
            return
        