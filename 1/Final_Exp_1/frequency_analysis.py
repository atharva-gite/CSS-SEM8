import matplotlib.pyplot as plt
from collections import Counter
import string

def plot_letter_frequency(text):
    text = ''.join(filter(str.isalpha, text.upper()))
    
    # count  frequency of each letter
    letter_counts = Counter(text)
    
    # calculate  total number of letters
    total_letters = sum(letter_counts.values())
    
    # calculate  relative frequency of each letter
    frequencies = {letter: count / total_letters for letter, count in letter_counts.items()}
    
    # sort by alphabet
    sorted_letters = sorted(frequencies.keys())
    sorted_frequencies = [frequencies[letter] for letter in sorted_letters]
    
    # plot
    plt.figure(figsize=(10, 6))
    plt.bar(sorted_letters, sorted_frequencies, color='skyblue')
    plt.title('Relative Frequency of Occurrence of Letters')
    plt.xlabel('Letters')
    plt.ylabel('Relative Frequency')
    plt.show()

ciphertext=input("Enter the ciphertext: ")
plot_letter_frequency(ciphertext)
