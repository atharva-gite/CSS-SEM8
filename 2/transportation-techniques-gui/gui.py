import tkinter as tk


class TransportationCiphers:
    def __init__(self, key):
        self.key = key

    # Rail Fence Cipher
    def rail_fence_encrypt(self, plaintext, num_rails):
        rail = [['\n' for _ in range(len(plaintext))] for _ in range(num_rails)]
        dir_down = False
        row, col = 0, 0

        for char in plaintext:
            if (row == 0) or (row == num_rails - 1):
                dir_down = not dir_down
            rail[row][col] = char
            col += 1
            row += 1 if dir_down else -1

        encrypted_text = []
        for i in range(num_rails):
            for j in range(len(rail[i])):
                if rail[i][j] != '\n':
                    encrypted_text.append(rail[i][j])
        return "".join(encrypted_text)

    # Row-Column Transposition Cipher
    def row_column_encrypt(self, plaintext):
        col = len(self.key)
        row = len(plaintext) // col + (len(plaintext) % col != 0)
        matrix = [['\n' for _ in range(col)] for _ in range(row)]

        index = 0
        for r in range(row):
            for c in range(col):
                if index < len(plaintext):
                    matrix[r][c] = plaintext[index]
                    index += 1

        sorted_key_indices = sorted(range(len(self.key)), key=lambda k: self.key[k])
        ciphertext = ""
        for c in sorted_key_indices:
            for r in range(row):
                if matrix[r][c] != '\n':
                    ciphertext += matrix[r][c]
        return ciphertext

    # Double Row-Column Transposition Cipher
    def double_row_column_encrypt(self, plaintext, second_key):
        # First Row-Column Transposition
        first_pass = self.row_column_encrypt(plaintext)
        # Set second key for second transposition
        self.key = second_key
        # Second Row-Column Transposition
        ciphertext = self.row_column_encrypt(first_pass)
        return ciphertext


# GUI Application with Tkinter
class TransportationCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Transportation Ciphers GUI")

        # Labels and entries for inputs
        self.lbl_plaintext = tk.Label(root, text="Plaintext:")
        self.lbl_plaintext.grid(row=0, column=0, padx=10, pady=10)
        self.txt_plaintext = tk.Entry(root, width=50)
        self.txt_plaintext.grid(row=0, column=1, padx=10, pady=10)

        self.lbl_key = tk.Label(root, text="Key:")
        self.lbl_key.grid(row=1, column=0, padx=10, pady=10)
        self.txt_key = tk.Entry(root, width=50)
        self.txt_key.grid(row=1, column=1, padx=10, pady=10)

        self.lbl_second_key = tk.Label(root, text="Second Key (for Double Transposition):")
        self.lbl_second_key.grid(row=2, column=0, padx=10, pady=10)
        self.txt_second_key = tk.Entry(root, width=50)
        self.txt_second_key.grid(row=2, column=1, padx=10, pady=10)

        self.lbl_ciphertext = tk.Label(root, text="Ciphertext:")
        self.lbl_ciphertext.grid(row=3, column=0, padx=10, pady=10)
        self.txt_ciphertext = tk.Entry(root, width=50)
        self.txt_ciphertext.grid(row=3, column=1, padx=10, pady=10)

        # Dropdown menu for selecting the cipher type
        self.cipher_var = tk.StringVar(root)
        self.cipher_var.set("Rail Fence")  # Default option
        self.lbl_cipher = tk.Label(root, text="Cipher:")
        self.lbl_cipher.grid(row=4, column=0, padx=10, pady=10)
        self.dropdown_cipher = tk.OptionMenu(
            root, self.cipher_var, "Rail Fence", "Row-Column", "Double Row-Column")
        self.dropdown_cipher.grid(row=4, column=1, padx=10, pady=10)

        # Buttons for encryption
        self.btn_encrypt = tk.Button(
            root, text="Encrypt", command=self.encrypt_text)
        self.btn_encrypt.grid(row=5, column=0, padx=10, pady=10)

    def encrypt_text(self):
        plaintext = self.txt_plaintext.get().replace(" ", "")
        key = self.txt_key.get()
        cipher_type = self.cipher_var.get()

        cipher = TransportationCiphers(key)

        if cipher_type == "Rail Fence":
            result = cipher.rail_fence_encrypt(plaintext, int(key))
        elif cipher_type == "Row-Column":
            result = cipher.row_column_encrypt(plaintext)
        elif cipher_type == "Double Row-Column":
            second_key = self.txt_second_key.get()
            result = cipher.double_row_column_encrypt(plaintext, second_key)
        else:
            result = "Invalid cipher type selected."

        self.txt_ciphertext.delete(0, tk.END)
        self.txt_ciphertext.insert(0, result)


if __name__ == "__main__":
    root = tk.Tk()
    app = TransportationCipherApp(root)
    root.mainloop()
