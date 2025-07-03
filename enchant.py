from multiprocessing import Pool
from random import random
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np

def single_trial(target: int, success_prob: float) -> int:
    level = 3
    bless_scrolls_used = 0
    while level < target:
        bless_scrolls_used += 1
        success = random() < success_prob
        if success:
            level += 1
        else:
            level = 3
    return bless_scrolls_used

def trial_batch(args) -> list[int]:
    target, success_prob, batch_size = args
    return [single_trial(target, success_prob) for _ in range(batch_size)]

def simulate_enchant(trials: int, target: int, success_prob: float, processes: int = 25, batch_size: int = 1000) -> list[int]:
    if trials % 1000 != 0:
        raise ValueError("trials size must be devitalise by 1000")
    batches = [(target, success_prob, batch_size)] * (trials // batch_size)
    with Pool(processes=processes) as pool:
        chunks = list(tqdm(pool.imap_unordered(trial_batch, batches), total=len(batches)))
    return [x for chunk in chunks for x in chunk]  # flatten

def main() -> None:
    target = 16
    success_prob = 0.50
    trials = 1_000_000
    results = simulate_enchant(trials, target, success_prob)

    sorted_results = sorted(results)
    cumulative_prob = np.arange(1, len(sorted_results) + 1) / len(sorted_results)

    # Calculate statistics
    median_val = np.median(results)
    mean_val = np.mean(results)
    p90_val = np.percentile(results, 90)
    p99_val = np.percentile(results, 99)
    p99_9_val = np.percentile(results, 99.9)
    below_avg = np.mean(np.array(results) < mean_val) * 100

    plt.figure(figsize=(10, 6))
    plt.plot(sorted_results, cumulative_prob, label="Cumulative Probability")
    plt.axhline(0.5, color='red', linestyle='dashed', label=f'Median: {median_val:.0f}')
    plt.axhline(0.9, color='orange', linestyle='dashed', label=f'90% ≤: {p90_val:.0f}')
    plt.axhline(0.99, color='green', linestyle='dashed', label=f'99% ≤: {p99_val:.0f}')
    plt.axhline(0.999, color='purple', linestyle='dashed', label=f'99.9% ≤: {p99_9_val:.0f}')
    plt.axvline(mean_val, color='blue', linestyle='dotted', label=f'Average: {mean_val:.0f}')
    plt.xlabel("Number of Blessed Scrolls")
    plt.xticks(np.linspace(0, max(sorted_results), 20, dtype=int))
    plt.ylabel("Cumulative Probability")
    plt.title(f"Cumulative Distribution of Blessed Scrolls to Reach +{target}\n"
              f"{below_avg:.2f}% of cases are below average ({mean_val:.0f})")
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()