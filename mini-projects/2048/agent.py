"""Both AIs behind the same interface: .pick(grid) -> 0 RIGHT / 1 UP / 2 LEFT / 3 DOWN (or None).

  Agent          : NEAT genome        (made by train_neat.py -> best_genome.json)
  BackpropAgent  : backprop network   (made by train.py      -> weights.json)

Both rank the 4 moves and play the best-ranked move that actually changes the board.
"""
import os
import game2048 as game
import neat_ai as neat

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "best_genome.json")


def _best_valid(scores, grid):
    for d in sorted(range(4), key=lambda i: -scores[i]):
        if game.move(grid, d)[2]:
            return d
    return None


class Agent:
    """NEAT agent."""

    def __init__(self, path=PATH):
        self.net = neat.Network(neat.Genome.load(path))

    def pick(self, grid):
        return _best_valid(self.net.activate(game.encode_grid(grid)), grid)


class BackpropAgent:
    """Agent using the network trained with backprop (ai.py + train.py)."""

    def __init__(self):
        import ai
        self.nn = ai.NeuralNetwork()
        if not self.nn.load():
            raise FileNotFoundError("weights.json not found")

    def pick(self, grid):
        return _best_valid(self.nn.forward(grid), grid)


def load_agents():
    """Returns {name: agent or None} and {name: error message or None}."""
    agents, errors = {}, {}
    for name, make, hint in (
        ("NEAT", Agent, "no best_genome.json - run train_neat.py"),
        ("BACKPROP", BackpropAgent, "no weights.json - run train.py"),
    ):
        try:
            agents[name], errors[name] = make(), None
        except FileNotFoundError:
            agents[name], errors[name] = None, hint
        except Exception as e:
            agents[name], errors[name] = None, f"{name} failed to load: {e}"
    return agents, errors