import os
import shutil
from pathlib import Path

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

def copy_pdfs_with_structure(source_dir, target_dir):
    """Copy PDF files from source_dir to target_dir, preserving the directory structure."""
    pdf_files = scan_for_pdfs(source_dir)

    if not pdf_files:
        print(f"No PDF files found in {source_dir}.")
        return

    for rel_path, pdf_file in pdf_files:
        source_file_path = os.path.join(source_dir, rel_path, pdf_file)
        target_file_path = os.path.join(target_dir, rel_path, pdf_file)

        # Ensure the target directory structure exists
        ensure_directory_structure(target_dir, rel_path)

        # Copy the PDF file
        shutil.copy2(source_file_path, target_file_path)
        print(f"Copied: {source_file_path} -> {target_file_path}")

    print("All PDF files copied successfully!")

if __name__ == "__main__":
    # Example usage
    source_directory = input("Enter the source directory path (e.g., 'iansurf/Wiskunde'): ").strip()
    target_directory = input("Enter the target directory path (e.g., 'iansurf/PublicMathPdfs'): ").strip()

    # Validate paths
    if not os.path.isdir(source_directory):
        print(f"Error: Source directory '{source_directory}' does not exist.")
        exit(1)

    if not os.path.isdir(target_directory):
        print(f"Error: Target directory '{target_directory}' does not exist.")
        exit(1)

    copy_pdfs_with_structure(source_directory, target_directory)