# Noughts and Crosses demo - Human players

import numpy as np
from matplotlib import pyplot as plt

from boardgame import BoardgameError
from noughtsandcrosses import (NoughtsAndCrossesGame,
                               HumanNoughtsAndCrossesPlayer,
                               DumbNoughtsAndCrossesPlayer,
                               NaiveNoughtsAndCrossesPlayer,
                               LearningNoughtsAndCrossesPlayer,
                               ExpertNoughtsAndCrossesPlayer)

np.random.seed(seed=0)

name1 = input("Enter name of one player: ")
name2 = input("Enter name of the other player: ")

player1 = HumanNoughtsAndCrossesPlayer(name1)
player2 = HumanNoughtsAndCrossesPlayer(name2)
game = NoughtsAndCrossesGame([player1,player2], verbosity=3)
game.play_game()
