from pyray import *

from grid import Grid
from vector2i import Vector2i
from tetrimino import Tetrimino, TetriminoVariant

# TODO: Make falling smoother (switch to floats), make which tetrimino feel more random (keep a log and weight the outcome), fix bugs (line going to top, crash on block placement)

def main():
    FAST_FALL_DELAY = 50
    STARTING_DELAY = 1000
    DELAY_DECAY_RATE = .01
    
    grid = Grid(Vector2i(10, 20), 30)
    
    set_config_flags(ConfigFlags.FLAG_WINDOW_RESIZABLE)
    init_window(1280, 720, "Raytris")
        
    current_tetrimino = Tetrimino.new()
    
    has_moved_down: bool = False
    
    score = 0
    
    fall_delay = 1000 # The number of milliseconds to delay between each fall tick, controls fall speed
    fall_delay_function = lambda time: int(STARTING_DELAY / ((DELAY_DECAY_RATE * time)**2 + 1)) # https://www.desmos.com/calculator/5xb1rmspe0
    
    while not window_should_close():
        # Move current tetrimino down if possible
        if int(get_time() * 1000) % fall_delay == 0:
            if not has_moved_down: # Prevent from moving multiple times in a single frame
                has_hit_bottom = not grid.try_move_tetrimino(current_tetrimino, Vector2i(0, 1))
                if has_hit_bottom:
                    grid.try_move_back_in_bounds(current_tetrimino) # Just in case
                    score += grid.freeze_tetrimino(current_tetrimino)
                    print(score)
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
        if is_key_pressed(KeyboardKey.KEY_UP) or is_key_pressed(KeyboardKey.KEY_W):
            current_tetrimino.rotation += 1
            grid.try_move_back_in_bounds(current_tetrimino)
            
        # Fast fall
        if is_key_pressed(KeyboardKey.KEY_DOWN) or is_key_pressed(KeyboardKey.KEY_S):
            grid.try_move_tetrimino(current_tetrimino, Vector2i(0, 1))
        if is_key_down(KeyboardKey.KEY_DOWN) or is_key_down(KeyboardKey.KEY_S):
            fall_delay = min(FAST_FALL_DELAY, fall_delay_function(get_time())) # Fast fall, but don't slow down if already faster than fast fall
        else:
            fall_delay = fall_delay_function(get_time())
        
        begin_drawing()
        clear_background(WHITE)
        
        grid.draw(current_tetrimino)
        
        end_drawing()
        
    close_window()

main()
