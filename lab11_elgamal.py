import random
from lab8 import generate_large_prime, find_primitive_root


def gcd(x, y):
    while y:
        x, y = y, x % y
    return abs(x)


def generate_keys(p, g):
    x = random.randrange(1, p - 1)  # Private key
    y = pow(g, x, p)  # Public key
    return x, y


def modular_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1


def elgamal_sign(p, g, x, message):
    while True:
        k = random.randrange(1, p - 1)
        if gcd(k, p - 1) == 1:
            break

    r = pow(g, k, p)
    k_inv = modular_inverse(k, p - 1)
    s = (k_inv * (message - x * r)) % (p - 1)
    return r, s


def elgamal_verify(p, g, y, message, signature):
    r, s = signature
    if not (0 < r < p and 0 < s < p - 1):
        return False
    v1 = pow(y, r, p) * pow(r, s, p) % p
    v2 = pow(g, message, p)
    return v1 == v2


keysize = 1024
p = generate_large_prime(keysize)
g = find_primitive_root(p)

print("Просте число (p):", p)
print("Генератор (g):", g)

private_key, public_key = generate_keys(p, g)

print("Приватний ключ:", private_key)
print("Публічний ключ:", public_key)

message = 123456789
signature = elgamal_sign(p, g, private_key, message)

print("Підписане повідомлення:", message)
print("Цифровий підпис (r, s):", signature)

verification = elgamal_verify(p, g, public_key, message, signature)
print("Перевірка підпису:", "Успішна" if verification else "Невдала")
