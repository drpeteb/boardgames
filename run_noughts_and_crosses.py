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
#player1 = ExpertNoughtsAndCrossesPlayer("Horatio")
#player2 = LearningNoughtsAndCrossesPlayer("Franklin")

player = LearningNoughtsAndCrossesPlayer("Franklin")
#opponents = [ExpertNoughtsAndCrossesPlayer("Horatio")]
opponents = [ExpertNoughtsAndCrossesPlayer("Horatio"),
                NaiveNoughtsAndCrossesPlayer("Hubert")]

result = []

num_games = 1000
num_eval = int(num_games/10)

idx = 1
for gg in range(num_games):
    if (((gg+1)%100) == 0):
        print("Played {} of {} games.".format(gg+1, num_games))
    #if gg > 500:
    #    idx = 1 - idx
    idx = 1 - idx
    game = NoughtsAndCrossesGame([player,opponents[idx]], verbosity=0)
    #game = NoughtsAndCrossesGame([player1, player2], verbosity=0)
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

result = np.array(result)
cost = np.array(player.neural_net.cost_sequence)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(np.where(result==1)[0], cost[result==1],'g')
ax.plot(np.where(result==0)[0], cost[result==0],'b')
ax.plot(np.where(result==-1)[0],cost[result==-1],'r')
plt.show()

