"""2048 | By Rudra Sharma

Controls
  Arrow keys / WASD : YOU move  (every real move is saved to data.jsonl for backprop)
  SPACE             : the selected AI plays ONE move
  P                 : toggle AI auto-play
  T                 : switch AI  (NEAT <-> BACKPROP)
  R                 : restart

Files needed in this folder:
  game2048.py, neat_ai.py, agent.py                (always)
  data.py                                          (saving your moves)
  ai.py                                            (backprop network)
  best_genome.json  <- made by train_neat.py       (NEAT AI)
  weights.json      <- made by train.py            (BACKPROP AI)
"""
import sys
import pygame

import game2048 as game
from agent import load_agents

try:
    import data                       # saves your moves for backprop training
    DATA_ERROR = None
except Exception as e:
    data = None
    DATA_ERROR = f"data.py missing - moves NOT saved"

agents, agent_errors = load_agents()

# ---------------------------------------------------------------- layout
WIDTH, HEIGHT = 400, 450
CELL_SIZE = 80
MARGIN = 10
START_X = 25
START_Y = 75
AUTO_DELAY_MS = 120

BG = (40, 40, 40)
EMPTY = (180, 180, 180)
TILE_COLORS = {
    1: (110, 110, 110), 2: (120, 140, 160), 4: (90, 150, 190),
    8: (80, 170, 150), 16: (100, 180, 100), 32: (170, 190, 80),
    64: (220, 180, 70), 128: (230, 140, 60), 256: (230, 100, 60),
    512: (220, 70, 70), 1024: (200, 60, 120), 2048: (170, 70, 200),
}
DEFAULT_TILE = (60, 60, 60)

KEY_TO_DIRECTION = {
    pygame.K_RIGHT: game.RIGHT, pygame.K_d: game.RIGHT,
    pygame.K_UP: game.UP,       pygame.K_w: game.UP,
    pygame.K_LEFT: game.LEFT,   pygame.K_a: game.LEFT,
    pygame.K_DOWN: game.DOWN,   pygame.K_s: game.DOWN,
}


def one_hot(direction):
    v = [0, 0, 0, 0]
    v[direction] = 1
    return v


class State:
    def __init__(self):
        self.ai_name = "NEAT"
        self.saved = 0                       # moves saved this session
        self.reset()

    def reset(self):
        self.grid = game.new_grid()
        self.score = 0
        self.moves = 0
        self.over = False
        self.auto = False
        self.message = DATA_ERROR or ""
        self.last_auto = 0

    def apply(self, direction, record=False):
        """Play a move. Only moves that change the board are played (and saved)."""
        if self.over:
            return False
        new, gained, moved = game.move(self.grid, direction)
        if not moved:
            return False                      # no-op: no spawn, NOT recorded
        if record and data is not None:
            flat = [v for row in self.grid for v in row]     # board BEFORE the move
            data.addMove(flat, one_hot(direction))
            self.saved += 1
        self.grid = new
        self.score += gained
        self.moves += 1
        game.spawn(self.grid)
        if not game.valid_moves(self.grid):
            self.over = True
            self.auto = False
        return True

    def current_agent(self):
        return agents.get(self.ai_name)

    def ai_move(self):
        a = self.current_agent()
        if a is None:
            self.message = f"{self.ai_name}: {agent_errors[self.ai_name]}"
            self.auto = False
            return
        d = a.pick(self.grid)
        if d is None:
            self.over = True
            self.auto = False
        else:
            self.apply(d)                     # AI moves are NOT recorded


def tile_font(fonts, value):
    digits = len(str(value))
    return fonts[0] if digits <= 2 else fonts[1] if digits == 3 else fonts[2]


def draw(screen, fonts, small, state):
    screen.fill(BG)

    best = max(max(r) for r in state.grid)
    head = small.render(f"Score: {state.score}    Best tile: {best}    Moves: {state.moves}",
                        True, (230, 230, 230))
    screen.blit(head, (START_X, 15))

    mode = f"AI AUTO-PLAY ({state.ai_name})" if state.auto else f"Your turn  |  AI: {state.ai_name}"
    saved = f"  |  Saved: {state.saved}" if data is not None else ""
    sub = small.render(mode + saved, True, (120, 200, 255) if state.auto else (160, 160, 160))
    screen.blit(sub, (START_X, 40))

    for r in range(4):
        for c in range(4):
            v = state.grid[r][c]
            x = START_X + c * (CELL_SIZE + MARGIN)
            y = START_Y + r * (CELL_SIZE + MARGIN)
            pygame.draw.rect(screen, EMPTY if v == 0 else TILE_COLORS.get(v, DEFAULT_TILE),
                             (x, y, CELL_SIZE, CELL_SIZE), border_radius=6)
            if v:
                text = tile_font(fonts, v).render(str(v), True, (255, 255, 255))
                screen.blit(text, text.get_rect(center=(x + CELL_SIZE / 2, y + CELL_SIZE / 2)))

    foot = state.message or "Arrows move  SPACE AI  P auto  T switch  R reset"
    screen.blit(small.render(foot, True, (150, 150, 150)), (START_X, HEIGHT - 22))

    if state.over:
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 150))
        screen.blit(shade, (0, 0))
        big = fonts[0].render("Game Over", True, (255, 255, 255))
        screen.blit(big, big.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 15)))
        hint = small.render("Press R to restart", True, (220, 220, 220))
        screen.blit(hint, hint.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 25)))


def handle_key(state, key):
    if key == pygame.K_r:
        state.reset()
        return
    state.message = ""
    if key in KEY_TO_DIRECTION:
        state.apply(KEY_TO_DIRECTION[key], record=True)
    elif key == pygame.K_SPACE:
        state.ai_move()
    elif key == pygame.K_t:
        state.ai_name = "BACKPROP" if state.ai_name == "NEAT" else "NEAT"
        state.auto = False
        if state.current_agent() is None:
            state.message = f"{state.ai_name}: {agent_errors[state.ai_name]}"
    elif key == pygame.K_p:
        if state.current_agent() is None:
            state.message = f"{state.ai_name}: {agent_errors[state.ai_name]}"
        elif not state.over:
            state.auto = not state.auto


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048 | By Rudra Sharma")
    clock = pygame.time.Clock()
    fonts = (pygame.font.SysFont("Arial", 36, bold=True),
             pygame.font.SysFont("Arial", 28, bold=True),
             pygame.font.SysFont("Arial", 22, bold=True))
    small = pygame.font.SysFont("Arial", 15)

    state = State()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                handle_key(state, event.key)

        if state.auto and not state.over:
            now = pygame.time.get_ticks()
            if now - state.last_auto >= AUTO_DELAY_MS:
                state.last_auto = now
                state.ai_move()

        draw(screen, fonts, small, state)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()