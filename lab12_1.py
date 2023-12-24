def find_points_on_curve(a, b, p):
    points = []
    for x in range(p):
        for y in range(p):
            if (y * y) % p == (x * x * x + a * x + b) % p:
                points.append((x, y))
    return points


def find_order_of_point(a, b, p, G):
    def _point_addition(point1, point2):
        if point1 is None:
            return point2
        if point2 is None:
            return point1

        x1, y1 = point1
        x2, y2 = point2

        if x1 == x2 and y1 != y2:
            return None

        if x1 == x2:
            m = (3 * x1 * x1 + a) * _inverse_mod(2 * y1, p)
        else:
            m = (y1 - y2) * _inverse_mod(x1 - x2, p)

        x3 = m * m - x1 - x2
        y3 = y1 + m * (x3 - x1)
        return (x3 % p, -y3 % p)

    def _inverse_mod(k, mod):
        if k == 0:
            raise ZeroDivisionError('division by zero')

        if k < 0:
            return mod - _inverse_mod(-k, mod)

        s, old_s = 0, 1
        t, old_t = 1, 0
        r, old_r = mod, k

        while r != 0:
            quotient = old_r // r
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
            old_t, t = t, old_t - quotient * t

        return old_s % mod

    n = 1
    current_point = G
    while current_point is not None:
        n += 1
        current_point = _point_addition(current_point, G)

    return n


if __name__ == '__main__':
    a = 1
    b = 1
    p = 23

    points_on_curve = find_points_on_curve(a, b, p)
    print(f"1. Точки на кривій з параметрами a={a} b={b} P={p}:")
    print(points_on_curve, '\n')

    G = (17, 20)

    order_of_G = find_order_of_point(a, b, p, G)
    print(f"2.Порядок n точки G = {G} на еліптичній кривій дорівнює {order_of_G}.")
