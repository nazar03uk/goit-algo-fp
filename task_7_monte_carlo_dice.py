import random
from collections import Counter
import matplotlib.pyplot as plt


def analytic_probabilities():
    """
    Аналітичні ймовірності для суми двох чесних кубиків.
    Кількість комбінацій = 36.
    """
    counts = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}
    probs = {s: c / 36 for s, c in counts.items()}
    return probs, counts


def monte_carlo_dice(num_rolls: int, seed: int | None = None):
    """
    Монте-Карло симуляція кидків двох кубиків.
    Повертає: лічильники сум та ймовірності.
    """
    if seed is not None:
        random.seed(seed)

    sums = Counter()
    for _ in range(num_rolls):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        sums[d1 + d2] += 1

    probs = {s: sums[s] / num_rolls for s in range(2, 13)}
    return sums, probs


def print_comparison_table(mc_counts, mc_probs, an_counts, an_probs, num_rolls: int):
    print(f"\nКількість симуляцій: {num_rolls}")
    print("Сума | MC_count | MC_prob  | Analytic_count | Analytic_prob | Abs_diff")
    print("-" * 73)
    for s in range(2, 13):
        mc_p = mc_probs[s]
        an_p = an_probs[s]
        diff = abs(mc_p - an_p)
        print(
            f"{s:>4} | {mc_counts[s]:>8} | {mc_p:>7.4f} |"
            f" {an_counts[s]:>13} | {an_p:>12.4f} | {diff:>8.4f}"
        )


def plot_probabilities(mc_probs, an_probs, num_rolls: int):
    x = list(range(2, 13))
    y_mc = [mc_probs[s] for s in x]
    y_an = [an_probs[s] for s in x]

    plt.figure(figsize=(10, 5))
    plt.plot(x, y_mc, marker="o", label=f"Monte Carlo (N={num_rolls})")
    plt.plot(x, y_an, marker="s", label="Analytic")
    plt.xticks(x)
    plt.xlabel("Сума (2..12)")
    plt.ylabel("Ймовірність")
    plt.title("Ймовірності сум при киданні двох кубиків: Монте-Карло vs Аналітика")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    num_rolls = 200_000  # можеш змінити (наприклад 10_000 / 1_000_000)
    seed = 42  # або None, якщо не потрібна відтворюваність

    an_probs, an_counts = analytic_probabilities()
    mc_counts, mc_probs = monte_carlo_dice(num_rolls=num_rolls, seed=seed)

    print_comparison_table(mc_counts, mc_probs, an_counts, an_probs, num_rolls)
    plot_probabilities(mc_probs, an_probs, num_rolls)


if __name__ == "__main__":
    main()
