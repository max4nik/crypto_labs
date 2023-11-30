from random import randint

from lab8 import generate_large_prime, find_primitive_root

# From lab 4
def gcdex(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


def inverse_element(a, n):
    d, x, y = gcdex(a, n)
    if d != 1:
        return None  # обернений елемент не існує
    else:
        x = x % n  # x має бути в межах [0, n-1]
        return x


def elgamal_key_generation():
    n = generate_large_prime(1024)
    g = find_primitive_root(n)
    a = randint(1, n - 1)
    h = pow(g, a, n)
    public_key = (n, g, h)
    private_key = (n, a)
    return public_key, private_key


def elgamal_encrypt(public_key, m):
    n, g, h = public_key
    r = randint(1, n - 1)
    c1 = pow(g, r, n)
    c2 = (m * pow(h, r, n)) % n
    return c1, c2


def elgamal_decrypt(private_key, ciphertext):
    n, a = private_key
    c1, c2 = ciphertext
    s = pow(c1, a, n)
    m = (c2 * inverse_element(s, n)) % n
    return m

if __name__ == '__main__':
    public_key, private_key = elgamal_key_generation()
    print("Публічний ключ:", public_key)
    print("Приватний ключ:", private_key)

    test_message = randint(1, public_key[0] - 1)
    print("Тестове повідомлення:", test_message)

    encrypted_message = elgamal_encrypt(public_key, test_message)
    print("Зашифроване повідомлення:", encrypted_message)

    decrypted_message = elgamal_decrypt(private_key, encrypted_message)
    print("Розшифроване повідомлення:", decrypted_message)

    print("Розшифроване повідомлення відповідає оригіналу:", test_message == decrypted_message)
