import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from sklearn.model_selection import train_test_split

# Parameters
vocab_size = 26  # For A-Z
max_len = 100    # Max length of input text (ciphertext)
embedding_dim = 64
lstm_units = 128

# Generate sample data (Caesar Cipher) for demonstration
def generate_data(num_samples=10000, max_len=max_len):
    plaintexts = []
    ciphertexts = []
    for _ in range(num_samples):
        shift = np.random.randint(1, 26)
        text_len = np.random.randint(5, max_len + 1)
        plaintext = ''.join(np.random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), text_len))
        ciphertext = ''.join(chr((ord(char) - ord('A') + shift) % 26 + ord('A')) for char in plaintext)
        plaintexts.append(plaintext)
        ciphertexts.append(ciphertext)
    return plaintexts, ciphertexts

# Preprocess the text (convert to numerical data)
def preprocess_text(texts, vocab_size):
    texts_encoded = [[ord(char) - ord('A') for char in text] for text in texts]
    texts_padded = tf.keras.preprocessing.sequence.pad_sequences(texts_encoded, maxlen=max_len, padding='post')
    return np.array(texts_padded)

# Generate data
plaintexts, ciphertexts = generate_data()

# Preprocess data
X = preprocess_text(ciphertexts, vocab_size)
y = preprocess_text(plaintexts, vocab_size)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Define the model
model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_len),
    LSTM(lstm_units, return_sequences=True),
    Dense(vocab_size, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=64)

# Function to decode ciphertext using the trained model
def decode_ciphertext(model, ciphertext):
    input_seq = preprocess_text([ciphertext], vocab_size)
    predicted_seq = model.predict(input_seq)
    predicted_text = ''.join(chr(np.argmax(char) + ord('A')) for char in predicted_seq[0])
    return predicted_text.strip()

# Test the model
ciphertext_example = "KHOORZRUOG"  # Encrypted form of "HELLOWORLD" with Caesar cipher shift of 3
decoded_text = decode_ciphertext(model, ciphertext_example)
print(f"Ciphertext: {ciphertext_example}")
print(f"Decoded text: {decoded_text}")
