import uuid
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)

        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2**layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)

        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2**layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)

    return graph


def draw_tree(tree_root: Node):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    colors = [node[1]["color"] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]["label"] for node in tree.nodes(data=True)}

    plt.figure(figsize=(10, 6))
    nx.draw(
        tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors
    )
    plt.axis("off")
    plt.show()


# -----------------------------
# ✅ Головне для Завдання 4
# -----------------------------
def heap_to_tree(heap: list[int]) -> Node | None:
    """
    Перетворює бінарну купу, задану масивом (0-indexed),
    у бінарне дерево Node.
    Для індексу i:
      left  = 2*i + 1
      right = 2*i + 2
    """
    if not heap:
        return None

    nodes = [Node(v) for v in heap]  # створюємо Node для кожного елемента

    for i in range(len(heap)):
        left_i = 2 * i + 1
        right_i = 2 * i + 2

        if left_i < len(heap):
            nodes[i].left = nodes[left_i]
        if right_i < len(heap):
            nodes[i].right = nodes[right_i]

    return nodes[0]  # корінь = heap[0]


def visualize_heap(heap: list[int]):
    """Створює дерево з купи і візуалізує його."""
    root = heap_to_tree(heap)
    if root is None:
        print("Купа порожня — нічого візуалізувати.")
        return
    draw_tree(root)


if __name__ == "__main__":
    # Приклад (можеш підставити свою купу)
    heap = [0, 4, 1, 5, 10, 3]

    # Візуалізація купи як дерева
    visualize_heap(heap)
