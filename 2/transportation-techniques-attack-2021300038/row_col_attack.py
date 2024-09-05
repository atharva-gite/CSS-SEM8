import itertools
import math
from collections import Counter

# Load a dictionary of common English words to validate decrypted text
with open('english_words.txt', 'r') as f:
    english_words = set(word.strip().lower() for word in f)

# Helper function to split text into chunks


def chunk_text(text, n):
    """Split text into chunks of size n."""
    return [text[i:i+n] for i in range(0, len(text), n)]

# Function to check for common English words in a given text


def is_valid_text(text, threshold=3):
    """Check if text contains at least a certain number of valid English words."""
    words = text.lower().split()
    valid_count = sum(1 for word in words if word in english_words)
    return valid_count >= threshold

# Function to decrypt columnar transposition cipher with a given key


def decrypt_columnar_transposition(ciphertext, num_cols):
    """Decrypts a columnar transposition cipher with a given number of columns."""
    num_rows = math.ceil(len(ciphertext) / num_cols)
    grid = chunk_text(ciphertext, num_rows)

    # Try all permutations of columns
    for perm in itertools.permutations(range(num_cols)):
        rearranged_columns = [''] * num_cols
        for i, p in enumerate(perm):
            rearranged_columns[p] = grid[i]

        # Flatten the grid into a single string
        decrypted_text = ''.join([''.join(column)
                                 for column in zip(*rearranged_columns)])
        if is_valid_text(decrypted_text):
            return decrypted_text, perm

    return None, None

# Main attack function


def columnar_transposition_attack(ciphertext):
    """Attempts to systematically decrypt a columnar transposition cipher."""
    ciphertext = ciphertext.replace(' ', '').upper()

    # Try all possible column numbers from 2 to len(ciphertext)
    for num_cols in range(2, len(ciphertext)):
        decrypted_text, key = decrypt_columnar_transposition(
            ciphertext, num_cols)
        if decrypted_text:
            print(f"Decrypted text: {decrypted_text}")
            print(f"Key (column permutation): {key}")
            break
    else:
        print("Decryption failed.")


# Example ciphertext from the document
ciphertext = """"""
columnar_transposition_attack(ciphertext)
