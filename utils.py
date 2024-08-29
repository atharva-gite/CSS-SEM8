import re

def clean_text(text):
    # Remove special characters and numbers
    text = re.sub(r"[^a-zA-Z\s]", "", text) 

    # Remove extra whitespace
    text = " ".join(text.split())

    # Convert to lowercase
    text = text.upper()

    return text

def main():
    with open("cipher_text_poly_a.txt") as f:
        cipher_text = f.read().replace("\n", "")

    cleaned_text = clean_text(cipher_text)
    return cleaned_text

cipher_text = main()
with open("cipher_text_poly_a_cleaned_3.txt", "w") as f:
    f.write(cipher_text)