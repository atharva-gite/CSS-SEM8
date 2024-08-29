import sympy as sp
import numpy as np
from itertools import product

def find_key_matrix(ciphertext_pairs, plaintext_pairs, modulus=26):
    """
    Solve for the Hill Cipher key matrix given pairs of plaintext and ciphertext digraphs.
    """
    P = np.array(plaintext_pairs)
    C = np.array(ciphertext_pairs)
    
    P_inv = np.linalg.inv(P) % modulus
    K = (C @ P_inv) % modulus
    
    return sp.Matrix(K.astype(int))

def decrypt_hill_cipher(ciphertext, key_matrix, modulus=26):
    """
    Decrypt a Hill Cipher encrypted message using the key matrix.
    """
    key_inverse = key_matrix.inv_mod(modulus)
    digraphs = np.array([(ord(ciphertext[i]) - ord('A'), ord(ciphertext[i + 1]) - ord('A'))
                         for i in range(0, len(ciphertext), 2)])
    
    plaintext = ""
    for digraph in digraphs:
        P = (key_inverse * sp.Matrix(digraph)) % modulus
        plaintext += ''.join(chr(int(p) + ord('A')) for p in P)
    
    return plaintext

def hill_cipher_cryptanalysis(ciphertext, known_part, position, modulus=26):
    """
    Perform cryptanalysis on a Hill Cipher given a known plaintext part (crib).
    """
    plaintext_pairs = [(ord(known_part[i]) - ord('A'), ord(known_part[i + 1]) - ord('A'))
                       for i in range(0, len(known_part), 2)]
    ciphertext_pairs = [(ord(ciphertext[position + i]) - ord('A'), ord(ciphertext[position + i + 1]) - ord('A'))
                        for i in range(0, len(known_part), 2)]

    try:
        key_matrix = find_key_matrix(ciphertext_pairs, plaintext_pairs, modulus)
        return decrypt_hill_cipher(ciphertext, key_matrix, modulus)
    except:
        print("Unable to find a valid key matrix. Trying brute force...")
        return brute_force_hill_cipher(ciphertext, known_part, position, modulus)

def brute_force_hill_cipher(ciphertext, known_part, position, modulus=26):
    """
    Perform a brute force attack on the Hill Cipher.
    """
    for key in product(range(modulus), repeat=4):
        key_matrix = sp.Matrix(2, 2, key)
        if key_matrix.det() % modulus != 0:
            try:
                decrypted = decrypt_hill_cipher(ciphertext, key_matrix, modulus)
                if decrypted[position:position+len(known_part)] == known_part:
                    return decrypted
            except:
                continue
    return "Unable to decrypt the message."

# Example usage
ciphertext = "XPUVLACBRAHNUKJNGCLSAZOFRAHWBUOEHDTUVXYFCS"
known_part = "WORD"
position = 13

decrypted_plaintext = hill_cipher_cryptanalysis(ciphertext, known_part, position)
print("Decrypted Plaintext:", decrypted_plaintext)