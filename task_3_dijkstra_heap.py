from __future__ import annotations

import heapq
from typing import Dict, List, Tuple, Any


Graph = Dict[Any, List[Tuple[Any, float]]]


def dijkstra(
    graph: Graph, start: Any
) -> tuple[dict[Any, float], dict[Any, Any | None]]:
    """
    Алгоритм Дейкстри з бінарною купою (heapq).
    Повертає:
      dist[v]  - найкоротша відстань від start до v
      prev[v]  - попередник v в найкоротшому шляху (для відновлення маршруту)
    """
    dist: Dict[Any, float] = {v: float("inf") for v in graph}
    prev: Dict[Any, Any | None] = {v: None for v in graph}

    dist[start] = 0.0
    heap: List[Tuple[float, Any]] = [(0.0, start)]  # (distance, vertex)

    while heap:
        cur_dist, u = heapq.heappop(heap)

        # Якщо це "застарілий" запис у купі — пропускаємо
        if cur_dist != dist[u]:
            continue

        for v, w in graph[u]:
            if w < 0:
                raise ValueError("Дейкстра не працює з від’ємними вагами ребер.")
            new_dist = cur_dist + w
            if new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(heap, (new_dist, v))

    return dist, prev


def reconstruct_path(prev: dict[Any, Any | None], start: Any, target: Any) -> list[Any]:
    """Відновлює шлях start -> target за словником prev."""
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()

    if not path or path[0] != start:
        return []  # недосяжно
    return path


def build_sample_graph() -> Graph:
    """
    Створюємо приклад зваженого графа (неорієнтований).
    Формат: graph[u] = [(v, weight), ...]
    """
    graph: Graph = {
        "A": [("B", 4), ("C", 2)],
        "B": [("A", 4), ("C", 1), ("D", 5)],
        "C": [("A", 2), ("B", 1), ("D", 8), ("E", 10)],
        "D": [("B", 5), ("C", 8), ("E", 2), ("F", 6)],
        "E": [("C", 10), ("D", 2), ("F", 3)],
        "F": [("D", 6), ("E", 3)],
    }
    return graph


if __name__ == "__main__":
    graph = build_sample_graph()
    start_vertex = "A"

    dist, prev = dijkstra(graph, start_vertex)

    print(f"Стартова вершина: {start_vertex}\n")
    print("Найкоротші відстані (dist):")
    for v in sorted(dist.keys()):
        print(f"  {start_vertex} -> {v}: {dist[v]}")

    print("\nШляхи (відновлення через prev):")
    for v in sorted(dist.keys()):
        path = reconstruct_path(prev, start_vertex, v)
        if not path:
            print(f"  {start_vertex} -> {v}: недосяжно")
        else:
            print(f"  {start_vertex} -> {v}: {' -> '.join(path)} (dist={dist[v]})")
