import itertools


def row_column_decrypt(ciphertext, key):
    col = len(key)
    row = len(ciphertext) // col
    matrix = [['\n' for _ in range(col)] for _ in range(row)]

    # Recreate the matrix by placing characters in the correct columns
    sorted_key_indices = sorted(range(len(key)), key=lambda k: key[k])
    index = 0
    for c in sorted_key_indices:
        for r in range(row):
            if index < len(ciphertext):
                matrix[r][c] = ciphertext[index]
                index += 1

    # Read off the matrix row by row to form the plaintext
    plaintext = ""
    for r in range(row):
        for c in range(col):
            if matrix[r][c] != '\n':
                plaintext += matrix[r][c]
    return plaintext


def double_row_column_decrypt(ciphertext, key1, key2):
    # First decryption with key2 (reverse of encryption order)
    first_pass = row_column_decrypt(ciphertext, key2)
    # Second decryption with key1
    plaintext = row_column_decrypt(first_pass, key1)
    return plaintext

# Brute-force attack for Double Row-Column Transposition Cipher


def brute_force_double_row_column(ciphertext, key_length):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    possible_keys = itertools.permutations(alphabet[:key_length])

    for key1_tuple in possible_keys:
        for key2_tuple in possible_keys:
            key1 = ''.join(key1_tuple)
            key2 = ''.join(key2_tuple)
            decrypted = double_row_column_decrypt(ciphertext, key1, key2)
            print(f"With keys '{key1}' and '{key2}': {decrypted}")


ciphertext = """"""
brute_force_double_row_column(ciphertext, 10)
