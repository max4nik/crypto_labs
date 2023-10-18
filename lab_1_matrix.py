import numpy as np


class MatrixCypher:

    def encrypt(self, text, row_key, col_key, matrix_row_length):
        text_matrix = self._build_matrix_from_text(text, matrix_row_length)
        text_matrix = np.array(text_matrix)
        col_key = col_key[:matrix_row_length]
        sorted_col_key = sorted(col_key, key=lambda x: ord(x))
        col_order = [col_key.index(char) for char in sorted_col_key]

        row_len, col_len = text_matrix.shape
        row_key = row_key[:row_len]
        sorted_row_key = sorted(row_key, key=lambda x: ord(x))
        row_order = [row_key.index(char) for char in sorted_row_key]
        text_matrix_permuted = self._permute_matrix(text_matrix, row_order, col_order)
        result = ''

        # Iterate through the columns
        for column in range(col_len):
            for row in range(row_len):
                char = text_matrix_permuted[row, column]
                result += char
            result += ' '
        return result

    def decrypt(self, encrypted_text, row_key, col_key, matrix_row_length):
        matrix = self._text_to_matrix(encrypted_text, matrix_row_length)
        # matrix.append([' '] * matrix_row_length)
        text_matrix = np.array(matrix)
        print(text_matrix)

        row_len, col_len = text_matrix.shape
        row_key = row_key[:row_len]
        sorted_row_key = sorted(row_key, key=lambda x: ord(x))
        row_original_permutation = [row_key.index(char) for char in sorted_row_key]
        row_order_reverse = self._find_inverse_permutation(row_original_permutation)

        col_key = col_key[:matrix_row_length]
        sorted_col_key = sorted(col_key, key=lambda x: ord(x))
        col_original_permutation = [col_key.index(char) for char in sorted_col_key]
        col_order_reverse = self._find_inverse_permutation(col_original_permutation)

        text_matrix_permuted = self._permute_matrix(text_matrix, row_order_reverse, col_order_reverse)
        result = ''
        for row in text_matrix_permuted:
            for char in row:
                result += char
        return result.strip()

    @staticmethod
    def _text_to_matrix(text, N):
        matrix = [[' ' for _ in range(N)] for _ in range((len(text) + N - 1) // N)]

        row, col = 0, 0

        for char in text:
            matrix[row][col] = char
            row += 1
            if row >= len(matrix):
                row = 0
                col += 1

        return matrix

    @staticmethod
    def _build_matrix_from_text(text, N):
        result = []
        current_chunk = []

        for char in text:
            current_chunk.append(char)
            if len(current_chunk) == N:
                result.append(current_chunk)
                current_chunk = []

        while len(current_chunk) < N:
            current_chunk.append(' ')

        result.append(current_chunk)

        return result

    @staticmethod
    def _permute_matrix(matrix, row_permutation, col_permutation):
        matrix = matrix[:, col_permutation]
        matrix = matrix[row_permutation, :]

        return matrix

    @staticmethod
    def _find_inverse_permutation(original_permutation):
        n = len(original_permutation)
        inverse_permutation = [0] * n

        for i in range(n):
            inverse_permutation[original_permutation[i]] = i

        return inverse_permutation


# Приклад використання
text = "програмнезабезпечення"
row_key = "шифр"
column_key = "крипто"
N = 6
user_input = False
if user_input:
    text = input('Введіть фразу для шифрування: ')
    column_key = input('Введіть стовпцеве слово-ключ: ')
    row_key = input('Введіть рядкове слово-ключ: ')
    N = int(input('Введіть бажану довжину матриці (опційно): '))

matrix_cypher = MatrixCypher()
encrypted_text = matrix_cypher.encrypt(text, row_key, column_key, N)
print("Оригінальний текст:", text)
print("Зашифрований текст:", encrypted_text)

decrypted_text = matrix_cypher.decrypt(encrypted_text, row_key, column_key, N)
print("Розшифрований текст:", decrypted_text)
