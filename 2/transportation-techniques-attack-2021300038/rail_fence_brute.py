def rail_fence_decrypt(ciphertext, num_rails):
    rail = [['\n' for _ in range(len(ciphertext))] for _ in range(num_rails)]
    dir_down = None
    row, col = 0, 0

    # Mark the places where characters will be placed
    for i in range(len(ciphertext)):
        if row == 0:
            dir_down = True
        if row == num_rails - 1:
            dir_down = False

        rail[row][col] = '*'
        col += 1
        row += 1 if dir_down else -1

    # Fill the rail matrix with ciphertext characters
    index = 0
    for i in range(num_rails):
        for j in range(len(ciphertext)):
            if rail[i][j] == '*' and index < len(ciphertext):
                rail[i][j] = ciphertext[index]
                index += 1

    # Read the rail matrix in zig-zag order to form the plaintext
    decrypted_text = []
    row, col = 0, 0
    for i in range(len(ciphertext)):
        if row == 0:
            dir_down = True
        if row == num_rails - 1:
            dir_down = False

        if rail[row][col] != '\n':
            decrypted_text.append(rail[row][col])
            col += 1
        row += 1 if dir_down else -1

    return "".join(decrypted_text)

# Brute-force attack for Rail Fence Cipher


def brute_force_rail_fence(ciphertext, max_rails=10):
    for num_rails in range(2, max_rails + 1):
        decrypted = rail_fence_decrypt(ciphertext, num_rails)
        print(f"With {num_rails} rails: {decrypted}")


ciphertext = ""
brute_force_rail_fence(ciphertext, 10)
