class Player:
    def __init__(self, name: str):
        self.name = name
        self.level = 1

    def increase_level(self):
        self.level += 1
