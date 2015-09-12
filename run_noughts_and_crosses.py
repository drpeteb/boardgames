from noughtsandcrosses import (NoughtsAndCrossesGame,
                               HumanNoughtsAndCrossesPlayer,
                               DumbNoughtsAndCrossesPlayer,
                               ExpertNoughtsAndCrossesPlayer)

#player1 = HumanNoughtsAndCrossesPlayer("Pete")
#player2 = HumanNoughtsAndCrossesPlayer("Katy")
player1 = DumbNoughtsAndCrossesPlayer("Colin")
player2 = ExpertNoughtsAndCrossesPlayer("Horatio")

game = NoughtsAndCrossesGame([player1,player2])
game.play_game()
