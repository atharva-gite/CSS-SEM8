import numpy as np

def hill_cipher_decrypt(ciphertext, key_matrix):
    # Ensure key matrix is invertible and find its inverse modulo 26
    det = int(np.round(np.linalg.det(key_matrix)))
    det_inv = pow(det, -1, 26)
    key_matrix_inv = (det_inv * np.round(det * np.linalg.inv(key_matrix)).astype(int) % 26)
    
    ciphertext_numbers = [(ord(char) - ord('A')) for char in ciphertext]
    plaintext_numbers = []

    for i in range(0, len(ciphertext_numbers), 2):
        vector = np.array(ciphertext_numbers[i:i+2])
        result = np.dot(key_matrix_inv, vector) % 26
        plaintext_numbers.extend(result)

    plaintext = ''.join(chr(int(num) + ord('A')) for num in plaintext_numbers)
    return plaintext

ciphertext=input("Enter the ciphertext: ")
key_matrix = np.array([[1, 2], [3, 5]])  

plaintext = hill_cipher_decrypt(ciphertext, key_matrix)
print("Decrypted text:", plaintext)
