class NegotiationMediator:
    def __init__(self):
        self.current_negotiation = None

    def start_negotiation(self, player1, player2, offer):
        self.current_negotiation = (player1, player2, offer)
        print(f"{player1.name} has offered {offer} to {player2.name}")

    def respond_to_offer(self, player, response):
        if player == self.current_negotiation[1]:
            print(f"{player.name} has {'accepted' if response else 'rejected'} the offer.")
            self.current_negotiation = None
        else:
            print("Not the correct player to respond.")