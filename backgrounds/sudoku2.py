import pygame
import random
import time
 
pygame.init()
pygame.mixer.init()  # Initialize the mixer
# initialise the pygame font
pygame.font.init()
 
# Total window (pixel x pixel)
screen = pygame.display.set_mode((700, 600))

# global var
global mistake_counter
mistake_counter = 0
 
try:
    pygame.mixer.music.load("game.mp3")  # Replace with your actual music file
    pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely
except pygame.error as e:
    print(f"Error loading music: {e}")

# Set title and set up our variables
pygame.display.set_caption("SUDOKU SOLVER USING BACKTRACKING")
x = 0
y = 0
dif = 500 / 9
val = 0

# Difficulty Levels, dictionary
DIFFICULTY_LEVELS = [
    {"name": "Easy", "empty_cells": 20, "bg": "beach.jpg"},
    {"name": "Novice", "empty_cells": 35, "bg": "mount.jpg"},
    {"name": "Mild", "empty_cells": 45, "bg": "forest.jpg"},
    {"name": "Evil", "empty_cells": 55, "bg": "arctic.jpg"},
    {"name": "Impossible", "empty_cells": 65, "bg": "des.jpg"}
]

# Time limits for each difficulty level (in seconds)
TIME_LIMITS = {
    "Easy": 240,  # 4 minutes
    "Novice": 300,  # 5 minutes
    "Mild": 360,  # 6 minutes
    "Evil": 420,  # 7 minutes
    "Impossible": 480  # 8 minutes
}

# Iterate through DIFFICULTY_LEVELS to set the background images
background_images = {}
try:
    for level in DIFFICULTY_LEVELS:
        background_images[level["name"]] = pygame.image.load(level["bg"])
        # Scale image to fit the window
        background_images[level["name"]] = pygame.transform.scale(
            background_images[level["name"]], (700, 600)
        )
except pygame.error:
    print("Warning: Could not load one or more background images. Using fallback color.")

global current_difficulty
current_difficulty = DIFFICULTY_LEVELS[1]  # Start from "Novice", 2nd level

# Default Sudoku Board, 2D List
default_grid =[
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]
 
# font1 = main numbers, font2 = instructions
font1 = pygame.font.SysFont("Arial", 40)
font2 = pygame.font.SysFont("Arial", 20)

def generate_sudoku(difficulty):
    """Generate a Sudoku board with a specified number of empty cells"""
    solved_grid = solve_full_grid(default_grid)
    grid_copy = [row[:] for row in solved_grid]
    
    cells_to_remove = difficulty['empty_cells']
    while cells_to_remove > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        
        if grid_copy[row][col] != 0:
            grid_copy[row][col] = 0
            cells_to_remove -= 1
    
    return grid_copy

def is_valid_move(grid, row, col, num):
    # Check row
    for x in range(9):
        if grid[row][x] == num:
            return False
    
    # Check column
    for x in range(9):
        if grid[x][col] == num:
            return False
    
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False 
    return True

def solve(grid, row, col):
    if row == 8 and col == 9:
        return True
    
    if col == 9:
        row += 1
        col = 0
    
    if grid[row][col] > 0:
        return solve(grid, row, col + 1)
    
    for num in range(1, 10):
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
            
            if solve(grid, row, col + 1):
                return True
        
        grid[row][col] = 0
    
    return False

def solve_full_grid(grid):
    solved_grid = [row[:] for row in grid]
    solve(solved_grid, 0, 0)
    return solved_grid

def get_cord(pos):
    global x
    x = int(pos[0]//dif)
    global y
    y = int(pos[1]//dif)
 
def draw_instructions_background():
    """Draw a semi-transparent background behind instructions for better visibility"""
    instruction_surface = pygame.Surface((600, 450))
    instruction_surface.fill((255, 255, 255))  # White background
    instruction_surface.set_alpha(200)  # Semi-transparent (0-255)
    screen.blit(instruction_surface, (370, 500))

     # Call the draw_timer function to display the timer
    draw_timer()

def draw_difficulty_menu():
    """Draw difficulty selection menu with semi-transparent background"""
    menu_x, menu_y = 510, 100
    
    # Draw menu background
    menu_surface = pygame.Surface((150, 250))
    menu_surface.fill((255, 255, 255))
    menu_surface.set_alpha(200)
    screen.blit(menu_surface, (menu_x, menu_y))
    
    # pastel purple
    SELECTED_COLOR = (203, 195, 227)    # Pastel purple
    UNSELECTED_COLOR = (229, 225, 237)  # Light pastel purple
    TEXT_COLOR = (75, 61, 96)           # Dark purple

    for i, diff in enumerate(DIFFICULTY_LEVELS):
        # text = font2.render(diff['name'], 1, (0, 0, 0))
        text = font2.render(diff['name'], 1, TEXT_COLOR)
        rect = pygame.Rect(menu_x, menu_y + i*50, 150, 40)
        
        if diff == current_difficulty:
           # pygame.draw.rect(screen, (100, 100, 100), rect)
            pygame.draw.rect(screen, SELECTED_COLOR, rect)
        else:
            # pygame.draw.rect(screen, (50, 50, 50), rect)
            pygame.draw.rect(screen, UNSELECTED_COLOR, rect)
        
        screen.blit(text, (menu_x + 10, menu_y + i*50 + 10))


def draw_box():
    # Draw the highlighted row, column, and 3x3 grid for the selected cell
    if selected_cell is not None:
        row, col = selected_cell
        
        # Highlight the row
        for i in range(9):
            pygame.draw.rect(screen, (255, 165, 0), (col * dif, i * dif, dif, dif), 2)
        
        # Highlight the column
        for i in range(9):
            pygame.draw.rect(screen, (255, 165, 0), (i * dif, row * dif, dif, dif), 2)
        
        # Highlight the 3x3 grid
        start_row = row // 3 * 3
        start_col = col // 3 * 3
        for i in range(3):
            for j in range(3):
                pygame.draw.rect(screen, (255, 165, 0), ((start_col + j) * dif, (start_row + i) * dif, dif, dif), 2)
    
    # Draw the selected cell's box
    for i in range(2):
        pygame.draw.line(screen, (255, 0, 0), (x * dif - 3, (y + i) * dif), (x * dif + dif + 3, (y + i) * dif), 7)
        pygame.draw.line(screen, (255, 0, 0), ((x + i) * dif, y * dif), ((x + i) * dif, y * dif + dif), 7)
    #for i in range(2):
       # pygame.draw.line(screen, (255, 0, 0), (x * dif-3, (y + i)*dif), (x * dif + dif + 3, (y + i)*dif), 7)
       # pygame.draw.line(screen, (255, 0, 0), ( (x + i)* dif, y * dif ), ((x + i) * dif, y * dif + dif), 7)''


def draw():
    # Draw background first
    try:
        screen.blit(background_images[current_difficulty["name"]], (0, 0))
    except (KeyError, TypeError):
        # Fallback if image loading failed
        screen.fill((255, 255, 255))
    
    # Draw semi-transparent game board background
    board_surface = pygame.Surface((500, 500))
    board_surface.fill((255, 255, 255))
    board_surface.set_alpha(200)  # Slightly transparent
    screen.blit(board_surface, (0, 0))
    
    # CHANGE
    mistake_text = font2.render(f"Mistakes: {mistake_counter}/5", True, (255, 0, 0))
    screen.blit(mistake_text, (510, 300))

    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                # Make filled cells more visible
                pygame.draw.rect(screen, (0, 153, 153), (j * dif, i * dif, dif + 1, dif + 1))
                text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(text1, (j * dif + 15, i * dif + 15))
    
    # Draw grid lines
    for i in range(10):
        thick = 7 if i % 3 == 0 else 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (500, i * dif), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 500), thick)

def instruction():
    draw_instructions_background()  # Add background behind instructions
    
    text1 = font2.render("PRESS R TO RESET              ", 1, (0, 0, 0))
    text2 = font2.render("PRESS D TO SOLVE              ", 1, (0, 0, 0))
    text3 = font2.render("PRESS ENTER AFTER INPUT", 1, (0, 0, 0))
    # text4 = font2.render("INPUT", 1, (0, 0, 0))

    text3_width = text3.get_width()
    text1_width = text1.get_width()
    text2_width = text2.get_width()
    # screen_width = 700
    right_margin = 50

    # screen.blit(text3, (screen_width - text4_width - right_margin, 570))
    screen.blit(text3, (700 - text3_width - right_margin, 570))
    screen.blit(text2, (700 - text2_width - right_margin, 550))
    screen.blit(text1, (700 - text1_width - right_margin, 530))

def raise_error1():
    text1 = font2.render("ERROR!", 1, (255, 0, 0))
    screen.blit(text1, (510, 500))
    pygame.display.update()
    pygame.time.delay(1000)

def raise_error2():
     # First display entered wrong value
    wrong_font = pygame.font.SysFont("Arial", 40, bold=True)
    wrong_num = wrong_font.render(str(val), True, (255, 0, 0))  # Red color
    
    num_width = wrong_num.get_width()
    num_x = (x * dif) + (dif - num_width) // 2
    num_y = y * dif + 15
    
    screen.blit(wrong_num, (num_x, num_y))
    pygame.display.update()
    pygame.time.delay(1000)
    
    # bold wrong message
    bold_font = pygame.font.SysFont("Arial", 30, bold=True)
    text1 = bold_font.render("WRONG!", 1, (255, 0, 0))

      # Get text dimensions
    text_width = text1.get_width()
    text_height = text1.get_height()
    
    # Calculate center position
    text_x = (500 - text_width) // 2  # Center horizontally within the game board
    text_y = 250  # Vertically centered on the board
    
    # Draw white background highlight
    highlight_surface = pygame.Surface((text_width + 20, text_height + 20), pygame.SRCALPHA)
    highlight_surface.fill((255, 255, 255, 200))  # White with some transparency
    screen.blit(highlight_surface, (text_x - 10, text_y - 10))
    
    # Draw text
    screen.blit(text1, (text_x, text_y))
    
    pygame.display.update()
    pygame.time.delay(1000)


def draw_timer():
    """Draw the timer on the bottom-left of the screen"""
    if current_difficulty:
        time_limit = TIME_LIMITS[current_difficulty["name"]]
        elapsed_time = time.time() - start_time
        remaining_time = max(0, time_limit - int(elapsed_time))

        minutes = remaining_time // 60
        seconds = remaining_time % 60
        timer_text = f"{minutes:02d}:{seconds:02d}"

        # Use a larger, bubbly font for the timer
        timer_font = pygame.font.Font(None, 48)
        timer_surface = timer_font.render(timer_text, True, (102, 0, 102))

        # Center the timer text horizontally
        text_rect = timer_surface.get_rect()
        text_rect.midleft = (10, 550)

        # Draw a semi-transparent background behind the timer
        bg_surface = pygame.Surface((text_rect.width + 20, text_rect.height + 10), pygame.SRCALPHA)
        bg_surface.fill((255, 255, 255, 200))
        screen.blit(bg_surface, (text_rect.left - 10, text_rect.top - 5))

        # Draw the timer text
        screen.blit(timer_surface, text_rect)

        # Bubbly font for mistake counter
        try:
            mistake_font = pygame.font.SysFont("Comic Sans MS", 28, bold=True)
        except:
            mistake_font = pygame.font.SysFont("Arial", 28, bold=True)

        # Add mistake counter next to timer
        mistake_text = mistake_font.render(f"Mistakes: {mistake_counter}/5", True, (75, 61, 96))  # Dark purple
        mistake_rect = mistake_text.get_rect()
        mistake_rect.midleft = (text_rect.right + 50, 550)
        
        # Add transparent background
        bg_surface = pygame.Surface((mistake_rect.width + 20, mistake_rect.height + 10), pygame.SRCALPHA)
        bg_surface.fill((255, 255, 255, 200))  # White with transparency
        screen.blit(bg_surface, (mistake_rect.left - 10, mistake_rect.top - 5))
        
        screen.blit(mistake_text, mistake_rect)
    
def show_game_over():

    # Create a bubbly font
    try:
        game_over_font = pygame.font.SysFont("Comic Sans MS", 72, bold=True)
    except:
        game_over_font = pygame.font.SysFont("Arial", 72, bold=True)
    
    text = game_over_font.render("GAME OVER!!!", True, (255, 0, 0))
    
    # Get text dimensions for centering
    text_width = text.get_width()
    text_height = text.get_height()
    
    # Center position
    text_x = (500 - text_width) // 2
    text_y = (500 - text_height) // 2
    
    # Draw semi-transparent black background
    overlay = pygame.Surface((500, 500))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    screen.blit(overlay, (0, 0))
    
    # Draw text
    screen.blit(text, (text_x, text_y))
    pygame.display.update()

def reset_game():
    global mistake_counter, grid, start_time, flag1, flag2, rs, error, selected_cell
    mistake_counter = 0
    grid = generate_sudoku(current_difficulty)
    start_time = time.time()
    flag1 = 0
    flag2 = 0
    rs = 0
    error = 0
    selected_cell = None

# Main game loop
grid = generate_sudoku(current_difficulty)
run = True
flag1 = 0
flag2 = 0
rs = 0
error = 0
mistake_counter = 0
selected_cell = None
start_time = time.time()  # Record the start time

while run:
    # Add this at the start of the loop
    current_time = time.time()
    if current_time - start_time > TIME_LIMITS[current_difficulty["name"]]:
        show_game_over("time")
        pygame.time.delay(2000)  # Show for 2 seconds
        grid = generate_sudoku(current_difficulty)  # Reset game
        start_time = time.time()  # Reset timer
        mistake_counter = 0
        flag1 = 0
        flag2 = 0
        rs = 0
        error = 0
        selected_cell = None
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Check difficulty menu clicks
            if mouse_x > 510 and mouse_x < 660:
                difficulty_index = (mouse_y - 100) // 50
                if 0 <= difficulty_index < len(DIFFICULTY_LEVELS):
                    current_difficulty = DIFFICULTY_LEVELS[difficulty_index]
                    grid = generate_sudoku(current_difficulty)
                    mistake_counter = 0
                    flag1 = 0
                    flag2 = 0
                    rs = 0
                    error = 0
            # Check grid clicks
            elif mouse_x < 500 and mouse_y < 500:
                flag1 = 1
                pos = pygame.mouse.get_pos()
                get_cord(pos)
                selected_cell = (int(y), int(x))
        
        if event.type == pygame.KEYDOWN:
            #music controls
            if event.key == pygame.K_m:  # Mute/Unmute
                if pygame.mixer.music.get_volume() > 0:
                    pygame.mixer.music.set_volume(0)
                else:
                    pygame.mixer.music.set_volume(0.5)
            
            if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:  # Increase volume
                current_volume = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(min(1.0, current_volume + 0.1))
            
            if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:  # Decrease volume
                current_volume = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(max(0.0, current_volume - 0.1))
            
        # end music loop
            if selected_cell is not None:
                row, col = selected_cell
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, 
                         pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                    val = int(event.unicode)
                    if is_valid_move(grid, row, col, val):
                        grid[row][col] = val
                        flag1 = 0
                    else:
                        mistake_counter += 1
                        raise_error2()
                        if mistake_counter >= 5:
                            show_game_over()
                            pygame.time.delay(2000)
                            reset_game()
                            continue
                        
            if event.key == pygame.K_RETURN:
                flag2 = 1
            elif event.key == pygame.K_r:
                grid = generate_sudoku(current_difficulty)
                start_time = time.time()
                mistake_counter = 0
                flag1 = flag2 = rs = error = 0
                selected_cell = None
            elif event.key == pygame.K_d:
                if solve(grid, 0, 0) == False:
                    error = 1
                else:
                    rs = 1
                    flag2 = 0
    
    if flag2 == 1:
        if solve(grid, 0, 0) == False:
            error = 1
        else:
            rs = 1
        flag2 = 0   
    
    draw() 
    draw_difficulty_menu()
    
    if flag1 == 1:
        draw_box()      
    
    instruction()   
    pygame.display.update() 
pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()