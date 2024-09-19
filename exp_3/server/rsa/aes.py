from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def generate_key():
    return get_random_bytes(16)  # 128-bit key

def encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(plaintext.encode(), AES.block_size)
    return cipher.encrypt(padded_data)

def decrypt(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = cipher.decrypt(ciphertext)
    return unpad(padded_data, AES.block_size).decode()

# Example usage
if __name__ == "__main__":
    key = generate_key()
    plaintext = "Hello, AES encryption!"
    
    encrypted = encrypt(plaintext, key)
    decrypted = decrypt(encrypted, key)
    
    print(f"Original text: {plaintext}")
    print(f"Encrypted (hex): {encrypted.hex()}")
    print(f"Decrypted: {decrypted}")