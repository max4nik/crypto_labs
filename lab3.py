def gcdex(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


print('1.')
a = 612
b = 342
print(f'Результат роботи ітераційного розширеного алгоритму Евкліда пошуку трійки для a = {a}, b = {b}')
d, x, y = gcdex(a, b)
print(f'gcd({a}, {b}) = {d}')
print(f'{a} * {x} + {b} * {y} = {d}')


def inverse_element(a, n):
    d, x, y = gcdex(a, n)
    if d != 1:
        return None  # обернений елемент не існує
    else:
        x = x % n  # x має бути в межах [0, n-1]
        return x


print('\n2.')
a = 5
n = 18
inverse = inverse_element(a, n)
if inverse is not None:
    print(f"Обернений елемент {a} по модулю {n} дорівнює {inverse}")
else:
    print(f"Не існує оберненого елементу {a} по модулю {n}")


def phi(m):
    if m == 1:
        return 1
    result = m
    p = 2
    while p * p <= m:
        if m % p == 0:
            while m % p == 0:
                m //= p
            result -= result // p
        p += 1

    if m > 1:
        result -= result // m

    return result


print('\n3.')
m = 12
result = phi(m)
print(f'Функція Ейлера φ({m}) = {result}')


def inverse_element_2(a, n):
    def mod_pow(base, exp, mod):
        result = 1
        base = base % mod
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            exp = exp // 2
            base = (base * base) % mod
        return result

    if n == 1:
        return None  # Обернений елемент не існує

    if n > 1:
        if gcdex(a, n)[0] != 1:
            return None  # Обернений елемент не існує

        # Використовуємо теорему Ейлера
        return mod_pow(a, phi(n) - 1, n)
    else:
        return None


print('\n4.')
a = 5
n = 18
inverse = inverse_element_2(a, n)
if inverse is not None:
    print(f"Обернений елемент {a} по модулю {n} дорівнює {inverse}")
else:
    print(f"Не існує оберненого елементу {a} по модулю {n}")
