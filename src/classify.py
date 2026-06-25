"""
classify.py

Rule-based page classification for planning documents.

Each page of the OCR text is analysed for key phrases that indicate
the type of document page (register, permission notice, approval notice, etc.).
"""

def classify_page(text: str) -> str:
    """
    Determine the document page type from OCR text.

    The classifier is intentionally simple and rule-based, matching
    expected phrases in the lowercased text.
    """

    text = text.lower()

    # Identify the main planning register page format first
    if "conditional approval granted" in text and "application no" in text:
        return "Planning Register"

    if "conditional planning permission" in text:
        return "Conditional Planning Permission"

    if "notice of approval" in text and "details" in text:
        return "Approval Notice"

    if "planning permission" in text and "application number" in text:
        return "Planning Permission Notice"

    # Fallback label for pages that do not match known patterns
    return "Other"
