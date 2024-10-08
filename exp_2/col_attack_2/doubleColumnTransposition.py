from math import ceil

def encrypt(text, key, double_encrypt=False):
    matrix = []
    pointer = 0
    # Number of columns
    col = ceil(len(text)/len(key))
    # Arranging plain text into matrix
    # In row format
    for i in range(col):
        temp = []
        for j in range(len(key)):
            # Add the padding character '_' in
            # the empty cell of the matix
            if(pointer == len(text) or pointer > len(text)):
                temp.append('_')
            else:
                temp.append(text[pointer])
            pointer+=1
        matrix.append(temp)
    print(matrix)
    # Encryption - reading text in column wise format
    encryptedText = ''
    keyList = list(key)
    keyList.sort()
    for i in keyList:
        index = key.index(i)
        for j in range(len(matrix)):
            encryptedText+=matrix[j][index]

    print("encrypted text is: \n"+encryptedText)
    
    if double_encrypt:
        encryptedText, key = encrypt(encryptedText, key)
    
    return encryptedText, key

def decrypt(text, key):
    matrix = []
    pointer = 0
    col = ceil(len(text)/len(key))
    # Arranging cipher text into matrix
    # In row format
    for i in range(len(key)):
        temp = []
        for j in range(col):
            temp.append(text[pointer])
            pointer+=1
        matrix.append(temp)

    # Decryption - reading msg in colum wise format
    decryptedText = ''
    keyList = list(key)
    keyList.sort()
    for i in range(col):
        for j in list(key):
            index = keyList.index(j)
            if matrix[index][i] != '_':
                decryptedText += matrix[index][i]
    print("decrypted text is: \n"+decryptedText)
    return

if __name__ == '__main__':
    plainText = str(input("Enter plain text: "))
    key = str(input("Enter key number format: "))
    double_encrypt = input("Perform double encryption? (y/n): ").lower() == 'y'
    cipherText, key = encrypt(plainText, key, double_encrypt)
    decrypt(cipherText, key)