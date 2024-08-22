import numpy as np


class SymmetricCiphers:
    def __init__(self, key):
        self.key = key

    # Caesar Cipher
    def caesar_cipher_encrypt(self, plaintext):
        shift = int(self.key) % 26
        encrypted_text = ""
        for char in plaintext:
            if char.isalpha():
                shift_base = ord("A") if char.isupper() else ord("a")
                encrypted_text += chr(
                    (ord(char) - shift_base + shift) % 26 + shift_base
                )
            else:
                encrypted_text += char
        return encrypted_text

    def caesar_cipher_decrypt(self, ciphertext):
        shift = int(self.key) % 26
        # Reverse the shift for decryption
        decrypt_shift = -shift
        decrypted_text = ""
        for char in ciphertext:
            if char.isalpha():
                shift_base = ord("A") if char.isupper() else ord("a")
                decrypted_text += chr(
                    (ord(char) - shift_base + decrypt_shift) % 26 + shift_base
                )
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

        return [matrix[i : i + 5] for i in range(0, 25, 5)]

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
            a, b = plaintext[i], plaintext[i + 1]
            row_a, col_a = find_position(matrix, a)
            row_b, col_b = find_position(matrix, b)

            if row_a == row_b:
                encrypted_text += (
                    matrix[row_a][(col_a + 1) % 5] + matrix[row_b][(col_b + 1) % 5]
                )
            elif col_a == col_b:
                encrypted_text += (
                    matrix[(row_a + 1) % 5][col_a] + matrix[(row_b + 1) % 5][col_b]
                )
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
            a, b = ciphertext[i], ciphertext[i + 1]
            row_a, col_a = find_position(matrix, a)
            row_b, col_b = find_position(matrix, b)

            if row_a == row_b:
                decrypted_text += (
                    matrix[row_a][(col_a - 1) % 5] + matrix[row_b][(col_b - 1) % 5]
                )
            elif col_a == col_b:
                decrypted_text += (
                    matrix[(row_a - 1) % 5][col_a] + matrix[(row_b - 1) % 5][col_b]
                )
            else:
                decrypted_text += matrix[row_a][col_b] + matrix[row_b][col_a]

        return decrypted_text

    def mod_inverse(self, matrix, modulus):
        det = int(np.round(np.linalg.det(matrix)))
        det_inv = pow(det, -1, modulus)
        matrix_inv = (
            det_inv * np.round(det * np.linalg.inv(matrix)).astype(int)
        ) % modulus
        return matrix_inv

    def hill_cipher_encrypt(self, plaintext):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # Convert key from letters to numbers
        key_matrix = np.array(
            [[alphabet.index(self.key[i * 2 + j]) for j in range(2)] for i in range(2)]
        )
        key_size = key_matrix.shape[0]
        # Convert plaintext to numbers
        plaintext_numbers = [alphabet.index(char) for char in plaintext.upper()]
        # Pad plaintext to make sure its length is a multiple of key_size
        padded_plaintext = plaintext_numbers + [0] * (
            (key_size - len(plaintext_numbers) % key_size) % key_size
        )
        ciphertext = ""
        for i in range(0, len(padded_plaintext), key_size):
            block = padded_plaintext[i : i + key_size]
            encrypted_block = np.dot(key_matrix, block) % 26
            ciphertext += "".join(alphabet[int(num)] for num in encrypted_block)
        return ciphertext

    def hill_cipher_decrypt(self, ciphertext):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # Convert key from letters to numbers
        key_matrix = np.array(
            [[alphabet.index(self.key[i * 2 + j]) for j in range(2)] for i in range(2)]
        )
        inverse_key_matrix = self.mod_inverse(key_matrix, 26)
        # Convert ciphertext to numbers
        ciphertext_numbers = [alphabet.index(char) for char in ciphertext.upper()]
        plaintext_numbers = []
        for i in range(0, len(ciphertext_numbers), key_matrix.shape[0]):
            block = ciphertext_numbers[i : i + key_matrix.shape[0]]
            decrypted_block = np.dot(inverse_key_matrix, block) % 26
            plaintext_numbers.extend(int(num) for num in decrypted_block)

        # Remove padding
        # Padding was added with 0 (A). Remove trailing zeros from plaintext_numbers
        key_size = key_matrix.shape[0]
        while plaintext_numbers and plaintext_numbers[-1] == 0:
            plaintext_numbers.pop()

        plaintext = "".join(alphabet[num] for num in plaintext_numbers)
        return plaintext

    # PolyAlphabetic Cipher
    def polyalphabetic_cipher_encrypt(self, plaintext):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        key = self.key.upper()
        key_repeated = (key * (len(plaintext) // len(key) + 1))[: len(plaintext)]
        encrypted_text = ""

        for p, k in zip(plaintext.upper(), key_repeated):
            if p.isalpha():
                encrypted_char = (ord(p) - ord("A") + ord(k) - ord("A")) % 26 + ord("A")
                encrypted_text += chr(encrypted_char)
            else:
                encrypted_text += p

        return encrypted_text

    def polyalphabetic_cipher_decrypt(self, ciphertext):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        key = self.key.upper()
        key_repeated = (key * (len(ciphertext) // len(key) + 1))[: len(ciphertext)]
        decrypted_text = ""

        for c, k in zip(ciphertext.upper(), key_repeated):
            if c.isalpha():
                decrypted_char = (ord(c) - ord("A") - (ord(k) - ord("A"))) % 26 + ord(
                    "A"
                )
                decrypted_text += chr(decrypted_char)
            else:
                decrypted_text += c

        return decrypted_text


def create_plain_cipher_pairs():
    # Get user input for plaintext and cipher type
    plaintext = input("Enter the plaintext: ")
    key = input("Enter the symmetric key: ")
    cipher_type = input(
        "Choose the cipher (caesar, monoalphabetic, playfair, hill, polyalphabetic): "
    )

    # Create an instance of the cipher class
    cipher = SymmetricCiphers(key)

    # Encrypt the plaintext based on the chosen cipher
    if cipher_type.lower() == "caesar":
        ciphertext = cipher.caesar_cipher_encrypt(plaintext)
    elif cipher_type.lower() == "monoalphabetic":
        ciphertext = cipher.monoalphabetic_cipher_encrypt(plaintext)
    elif cipher_type.lower() == "playfair":
        ciphertext = cipher.playfair_cipher_encrypt(plaintext)
    elif cipher_type.lower() == "hill":
        ciphertext = cipher.hill_cipher_encrypt(plaintext)
    elif cipher_type.lower() == "polyalphabetic":
        ciphertext = cipher.polyalphabetic_cipher_encrypt(plaintext)
    else:
        print("Invalid cipher choice.")
        return

    # Output the result
    print(f"Plaintext: {plaintext}")
    print(f"Ciphertext: {ciphertext}")

    # Save the pair to a file
    with open("plain_cipher_pairs.txt", "a") as f:
        f.write(
            f"Cipher Type: {cipher_type}, Key: {key}, Plaintext: {plaintext}, Ciphertext: {ciphertext}\n"
        )


def main():
    while True:
        print("\n--- Symmetric Encryption Main Menu ---")
        print("1. Create and share plain-cipher text pairs")
        print("2. Decrypt received ciphertext")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            create_plain_cipher_pairs()
        elif choice == "2":
            # Decrypt a received ciphertext
            ciphertext = input("Enter the received ciphertext: ")
            key = input("Enter the symmetric key: ")
            cipher_type = input(
                "Choose the cipher used for encryption (caesar, monoalphabetic, playfair, hill, polyalphabetic): "
            )

            cipher = SymmetricCiphers(key)

            if cipher_type.lower() == "caesar":
                plaintext = cipher.caesar_cipher_decrypt(ciphertext)
            elif cipher_type.lower() == "monoalphabetic":
                plaintext = cipher.monoalphabetic_cipher_decrypt(ciphertext)
            elif cipher_type.lower() == "playfair":
                plaintext = cipher.playfair_cipher_decrypt(ciphertext)
            elif cipher_type.lower() == "hill":
                plaintext = cipher.hill_cipher_decrypt(ciphertext)
            elif cipher_type.lower() == "polyalphabetic":
                plaintext = cipher.polyalphabetic_cipher_decrypt(ciphertext)
            else:
                print("Invalid cipher choice.")
                continue

            print(f"Decrypted Plaintext: {plaintext}")
        elif choice == "3":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


import random
import regex as re

if __name__ == "__main__":
    # main()
    plain_text = """Cryptography: The Art and Science of Securing Information

Cryptography is the practice and study of techniques for securing communication and data in the presence of adversaries. It is a fundamental aspect of modern computing and communication systems, enabling the protection of sensitive information such as passwords, credit card numbers, and confidential messages. The core purpose of cryptography is to ensure the confidentiality, integrity, authenticity, and non-repudiation of information.

Historically, cryptography has been used for military and diplomatic communication. One of the earliest known systems, the Caesar cipher, was used by Julius Caesar to secure military messages. This simple substitution cipher shifted the letters of the alphabet by a fixed number, making the message unreadable to unauthorized parties. As communication technologies evolved, so did the complexity of cryptographic techniques, leading to the development of more sophisticated methods such as the Enigma machine used by the Germans in World War II.

Modern cryptography is built on mathematical principles and computer science, utilizing algorithms and protocols to secure digital data. These algorithms fall into two main categories: symmetric and asymmetric. Symmetric encryption uses a single key for both encryption and decryption, making it efficient but requiring secure key distribution. Examples include the Advanced Encryption Standard (AES) and Data Encryption Standard (DES). Asymmetric encryption, on the other hand, uses a pair of keys – a public key for encryption and a private key for decryption. This method is widely used in secure communication protocols like SSL/TLS and in digital signatures.

One of the key challenges in cryptography is balancing security with performance. Strong encryption algorithms often require significant computational resources, which can slow down systems. However, the rapid advancement in computing power and the development of specialized hardware have mitigated these challenges, enabling the widespread use of cryptography in everyday applications.

Cryptography is not without its limitations. The strength of cryptographic systems relies heavily on the secrecy of keys and the security of underlying algorithms. With the advent of quantum computing, traditional cryptographic methods are at risk of being broken, prompting the development of quantum-resistant algorithms. Additionally, the human element remains a significant vulnerability; weak passwords, phishing attacks, and social engineering can compromise even the most robust cryptographic systems.

In conclusion, cryptography is an essential tool in the digital age, safeguarding our data and communication from unauthorized access. Its continuous evolution reflects the ongoing battle between securing information and the ever-present threat of cyber-attacks. As technology advances, so too will the methods of cryptography, ensuring that it remains a cornerstone of information security."""
    def clean_text(text):
        # Remove special characters and numbers
        text = re.sub(r"[^a-zA-Z\s]", "", text)

        # Remove extra whitespace
        text = " ".join(text.split())

        # Convert to lowercase
        text = text.upper()

        return text

    plain_text = clean_text(plain_text)
    # alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # arr = list(alphabets)
    # random.shuffle(arr)
    arr = [
        "M",
        "U",
        "B",
        "R",
        "T",
        "L",
        "Q",
        "P",
        "K",
        "A",
        "E",
        "G",
        "W",
        "C",
        "D",
        "X",
        "I",
        "H",
        "J",
        "Y",
        "O",
        "V",
        "N",
        "Z",
        "F",
        "S",
    ]
    # print(arr)
    # print()
    # print()

    cipher = SymmetricCiphers("".join(arr)).monoalphabetic_cipher_encrypt(plain_text)
    print(cipher)
