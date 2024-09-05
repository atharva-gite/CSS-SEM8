def row_column_decrypt(ciphertext, key):
    col = len(key)
    row = len(ciphertext) // col + (len(ciphertext) % col != 0)
    matrix = [['\n' for _ in range(col)] for _ in range(row)]

    # Determine the order of columns based on the sorted key
    sorted_key_indices = sorted(range(len(key)), key=lambda k: key[k])

    # Fill the matrix with the ciphertext in column-wise order based on sorted key
    index = 0
    for c in sorted_key_indices:
        for r in range(row):
            if index < len(ciphertext):
                matrix[r][c] = ciphertext[index]
                index += 1

    # Read the matrix row-wise to get the plaintext
    plaintext = ""
    for r in range(row):
        for c in range(col):
            if matrix[r][c] != '\n':
                plaintext += matrix[r][c]

    return plaintext


def double_row_column_decrypt(ciphertext, key1, key2):
    # Reverse the second Row-Column Transposition
    first_pass = row_column_decrypt(ciphertext, key2)
    # Reverse the first Row-Column Transposition
    plaintext = row_column_decrypt(first_pass, key1)
    return plaintext
