"""Headless 2048 engine (no pygame). Same tile spawn rules as your 2048.py.
Directions match your network outputs: 0 RIGHT, 1 UP, 2 LEFT, 3 DOWN."""
import math
import random

RIGHT, UP, LEFT, DOWN = 0, 1, 2, 3


def spawn(grid, rng=random):
    """Place a new tile on a random empty cell (same odds as your generateNumber)."""
    empty = [(i, j) for i in range(4) for j in range(4) if grid[i][j] == 0]
    if not empty:
        return False
    i, j = rng.choice(empty)
    if rng.random() > 0.9:
        grid[i][j] = 4
    elif rng.random() > 0.6:
        grid[i][j] = 2
    else:
        grid[i][j] = 1
    return True


def new_grid(rng=random):
    grid = [[0] * 4 for _ in range(4)]
    spawn(grid, rng)
    spawn(grid, rng)
    spawn(grid, rng)  # your game starts with 3 tiles
    return grid


def _slide_left(row):
    """Slide + merge one row to the left. Each tile merges at most ONCE per move."""
    tiles = [v for v in row if v]
    out, gained, i = [], 0, 0
    while i < len(tiles):
        if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
            out.append(tiles[i] * 2)
            gained += tiles[i] * 2
            i += 2
        else:
            out.append(tiles[i])
            i += 1
    out += [0] * (4 - len(out))
    return out, gained


def _transpose(g):
    return [list(r) for r in zip(*g)]


def move(grid, direction):
    """Returns (new_grid, score_gained, moved). Does NOT modify `grid`."""
    if direction in (UP, DOWN):
        work = _transpose(grid)
    else:
        work = [row[:] for row in grid]

    reverse = direction in (RIGHT, DOWN)
    total = 0
    result = []
    for row in work:
        r = row[::-1] if reverse else row
        r, gained = _slide_left(r)
        total += gained
        result.append(r[::-1] if reverse else r)

    if direction in (UP, DOWN):
        result = _transpose(result)
    return result, total, result != grid


def valid_moves(grid):
    return [d for d in range(4) if move(grid, d)[2]]


def encode_grid(grid):
    """Flatten + log-scale so inputs stay small (0 -> 0, 1 -> 1/12, 2 -> 2/12, 4 -> 3/12 ...)."""
    return [0.0 if v == 0 else (math.log2(v) + 1) / 12.0 for row in grid for v in row]