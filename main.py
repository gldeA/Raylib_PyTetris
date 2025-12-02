from pyray import *

from grid import Grid
from vector2i import Vector2i
from tetrimino import Tetrimino

def main():
    FAST_FALL_DELAY = 60
    STARTING_DELAY = 500
    DELAY_DECAY_RATE = .025
    
    GRID_SIZE = Vector2i(10, 20)
    CELL_SIZE = 32
    
    NEXT_GRID_CELL_SIZE = 20
    NEXT_GRID_POSITION = Vector2i(212, -220)
    
    grid = Grid(GRID_SIZE, CELL_SIZE)
    next_grid = Grid(Vector2i(4, 4), NEXT_GRID_CELL_SIZE, NEXT_GRID_POSITION) # Shows the upcoming tetrimino in the top right, 4x4 to allow for all tetriminoes
        
    current_tetrimino = Tetrimino.new(Vector2i(4, 0))
    next_tetrimino = Tetrimino.new()
    
    score = 0
    
    fall_delay_function = lambda time: int(STARTING_DELAY / ((DELAY_DECAY_RATE * time)**2 + 1)) # https://www.desmos.com/calculator/5xb1rmspe0
    current_fall_delay = fall_delay_function(score) # The number of milliseconds to delay between each fall tick, controls fall speed
    
    has_moved_down: bool = False # Prevents moving down multiple times in a single frame
    lr_press_time = 0.0 # Used for the Left/Right sliding after the initial press
    game_over = False # Pauses logic and displays game over text on a loss
    should_exit_game = False # Flags the game to close
    
    set_config_flags(ConfigFlags.FLAG_WINDOW_RESIZABLE)
    init_window(1280, 720, "PyTetris")
    
    while not window_should_close() and not should_exit_game:
        if not game_over: # Game logic, only occurs if the game is still going
            # Attempt to move the tetrimino down
            if int(get_time() * 1000) % current_fall_delay == 0:
                if not has_moved_down: # Prevent from moving multiple times in a single frame
                    has_hit_bottom = not grid.try_move_tetrimino(current_tetrimino, Vector2i(0, 1))
                    if has_hit_bottom:
                        amount_scored = grid.freeze_tetrimino(current_tetrimino)
                        if amount_scored == -1: # Indicates a loss
                            game_over = True
                            continue
                        if amount_scored == 4:
                            amount_scored += 2 # 2 bonus points for getting a tetris, 4 rows in one move
                        score += amount_scored
                        current_tetrimino = next_tetrimino
                        current_tetrimino.position = Vector2i(4, 0)
                        next_tetrimino = Tetrimino.new()
                    has_moved_down = True
            else:
                has_moved_down = False
                    
            # Move left/right (an initial movement right on button press, then sliding so long as the button remains down
            if is_key_pressed(KeyboardKey.KEY_LEFT) or is_key_pressed(KeyboardKey.KEY_A):
                lr_press_time = get_time()
                grid.try_move_tetrimino(current_tetrimino, Vector2i(-1, 0))
            if is_key_pressed(KeyboardKey.KEY_RIGHT) or is_key_pressed(KeyboardKey.KEY_D):
                lr_press_time = get_time()
                grid.try_move_tetrimino(current_tetrimino, Vector2i(1, 0))
            if (is_key_down(KeyboardKey.KEY_LEFT) or is_key_down(KeyboardKey.KEY_A)) and int((get_time() - lr_press_time) * 1000 + 1) % 125 == 0:
                grid.try_move_tetrimino(current_tetrimino, Vector2i(-1, 0))
            if (is_key_down(KeyboardKey.KEY_RIGHT) or is_key_down(KeyboardKey.KEY_D)) and int((get_time() - lr_press_time) * 1000 + 1) % 125 == 0:
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
                current_fall_delay = min(FAST_FALL_DELAY, fall_delay_function(score)) # Fast fall, but don't slow down if already faster than fast fall
            else:
                current_fall_delay = fall_delay_function(score)
        
        begin_drawing()
        if not game_over:
            clear_background(WHITE)
        else:
            clear_background(LIGHTGRAY)
        
        grid.draw(current_tetrimino) # Main grid
        draw_text(f"Score: {score}", (get_screen_width() // 2) + 170, (get_screen_height() // 2) - 320, 28, BLACK)
        draw_text("Next:", (get_screen_width() // 2) + 170, (get_screen_height() // 2) - 290, 28, BLACK)
        next_grid.draw(next_tetrimino) # Miniature grid in top right
        
        if game_over:
            draw_text("You Lost.", get_screen_width() // 2 - 150, get_screen_height() // 2 - 200, 64, Color(127, 0, 0, 255))
            draw_text("Play Again?", get_screen_width() // 2 - 140, get_screen_height() // 2 - 100, 48, BLACK)
            draw_rectangle(get_screen_width() // 2 - 157, get_screen_height() // 2, 110, 48, GREEN)
            draw_text("YES", get_screen_width() // 2 - 150, get_screen_height() // 2, 48, BLACK)
            draw_rectangle(get_screen_width() // 2 + 70, get_screen_height() // 2, 80, 48, RED)
            draw_text("NO", get_screen_width() // 2 + 80, get_screen_height() // 2, 48, BLACK)
            
            # Button logic
            if Vector2i.from_vector2(get_mouse_position()).within(Vector2i(get_screen_width() // 2 - 157, get_screen_height() // 2), Vector2i(get_screen_width() // 2 - 47, get_screen_height() // 2 + 48)) and is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                grid = Grid(Vector2i(10, 20), 32)
                current_tetrimino = Tetrimino.new(Vector2i(4, 0))
                next_tetrimino = Tetrimino.new()
                score = 0
                game_over = False
            elif Vector2i.from_vector2(get_mouse_position()).within(Vector2i(get_screen_width() // 2 + 70, get_screen_height() // 2), Vector2i(get_screen_width() // 2 + 150, get_screen_height() // 2 + 48)) and is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                should_exit_game = True
        
        end_drawing()
        
    close_window()

main()
