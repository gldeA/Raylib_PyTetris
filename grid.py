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
        self.cell_size: int = cell_size
    
    def set_cell(self, cell: Vector2i, color: Color):
        self.array[cell.y][cell.x] = color
        
    def is_in_bounds(self, x: int, y: int) -> bool:
        return y >= 0 and x >= 0 and y < len(self.array) and x < len(self.array[0])

    def is_in_boundsV(self, position: Vector2i) -> bool:
        return self.is_in_bounds(position.x, position.y)
    
    def draw(self, current_tetrimino: Tetrimino, current_tetrimino_pos: Vector2i):
        """Draws the grid on the screen"""
        screen_width = get_screen_width()
        screen_height = get_screen_height()
        grid_width = len(self.array[0]) * self.cell_size
        grid_height = len(self.array) * self.cell_size
        
        # Draw cells
        x: int = (screen_width // 2) - (grid_width // 2)
        y: int = (screen_height // 2) - (grid_height // 2)
        
        for r in self.array:
            for c in r:
                draw_rectangle(x, y, self.cell_size, self.cell_size, c) # c contains the color
                x += self.cell_size
            x = (screen_width // 2) - (grid_width // 2)
            y += self.cell_size
            
        # Draw Tetrimino
        # TODO: Draw the tetrimino
        
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
        