import numpy as np
from matplotlib import pyplot as plt

from boardgame import BoardgameError
from noughtsandcrosses import (NoughtsAndCrossesGame,
                               HumanNoughtsAndCrossesPlayer,
                               DumbNoughtsAndCrossesPlayer,
                               NaiveNoughtsAndCrossesPlayer,
                               LearningNoughtsAndCrossesPlayer,
                               ExpertNoughtsAndCrossesPlayer)

np.random.seed(seed=5)

#player1 = HumanNoughtsAndCrossesPlayer("Pete")
#player2 = HumanNoughtsAndCrossesPlayer("Katy")
#player1 = DumbNoughtsAndCrossesPlayer("Colin")
#player1 = NaiveNoughtsAndCrossesPlayer("Hubert")
#player1 = ExpertNoughtsAndCrossesPlayer("Persephone")
player1 = ExpertNoughtsAndCrossesPlayer("Horatio")
#player = LearningNoughtsAndCrossesPlayer("Franklin")
player2 = LearningNoughtsAndCrossesPlayer("Franklin")
#opponents = [NaiveNoughtsAndCrossesPlayer("Hubert"), \
#             ExpertNoughtsAndCrossesPlayer("Horatio")]
#opponents = [ExpertNoughtsAndCrossesPlayer("Horatio")]

result = []

num_games = 500
num_eval = 50

for gg in range(num_games):
    if (((gg+1)%100) == 0):
        print("Played {} of {} games.".format(gg+1, num_games))
    #game = NoughtsAndCrossesGame([player,opponents[gg%1]], verbosity=0)
    game = NoughtsAndCrossesGame([player1, player2], verbosity=0)
    game.play_game()
    if game.winner == "Franklin":
        result.append(1)
    elif game.winner == "Draw":
        result.append(0)
    else:
        result.append(-1)

#    if game.winner == "Franklin":
#        raise BoardgameError("Horatio should be unbeatable!!")

if result[0] == 1:
    print("First game was won by Franklin.")
elif result[0] == 0:
    print("First game was drawn by Franklin.")
elif result[0] == -1:
    print("First game was lost by Franklin.")
    
print("Franklin won {}\% of the first {} games.".format(
                    100*np.mean(np.array(result[:num_eval]) == 1), num_eval))
print("Franklin drew {}\% of the first {} games.".format(
                    100*np.mean(np.array(result[:num_eval]) == 0), num_eval))

print("Franklin won {}\% of the last {} games.".format(
                    100*np.mean(np.array(result[-num_eval:]) == 1), num_eval))
print("Franklin drew {}\% of the last {} games.".format(
                    100*np.mean(np.array(result[-num_eval:]) == 0), num_eval))

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(result)
plt.show()

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(player2.neural_net.cost_sequence)
plt.show()

