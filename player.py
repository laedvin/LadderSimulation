class Player:
    def __init__(self, skill_x=0, skill_y=0, skill_z=0):
        # Define some abstract skills
        self.skill_x = skill_x
        self.skill_y = skill_y
        self.skill_z = skill_z

        # Define ranking statistics
        self.mmr = 1000
        self.wins = 0
        self.losses = 0
