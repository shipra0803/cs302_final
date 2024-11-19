# claude2.py
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
    {"name": "Very Easy", "empty_cells": 20},
    {"name": "Easy", "empty_cells": 35},
    {"name": "Medium", "empty_cells": 45},
    {"name": "Hard", "empty_cells": 55},
    {"name": "Expert", "empty_cells": 65}
]
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
    # Assuming you have a solve function from your existing code
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
    """Check if the value can be placed at the given row and column for user input"""
    # Check row
    for x in range(9):
        if grid[row][x] == val and x != col:
            return False
    
    # Check column
    for x in range(9):
        if grid[x][col] == val and x != row:
            return False
    
    # Check 3x3 box
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == val and (start_row + i != row or start_col + j != col):
                return False
    
    return True

def solve(grid, row, col):
    # Base case: if we've reached the end of the grid, we're done
    if row == 8 and col == 9:
        return True
    
    # Move to next row if we've reached the end of current row
    if col == 9:
        row += 1
        col = 0
    
    # If cell is already filled, move to next cell
    if grid[row][col] > 0:
        return solve(grid, row, col + 1)
    
    # Try placing numbers 1-9
    for num in range(1, 10):
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
            
            # Recursively try to solve the rest of the grid
            if solve(grid, row, col + 1):
                return True
        
        # If placing the number doesn't work, backtrack
        grid[row][col] = 0
    
    # If no number works, return False
    return False

def solve_full_grid(grid):
    # Implement a full grid solving function similar to your existing solve function
    # This is a placeholder - you'll need to implement the actual solving logic
    solved_grid = [row[:] for row in grid]
    solve(solved_grid, 0, 0)
    return solved_grid

def get_cord(pos):
    global x
    x = int(pos[0]//dif)
    global y
    y = int(pos[1]//dif)
 
def draw_difficulty_menu():
    """Draw difficulty selection menu on the screen"""
    menu_x, menu_y = 510, 100
    for i, diff in enumerate(DIFFICULTY_LEVELS):
        text = font2.render(diff['name'], 1, (255, 255, 255))
        rect = pygame.Rect(menu_x, menu_y + i*50, 150, 40)
        
        # Highlight current difficulty
        if diff == current_difficulty:
            pygame.draw.rect(screen, (100, 100, 100), rect)
        else:
            pygame.draw.rect(screen, (50, 50, 50), rect)
        
        screen.blit(text, (menu_x + 10, menu_y + i*50 + 10))

# Rest of your existing functions (draw_box, draw, draw_val, etc.)
def draw_box():
    for i in range(2):
        pygame.draw.line(screen, (255, 0, 0), (x * dif-3, (y + i)*dif), (x * dif + dif + 3, (y + i)*dif), 7)
        pygame.draw.line(screen, (255, 0, 0), ( (x + i)* dif, y * dif ), ((x + i) * dif, y * dif + dif), 7)  
 
def draw():
    for i in range (9):
        for j in range (9):
            if grid[i][j]!= 0:
                pygame.draw.rect(screen, (0, 153, 153), (i * dif, j * dif, dif + 1, dif + 1))
                text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(text1, (i * dif + 15, j * dif + 15))
    
    for i in range(10):
        if i % 3 == 0 :
            thick = 7
        else:
            thick = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (500, i * dif), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 500), thick)     
 
# Other existing functions (draw_val, raise_error1, raise_error2, valid, solve, instruction, result)
# ... (keep all your existing implementation)

def instruction():
    # Render instruction text
    text1 = font2.render("PRESS R TO RESET", 1, (0, 0, 0))
    text2 = font2.render("PRESS D TO SOLVE", 1, (0, 0, 0))
    text3 = font2.render("PRESS ENTER AFTER INPUT", 1, (0, 0, 0))
    
    # Blit (draw) instructions on the screen
    screen.blit(text1, (510, 520))
    screen.blit(text2, (510, 540))
    screen.blit(text3, (510, 560))

def raise_error1():
    """Display an error for other invalid inputs"""
    text1 = font2.render("ERROR!", 1, (255, 0, 0))
    screen.blit(text1, (510, 500))
    pygame.display.update()
    pygame.time.delay(1000)  # Show error for 1 second

def raise_error2():
    """Display an error when an invalid number is entered"""
    text1 = font2.render("WRONG!", 1, (255, 0, 0))
    screen.blit(text1, (510, 500))
    pygame.display.update()
    pygame.time.delay(1000)  # Show error for 1 second

# Main game loop
grid = generate_sudoku(current_difficulty)
run = True
flag1 = 0
flag2 = 0
rs = 0
error = 0

while run:
    screen.fill((255, 255, 255))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
        
        # Difficulty selection
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Check if difficulty menu is clicked
            if mouse_x > 510 and mouse_x < 660:
                difficulty_index = (mouse_y - 100) // 50
                if 0 <= difficulty_index < len(DIFFICULTY_LEVELS):
                    current_difficulty = DIFFICULTY_LEVELS[difficulty_index]
                    # Regenerate grid with new difficulty
                    grid = generate_sudoku(current_difficulty)
                    # Reset game state
                    flag1 = 0
                    flag2 = 0
                    rs = 0
                    error = 0
        
        # Rest of your existing event handling
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag1 = 1
            pos = pygame.mouse.get_pos()
            get_cord(pos)
        
        # Existing key handling code...
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, 
                     pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                val = int(event.unicode)
                if valid(grid, y, x, val):
                    grid[y][x] = val
                    flag1 = 0
                else:
                    raise_error2()
            elif event.key == pygame.K_RETURN:
                flag2 = 1
            elif event.key == pygame.K_r:
                grid = generate_sudoku(current_difficulty)
                flag1 = 0
                flag2 = 0
                rs = 0
                error = 0
            elif event.key == pygame.K_d:
                if solve(grid, 0, 0) == False:
                    error = 1
                else:
                    rs = 1
                    flag2 = 0
    
    # Existing game logic
    if flag2 == 1:
        if solve(grid, 0, 0)== False:
            error = 1
        else:
            rs = 1
        flag2 = 0   
    
    # Rest of your existing game loop logic
    
    draw() 
    draw_difficulty_menu()
    
    if flag1 == 1:
        draw_box()      
    
    instruction()   
 
    pygame.display.update() 
 
pygame.quit()