import numpy as np
from matplotlib import pyplot as plt

from boardgame import BoardgameError
from noughtsandcrosses import (NoughtsAndCrossesGame,
                               HumanNoughtsAndCrossesPlayer,
                               DumbNoughtsAndCrossesPlayer,
                               LearningNoughtsAndCrossesPlayer,
                               ExpertNoughtsAndCrossesPlayer)

#player1 = HumanNoughtsAndCrossesPlayer("Pete")
#player2 = HumanNoughtsAndCrossesPlayer("Katy")
#player1 = DumbNoughtsAndCrossesPlayer("Colin")
#player1 = ExpertNoughtsAndCrossesPlayer("Persephone")
player1 = ExpertNoughtsAndCrossesPlayer("Horatio")
player2 = LearningNoughtsAndCrossesPlayer("Franklin")

result = []

num_games = 10000
num_eval = 1000

for gg in range(num_games):
    game = NoughtsAndCrossesGame([player1,player2])
    game.play_game()
    if game.winner == "Franklin":
        result.append(1)
    elif game.winner == "Draw":
        result.append(0)
    else:
        result.append(-1)

#    if game.winner == "Franklin":
#        raise BoardgameError("Horatio should be unbeatable!!")

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

