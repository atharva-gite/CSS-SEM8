import time

def xor_binary_strings(a, b):
    return ''.join('1' if x != y else '0' for x, y in zip(a, b))

def pad_to_8_bits(binary_string):
    return binary_string.ljust(8, '0')

def binary_to_hex(binary):
    return hex(int(binary, 2))[2:].zfill(2)

# Input variables
plaintext = "110000000011110010101"
iv = "11001100"
key = "10000101"
ipad = "01011100"  # 0x5C
opad = "00110110"  # 0x36

# Step 1: Divide plaintext into 8-bit chunks
chunks = [plaintext[i:i+8] for i in range(0, len(plaintext), 8)]
chunks[-1] = pad_to_8_bits(chunks[-1])

print(f"Plaintext chunks: {chunks}")

# Step 2: Calculate z0
z0 = iv + xor_binary_strings(key, ipad)
print(f"\nz0: {z0}")

# Steps 3-4: Calculate z1 to z(k+1)
z = z0
for i, chunk in enumerate(chunks, 1):
    input_text = z + chunk
    print(f"\nEnter this in 'Your text' field to get z{i}: {input_text}")
    time.sleep(5)  # Give user time to input and get hash
    z = input(f"Enter the 8-bit hash value for z{i}: ")

# Calculate z(k+1) with message length
L = pad_to_8_bits(bin(len(plaintext))[2:])
input_text = z + L
print(f"\nEnter this in 'Your text' field to get z{len(chunks)+1}: {input_text}")
time.sleep(5)
z_final = input(f"Enter the 8-bit hash value for z{len(chunks)+1}: ")

# Calculate p and q
p = iv + xor_binary_strings(key, opad)
print(f"\nEnter this in 'Your text' field to get q: {p}")
time.sleep(5)
q = input("Enter the 8-bit hash value for q: ")

# Calculate r and final HMAC tag t
r = q + z_final
print(f"\nEnter this in 'Your text' field to get final HMAC tag t: {r}")
time.sleep(5)
t = input("Enter the 8-bit hash value for final HMAC tag t: ")

# Convert final tag to hexadecimal
t_hex = binary_to_hex(t)

print(f"\nFinal Output (enter this in 'Final Output' field): {t_hex}")