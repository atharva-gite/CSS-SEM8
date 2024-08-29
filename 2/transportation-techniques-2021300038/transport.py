def rail_fence_encrypt(plaintext, key):
    # Create an empty matrix to store the zig-zag pattern
    rail = [['\n' for i in range(len(plaintext))] for j in range(key)]

    # Fill the matrix according to the zig-zag pattern
    dir_down = False
    row, col = 0, 0

    for char in plaintext:
        if (row == 0) or (row == key - 1):
            dir_down = not dir_down

        # Place the character in the matrix
        rail[row][col] = char
        col += 1

        # Move to the next row
        row += 1 if dir_down else -1

    # Read the matrix in a linear fashion to create the ciphertext
    ciphertext = []
    for i in range(key):
        for j in range(len(rail[i])):
            if rail[i][j] != '\n':
                ciphertext.append(rail[i][j])
    return "".join(ciphertext)


def row_column_encrypt(plaintext, key):
    col = len(key)
    row = len(plaintext) // col + (len(plaintext) % col != 0)
    matrix = [['\n' for _ in range(col)] for _ in range(row)]

    index = 0
    for r in range(row):
        for c in range(col):
            if index < len(plaintext):
                matrix[r][c] = plaintext[index]
                index += 1

    sorted_key_indices = sorted(range(len(key)), key=lambda k: key[k])
    ciphertext = ""
    for c in sorted_key_indices:
        for r in range(row):
            if matrix[r][c] != '\n':
                ciphertext += matrix[r][c]
    return ciphertext


def double_row_column_encrypt(plaintext, key1, key2):
    # First Row-Column Transposition
    first_pass = row_column_encrypt(plaintext, key1)
    # Second Row-Column Transposition
    ciphertext = row_column_encrypt(first_pass, key2)
    return ciphertext


plaintext = "HELLO WORLD"
key1 = "31524"  # Example key for Row-Column Transposition
key2 = "24153"  # Example second key for Double Row-Column Transposition

# Rail Fence Encryption
rf_encrypted = rail_fence_encrypt(plaintext, 3)
print("Rail Fence Encrypted:", rf_encrypted)

# Row-Column Encryption
rc_encrypted = row_column_encrypt(plaintext.replace(" ", ""), key1)
print("Row-Column Encrypted:", rc_encrypted)

# Double Row-Column Encryption
double_rc_encrypted = double_row_column_encrypt(plaintext.replace(" ", ""), key1, key2)
print("Double Row-Column Encrypted:", double_rc_encrypted)
