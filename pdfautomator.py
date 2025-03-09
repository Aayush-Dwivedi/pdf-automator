import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import PyPDF2
import os

def select_pdf():
    file_path.set(filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")]))

def merge_pdfs():
    files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    if not files:
        return
    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if output_path:
        merger = PyPDF2.PdfMerger()
        for pdf in files:
            merger.append(pdf)
        merger.write(output_path)
        merger.close()
        messagebox.showinfo("Success", "PDFs Merged Successfully!")

def split_pdf():
    file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not file:
        return
    reader = PyPDF2.PdfReader(file)
    for i in range(len(reader.pages)):
        writer = PyPDF2.PdfWriter()
        writer.add_page(reader.pages[i])
        output_filename = f"{file[:-4]}_page_{i+1}.pdf"
        with open(output_filename, "wb") as output_pdf:
            writer.write(output_pdf)
    messagebox.showinfo("Success", "PDF Split Successfully!")

def compress_pdf():
    file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not file:
        return
    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if output_path:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()
        for page in reader.pages:
            page.compress_content_streams()
            writer.add_page(page)
        with open(output_path, "wb") as output_pdf:
            writer.write(output_pdf)
        messagebox.showinfo("Success", "PDF Compressed Successfully!")

def extract_text():
    file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not file:
        return
    reader = PyPDF2.PdfReader(file)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    messagebox.showinfo("Extracted Text", text if text else "No text found!")

def encrypt_pdf():
    file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not file:
        return
    password = simpledialog.askstring("Password", "Enter encryption password:", show='*')
    if password:
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if output_path:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            writer.encrypt(password)
            with open(output_path, "wb") as output_pdf:
                writer.write(output_pdf)
            messagebox.showinfo("Success", "PDF Encrypted Successfully!")

def toggle_theme():
    if style.theme_use() == "darkly":
        style.theme_use("flatly")
        root.configure(bg="#ADD8E6")  
    else:
        style.theme_use("darkly")
        root.configure(bg="#333333")  # Dark mode background

# Main Window Setup
root = TkinterDnD.Tk()
root.title("PDF Automator")
root.state('zoomed')
root.configure(bg="#ADD8E6")  # Default Light Blue Background

style = ttk.Style()
style.theme_use("flatly")
style.configure("TButton", font=("Arial", 14), padding=10)

file_path = tk.StringVar()

def drop(event):
    file_path.set(event.data.strip('{}'))

label = tk.Label(root, text="📂 Drop your PDF here", font=("Arial", 18, "bold"), bg="#ffffff", fg="#333", relief="solid", padx=20, pady=10)
label.pack(pady=20)

entry = ttk.Entry(root, textvariable=file_path, width=70, font=("Arial", 14))
entry.pack(pady=10)

root.drop_target_register(DND_FILES)
root.dnd_bind("<<Drop>>", drop)

button_frame = ttk.Frame(root)
button_frame.pack(pady=20)

buttons = [
    ("📂 Select PDF", select_pdf),
    ("📑 Merge PDFs", merge_pdfs),
    ("✂️ Split PDF", split_pdf),
    ("📉 Compress PDF", compress_pdf),
    ("📄 Extract Text", extract_text),
    ("🔒 Encrypt PDF", encrypt_pdf)
]

for i, (text, command) in enumerate(buttons):
    btn = ttk.Button(button_frame, text=text, command=command, bootstyle="primary")
    btn.grid(row=i//3, column=i%3, padx=15, pady=15, sticky="ew")

button_frame.columnconfigure((0, 1, 2), weight=1)

# Dark Mode Toggle Button
theme_button = ttk.Button(root, text="🌙 Toggle Dark Mode", command=toggle_theme, bootstyle="dark")
theme_button.pack(pady=10)

root.mainloop()
