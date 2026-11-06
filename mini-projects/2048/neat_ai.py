"""A compact NEAT implementation (feed-forward only, no dependencies)."""
import math
import random
import json


class Config:
    # mutation
    p_weight = 0.8          # chance a genome gets its weights mutated
    p_perturb = 0.97        # per-weight: small nudge (else replaced with new random value)
    perturb_std = 0.3
    p_add_conn = 0.15
    p_add_node = 0.05
    weight_limit = 8.0
    # speciation
    target_species = 8
    threshold = 1.0         # adjusted automatically each generation
    c_struct = 1.0
    c_weight = 0.4
    # reproduction
    survival = 0.25
    elitism_min_species = 5
    stale_limit = 15
    p_crossover = 0.75


class ConnGene:
    __slots__ = ("innov", "inp", "out", "w", "enabled")

    def __init__(self, innov, inp, out, w, enabled=True):
        self.innov, self.inp, self.out, self.w, self.enabled = innov, inp, out, w, enabled


class Innovations:
    """Gives the same id to the same structural change, so genomes can be aligned later."""

    def __init__(self, first_free_node):
        self.conn_ids = {}   # (in, out) -> innovation id
        self.split_ids = {}  # innovation id of split connection -> new node id
        self.next_innov = 0
        self.next_node = first_free_node

    def conn(self, a, b):
        key = (a, b)
        if key not in self.conn_ids:
            self.conn_ids[key] = self.next_innov
            self.next_innov += 1
        return self.conn_ids[key]

    def node_for_split(self, innov):
        if innov not in self.split_ids:
            self.split_ids[innov] = self.next_node
            self.next_node += 1
        return self.split_ids[innov]


class Genome:
    def __init__(self, n_in, n_out):
        self.n_in, self.n_out = n_in, n_out
        self.conns = {}  # innov -> ConnGene
        self.fitness = 0.0

    # node ids: inputs 0..n_in-1 | bias n_in | outputs n_in+1.. | hidden after that
    @property
    def bias_id(self):
        return self.n_in

    @property
    def output_ids(self):
        return list(range(self.n_in + 1, self.n_in + 1 + self.n_out))

    @property
    def first_hidden(self):
        return self.n_in + 1 + self.n_out

    def hidden_nodes(self):
        nodes = set()
        for c in self.conns.values():
            for n in (c.inp, c.out):
                if n >= self.first_hidden:
                    nodes.add(n)
        return nodes

    @staticmethod
    def initial(n_in, n_out, inn):
        g = Genome(n_in, n_out)
        for a in list(range(n_in)) + [n_in]:           # inputs + bias
            for b in g.output_ids:
                innov = inn.conn(a, b)
                g.conns[innov] = ConnGene(innov, a, b, random.gauss(0, 1))
        return g

    def copy(self):
        g = Genome(self.n_in, self.n_out)
        g.conns = {k: ConnGene(c.innov, c.inp, c.out, c.w, c.enabled) for k, c in self.conns.items()}
        g.fitness = self.fitness
        return g

    # ---------------- mutation ----------------
    def _creates_cycle(self, a, b):
        """Would adding a -> b create a loop? (is there already a path b -> ... -> a)"""
        if a == b:
            return True
        children = {}
        for c in self.conns.values():
            children.setdefault(c.inp, []).append(c.out)
        stack, seen = [b], set()
        while stack:
            n = stack.pop()
            if n == a:
                return True
            if n in seen:
                continue
            seen.add(n)
            stack.extend(children.get(n, []))
        return False

    def mutate(self, inn, cfg):
        if random.random() < cfg.p_weight:
            for c in self.conns.values():
                if random.random() < cfg.p_perturb:
                    c.w += random.gauss(0, cfg.perturb_std)
                else:
                    c.w = random.uniform(-2, 2)
                c.w = max(-cfg.weight_limit, min(cfg.weight_limit, c.w))
        if random.random() < cfg.p_add_conn:
            self.add_conn(inn)
        if random.random() < cfg.p_add_node:
            self.add_node(inn)

    def add_conn(self, inn):
        hidden = list(self.hidden_nodes())
        sources = list(range(self.n_in + 1)) + hidden
        targets = self.output_ids + hidden
        existing = {(c.inp, c.out) for c in self.conns.values()}
        for _ in range(30):
            a, b = random.choice(sources), random.choice(targets)
            if (a, b) in existing or self._creates_cycle(a, b):
                continue
            innov = inn.conn(a, b)
            self.conns[innov] = ConnGene(innov, a, b, random.uniform(-1, 1))
            return True
        return False

    def add_node(self, inn):
        candidates = [c for c in self.conns.values() if c.enabled]
        if not candidates:
            return False
        c = random.choice(candidates)
        new_node = inn.node_for_split(c.innov)
        if new_node in self.hidden_nodes():
            return False
        c.enabled = False
        i1 = inn.conn(c.inp, new_node)
        i2 = inn.conn(new_node, c.out)
        self.conns[i1] = ConnGene(i1, c.inp, new_node, 1.0)   # keeps behaviour almost unchanged
        self.conns[i2] = ConnGene(i2, new_node, c.out, c.w)
        return True

    # ---------------- (de)serialisation ----------------
    def to_dict(self):
        return {"n_in": self.n_in, "n_out": self.n_out, "fitness": self.fitness,
                "conns": [[c.innov, c.inp, c.out, c.w, c.enabled] for c in self.conns.values()]}

    @staticmethod
    def from_dict(d):
        g = Genome(d["n_in"], d["n_out"])
        g.fitness = d.get("fitness", 0.0)
        for innov, a, b, w, en in d["conns"]:
            g.conns[innov] = ConnGene(innov, a, b, w, en)
        return g

    def save(self, path):
        with open(path, "w") as f:
            json.dump(self.to_dict(), f)

    @staticmethod
    def load(path):
        with open(path) as f:
            return Genome.from_dict(json.load(f))


def distance(a, b, cfg):
    ia, ib = set(a.conns), set(b.conns)
    n = max(len(ia), len(ib), 1)
    structural = len(ia ^ ib) / n                      # excess + disjoint genes
    shared = ia & ib
    wdiff = sum(abs(a.conns[i].w - b.conns[i].w) for i in shared) / len(shared) if shared else 0.0
    return cfg.c_struct * structural + cfg.c_weight * wdiff


def crossover(a, b):
    """Child keeps the fitter parent's structure; shared genes get weights from either parent."""
    fit, other = (a, b) if a.fitness >= b.fitness else (b, a)
    child = Genome(fit.n_in, fit.n_out)
    for innov, g in fit.conns.items():
        og = other.conns.get(innov)
        src = og if (og is not None and random.random() < 0.5) else g
        enabled = True
        if not g.enabled or (og is not None and not og.enabled):
            enabled = random.random() > 0.75           # 75% chance to stay disabled
        child.conns[innov] = ConnGene(innov, g.inp, g.out, src.w, enabled)
    return child


class Network:
    def __init__(self, genome):
        self.n_in = genome.n_in
        self.bias = genome.bias_id
        self.outputs = genome.output_ids
        enabled = [c for c in genome.conns.values() if c.enabled]

        nodes = set(range(genome.n_in + 1)) | set(self.outputs) | genome.hidden_nodes()
        indeg = {n: 0 for n in nodes}
        children = {n: [] for n in nodes}
        self.incoming = {n: [] for n in nodes}
        for c in enabled:
            indeg[c.out] += 1
            children[c.inp].append(c.out)
            self.incoming[c.out].append((c.inp, c.w))

        queue = [n for n in nodes if indeg[n] == 0]
        order = []
        while queue:                                    # topological order (Kahn)
            n = queue.pop()
            order.append(n)
            for m in children[n]:
                indeg[m] -= 1
                if indeg[m] == 0:
                    queue.append(m)
        self.order = [n for n in order if n > self.bias]  # skip inputs + bias

    def activate(self, inputs):
        vals = {i: x for i, x in enumerate(inputs)}
        vals[self.bias] = 1.0
        for n in self.order:
            s = 0.0
            for src, w in self.incoming[n]:
                s += vals.get(src, 0.0) * w
            vals[n] = math.tanh(s)
        return [vals.get(o, 0.0) for o in self.outputs]


class Species:
    def __init__(self, sid, rep):
        self.id = sid
        self.rep = rep
        self.members = []
        self.best_fitness = -1e18
        self.stale = 0


class Population:
    def __init__(self, size, n_in, n_out, cfg=None):
        self.cfg = cfg or Config()
        self.size = size
        self.inn = Innovations(first_free_node=n_in + 1 + n_out)
        self.genomes = [Genome.initial(n_in, n_out, self.inn) for _ in range(size)]
        self.species = []
        self.next_species_id = 0
        self.generation = 0
        self.best = None  # best genome ever (copy)

    def speciate(self):
        cfg = self.cfg
        for s in self.species:
            s.members = []
        for g in self.genomes:
            for s in self.species:
                if distance(g, s.rep, cfg) < cfg.threshold:
                    s.members.append(g)
                    break
            else:
                s = Species(self.next_species_id, g)
                self.next_species_id += 1
                s.members.append(g)
                self.species.append(s)
        self.species = [s for s in self.species if s.members]
        # keep the number of species near the target by moving the threshold
        if len(self.species) > cfg.target_species:
            cfg.threshold += 0.1
        elif len(self.species) < cfg.target_species:
            cfg.threshold = max(0.2, cfg.threshold - 0.1)

    def next_generation(self):
        """Call after setting genome.fitness for every genome."""
        cfg = self.cfg
        self.speciate()

        for g in self.genomes:
            if self.best is None or g.fitness > self.best.fitness:
                self.best = g.copy()

        for s in self.species:
            s.members.sort(key=lambda g: g.fitness, reverse=True)
            if s.members[0].fitness > s.best_fitness:
                s.best_fitness = s.members[0].fitness
                s.stale = 0
            else:
                s.stale += 1

        # drop stagnant species, but always keep the 2 best
        ranked = sorted(self.species, key=lambda s: s.best_fitness, reverse=True)
        keep = set(id(s) for s in ranked[:2])
        self.species = [s for s in self.species if s.stale < cfg.stale_limit or id(s) in keep]

        # offspring per species ~ its average fitness (fitness sharing)
        means = [sum(g.fitness for g in s.members) / len(s.members) for s in self.species]
        total = sum(means)
        if total <= 0:
            quotas = [self.size // len(self.species)] * len(self.species)
        else:
            quotas = [int(self.size * m / total) for m in means]
        best_idx = max(range(len(means)), key=lambda i: means[i])
        quotas[best_idx] += self.size - sum(quotas)

        new = []
        for s, quota in zip(self.species, quotas):
            if quota <= 0:
                continue
            if len(s.members) >= cfg.elitism_min_species:
                new.append(s.members[0].copy())          # champion survives unchanged
            cut = max(2, math.ceil(len(s.members) * cfg.survival))
            parents = s.members[:cut]
            while len(new) < sum(quotas[:self.species.index(s) + 1]) and len(new) < self.size:
                p1 = random.choice(parents)
                if random.random() < cfg.p_crossover and len(parents) > 1:
                    child = crossover(p1, random.choice(parents))
                else:
                    child = p1.copy()
                child.mutate(self.inn, cfg)
                child.fitness = 0.0
                new.append(child)
            s.rep = random.choice(s.members)

        while len(new) < self.size:                      # safety net for rounding
            child = random.choice(self.genomes).copy()
            child.mutate(self.inn, cfg)
            new.append(child)

        self.genomes = new[:self.size]
        self.generation += 1