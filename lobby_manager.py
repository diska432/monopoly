from game import Game

class LobbyManager:
    _instance = None
    lobbies = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LobbyManager, cls).__new__(cls)
        return cls._instance

    def create_lobby(self, lobby_id):
        if lobby_id not in self.lobbies:
            game = Game(lobby_id)
            self.lobbies[lobby_id] = game
            return game
        return self.lobbies[lobby_id]

    def remove_lobby(self, lobby_id):
        if lobby_id not in self.lobbies:
            print("Cannot remove not existing lobby\n")
            return
        else:
            del self.lobbies[lobby_id]
            

    def get_lobby(self, lobby_id):
        return self.lobbies.get(lobby_id, None)