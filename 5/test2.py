import tkinter as tk
from tkinter import ttk


def xor_binary_strings(a, b):
    return ''.join('1' if x != y else '0' for x, y in zip(a, b))


def pad_to_8_bits(binary_string):
    return binary_string.ljust(8, '0')


class HMACCalculator:
    def __init__(self, master):
        self.master = master
        master.title("HMAC Calculator")
        master.geometry("600x400")

        # Initial values
        self.plaintext = "1001110011011100000110100111110011110000001"
        self.iv = "11001100"  # 8-bit IV
        self.key = "10000101"  # 8-bit key
        self.ipad = "01011100"  # 0x5C (8-bit)
        self.opad = "00110110"  # 0x36 (8-bit)

        self.create_widgets()
        self.current_step = 0
        self.chunks = []
        self.z_values = []
        self.next_step()

    def create_widgets(self):
        self.frame = ttk.Frame(self.master, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.instruction_label = ttk.Label(self.frame, text="", wraplength=550)
        self.instruction_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.input_label = ttk.Label(self.frame, text="Input for hash:")  # Changed label
        self.input_label.grid(row=1, column=0, sticky=tk.E, pady=5)

        self.input_entry = ttk.Entry(self.frame, width=50)
        self.input_entry.grid(row=1, column=1, pady=5)

        self.hash_label = ttk.Label(self.frame, text="Hash result (16-bits):")
        self.hash_label.grid(row=2, column=0, sticky=tk.E, pady=5)

        self.hash_entry = ttk.Entry(self.frame, width=50)
        self.hash_entry.grid(row=2, column=1, pady=5)

        self.final_output_label = ttk.Label(self.frame, text="Final Output:")
        self.final_output_label.grid(row=3, column=0, sticky=tk.E, pady=5)

        self.final_output_entry = ttk.Entry(self.frame, width=50)
        self.final_output_entry.grid(row=3, column=1, pady=5)

        self.next_button = ttk.Button(
            self.frame, text="Next Step", command=self.next_step)
        self.next_button.grid(row=4, column=0, columnspan=2, pady=10)

    def next_step(self):
        if self.current_step == 0:
            # Step 0: Compute z0 as "IV || (key XOR ipad)"
            self.chunks = [self.plaintext[i:i + 8] for i in range(0, len(self.plaintext), 8)]
            self.chunks[-1] = pad_to_8_bits(self.chunks[-1])  # Pad the last chunk if needed
            z0_input = self.iv + xor_binary_strings(self.key, self.ipad)
            self.z_values = [z0_input]

            self.instruction_label.config(
                text="Step 0: Input for z0 (IV + (key ⊕ ipad)). Enter the hash result in the 'Hash result' field.")
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, z0_input)
            self.current_step += 1

        elif self.current_step <= len(self.chunks):
            # Step 1 to k: Hash the previous z value and concatenate with the current chunk
            previous_hash = self.hash_entry.get()  # Input hash from user
            chunk = self.chunks[self.current_step - 1]
            z_input = previous_hash + chunk

            self.instruction_label.config(
                text=f"Step {self.current_step}: Input for z{self.current_step} (hash of z{self.current_step - 1} + chunk). Enter the hash result in the 'Hash result' field.")
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, z_input)
            self.current_step += 1

        elif self.current_step == len(self.chunks) + 1:
            # After all chunks, append length L and hash the result
            previous_hash = self.hash_entry.get()  # Input hash from user
            L = pad_to_8_bits(bin(len(self.plaintext))[2:])
            z_input = previous_hash + L

            self.instruction_label.config(
                text=f"Step {self.current_step}: Input for z(k+1) (hash of zk + length). Enter the hash result in the 'Hash result' field.")
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, z_input)
            self.current_step += 1

        elif self.current_step == len(self.chunks) + 2:
            # Compute p = "IV || (key XOR opad)" and get hash
            p_input = self.iv + xor_binary_strings(self.key, self.opad)

            self.instruction_label.config(
                text=f"Step {self.current_step}: Input for p (IV + (key ⊕ opad)). Enter the hash result in the 'Hash result' field.")
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, p_input)
            self.current_step += 1

        elif self.current_step == len(self.chunks) + 3:
            # Final step: Concatenate q (hash of p) with z(k+1) and hash the result
            q_hash = self.hash_entry.get()  # Hash of p (user input)
            z_final_hash = self.hash_entry.get()  # Input z(k+1) from user
            r_input = q_hash + z_final_hash

            self.instruction_label.config(
                text=f"Final Step: Input for final HMAC (hash of q + z(k+1)). Enter the final hash result in 'Hash result' field.")
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, r_input)
            self.current_step += 1

        if self.current_step <= len(self.chunks) + 3:
            self.hash_entry.delete(0, tk.END)
            self.hash_entry.config(state="normal")
        else:
            # Final HMAC tag calculation
            t = self.hash_entry.get()  # Final HMAC tag (user input)
            self.final_output_entry.delete(0, tk.END)
            self.final_output_entry.insert(0, t)
            self.instruction_label.config(
                text=f"HMAC calculation complete! Final Output: {t}")
            self.next_button.config(state="disabled")

    def run(self):
        self.master.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = HMACCalculator(root)
    app.run()
