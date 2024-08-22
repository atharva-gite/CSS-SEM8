import string
import itertools
def polyalphabetic_brute_force(ciphertext, max_key_length=5):
    alphabet = string.ascii_uppercase
    possible_plaintexts = []

    for key_length in range(1, max_key_length + 1):
        for key in itertools.product(alphabet, repeat=key_length):
            key = ''.join(key)
            decrypted_text = ""
            key_shifts = [ord(k) - ord('A') for k in key]
            for i, char in enumerate(ciphertext):
                if char.isalpha():
                    shift = key_shifts[i % key_length]
                    decrypted_text += chr((ord(char.upper()) - ord('A') - shift) % 26 + ord('A'))
                else:
                    decrypted_text += char
            possible_plaintexts.append((key, decrypted_text))
    
    return possible_plaintexts

ciphertext=input("Enter the ciphertext: ")

# Perform brute-force attack
all_plaintexts = polyalphabetic_brute_force(ciphertext)

# Display all possible plaintexts
for key, plaintext in all_plaintexts:
    print(f"Key {key}: {plaintext}")
