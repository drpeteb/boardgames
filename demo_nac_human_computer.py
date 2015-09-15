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

name = input("Enter name of human player: ")

player1 = HumanNoughtsAndCrossesPlayer(name)
player2 = DumbNoughtsAndCrossesPlayer("Colin")
player3 = NaiveNoughtsAndCrossesPlayer("Hubert")
player4 = ExpertNoughtsAndCrossesPlayer("Horatio")

game = NoughtsAndCrossesGame([player1,player2], verbosity=3)
game.play_game()

game = NoughtsAndCrossesGame([player1,player3], verbosity=3)
game.play_game()

game = NoughtsAndCrossesGame([player1,player4], verbosity=3)
game.play_game()

