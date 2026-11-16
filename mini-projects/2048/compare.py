"""Fair head-to-head: NEAT vs BACKPROP vs random, on the SAME game seeds.
Run:  python compare.py        (optionally: python compare.py 100)"""
import sys
import random
import game2048 as game
from agent import load_agents


class RandomAgent:
    def pick(self, grid):
        moves = game.valid_moves(grid)
        return random.choice(moves) if moves else None


def play(agent, seed, max_moves=5000):
    rng = random.Random(seed)
    grid = game.new_grid(rng)
    score = moves = 0
    while moves < max_moves:
        d = agent.pick(grid)
        if d is None:
            break
        grid, gained, _ = game.move(grid, d)
        score += gained
        game.spawn(grid, rng)
        moves += 1
    return score, max(max(r) for r in grid), moves


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    agents, errors = load_agents()
    agents["RANDOM"] = RandomAgent()
    seeds = [10_000_000 + i for i in range(n)]       # unseen by training (it uses small seeds)
    print(f"{n} games each, same seeds for everyone\n")
    print(f"{'agent':10s} {'avg score':>10s} {'best score':>11s} {'best tile':>10s} {'avg moves':>10s}")
    for name, a in agents.items():
        if a is None:
            print(f"{name:10s} unavailable ({errors.get(name)})")
            continue
        random.seed(0)
        res = [play(a, s) for s in seeds]
        print(f"{name:10s} {sum(r[0] for r in res)/n:10.0f} {max(r[0] for r in res):11d} "
              f"{max(r[1] for r in res):10d} {sum(r[2] for r in res)/n:10.0f}")