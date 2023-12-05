import math


class MD5:
    def __init__(self):
        self._INITIAL_VALUES = [int(abs(math.sin(i + 1)) * 2 ** 32) & 0xFFFFFFFF for i in range(64)]

        self._INDICES = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            [1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12],
            [5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2],
            [0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9]
        ]

        self._SHIFTS = [[7, 12, 17, 22] * 4, [5, 9, 14, 20] * 4, [4, 11, 16, 23] * 4, [6, 10, 15, 21] * 4]

        self._ROUND_FUNCTIONS = [
            lambda x, y, d: (x & y) | (~x & d),
            lambda x, y, d: (x & d) | (y & ~d),
            lambda x, y, d: x ^ y ^ d,
            lambda x, y, d: y ^ (x | ~d),
        ]

    def _left_circular_shift(self, x, bits):
        return (x % 2 ** 32 << bits % 32) % 2 ** 32 | (x % 2 ** 32 >> (32 - bits % 32))

    def _block_divide(self, block, chunks):
        size = len(block) // chunks
        return [int.from_bytes(block[i * size:(i + 1) * size], byteorder="little") for i in range(chunks)]

    def _round_function(self, func, a, b, c, d, block_part, shifts, values):
        return b + self._left_circular_shift(a + func(b, c, d) + block_part + values, shifts)

    def _process_round(self, a, b, c, d, block_part, round_num):
        for i in range(16):
            indices = self._INDICES[round_num]
            shifts = self._SHIFTS[round_num]

            values = self._INITIAL_VALUES[round_num * 16:round_num * 16 + 16]

            a = self._round_function(
                func=self._ROUND_FUNCTIONS[round_num],
                a=a,
                b=b,
                c=c,
                d=d,
                block_part=block_part[indices[i]],
                shifts=shifts[i],
                values=values[i]
            )
            a, b, c, d = d, a, b, c
        return a, b, c, d

    def get_hash(self, plaintext):
        len_text = len(plaintext) * 8 % 2 ** 64
        plaintext += b'\x80'
        zero_bytes_to_add = (448 - (len_text + 8) % 512) % 512 // 8
        plaintext += b'\x00' * zero_bytes_to_add + len_text.to_bytes(8, byteorder='little')

        len_text = len(plaintext) * 8
        iterations = len_text // 512

        h0, h1, h2, h3 = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476

        for i in range(iterations):
            a, b, c, d = h0, h1, h2, h3
            block = plaintext[i * 64:(i + 1) * 64]
            block_part = self._block_divide(block, 16)

            for i in range(4):
                a, b, c, d = self._process_round(a, b, c, d, block_part, i)

            h0, h1, h2, h3 = (h0 + a) % 2 ** 32, (h1 + b) % 2 ** 32, (h2 + c) % 2 ** 32, (h3 + d) % 2 ** 32

        return ''.join([i.to_bytes(4, byteorder='little').hex() for i in [h0, h1, h2, h3]])


# Тестування створеної функції хешування md5
plaintext = "md5TestString123"
print("Оригінальний текст:", plaintext)
md5 = MD5()
md5_result_hash = md5.get_hash(plaintext.encode())
print("Результат хешування:", md5_result_hash)

# Тестування з результатом виконання функції з бібліотеки hashlib
import hashlib

hashlib_md5_result_hash = hashlib.md5(plaintext.encode()).hexdigest()
print("Результат хешування з використанням бібліотеки hashlib:", hashlib_md5_result_hash)

# Перевірка однаковості результатів
results_same = md5_result_hash == hashlib_md5_result_hash
assert results_same
print("Результати однакові:", results_same)
