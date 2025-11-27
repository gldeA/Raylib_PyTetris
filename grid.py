from pyray import *

from vector2i import Vector2i
from tetrimino import Tetrimino

class Grid:
    """A class that contains the game grid, should have only one instance"""    
    def __init__(self, cells: Vector2i, cell_size: int):
        """Constructs a new Grid with the given number of cells and the cell_size

        Args:
            cells (Vector2i): (rows, columns), the size of the grid
            cell_size (int): the size of each square cell in pixels, used for drawing
        """
        self.array = [[BLANK for _ in range(cells[1])] for _ in range(cells[0])]
        self.temp_array = [[BLANK for _ in range(cells[1])] for _ in range(cells[0])] # Used for drawing the currently moving tetrimino, cleared every draw
        self.cell_size: int = cell_size
    
    def set_cell(self, cell: Vector2i, color: Color):
        self.array[cell.y][cell.x] = color
        
    def is_in_bounds(self, x: int, y: int) -> bool:
        return y >= 0 and x >= 0 and y < len(self.array) and x < len(self.array[0])

    def is_in_boundsV(self, position: Vector2i) -> bool:
        return self.is_in_bounds(position.x, position.y)
    
    def can_tetrimino_move(self, tetrimino: Tetrimino, direction: Vector2i = Vector2i(0, 0)) -> bool:
        """Whether a tetrimino can move in the given direction and still be valid

        Args:
            tetrimino (Tetrimino): The tetrimino to check
            direction (Vector2i): The direction/distance the tetrimino will move in, defaults to no movement

        Returns:
            bool: Whether the tetrimino can move in the give direction
        """
        can_move = True
        for i in range(len(tetrimino.get_array())):
            for j in range(len(tetrimino.get_array()[0])):
                cell_to_check: Vector2i = Vector2i(tetrimino.position[0] + j, tetrimino.position[1] + i)
                # If this cell is out of bounds or occupied
                if not self.is_in_boundsV(cell_to_check + direction) or (tetrimino.get_array()[i][j] == True and self.getV(cell_to_check + direction) != BLANK):
                    can_move = False
        return can_move
    
    def try_move_tetrimino(self, tetrimino: Tetrimino, direction: Vector2i) -> bool:
        """Attempts to move a tetrimino in the given direction, mutating the tetrimino if the desired movement is valid.

        Args:
            tetrimino (Tetrimino): The tetrimino to attempt to move
            direction (Vector2i): The direction/distance the tetrimino will attempt to move
        
        Returns:
            bool: Whether the move was successfull
        """
        if self.can_tetrimino_move(tetrimino, direction):
            tetrimino.position += direction
            return True
    
    # TODO: Make this work properly
    def back_in_bounds_dir(self, tetrimino: Tetrimino, move_direction: Vector2i = Vector2i(0, 0)) -> Vector2i:
        """Returns the direction that the tetrimino should move to get back in bounds

        Args:
            tetrimino (Tetrimino): The tetrimino to check
            move_direction (Vector2i): The direction the tetrimino will shift in. Defaults to the current position.

        Returns:
            Vector2i: The direction to move the tetrimino to get it back in bounds
        """
        if self.can_tetrimino_move(tetrimino, move_direction):
            return Vector2i(0, 0)
        
        for i in range(len(tetrimino.get_array())):
            for j in range(len(tetrimino.get_array()[0])):
                cell_to_check: Vector2i = Vector2i(tetrimino.position[0] + j, tetrimino.position[1] + i) + move_direction
                # If this cell is out of bounds
                if not self.is_in_boundsV(cell_to_check):
                    if cell_to_check.y <= 0:
                        return Vector2i(0, 1)
                    if cell_to_check.x <= 0:
                        return Vector2i(1, 0)
                    if cell_to_check.y > len(self.array):
                        return Vector2i(0, -1)
                    if cell_to_check.x > len(self.array[0]):
                        return Vector2i(-1, 0)
                # If this cell is occupied
                elif tetrimino.get_array()[i][j] == True and self.getV(cell_to_check) != BLANK:
                    return Vector2i(0, -1) # This assumes it's just falling into one, it will need to be updated later, likely with a way to prevent the tetrimino from rotating

        print("Invaild case for grid.back_in_bounds_direction")
        return Vector2i(0, 0) # Something probably went wrong
    
    def draw(self, current_tetrimino: Tetrimino):
        """Draws the grid on the screen"""
        screen_width = get_screen_width()
        screen_height = get_screen_height()
        grid_width = len(self.array[0]) * self.cell_size
        grid_height = len(self.array) * self.cell_size
        
        # Draw Current Tetrimino
        self.temp_array = [[BLANK for _ in range(len(self.array[0]))] for _ in range(len(self.array))]
        for i in range(len(current_tetrimino.get_array())):
            for j in range(len(current_tetrimino.get_array()[0])):
                if current_tetrimino.get_array()[i][j] == True:
                    self.temp_array[current_tetrimino.position[1] + i][current_tetrimino.position[0] + j] = current_tetrimino.color
        
        # Draw cells
        x: int = (screen_width // 2) - (grid_width // 2)
        y: int = (screen_height // 2) - (grid_height // 2)
        
        for i in range(len(self.array)):
            for j in range(len(self.array[0])):
                draw_rectangle(x, y, self.cell_size, self.cell_size, self.array[i][j])
                draw_rectangle(x, y, self.cell_size, self.cell_size, self.temp_array[i][j]) # Draw current tetrimino
                x += self.cell_size
            x = (screen_width // 2) - (grid_width // 2)
            y += self.cell_size
        
        # Draw vertical lines
        x = (screen_width // 2) - (grid_width // 2)
        top_y = (screen_height // 2) - (grid_height // 2)
        bottom_y = (screen_height // 2) + (grid_height // 2)
        
        for _ in range(len(self.array[0]) + 1):
            draw_line(x, top_y, x, bottom_y, GRAY)
            x += self.cell_size
        
        # Draw horizontal lines
        y = (screen_height // 2) - (grid_height // 2)
        left_x = (screen_width // 2) - (grid_width // 2)
        right_x = (screen_width // 2) + (grid_width // 2)
        
        for _ in range(len(self.array) + 1):
            draw_line(left_x, y, right_x, y, GRAY)
            y += self.cell_size
    
    def get(self, x: int, y: int) -> Color:
        return self.array[y][x]
    
    def getV(self, pos: Vector2i) -> Color:
        return self.get(pos.x, pos.y)
    
    def __str__(self):
        output = ""
        for r in self.array:
            for c in r:
                if c == None:
                    output += ' '
                else:
                    output += str(c)
            output += '\n'
        
        return output
        