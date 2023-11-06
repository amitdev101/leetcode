import PyPDF2
import os
import sys

def decrypt_pdf(input_pdf_path, output_pdf_path, password):
    with open(input_pdf_path, 'rb') as input_file:
        reader = PyPDF2.PdfReader(input_file)
        if reader.is_encrypted:
            # Try to decrypt the PDF with the provided password
            if reader.decrypt(password):
                writer = PyPDF2.PdfWriter()
                # Add all pages to the writer
                for page in reader.pages:
                    writer.add_page(page)
                # Write the decrypted PDF to the new file
                with open(output_pdf_path, 'wb') as output_file:
                    writer.write(output_file)
                return True
        return False

def main(pdf_directory, password):
    for filename in os.listdir(pdf_directory):
        if filename.lower().endswith('.pdf'):
            input_pdf_path = os.path.join(pdf_directory, filename)
            output_filename = filename.replace(".pdf","_decrypted.pdf")
            output_pdf_path = os.path.join(pdf_directory, output_filename)
            success = decrypt_pdf(input_pdf_path, output_pdf_path, password)
            if success:
                print(f"The password has been removed from {filename}")
            else:
                print(f"Failed to decrypt {filename} or it was not password protected.")

if __name__ == "__main__":
     # hardcoding
    pdf_directory = './pdf'
    password = 'Your_password_here'
    main(pdf_directory, password)
    print("done")
    
    # if len(sys.argv) != 3:
    #     print("Usage: python remove_pdf_passwords.py [pdf_directory] [password]")
    # else:
    #     pdf_directory = sys.argv[1]
    #     password = sys.argv[2]
    #     main(pdf_directory, password)
