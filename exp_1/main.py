# Import necessary libraries
import string
import numpy as np
import logging
from typing import List, Tuple

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class SubstitutionCiphers:
    def __init__(self):
        self.alphabet = string.ascii_uppercase

    def caesar_cipher(self, text: str, shift: int) -> str:
        """Encrypts text using Caesar Cipher."""
        result = []
        for char in text.upper():
            if char in self.alphabet:
                index = (self.alphabet.index(char) + shift) % 26
                result.append(self.alphabet[index])
            else:
                result.append(char)
        return ''.join(result)

    def monoalphabetic_cipher(self, text: str, key: str) -> str:
        """Encrypts text using Monoalphabetic Cipher."""
        key_map = {self.alphabet[i]: key[i] for i in range(26)}
        return ''.join(key_map.get(char, char) for char in text.upper())

    def playfair_cipher(self, text: str, key: str) -> str:
        """Encrypts text using Playfair Cipher."""
        # Implementation of Playfair Cipher
        pass  # Placeholder for actual implementation

    def hill_cipher(self, text: str, key_matrix: List[List[int]]) -> str:
        """Encrypts text using Hill Cipher."""
        result = []
        text = ''.join(char.upper() for char in text if char.isalpha())  # Keep only alphabetic characters
        text_length = len(text)
        key_size = len(key_matrix)
        padding = key_size - (text_length % key_size)
        text += 'X' * padding  # Padding the text with 'X' if necessary

        for i in range(0, text_length, key_size):
            chunk = text[i:i+key_size]
            chunk_vector = [self.alphabet.index(char) for char in chunk]
            encrypted_vector = np.dot(key_matrix, chunk_vector) % 26
            encrypted_chunk = ''.join(self.alphabet[index] for index in encrypted_vector)
            result.append(encrypted_chunk)

        return ''.join(result)
    
    
    def polyalphabetic_cipher(self, text: str, key: str) -> str:
        """Encrypts text using Polyalphabetic Cipher."""
        result = []
        key_length = len(key)
        for i, char in enumerate(text.upper()):
            if char in self.alphabet:
                shift = self.alphabet.index(key[i % key_length])
                index = (self.alphabet.index(char) + shift) % 26
                result.append(self.alphabet[index])
            else:
                result.append(char)
        return ''.join(result)

    def brute_force_attack(self, cipher_text: str) -> List[str]:
        """Performs brute-force attack on Caesar Cipher."""
        possible_texts = []
        for shift in range(26):
            possible_texts.append(self.caesar_cipher(cipher_text, -shift))
        return possible_texts

def main():
    # Example usage
    cipher = SubstitutionCiphers()
    plain_text = "HELLO WORLD"
    caesar_encrypted = cipher.caesar_cipher(plain_text, 3)
    logging.info(f"Caesar Cipher: {caesar_encrypted}")

    mono_key = "QWERTYUIOPLKJHGFDSAZXCVBNM"
    mono_encrypted = cipher.monoalphabetic_cipher(plain_text, mono_key)
    logging.info(f"Monoalphabetic Cipher: {mono_encrypted}")

    # Add more examples for other ciphers


def main_poly(key):
    cipher = SubstitutionCiphers()
    plain_text = ""
    # with open("plain_text.txt") as f:
    with open("plain_text_2.txt") as f:
        plain_text = f.read().replace("\n", "") 
        
    # Using polyalphabetic cipher
    # poly_key = "KEY"
    poly_key = key
    poly_encrypted = cipher.polyalphabetic_cipher(plain_text, poly_key)
    logging.info(f"Polyalphabetic Cipher: {poly_encrypted}")
    with open("cipher_text_poly_act.txt", "w") as f:
        f.write(poly_encrypted)

def main_hill():
    cipher = SubstitutionCiphers()
    plain_text = ""
    with open("plain_text.txt") as f:
        plain_text = f.read().replace("\n", "")

    # Using Hill cipher
    key_matrix = [[6, 24, 1], [13, 16, 10], [20, 17, 15]]
    hill_encrypted = cipher.hill_cipher(plain_text, key_matrix)
    logging.info(f"Hill Cipher: {hill_encrypted}")
    with open("cipher_text_hill.txt", "w") as f:
        f.write(hill_encrypted)

if __name__ == "__main__":
    # main()
    main_poly("ACT")
    # main_hill()
