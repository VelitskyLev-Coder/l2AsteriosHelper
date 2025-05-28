import itertools
import random
from typing import NamedTuple
import matplotlib.pyplot as plt

percentages = [
    0.97,
    0.95,
    0.93,
    0.91,
    0.89,
    0.87,
    0.85,
    0.83,
    0.81,
    0.79,
    0.77,
    0.75,
    0.73,
    0.71,
    0.69,
    0.67,
    0.65,
    0.63,
    0.61,
    0.59,
    0.57,
    0.55,
    0.53,
    0.51,
    0.44,
    0.42,
    0.40,
    0.28,
    0.26,
    0.24
]

costs = list(itertools.chain.from_iterable(
    [140_000+i*40000]*3 for i in range(10)))

class EncRecord(NamedTuple):
    n_codex: int
    n_master_codex: int
    n_adena: int
    n_sp: int
    n_exp: int

def simulate(master_threshold: int):
    n_codex = 0
    n_master_codex = 0
    n_adena = 0
    n_sp = 0
    n_exp = 0

    cur_level = 0
    max_level = 30

    while cur_level < max_level:
        is_master = (cur_level >= master_threshold)

        if is_master:
            master_multiplier = 5
            n_master_codex += 1
        else:
            master_multiplier = 1
            n_codex += 1

        n_adena += costs[cur_level]*master_multiplier
        if random.random() <= percentages[cur_level]:
            cur_level += 1
        else:
            cur_level = cur_level if is_master else 0
    return EncRecord(
                n_codex=n_codex,
                n_master_codex=n_master_codex,
                n_adena=n_adena,
                n_sp=n_sp,
                n_exp=n_exp,
    )

def sim_and_aggregate(master_threshold: int, n: int = 10000) -> EncRecord:
    results = [simulate(master_threshold) for _ in range(n)]
    averages = tuple(sum(x[i] for x in results) / n for i in range(len(results[0])))
    return EncRecord(*averages)

def get_cost(record: EncRecord, codex_cost: int, master_cost: int) -> int | float:
    return record.n_adena + codex_cost * record.n_codex + master_cost * record.n_master_codex

thresholds = list(range(5, 21))
costs = [get_cost(sim_and_aggregate(t), codex_cost=400_000, master_cost=20_000_000) for t in thresholds]

# Plotting
plt.figure()
plt.plot(thresholds, costs, marker='o')
plt.title("Cost vs Threshold")
plt.xlabel("Threshold")
plt.ylabel("Cost")
plt.grid(True)
plt.tight_layout()
plt.show()

