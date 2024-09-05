import numpy as np
from sympy import Matrix
import string

def text_to_numbers(text):
    return [ord(char) - ord('A') for char in text.upper() if char in string.ascii_uppercase]

def numbers_to_text(numbers):
    return ''.join([chr(num + ord('A')) for num in numbers])

def matrix_mod_inv(matrix, modulus):
    return Matrix(matrix).inv_mod(modulus)

def hill_cipher_attack(plaintext, ciphertext):
    P = text_to_numbers(plaintext)
    P_reshaped = []
    for i in P:
        P_reshaped.append([i])
    print(P)
    # [
    # [],
    # [],
    # []
    # ]

    # reshape P into the above format

    C = text_to_numbers(ciphertext)
    C_reshaped = []
    for i in C:
        C_reshaped.append([i])
    C_inv = np.invert(C)
    K = C_inv * P
    print(K)
    

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
plaintext = "ACT"
plain_texts = [
            "ACT",
            "BDF",
            "UIG"
        ]

ciphertexts = [
    "POH",
    "FHQ",
    "GGC"
]

M = []

for text in plain_texts:
    M.append(text_to_numbers(text))

C = []

for text in ciphertexts:
    C.append(text_to_numbers(text))

# M_inv = Matrix(M).inv_mod(26)
M_inv = Matrix(M).inv()
C = np.array(C)
K = np.dot(M_inv, C) % 26
# approximate to decimal
for i in range(len(K)):
    for j in range(len(K[i])):
        K[i][j] = int(round(K[i][j], 0))

print(K)


# # with open("plain_text.txt", "r") as file:
# #     plaintext = file.read().replace("\n", "")


# ciphertext = "POH"
# # with open("cipher_text_hill.txt", "r") as file:
# #     ciphertext = file.read().replace("\n", "")
 

# try:
#     print("Attacking Hill cipher...")
#     key = hill_cipher_attack(plaintext, ciphertext)
#     print(f"Recovered key:\n{key}")

#     # Test the recovered key by decrypting the ciphertext
#     decrypted = hill_cipher_decrypt(ciphertext, key)
#     print(f"\nDecrypted text: {decrypted}")

#     if decrypted.startswith(plaintext):
#         print("Attack successful! The decrypted text matches the original plaintext.")
#     else:
#         print("Attack may have failed. The decrypted text doesn't match the original plaintext.")

# except Exception as e:
#     print(f"An error occurred: {str(e)}")