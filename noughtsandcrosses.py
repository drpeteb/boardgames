from copy import deepcopy
import numpy as np
from boardgame import Boardgame, Player, BoardgameError

class NoughtsAndCrossesBoard:
    """
    A Noughts and Crosses Board
    """
    index = np.array([['a','b','c'],
                      ['d','e','f'],
                      ['g','h','i']])
    marks = np.array(['.','X','O'])
    
    def __init__(self):
        """
        Create the board
        """
        self.state = np.zeros((3,3),dtype=int)
        self._next = 1
        self.over = False

    def copy(self):
        """
        Copy the board.
        """
        return deepcopy(self)

    def display_board(self):
        """
        Display the board at the command line.
        """
        message = """
        -------
        |{}|{}|{}|
        -------
        |{}|{}|{}|
        -------
        |{}|{}|{}|
        ------- """
        entries = tuple(self.marks[self.state].flatten())
        print(message.format(*entries))

    def display_index(self):
        """
        Display the input index at the command line.
        """
        message = """
        -------
        |{}|{}|{}|
        -------
        |{}|{}|{}|
        -------
        |{}|{}|{}|
        ------- """
        entries = tuple(self.index.flatten())
        print(message.format(*entries))

    @property
    def turn(self):
        """
        Indicate the mark of the player whose turn it is.
        """
        return self.marks[self._next]

    def verify(self, move):
        """
        Verify that a move is valid
        """
        if self.over:
            return False

        empty = (self.state == 0) 
        if move not in self.index[empty]:
            valid = False
        else:
            valid = True
        return valid

    def move(self, move):
        """
        Make a move
        """
        if self.over:
            raise BoardgameError("The game is over")

        empty = (self.state == 0)
        if move not in self.index[empty]:
            raise BoardgameError("That move is not valid")
        else:
            self.state[self.index==move] = self._next
            status = self._check_result()
            if status is not None:
                self.over = True
                self.winner = self.marks[status]
                self._next = 0
            else:
                self._next = -self._next

    def _check_result(self):
        """
        Check to see if the game is over and what the result is
        status = +1,-1 indicates a victory for the first/second player
        status = 0 indicates a draw
        status = None indicates the game is still in progress
        """
        row_sums = np.sum(self.state, axis=0)
        col_sums = np.sum(self.state, axis=1)

        # See if +1 has won
        if (np.any(row_sums == 3) or np.any(col_sums == 3)):
            xwin = True
        else:
            xwin = False
        
        # See if -1 has won
        if (np.any(row_sums == -3) or np.any(col_sums == -3)):
            owin = True
        else:
            owin = False

        if (xwin and owin):
            raise BoardgameError("Both players appear to have won.")
        elif xwin:
            status = 1
        elif owin:
            status = -1
        elif np.all(self.state != 0):
            status = 0
        else:
            status = None
        
        return status

class NoughtsAndCrossesGame(Boardgame):
    """
    Noughts and crosses game.
    Each move, the game passes a board object to the current player, who
    should return it with an appropriate change.
    """
    game_name = "Noughts & Crosses"
    _player_limit = 2

    def __init__(self, players):
        """
        Add players. Create the board. Decide who starts.
        """
        self.players = []
        self.add_players(players)
        self.board = NoughtsAndCrossesBoard()
        shuffle = np.random.random_integers(0,1)
        self.playermarks = {'X':self.players[shuffle],
                            'O':self.players[1-shuffle]}

    def play_game(self):
        """
        Iterate fetching moves from each player.
        """
        while True:
            plyr = self.playermarks[self.board.turn]
            self._announce("Player {}, please make a move.".format(plyr.name))
            move = plyr.move(self.board.copy())
            valid = self.board.verify(move)
            if not valid:
                self._announce("Invalid move from player {}.".format(plyr.name))
            else:
                self.board.move(move)
                self._announce("Player {} made a move.".format(plyr.name))
                if self.board.over:
                    if self.board.winner == '.':
                        self._announce("It's a draw.")
                    else:
                        self._announce("Player {} wins!".format(plyr.name))
                    self.board.display_board()
                    self.remove_players(self.players)
                    break


class HumanNoughtsAndCrossesPlayer(Player):
    """
    Human player for noughts and crosses. Command line input.
    """

    def move(self, board):
        """
        Obtain a move from a human player
        """
        print("The board looks like this:")
        board.display_board()
        print("")
        board.display_index()
        move = input("Enter a letter to indicate where you would like to go: ")
        print(move)
        return move


