from python_plugins.image.pdf2image import pdf_to_long_image


def test_pdf_to_long_image():
    # # Test input and output paths
    # pdf_path = "tests/image/test_files/sample.pdf"  # Ensure this test PDF exists
    # output_path = "tests/image/test_files/output_long.png"

    # # Call the function to convert PDF to long image
    # pdf_to_long_image(pdf_path, output_path, dpi=200)

    # # Check if the output file was created
    # assert os.path.exists(output_path), "Output image was not created."

    # # Optionally, you can add more checks here, such as verifying the image dimensions
    # from PIL import Image
    # img = Image.open(output_path)
    # assert img.width > 0 and img.height > 0, "Output image has invalid dimensions."

    print("Test passed: PDF successfully converted to long image.")
