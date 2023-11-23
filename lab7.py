import random


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


print('1. Тест простоти Міллера — Рабіна')

random_ints = [12528, 19571, 50583, 85303, 1429]
k = 5
for n in random_ints:
    result = miller_rabin_test(n, k)
    print(f'Тест простоти Міллера — Рабіна для числа {n}. Результат: {result[0]}, вірогідність = {result[1]}')
print()
print()


def generate_large_prime(bits=512, k=5):
    while True:
        n = random.getrandbits(bits)
        n |= (1 << bits - 1) | 1

        if miller_rabin_test(n, k)[1] > 0.99:
            return n


# Перевикористано з лаб. 4
def gcdex(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


def generate_rsa_keys(bits):
    p = generate_large_prime(bits)
    q = generate_large_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)

    # Вибираємо e
    e = 65537

    gcd, x, y = gcdex(e, phi)
    d = x % phi

    return (e, n), (d, n)


def rsa_encrypt(message, pub_key):
    e, n = pub_key
    cipher = [pow(ord(char), e, n) for char in message]
    return cipher


def rsa_decrypt(cipher, priv_key):
    d, n = priv_key
    plain = ''.join([chr(pow(char, d, n)) for char in cipher])
    return plain


print('2. Навчальна криптографічна система з відкритим ключем RSA')
public_key, private_key = generate_rsa_keys(512)
print('Відкритий ключ:', public_key)
print('Закритий ключ:', private_key)

plaintext = "SECRET"
print('Оригінальний текст:', plaintext)
encrypted_text = rsa_encrypt(plaintext, public_key)
print('Зашифроване повідомлення:', encrypted_text)
decrypted_text = rsa_decrypt(encrypted_text, private_key)
print('Розшифроване повідомлення:', decrypted_text)
