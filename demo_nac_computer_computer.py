# Noughts and Crosses demo - Computer players
import numpy as np
from matplotlib import pyplot as plt

from boardgame import BoardgameError
from noughtsandcrosses import (NoughtsAndCrossesGame,
                               DumbNoughtsAndCrossesPlayer,
                               NaiveNoughtsAndCrossesPlayer,
                               LearningNoughtsAndCrossesPlayer,
                               ExpertNoughtsAndCrossesPlayer)

np.random.seed(seed=0)

players = []
players.append(DumbNoughtsAndCrossesPlayer("Colin"))
players.append(NaiveNoughtsAndCrossesPlayer("Hubert"))
players.append(ExpertNoughtsAndCrossesPlayer("Horatio"))

matches = [[0,1],[0,2],[1,2]]

num_games = 100

for idx in matches:
    results = []
    opponents = [players[idx[0]],players[idx[1]]]
    for gg in range(num_games):
        game = NoughtsAndCrossesGame(opponents, verbosity=0)
        game.play_game()
        results.append(game.winner)

    print("")
    print("Played {} games:".format(num_games))
    print("{} won {} games.".format(opponents[0].name, 
                                            results.count(opponents[0].name)))
    print("{} won {} games.".format(opponents[1].name, 
                                            results.count(opponents[1].name)))
    print("{} games were draws.".format(results.count("Draw")))




