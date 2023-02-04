import math

# ceaser cipher
def ceaser_cipher_encrypt(message, key):
    message = list(message)
    for i in range(len(message)):
        if message[i].isalpha():
            if message[i].isupper():
                message[i] = chr((ord(message[i]) + key - 65) % 26 + 65)
            else:
                message[i] = chr((ord(message[i]) + key - 97) % 26 + 97)
    return ''.join(message)

def ceaser_cipher_decrypt(message, key):
    message = list(message)
    for i in range(len(message)):
        if message[i].isalpha():
            if message[i].isupper():
                message[i] = chr((ord(message[i]) - key - 65) % 26 + 65)
            else:
                message[i] = chr((ord(message[i]) - key - 97) % 26 + 97)
    return ''.join(message)

# rail fence cipher

def rail_fence_encrypt(plaintext, key):
    rail = [['\n' for i in range(len(plaintext))] for j in range(key)]
    # create a 2D list with key rows and length of plaintext columns
    # fill it with newline characters
    dir_down = False
    row, col = 0, 0
    for char in plaintext:
        rail[row][col] = char
        if (row == 0) or (row == key - 1):
            dir_down = not dir_down
        row += 1 if dir_down else -1
        col += 1
    result = []
    for row in rail:
        for char in row:
            if char != '\n':
                result.append(char)
    return "".join(result)

def rail_fence_decrypt(ciphertext, key):
    rail = [['\n' for i in range(len(ciphertext))] for j in range(key)]
    # create a 2D list with key rows and length of ciphertext columns
    # fill it with newline characters
    dir_down = None
    row, col = 0, 0
    for i in range(len(ciphertext)):
        rail[row][col] = '*'
        if (row == 0):
            dir_down = True
        if (row == key-1):
            dir_down = False
        row += 1 if dir_down else -1
        col += 1

    index = 0
    for row in range(key):
        for col in range(len(ciphertext)):
            if ((rail[row][col] == '*') and (index < len(ciphertext))):
                rail[row][col] = ciphertext[index]
                index += 1
    result = []
    row, col = 0, 0
    for i in range(len(ciphertext)):
        if (row == 0):
            dir_down = True
        if (row == key-1):
            dir_down = False
        if (rail[row][col] != '\n'):
            result.append(rail[row][col])
            col += 1
        row += 1 if dir_down else -1
    return "".join(result)

# simple transposition cipher (columnar transposition)

def columnar_transposition_encrypt(plaintext, key):
    # Create a grid with the plaintext
    grid = [''] * key
    for col in range(key):
        pointer = col
        while pointer < len(plaintext):
            grid[col] += plaintext[pointer]
            pointer += key
    # Read the ciphertext off by columns
    ciphertext = ''
    for col in range(key):
        ciphertext += grid[col]
    return ciphertext

def columnar_transposition_decrypt(ciphertext, key):
    numOfRows = key
    plaintext = [''] * len(ciphertext)
    col = 0
    row = 0
    for symbol in ciphertext:
        plaintext[col] += symbol
        col += numOfRows
        if (col >= len(ciphertext)):
            col = row + 1
            row += 1
    print(plaintext)
    return ''.join(plaintext)

# plaintext = "HELLO WORLD"
# print('Original Text:', plaintext)

# print('Ceaser Cipher')
# key = 3
# ciphertext = ceaser_cipher_encrypt(plaintext, key)
# print("Ciphertext:", ciphertext)
# decrypted_text = ceaser_cipher_decrypt(ciphertext, key)
# print("Decrypted Text:", decrypted_text)

# print('Rail Fence Cipher')
# key = 3
# ciphertext = rail_fence_encrypt(plaintext, key)
# print("Ciphertext:", ciphertext)
# decrypted_text = rail_fence_decrypt(ciphertext, key)
# print("Decrypted Text:", decrypted_text)

# print('Columnar Transposition Cipher')       
# key = 5
# ciphertext = columnar_transposition_encrypt(plaintext, key)
# print("Ciphertext:", ciphertext)
# decrypted_text = columnar_transposition_decrypt(ciphertext, key)
# print("Decrypted Text:", decrypted_text)

ciphertext = 'hs yis ls eftstof n^ TyymrieraseMr e ho ec^etose Dole^'
key = 24153
print(columnar_transposition_decrypt(ciphertext, key))