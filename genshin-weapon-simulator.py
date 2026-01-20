import random
import numpy as np
import matplotlib.pyplot as plt

BASE_RATE = 0.006
SOFT_PITY_START = 65
HARD_PITY = 80

TARGET_RATE_UPS = 5
EXPERIMENTS = 10000  # smoother stats
RATE_UP_CHANCE = 0.375  # 75% rate-up (50% for specific one out of two), 25% off-banner

def five_star_chance(pity):
    """Return the chance of pulling a 5★ at current pity count."""
    if pity < SOFT_PITY_START:
        return BASE_RATE
    ramp_steps = HARD_PITY - SOFT_PITY_START
    increase_per_pull = (1.0 - BASE_RATE) / ramp_steps
    return min(1.0, BASE_RATE + (pity - SOFT_PITY_START + 1) * increase_per_pull)

def run_experiment():
    pulls = 0
    pity = 0
    rate_up_count = 0
    first_rate_up_pull = None
    guarantee_rate_up = False

    while rate_up_count < TARGET_RATE_UPS:
        pulls += 1
        pity += 1

        # Hard pity
        if pity >= HARD_PITY:
            pity = 0
            if guarantee_rate_up or random.random() < RATE_UP_CHANCE:
                rate_up_count += 1
                if first_rate_up_pull is None:
                    first_rate_up_pull = pulls
                guarantee_rate_up = False
            else:
                guarantee_rate_up = True
            continue

        # Normal pull
        if random.random() < five_star_chance(pity):
            pity = 0
            if guarantee_rate_up or random.random() < RATE_UP_CHANCE:
                rate_up_count += 1
                if first_rate_up_pull is None:
                    first_rate_up_pull = pulls
                guarantee_rate_up = False
            else:
                guarantee_rate_up = True

    return pulls, first_rate_up_pull

def main():
    total_pulls_list = []
    first_rate_up_list = []

    for _ in range(EXPERIMENTS):
        total_pulls, first_pull = run_experiment()
        total_pulls_list.append(total_pulls)
        first_rate_up_list.append(first_pull)

    # ---------- Statistics ----------
    min_pulls = min(total_pulls_list)
    max_pulls = max(total_pulls_list)
    avg_pulls = np.mean(total_pulls_list)
    perc_5 = np.percentile(total_pulls_list, 5)
    perc_95 = np.percentile(total_pulls_list, 95)

    avg_first_pull = np.mean(first_rate_up_list)
    perc_5_first = np.percentile(first_rate_up_list, 5)
    perc_95_first = np.percentile(first_rate_up_list, 95)

    print("========== RESULTS ==========")
    print(f"Experiments run: {EXPERIMENTS}")
    print(f"Best Luck Scenario (minimum pulls): {min_pulls}")
    print(f"Worst Luck Scenario (maximum pulls): {max_pulls}")
    print(f"Average pulls needed for {TARGET_RATE_UPS} rate-ups: {avg_pulls:.2f}")
    print(f"5th percentile pulls (rate-ups): {perc_5}")
    print(f"95th percentile pulls (rate-ups): {perc_95}")
    print()
    print(f"Average pulls for FIRST rate-up: {avg_first_pull:.2f}")
    print(f"5th percentile first rate-up: {perc_5_first}")
    print(f"95th percentile first rate-up: {perc_95_first}")

    # ---------- Smooth line distributions ----------
    bins = np.arange(0, max(total_pulls_list)+2, 1)
    counts, _ = np.histogram(total_pulls_list, bins=bins)
    plt.figure(figsize=(10,6))
    plt.plot(bins[:-1], counts, linewidth=2)
    plt.xlabel("Total Pulls")
    plt.ylabel("Frequency")
    plt.title(f"Distribution of Pulls Needed for {TARGET_RATE_UPS} Rate-Ups (75% rate-up)")
    plt.grid(True)
    plt.show()

    bins_first = np.arange(0, max(first_rate_up_list)+2, 1)
    counts_first, _ = np.histogram(first_rate_up_list, bins=bins_first)
    plt.figure(figsize=(10,6))
    plt.plot(bins_first[:-1], counts_first, linewidth=2)
    plt.xlabel("Pulls to First Rate-Up")
    plt.ylabel("Frequency")
    plt.title("Distribution of Pulls Needed for First Rate-Up (75% rate-up)")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
