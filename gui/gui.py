# gui.py - Tkinter GUI za Enigma mašinu

import tkinter as tk
from tkinter import ttk

def encrypt_message():
    pass  # Pozvati Enigma backend ovde

root = tk.Tk()
root.title("Enigma Mašina")

tk.Label(root, text="Unesi poruku:").grid(row=0, column=0)
entry_message = tk.Entry(root, width=50)
entry_message.grid(row=0, column=1, columnspan=3)

tk.Label(root, text="Rezultat:").grid(row=1, column=0)
output_message = tk.Entry(root, width=50)
output_message.grid(row=1, column=1, columnspan=3)

tk.Button(root, text="Šifruj", command=encrypt_message).grid(row=2, column=1)

root.mainloop()
