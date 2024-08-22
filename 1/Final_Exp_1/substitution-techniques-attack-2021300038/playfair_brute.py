def create_playfair_matrix(key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key = "".join(sorted(set(key), key=key.index)).replace("J", "I")
    matrix = []
    for char in key:
        if char not in matrix:
            matrix.append(char)
    for char in alphabet:
        if char not in matrix:
            matrix.append(char)
    return [matrix[i:i + 5] for i in range(0, 25, 5)]

def playfair_decrypt(ciphertext, matrix):
    def find_position(char, matrix):
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == char:
                    return row, col
        return None

    decrypted_text = ""
    ciphertext = ciphertext.upper().replace("J", "I").replace(" ", "")
    
    for i in range(0, len(ciphertext), 2):
        char1, char2 = ciphertext[i], ciphertext[i+1]
        row1, col1 = find_position(char1, matrix)
        row2, col2 = find_position(char2, matrix)

        if row1 == row2:
            decrypted_text += matrix[row1][(col1 - 1) % 5]
            decrypted_text += matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            decrypted_text += matrix[(row1 - 1) % 5][col1]
            decrypted_text += matrix[(row2 - 1) % 5][col2]
        else:
            decrypted_text += matrix[row1][col2]
            decrypted_text += matrix[row2][col1]

    return decrypted_text

key = "PLAYFAIR EXAMPLE"  
ciphertext=input("Enter the ciphertext: ")
matrix = create_playfair_matrix(key)
plaintext = playfair_decrypt(ciphertext, matrix)
print("Decrypted text:", plaintext)
