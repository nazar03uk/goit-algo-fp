from typing import Dict, List, Tuple


items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}


def greedy_algorithm(
    items: Dict[str, Dict[str, int]], budget: int
) -> Dict[str, object]:
    """
    Жадібний вибір за найбільшим співвідношенням calories/cost.
    Повертає: обрані страви, сумарну вартість, сумарні калорії.
    """
    sorted_items = sorted(
        items.items(),
        key=lambda kv: kv[1]["calories"] / kv[1]["cost"],
        reverse=True,
    )

    chosen: List[str] = []
    total_cost = 0
    total_calories = 0

    for name, data in sorted_items:
        c = data["cost"]
        cal = data["calories"]
        if total_cost + c <= budget:
            chosen.append(name)
            total_cost += c
            total_calories += cal

    return {
        "chosen": chosen,
        "total_cost": total_cost,
        "total_calories": total_calories,
    }


def dynamic_programming(
    items: Dict[str, Dict[str, int]], budget: int
) -> Dict[str, object]:
    """
    Динамічне програмування (0/1 knapsack):
    кожну страву можна взяти 0 або 1 раз.
    Повертає оптимальний набір страв для max калорій при обмеженні budget.
    """
    names = list(items.keys())
    costs = [items[n]["cost"] for n in names]
    calories = [items[n]["calories"] for n in names]
    n = len(names)

    # dp[i][b] = макс калорій, використовуючи перші i предметів і бюджет b
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost_i = costs[i - 1]
        cal_i = calories[i - 1]
        for b in range(budget + 1):
            dp[i][b] = dp[i - 1][b]  # не беремо i-й
            if cost_i <= b:
                dp[i][b] = max(dp[i][b], dp[i - 1][b - cost_i] + cal_i)

    # Відновлення набору
    chosen: List[str] = []
    b = budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            chosen.append(names[i - 1])
            b -= costs[i - 1]

    chosen.reverse()
    total_cost = sum(items[name]["cost"] for name in chosen)
    total_calories = sum(items[name]["calories"] for name in chosen)

    return {
        "chosen": chosen,
        "total_cost": total_cost,
        "total_calories": total_calories,
    }


if __name__ == "__main__":
    budget = 100

    g = greedy_algorithm(items, budget)
    d = dynamic_programming(items, budget)

    print("Greedy:", g)
    print("DP    :", d)
