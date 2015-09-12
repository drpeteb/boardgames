from copy import deepcopy
import numpy as np
from boardgame import Boardgame, Player, BoardgameError

class NoughtsAndCrossesBoard:
    """
    A Noughts and Crosses Board.
    Players moves are indicated in state using +1/-1.
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
        -------
        """
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
        -------
        """
        entries = tuple(self.index.flatten())
        print(message.format(*entries))

    @property
    def turn(self):
        """
        Indicate the mark of the player whose turn it is.
        """
        return self.marks[self._next]

    @property
    def permitted_moves(self):
        """
        Returns a list of legal moves
        """
        if not self.over:
            return self.index[self.state==0]
        else:
            return []

    @property
    def _sums(self):
        """
        Calculates sums along all the rows, columns, and diagonals.
        """
        row_sums = np.sum(self.state, axis=0)
        col_sums = np.sum(self.state, axis=1)
        diag_sum1 = np.sum(np.diag(self.state), keepdims=True)
        diag_sum2 = np.sum(np.diag(self.state[:,::-1]), keepdims=True)

        sums = np.concatenate((row_sums, col_sums, diag_sum1, diag_sum2))
        return sums

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
        sums = self._sums

        # See if +1 has won
        if np.any(sums == 3):
            xwin = True
        else:
            xwin = False
        
        # See if -1 has won
        if np.any(sums == -3):
            owin = True
        else:
            owin = False

        if (xwin and owin):
            raise BoardgameError("Both players appear to have won. "
                                 "That shouldn't be possible.")
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
        self.playermarks = {self.board.marks[1]:self.players[shuffle],
                            self.board.marks[-1]:self.players[1-shuffle]}
        self._announce("I flipped a coin and player {} will go first.".format(
                self.playermarks[self.board.marks[1]].name))

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
        Obtain a move from a human player.
        """
        print("The board looks like this:")
        board.display_board()
        print("You are {}".format(board.turn))
        board.display_index()
        move = input("Enter a letter to indicate where you would like to go: ")
        return move


class DumbNoughtsAndCrossesPlayer(Player):
    """
    A really dumb computer player for noughts and crosses. Plays randomly.
    """
   
    def move(self, board):
        """
        Obtain a move.
        """ 
        legal_moves = board.permitted_moves
        move = np.random.choice(legal_moves)
        return move


class ExpertNoughtsAndCrossesPlayer(Player):
    """
    Expert computer player for noughts and crosses. Plays by optimal strategy.
    (see https://en.wikipedia.org/wiki/Tic-tac-toe) 
    """
    strategies = ['win',
                  'block',
                  'fork',
                  'threat',
                  'spoon',
                  'centre',
                  'opposite',
                  'corner',
                  'edge']

    def move(self, board):
        """
        Obtain a move
        """
        options = dict()
        for st in self.strategies:
            options[st] = []

        legal_moves = board.permitted_moves
        
        # Loop through the opponents possible moves
        for mv in legal_moves:
            bd = board.copy()
            bd._next *= -1
            bd.move(mv)

            # See if they won (or if it was a draw)
            if bd.over:
                options['block'].append(mv)

            # See if they made a fork
            sums = -bd._next*bd._sums
            if np.sum(sums == 2) == 2:
                options['spoon'].append(mv)

        # Loop through possible moves to check strategies
        for mv in legal_moves:
            bd = board.copy()
            bd.move(mv)

            # See if we won (or it was a draw)
            if bd.over:
                options['win'].append(mv)

            # See if we made a fork
            sums = -bd._next*bd._sums
            if np.sum(sums == 2) == 2:
                options['fork'].append(mv)

            # See if we made a threat
            if np.sum(sums == 2) == 1:
                # Ensure that blocking the threat doesn't give away a fork
                still_good = True
                for omv in legal_moves:
                    if omv != mv:
                        obd = bd.copy()
                        obd.move(omv)
                        osums = -obd._next*obd._sums
                        if ((np.sum(osums == 2) == 2) and
                            (np.sum(osums == -2) == 0)):
                            still_good = False
                            break
                if still_good:
                    options['threat'].append(mv)

            mvidx = np.where(mv == board.index.flatten())[0][0]

            # Is it the centre? (and not the first play)
            if ((mvidx == 4) and (np.sum(np.abs(board.state)) > 0)):
                options['centre'].append(mv)

            # Is it an opposite corner?
            if ((mvidx in [0,2,6,8]) and 
                (np.sum(bd.state.flatten()[[mvidx,8-mvidx]]) == 0)):
                    options['opposite'].append(mv)

            # Is it a corner?
            if (mvidx in [0,2,6,8]):
                options['corner'].append(mv)

            # Is it an edge?
            if (mvidx in [1,3,5,7,]):
                options['edge'].append(mv)


        # Decide which option to take
        move = None
        for st in self.strategies:
            if options[st]:
                move = np.random.choice(options[st])
                break

        if not move:
            raise BoardgameError("Failed to find an appropriate move.")

        #print(options)
        return move

