import string


def generate_key_square_from_partial(known_plaintext, ciphertext):
    alphabet = string.ascii_uppercase.replace('J', '')
    key_square, reverse_key_square = {}, {}

    for pt, ct in zip(known_plaintext, ciphertext):
        if pt == 'J':
            pt = 'I'  # Handle 'J' as 'I'
        if key_square.get(pt, ct) != ct or reverse_key_square.get(ct, pt) != pt:
            return None, None  # Inconsistent mapping
        key_square[pt], reverse_key_square[ct] = ct, pt

    # Fill remaining letters
    remaining_letters = [c for c in alphabet if c not in key_square]
    remaining_positions = [c for c in alphabet if c not in reverse_key_square]

    key_square.update(zip(remaining_letters, remaining_positions))

    # Convert to 5x5 matrix
    key_matrix = [[None]*5 for _ in range(5)]
    idx = 0
    for row in range(5):
        for col in range(5):
            key_matrix[row][col] = key_square[alphabet[idx]]
            idx += 1

    return key_matrix, reverse_key_square


def find_position(key_square, char):
    for row, line in enumerate(key_square):
        if char in line:
            return row, line.index(char)
    return None, None


def decrypt_digraph(key_square, digraph):
    row1, col1 = find_position(key_square, digraph[0])
    row2, col2 = find_position(key_square, digraph[1])

    if row1 == row2:
        # Same row, move left
        return key_square[row1][(col1 - 1) % 5] + key_square[row2][(col2 - 1) % 5]
    elif col1 == col2:
        # Same column, move up
        return key_square[(row1 - 1) % 5][col1] + key_square[(row2 - 1) % 5][col2]
    else:
        # Rectangle swap
        return key_square[row1][col2] + key_square[row2][col1]


def decrypt_playfair(ciphertext, key_matrix):
    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        digraph = ciphertext[i:i+2]
        plaintext += decrypt_digraph(key_matrix, digraph)
    return plaintext


# Example usage
ciphertext = "DLMQGDUUEOTGOHCTQD"
known_plaintext = "THIS"

key_matrix, reverse_key_matrix = generate_key_square_from_partial(
    known_plaintext, ciphertext[:len(known_plaintext)])

if key_matrix:
    decrypted_text = decrypt_playfair(ciphertext, reverse_key_matrix)
    print(f"Decrypted text: {decrypted_text}")
else:
    print("Failed to reconstruct the key.")
