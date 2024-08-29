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


# Brute-force attack for Row-Column Transposition Cipher


def brute_force_row_column(ciphertext, key_length):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    possible_keys = itertools.permutations(alphabet[:key_length])

    for key_tuple in possible_keys:
        key = ''.join(key_tuple)
        decrypted = row_column_decrypt(ciphertext, key)
        print(f"With key '{key}': {decrypted}")


ciphertext = """"""
brute_force_row_column(ciphertext, 10)
