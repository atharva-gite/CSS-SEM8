def caesar_cipher_decrypt(ciphertext, shift):
    decrypted_text = ""
    for char in ciphertext:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            decrypted_text += chr((ord(char) - shift_base -
                                  shift) % 26 + shift_base)
        else:
            decrypted_text += char
    return decrypted_text


ciphertext = """"""
with open("cipher_text_caesar.txt") as f:
    ciphertext = f.read().replace("\n", "")
for shift in range(1, 26):
    print(f"Shift {shift}: {caesar_cipher_decrypt(ciphertext, shift)}")
