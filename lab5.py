def mul02(byte_val):
    result = byte_val << 1
    # Перевіряємо що результат буде залишатись в рамках 8-бітового поля
    if byte_val & 0x80:
        # m(x) = x^8 + x^4 + x^3 + x + 1 -> 100011011 -> 0001∣0001∣1011 -> 0x1B
        result ^= 0x1B
    # Перевіряємо що результат буде восьмибітовим числом
    return result & 0xFF


def mul03(byte_val):
    # BF * 03 = BF * (02+01) = BF * 02 + BF = mul02(byte_val) + byte_val
    return mul02(byte_val) ^ byte_val


# Тестування на прикладах
assert mul02(0xD4) == 0xB3
assert mul03(0xBF) == 0xDA

print(f"D4 * 02 = {mul02(0xD4):02X}")
print(f"BF * 03 = {mul03(0xBF):02X}")
