"""
config.py

Central configuration for the HMLR document analysis project.

This file defines common paths and constants used across the pipeline.
Keeping configuration in one place makes the project easier to maintain
and avoids hardcoding values in multiple modules.
"""

from pathlib import Path

# Project root directory for relative paths used throughout the package
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Data folders used by the pipeline
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_IMAGES = PROJECT_ROOT / "data" / "images"
OUTPUTS = PROJECT_ROOT / "outputs"

# OCR and image processing settings
DPI = 300
TESSERACT_CONFIG = "--oem 3 --psm 6"
