import os
import fitz  # PyMuPDF for PDF compression & text extraction
import PyPDF2  # For merging, splitting, and encryption
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to merge PDFs
def merge_pdfs(pdf_list, output_path):
    merger = PyPDF2.PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()
    print(f"Merged PDF saved as: {output_path}")

# Function to split a PDF into separate pages
def split_pdf(input_pdf, output_folder):
    with open(input_pdf, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for i in range(len(reader.pages)):
            writer = PyPDF2.PdfWriter()
            writer.add_page(reader.pages[i])
            output_path = os.path.join(output_folder, f"page_{i + 1}.pdf")
            with open(output_path, "wb") as output_pdf:
                writer.write(output_pdf)
            print(f"Saved: {output_path}")

# Function to compress a PDF
def compress_pdf(input_pdf, output_pdf):
    doc = fitz.open(input_pdf)
    doc.save(output_pdf, garbage=4, deflate=True)
    doc.close()
    print(f"Compressed PDF saved as: {output_pdf}")

# Function to encrypt a PDF
def encrypt_pdf(input_pdf, output_pdf, password):
    with open(input_pdf, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(password)
        with open(output_pdf, "wb") as output_file:
            writer.write(output_file)
    print(f"Encrypted PDF saved as: {output_pdf}")

# Function to extract text from a PDF
def extract_text(input_pdf):
    doc = fitz.open(input_pdf)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

# GUI for user interaction
def open_gui():
    root = tk.Tk()
    root.title("PDF Automator")
    root.geometry("400x500")

    def choose_files():
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        return list(files)

    def choose_file():
        file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        return file

    def choose_folder():
        folder = filedialog.askdirectory()
        return folder

    def merge_action():
        files = choose_files()
        if not files:
            messagebox.showerror("Error", "No files selected")
            return
        output = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if output:
            merge_pdfs(files, output)
            messagebox.showinfo("Success", "PDFs Merged Successfully!")

    def split_action():
        file = choose_file()
        if not file:
            messagebox.showerror("Error", "No file selected")
            return
        folder = choose_folder()
        if folder:
            split_pdf(file, folder)
            messagebox.showinfo("Success", "PDF Split Successfully!")

    def compress_action():
        file = choose_file()
        if not file:
            messagebox.showerror("Error", "No file selected")
            return
        output = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if output:
            compress_pdf(file, output)
            messagebox.showinfo("Success", "PDF Compressed Successfully!")

    def encrypt_action():
        file = choose_file()
        if not file:
            messagebox.showerror("Error", "No file selected")
            return
        password = tk.simpledialog.askstring("Password", "Enter password:", show="*")
        if not password:
            messagebox.showerror("Error", "No password entered")
            return
        output = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if output:
            encrypt_pdf(file, output, password)
            messagebox.showinfo("Success", "PDF Encrypted Successfully!")

    def extract_text_action():
        file = choose_file()
        if not file:
            messagebox.showerror("Error", "No file selected")
            return
        text = extract_text(file)
        messagebox.showinfo("Extracted Text", text[:1000])  # Show first 1000 characters

    # Buttons
    tk.Button(root, text="Merge PDFs", command=merge_action).pack(pady=10)
    tk.Button(root, text="Split PDF", command=split_action).pack(pady=10)
    tk.Button(root, text="Compress PDF", command=compress_action).pack(pady=10)
    tk.Button(root, text="Encrypt PDF", command=encrypt_action).pack(pady=10)
    tk.Button(root, text="Extract Text", command=extract_text_action).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    open_gui()
