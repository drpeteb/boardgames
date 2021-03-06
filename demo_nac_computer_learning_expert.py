# Noughts and Crosses demo - Learning not to lose to the expert computer player
import numpy as np
from matplotlib import pyplot as plt

from boardgame import BoardgameError
from noughtsandcrosses import (NoughtsAndCrossesGame,
                               ExpertNoughtsAndCrossesPlayer,
                               LearningNoughtsAndCrossesPlayer)

np.random.seed(seed=0)

player1 = ExpertNoughtsAndCrossesPlayer("Horatio")
player2 = LearningNoughtsAndCrossesPlayer("Franklin")


num_training_games = 1000
num_testing_games = 100

# Testing
testing_results = []
player2.learning = False    # Turns off stochastic decisions and updating
test_result = []
for gg in range(num_testing_games):
    game = NoughtsAndCrossesGame([player1,player2], verbosity=0)
    game.play_game()
    testing_results.append(game.winner)
print("Played {} games:".format(num_testing_games))
print("{} won {} games.".format("Franklin", testing_results.count("Franklin")))
print("{} won {} games.".format("Horatio", testing_results.count("Horatio")))
print("{} games were draws.".format(testing_results.count("Draw")))

# Training
player2.learning = True
for gg in range(num_training_games):
    if (((gg+1)%100) == 0):
        print("Played {} of {} games.".format(gg+1, num_training_games))

    game = NoughtsAndCrossesGame([player1, player2], verbosity=0)
    game.play_game()

# Testing
testing_results = []
player2.learning = False    # Turns off stochastic decisions and updating
test_result = []
for gg in range(num_testing_games):
    game = NoughtsAndCrossesGame([player1,player2], verbosity=0)
    game.play_game()
    testing_results.append(game.winner)
print("Played {} games:".format(num_testing_games))
print("{} won {} games.".format("Franklin", testing_results.count("Franklin")))
print("{} won {} games.".format("Horatio", testing_results.count("Horatio")))
print("{} games were draws.".format(testing_results.count("Draw")))
