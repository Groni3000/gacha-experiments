import random
import numpy as np
import matplotlib.pyplot as plt

# --------------------
# Constants
# --------------------
SIX_STAR_CHANCE = 0.04
RATE_UP_CHANCE = 0.25
PULLS_PER_SET = 10
GUARANTEED_6_START = 31
GUARANTEED_6_END = 40
FIRST_RATE_UP_PITY_START = 71
FIRST_RATE_UP_PITY_END = 80
EXTRA_RATE_UPS = [180, 340, 500, 660, 820]

TARGET_RATE_UPS = 6
EXPERIMENTS = 10000

# --------------------
# Run a single experiment
# --------------------
def run_experiment():
    pulls = 0
    rate_up_count = 0
    six_star_counter = 0
    first_rate_up_obtained = False
    first_rate_up_pull = None
    extra_rate_up_schedule = EXTRA_RATE_UPS.copy()

    while rate_up_count < TARGET_RATE_UPS:
        for _ in range(PULLS_PER_SET):
            pulls += 1
            six_star_counter += 1
            got_six_star = False

            # --- Guaranteed first rate-up (71–80) ---
            if not first_rate_up_obtained and pulls == FIRST_RATE_UP_PITY_END:
                first_rate_up_obtained = True
                rate_up_count += 1
                first_rate_up_pull = pulls
                six_star_counter = 0

            else:
                # --- Guaranteed 6★ between 31–40 ---
                if six_star_counter >= GUARANTEED_6_START:
                    if six_star_counter >= GUARANTEED_6_END:
                        got_six_star = True
                        six_star_counter = 0
                    elif random.random() < SIX_STAR_CHANCE:
                        got_six_star = True
                        six_star_counter = 0
                elif random.random() < SIX_STAR_CHANCE:
                    got_six_star = True
                    six_star_counter = 0

                # --- Rate-up check ---
                if got_six_star:
                    if random.random() < RATE_UP_CHANCE:
                        rate_up_count += 1
                        if not first_rate_up_obtained:
                            first_rate_up_obtained = True
                            first_rate_up_pull = pulls

            # --- Extra scheduled rate-ups ---
            for extra_pull in extra_rate_up_schedule[:]:
                if pulls == extra_pull:
                    rate_up_count += 1
                    extra_rate_up_schedule.remove(extra_pull)

            if rate_up_count >= TARGET_RATE_UPS:
                break

    return pulls, first_rate_up_pull

# --------------------
# Main simulation
# --------------------
def main():
    results = []
    first_rate_up_pulls = []

    for _ in range(EXPERIMENTS):
        total_pulls, first_pull = run_experiment()
        results.append(total_pulls)
        first_rate_up_pulls.append(first_pull)

    # ---------- Statistics ----------
    best_luck = np.min(results)
    worst_luck = np.max(results)
    avg_pulls_6 = np.mean(results)
    perc_5_6 = np.percentile(results, 5)
    perc_95_6 = np.percentile(results, 95)

    avg_first_pull = np.mean(first_rate_up_pulls)
    perc_5_first = np.percentile(first_rate_up_pulls, 5)
    perc_95_first = np.percentile(first_rate_up_pulls, 95)

    # Round 5th and 95th percentiles to nearest tens
    perc_5_6_rounded = int(np.ceil(perc_5_6 / 10) * 10)
    perc_95_6_rounded = int(np.ceil(perc_95_6 / 10) * 10)
    perc_5_first_rounded = int(np.ceil(perc_5_first / 10) * 10)
    perc_95_first_rounded = int(np.ceil(perc_95_first / 10) * 10)

    print("========== RESULTS ==========")
    print(f"Experiments run: {EXPERIMENTS}")
    print(f"Best Luck Scenario (minimum pulls): {best_luck}")
    print(f"Worst Luck Scenario (maximum pulls): {worst_luck}")
    print(f"Average pulls needed for 6 rate-ups: {avg_pulls_6:.2f}")
    print(f"5th percentile pulls (6 rate-ups): {perc_5_6_rounded}")
    print(f"95th percentile pulls (6 rate-ups): {perc_95_6_rounded}")
    print()
    print(f"Average pulls for FIRST rate-up: {avg_first_pull:.2f}")
    print(f"5th percentile first rate-up: {perc_5_first_rounded}")
    print(f"95th percentile first rate-up: {perc_95_first_rounded}")

    # ---------- Distribution plots ----------
    # 6 rate-ups
    bins = np.arange(PULLS_PER_SET, max(results)+PULLS_PER_SET, PULLS_PER_SET)
    counts, _ = np.histogram(results, bins=bins)
    bin_x = bins[:-1]
    plt.figure(figsize=(10,6))
    plt.plot(bin_x, counts, linewidth=2)
    for milestone in [180, 340, 500, 660]:
        plt.axvline(milestone, linestyle=":", linewidth=2, label=f"{milestone} pulls")
    plt.xlabel("Total Pulls")
    plt.ylabel("Frequency")
    plt.title("Total Pulls Needed for 6 Rate-Ups (Binned by 10)")
    plt.legend()
    plt.grid(True)
    plt.show()

    # First rate-up
    bins_first = np.arange(PULLS_PER_SET, max(first_rate_up_pulls)+PULLS_PER_SET*2, PULLS_PER_SET)
    counts_first, _ = np.histogram(first_rate_up_pulls, bins=bins_first)
    bin_x_first = bins_first[:-1]
    plt.figure(figsize=(10,6))
    plt.plot(bin_x_first, counts_first, linewidth=2)
    plt.axvline(80, linestyle="--", linewidth=2, label="80 Pull Cap")
    plt.xlabel("Pulls to First Rate-Up")
    plt.ylabel("Frequency")
    plt.title("Pulls Needed for First Rate-Up (Binned by 10)")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
