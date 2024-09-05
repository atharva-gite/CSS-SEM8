def rail_fence_decrypt(ciphertext, key):
    # Create an empty matrix to mark the positions of characters
    rail = [['\n' for _ in range(len(ciphertext))] for _ in range(key)]

    # Fill the rail matrix with markers to identify positions of characters
    dir_down = None
    row, col = 0, 0

    # Mark the positions with '*'
    for i in range(len(ciphertext)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False

        # Mark the position with a placeholder
        rail[row][col] = '*'
        col += 1

        # Move to the next row
        row += 1 if dir_down else -1

    # Fill the rail matrix with the characters of the ciphertext
    index = 0
    for i in range(key):
        for j in range(len(ciphertext)):
            if rail[i][j] == '*' and index < len(ciphertext):
                rail[i][j] = ciphertext[index]
                index += 1

    # Read the matrix in zig-zag to reconstruct the plaintext
    result = []
    row, col = 0, 0
    for i in range(len(ciphertext)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False

        # Append the character to result
        if rail[row][col] != '\n':
            result.append(rail[row][col])
            col += 1

        # Move to the next row
        row += 1 if dir_down else -1

    return "".join(result)


ciphertext = ''
with open("CSS-SEM8/2/transportation-techniques-2021300038/rail_fence_output_file.txt", 'r') as f:
    ciphertext = f.read()

result = rail_fence_decrypt(ciphertext, '3')
print(result)
