class Vector2i:
    """A vector 2 that stores integers"""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
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
    