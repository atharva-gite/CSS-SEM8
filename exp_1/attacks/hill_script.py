import numpy as np
from sympy import Matrix
import string

def text_to_numbers(text):
    return [ord(char) - ord('A') for char in text.upper() if char in string.ascii_uppercase]

def numbers_to_text(numbers):
    return ''.join([chr(num + ord('A')) for num in numbers])

def matrix_mod_inv(matrix, modulus):
    return Matrix(matrix).inv_mod(modulus)

def hill_cipher_attack(plaintext, ciphertext, block_size):
    # Convert plaintext and ciphertext to numbers
    P = text_to_numbers(plaintext)
    C = text_to_numbers(ciphertext)

    # Ensure we have enough plaintext-ciphertext pairs
    if len(P) < block_size * block_size or len(C) < block_size * block_size:
        raise ValueError("Not enough plaintext-ciphertext pairs for the given block size")

    # Create matrices
    P_matrix = np.array(P[:block_size * block_size]).reshape(block_size, block_size)
    C_matrix = np.array(C[:block_size * block_size]).reshape(block_size, block_size)

    print("uninverted", P_matrix)

    # Calculate the key matrix
    P_inv = matrix_mod_inv(P_matrix, 26)
    K = (P_inv * Matrix(C_matrix)) % 26

    return np.array(K).astype(int)

def hill_cipher_decrypt(ciphertext, key):
    block_size = key.shape[0]
    C = text_to_numbers(ciphertext)
    P = []

    # Pad the ciphertext if necessary
    if len(C) % block_size != 0:
        C += [0] * (block_size - (len(C) % block_size))

    # Decrypt in blocks
    for i in range(0, len(C), block_size):
        block = np.array(C[i:i+block_size])
        decrypted_block = np.dot(matrix_mod_inv(key, 26), block) % 26
        P.extend(decrypted_block)

    return numbers_to_text(P)

# Example usage
plaintext = ""
with open("plain_text.txt", "r") as file:
    plaintext = file.read().replace("\n", "")


ciphertext = ""
with open("cipher_text_hill.txt", "r") as file:
    ciphertext = file.read().replace("\n", "")

block_size = 3

try:
    print("Attacking Hill cipher...")
    key = hill_cipher_attack(plaintext, ciphertext, block_size)
    print(f"Recovered key:\n{key}")

    # Test the recovered key by decrypting the ciphertext
    decrypted = hill_cipher_decrypt(ciphertext, key)
    print(f"\nDecrypted text: {decrypted}")

    if decrypted.startswith(plaintext):
        print("Attack successful! The decrypted text matches the original plaintext.")
    else:
        print("Attack may have failed. The decrypted text doesn't match the original plaintext.")

except Exception as e:
    print(f"An error occurred: {str(e)}")