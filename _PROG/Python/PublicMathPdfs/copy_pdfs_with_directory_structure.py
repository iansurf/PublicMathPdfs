import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def scan_for_pdfs(source_dir):
    """Scan the source directory for all PDF files and their relative paths."""
    pdf_files = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                rel_path = os.path.relpath(root, source_dir)
                pdf_files.append((rel_path, file))
    return pdf_files

def ensure_directory_structure(target_dir, rel_path):
    """Ensure the target directory has the same subdirectory structure as the source."""
    target_path = os.path.join(target_dir, rel_path)
    if not os.path.exists(target_path):
        os.makedirs(target_path, exist_ok=True)
        print(f"Created directory: {target_path}")

def copy_pdfs_with_structure(source_dir, target_dir, overwrite=False):
    """Copy PDF files from source_dir to target_dir, preserving the directory structure."""
    pdf_files = scan_for_pdfs(source_dir)

    if not pdf_files:
        messagebox.showinfo("Info", f"No PDF files found in {source_dir}.")
        return

    for rel_path, pdf_file in pdf_files:
        source_file_path = os.path.join(source_dir, rel_path, pdf_file)
        target_file_path = os.path.join(target_dir, rel_path, pdf_file)

        # Ensure the target directory structure exists
        ensure_directory_structure(target_dir, rel_path)

        # Check if the file already exists in the target directory
        if os.path.exists(target_file_path):
            if overwrite:
                print(f"Overwriting existing file: {target_file_path}")
            else:
                print(f"Skipping existing file: {target_file_path}")
                continue

        # Copy the PDF file
        shutil.copy2(source_file_path, target_file_path)
        print(f"Copied: {source_file_path} -> {target_file_path}")

    messagebox.showinfo("Success", "All PDF files copied successfully!")

def select_directory(title, root):
    """Open a directory selection dialog and return the selected path."""
    dir_path = filedialog.askdirectory(title=title, parent=root)
    return dir_path

def ask_overwrite(root):
    """Ask the user if they want to overwrite existing files."""
    response = messagebox.askyesno("Overwrite Files", "Do you want to overwrite existing PDF files in the target directory?", parent=root)
    return response

if __name__ == "__main__":
    # Create a single Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    try:
        # Select source directory
        source_directory = select_directory("Select Source Directory (e.g., iansurf/Wiskunde)", root)
        if not source_directory:
            messagebox.showerror("Error", "No source directory selected.", parent=root)
            exit(1)

        # Select target directory
        target_directory = select_directory("Select Target Directory (e.g., iansurf/PublicMathPdfs)", root)
        if not target_directory:
            messagebox.showerror("Error", "No target directory selected.", parent=root)
            exit(1)

        # Validate paths
        if not os.path.isdir(source_directory):
            messagebox.showerror("Error", f"Source directory '{source_directory}' does not exist.", parent=root)
            exit(1)

        if not os.path.isdir(target_directory):
            messagebox.showerror("Error", f"Target directory '{target_directory}' does not exist.", parent=root)
            exit(1)

        # Ask if the user wants to overwrite existing files
        overwrite = ask_overwrite(root)

        copy_pdfs_with_structure(source_directory, target_directory, overwrite)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}", parent=root)
    finally:
        root.destroy()  # Clean up the Tkinter root window