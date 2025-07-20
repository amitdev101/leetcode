#!/usr/bin/env python3
import os
import sys
from PyPDF2 import PdfMerger

def merge_pdfs(input_folder: str, output_path: str):
    """
    Merge all PDF files in input_folder (sorted by name)
    into a single PDF at output_path.
    """
    # List all files ending with .pdf (case-insensitive), sorted alphanumerically
    pdf_files = sorted(
        f for f in os.listdir(input_folder)
        if os.path.isfile(os.path.join(input_folder, f)) and f.lower().endswith('.pdf')
    )

    if not pdf_files:
        print(f"No PDFs found in {input_folder!r}. Exiting.")
        sys.exit(1)

    merger = PdfMerger()
    for fname in pdf_files:
        full_path = os.path.join(input_folder, fname)
        print(f"Appending {fname}...")
        merger.append(full_path)

    # Write out the merged PDF
    merger.write(output_path)
    merger.close()
    print(f"\nSuccessfully merged {len(pdf_files)} files into {output_path!r}.")

if __name__ == "__main__":
    # Determine script directory, so this works no matter where it's called from
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_folder = os.path.join(base_dir, 'pdfs')
    output_file = os.path.join(base_dir, 'merged.pdf')

    merge_pdfs(pdf_folder, output_file)
