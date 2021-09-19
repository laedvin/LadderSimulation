from player import Player
import numpy as np
import random


# Initialize stuff
num_players = 1000
num_games = 100000  # Number of games to simulate
k = 30  # the K-factor, pertaining to how much MMR adjusts after a game

# Note that the skill distribution might not be good.
players = [Player(skill) for skill in np.random.normal(0, 1, num_players)]


# Play some games
for i in range(num_games):
    player_a, player_b = random.sample(players, 2)
    # Calculate probability of player A winning,
    # based on Elo (logistics curve)
    skill_a = 10**player_a.skill
    skill_b = 10**player_b.skill
    p_a_win = skill_a/(skill_a + skill_b)

    if random.random() < p_a_win:
        # Player A won
        s_a = 1
        s_b = 0
        player_a.wins += 1
        player_b.losses += 1
    else:
        # Player B won
        s_a = 0
        s_b = 1
        player_a.losses += 1
        player_b.wins += 1

    # Update MMR
    q_a = 10**(player_a.mmr/400)
    q_b = 10**(player_b.mmr/400)
    e_a = q_a/(q_a + q_b)
    e_b = q_b/(q_a + q_b)

    player_a.mmr += k * (s_a - e_a)
    player_b.mmr += k * (s_b - e_b)

for player in players:
    print(player.mmr)

sample_player = random.choice(players)
print(f"Sample win-loss: {sample_player.wins}-{sample_player.losses}," +
      f"\nMMR: {sample_player.mmr}\nSkill: {sample_player.skill}")
