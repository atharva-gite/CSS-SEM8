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
    with open(r"CSS-SEM8\2\transportation-techniques-2021300038\input.txt") as f:
        cipher_text = f.read().replace("\n", "")

    cleaned_text = clean_text(cipher_text)
    return cleaned_text

cipher_text = main()
with open("transport_cipher.txt", "w") as f:
    f.write(cipher_text)