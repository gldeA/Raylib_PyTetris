from enum import Enum
from pyray import *
from vector2i import Vector2i
import random

# TODO: Docstrings for this and everything else

class Rotation:
        def __init__(self, direction: int = 0):
            self.directions = ["up", "right", "down", "left"]
            self.current_direction = direction
        
        def __add__(self, other):
            return Rotation((self.current_direction + 1) % 4)
        
        def __sub__(self, other):
            return Rotation((self.current_direction - 1) % 4)
        
        def get(self) -> str:
            return self.directions[self.current_direction]
        
        def __hash__(self):
            return self.current_direction
        
        def __eq__(self, other):
            return isinstance(other, Rotation) and self.current_direction == other.current_direction

class TetriminoVariant(Enum):
    NULL = {Rotation(0): [[]],
            Rotation(1): [[]],
            Rotation(2): [[]],
            Rotation(3): [[]]}
    LINE = {Rotation(0): [[True],
                          [True],
                          [True],
                          [True]],
            Rotation(1): [[True, True, True, True]],
            Rotation(2): [[True],
                          [True],
                          [True],
                          [True]],
            Rotation(3): [[True, True, True, True]]}
    L = {Rotation(0): [[True, False],
                       [True, False],
                       [True, True]],
            Rotation(1): [[True, True, True],
                          [True, False, False]],
            Rotation(2): [[True, True],
                          [False, True],
                          [False, True]],
            Rotation(3): [[False, False, True],
                          [True, True, True]]}
    INVERTED_L = {Rotation(0): [[False, True],
                                [False, True],
                                [True, True]],
                  Rotation(1): [[True, False, False],
                                [True, True, True]],
                  Rotation(2): [[True, True],
                                [True, False],
                                [True, False]],
                   Rotation(3): [[True, True, True],
                                 [False, False, True]]}
    T = {Rotation(0): [[False, True, False],
                       [True, True, True]],
            Rotation(1): [[True, False],
                          [True, True],
                          [True, False]],
            Rotation(2): [[True, True, True],
                          [False, True, False]],
            Rotation(3): [[False, True],
                          [True, True],
                          [False, True]]}
    SQUARE = {Rotation(0): [[True, True],
                            [True, True]],
              Rotation(1): [[True, True],
                            [True, True]],
              Rotation(2): [[True, True],
                            [True, True]],
              Rotation(3): [[True, True],
                            [True, True]]}
    LR_STAIR = {Rotation(0): [[False, True, True],
                              [True, True, False]],
                Rotation(1): [[True, False],
                              [True, True],
                              [False, True]],
                Rotation(2): [[False, True, True],
                              [True, True, False]],
                Rotation(3): [[True, False],
                              [True, True],
                              [False, True]]}
    RL_STAIR = {Rotation(0): [[True, True, False],
                              [False, True, True]],
                Rotation(1): [[False, True],
                              [True, True],
                              [True, False]],
                Rotation(2): [[True, True, False],
                              [False, True, True]],
                Rotation(3): [[False, True],
                              [True, True],
                              [True, False]]}

class Tetrimino:
    bag = [] # Used to make Tetrimino generation feel fair, as explained in new()
    
    """Stores the possible different tetriminoes"""
    def __init__(self, variant: TetriminoVariant = TetriminoVariant.NULL, rotation: Rotation = Rotation(0), position: Vector2i = Vector2i(0, 0)):
        self.variant = variant
        self.rotation = rotation
        self.position = position
    
    def get_array(self) -> list:
        """Get the array representation of the variant in the current rotation

        Returns:
            list: The array representation of the Tetrimino
        """
        return self.variant.value[self.rotation]
    
    def get_color(self) -> Color:
        """Get the color of this variant of Tetrimino

        Returns:
            Color: The correct color
        """
        match self.variant:
            case TetriminoVariant.NULL:       return BLANK
            case TetriminoVariant.LINE:       return BLUE
            case TetriminoVariant.L:          return ORANGE
            case TetriminoVariant.INVERTED_L: return DARKBLUE
            case TetriminoVariant.T:          return PURPLE
            case TetriminoVariant.SQUARE:     return YELLOW
            case TetriminoVariant.LR_STAIR:   return GREEN
            case TetriminoVariant.RL_STAIR:   return RED
    
    @staticmethod
    def new(start_position: Vector2i = Vector2i(0, 0)):
        """Constructs a new "random" Tetrimino.
        Uses the bag system, where a bag of every Tetrimino variant is generated and then randomly pulled from until empty, then refilled.
        
        Args:
            start_position (Vector2i): The postion to start the tetrimino at. Defaults to (0, 0).
        """
        if len(Tetrimino.bag) == 0:
            Tetrimino.bag = list(TetriminoVariant)[1:]
        random.shuffle(Tetrimino.bag)
        variant = Tetrimino.bag.pop()
        rotation = Rotation(random.randint(0, 3))
        return Tetrimino(variant, rotation, start_position)
    
    def __str__(self):
        return str(self.variant[self.rotation])
    
