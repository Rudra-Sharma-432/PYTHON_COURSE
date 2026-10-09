import pygame
import sys
import random
import ai
import score

# 1. Initialize Pygame engine
pygame.init()
screen = pygame.display.set_mode((400, 450))
pygame.display.set_caption("2048 | By Rudra Sharma")
clock = pygame.time.Clock()

# grid = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
grid = [
    [0, 2, 0, 0],
    [4, 0, 4, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0]
]
emptyCells = []


nn = ai.NeuralNetwork()
# output = nn.forward(grid)
# print("Outputs:", output)
# print("Chosen move:", nn.predict(grid))

def goDOWN():
  for t in range(3):
    for i in range(3):
      for j in range(4):
        if grid[-i-1][j] == 0:
          grid[-i-1][j] = grid[-i-2][j]
          grid[-i-2][j] = 0
        elif grid[-i-1][j] == grid[-i-2][j]:
          grid[-i-1][j] *= 2
          grid[-i-2][j] = 0

def goUP():
  for t in range(3):
    for i in range(3):
      for j in range(4):
        if grid[i][j] == 0:
          grid[i][j] = grid[i+1][j]
          grid[i+1][j] = 0
        elif grid[i][j] == grid[i+1][j]:
          grid[i][j] *= 2
          grid[i+1][j] = 0

def goLEFT():
  for t in range(3):
    for i in range(4):
      for j in range(3):
        if grid[i][j] == 0:
          grid[i][j] = grid[i][j+1]
          grid[i][j+1] = 0
        elif grid[i][j] == grid[i][j+1]:
          grid[i][j] *= 2
          grid[i][j+1] = 0

def goRIGHT():
  for t in range(3):
    for i in range(4):
      for j in range(3):
        if grid[i][-j-1] == 0:
          grid[i][-j-1] = grid[i][-j-2]
          grid[i][-j-2] = 0
        elif grid[i][-j-1] == grid[i][-j-2]:
          grid[i][-j-1] *= 2
          grid[i][-j-2] = 0


def getEmptyCell():
  emptyCells = []
  for i in range(4):
     for j in range(4):
        if grid[i][j] == 0:
          emptyCells.append((i,j))

def generateNumber():
  emptyCells = []
  for i in range(4):
     for j in range(4):
        if grid[i][j] == 0:
          emptyCells.append((i,j))
  randomCell = random.choice(emptyCells)

  if random.random() > 0.9:
     grid[randomCell[0]][randomCell[1]] = 4
  elif random.random() > 0.6:
       grid[randomCell[0]][randomCell[1]] = 2
  else:
     grid[randomCell[0]][randomCell[1]] = 1


def aiMove():
    move = nn.predict(grid)

    output = nn.forward(grid)
    print("Outputs:", output)

    if move == 0:
        goUP()
        print("Chosen move: UP")
    elif move == 1:
        goDOWN()
        print("Chosen move: DOWN")
    elif move == 2:
        goLEFT()
        print("Chosen move: LEFT")
    elif move == 3:
        goRIGHT()
        print("Chosen move: RIGHT")

    generateNumber()
    

# 3. Grid Visual Dimensions
CELL_SIZE = 80   # Size of each square block
MARGIN = 10      # Gap between square blocks
START_X = 25     # Left offset to center the grid
START_Y = 75     # Top offset to center the grid

# Load a clean text font
FONT = pygame.font.SysFont("Arial", 36, bold=True)

# 2. Run the continuous Game Loop
while True:
    # Handle user inputs (keyboard/mouse)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # This block triggers EXACTLY ONCE per physical key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                goLEFT()
                generateNumber()

            elif event.key == pygame.K_RIGHT:
                goRIGHT()
                generateNumber()

            elif event.key == pygame.K_UP:
                goUP()
                generateNumber()

            elif event.key == pygame.K_DOWN:
                goDOWN()
                generateNumber()

            elif event.key == pygame.K_SPACE:
                aiMove()


    # 3. Render updates onto the window screen
    # Clear screen with a background color (Dark gray)
    screen.fill((40, 40, 40))

    # 4. Render the 4x4 Grid
    for row_idx in range(len(grid)):
        for col_idx in range(len(grid[row_idx])):
            # Fetch the actual number from your array
            number = grid[row_idx][col_idx]

            # Calculate the exact pixel position for this cell
            x = START_X + col_idx * (CELL_SIZE + MARGIN)
            y = START_Y + row_idx * (CELL_SIZE + MARGIN)

            # Draw the square grid background box (Light gray)
            pygame.draw.rect(screen, (180, 180, 180), (x, y, CELL_SIZE, CELL_SIZE))

            # Only draw the text if the value is not 0 (typical for games like 2048 or Sudoku)
            if number != 0:
              pygame.draw.rect(screen, (100, 100, 100), (x, y, CELL_SIZE, CELL_SIZE))
              text_surface = FONT.render(str(number), True, (0, 0, 0)) # Black text
                
              # Perfect alignment: Center the text inside the cell block
              text_rect = text_surface.get_rect(center=(x + CELL_SIZE/2, y + CELL_SIZE/2))
              screen.blit(text_surface, text_rect)

    # FONT.render(str(score.currentScore(grid)), True, (0, 0, 0))

    pygame.display.flip() # Refresh display
    clock.tick(60) # Lock frame rate to 60 FPS
