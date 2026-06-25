"""
pdf_to_images.py

Utility for converting PDF documents into page-level images.

This step is required because the planning documents are scanned PDFs,
meaning the text exists as images rather than machine-readable text.
The generated images are later used as input for OCR processing.
"""

from pathlib import Path
from pdf2image import convert_from_path


def pdf_to_images(pdf_path: Path, output_dir: Path, dpi: int = 300) -> list[Path]:
    """
    Convert a PDF file into PNG images (one per page).

    Parameters
    ----------
    pdf_path : Path
        Path to the input PDF file.
    output_dir : Path
        Directory where images will be stored.
    dpi : int
        Resolution used when rendering the PDF pages.

    Returns
    -------
    list[Path]
        List of generated image paths.
    """

    output_dir.mkdir(parents=True, exist_ok=True)

    pages = convert_from_path(str(pdf_path), dpi=dpi)
    image_paths = []

    # Use a sanitized file stem to avoid spaces in generated file names
    stem = pdf_path.stem.replace(" ", "_")

    for page_num, page in enumerate(pages, start=1):
        image_path = output_dir / f"{stem}_page_{page_num:04d}.png"
        page.save(image_path, "PNG")
        image_paths.append(image_path)

    return image_paths
