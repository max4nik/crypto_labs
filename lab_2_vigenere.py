class VigenereCypher:

    def encrypt(self, plaintext, key):
        alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
        encrypted_text = ""

        key_length = len(key)
        key_repeated = key * (len(plaintext) // key_length) + key[:len(plaintext) % key_length]

        for i in range(len(plaintext)):
            if plaintext[i] in alphabet:
                plaintext_index = alphabet.index(plaintext[i])
                key_index = alphabet.index(key_repeated[i])
                encrypted_index = (plaintext_index + key_index) % len(alphabet)
                encrypted_text += alphabet[encrypted_index]
            else:
                encrypted_text += plaintext[i]

        return encrypted_text

    def decrypt(self, encrypted_text, key):
        alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
        decrypted_text = ""

        key_length = len(key)
        key_repeated = key * (len(encrypted_text) // key_length) + key[:len(encrypted_text) % key_length]

        for i in range(len(encrypted_text)):
            if encrypted_text[i] in alphabet:
                encrypted_index = alphabet.index(encrypted_text[i])
                key_index = alphabet.index(key_repeated[i])
                decrypted_index = (encrypted_index - key_index) % len(alphabet)
                decrypted_text += alphabet[decrypted_index]
            else:
                decrypted_text += encrypted_text[i]

        return decrypted_text


text = "наступаємонасвітанку"
key = "віженер"
user_input = False
if user_input:
    plaintext = input('Введіть фразу для шифрування: ')
    key = input('Введіть слово-ключ: ')

vigenere_cypher = VigenereCypher()
encrypted_text = vigenere_cypher.encrypt(text, key)
decrypted_text = vigenere_cypher.decrypt(encrypted_text, key)

print("Оригінальний текст:", text)
print("Ключ шифрування:", key)
print("Зашифрований текст:", encrypted_text)
print("Розшифрований текст:", decrypted_text)
