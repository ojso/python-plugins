import fitz  # PyMuPDF
from PIL import Image
import os

def pdf_to_long_image(pdf_path, output_path, dpi=200):
    """
    Convert a multi-page PDF into a single vertical long image.

    Args:
        pdf_path: Path to the input PDF file.
        output_path: Path for the output image (recommended: .png).
        dpi: Resolution for the output images. Higher values give better quality
             but produce larger files. Default is 200.
    """
    # 1. Open the PDF document
    doc = fitz.open(pdf_path)
    images = []

    # 2. Render each page to a PIL Image object
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        # Get pixmap with specified DPI
        pix = page.get_pixmap(dpi=dpi)
        # Convert pixmap to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)

    doc.close()

    # 3. Calculate total height and create a blank canvas
    total_height = sum(img.height for img in images)
    # Assume all pages have the same width; take width from the first page
    width = images[0].width
    long_image = Image.new('RGB', (width, total_height))

    # 4. Paste each page image vertically
    y_offset = 0
    for img in images:
        long_image.paste(img, (0, y_offset))
        y_offset += img.height

    # 5. Save the final long image
    long_image.save(output_path)
    print(f"✅ Successfully converted PDF to long image: {output_path}")

# --- Example usage ---
if __name__ == '__main__':
    pdf_file = "example.pdf"          # Replace with your PDF path
    output_file = "output_long.png"   # Output image path
    pdf_to_long_image(pdf_file, output_file, dpi=300)  # Use 300 DPI for high quality

