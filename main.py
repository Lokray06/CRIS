import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import filedialog, messagebox
from encoder import encode_file
from decoder import decode_file
from keygen import generate_rsa_keys  # Assuming you have a keygen module for key generation

def generate_keys_gui():
    name = key_name_entry.get()
    if not name:
        messagebox.showerror("Error", "Please enter a name for the keys.")
        return
    generate_rsa_keys(name)
    messagebox.showinfo("Success", "Keys generated successfully!")

def encode_gui():
    file_path = file_entry.get()
    image_path = image_entry.get()
    key_path = key_entry.get()
    
    if file_path and image_path and key_path:
        encode_file(file_path, image_path, key_path)
        messagebox.showinfo("Success", "File successfully encoded!")
    else:
        messagebox.showerror("Error", "Please select all required files.")

def decode_gui():
    encoded_image_path = encoded_image_entry.get()
    output_file = output_entry.get()
    key_path = private_key_entry.get()
    
    if encoded_image_path and output_file and key_path:
        decode_file(encoded_image_path, output_file, key_path)
        messagebox.showinfo("Success", "File successfully decoded!")
    else:
        messagebox.showerror("Error", "Please select all required files.")

def browse_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tb.END)
    entry.insert(0, file_path)

def about_info():
    messagebox.showinfo("About", "This is a simple RSA-based image steganography tool.")

# Initialize the main window with Breeze dark theme
root = tb.Window(themename="darkly")  # 'superhero' is a dark theme similar to Breeze Dark
root.title("CRIS")

#Set the icon
image = tk.PhotoImage(file= "icon.png")
root.wm_iconphoto(False, image)


notebook = tb.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

# Key Generation Tab
key_tab = tb.Frame(notebook)
notebook.add(key_tab, text="Generate Keys")
tb.Label(key_tab, text="Enter Key Name:").pack(pady=5)
key_name_entry = tb.Entry(key_tab)
key_name_entry.pack(pady=5)
tb.Button(key_tab, cursor="hand2", text="Generate Keys", bootstyle="primary", command=generate_keys_gui).pack(pady=10)

# Encoding Tab
encode_tab = tb.Frame(notebook)
notebook.add(encode_tab, text="Encode")
tb.Label(encode_tab, text="Select File to Encode:").pack(pady=5)
file_entry = tb.Entry(encode_tab, width=50)
file_entry.pack(pady=5)
tb.Button(encode_tab, cursor="hand2", text="Browse", bootstyle="info", command=lambda: browse_file(file_entry)).pack(pady=5)

tb.Label(encode_tab, text="Select Image:").pack(pady=5)
image_entry = tb.Entry(encode_tab, width=50)
image_entry.pack(pady=5)
tb.Button(encode_tab, cursor="hand2", text="Browse", bootstyle="info", command=lambda: browse_file(image_entry)).pack(pady=5)

tb.Label(encode_tab, text="Select Public Key:").pack(pady=5)
key_entry = tb.Entry(encode_tab, width=50)
key_entry.pack(pady=5)
tb.Button(encode_tab, cursor="hand2", text="Browse", bootstyle="info", command=lambda: browse_file(key_entry)).pack(pady=5)

tb.Button(encode_tab, cursor="hand2", text="Encode", bootstyle="success", command=encode_gui).pack(pady=10)

# Decoding Tab
decode_tab = tb.Frame(notebook)
notebook.add(decode_tab, text="Decode")
tb.Label(decode_tab, text="Select Encoded Image:").pack(pady=5)
encoded_image_entry = tb.Entry(decode_tab, width=50)
encoded_image_entry.pack(pady=5)
tb.Button(decode_tab, cursor="hand2", text="Browse", bootstyle="info", command=lambda: browse_file(encoded_image_entry)).pack(pady=5)

tb.Label(decode_tab, text="Select Output File:").pack(pady=5)
output_entry = tb.Entry(decode_tab, width=50)
output_entry.pack(pady=5)
tb.Button(decode_tab, cursor="hand2", text="Browse", bootstyle="info", command=lambda: browse_file(output_entry)).pack(pady=5)

tb.Label(decode_tab, text="Select Private Key:").pack(pady=5)
private_key_entry = tb.Entry(decode_tab, width=50)
private_key_entry.pack(pady=5)
tb.Button(decode_tab, cursor="hand2", text="Browse", bootstyle="info", command=lambda: browse_file(private_key_entry)).pack(pady=5)

tb.Button(decode_tab, cursor="hand2", text="Decode", bootstyle="success", command=decode_gui).pack(pady=10)

import webbrowser
import ttkbootstrap as tb

# About Tab
about_tab = tb.Frame(notebook)
notebook.add(about_tab, text="About")

# App Name
tb.Label(about_tab, text="CRIS", font=("Helvetica", 18, "bold")).pack(pady=(10, 5))

# Short Description
tb.Label(
    about_tab,
    text="Cryptographic RSA Image Steganography",
    font=("Helvetica", 12, "italic")
).pack(pady=5)

# Detailed Description
about_text = (
    "CRIS is a tool that allows you to securely hide encrypted data inside images using RSA encryption.\n\n"
    "- Generate RSA key pairs for encryption and decryption.\n"
    "- Embed sensitive information inside images using a public key.\n"
    "- Extract and decrypt hidden data with the corresponding private key.\n\n"
    "This ensures your data remains confidential and only accessible to those with the correct decryption key."
)

tb.Label(about_tab, text=about_text, wraplength=400, justify="left").pack(pady=10, padx=10)

# GitHub Link (styled manually as a link)
link_label = tb.Label(
    about_tab,
    text="GitHub Repository",
    font=("Helvetica", 12, "underline"),  # Underline the text
    foreground="turquoise",  # Make it look like a hyperlink
    cursor="hand2"  # Change cursor on hover
)
link_label.pack(pady=5)

# Make link clickable
def open_github(event):
    webbrowser.open("https://github.com/Lokray06/CRIS")

link_label.bind("<Button-1>", open_github)  # Open link on click

#Porfolio Link
link_label = tb.Label(
    about_tab,
    text="My web",
    font=("Helvetica", 12, "underline"),  # Underline the text
    foreground="turquoise",  # Make it look like a hyperlink
    cursor="hand2"  # Change cursor on hover
)
link_label.pack(pady=5)

# Make link clickable
def open_github(event):
    webbrowser.open("https://jpgp.es")

link_label.bind("<Button-1>", open_github)  # Open link on click


root.mainloop()