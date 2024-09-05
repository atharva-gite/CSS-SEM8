def row_column_decrypt(ciphertext, key):
    col = len(key)
    row = len(ciphertext) // col + (len(ciphertext) % col != 0)

    # Initialize the matrix with empty strings
    matrix = [['' for _ in range(col)] for _ in range(row)]

    # Get the key order to determine how to fill the columns (unsorted key order)
    key_order = [int(k) - 1 for k in key]  # Convert '31524' to [2, 0, 4, 1, 3]

    # Fill the matrix by columns based on the key order
    index = 0
    for i in range(col):
        # Fill the matrix by column order specified by key
        current_col = key_order[i]
        for r in range(row):
            if index < len(ciphertext):
                matrix[r][current_col] = ciphertext[index]
                index += 1

    # Read the matrix row by row to get the plaintext
    plaintext = ""
    for r in range(len(matrix)):
        for c in range(col):
            if matrix[r][c] != '':  # Ignore any padding
                plaintext += matrix[r][c]

    return plaintext


ciphertext = ''
with open("2/transportation-techniques-2021300038/row_column_output_file.txt", 'r') as f:
    ciphertext = f.read()

result = row_column_decrypt(ciphertext, '31524')
print("Decrypted result:", result)
