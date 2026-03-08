"""
classify.py

Rule-based page classification for planning documents.

Each page of the OCR text is analysed for key phrases that indicate
the type of document page (register, permission notice, approval notice, etc.).
"""

def classify_page(text: str) -> str:
    """
    Determine the document page type based on text patterns.
    """

    text = text.lower()

    if "conditional approval granted" in text and "application no" in text:
        return "Planning Register"

    if "conditional planning permission" in text:
        return "Conditional Planning Permission"

    if "notice of approval" in text and "details" in text:
        return "Approval Notice"

    if "planning permission" in text and "application number" in text:
        return "Planning Permission Notice"

    return "Other"
