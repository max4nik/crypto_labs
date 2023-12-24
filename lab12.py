import random


class ECElGamal:
    def __init__(self, a, b, p, G):
        self.a = a
        self.b = b
        self.p = p
        self.G = G

    def _inverse_mod(self, k, mod):
        if k == 0:
            raise ZeroDivisionError('division by zero')

        if k < 0:
            return mod - self._inverse_mod(-k, mod)

        s, old_s = 0, 1
        t, old_t = 1, 0
        r, old_r = mod, k

        while r != 0:
            quotient = old_r // r
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
            old_t, t = t, old_t - quotient * t

        return old_s % mod

    def _point_addition(self, point1, point2):
        if point1 is None:
            return point2
        if point2 is None:
            return point1

        x1, y1 = point1
        x2, y2 = point2

        if x1 == x2 and y1 != y2:
            return None

        if x1 == x2:
            m = (3 * x1 * x1 + self.a) * self._inverse_mod(2 * y1, self.p)
        else:
            m = (y1 - y2) * self._inverse_mod(x1 - x2, self.p)

        x3 = m * m - x1 - x2
        y3 = y1 + m * (x3 - x1)
        return x3 % self.p, -y3 % self.p

    def _scalar_multiplication(self, k, point):
        result = None
        addend = point

        while k:
            if k & 1:
                result = self._point_addition(result, addend)

            addend = self._point_addition(addend, addend)
            k >>= 1

        return result

    def generate_keys(self, defined_private_key=None):
        private_key = defined_private_key or random.randrange(1, self.p)
        public_key = self._scalar_multiplication(private_key, self.G)
        return private_key, public_key

    def encrypt(self, public_key, message_point, defined_k=None):
        k = defined_k or random.randrange(1, self.p)
        c1 = self._scalar_multiplication(k, self.G)
        c2 = self._point_addition(message_point, self._scalar_multiplication(k, public_key))
        return c1, c2

    def decrypt(self, private_key, ciphertext):
        c1, c2 = ciphertext
        s = self._scalar_multiplication(private_key, c1)
        s_inverse = (s[0], -s[1] % self.p)
        return self._point_addition(c2, s_inverse)


if __name__ == '__main__':
    p = 23
    a = 1
    b = 1
    G = (17, 20)
    message_point = (12, 19)
    # Test settings
    is_test = False
    test_keys_kwargs = {"defined_private_key": 3} if is_test else {}
    test_encrypt_kwargs = {"defined_k": 2} if is_test else {}
    if is_test:
        p = 127
        a = -1
        b = 3
        G = (77, 104)
        message_point = (73, 94)

    ec_elgamal = ECElGamal(a, b, p, G)

    private_key, public_key = ec_elgamal.generate_keys(**test_keys_kwargs)

    encrypted_message = ec_elgamal.encrypt(public_key, message_point, **test_encrypt_kwargs)

    decrypted_message = ec_elgamal.decrypt(private_key, encrypted_message)

    if is_test:
        print("Тестування з використанням параметрів з контрольної №2, Варіант 20\n")
    print("Оригінальне повідомлення:", message_point)
    print("Приватний ключ:", private_key)
    print("Відкритий ключ:", public_key)
    print("Зашифроване повідомлення:", encrypted_message)
    print("Розшифроване повідомлення:", decrypted_message)
