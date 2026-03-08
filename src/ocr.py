"""
ocr.py

Functions responsible for performing Optical Character Recognition (OCR)
on document images using the Tesseract OCR engine.

The OCR step converts page images into machine-readable text which
can then be analysed using text-processing techniques.
"""

from pathlib import Path
from PIL import Image
import pytesseract


def ocr_image(image_path: Path, page_number: int, config: str) -> str:
    """
    Extract text from an image using Tesseract OCR.

    Parameters
    ----------
    image_path : Path
        Path to the page image.
    page_number : int
        Page index used for page-specific processing.
    config : str
        Tesseract configuration string.

    Returns
    -------
    str
        Cleaned OCR text.
    """

    image = Image.open(image_path)

    # Convert to grayscale to improve OCR contrast
    image = image.convert("L")

    width, height = image.size

    # Special handling for the first page
    # The register table tends to produce noisy OCR results
    if page_number == 1:

        crop_start = int(height * 0.35)
        image = image.crop((0, crop_start, width, height))

    text = pytesseract.image_to_string(image, config=config)

    # Collapse excessive whitespace
    text = " ".join(text.split())

    return text
