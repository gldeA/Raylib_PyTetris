from pyray import *

from grid import Grid
from vector2i import Vector2i
from tetrimino import Tetrimino

def main():
    grid = Grid((20, 10), 30)
    
    set_config_flags(ConfigFlags.FLAG_WINDOW_RESIZABLE)
    init_window(1280, 720, "Raytris")
    
    cell_pos = Vector2i(0, 0)
    
    
    while not window_should_close():
        grid.set_cell(cell_pos, BLANK)
        if (is_key_pressed(KeyboardKey.KEY_UP) or is_key_pressed(KeyboardKey.KEY_W)) and grid.is_in_bounds(cell_pos.x, cell_pos.y - 1):
            cell_pos.y -= 1
        if (is_key_pressed(KeyboardKey.KEY_DOWN) or is_key_pressed(KeyboardKey.KEY_S)) and grid.is_in_bounds(cell_pos.x, cell_pos.y + 1):
            cell_pos.y += 1
        if (is_key_pressed(KeyboardKey.KEY_LEFT) or is_key_pressed(KeyboardKey.KEY_A)) and grid.is_in_bounds(cell_pos.x - 1, cell_pos.y):
            cell_pos.x -= 1
        if (is_key_pressed(KeyboardKey.KEY_RIGHT) or is_key_pressed(KeyboardKey.KEY_D)) and grid.is_in_bounds(cell_pos.x + 1, cell_pos.y):
            cell_pos.x += 1
        
        grid.set_cell(cell_pos, RED)
        
        begin_drawing()
        clear_background(WHITE)
        
        grid.draw()
        
        end_drawing()
        
    close_window()

main()
