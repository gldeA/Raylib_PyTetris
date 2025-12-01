from pyray import *

from vector2i import Vector2i
from tetrimino import Tetrimino

class Grid:
    """A class that contains the game grid, should have only one instance"""    
    def __init__(self, cells: Vector2i, cell_size: int, center: Vector2i = Vector2i(0, 0)):
        """Constructs a new Grid with the given number of cells and the cell_size

        Args:
            cells (Vector2i): (rows, columns), the size of the grid
            cell_size (int): the size of each square cell in pixels, used for drawing
            center (Vector2i): The center position, offset from the center. Defaults to (0, 0)
        """
        self.array = [[BLANK for _ in range(cells[0])] for _ in range(cells[1])]
        self.temp_array = [[BLANK for _ in range(cells[0])] for _ in range(cells[1])] # Used for drawing the currently moving tetrimino, cleared every draw
        self.cell_size: int = cell_size
        self.center = center
    
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
    
    def back_in_bounds_dir(self, tetrimino: Tetrimino, move_direction: Vector2i = Vector2i(0, 0)) -> Vector2i:
        """Returns the direction that the tetrimino should move to get back in bounds

        Args:
            tetrimino (Tetrimino): The tetrimino to check
            move_direction (Vector2i): The direction the tetrimino will shift in. Defaults to the current position.

        Returns:
            Vector2i: The direction to move the tetrimino to get it back in bounds
        """
        possible_directions = [Vector2i(0, 0), Vector2i(0, -1), Vector2i(1, 0), Vector2i(-1, 0), Vector2i(0, 1),
                                               Vector2i(1, 1), Vector2i(-1, 1), Vector2i(1, -1), Vector2i(-1, -1), 
                                               Vector2i(0, -2), Vector2i(2, 0), Vector2i(-2, 0), Vector2i(0, 2),
                                               Vector2i(0, -3), Vector2i(3, 0), Vector2i(-3, 0), Vector2i(0, 3)]
        for direction in possible_directions:
            if self.can_tetrimino_move(tetrimino, direction):
                return direction
        return None
    
    def try_move_back_in_bounds(self, tetrimino: Tetrimino, move_direction: Vector2i = Vector2i(0, 0)) -> bool:
        """Attempts to move the tetrimino back in bounds after applying the optional move_direction translation.
        Perfectly valid for tetriminoes already in bounds.

        Args:
            tetrimino (Tetrimino): The tetrimino to move
            move_direction (Vector2i, optional): The direction to move the tetrimino. Defaults to no movement.

        Returns:
            bool: Whether the movement was successful
        """
        bounds_dir = self.back_in_bounds_dir(tetrimino, move_direction)
        if bounds_dir is not None: # No possible movement
            tetrimino.position += (move_direction + bounds_dir)
            return True
        else:
            return False
    
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
                    self.temp_array[current_tetrimino.position[1] + i][current_tetrimino.position[0] + j] = current_tetrimino.get_color()
        
        # Draw cells
        x: int = (screen_width // 2) - (grid_width // 2)
        y: int = (screen_height // 2) - (grid_height // 2)
        
        for i in range(len(self.array)):
            for j in range(len(self.array[0])):
                draw_rectangle(x + self.center.x, y + self.center.y, self.cell_size, self.cell_size, self.array[i][j])
                draw_rectangle(x + self.center.x, y + self.center.y, self.cell_size, self.cell_size, self.temp_array[i][j]) # Draw current tetrimino
                x += self.cell_size
            x = (screen_width // 2) - (grid_width // 2)
            y += self.cell_size
        
        # Draw vertical lines
        x = (screen_width // 2) - (grid_width // 2) + self.center.x
        top_y = (screen_height // 2) - (grid_height // 2) + self.center.y
        bottom_y = (screen_height // 2) + (grid_height // 2) + self.center.y
        
        for _ in range(len(self.array[0]) + 1):
            draw_line(x, top_y, x, bottom_y, GRAY)
            x += self.cell_size
        
        # Draw horizontal lines
        y = (screen_height // 2) - (grid_height // 2) + self.center.y
        left_x = (screen_width // 2) - (grid_width // 2) + self.center.x
        right_x = (screen_width // 2) + (grid_width // 2) + self.center.x
        
        for _ in range(len(self.array) + 1):
            draw_line(left_x, y, right_x, y, GRAY)
            y += self.cell_size
    
    def get(self, x: int, y: int) -> Color:
        return self.array[y][x]
    
    def getV(self, pos: Vector2i) -> Color:
        return self.get(pos.x, pos.y)
    
    def freeze_tetrimino(self, tetrimino: Tetrimino) -> int:
        """Adds a tetrimino to the persistent grid and checks for a complete line

        Args:
            tetrimino (Tetrimino): The tetrimino to add
            
        Returns:
            int: how many lines were completed as a result
        """
        for i in range(len(tetrimino.get_array()[0])):
            for j in range(len(tetrimino.get_array())):
                if tetrimino.get_array()[j][i] == True:
                    cell_to_set: Vector2i = Vector2i(tetrimino.position[0] + i, tetrimino.position[1] + j)
                    if self.getV(cell_to_set) != BLANK: # Overwriting another cell, should be a loss or a bug
                        return -1
                    self.set_cell(cell_to_set, tetrimino.get_color())
        
        # Check for line
        complete_lines = 0
        for r in range(len(self.array)):
            is_complete = True
            for c in range(len(self.array[0])):
                if self.get(c, r) == BLANK:
                    is_complete = False
            if is_complete == True:
                complete_lines += 1
                for row_above in range(r, 0, -1): # All the rows down to and including the complete one (except for the top one)
                    self.array[row_above] = list(self.array[row_above - 1]) # Set it equal to the row immediately above, dropping it down by one
        
        return complete_lines
    
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
        