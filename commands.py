from player import Player

class Command:
    def execute(self):
        pass

class MoveCommand(Command):
    def __init__(self, player, steps):
        self.player = player
        self.steps = steps

    def execute(self):
        print(f"{self.player.name} moves {self.steps} steps forward.")

class BuyCommand(Command):
    def __init__(self, player, company):
        self.player = player
        self.company = company

    def execute(self):
        self.player.buy_company(self.company)