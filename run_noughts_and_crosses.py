from noughtsandcrosses import (NoughtsAndCrossesGame,
                               HumanNoughtsAndCrossesPlayer)

player1 = HumanNoughtsAndCrossesPlayer("Pete")
player2 = HumanNoughtsAndCrossesPlayer("Katy")

game = NoughtsAndCrossesGame([player1,player2])
game.play_game()
