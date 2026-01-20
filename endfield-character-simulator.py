import random
import statistics
import numpy as np
import matplotlib.pyplot as plt

# --------------------
# Base rates and constants
# --------------------
BASE_SIX_STAR_RATE = 0.008
PITY_START = 66
PITY_INCREMENT = 0.05
MAX_PITY = 80

GUARANTEE_120 = 120
RATE_UP_240 = 240

BASE_FIVE_STAR_RATE = 0.08
BASE_FOUR_STAR_RATE = 0.912

# --------------------
# ARSENAL TICKETS
# --------------------
TICKETS_SIX_STAR = 2000
TICKETS_FIVE_STAR = 200
TICKETS_FOUR_STAR = 20

# --------------------
# Simulation parameters
# --------------------
TARGET_RATE_UPS = 6
EXPERIMENTS = 10000

# --------------------
# 6★ chance function with pity
# --------------------
def six_star_chance(pity):
    if pity < PITY_START:
        return BASE_SIX_STAR_RATE
    return min(1.0, BASE_SIX_STAR_RATE + (pity - 65) * PITY_INCREMENT)

# --------------------
# Run a single experiment
# --------------------
def run_experiment():
    pulls = 0
    six_star_pity = 0
    five_star_pity = 0
    rate_up_count = 0
    tickets_total = 0

    first_rate_up_pull = None
    tickets_at_first_rate_up = None
    off_banner_before_first = 0
    hit_120_guarantee = False

    while rate_up_count < TARGET_RATE_UPS:
        pulls += 1
        if pulls == 120:
            tickets_at_120 = tickets_total
        six_star_pity += 1
        five_star_pity += 1

        current_six_star_rate = six_star_chance(six_star_pity)
        remaining_rate = 1.0 - current_six_star_rate
        current_five_star_rate = BASE_FIVE_STAR_RATE * remaining_rate

        guaranteed_5_star = five_star_pity == 10
        roll = random.random()

        # --- Hard pity ---
        if six_star_pity >= MAX_PITY:
            six_star_pity = 0
            five_star_pity = 0
            tickets_total += TICKETS_SIX_STAR
            if random.random() < 0.5:
                rate_up_count += 1
                if first_rate_up_pull is None:
                    first_rate_up_pull = pulls
                    tickets_at_first_rate_up = tickets_total
            else:
                if first_rate_up_pull is None:
                    off_banner_before_first += 1
            continue

        # --- 240 guaranteed ---
        if pulls % RATE_UP_240 == 0:
            rate_up_count += 1
            tickets_total += 0 # NO TICKETS GAINED FOR POTENTIAL TOKEN
            six_star_pity = 0
            five_star_pity = 0
            if first_rate_up_pull is None:
                first_rate_up_pull = pulls
                tickets_at_first_rate_up = tickets_total
            continue

        # --- 120 guaranteed first ---
        if pulls >= GUARANTEE_120 and rate_up_count == 0:
            rate_up_count += 1
            tickets_total += TICKETS_SIX_STAR
            six_star_pity = 0
            five_star_pity = 0
            first_rate_up_pull = pulls
            tickets_at_first_rate_up = tickets_total
            hit_120_guarantee = True
            continue

        # --- Normal roll ---
        if roll < current_six_star_rate:
            six_star_pity = 0
            five_star_pity = 0
            tickets_total += TICKETS_SIX_STAR
            if random.random() < 0.5:
                rate_up_count += 1
                if first_rate_up_pull is None:
                    first_rate_up_pull = pulls
                    tickets_at_first_rate_up = tickets_total
            else:
                if first_rate_up_pull is None:
                    off_banner_before_first += 1

        elif roll < current_six_star_rate + current_five_star_rate or guaranteed_5_star:
            five_star_pity = 0
            tickets_total += TICKETS_FIVE_STAR
        else:
            tickets_total += TICKETS_FOUR_STAR

    return pulls, tickets_total, first_rate_up_pull, tickets_at_first_rate_up, off_banner_before_first, hit_120_guarantee, tickets_at_120

# --------------------
# Main simulation
# --------------------
def main():
    pulls_list = []
    tickets_list = []
    first_rate_up_pulls = []
    first_rate_up_tickets = []
    off_banner_counts = []
    count_120_guarantee = 0
    tickets_at_120_guarantee = []

    for _ in range(EXPERIMENTS):
        p, t, fr, fr_t, off, g120, t120 = run_experiment()
        pulls_list.append(p)
        tickets_list.append(t)
        first_rate_up_pulls.append(fr)
        first_rate_up_tickets.append(fr_t)
        off_banner_counts.append(off)
        if g120:
            count_120_guarantee += 1
            tickets_at_120_guarantee.append(t120)

    # --------------------
    # Core statistics
    # --------------------
    best = min(pulls_list)
    worst = max(pulls_list)
    avg = sum(pulls_list) / len(pulls_list)
    median_pulls = statistics.median(pulls_list)
    p5 = int(np.percentile(pulls_list, 5))
    p95 = int(np.percentile(pulls_list, 95))

    median_pulls_int = int(median_pulls)
    tickets_at_median_6_rateups = [
        tickets
        for pull, tickets in zip(pulls_list, tickets_list)
        if pull == median_pulls_int
    ]
    median_6_rateup_tickets = sum(tickets_at_median_6_rateups) / len(tickets_at_median_6_rateups)

    avg_first_rate_up = sum(first_rate_up_pulls) / len(first_rate_up_pulls)
    at_most_80_first_rate_up = sum(
        1 for x in first_rate_up_pulls if x <= 80
    )

    median_first_rate_up_pulls = int(statistics.median(first_rate_up_pulls))
    tickets_at_median_first_rate_up = [
        tickets
        for pull, tickets in zip(first_rate_up_pulls, first_rate_up_tickets)
        if pull == median_first_rate_up_pulls
    ]
    median_first_rate_up_tickets = sum(tickets_at_median_first_rate_up) / len(tickets_at_median_first_rate_up)

    avg_tickets_120 = (
        sum(tickets_at_120_guarantee) / len(tickets_at_120_guarantee)
        if tickets_at_120_guarantee else 0
    )

    # Off-banner stats
    first_hit = sum(1 for x in off_banner_counts if x == 0)
    one = sum(1 for x in off_banner_counts if x == 1)
    two = sum(1 for x in off_banner_counts if x == 2)
    three_plus = sum(1 for x in off_banner_counts if x >= 3)

    # --------------------
    # Print results
    # --------------------
    print("========== RESULTS ==========")
    print(f"Best Luck Scenario (minimum pulls): {best}")
    print(f"Worst Luck Scenario (maximum pulls): {worst}")
    print(f"Average pulls needed for 6 rate-ups: {avg:.2f}")
    print(f"Median pulls for 6 rate-ups: {median_pulls}")
    print(f"5th percentile pulls: {p5}")
    print(f"95th percentile pulls: {p95}")
    print(f"Arsenal tickets at median pulls for 6 rate-ups: {median_6_rateup_tickets}")
    print(f"Number of weapon rolls possible at median: {median_6_rateup_tickets/1980*10:.2f}")

    print(f"\nAverage pulls for FIRST rate-up: {avg_first_rate_up:.2f}")
    print(f"Median pulls for FIRST rate-up: {median_first_rate_up_pulls}")
    print(f"Arsenal tickets for median FIRST rate-up: {median_first_rate_up_tickets}")
    print(f"Number of weapon rolls possible at median: {median_first_rate_up_tickets/1980*10:.2f}")
    print(f"Number of experiments hitting 120-pull guarantee: {count_120_guarantee}")
    print(f"Average arsenal tickets when hitting 120-pull guarantee: {avg_tickets_120:.2f}")
    print(f"Number of weapon rolls possible at average (120 guarantee): {avg_tickets_120/1980*10:.2f}")
    print(f"Number of experiments using at most 80 pulls to get at least one rate-up: {at_most_80_first_rate_up}")

    print("\nOff-banner statistics before first rate-up:")
    print(f"  First rate-up on first 6★: {first_hit}")
    print(f"  1 off-banner before first rate-up: {one}")
    print(f"  2 off-banners before first rate-up: {two}")
    print(f"  3 or more off-banners before first rate-up: {three_plus}")

    # --------------------
    # SMOOTH LINE GRAPHS (per integer)
    # --------------------
    counts = np.bincount(pulls_list)
    x = np.arange(len(counts))

    plt.figure(figsize=(10,6))
    plt.plot(x, counts, label="Frequency")

    # --- Dotted milestone lines ---
    for milestone in [240, 480, 720]:
        plt.axvline(
            milestone,
            linestyle=":",
            linewidth=2,
            label=f"{milestone} pulls"
        )

    plt.xlabel("Total Pulls")
    plt.ylabel("Frequency")
    plt.title("Distribution of Total Pulls Needed for 6 Rate-Ups (Per Pull)")
    plt.legend()
    plt.grid(True)
    plt.show()


    counts = np.bincount(first_rate_up_pulls)
    x = np.arange(len(counts))

    plt.figure(figsize=(10,6))
    plt.plot(x, counts)
    plt.axvline(120, linestyle='--', label='120 Guarantee')
    plt.xlabel("Pulls")
    plt.ylabel("Frequency")
    plt.title("Distribution of Pulls Needed for First Featured Unit")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
