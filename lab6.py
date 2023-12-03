class AES:
    def __init__(
            self,
            s_box,
            inv_s_box,
            rcon,
    ):
        self.s_box = s_box
        self.inv_s_box = inv_s_box
        self.rcon = rcon
        self.Nb = 4  # кількість колонок в стані (фіксовано)
        self.Nk = 4  # кількість 32-бітних слів у ключі
        self.Nr = 10  # кількість раундів у шифруванні

    def _sub_bytes(self, state):
        for i in range(4):
            for j in range(self.Nb):
                state[i][j] = self.s_box[state[i][j]]

        return state

    def _shift_rows(self, state):
        state[1][0], state[1][1], state[1][2], state[1][3] = state[1][1], state[1][2], state[1][3], state[1][0]
        state[2][0], state[2][1], state[2][2], state[2][3] = state[2][2], state[2][3], state[2][0], state[2][1]
        state[3][0], state[3][1], state[3][2], state[3][3] = state[3][3], state[3][0], state[3][1], state[3][2]
        return state

    def _mix_columns(self, state):
        for i in range(4):
            col = [state[j][i] for j in range(self.Nb)]

            state[0][i] = self._gmul(col[0], 2) ^ self._gmul(col[1], 3) ^ self._gmul(col[2], 1) ^ self._gmul(col[3], 1)
            state[1][i] = self._gmul(col[0], 1) ^ self._gmul(col[1], 2) ^ self._gmul(col[2], 3) ^ self._gmul(col[3], 1)
            state[2][i] = self._gmul(col[0], 1) ^ self._gmul(col[1], 1) ^ self._gmul(col[2], 2) ^ self._gmul(col[3], 3)
            state[3][i] = self._gmul(col[0], 3) ^ self._gmul(col[1], 1) ^ self._gmul(col[2], 1) ^ self._gmul(col[3], 2)

        return state

    def _add_round_key(self, state, round_key):
        for i in range(4):
            for j in range(self.Nb):
                state[i][j] ^= round_key[i][j]
        return state

    def _key_expansion(self, key):
        total_round_keys = self.Nb * (self.Nr + 1)
        round_keys = [[0] * 4 for _ in range(total_round_keys)]

        for r in range(self.Nk):
            for c in range(4):
                round_keys[r][c] = key[r * 4 + c]

        for i in range(self.Nk, total_round_keys):
            temp = round_keys[i - 1].copy()
            if i % self.Nk == 0:
                temp = self._sub_word(self._rot_word(temp))
                temp[0] = temp[0] ^ self.rcon[i // self.Nk]
            for j in range(4):
                round_keys[i][j] = round_keys[i - self.Nk][j] ^ temp[j]
        for l in round_keys:
            print([a for a in l])
        return round_keys


    def encrypt(self, input, key):
        if not isinstance(input, bytearray):
            input = bytearray(input)

        if len(input) % 16 != 0:
            padding_length = 16 - (len(input) % 16)
            input.extend([padding_length] * padding_length)

        # Початкове перетворення ключа
        round_keys = self._key_expansion(bytearray(key))
        encrypted_blocks = bytearray()
        for i in range(0, len(input), 16):
            block = input[i:i + 16]
            state = [[block[i * 4 + j] for j in range(4)] for i in range(4)]

            state = self._add_round_key(state, round_keys[:self.Nb])

            # Основні раунди
            for i in range(1, self.Nr):
                state = self._sub_bytes(state)
                state = self._shift_rows(state)
                state = self._mix_columns(state)
                state = self._add_round_key(state, round_keys[i * self.Nb:(i + 1) * self.Nb])

            # Останній раунд (без MixColumns)
            state = self._sub_bytes(state)
            state = self._shift_rows(state)
            state = self._add_round_key(state, round_keys[self.Nr * self.Nb:])

            encrypted_block = [byte for row in state for byte in row]
            encrypted_blocks.extend(encrypted_block)

        return encrypted_blocks

    def _inv_sub_bytes(self, state):
        for i in range(4):
            for j in range(self.Nb):
                state[i][j] = self.inv_s_box[state[i][j]]
        return state

    def _inv_shift_rows(self, state):
        state[1][0], state[1][1], state[1][2], state[1][3] = state[1][3], state[1][0], state[1][1], state[1][2]
        state[2][0], state[2][1], state[2][2], state[2][3] = state[2][2], state[2][3], state[2][0], state[2][1]
        state[3][0], state[3][1], state[3][2], state[3][3] = state[3][1], state[3][2], state[3][3], state[3][0]
        return state

    def _inv_mix_columns(self, state):
        for i in range(4):
            col = [state[j][i] for j in range(4)]
            state[0][i] = self._gmul(col[0], 14) ^ self._gmul(col[1], 11) ^ self._gmul(col[2], 13) ^ self._gmul(col[3],
                                                                                                                9)
            state[1][i] = self._gmul(col[0], 9) ^ self._gmul(col[1], 14) ^ self._gmul(col[2], 11) ^ self._gmul(col[3],
                                                                                                               13)
            state[2][i] = self._gmul(col[0], 13) ^ self._gmul(col[1], 9) ^ self._gmul(col[2], 14) ^ self._gmul(col[3],
                                                                                                               11)
            state[3][i] = self._gmul(col[0], 11) ^ self._gmul(col[1], 13) ^ self._gmul(col[2], 9) ^ self._gmul(col[3],
                                                                                                               14)
        return state

    def decode(self, cryptotext, key):
        round_keys = self._key_expansion(key)

        state = [[cryptotext[i * 4 + j] for j in range(4)] for i in range(4)]

        state = self._add_round_key(state, round_keys[self.Nr * self.Nb:])

        # Основні раунди
        for i in range(self.Nr - 1, 0, -1):
            state = self._inv_shift_rows(state)
            state = self._inv_sub_bytes(state)
            state = self._add_round_key(state, round_keys[i * self.Nb:(i + 1) * self.Nb])
            state = self._inv_mix_columns(state)

        # Останній раунд (без InvMixColumns)
        state = self._inv_shift_rows(state)
        state = self._inv_sub_bytes(state)
        state = self._add_round_key(state, round_keys[:self.Nb])

        decoded_text = [byte for row in state for byte in row]

        return decoded_text

    def _gmul(self, a, b):
        p = 0
        for counter in range(8):
            if b & 1:
                p ^= a
            carry = a & 0x80
            a <<= 1
            if carry:
                a ^= 0x11b
            b >>= 1
        return p & 0xFF

    def _rot_word(self, word):
        return word[1:] + word[:1]

    def _sub_word(self, word):
        return [self.s_box[b] for b in word]

s_box = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
)
inv_s_box = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D
)

rcon = [
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C
]


# Testing
aes = AES(s_box, inv_s_box, rcon)
plaintext_str = "AESAlgorithmTest"
plaintext = [int(ord(c)) for c in plaintext_str]
key = (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)

print("Ключ (128 біт):", [hex(b) for b in key])
print("Оригінальний текст:", plaintext_str)
print("Оригінальний текст (128 біт):", [hex(b) for b in plaintext])

encrypted_text = aes.encrypt(bytearray(plaintext), bytearray(key))
encrypted_text_str = ''.join([chr(b) for b in encrypted_text])
print("Зашифрований текст:", encrypted_text_str)
print("Зашифрований текст (128 біт):", [hex(b) for b in encrypted_text])

decrypted_text = aes.decode(encrypted_text, bytearray(key))
decrypted_text_str = ''.join([chr(b) for b in decrypted_text])
print("Розшифрований текст:", decrypted_text_str)
print("Розшифрований текст (128 біт):", [hex(b) for b in decrypted_text])
assert decrypted_text == list(plaintext)
assert decrypted_text_str == plaintext_str

