"""
pipeline.py

End-to-end document processing pipeline for the HMLR challenge.

The pipeline performs the following steps:
1. Convert PDF documents into images
2. Run OCR on each page
3. Build a page-level dataset
4. Classify page types
5. Extract application numbers and applicant names
6. Produce a structured output table
"""

from pathlib import Path
import pandas as pd

from .config import DATA_IMAGES, DPI, TESSERACT_CONFIG
from .pdf_to_images import pdf_to_images
from .ocr import ocr_image
from .classify import classify_page
from .extract import extract_application_numbers, extract_applicants


def _join_list(values: list[str]) -> str:
    """Format a list of strings as a semicolon-separated value."""
    return "; ".join(values) if values else ""


def process_document(pdf_path: Path, dpi: int = DPI) -> pd.DataFrame:
    """
    Run the full processing pipeline for a single PDF document.

    The resulting DataFrame contains one row per page and includes the
    detected page type, extracted application numbers, and applicants.
    """

    print(f"Processing: {pdf_path.name}")

    # Convert PDF pages into images so OCR can process them page-by-page.
    image_paths = pdf_to_images(pdf_path, DATA_IMAGES, dpi)

    # Run OCR on every generated page image.
    texts = [
        ocr_image(img_path, page_num, config=TESSERACT_CONFIG)
        for page_num, img_path in enumerate(image_paths, start=1)
    ]

    # Build page-level dataset with the raw OCR text and image paths.
    df = pd.DataFrame({
        "page": range(1, len(texts) + 1),
        "image_path": [str(p) for p in image_paths],
        "text": texts,
    })

    # Classify each page based on its OCR text.
    df["page_type"] = df["text"].apply(classify_page)

    # Extract structured information from the page text.
    df["application_numbers"] = df["text"].apply(extract_application_numbers)
    df["applicants"] = df["text"].apply(extract_applicants)

    # Create the final export table with formatted list values.
    df_export = df[["page", "page_type", "application_numbers", "applicants"]].copy()
    df_export["application_numbers"] = df_export["application_numbers"].apply(_join_list)
    df_export["applicants"] = df_export["applicants"].apply(_join_list)

    return df_export
