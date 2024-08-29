import random
import string
from collections import Counter

def generate_random_key_square():
    alphabet = list(string.ascii_uppercase.replace('J', ''))
    random.shuffle(alphabet)
    return [alphabet[i:i + 5] for i in range(0, 25, 5)]

def find_position(key_square, char):
    for row in range(5):
        for col in range(5):
            if key_square[row][col] == char:
                return row, col
    return None, None

def decrypt_digraph(key_square, digraph):
    char1, char2 = digraph[0], digraph[1]
    row1, col1 = find_position(key_square, char1)
    row2, col2 = find_position(key_square, char2)

    if row1 == row2:
        # Same row, move left
        return key_square[row1][(col1 - 1) % 5] + key_square[row2][(col2 - 1) % 5]
    elif col1 == col2:
        # Same column, move up
        return key_square[(row1 - 1) % 5][col1] + key_square[(row2 - 1) % 5][col2]
    else:
        # Rectangle swap
        return key_square[row1][col2] + key_square[row2][col1]

def decrypt_playfair(ciphertext, key_square):
    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        digraph = ciphertext[i:i+2]
        plaintext += decrypt_digraph(key_square, digraph)
    return plaintext

def score_text(text):
    # Simple scoring based on common English digraphs
    common_digraphs = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ED', 'ON', 'ES', 'ST']
    score = 0
    for digraph in common_digraphs:
        score += text.count(digraph)
    return score

def brute_force_playfair(ciphertext, iterations=10000):
    best_score = 0
    best_plaintext = ""
    best_key = None

    for _ in range(iterations):
        key_square = generate_random_key_square()
        decrypted_text = decrypt_playfair(ciphertext, key_square)
        current_score = score_text(decrypted_text)

        if current_score > best_score:
            best_score = current_score
            best_plaintext = decrypted_text
            best_key = key_square

    return best_plaintext, best_key

# Example usage
ciphertext = "BPLYKRLHFEKIDBNFVUVIVZHZOPKERVNDFVLXWFESFEYSPTONLYNRBLEPHZSFTABQBNSEMBNZVAQZ"
best_plaintext, best_key = brute_force_playfair(ciphertext, iterations=10000)
print(f"Best decryption attempt:\n{best_plaintext}")
