import random
import numpy as np
import matplotlib.pyplot as plt

# --------------------
# Constants
# --------------------
BASE_RATE = 0.02          # 2%
SOFT_PITY_START = 50      # soft pity starts after 50
SOFT_PITY_INCREMENT = 0.02  # +2% per pull after 50
GUARANTEED_FIRST_RATE_UP = 150  # First guaranteed rate-up
TARGET_RATE_UPS = 6       # max potential
EXPERIMENTS = 10000

# --------------------
# Run a single experiment
# --------------------
def run_experiment():
    pulls = 0
    rate_up_count = 0
    first_rate_up_pull = None
    pulls_since_last_6_star = 0
    guarantee_first_rate_up = True  # 150-pull protection available

    while rate_up_count < TARGET_RATE_UPS:
        pulls += 1
        pulls_since_last_6_star += 1

        # Calculate 6★ chance with soft pity
        if pulls_since_last_6_star <= SOFT_PITY_START:
            six_star_chance = BASE_RATE
        else:
            six_star_chance = BASE_RATE + (pulls_since_last_6_star - SOFT_PITY_START) * SOFT_PITY_INCREMENT
            six_star_chance = min(six_star_chance, 1.0)

        # Roll for 6★
        if random.random() < six_star_chance:
            pulls_since_last_6_star = 0  # reset soft pity counter

            # Determine if this is a rate-up
            if guarantee_first_rate_up and pulls >= GUARANTEED_FIRST_RATE_UP:
                is_rate_up = True
                guarantee_first_rate_up = False  # consume guarantee
            else:
                is_rate_up = random.random() < 0.5  # 50/50 chance

            if is_rate_up:
                rate_up_count += 1
                if first_rate_up_pull is None:
                    first_rate_up_pull = pulls
            # Off-banner 6★s do not count toward TARGET_RATE_UPS

    return pulls, first_rate_up_pull

# --------------------
# Main simulation
# --------------------
def main():
    total_pulls_list = []
    first_rate_up_pulls = []

    for _ in range(EXPERIMENTS):
        pulls_needed, first_pull = run_experiment()
        total_pulls_list.append(pulls_needed)
        first_rate_up_pulls.append(first_pull)

    # --------------------
    # Stats
    # --------------------
    print("========== RESULTS ==========")
    print(f"Experiments run: {EXPERIMENTS}")
    print(f"Minimum pulls to max potential: {min(total_pulls_list)}")
    print(f"Maximum pulls to max potential: {max(total_pulls_list)}")
    print(f"Average pulls to max potential: {np.mean(total_pulls_list):.2f}")
    print(f"5th percentile pulls: {np.percentile(total_pulls_list,5):.0f}")
    print(f"95th percentile pulls: {np.percentile(total_pulls_list,95):.0f}")
    print()
    print(f"Average pulls to first on-rate: {np.mean(first_rate_up_pulls):.2f}")
    print(f"5th percentile first rate-up: {np.percentile(first_rate_up_pulls,5):.0f}")
    print(f"95th percentile first rate-up: {np.percentile(first_rate_up_pulls,95):.0f}")

    # --------------------
    # Smooth integer-based line: total pulls
    # --------------------
    counts_total = np.bincount(total_pulls_list)
    x_total = np.arange(len(counts_total))
    plt.figure(figsize=(10,6))
    plt.plot(x_total, counts_total, linewidth=2)
    plt.xlabel("Total Pulls")
    plt.ylabel("Frequency")
    plt.title("Pulls Needed for 6 Rate-Ups (Max Potential)")
    plt.grid(True)
    plt.show()

    # --------------------
    # Smooth integer-based line: first rate-up
    # --------------------
    counts_first = np.bincount(first_rate_up_pulls)
    x_first = np.arange(len(counts_first))
    plt.figure(figsize=(10,6))
    plt.plot(x_first, counts_first, linewidth=2, color='orange')
    plt.axvline(GUARANTEED_FIRST_RATE_UP, linestyle="--", color="red", label="Guaranteed Rate-Up at 150")
    plt.xlabel("Pulls to First Rate-Up")
    plt.ylabel("Frequency")
    plt.title("Pulls Needed for First Rate-Up (Max Potential)")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
