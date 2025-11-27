from enum import Enum
from pyray import *
from vector2i import Vector2i

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
    # TODO: Add inverted L, T, square, and left and right stairsteps

class Tetrimino:
    """Stores the possible different tetriminoes"""
    def __init__(self, variant: TetriminoVariant = TetriminoVariant.NULL, rotation: Rotation = Rotation(0), color: Color = BLACK, position: Vector2i = Vector2i(0, 0)):
        self.variant = variant
        self.rotation = rotation
        self.color = color
        self.position = position
    
    def get_array(self) -> list:
        """Get the array representation of the variant in the current rotation

        Returns:
            list: The array representation of the Tetrimino
        """
        return self.variant.value[self.rotation]
    
    def __str__(self):
        return str(self.variant[self.rotation])
    
