class DES:
    def __init__(
            self,
            initial_permutation,
            final_permutation,
            expansion_d_box,
            straight_permutation,
            s_box,
            key_permutation,
            key_comp_permutation,
            shift_table
    ):
        self.initial_permutation = initial_permutation
        self.final_permutation = final_permutation
        self.expansion_d_box = expansion_d_box
        self.straight_permutation = straight_permutation
        self.s_box = s_box
        self.key_permutation = key_permutation
        self.key_comp_permutation = key_comp_permutation
        self.shift_table = shift_table

    def permute(self, k, arr, n):
        permutation = ""
        for i in range(0, n):
            permutation += k[arr[i] - 1]
        return permutation

    def shift_left(self, k, nth_shifts):
        s = ""
        for i in range(nth_shifts):
            for j in range(1, len(k)):
                s += k[j]
            s += k[0]
            k = s
            s = ""
        return k

    def xor(self, a, b):
        ans = ""
        for i in range(len(a)):
            if a[i] == b[i]:
                ans += "0"
            else:
                ans += "1"
        return ans

    def encrypt(self, pt, rkb):
        pt = self.permute(pt, self.initial_permutation, 64)
        left = pt[0:32]
        right = pt[32:64]
        for i in range(0, 16):
            right_expanded = self.permute(right, self.expansion_d_box, 48)

            xor_x = self.xor(right_expanded, rkb[i])

            sbox_str = ""
            for j in range(0, 8):
                row = bin(2 * int(xor_x[j * 6], 2) + int(xor_x[j * 6 + 5], 2))[2:].zfill(2)
                col = bin(int(xor_x[j * 6 + 1:j * 6 + 5], 2))[2:].zfill(4)
                val = self.s_box[j][int(row, 2)][int(col, 2)]
                sbox_str += bin(val)[2:].zfill(4)

            sbox_str = self.permute(sbox_str, self.straight_permutation, 32)

            result = self.xor(left, sbox_str)
            left = result

            if i != 15:
                left, right = right, left

        combine = left + right

        cipher_text = self.permute(combine, self.final_permutation, 64)
        return cipher_text

    def decrypt(self, ct, rkb):
        ct = self.permute(ct, self.initial_permutation, 64)
        left = ct[0:32]
        right = ct[32:64]
        for i in range(15, -1, -1):
            right_expanded = self.permute(right, self.expansion_d_box, 48)

            xor_x = self.xor(right_expanded, rkb[i])

            sbox_str = ""
            for j in range(0, 8):
                row = bin(2 * int(xor_x[j * 6], 2) + int(xor_x[j * 6 + 5], 2))[2:].zfill(2)
                col = bin(int(xor_x[j * 6 + 1:j * 6 + 5], 2))[2:].zfill(4)
                val = self.s_box[j][int(row, 2)][int(col, 2)]
                sbox_str += bin(val)[2:].zfill(4)

            sbox_str = self.permute(sbox_str, self.straight_permutation, 32)

            result = self.xor(left, sbox_str)
            left = result

            if i != 0:
                left, right = right, left

        combine = left + right

        plain_text = self.permute(combine, self.final_permutation, 64)
        return plain_text

    def get_round_key(self, key):
        key = self.permute(key, self.key_permutation, 56)
        left = key[0:28]
        right = key[28:56]
        rkb = []
        for i in range(0, 16):
            left = self.shift_left(left, self.shift_table[i])
            right = self.shift_left(right, self.shift_table[i])
            combine_str = left + right
            round_key = self.permute(combine_str, self.key_comp_permutation, 48)
            rkb.append(round_key)
        return rkb


# Initial permutation table
initial_permutation = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Final permutation table
final_permutation = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

# Expansion D-box table
expansion_d_box = [
    32, 1, 2, 3, 4, 5, 4, 5,
    6, 7, 8, 9, 8, 9, 10, 11,
    12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21,
    22, 23, 24, 25, 24, 25, 26, 27,
    28, 29, 28, 29, 30, 31, 32, 1
]

# Straight permutation table
straight_permutation = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]

# S-Box
s_box = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],

    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],

    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],

    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],

    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],

    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],

    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],

    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

key_permutation = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

# Key compression table
key_comp_permutation = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

# Shift table
shift_table = [
    1, 1, 2, 2,
    2, 2, 2, 2,
    1, 2, 2, 2,
    2, 2, 2, 1
]


def ascii_to_bin(ascii_string):
    return ''.join(format(ord(char), '08b') for char in ascii_string)


def bin_to_ascii(bin_string):
    ascii_text = ""
    for i in range(0, len(bin_string), 8):
        byte = bin_string[i:i+8]
        ascii_text += chr(int(byte, 2))
    return ascii_text


des = DES(
    initial_permutation=initial_permutation,
    final_permutation=final_permutation,
    expansion_d_box=expansion_d_box,
    straight_permutation=straight_permutation,
    s_box=s_box,
    key_permutation=key_permutation,
    key_comp_permutation=key_comp_permutation,
    shift_table=shift_table
)

plaintext = "SECRET12"
key = "DESKEY12"
print('Оригінальний текст (ascii):', plaintext)
print('Ключ: (ascii)', key)
# Переведення тексту та ключа в двійкову систему
plaintext_bin = ascii_to_bin(plaintext)
key_bin = ascii_to_bin(key)
print('Оригінальний текст (bin):', plaintext_bin)
print('Ключ (bin):', key_bin)

rkb = des.get_round_key(key_bin)

encrypted_text_bin = des.encrypt(plaintext_bin, rkb)
encrypted_text = bin_to_ascii(encrypted_text_bin)
print('Зашифрований текст (ascii):', encrypted_text)
print('Зашифрований текст (bin):', encrypted_text_bin)
decrypted_text_bin = des.decrypt(encrypted_text_bin, rkb)
decrypted_text = bin_to_ascii(decrypted_text_bin)
print('Розшифрований текст (ascii):', decrypted_text)
print('Розшифрований текст (bin):', decrypted_text_bin)

assert plaintext_bin == decrypted_text_bin
