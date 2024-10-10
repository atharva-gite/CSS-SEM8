import hashlib

# Constants
l = 8  # Length of the Initialization Vector (IV) and chunks
ipad = 0x5C  # Inner padding byte (binary: 01011100)
opad = 0x36  # Outer padding byte (binary: 00110110)

def xor_binary_strings(bin_str, pad):
    """XOR a binary string with a byte pad."""
    pad_bin_str = f"{pad:08b}"
    return ''.join(str(int(a) ^ int(b)) for a, b in zip(bin_str, pad_bin_str))

def hmac_sha1_step_by_step(plaintext, iv, key):
    # Step 1: Compute z0 = IV || (key XOR ipad)
    z0 = iv + xor_binary_strings(key, ipad)
    print("z0:", z0)  # This value should be entered in "Your text" field for the next step

    # Step 2: Concatenate z0 with m1 to mk (message chunks)
    z1 = z0 + plaintext  # Concatenation with the plaintext
    print("z1:", z1)  # This value should be entered in "Your text" field for the next step

    # Step 3: Compute p = IV || (key XOR opad)
    p = iv + xor_binary_strings(key, opad)
    print("p:", p)  # Enter this value for further steps to get r

    # Final step: z(k+1) = zk || L (L is the length of the message in bits)
    L = bin(len(plaintext))[2:].zfill(8)  # Length of plaintext in binary (8 bits)
    z_k_plus_1 = z1 + L
    print("z(k+1):", z_k_plus_1)  # Manually enter in "Your text" to get the next hash value

    # r = p || z(k+1)
    r = p + z_k_plus_1
    print("r:", r)  # Final result to enter in "Your text" field for the final output

    # Hash the result to get the final HMAC tag
    hmac_tag = hashlib.sha1(r.encode()).hexdigest()
    return hmac_tag

# Example inputs from the image
plaintext = "1100000000111100101010"  # Your binary plaintext
iv = "11001100"  # Initialization vector
key = "10000101"  # Key (binary)

# Step-by-step HMAC computation
hmac_tag = hmac_sha1_step_by_step(plaintext, iv, key)
print("Final HMAC tag:", hmac_tag)
