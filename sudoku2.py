import pygame
import random
 
# initialise the pygame font
pygame.font.init()
 
# Total window
screen = pygame.display.set_mode((700, 600))
 
# Title and Icon
pygame.display.set_caption("SUDOKU SOLVER USING BACKTRACKING")
x = 0
y = 0
dif = 500 / 9
val = 0

# Difficulty Levels
DIFFICULTY_LEVELS = [
    {"name": "Easy", "empty_cells": 20, "bg": "beach.jpg"},
    {"name": "Novice", "empty_cells": 35, "bg": "mtn.jpg"},
    {"name": "Mild", "empty_cells": 45, "bg": "forest.jpg"},
    {"name": "Evil", "empty_cells": 55, "bg": "arctic.jpg"},
    {"name": "Impossible", "empty_cells": 65, "bg": "desert.jpg"}
]

# Load background images
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
current_difficulty = DIFFICULTY_LEVELS[1]  # Default to "Easy"

# Default Sudoku Board
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
 
# Load test fonts for future use
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

def valid(grid, row, col, val):
    """Check if the value can be placed at the given row and column"""
    # Check row
    for x in range(9):
        if grid[row][x] == val:
            return False
    
    # Check column
    for x in range(9):
        if grid[x][col] == val:
            return False
    
    # Check 3x3 box
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == val:
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
    instruction_surface = pygame.Surface((190, 100))
    instruction_surface.fill((255, 255, 255))  # White background
    instruction_surface.set_alpha(200)  # Semi-transparent (0-255)
    screen.blit(instruction_surface, (500, 470))

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
    for i in range(2):
        pygame.draw.line(screen, (255, 0, 0), (x * dif-3, (y + i)*dif), (x * dif + dif + 3, (y + i)*dif), 7)
        pygame.draw.line(screen, (255, 0, 0), ( (x + i)* dif, y * dif ), ((x + i) * dif, y * dif + dif), 7)  

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
    
    text1 = font2.render("PRESS R TO RESET", 1, (0, 0, 0))
    text2 = font2.render("PRESS D TO SOLVE", 1, (0, 0, 0))
    text3 = font2.render("PRESS ENTER AFTER", 1, (0, 0, 0))
    text4 = font2.render("INPUT", 1, (0, 0, 0))

    text4_width = text4.get_width()
    screen_width = 700
    right_margin = 20

    screen.blit(text1, (510, 480))
    screen.blit(text2, (510, 500))
    screen.blit(text3, (510, 520))
    screen.blit(text4, (screen_width - text4_width - right_margin, 540))

def raise_error1():
    text1 = font2.render("ERROR!", 1, (255, 0, 0))
    screen.blit(text1, (510, 500))
    pygame.display.update()
    pygame.time.delay(1000)

def raise_error2():
    text1 = font2.render("WRONG!", 1, (255, 0, 0))
    screen.blit(text1, (510, 500))
    pygame.display.update()
    pygame.time.delay(1000)

# Main game loop
grid = generate_sudoku(current_difficulty)
run = True
flag1 = 0
flag2 = 0
rs = 0
error = 0
selected_cell = None

while run:
    # screen.fill((255, 255, 255))
    
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
            if selected_cell is not None:
                row, col = selected_cell
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, 
                         pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                    val = int(event.unicode)
                    if valid(grid, row, col, val):
                        grid[row][col] = val
                        flag1 = 0
                    else:
                        raise_error2()
                        
            if event.key == pygame.K_RETURN:
                flag2 = 1
            elif event.key == pygame.K_r:
                grid = generate_sudoku(current_difficulty)
                flag1 = 0
                flag2 = 0
                rs = 0
                error = 0
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
 
pygame.quit()