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

    for letter, position in zip(remaining_letters, remaining_positions):
        key_square[letter] = position
        reverse_key_square[position] = letter

    # Convert to 5x5 matrix
    key_matrix = [[key_square[alphabet[5*row + col]]
                   for col in range(5)] for row in range(5)]

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
        return key_square[row1][(col1 - 1) % 5] + key_square[row2][(col2 - 1) % 5]
    elif col1 == col2:
        return key_square[(row1 - 1) % 5][col1] + key_square[(row2 - 1) % 5][col2]
    else:
        return key_square[row1][col2] + key_square[row2][col1]


def decrypt_playfair(ciphertext, key_matrix):
    return ''.join(decrypt_digraph(key_matrix, ciphertext[i:i+2]) for i in range(0, len(ciphertext), 2))


def format_key_square(key_matrix):
    return '\n'.join(' '.join(row) for row in key_matrix)


# Example usage
ciphertext = "MUGSPPLHKDWFQPZONP"
known_plaintext = "IWANT"

key_matrix, reverse_key_matrix = generate_key_square_from_partial(
    known_plaintext, ciphertext[:len(known_plaintext)])

if key_matrix:
    decrypted_text = decrypt_playfair(ciphertext, key_matrix)
    print(f"Reconstructed Key Square:")
    print(format_key_square(key_matrix))
    print(f"\nDecrypted text: {decrypted_text}")
else:
    print("Failed to reconstruct the key.")
