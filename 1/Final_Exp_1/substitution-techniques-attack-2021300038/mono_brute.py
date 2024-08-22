import itertools
import string
def monoalphabetic_brute_force(ciphertext):
    alphabet = string.ascii_uppercase
    possible_plaintexts = []
    
    for perm in itertools.permutations(alphabet):
        key_map = dict(zip(perm, alphabet))
        decrypted_text = ''.join(key_map.get(char, char) for char in ciphertext)
        possible_plaintexts.append(decrypted_text)
        
        # This would generate a large number of possibilities, so it's often combined with some form of analysis.
    
    return possible_plaintexts

# 
ciphertext=input("Enter the ciphertext: ")

# Brute-force (Note: For large texts, this is computationally infeasible)
# Uncomment the following to run it; it's more for educational purposes.
all_plaintexts = monoalphabetic_brute_force(ciphertext)
print(all_plaintexts)