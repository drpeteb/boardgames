from abc import ABCMeta, abstractmethod
from collections import namedtuple, deque
import string
import random

import numpy as np
import scipy as sp
import scipy.misc as spmisc


class BoardgameError(ValueError):
    """
    Generic Boardgame-specific error
    """

class Boardgame:
    __metaclass__ = ABCMeta
    """
    Abstract boardgame class.
    Derived classes should implement __init__ to setup the game and
    play_game to execute it. 
    """
    game_name = "Abstract Game"
    _player_limit = None

    def __init__(self, verbosity=1):
        self._generate_id()
        self.verbosity = verbosity

    def _generate_id(self):
        """
        Generate an ID for the game, with which to lock the players.
        """
        self.game_id = ''.join(random.choice(string.ascii_uppercase) for \
                                                            _ in range(10))

    def _announce(self, message, v=1):
        """
        Make an announcement
        """
        if (v <= self.verbosity):
            print('\n'+message+'\n')

    def _notify(self, event, info=None):
        """
        A simple mechanism for notifying players of game events.
        """
        for plyr in self.players:
            plyr.notify(event, info)

    def add_players(self, players):
        """
        Add players.
        """
        for plyr in players:
            if ((self._player_limit is not None) and 
                    (len(self.players) >= self._player_limit)):
                raise BoardgameError("Cannot have more than {}"
                                     "players in a game of {}".format(
                    (self._player_limit, self.game_name)))
            if plyr in self.players:
                raise BoardgameError("Player {} is already in the game".format(
                    plyr.name))
            plyr.connect(self.game_id)
            self.players.append(plyr)
    
    def remove_players(self):
        """
        Remove players
        """
        for plyr in self.players:
            plyr.disconnect(self.game_id)
        self.players = []
            
    @abstractmethod
    def play_game(self):
        """
        Main game routine.
        """
        pass

class Player:
    __metaclass__ = ABCMeta
    """
    Abstract player class.
    """
    _current_game_id = None

    def __init__(self, name):
        """
        Create the player.
        """
        self.name = name
    
    def connect(self, game_id):
        """
        Connect player to a game.
        """
        if self._current_game_id is None:
            self._current_game_id = game_id
        else:
            raise BoardgameError("Player {} is already"
                                 " playing a game.".format(self.name))

    def disconnect(self, game_id, feedback=None):
        """
        Disconnect from a game
        """
        if self._current_game_id is game_id:
            self._current_game_id = None

    def notify(self, event, info):
        """
        Act on an event notification from the game.
        """
        pass

    @abstractmethod
    def move(self, state):
        """
        Make a move.
        """
        pass



Layer = namedtuple('Layer', ['weight', 'bias'])

class BoardgameNeuralNet:
    """
    A simple neural net to make learning boardgame players. The number of
    hidden layers and units can be adjusted. The output has three elements
    with a soft-max nonlinearity, and represents the probabilities of
    win/draw/lose. Input and hidden layers use ReLU nonlinearity.
    """
    def __init__(self,
                 random_state=None,
                 num_inputs=10,
                 num_hidden_layers=1,
                 num_hidden_units=[100],
                 step_size=1E-1,
                 regulariser=1E-4,
                 ):
        """
        Initialise the net.
        """
        if (len(num_hidden_units) != num_hidden_layers):
            raise ValueError("Must specify the number of hidden units"
                             "for each hidden layer.")

        self.num_inputs = num_inputs
        self.num_hidden_layers = num_hidden_layers
        self.num_hidden_units = num_hidden_units
        self.step_size = step_size
        self.regulariser = regulariser

        if random_state is not None:
            np.random.seed(seed=random_state)

        self.layers = []

        self.layers.append(self.initialise_layer(num_inputs,
                                                    num_hidden_units[0]))
        for ii in range(num_hidden_layers-1):                                
            self.layers.append(self.initialise_layer(num_hidden_units[ii],
                                                    num_hidden_units[ii+1]))
        self.layers.append(self.initialise_layer(num_hidden_units[-1], 3))        

        self.cost_sequence = []

    def initialise_layer(self, num_in, num_out):
        """
        Randomly initialise weights and biases for a layer
        """
        weight = np.random.randn(num_in, num_out)/np.sqrt(num_in)
        bias = np.zeros(num_out)
        return Layer(weight, bias)
        
    def predict(self, X):
        """
        Predict.
        X is a NxD array where N is the number of data points and D the
        number of input dimensions.
        """
        # Propagate through network
        output = X
        for ii in range(self.num_hidden_layers+1):
            output = np.dot(output, self.layers[ii].weight) \
                                                        + self.layers[ii].bias
            if (ii <= self.num_hidden_layers):
                output = np.maximum(0, output)

        # Output layer
        output -= np.max(output, axis=1, keepdims=True)    # Prevents overflow
        log_prob = output - spmisc.logsumexp(output, axis=1, keepdims=True)

        return log_prob

    def update(self, X, y):
        """
        Update using back propagation
        """
        N,D = X.shape

        # Propagate through network
        layer_output = [X]
        output = X
        for ii in range(self.num_hidden_layers+1):
            output = np.dot(output, self.layers[ii].weight) \
                                                        + self.layers[ii].bias
            layer_output.append(output.copy())
            if (ii <= self.num_hidden_layers):
                output = np.maximum(0, output)

        # Output layer
        output -= np.max(output, axis=1, keepdims=True)    # Prevents overflow
        log_prob = output - spmisc.logsumexp(output, axis=1, keepdims=True)
        truth_log_prob = log_prob[range(N), y]
        cost = -np.sum(truth_log_prob)/N
        for layer in self.layers:
            cost += 0.5 * self.regulariser * np.sum(layer.weight**2)
        self.cost_sequence.append(cost)

        # Back propagation
        d_out = np.exp(log_prob)
        d_out[range(N), y] -= 1
        d_layer_output = d_out
        d_layer_params = deque([])
        for ii in reversed(range(self.num_hidden_layers+1)):
            dW = np.dot(layer_output[ii].T, d_layer_output)/N \
                    + self.regulariser*self.layers[ii].weight
            db = np.sum(d_layer_output, axis=0)/N
            d_layer_params.appendleft(Layer(dW, db))

            if ii > 0:
                d_layer_output = np.dot(d_layer_output,
                                                    self.layers[ii].weight.T)
                d_layer_output[layer_output[ii]<0] = 0

        # Check for infinities
        for dl in d_layer_params:
            if (np.any(np.isinf(dl.weight)) or np.any(np.isinf(dl.bias))):
                print(d_layer_params)
                raise ValueError("Infinities in the parameter derivatives.") 
        
        # Training update
        for ii in range(self.num_hidden_layers+1):
            self.layers[ii].weight[:] -= self.step_size*d_layer_params[ii].weight
            self.layers[ii].bias[:] -= self.step_size*d_layer_params[ii].bias
        
