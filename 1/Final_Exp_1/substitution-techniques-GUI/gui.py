import numpy as np
import tkinter as tk
from tkinter import messagebox


class SymmetricCiphers:
    def __init__(self, key):
        self.key = key

    # Caesar Cipher
    def caesar_cipher_encrypt(self, plaintext):
        shift = int(self.key) % 26
        encrypted_text = ""
        for char in plaintext:
            if char.isalpha():
                shift_base = ord('A') if char.isupper() else ord('a')
                encrypted_text += chr((ord(char) -
                                      shift_base + shift) % 26 + shift_base)
            else:
                encrypted_text += char
        return encrypted_text

    def caesar_cipher_decrypt(self, ciphertext):
        shift = int(self.key) % 26
        decrypt_shift = -shift
        decrypted_text = ""
        for char in ciphertext:
            if char.isalpha():
                shift_base = ord('A') if char.isupper() else ord('a')
                decrypted_text += chr((ord(char) - shift_base +
                                      decrypt_shift) % 26 + shift_base)
            else:
                decrypted_text += char
        return decrypted_text

    # Monoalphabetic Cipher
    def monoalphabetic_cipher_encrypt(self, plaintext):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        key = self.key.upper()
        key_map = {alphabet[i]: key[i] for i in range(26)}
        encrypted_text = ""
        for char in plaintext.upper():
            if char.isalpha():
                encrypted_text += key_map[char]
            else:
                encrypted_text += char
        return encrypted_text

    def monoalphabetic_cipher_decrypt(self, ciphertext):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        key = self.key.upper()
        inverse_key_map = {key[i]: alphabet[i] for i in range(26)}
        decrypted_text = ""
        for char in ciphertext.upper():
            if char.isalpha():
                decrypted_text += inverse_key_map[char]
            else:
                decrypted_text += char
        return decrypted_text

    # Playfair Cipher
    def generate_playfair_matrix(self):
        key = self.key.upper().replace("J", "I")
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        matrix = []
        used_chars = set()

        for char in key:
            if char not in used_chars and char in alphabet:
                matrix.append(char)
                used_chars.add(char)

        for char in alphabet:
            if char not in used_chars:
                matrix.append(char)

        return [matrix[i:i + 5] for i in range(0, 25, 5)]

    def playfair_cipher_encrypt(self, plaintext):
        def find_position(matrix, char):
            for i, row in enumerate(matrix):
                for j, col in enumerate(row):
                    if col == char:
                        return i, j

        plaintext = plaintext.upper().replace("J", "I").replace(" ", "")
        if len(plaintext) % 2 != 0:
            plaintext += "X"

        matrix = self.generate_playfair_matrix()
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

    def playfair_cipher_decrypt(self, ciphertext):
        def find_position(matrix, char):
            for i, row in enumerate(matrix):
                for j, col in enumerate(row):
                    if col == char:
                        return i, j

        matrix = self.generate_playfair_matrix()
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

    # Hill Cipher (using 2x2 matrix)
    def mod_inverse(self, matrix, modulus):
        det = int(np.round(np.linalg.det(matrix)))
        det_inv = pow(det, -1, modulus)
        matrix_inv = (
            det_inv * np.round(det * np.linalg.inv(matrix)).astype(int)) % modulus
        return matrix_inv

    def hill_cipher_encrypt(self, plaintext):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        key_matrix = np.array([[alphabet.index(self.key[i * 2 + j])
                               for j in range(2)] for i in range(2)])
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

    def hill_cipher_decrypt(self, ciphertext):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        key_matrix = np.array([[alphabet.index(self.key[i * 2 + j])
                               for j in range(2)] for i in range(2)])
        inverse_key_matrix = self.mod_inverse(key_matrix, 26)
        ciphertext_numbers = [alphabet.index(
            char) for char in ciphertext.upper()]
        plaintext_numbers = []
        for i in range(0, len(ciphertext_numbers), key_matrix.shape[0]):
            block = ciphertext_numbers[i:i + key_matrix.shape[0]]
            decrypted_block = np.dot(inverse_key_matrix, block) % 26
            plaintext_numbers.extend(int(num) for num in decrypted_block)
        key_size = key_matrix.shape[0]
        while plaintext_numbers and plaintext_numbers[-1] == 0:
            plaintext_numbers.pop()

        plaintext = ''.join(alphabet[num] for num in plaintext_numbers)
        return plaintext

    # Polyalphabetic Cipher (Vigenère Cipher)
    def polyalphabetic_cipher_encrypt(self, plaintext):
        key = self.key.upper()
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

    def polyalphabetic_cipher_decrypt(self, ciphertext):
        key = self.key.upper()
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


# GUI Application with Tkinter
class CipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Symmetric Ciphers GUI")

        # Labels and entries for inputs
        self.lbl_plaintext = tk.Label(root, text="Plaintext:")
        self.lbl_plaintext.grid(row=0, column=0, padx=10, pady=10)
        self.txt_plaintext = tk.Entry(root, width=50)
        self.txt_plaintext.grid(row=0, column=1, padx=10, pady=10)

        self.lbl_key = tk.Label(root, text="Key:")
        self.lbl_key.grid(row=1, column=0, padx=10, pady=10)
        self.txt_key = tk.Entry(root, width=50)
        self.txt_key.grid(row=1, column=1, padx=10, pady=10)

        self.lbl_ciphertext = tk.Label(root, text="Ciphertext:")
        self.lbl_ciphertext.grid(row=2, column=0, padx=10, pady=10)
        self.txt_ciphertext = tk.Entry(root, width=50)
        self.txt_ciphertext.grid(row=2, column=1, padx=10, pady=10)

        # Dropdown menu for selecting the cipher type
        self.cipher_var = tk.StringVar(root)
        self.cipher_var.set("Caesar")  # Default option
        self.lbl_cipher = tk.Label(root, text="Cipher:")
        self.lbl_cipher.grid(row=3, column=0, padx=10, pady=10)
        self.dropdown_cipher = tk.OptionMenu(
            root, self.cipher_var, "Caesar", "Monoalphabetic", "Playfair", "Hill", "Polyalphabetic")
        self.dropdown_cipher.grid(row=3, column=1, padx=10, pady=10)

        # Buttons for encryption and decryption
        self.btn_encrypt = tk.Button(
            root, text="Encrypt", command=self.encrypt_text)
        self.btn_encrypt.grid(row=4, column=0, padx=10, pady=10)

        self.btn_decrypt = tk.Button(
            root, text="Decrypt", command=self.decrypt_text)
        self.btn_decrypt.grid(row=4, column=1, padx=10, pady=10)

    def encrypt_text(self):
        plaintext = self.txt_plaintext.get()
        key = self.txt_key.get()
        cipher = SymmetricCiphers(key)
        cipher_type = self.cipher_var.get()

        if cipher_type == "Caesar":
            result = cipher.caesar_cipher_encrypt(plaintext)
        elif cipher_type == "Monoalphabetic":
            result = cipher.monoalphabetic_cipher_encrypt(plaintext)
        elif cipher_type == "Playfair":
            result = cipher.playfair_cipher_encrypt(plaintext)
        elif cipher_type == "Hill":
            result = cipher.hill_cipher_encrypt(plaintext)
        elif cipher_type == "Polyalphabetic":
            result = cipher.polyalphabetic_cipher_encrypt(plaintext)
        else:
            result = "Invalid cipher type selected."

        self.txt_ciphertext.delete(0, tk.END)
        self.txt_ciphertext.insert(0, result)

    def decrypt_text(self):
        ciphertext = self.txt_ciphertext.get()
        key = self.txt_key.get()
        cipher = SymmetricCiphers(key)
        cipher_type = self.cipher_var.get()

        if cipher_type == "Caesar":
            result = cipher.caesar_cipher_decrypt(ciphertext)
        elif cipher_type == "Monoalphabetic":
            result = cipher.monoalphabetic_cipher_decrypt(ciphertext)
        elif cipher_type == "Playfair":
            result = cipher.playfair_cipher_decrypt(ciphertext)
        elif cipher_type == "Hill":
            result = cipher.hill_cipher_decrypt(ciphertext)
        elif cipher_type == "Polyalphabetic":
            result = cipher.polyalphabetic_cipher_decrypt(ciphertext)
        else:
            result = "Invalid cipher type selected."

        self.txt_plaintext.delete(0, tk.END)
        self.txt_plaintext.insert(0, result)


if __name__ == "__main__":
    root = tk.Tk()
    app = CipherApp(root)
    root.mainloop()
