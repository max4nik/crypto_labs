import random


# From Lab8
def miller_rabin_test(n, k):
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    def is_composite(a):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return False
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                return False
        return True

    for _ in range(k):
        a = random.randint(2, n - 2)
        if is_composite(a):
            return False, 0

    return True, 1 - 1 / (4 ** k)


def generate_prime_candidate(length):
    p = random.randint(2 ** (length - 1), 2 ** length - 1)
    return p | 1  # ensure it is odd


def generate_large_prime(length=1024):
    p = generate_prime_candidate(length)
    while not miller_rabin_test(p, 5)[0]:
        p = generate_prime_candidate(length)
    return p


def find_primitive_root(p):
    """ Вибрір g рандомно за умови, що воно є первісним коренем за модулем p"""
    if p == 2:
        return 1
    p1 = 2
    p2 = (p - 1) // p1

    while True:
        g = random.randint(2, p - 1)
        if not (pow(g, (p - 1) // p1, p) == 1):
            if not (pow(g, (p - 1) // p2, p) == 1):
                return g


if __name__ == '__main__':
    p = generate_large_prime(128)
    print(f"p: {p}")

    g = find_primitive_root(p)
    print("g (первісний корінь за модулем p, вибраний рандомно в проміжку {2, p-1}):", g)

    alice_private_key = 10
    bob_private_key = 11

    alice_public_key = pow(g, alice_private_key, p)
    bob_public_key = pow(g, bob_private_key, p)
    print(f"Публічний ключ Аліси: {alice_public_key}")
    print(f"Публічний ключ Боба: {bob_public_key}")

    # Calculating shared secret for both Alice and Bob
    alice_shared_secret = pow(bob_public_key, alice_private_key, p)
    bob_shared_secret = pow(alice_public_key, bob_private_key, p)
    print(f"Спільний секретний ключ Аліси: {alice_shared_secret}")
    print(f"Спільний секретний ключ Боба: {bob_shared_secret}")

    # Ensuring both secrets are equal
    assertion = alice_shared_secret == bob_shared_secret
    print(f"Ключі однакові: {assertion}")
