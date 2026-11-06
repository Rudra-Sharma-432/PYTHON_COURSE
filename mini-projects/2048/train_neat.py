import os
import sys
import time
import random
import multiprocessing as mp

import game2048 as game
import neat_ai as neat

POP_SIZE = 150
GENERATIONS = 200
GAMES_PER_GENOME = 3          # average over several games: 2048 spawns are random
MAX_MOVES = 3000
SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "best_genome.json")


def pick_move(net, grid):
    """Network ranks the 4 moves; we play the best-ranked move that actually changes the board."""
    out = net.activate(game.encode_grid(grid))
    for d in sorted(range(4), key=lambda i: -out[i]):
        new, gained, moved = game.move(grid, d)
        if moved:
            return new, gained
    return None, 0


def play(genome, seed):
    net = neat.Network(genome)
    rng = random.Random(seed)
    grid = game.new_grid(rng)
    score = 0
    for _ in range(MAX_MOVES):
        new, gained = pick_move(net, grid)
        if new is None:
            break                                        # no legal move: game over
        grid = new
        score += gained
        game.spawn(grid, rng)
    return score, max(max(r) for r in grid)


def evaluate(args):
    genome, seeds = args
    results = [play(genome, s) for s in seeds]
    return sum(r[0] for r in results) / len(results), max(r[1] for r in results)


def main():
    pop = neat.Population(POP_SIZE, n_in=16, n_out=4)
    workers = max(1, (os.cpu_count() or 2) - 1)
    pool = mp.Pool(workers)
    print(f"NEAT: pop={POP_SIZE}, workers={workers}, games/genome={GAMES_PER_GENOME}")

    best_saved = -1
    try:
        for gen in range(GENERATIONS):
            t0 = time.time()
            # every genome plays the SAME seeds this generation -> fair comparison
            seeds = [gen * 1000 + k for k in range(GAMES_PER_GENOME)]
            results = pool.map(evaluate, [(g, seeds) for g in pop.genomes])
            for g, (fit, _) in zip(pop.genomes, results):
                g.fitness = fit

            best_i = max(range(len(results)), key=lambda i: results[i][0])
            mean = sum(r[0] for r in results) / len(results)
            n_conns = len([c for c in pop.genomes[best_i].conns.values() if c.enabled])
            n_hidden = len(pop.genomes[best_i].hidden_nodes())
            print(f"gen {gen:3d} | best {results[best_i][0]:8.1f} | mean {mean:7.1f} | "
                  f"max tile {max(r[1] for r in results):4d} | species {len(pop.species):2d} | "
                  f"best net: {n_hidden} hidden, {n_conns} conns | {time.time() - t0:.1f}s")

            if results[best_i][0] > best_saved:
                best_saved = results[best_i][0]
                pop.genomes[best_i].save(SAVE_PATH)

            pop.next_generation()
    except KeyboardInterrupt:
        print("\nStopped. Best genome is already saved.")
    finally:
        pool.terminate()
    print("Saved:", SAVE_PATH)


if __name__ == "__main__":
    main()