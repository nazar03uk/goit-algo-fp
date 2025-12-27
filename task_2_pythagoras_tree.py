import argparse
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


def rotate(vec, angle_rad):
    """Повертає вектор (x, y) на кут angle_rad (радіани) проти год. стрілки."""
    x, y = vec
    ca, sa = math.cos(angle_rad), math.sin(angle_rad)
    return (x * ca - y * sa, x * sa + y * ca)


def add_vec(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub_vec(a, b):
    return (a[0] - b[0], a[1] - b[1])


def mul_vec(v, k):
    return (v[0] * k, v[1] * k)


def perp_ccw(v):
    """Перпендикуляр (поворот на +90°)"""
    return (-v[1], v[0])


def draw_square(ax, p, v, w, edgecolor="black", linewidth=0.6):
    """
    Малює квадрат за:
    p — нижній лівий кут,
    v — вектор сторони (вздовж основи),
    w — вектор сторони (перпендикулярний до v), така ж довжина.
    """
    a = p
    b = add_vec(p, v)
    c = add_vec(b, w)
    d = add_vec(p, w)
    poly = Polygon(
        [a, b, c, d], closed=True, fill=False, edgecolor=edgecolor, linewidth=linewidth
    )
    ax.add_patch(poly)
    return a, b, c, d


def pythagoras_tree(ax, p, v, w, depth, theta_rad):
    """
    Рекурсивне “дерево Піфагора”.
    На верхній стороні поточного квадрата будуємо два нові квадрати.
    """
    # 1) малюємо поточний квадрат
    a, b, c, d = draw_square(ax, p, v, w)

    if depth == 0:
        return

    # Верхня сторона квадрата: D -> C (ліва верхня -> права верхня)
    A = d
    B = c
    top_edge = sub_vec(B, A)  # вектор верхньої сторони
    s = math.hypot(top_edge[0], top_edge[1])  # довжина сторони (side)

    # Одиничний напрям верхнього ребра
    u = (top_edge[0] / s, top_edge[1] / s)

    # Будуємо точку C (вершина прямого трикутника), що ділить AB на дві “ноги”
    # Ліва “нога” під кутом theta до u, довжина s*cos(theta)
    AC = mul_vec(rotate(u, theta_rad), s * math.cos(theta_rad))
    C_point = add_vec(A, AC)

    # Правий вектор CB = B - C_point (автоматично буде довжини s*sin(theta))
    CB = sub_vec(B, C_point)

    # Лівий дочірній квадрат: база A -> C_point
    vL = sub_vec(C_point, A)
    wL = perp_ccw(vL)  # перпендикуляр тієї ж довжини

    # Правий дочірній квадрат: база C_point -> B
    vR = CB
    wR = perp_ccw(vR)

    # Рекурсія для двох гілок
    pythagoras_tree(ax, A, vL, wL, depth - 1, theta_rad)
    pythagoras_tree(ax, C_point, vR, wR, depth - 1, theta_rad)


def main():
    parser = argparse.ArgumentParser(description="Pythagoras Tree fractal (recursive).")
    parser.add_argument(
        "-d",
        "--depth",
        type=int,
        default=None,
        help="Рівень рекурсії (наприклад 8..12). Якщо не задано — буде запит через input().",
    )
    parser.add_argument(
        "-a",
        "--angle",
        type=float,
        default=45.0,
        help="Кут розгалуження в градусах (0..90). Типово 45.",
    )
    parser.add_argument(
        "-s",
        "--size",
        type=float,
        default=1.0,
        help="Розмір базового квадрата. Типово 1.0",
    )
    args = parser.parse_args()

    depth = args.depth
    if depth is None:
        depth = int(input("Вкажіть рівень рекурсії (наприклад 8..12): ").strip())

    angle = args.angle
    if not (0.0 < angle < 90.0):
        raise ValueError("Кут має бути в межах (0, 90).")

    theta_rad = math.radians(angle)

    # Базовий квадрат: p=(0,0), v вздовж X, w вгору (перпендикуляр)
    p0 = (0.0, 0.0)
    v0 = (args.size, 0.0)
    w0 = perp_ccw(v0)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")

    pythagoras_tree(ax, p0, v0, w0, depth, theta_rad)

    # Автомасштаб (приблизно): беремо поточні межі патчів
    ax.relim()
    ax.autoscale_view()

    plt.title(f"Pythagoras Tree | depth={depth}, angle={angle}°", fontsize=11)
    plt.show()


if __name__ == "__main__":
    main()
