from pyray import *

from grid import Grid
from vector2i import Vector2i
from tetrimino import Tetrimino, TetriminoVariant

def main():
    grid = Grid(Vector2i(10, 20), 30)
    
    set_config_flags(ConfigFlags.FLAG_WINDOW_RESIZABLE)
    init_window(1280, 720, "Raytris")
        
    current_tetrimino = Tetrimino.new()
    
    has_moved_down: bool = False
    
    fall_delay = 500 # The number of milliseconds to delay between each fall tick, controls fall speed
    
    while not window_should_close():
        # Move current tetrimino down if possible
        if int(get_time() * 1000) % fall_delay == 0:
            if not has_moved_down: # Prevent from moving multiple times in a single frame
                has_hit_bottom = not grid.try_move_tetrimino(current_tetrimino, Vector2i(0, 1))
                if has_hit_bottom:
                    grid.freeze_tetrimino(current_tetrimino)
                    current_tetrimino = Tetrimino.new()
                has_moved_down = True
        else:
            has_moved_down = False
                
        # Move left/right
        if is_key_pressed(KeyboardKey.KEY_LEFT) or is_key_pressed(KeyboardKey.KEY_A):
            grid.try_move_tetrimino(current_tetrimino, Vector2i(-1, 0))
        if is_key_pressed(KeyboardKey.KEY_RIGHT) or is_key_pressed(KeyboardKey.KEY_D):
            grid.try_move_tetrimino(current_tetrimino, Vector2i(1, 0))
        
        # Rotate
        if is_key_pressed(KeyboardKey.KEY_R):
            current_tetrimino.rotation += 1
            grid.try_move_back_in_bounds(current_tetrimino)
        
        begin_drawing()
        clear_background(WHITE)
        
        grid.draw(current_tetrimino)
        
        end_drawing()
        
    close_window()

main()
