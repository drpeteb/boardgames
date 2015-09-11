from abc import ABCMeta, abstractmethod

import numpy as np


class Boardgame:
    __metaclass__ = ABCMeta
    """
    Abstract boardgame class.  
    """
    
    def __init__(self, players=[]):
    """
    Create the game.
    """
    self.add_players(players)

    def add_players(self, players):
    """
    Add players.
    """
    for py in players:
        py.connect(self)
        self.players.append(py)
    
    @abstractmethod
    def initialise_game(self):
    """
    Run any necessary setup or dealing operations.
    """

    @abstractmethod
    def conclude_game(self):
    """
    End the game and clear up afterwards.
    """

    @abstractmethod
    def play_game(self):
    """
    Main game routine.
    """

class Player:
    __metaclass__ = ABCMeta
    """
    Abstract player class.
    """

    def __init__(self, name):
    """
    Create the player.
    """
    self.name = name
    self.game = None
    
    def connect(self, game):
    """
    Connect player to a game.
    """
    if self.game is None:
        self.game = game
    else:
        raise ValueError("Player {} is already"
                         " playing a game.".format(self.name))

    @abstractmethod
    def move(self, state):
    """
    Make a move.
    """
