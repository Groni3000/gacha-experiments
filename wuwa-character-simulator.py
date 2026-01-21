import random

import matplotlib.pyplot as plt
import numpy as np

SEED = 42  # 42 is the answer
BASE_RATE = 0.008
SOFT_PITY_START = 65
HARD_PITY = 80

TARGET_ON_RATES = 5
EXPERIMENTS = 10000


def five_star_chance(pity):
    if pity >= 79:
        return 1.0
    elif pity > 75:
        additional_rate = 0.6 + 0.1 * (pity - 75)
    elif pity > 70:
        additional_rate = 0.2 + 0.08 * (pity - 70)
    elif pity > 65:
        additional_rate = 0.04 * (pity - 65)
    else:
        additional_rate = 0

    rate = BASE_RATE + additional_rate

    return rate


def run_experiment():
    pulls = 0
    pity = 0
    on_rate_count = 0
    guarantee_on_rate = False
    first_on_rate_pull = None
    first_5star_obtained = False
    first_5050_lost = False

    while on_rate_count < TARGET_ON_RATES:
        pulls += 1
        pity += 1

        if pity >= HARD_PITY:  # Hard pity
            pity = 0
            if guarantee_on_rate or random.random() < 0.5:
                on_rate_count += 1
                if first_on_rate_pull is None:
                    first_on_rate_pull = pulls
                guarantee_on_rate = False
            else:
                guarantee_on_rate = True
            continue

        if random.random() < five_star_chance(pity):
            pity = 0
            if not first_5star_obtained:
                first_5star_obtained = True
                if random.random() >= 0.5:  # lost 50/50
                    first_5050_lost = True
                    guarantee_on_rate = True
                else:
                    on_rate_count += 1
                    first_on_rate_pull = pulls
            else:
                if guarantee_on_rate or random.random() < 0.5:
                    on_rate_count += 1
                    if first_on_rate_pull is None:
                        first_on_rate_pull = pulls
                    guarantee_on_rate = False
                else:
                    guarantee_on_rate = True

    return pulls, first_on_rate_pull, first_5050_lost


def main():
    # Set random seed to have reproducable results
    np.random.seed(SEED)
    results = []
    first_on_rate_pulls = []
    first_5050_count = 0

    for _ in range(EXPERIMENTS):
        pulls_needed, first_pull, lost_first_5050 = run_experiment()
        results.append(pulls_needed)
        first_on_rate_pulls.append(first_pull)
        if lost_first_5050:
            first_5050_count += 1

    print("========== RESULTS ==========")
    print(f"Experiments run: {EXPERIMENTS}")
    print(f"Minimum pulls needed: {min(results)}")
    print(f"Maximum pulls needed: {max(results)}")
    print(f"Average pulls needed: {np.mean(results):.2f}")
    print(f"5th percentile pulls needed: {np.percentile(results, 5):.0f}")
    print(f"95th percentile pulls needed: {np.percentile(results, 95):.0f}")
    print(f"Average pulls to first rate-up: {np.mean(first_on_rate_pulls):.2f}")
    print(
        f"5th percentile for first rate-up: {np.percentile(first_on_rate_pulls, 5):.0f}"
    )
    print(
        f"95th percentile for first rate-up: {np.percentile(first_on_rate_pulls, 95):.0f}"
    )
    print(f"Number of experiments that lost the first 50/50: {first_5050_count}")

    # --------------------
    # Smooth integer-based line: total pulls
    # --------------------
    counts = np.bincount(results)
    x = np.arange(len(counts))
    plt.figure(figsize=(10, 6))
    plt.plot(x, counts, linewidth=2)
    plt.xlabel("Pulls Required")
    plt.ylabel("Frequency")
    plt.title("(WUWA) Total Pulls Needed for 5 Character On-Rates")
    plt.grid(True)
    plt.show()

    # --------------------
    # Smooth integer-based line: first on-rate
    # --------------------
    counts_first = np.bincount(first_on_rate_pulls)
    x_first = np.arange(len(counts_first))
    plt.figure(figsize=(10, 6))
    plt.plot(x_first, counts_first, linewidth=2)
    plt.xlabel("Pulls to First Rate-Up")
    plt.ylabel("Frequency")
    plt.title("(WUWA) Total Pulls Needed for First Character On-Rate")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
