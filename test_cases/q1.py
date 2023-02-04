def xor_with(string, key):
    res = []
    for i in range(len(string)):
        res.append(chr(ord(string[i])^key))
    res = ''.join(res)
    print(f'XOR with {key}: {res}')

def and_with(string, key):
    res = []
    for i in range(len(string)):
        res.append(chr(ord(string[i])&key))
    res = ''.join(res)
    print(f'AND with {key}: {res}')

def or_with(string, key):
    res = []
    for i in range(len(string)):
        res.append(ord(string[i])|key)
    res = ''.join(str(res))
    print(f'OR with {key}: {res}')


def main():
    string = "Hello World"
    xor_with(string, 0)
    xor_with(string, 1)
    or_with(string, 127)
    and_with(string, 127)
    xor_with(string, 127)
    

if __name__ == "__main__":
    main()

# a)The result will be the same as the original string, this is because XORing a value with 0 does not change its value.
# b) XORing a value with 1 will invert the bits of the value.
# c) The results of the AND, OR, and XOR operations will be different because these operations work on the individual bits of a value.
# The AND operation will keep only the bits that are 1 in both the value and the number it is being ANDed with (127 in this case).
# The OR operation will set to 1 any bit that is 1 in either the value or the number it is being ORed with. 
# The XOR operation will invert the bits that are different between the value and the number it is being XORed with.
# The delete control character (also called DEL or rubout) is the last character in the ASCII repertoire, with the code 127 - 
# ORing with 127 will set all the bits to 1, i.e, the values will be 127. Which is why the result is an empty string.