# import hashlib
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import AES, PKCS1_OAEP
# from Crypto.Random import get_random_bytes

# # Part 1: SHA-512 Hash Function


# def sha512_hash(data):
#     sha512 = hashlib.sha512()
#     sha512.update(data)
#     return sha512.hexdigest()

# # Part 2: Symmetric Encryption (AES)


# def aes_encrypt(data, key):
#     cipher = AES.new(key, AES.MODE_EAX)
#     nonce = cipher.nonce
#     ciphertext, tag = cipher.encrypt_and_digest(data)
#     return nonce, ciphertext, tag

# # Part 3: Public-Key Encryption (RSA)


# def rsa_encrypt(data, public_key):
#     cipher_rsa = PKCS1_OAEP.new(public_key)
#     encrypted_data = cipher_rsa.encrypt(data)
#     return encrypted_data

# # Generate RSA keys


# def generate_rsa_keys():
#     key = RSA.generate(2048)
#     private_key = key
#     public_key = key.publickey()
#     return private_key, public_key

# # Simulate the four cases


# def simulate_cases(data_list):
#     private_key, public_key = generate_rsa_keys()
#     aes_key = get_random_bytes(16)  # AES requires a 16-byte key for AES-128

#     for idx, data in enumerate(data_list):
#         print(f"\nCase {idx + 1}:")

#         # 1. SHA-512 Hash
#         hash_value = sha512_hash(data)
#         print(f"SHA-512 Hash: {hash_value}")

#         # 2. AES Encryption
#         nonce, ciphertext, tag = aes_encrypt(data, aes_key)
#         print(f"AES Encrypted: {ciphertext.hex()}")

#         # 3. RSA Encryption
#         rsa_encrypted_data = rsa_encrypt(data, public_key)
#         print(f"RSA Encrypted: {rsa_encrypted_data.hex()}")


# # Sample data for four cases
# data_list = [
#     b"Hello, this is case 1",
#     b"Different message for case 2",
#     b"Another one for case 3",
#     b"Final message for case 4"
# ]

# # Run the simulation for four cases
# simulate_cases(data_list)


# # Explanation:
# # SHA-512 Function: Uses Python's hashlib to compute the SHA-512 hash of the input data.
# # AES Encryption: Uses pycryptodome for AES encryption. The AES key is randomly generated, and we use AES in EAX mode, which provides authentication.
# # RSA Encryption: Uses RSA public-key encryption with PKCS1_OAEP from pycryptodome.
# # simulate_cases: This function runs the SHA-512 hash, AES encryption, and RSA encryption on four different pieces of data.
print(len('1001110011011100000110100111110011110000001'))