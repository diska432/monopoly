from lobby_manager import LobbyManager
from player import Player
import random
import string

#need to change this logic in the future to a player creating lobbies (will possibly have to change game class or lobby_manager)

lobby_manager = LobbyManager()
while True:
    choice = input("Please select your option:\n create = create new lobby\n join = join existing lobby\n")
    if choice == "create":
        N = 10
        lobby_id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation, k=10))
        game = lobby_manager.create_lobby(lobby_id)
        game.state = "lobby"
        game.play()
    elif choice == "join":
        id = input("Please enter lobby ID")
        #logic with existing lobbies to be implemented