from pyray import *

class Vector2i:
    """A vector 2 that stores integers"""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    @staticmethod
    def from_vector2(vec: Vector2):
        """Constructs a Vector2i from a Vector2

        Args:
            vec (Vector2): The Vector2 to generate from
        
        Returns:
            A new Vector2i from the Vector2
        """
        return Vector2i(int(vec.x), int(vec.y))
    
    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Index out of bounds for Vector2i")
    
    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("Index out of bounds for Vector2i")
    
    def __add__(self, other):
        return Vector2i(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2i(self.x - other.x, self.y - other.y)
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Vector2i({self.x}, {self.y})"
    
    def within(self, top_left, bottom_right) -> bool:
        """Whether this Vector2i is between the top_left and bottom_right

        Args:
            top_left (Vector2i): The top left
            bottom_right (Vector2i): The bottom right

        Returns:
            bool: Whether the Vector2i is within these bounds
        """
        return self.x > top_left.x and self.x < bottom_right.x and self.y > top_left.y and self.y < bottom_right.y
    