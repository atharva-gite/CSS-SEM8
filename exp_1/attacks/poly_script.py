import string
from collections import Counter

def calculate_ic(text):
    n = len(text)
    freqs = Counter(text)
    if n <= 1:
        return 0  # Avoid division by zero
    ic = sum([freqs[c] * (freqs[c] - 1) for c in freqs]) / (n * (n - 1))
    return ic

def find_key_length(ciphertext, max_length=20):
    avg_ics = []
    for length in range(1, max_length + 1):
        substrings = [ciphertext[i::length] for i in range(length)]
        avg_ic = sum(calculate_ic(s) for s in substrings) / length
        avg_ics.append((length, avg_ic))
    return max(avg_ics, key=lambda x: x[1])[0]

def shift_letter(letter, shift):
    if letter in string.ascii_uppercase:
        return chr((ord(letter) - ord('A') + shift) % 26 + ord('A'))
    return letter

def vigenere_decrypt(ciphertext, key):
    plaintext = []
    key_length = len(key)
    for i, char in enumerate(ciphertext):
        shift = ord(key[i % key_length]) - ord('A')
        plaintext.append(shift_letter(char, -shift))
    return ''.join(plaintext)

def frequency_analysis(text):
    freq = Counter(text)
    total = sum(freq.values())
    return {char: count / total for char, count in freq.items()}

def find_likely_key_char(column, english_freqs):
    best_correlation = float('-inf')
    best_shift = 0
    for shift in range(26):
        shifted_freq = frequency_analysis(''.join(shift_letter(c, -shift) for c in column))
        correlation = sum(shifted_freq.get(c, 0) * english_freqs.get(c, 0) for c in string.ascii_uppercase)
        if correlation > best_correlation:
            best_correlation = correlation
            best_shift = shift
    return chr(best_shift + ord('A'))

def polyalphabetic_attack(ciphertext):
    english_freqs = {'E': 0.1202, 'T': 0.0910, 'A': 0.0812, 'O': 0.0768, 'I': 0.0731,
                     'N': 0.0695, 'S': 0.0628, 'R': 0.0602, 'H': 0.0592, 'D': 0.0432,
                     'L': 0.0398, 'U': 0.0288, 'C': 0.0271, 'M': 0.0261, 'F': 0.0230,
                     'Y': 0.0211, 'W': 0.0209, 'G': 0.0203, 'P': 0.0182, 'B': 0.0149,
                     'V': 0.0111, 'K': 0.0069, 'X': 0.0017, 'Q': 0.0011, 'J': 0.0010, 'Z': 0.0007}
    
    key_length = find_key_length(ciphertext)
    key = ''
    for i in range(key_length):
        column = ciphertext[i::key_length]
        key += find_likely_key_char(column, english_freqs)
    
    plaintext = vigenere_decrypt(ciphertext, key)
    return plaintext, key

# Example usage
ciphertext = ""
with open("cipher_text_poly.txt") as f:
    ciphertext = f.read().replace("\n", "")
plaintext, key = polyalphabetic_attack(ciphertext)
print(f"Recovered key: {key}")
print(f"Decrypted plaintext: {plaintext}")