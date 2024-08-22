import itertools
import numpy as np
import matplotlib.pyplot as plt


class Ciphers:
    # Caesar Cipher Start
    def caesar_cipher_encrypt(plaintext, shift):
        encrypted_text = ""
        for char in plaintext:
            if char.isalpha():
                shift_base = ord('A') if char.isupper() else ord('a')
                encrypted_text += chr((ord(char) -
                                      shift_base + shift) % 26 + shift_base)
            else:
                encrypted_text += char
        return encrypted_text

    def caesar_cipher_decrypt(ciphertext, shift):
        return Ciphers.caesar_cipher_encrypt(ciphertext, -shift)
    # Caesar Cipher End

    def monoalphabetic_cipher_encrypt(plaintext, key):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        key_map = {alphabet[i]: key[i] for i in range(26)}
        encrypted_text = ""
        for char in plaintext.upper():
            if char.isalpha():
                encrypted_text += key_map[char]
            else:
                encrypted_text += char
        return encrypted_text

    def monoalphabetic_cipher_decrypt(ciphertext, key):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        inverse_key_map = {key[i]: alphabet[i] for i in range(26)}
        decrypted_text = ""
        for char in ciphertext.upper():
            if char.isalpha():
                decrypted_text += inverse_key_map[char]
            else:
                decrypted_text += char
        return decrypted_text
    # MonoAlphabetic Cipher End

    # Playfair Cipher Start
    def generate_playfair_matrix(key):
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        matrix = []
        used_chars = set()
        key = key.upper().replace("J", "I")

        for char in key:
            if char not in used_chars and char in alphabet:
                matrix.append(char)
                used_chars.add(char)

        for char in alphabet:
            if char not in used_chars:
                matrix.append(char)

        return [matrix[i:i + 5] for i in range(0, 25, 5)]

    def playfair_cipher_encrypt(plaintext, key):
        def find_position(matrix, char):
            for i, row in enumerate(matrix):
                for j, col in enumerate(row):
                    if col == char:
                        return i, j

        plaintext = plaintext.upper().replace("J", "I").replace(" ", "")
        if len(plaintext) % 2 != 0:
            plaintext += "X"

        matrix = Ciphers.generate_playfair_matrix(key)
        encrypted_text = ""

        for i in range(0, len(plaintext), 2):
            a, b = plaintext[i], plaintext[i+1]
            row_a, col_a = find_position(matrix, a)
            row_b, col_b = find_position(matrix, b)

            if row_a == row_b:
                encrypted_text += matrix[row_a][(col_a + 1) %
                                                5] + matrix[row_b][(col_b + 1) % 5]
            elif col_a == col_b:
                encrypted_text += matrix[(row_a + 1) %
                                         5][col_a] + matrix[(row_b + 1) % 5][col_b]
            else:
                encrypted_text += matrix[row_a][col_b] + matrix[row_b][col_a]

        return encrypted_text

    def playfair_cipher_decrypt(ciphertext, key):
        def find_position(matrix, char):
            for i, row in enumerate(matrix):
                for j, col in enumerate(row):
                    if col == char:
                        return i, j

        matrix = Ciphers.generate_playfair_matrix(key)
        decrypted_text = ""

        for i in range(0, len(ciphertext), 2):
            a, b = ciphertext[i], ciphertext[i+1]
            row_a, col_a = find_position(matrix, a)
            row_b, col_b = find_position(matrix, b)

            if row_a == row_b:
                decrypted_text += matrix[row_a][(col_a - 1) %
                                                5] + matrix[row_b][(col_b - 1) % 5]
            elif col_a == col_b:
                decrypted_text += matrix[(row_a - 1) %
                                         5][col_a] + matrix[(row_b - 1) % 5][col_b]
            else:
                decrypted_text += matrix[row_a][col_b] + matrix[row_b][col_a]

        return decrypted_text
    # Playfair Cipher End

    # HILL CIPHER Start
    def mod_inverse(matrix, modulus):
        det = int(np.round(np.linalg.det(matrix)))
        det_inv = pow(det, -1, modulus)
        matrix_inv = (
            det_inv * np.round(det * np.linalg.inv(matrix)).astype(int)) % modulus
        return matrix_inv

    def hill_cipher_encrypt(plaintext, key_matrix):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        key_size = key_matrix.shape[0]
        plaintext_numbers = [alphabet.index(char)
                             for char in plaintext.upper()]
        padded_plaintext = plaintext_numbers + \
            [0] * ((key_size - len(plaintext_numbers) % key_size) % key_size)
        ciphertext = ""
        for i in range(0, len(padded_plaintext), key_size):
            block = padded_plaintext[i:i + key_size]
            encrypted_block = np.dot(key_matrix, block) % 26
            ciphertext += ''.join(alphabet[int(num)]
                                  for num in encrypted_block)
        return ciphertext

    def hill_cipher_decrypt(ciphertext, key_matrix):
        inverse_key_matrix = Ciphers.mod_inverse(key_matrix, 26)
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ciphertext_numbers = [alphabet.index(
            char) for char in ciphertext.upper()]
        plaintext = ""
        for i in range(0, len(ciphertext_numbers), key_matrix.shape[0]):
            block = ciphertext_numbers[i:i + key_matrix.shape[0]]
            decrypted_block = np.dot(inverse_key_matrix, block) % 26
            plaintext += ''.join(alphabet[int(num)] for num in decrypted_block)
        return plaintext
    # HILL CIPHER End

    # PolyAlphabetic Cipher Start
    def vigenere_cipher_encrypt(plaintext, key):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        key = key.upper()
        key_repeated = (key * (len(plaintext) // len(key) + 1)
                        )[:len(plaintext)]
        encrypted_text = ""

        for p, k in zip(plaintext.upper(), key_repeated):
            if p.isalpha():
                encrypted_char = (ord(p) - ord('A') +
                                  ord(k) - ord('A')) % 26 + ord('A')
                encrypted_text += chr(encrypted_char)
            else:
                encrypted_text += p

        return encrypted_text

    def vigenere_cipher_decrypt(ciphertext, key):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        key = key.upper()
        key_repeated = (key * (len(ciphertext) // len(key) + 1)
                        )[:len(ciphertext)]
        decrypted_text = ""

        for c, k in zip(ciphertext.upper(), key_repeated):
            if c.isalpha():
                decrypted_char = (ord(c) - ord('A') -
                                  (ord(k) - ord('A'))) % 26 + ord('A')
                decrypted_text += chr(decrypted_char)
            else:
                decrypted_text += c

        return decrypted_text

    # PolyAlphabetic Cipher End


class BruteForce:
    def brute_force_caesar(ciphertext):
        for shift in range(26):
            decrypted_text = Ciphers.caesar_cipher_decrypt(ciphertext, shift)
            print(f"Shift {shift}: {decrypted_text}")

    def brute_force_vigenere(ciphertext, max_key_length=10):
        for key_length in range(1, max_key_length + 1):
            for key in itertools.product("ABCDEFGHIJKLMNOPQRSTUVWXYZ", repeat=key_length):
                key = ''.join(key)
                decrypted_text = Ciphers.vigenere_cipher_decrypt(
                    ciphertext, key)
                print(f"Key {key}: {decrypted_text}")


class FrequencyAnalysis:
    def plot_frequency(text):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        frequency = {char: 0 for char in alphabet}

        for char in text.upper():
            if char in alphabet:
                frequency[char] += 1

        total_chars = sum(frequency.values())
        relative_frequency = {char: count /
                              total_chars for char, count in frequency.items()}

        plt.bar(relative_frequency.keys(), relative_frequency.values())
        plt.xlabel('Letters')
        plt.ylabel('Relative Frequency')
        plt.title('Relative Frequency of Letters')
        plt.show()
