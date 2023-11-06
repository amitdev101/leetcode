import fitz  # PyMuPDF
from PIL import Image
import io

def convert_pdf_to_images(pdf_path, dpi=200):
    doc = fitz.open(pdf_path)
    images = []
    for page in doc:
        # Specify the dpi for the image
        zoom = dpi / 72  # Default DPI in PyMuPDF is 72
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        images.append(img)
    doc.close()
    return images

# Use PNG for a lossless format
def save_images_as_png(images, quality=90):
    png_images = []
    for i, image in enumerate(images):
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG', quality=quality)
        img_byte_arr = img_byte_arr.getvalue()
        png_images.append(Image.open(io.BytesIO(img_byte_arr)))
    return png_images

def create_pdf_from_images(images, output_pdf_path):
    images[0].save(output_pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:])


if __name__=='__main__':
    pdf_path = 'test.pdf'
    output_pdf_path = 'test_compressed.pdf'
    # Convert PDF to images with higher DPI for better quality
    images = convert_pdf_to_images(pdf_path, dpi=200)
    # Save images as PNG instead of JPEG for better quality
    png_images = save_images_as_png(images, quality=90)
    # Create a PDF from the PNG images
    create_pdf_from_images(png_images, output_pdf_path)
