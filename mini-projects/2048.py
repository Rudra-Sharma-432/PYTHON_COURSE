import pygame
import sys

# 1. Initialize Pygame engine
pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("2048 | By Rudra Sharma")
clock = pygame.time.Clock()

# grid = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
grid = [
    [0, 2, 0, 0],
    [4, 0, 4, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 3]
]

def goUP():
  print("hello")

def goRIGHT():
  for i in range(4):
     for j in range(3):
        if grid[i][j] == 0:
           grid[i][j] = grid[i][j+1]
           grid[i][j+1] = 0
        elif grid[i][j] == grid[i][j+1]:
          grid[i][j] += 2 * grid[i][j]
          grid[i][j+1] = 0


def goDOWN():
    print()

def goLEFT():
   print()

x = 10
y = 10


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
            elif event.key == pygame.K_RIGHT:
                goRIGHT()
            elif event.key == pygame.K_UP:
                goUP()
            elif event.key == pygame.K_DOWN:
                goDOWN()

            print(grid)

    # Move player using keyboard state
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_LEFT]:  goLEFT()
    # if keys[pygame.K_RIGHT]: goRIGHT()
    # if keys[pygame.K_UP]:    goUP()
    # if keys[pygame.K_DOWN]:  goDOWN()

    # 3. Render updates onto the window screen
    screen.fill((0, 0, 0)) # Clear screen with black
    pygame.draw.rect(screen, (0, 255, 0), (x, y, 30, 30)) # Draw player
    
    pygame.display.flip() # Refresh display
    clock.tick(60) # Lock frame rate to 60 FPS
