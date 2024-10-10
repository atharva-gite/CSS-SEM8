import tkinter as tk
from tkinter import ttk, messagebox


def xor_binary_strings(a, b):
    return ''.join('1' if x != y else '0' for x, y in zip(a, b))


def pad_to_8_bits(binary_string):
    return binary_string.ljust(8, '0')


def binary_to_hex(binary):
    return hex(int(binary, 2))[2:].zfill(2)


class HMACCalculator:
    def __init__(self, master):
        self.master = master
        master.title("HMAC Calculator")
        master.geometry("600x400")

        self.plaintext = "011110100000110111000110011000110010010000011100011001"
        self.iv = "11001100"
        self.key = "10000101"
        self.ipad = "01011100"  # 0x5C
        self.opad = "00110110"  # 0x36

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

        self.input_label = ttk.Label(self.frame, text="Input:")
        self.input_label.grid(row=1, column=0, sticky=tk.E, pady=5)

        self.input_entry = ttk.Entry(self.frame, width=50)
        self.input_entry.grid(row=1, column=1, pady=5)

        self.result_label = ttk.Label(self.frame, text="Result:")
        self.result_label.grid(row=2, column=0, sticky=tk.E, pady=5)

        self.result_entry = ttk.Entry(self.frame, width=50)
        self.result_entry.grid(row=2, column=1, pady=5)

        self.next_button = ttk.Button(
            self.frame, text="Next Step", command=self.next_step)
        self.next_button.grid(row=3, column=0, columnspan=2, pady=10)

    def next_step(self):
        if self.current_step == 0:
            self.chunks = [self.plaintext[i:i+8]
                           for i in range(0, len(self.plaintext), 8)]
            self.chunks[-1] = pad_to_8_bits(self.chunks[-1])
            self.z0 = self.iv + xor_binary_strings(self.key, self.ipad)
            self.z_values = [self.z0]
            self.instruction_label.config(
                text="z0 has been calculated. Enter the result in the 'Result' field and press 'Next Step' to continue.")
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.z0)
            self.current_step += 1
        elif self.current_step <= len(self.chunks):
            chunk = self.chunks[self.current_step - 1]
            # Get the previous result from the result field
            prev_result = self.result_entry.get()
            # Concatenate the previous result with the current chunk
            input_text = prev_result + chunk
            self.instruction_label.config(
                text=f"Step {self.current_step}: Enter the result in the 'Result' field to get z{self.current_step}: {input_text}")
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, input_text)
            self.current_step += 1
        elif self.current_step == len(self.chunks) + 1:
            L = pad_to_8_bits(bin(len(self.plaintext))[2:])
            prev_result = self.result_entry.get()
            input_text = prev_result + L
            self.instruction_label.config(
                text=f"Step {self.current_step}: Enter the result in the 'Result' field to get z{self.current_step}: {input_text}")
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, input_text)
            self.current_step += 1
        elif self.current_step == len(self.chunks) + 2:
            p = self.iv + xor_binary_strings(self.key, self.opad)
            self.instruction_label.config(
                text=f"Step {self.current_step}: Enter the result in the 'Result' field to get q: {p}")
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, p)
            self.current_step += 1
        elif self.current_step == len(self.chunks) + 3:
            q = self.result_entry.get()
            z_final = self.result_entry.get()  # Get the final z from the result field
            r = q + z_final
            self.instruction_label.config(
                text=f"Final Step: Enter the result in the 'Result' field to get final HMAC tag t: {r}")
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, r)
            self.current_step += 1
        else:
            t = self.result_entry.get()
            t_hex = binary_to_hex(t)
            self.instruction_label.config(
                text=f"HMAC calculation complete! Final Output (enter this in 'Final Output' field): {t_hex}")
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, t_hex)
            self.next_button.config(state="disabled")

        if 1 <= self.current_step <= len(self.chunks) + 3:
            self.result_entry.delete(0, tk.END)
            self.result_entry.config(state="normal")
        else:
            self.result_entry.config(state="disabled")

    def run(self):
        self.master.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = HMACCalculator(root)
    app.run()
