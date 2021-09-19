class Player:
    def __init__(self, skill=100):
        self.skill = skill  # Actual skill
        self.mmr = 1000  # Just a number
        self.wins = 0
        self.losses = 0
