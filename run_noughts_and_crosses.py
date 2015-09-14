from noughtsandcrosses import (NoughtsAndCrossesGame,
                               HumanNoughtsAndCrossesPlayer,
                               DumbNoughtsAndCrossesPlayer,
                               LearningNoughtsAndCrossesPlayer,
                               ExpertNoughtsAndCrossesPlayer)

player1 = HumanNoughtsAndCrossesPlayer("Pete")
#player2 = HumanNoughtsAndCrossesPlayer("Katy")
#player1 = DumbNoughtsAndCrossesPlayer("Colin")
#player1 = ExpertNoughtsAndCrossesPlayer("Persephone")
#player2 = ExpertNoughtsAndCrossesPlayer("Horatio")
player2 = LearningNoughtsAndCrossesPlayer("Franklin")


game = NoughtsAndCrossesGame([player1,player2])
game.play_game()
