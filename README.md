# HMLR Document Analysis Task

A modular pipeline for analysing **scanned planning documents** and extracting structured information from them. The project demonstrates how **OCR and rule-based text processing** can be combined to convert historical planning records into a structured dataset suitable for analysis.

---
# Overview

Planning decision documents are often distributed as **scanned PDFs**, meaning the text cannot be directly extracted.
This project implements a workflow that converts these documents into machine-readable text and identifies key information.
The pipeline performs the following steps:

```
PDF Document
      ↓
PDF → Image Conversion
      ↓
Optical Character Recognition (OCR)
      ↓
Page Classification
      ↓
Entity Extraction
   • Application Numbers
   • Applicant Names
      ↓
Structured Dataset
```

The final output is a clean table containing:
* Page number
* Document type
* Application number(s)
* Applicant name(s)

---
# Project Structure

The repository is organised into modular pipeline components, notebooks for execution and analysis, and dedicated folders for input data and documentation assets.


```
hmlr-document-analysis
│
├── analysis_report.md           # One-page challenge analysis
│
├── data/
│   ├── raw/
│   │   └── .gitkeep              # Placeholder so folder exists in Git
│   └── images/
│       └── .gitkeep              # Generated page images (OCR input)
│
├── notebooks/
│   ├── 01_Document_Analysis_walkthrough.ipynb
│   └── 02_run_pipeline.ipynb
│
├── src/
│   ├── pdf_to_images.py          # PDF → image conversion
│   ├── ocr.py                    # OCR text extraction
│   ├── classify.py               # Page classification rules
│   ├── extract.py                # Entity extraction logic
│   └── pipeline.py               # End-to-end processing pipeline
│
├── assets/
│   └── pipeline.png              # Pipeline diagram used in README
│
├── README.md
├── requirements.txt
└── .gitignore
```

This structure separates **analysis**, **reusable code**, and **data**, making the project easier to maintain and extend.

---
## Analysis Report

A brief one-page analysis of the document structure, exploratory observations, limitations of the approach, and potential alternative methods is included in:

`analysis_report.md`

This report summarises key insights from the document inspection and discusses potential improvements such as machine learning based page classification and named entity recognition approaches.

---

# Pipeline Description

## 1. PDF to Image Conversion

Each page of the input PDF is converted into a **high-resolution image** using `pdf2image`.

This step is required because OCR engines operate on images rather than PDF structures.

---

## 2. Optical Character Recognition (OCR)

Text is extracted from each page image using **Tesseract OCR** via the `pytesseract` Python interface.

Key preprocessing steps include:

* grayscale conversion
* optional page cropping
* whitespace normalisation

These steps improve recognition quality for scanned documents.

---

## 3. Page Classification

Each page is classified based on textual cues detected in the OCR output.

The current rule-based classifier identifies:

* Planning Register
* Planning Permission Notice
* Conditional Planning Permission
* Approval Notice

A rule-based approach was chosen because:

* the dataset is small
* page types contain clear textual signals
* the rules are transparent and easy to validate

---

## 4. Entity Extraction

Two key entities are extracted from the OCR text.

### Application Numbers

Application numbers are detected using **regex patterns anchored to phrases such as**:

```
Application No
Application Number
```

This prevents false positives from dates or other numeric values.

Example formats detected:

```
02/80/1609
02/81/1237
P/00/0759
P/98/0964
```

OCR artefacts such as `o` instead of `0` are normalised during extraction.

---

### Applicant Names

Applicants may be either **individuals or companies**.

Examples detected:

```
Mr M Dale
Mrs AM Stephens
Mr & Mrs JM Doe
My First Company Ltd
```

Extraction uses pattern matching combined with text normalisation to handle common OCR issues.

Duplicate matches are removed while preserving the original order.

---

# Installation

## 1. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

---

## 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

# Install Tesseract OCR

The OCR step requires **Tesseract OCR** to be installed on your system.

### macOS (Homebrew)

```bash
brew install tesseract
```

### Ubuntu / Linux

```bash
sudo apt install tesseract-ocr
```

### Windows

Download from:

```
https://github.com/tesseract-ocr/tesseract
```

---

# Running the Pipeline

## Step 1 - Add Input Document

Place the planning document inside:

```
data/raw/
```

Example:

```
data/raw/anonymised.pdf
```

---

## Step 2 - Run the Pipeline

Open the execution notebook:

```
notebooks/02_run_pipeline.ipynb
```

Run all cells.

---

The pipeline produces a structured dataset saved to:

```
outputs/results.csv
```

Example output:

| page | page_type                  | application_number | applicant            |
| ---- | -------------------------- | ------------------ | -------------------- |
| 1    | Planning Register          | ******1609         | Mr *********Doe      |
| 1    | Planning Register          | 02/8******        | My ************** Ltd |
| 2    | Planning Permission Notice | P/********          | Mr ***ale           |
| 4    | Approval Notice            | **********         | Mrs A********ns      |

This format is designed to be easily analysed in tools such as **Excel or pandas**.

---

# Reproducibility

To reproduce the workflow:

1. Create and activate a virtual environment
2. Install dependencies from `requirements.txt`
3. Install Tesseract OCR locally
4. Place the input PDF in `data/raw/`
5. Run `notebooks/run_pipeline.ipynb`

The repository excludes source documents, generated images, and outputs from version control to keep the project lightweight and protect challenge data.

NOTE: Generated artifacts such as page images and output datasets are excluded from version control and will be created automatically when the pipeline is executed.

---

# Design Considerations

The pipeline was designed to prioritise:

* **Readability** - clear modular Python functions
* **Reproducibility** - consistent directory structure
* **Extensibility** - easy to add new extraction rules or document types

Separating reusable logic into the `src/` modules allows the notebooks to focus on **analysis and demonstration**, while the processing code remains reusable.

---

# Future Improvements

Possible extensions include:

* improved OCR preprocessing for noisy scans
* machine learning based page classification
* named entity recognition for more flexible applicant detection
* automated processing of document batches

---

# Author

**Olaoluwa Johnson Taiwo**

Data Scientist
Document Analysis Pipeline
