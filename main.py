from lobby_manager import LobbyManager
from player import Player

lobby_manager = LobbyManager()
game = lobby_manager.create_lobby("Lobby1")
game.play()

# Adding players
# player1 = Player("Alice", "Red")
# player2 = Player("Bob", "Blue")

# game.add_player(player1)
# game.add_player(player2)

# # Starting the game
# game.start_game()
# game.play_turn() 