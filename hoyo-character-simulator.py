import random
import numpy as np
import matplotlib.pyplot as plt

BASE_RATE = 0.006
SOFT_PITY_START = 74
HARD_PITY = 90

TARGET_ON_RATES = 7
EXPERIMENTS = 10000

def five_star_chance(pity):
    if pity < SOFT_PITY_START:
        return BASE_RATE
    ramp_steps = HARD_PITY - SOFT_PITY_START
    increase_per_pull = (1.0 - BASE_RATE) / ramp_steps
    return min(1.0, BASE_RATE + (pity - SOFT_PITY_START + 1) * increase_per_pull)

def run_experiment():
    pulls = 0
    pity = 0
    on_rate_count = 0
    guarantee_on_rate = False
    first_on_rate_pull = None
    first_5050_lost = False
    first_5star_obtained = False

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
                if random.random() >= 0.5:
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
    print(f"Minimum pulls: {min(results)}")
    print(f"Maximum pulls: {max(results)}")
    print(f"Average pulls: {np.mean(results):.2f}")
    print(f"5th percentile pulls: {np.percentile(results,5):.0f}")
    print(f"95th percentile pulls: {np.percentile(results,95):.0f}")
    print(f"Average pulls to first on-rate: {np.mean(first_on_rate_pulls):.2f}")
    print(f"5th percentile first rate-up: {np.percentile(first_on_rate_pulls,5):.0f}")
    print(f"95th percentile first rate-up: {np.percentile(first_on_rate_pulls,95):.0f}")
    print(f"Number of experiments that lost the first 50/50: {first_5050_count}")

    # --------------------
    # Smooth integer-based line: total pulls
    # --------------------
    counts = np.bincount(results)
    x = np.arange(len(counts))
    plt.figure(figsize=(10,6))
    plt.plot(x, counts, linewidth=2, color='green')
    plt.xlabel("Pulls Required")
    plt.ylabel("Frequency")
    plt.title("(HOYO) Total Pulls Needed for 7 Character On-Rates")
    plt.grid(True)
    plt.show()

    # --------------------
    # Smooth integer-based line: first on-rate
    # --------------------
    counts_first = np.bincount(first_on_rate_pulls)
    x_first = np.arange(len(counts_first))
    plt.figure(figsize=(10,6))
    plt.plot(x_first, counts_first, linewidth=2, color='orange')
    plt.xlabel("Pulls to First Rate-Up")
    plt.ylabel("Frequency")
    plt.title("(HOYO) Total Pulls Needed for First Character On-Rate")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
