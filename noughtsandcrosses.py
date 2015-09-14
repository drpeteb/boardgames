from copy import deepcopy
import numpy as np
from boardgame import Boardgame, Player, BoardgameError, BoardgameNeuralNet

class NoughtsAndCrossesBoard:
    """
    A Noughts and Crosses Board.
    Players moves are indicated in state using +1/-1.
    """
    index = np.array([[0,1,2],
                      [3,4,5],
                      [6,7,8]])
    marks = np.array(['.','X','O'])
    board_string = """
        -------
        |{}|{}|{}|
        -------
        |{}|{}|{}|
        -------
        |{}|{}|{}|
        -------
        """
    
    def __init__(self):
        """
        Create the board
        """
        self.state = np.zeros((3,3),dtype=int)
        self.turn = 1
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
        entries = self.marks[self.state]
        print(self.board_string.format(*entries.flatten()))

    def display_index(self, entries):
        """
        Display the input index at the command line.
        """
        print(self.board_string.format(*entries.flatten()))

    @property
    def permitted_moves(self):
        """
        Returns a list of legal moves
        """
        if not self.over:
            return self.index[self.state == 0]
        else:
            return []

    @property
    def sums(self):
        """
        Calculates sums along all the rows, columns, and diagonals.
        """
        row_sums = np.sum(self.state, axis=1)
        col_sums = np.sum(self.state, axis=0)
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

        empty = self.index[self.state == 0]
        if move not in empty:
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

        empty = self.index[self.state == 0]

        if move not in empty:
            raise BoardgameError("That move is not valid")
        else:
            self.state[move == self.index] = self.turn
            status = self._check_result()
            if status is not None:
                self.over = True
                self.winner = status
                self.turn = 0
            else:
                self.turn = -self.turn


    def _check_result(self):
        """
        Check to see if the game is over and what the result is
        status = +1,-1 indicates a victory for the first/second player
        status = 0 indicates a draw
        status = None indicates the game is still in progress
        """
        sums = self.sums

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
        self._generate_id()
        self.players = []
        self.add_players(players)
        if (len(self.players) != 2):
            raise BoardgameError("Must have 2 players for Noughts and Crosses")
        self.board = NoughtsAndCrossesBoard()
        shuffle = np.random.random_integers(0,1)
        self._order = [None, self.players[shuffle], self.players[1-shuffle]]
        self._announce("Beginning Noughts and Crosses game: {}".format(
                self.game_id))
        self._announce("I flipped a coin to decide who starts."
                       "Player {} will go first and be X.".format(
                self._order[1].name))

    def play_game(self):
        """
        Iterate fetching moves from each player.
        """
        self._notify("begin")
        while True:
            plyr = self._order[self.board.turn]
            self._announce("Player {}, please make a move.".format(plyr.name))
            move = plyr.move(self.board.copy())
            valid = self.board.verify(move)
            if not valid:
                self._announce("Invalid move from player {}.".format(
                                                                    plyr.name))
            else:
                self.board.move(move)
                self._announce("Player {} made a move.".format(plyr.name))
                self.board.display_board()
                if self.board.over:
                    if self.board.winner == 0:
                        self._announce("It's a draw.")
                    else:
                        self._announce("Player {} wins!".format(plyr.name))
                    self.board.display_board()
                    self._notify("finish", self.board.winner)
                    self.remove_players()
                    break


class HumanNoughtsAndCrossesPlayer(Player):
    """
    Human player for noughts and crosses. Command line input.
    """
    index = np.array([['a','b','c'],
                      ['d','e','f'],
                      ['g','h','i']])

    def move(self, board):
        """
        Obtain a move from a human player.
        """
        print("The board looks like this:")
        board.display_board()
        print("You are {}".format(board.marks[board.turn]))
        board.display_index(self.index)
        move = None
        while move is None:
            pick = input("Enter a letter to indicate "
                         "where you would like to go: ")
            if pick in self.index:
                move = board.index[pick == self.index][0]
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

    sum_elements = np.array([[0,1,2],
                             [3,4,5],
                             [6,7,8],
                             [0,3,6],
                             [1,4,7],
                             [2,5,8],
                             [0,4,8],
                             [2,4,6]])

    def move(self, board):
        """
        Obtain a move
        """
        #TODO Replace the inefficient dict with a nice named tuple

        options = dict()
        for st in self.strategies:
            options[st] = []

        legal_moves = board.permitted_moves
        
        # Loop through the opponents possible moves
        for mv in legal_moves:
            bd = board.copy()
            bd.turn = -bd.turn
            bd.move(mv)

            # See if they won (or if it was a draw)
            if bd.over:
                options['block'].append(mv)

            # See if they made a fork
            sums = -bd.turn*bd.sums
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
            sums = -bd.turn*bd.sums
            if np.sum(sums == 2) == 2:
                options['fork'].append(mv)

            # See if we made a threat
            if np.sum(sums == 2) == 1:
                # Ensure that blocking the threat doesn't give away a fork
                threat_group = self.sum_elements[sums == 2]
                possible_fork = np.intersect1d(bd.permitted_moves,
                                               threat_group)
                obd = bd.copy()
                obd.move(possible_fork)
                osums = -obd.turn*obd.sums
                if not ((np.sum(osums == 2) == 2) and
                        (np.sum(osums == -2) == 0)):
                    options['threat'].append(mv)

            # Is it the centre? (and not the first play)
            if ((mv == 4) and (np.sum(np.abs(board.state)) > 0)):
                options['centre'].append(mv)

            # Is it an opposite corner?
            if ((mv in [0,2,6,8]) and 
                (np.sum(bd.state.flatten()[[mv,8-mv]]) == 0)):
                    options['opposite'].append(mv)

            # Is it a corner?
            if (mv in [0,2,6,8]):
                options['corner'].append(mv)

        # Is it an edge?
            if (mv in [1,3,5,7,]):
                options['edge'].append(mv)

        #print(options)

        # Decide which option to take
        move = None
        for st in self.strategies:
            if options[st]:
                move = np.random.choice(options[st])
                break

        if move is None:
            raise BoardgameError("Failed to find an appropriate move.")

        return move



class LearningNoughtsAndCrossesPlayer(Player):
    """
    A learning computer player for noughts and crosses. Uses a neural net to
    estimate the probability of winning from any state (when the opponent is
    about to play).
    """
    def __init__(self, name):
        """
        Create the player.
        """
        self.name = name
        self.neural_net = BoardgameNeuralNet(num_inputs=9)

    def move(self, board):
        """
        Obtain a move.
        """
        legal_moves = board.permitted_moves
        prob = np.zeros((len(legal_moves),3))
        
        # Loop through possible moves
        for mm in range(len(legal_moves)):
            mv = legal_moves[mm]
            bd = board.copy()
            bd.move(mv)

            # Estimate probability of winning
            state = board.turn * bd.state.flatten()[np.newaxis,:]
            prob[mm,:] = self.neural_net.predict(state)
            
            print("Probability of win/draw/lose if I make move{} is {}/{}/{}."\
                                                .format(state, *prob[mm,:]))

        # Select the move which leads to the maximum probability of winning
        #TODO Would the minimum probability of losing be better? Or some
        #     combination of the two? Like win_prob - lose_prob?
        move = legal_moves[np.argmax(prob[:,0])]

        # Store the board for learning later
        board.move(move)
        self._game_history.append(board.state.flatten())

        return move

    def learn(self, winner):
        """
        Update net.
        """
        # Parse the game history to make training data
        states = np.array(self._game_history)
        output = np.zeros(3)
        output[winner] = 1

        # Add symmetric equivalents
        states = self.symmetric_equivalents(states)

        # Update the net
        self.neural_net.update(states, winner)

    def notify(self, event, info):
        """
        Act on an event notification from the game.
        """
        if (event == "begin"):
            self._game_history = []
        elif (event == "finish"):
            self.learn(info)
        else:
            pass

    def symmetric_equivalents(self, states):
        """
        Add symmetrically identical states to an array of game states.
        """
        #TODO Write this function
        pass
