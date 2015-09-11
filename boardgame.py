from abc import ABCMeta, abstractmethod

import numpy as np


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

    def _announce(self, message):
        """
        Make an announcement
        """
        print('\n'+message+'\n')

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
            plyr.connect(self)
            self.players.append(plyr)
    
    def remove_players(self, players):
        """
        Remove players
        """
        for plyr in players:
            if plyr in self.players:
                plyr.disconnect(self)
                self.players.remove(plyr)

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
    _current_game = None

    def __init__(self, name):
        """
        Create the player.
        """
        self.name = name
    
    def connect(self, game):
        """
        Connect player to a game.
        """
        if self._current_game is None:
            self._current_game = game
        else:
            raise BoardgameError("Player {} is already"
                                 " playing a game.".format(self.name))

    def disconnect(self, game):
        """
        Disconnect from a game
        """
        if self._current_game is game:
            self._current_game = None

    @abstractmethod
    def move(self, state):
        """
        Make a move.
        """
        pass

