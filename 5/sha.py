import hashlib
import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

# Generate DH parameters (in practice, these should be exchanged)
parameters = dh.generate_parameters(
    generator=2, key_size=2048, backend=default_backend())

# Generate private keys for both parties (Alice and Bob)
alice_private_key = parameters.generate_private_key()
bob_private_key = parameters.generate_private_key()

# Generate public keys
alice_public_key = alice_private_key.public_key()
bob_public_key = bob_private_key.public_key()

# Alice and Bob exchange public keys and compute the shared secret
alice_shared_key = alice_private_key.exchange(bob_public_key)
bob_shared_key = bob_private_key.exchange(alice_public_key)

# Use a key derivation function (HKDF) to create a symmetric key from the shared secret
derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,  # For AES-256
    salt=None,
    info=b'handshake data',
    backend=default_backend()
).derive(alice_shared_key)

# Ensure both shared keys match
assert alice_shared_key == bob_shared_key, "Key exchange failed!"


# AES Encryption function

def aes_encrypt(key, plaintext):
    # Generate a random initialization vector (IV)
    iv = os.urandom(16)

    # Pad the plaintext to ensure it's a multiple of the block size (AES block size is 128 bits)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()

    # Create AES cipher in CBC mode with the derived key and IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                    backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the padded plaintext
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    return iv, ciphertext

# AES Decryption function


def aes_decrypt(key, iv, ciphertext):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                    backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the ciphertext
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext


# Test the AES encryption and decryption
message = b"cbc"
#examples as per book
# 'abc', 'cbc'
iv, ciphertext = aes_encrypt(derived_key, message)
decrypted_message = aes_decrypt(derived_key, iv, ciphertext)

assert message == decrypted_message, "Decryption failed!"
print("Decrypted message:", decrypted_message.decode())


# Hash the original message
sha512_hash = hashlib.sha512(message).hexdigest()
print("SHA-512 Hash of the original message:", sha512_hash)

# # Hash the ciphertext (optional)
# ciphertext_hash = hashlib.sha512(ciphertext).hexdigest()
# print("SHA-512 Hash of the ciphertext:", ciphertext_hash)
