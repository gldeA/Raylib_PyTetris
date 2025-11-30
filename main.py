from pyray import *

from grid import Grid
from vector2i import Vector2i
from tetrimino import Tetrimino, TetriminoVariant

# TODO: fix bugs (line going to top, crash on block placement)

def main():
    FAST_FALL_DELAY = 50
    STARTING_DELAY = 500
    DELAY_DECAY_RATE = .025
    
    grid = Grid(Vector2i(10, 20), 30)
    
    set_config_flags(ConfigFlags.FLAG_WINDOW_RESIZABLE)
    init_window(1280, 720, "Raytris")
    
    lr_press_time = 0.0 # Used for the Left/Right sliding after the initial press
    
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
                    amount_scored = grid.freeze_tetrimino(current_tetrimino)
                    if amount_scored == 4:
                        amount_scored += 2 # 2 bonus points for getting a tetris, 4 rows in one move
                    score += amount_scored
                    print(score)
                    current_tetrimino = Tetrimino.new()
                has_moved_down = True
        else:
            has_moved_down = False
                
        # Move left/right
        if is_key_pressed(KeyboardKey.KEY_LEFT) or is_key_pressed(KeyboardKey.KEY_A):
            lr_press_time = get_time()
            grid.try_move_tetrimino(current_tetrimino, Vector2i(-1, 0))
        if is_key_pressed(KeyboardKey.KEY_RIGHT) or is_key_pressed(KeyboardKey.KEY_D):
            lr_press_time = get_time()
            grid.try_move_tetrimino(current_tetrimino, Vector2i(1, 0))
        if (is_key_down(KeyboardKey.KEY_LEFT) or is_key_down(KeyboardKey.KEY_A)) and int((get_time() - lr_press_time) * 1000 + 1) % 150 == 0:
            grid.try_move_tetrimino(current_tetrimino, Vector2i(-1, 0))
        if (is_key_down(KeyboardKey.KEY_RIGHT) or is_key_down(KeyboardKey.KEY_D)) and int((get_time() - lr_press_time) * 1000 + 1) % 150 == 0:
            grid.try_move_tetrimino(current_tetrimino, Vector2i(1, 0))
        
        # Rotate
        if is_key_pressed(KeyboardKey.KEY_UP) or is_key_pressed(KeyboardKey.KEY_W):
            current_tetrimino.rotation += 1
            if not grid.try_move_back_in_bounds(current_tetrimino):
                current_tetrimino.rotation -= 1
            
        # Fast fall
        if is_key_pressed(KeyboardKey.KEY_DOWN) or is_key_pressed(KeyboardKey.KEY_S):
            grid.try_move_tetrimino(current_tetrimino, Vector2i(0, 1))
        if is_key_down(KeyboardKey.KEY_DOWN) or is_key_down(KeyboardKey.KEY_S):
            fall_delay = min(FAST_FALL_DELAY, fall_delay_function(get_time())) # Fast fall, but don't slow down if already faster than fast fall
        else:
            fall_delay = fall_delay_function(score)
        
        begin_drawing()
        clear_background(WHITE)
        
        grid.draw(current_tetrimino)
        
        end_drawing()
        
    close_window()

main()
