class Ciphers:
    def caesar_cipher_decrypt(ciphertext, shift):
        decrypted_text = ""
        for char in ciphertext:
            if char.isalpha():
                shift_base = ord('A') if char.isupper() else ord('a')
                decrypted_text += chr((ord(char) - shift_base - shift) % 26 + shift_base)
            else:
                decrypted_text += char
        return decrypted_text

    def hill_Cipher(text):
        return 0

    def caesar_Cipher(text, key):
        return 0

def main():
    print("Enter 1 for Caesar Cipher.\n")
    print("Enter 2 for MonoAlphabetic Cipher.\n")
    print("Enter 3 for Playfair Cipher\n")
    print("Enter 4 for Hill Cipher.\n")
    print("Enter 5 for PolyAlphabetic Cipher.\n")
    x = input('Enter a choice: ')
    x=int(x)
    if x==1:
        ciphertext=input("Enter the ciphertext: ")
        for shift in range(1, 26):
            print(f"Shift {shift}: {Ciphers.caesar_cipher_decrypt(ciphertext, shift)}")
    elif x==2:
        return 0
    elif x==3:
        return 0
    elif x==4:
        return 0
    elif x==5:
        return 0

if __name__=="__main__":
    main()
