"""Loads best_genome.json and picks moves for the real game."""
import os
import game2048 as game
import neat_ai as neat

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "best_genome.json")


class Agent:
    def __init__(self, path=PATH):
        self.net = neat.Network(neat.Genome.load(path))

    def pick(self, grid):
        """Returns 0 RIGHT / 1 UP / 2 LEFT / 3 DOWN, or None if no move is possible."""
        out = self.net.activate(game.encode_grid(grid))
        for d in sorted(range(4), key=lambda i: -out[i]):
            if game.move(grid, d)[2]:
                return d
        return None