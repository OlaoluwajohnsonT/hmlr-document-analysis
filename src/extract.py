"""
extract.py

Text extraction helpers for the HMLR document analysis project.

This module contains utilities for extracting application numbers and
applicant names from OCR-produced text, while normalising common OCR
errors and removing duplicate candidates.
"""

import re


# ------------------------------------------------
# Application number extraction
# ------------------------------------------------

APP_NO_PATTERN = re.compile(
    r"""
    Application\s*(?:No\.?|Nos\.?|Number)\s*[:\-]?\s*
    (
        (?:[A-Z]\s*/\s*\d{2}\s*/\s*[0-9oO]{4,5})
        |
        (?:\d{2}\s*/\s*\d{2}\s*/\s*\d{4})
    )
    """,
    flags=re.IGNORECASE | re.VERBOSE,
)


def extract_application_numbers(text: str) -> list[str]:
    """Extract application numbers from OCR text."""
    matches = APP_NO_PATTERN.findall(text)
    cleaned = []

    for m in matches:
        m = re.sub(r"\s+", "", m)
        m = m.replace("o", "0").replace("O", "0")

        parts = m.split("/")
        if len(parts) == 3 and len(parts[-1]) == 5 and parts[-1].isdigit():
            parts[-1] = parts[-1][-4:]
            m = "/".join(parts)

        cleaned.append(m)

    seen = set()
    result = []

    for m in cleaned:
        if m not in seen:
            seen.add(m)
            result.append(m)

    return result


# ------------------------------------------------
# Applicant extraction
# ------------------------------------------------

PERSON_PATTERN = re.compile(
    r"""
    \b(?:Mr|Mrs|Miss|Ms)\.?\s*
    (?:&\s*(?:Mr|Mrs)\.?\s*)?
    (?:[A-Z]\.?\s*){1,4}
    [A-Z][A-Za-z]{1,30}\b
    """,
    flags=re.VERBOSE,
)

COMPANY_PATTERN = re.compile(
    r"\b[A-Z][A-Za-z]*(?:\s+[A-Z][A-Za-z]*){0,6}\s+(?:Ltd|Limited)\b"
)


# ------------------------------------------------
# OCR cleanup
# ------------------------------------------------

def _normalise_ocr_text(text: str) -> str:
    """Normalise common OCR artefacts in extracted text."""
    text = " ".join(text.split())
    text = re.sub(r"\bVirs\b", "Mrs", text, flags=re.IGNORECASE)
    text = re.sub(r"\bMra\b", "Mrs", text, flags=re.IGNORECASE)
    return text


# ------------------------------------------------
# Applicant cleaning
# ------------------------------------------------

def _clean_applicant(candidate: str) -> str:
    """Clean and normalise an applicant candidate string."""
    candidate = candidate.strip(" ,.|;:-")
    candidate = re.sub(
        r"^Conditional approval granted to\s+",
        "",
        candidate,
        flags=re.IGNORECASE,
    )

    candidate = re.split(r"[©|]", candidate)[0].strip()
    candidate = candidate.replace(".", "")
    candidate = re.sub(r"\s+", " ", candidate).strip()
    candidate = re.sub(r"\s*&\s*", " & ", candidate)

    # Fix OCR title spacing (MrsJ -> Mrs J)
    candidate = re.sub(r"\b(Mr|Mrs|Miss|Ms)([A-Z])", r"\1 \2", candidate)
    # Collapse spaced initials (J D -> JD)
    candidate = re.sub(r"\b([A-Z])\s+([A-Z])\b", r"\1\2", candidate)
    return candidate


# ------------------------------------------------
# Canonical form for deduplication
# ------------------------------------------------

def _canonical_name(name: str) -> str:
    """Return a normalised key for comparing applicant names."""
    name = name.lower()
    name = name.replace(".", "")
    name = re.sub(r"\s+", " ", name).strip()

    # remove spaces between initials
    name = re.sub(r"\b([a-z])\s+([a-z])\b", r"\1\2", name)
    # normalise common title variants
    name = name.replace("mr & mrs", "mr mrs")
    return name


# ------------------------------------------------
# Deduplication
# ------------------------------------------------

def _dedupe_preserve_order(values: list[str]) -> list[str]:
    """Remove duplicate values while preserving original order."""
    seen = set()
    result = []

    for value in values:
        key = _canonical_name(value)
        if key not in seen:
            seen.add(key)
            result.append(value)

    return result


# ------------------------------------------------
# Main extraction
# ------------------------------------------------

def extract_applicants(text: str) -> list[str]:
    """Extract applicant names from OCR text."""
    text = _normalise_ocr_text(text)

    candidates = []
    candidates.extend(PERSON_PATTERN.findall(text))
    candidates.extend(COMPANY_PATTERN.findall(text))

    cleaned = []
    for c in candidates:
        c = _clean_applicant(c)
        if len(c.split()) < 2:
            continue
        cleaned.append(c)

    return _dedupe_preserve_order(cleaned)
