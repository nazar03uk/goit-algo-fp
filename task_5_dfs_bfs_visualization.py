import uuid
from collections import deque

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


def build_nx_graph(tree_root):
    """Один раз будуємо nx-граф і координати, щоб далі тільки перемальовувати кольори."""
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    labels = {node[0]: node[1]["label"] for node in tree.nodes(data=True)}
    return tree, pos, labels


def draw_step(tree, pos, labels, title):
    """Перемальовує дерево, беручи колір вузлів із атрибутів nx-графа."""
    colors = [tree.nodes[n]["color"] for n in tree.nodes()]
    plt.clf()
    plt.title(title)
    nx.draw(
        tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors
    )
    plt.axis("off")
    plt.pause(0.6)  # швидкість анімації (можеш змінити)


def hex_to_rgb(hex_color: str):
    hex_color = hex_color.lstrip("#")
    return int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)


def rgb_to_hex(rgb):
    r, g, b = rgb
    return f"#{r:02X}{g:02X}{b:02X}"


def gradient_colors(n: int, start_hex="#0B1B3A", end_hex="#A6D8FF"):
    """
    Дає n кольорів від темного до світлого (hex).
    start_hex/end_hex — можна змінювати.
    """
    if n <= 0:
        return []
    if n == 1:
        return [start_hex]

    sr, sg, sb = hex_to_rgb(start_hex)
    er, eg, eb = hex_to_rgb(end_hex)

    colors = []
    for i in range(n):
        t = i / (n - 1)
        r = round(sr + (er - sr) * t)
        g = round(sg + (eg - sg) * t)
        b = round(sb + (eb - sb) * t)
        colors.append(rgb_to_hex((r, g, b)))
    return colors


def iter_nodes_bfs(root: Node):
    """BFS: черга (FIFO). Без рекурсії."""
    q = deque([root])
    order = []
    while q:
        node = q.popleft()
        order.append(node)
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
    return order


def iter_nodes_dfs(root: Node):
    """
    DFS: стек (LIFO). Без рекурсії.
    Робимо pre-order: node -> left -> right.
    Щоб лівий обробився першим, в стек пушимо right, потім left.
    """
    stack = [root]
    order = []
    while stack:
        node = stack.pop()
        order.append(node)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return order


def visualize_traversal(tree_root: Node, mode: str):
    """
    mode: 'bfs' або 'dfs'
    Малює кроки обходу, фарбуючи вузли по порядку від темного до світлого.
    """
    tree, pos, labels = build_nx_graph(tree_root)

    # 1) беремо порядок обходу (список Node)
    if mode.lower() == "bfs":
        order = iter_nodes_bfs(tree_root)
        title_prefix = "BFS"
    elif mode.lower() == "dfs":
        order = iter_nodes_dfs(tree_root)
        title_prefix = "DFS"
    else:
        raise ValueError("mode має бути 'bfs' або 'dfs'.")

    # 2) генеруємо палітру кольорів під довжину обходу
    colors = gradient_colors(len(order), start_hex="#0B1B3A", end_hex="#A6D8FF")

    # 3) стартовий колір для всіх (не відвідані)
    for node_id in tree.nodes():
        tree.nodes[node_id]["color"] = "#D3D3D3"  # сірий (не відвідано)

    plt.figure(figsize=(10, 6))

    # 4) покроково фарбуємо вузли по порядку і перемальовуємо
    for step, (node, color) in enumerate(zip(order, colors), start=1):
        tree.nodes[node.id]["color"] = color
        draw_step(tree, pos, labels, f"{title_prefix} step {step}/{len(order)}")

    plt.show()


if __name__ == "__main__":
    # Приклад дерева (можеш взяти з 4-го завдання)
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)

    # Візуалізація BFS
    visualize_traversal(root, mode="bfs")

    # Візуалізація DFS
    visualize_traversal(root, mode="dfs")
