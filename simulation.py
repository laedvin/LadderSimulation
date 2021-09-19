from player import Player
import numpy as np
import random
import math


# Initialize stuff
num_players = 1000
num_games = 200000  # Number of games to simulate
k = 30  # the K-factor, pertaining to how much MMR adjusts after a game
playstyle_factor = 1  # How different skills affect winrate in a matchup
winrate_factor = 20  # The adjusted skill difference needed for ~91% winrate
# playstyle_factor = 0 means taking the sum of a player's x, y and z.

# Note that the skill distribution isn't tuned.
xs = np.abs(np.random.normal(0, 1, num_players))
ys = np.abs(np.random.normal(0, 1, num_players))
zs = np.abs(np.random.normal(0, 1, num_players))
skills = zip(xs, ys, zs)
players = [Player(x, y, z) for x, y, z in skills]


def calc_winrate(player_a, player_b):
    """
    Takes two player objects as inputs.
    Returns the probability of winning for player A.
    """

    # Extract the individual skills
    a_x, a_y, a_z = player_a.skill_x, player_a.skill_y, player_a.skill_z
    b_x, b_y, b_z = player_b.skill_x, player_b.skill_y, player_b.skill_z

    # Calculate the adjusted skill
    skill_a = (a_x * math.exp((a_x-b_y) * playstyle_factor) +
               a_y * math.exp((a_y-b_z) * playstyle_factor) +
               a_z * math.exp((a_z-b_x) * playstyle_factor))

    skill_b = (b_x * math.exp((b_x-a_y) * playstyle_factor) +
               b_y * math.exp((b_y-a_z) * playstyle_factor) +
               b_z * math.exp((b_z-a_x) * playstyle_factor))

    skill_a = 10**(skill_a/winrate_factor)
    skill_b = 10**(skill_b/winrate_factor)

    return skill_a/(skill_a + skill_b)


# Play some games
for i in range(num_games):
    player_a, player_b = random.sample(players, 2)
    p_a_win = calc_winrate(player_a, player_b)

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

#for player in players:
#    print(player.mmr)

strongest_player = players[np.argmax([player.mmr for player in players])]
print(f"\nStrongest player, w-l: {strongest_player.wins}-{strongest_player.losses}," +
      f"\nMMR: {strongest_player.mmr}\nSkill x: {strongest_player.skill_x}" + 
      f"\nSkill y: {strongest_player.skill_y}\nSkill z: {strongest_player.skill_z}")

weakest_player = players[np.argmax([-player.mmr for player in players])]
print(f"\nWeakest player, w-l: {weakest_player.wins}-{weakest_player.losses}," +
      f"\nMMR: {weakest_player.mmr}\nSkill x: {weakest_player.skill_x}" + 
      f"\nSkill y: {weakest_player.skill_y}\nSkill z: {weakest_player.skill_z}")

sample_player = random.choice(players)
print(f"\nRandom player, w-l: {sample_player.wins}-{sample_player.losses}," +
      f"\nMMR: {sample_player.mmr}\nSkill x: {sample_player.skill_x}" + 
      f"\nSkill y: {sample_player.skill_y}\nSkill z: {sample_player.skill_z}")
