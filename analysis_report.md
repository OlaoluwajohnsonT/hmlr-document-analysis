# Analysis Report

## Overview

The objective of this challenge was to process scanned planning decision notices and extract structured information from them. The documents are provided as scanned PDFs, meaning the textual content is not directly machine-readable and must first be recovered using Optical Character Recognition (OCR). The pipeline developed for this task converts each PDF page into an image, extracts text using OCR, classifies the page type, and extracts key entities such as application numbers and applicant names into a structured dataset.

## Exploratory Observations

Initial inspection of the document revealed that each page represents a planning decision notice with relatively consistent formatting. Although the documents are scanned images, key textual signals are clearly visible in the OCR output. In particular, page types contain distinctive phrases such as *Planning Register*, *Planning Permission Notice*, and *Approval Notice*. These phrases provide reliable indicators for determining the category of each page.

Application numbers also follow consistent formatting patterns. Examples observed in the OCR output include formats such as:

02/80/1609  
P/00/0759  

These structured identifiers make it feasible to detect application numbers using regular expressions anchored to contextual phrases such as “Application No” or “Application Number”.

Applicant names typically appear either as titled individuals (e.g. *Mr*, *Mrs*) or as organisation names (e.g. *Company Ltd*). These patterns enable relatively robust extraction using rule-based pattern matching.

## Approach

Given the limited dataset size and the clear textual signals present in the documents, a rule-based approach was adopted for both page classification and entity extraction.

Page classification is performed by searching for specific keywords associated with each document type within the OCR text. This approach provides transparent and easily interpretable decision rules while avoiding the need for training data.

Application numbers are extracted using regular expressions designed to capture common planning reference formats. Applicant names are detected using pattern-based matching combined with simple text normalisation to mitigate OCR artefacts.

This approach prioritises robustness, interpretability, and simplicity while remaining effective for the relatively structured document format.

## Limitations

The primary limitation of the current pipeline arises from OCR accuracy. OCR errors may occur due to scanning quality, font variation, or image noise. Characters such as “0” and “O” or “1” and “l” may occasionally be confused, which can introduce minor inaccuracies in extracted entities.

Additionally, rule-based classification depends on the presence of specific textual phrases. If future documents use different wording or formatting, the classification rules may need to be extended.

Similarly, the regex-based extraction approach assumes relatively consistent entity formats. Unusual applicant name structures or heavily degraded OCR output could reduce extraction accuracy.

## Potential Improvements

Several enhancements could further improve the robustness of the system.

Image preprocessing techniques such as deskewing, adaptive thresholding, and noise reduction could improve OCR accuracy for lower-quality scans.

For page classification, machine learning approaches such as logistic regression or transformer-based text classifiers could be explored if larger labelled datasets were available.

Entity extraction could also be enhanced using Named Entity Recognition (NER) models such as spaCy or transformer-based NER systems, which may generalise better to diverse name formats.

Finally, the pipeline could be extended to support large-scale batch processing, enabling automated processing of large historical document collections.

## Example Output

The pipeline converts the scanned document into a structured dataset containing the page number, document type, application number, and applicant name.

Example extracted records (values partially masked for privacy):

| page | page_type                  | application_number | applicant            |
|------|----------------------------|--------------------|----------------------|
| 1    | Planning Register          | 02/8****609        | Mr J**** Doe         |
| 1    | Planning Register          | 02/8****237        | Example Company Ltd  |
| 2    | Planning Permission Notice | P/0****759         | Mr M**** Dale        |
| 4    | Approval Notice            | P/9****964         | Mrs A**** Stephens   |

This structured representation allows the information contained within historical planning documents to be analysed programmatically while protecting potentially identifiable information in documentation examples.