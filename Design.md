# O-1A Visa Qualification AI Application

This document explains the design choices, evaluation criteria, and additional notes on the implementation of the AI application that assesses a candidate's qualifications for an O-1A visa. The application takes a PDF CV, extracts its text, uses a pre-trained zero-shot classification model to map content to O-1A evidentiary requirements, and generates an HTML report.

---

## Overview

The application is built with FastAPI and comprises the following key components:
- **PDF Extraction:** Uses PyMuPDF to extract text from PDF files.
- **Classification:** Employs HuggingFace’s zero-shot classification (with `facebook/bart-large-mnli`) to classify CV text into eight O-1A criteria:  
  - Awards
  - Membership
  - Press
  - Judging
  - Original Contribution
  - Scholarly Articles
  - Critical Employment
  - High Remuneration
- **Report Generation:** Creates an HTML report (displayed directly in the browser) that shows both the detailed classification and an overall rating (Low, Medium, High) based on a simple heuristic.

---

## Design Choices

### FastAPI as the Web Framework
- **Reason:**  
  - FastAPI is modern, asynchronous, and offers auto-generated interactive API docs via Swagger UI.
- **Benefits:**  
  - High performance and ease of use.
  - Built-in support for file uploads using `UploadFile` and `python-multipart`.

### PDF Extraction using PyMuPDF
- **Reason:**  
  - PyMuPDF (fitz) provides fast and reliable text extraction from PDF files.
- **Benefits:**  
  - Excellent performance and simplicity.
  - Ability to extract text accurately from various PDF formats.

### Classification Using Zero-Shot Learning
- **Reason:**  
  - Using a pre-trained model like `facebook/bart-large-mnli` allows for multi-label classification without the need for extensive labeled data.
- **Benefits:**  
  - Flexibility to define custom labels (the O-1A criteria).
  - Leverages state-of-the-art NLP capabilities.
  - Avoids the need to train a custom model from scratch.

### HTML Report Generation Instead of PDF
- **Reason:**  
  - Due to dependency issues with PDF generation (WeasyPrint and system library mismatches), we opted to generate the report as HTML.
- **Benefits:**  
  - Eliminates dependency on native libraries that might conflict with your system (e.g., outdated Pango libraries).
  - HTML reports can be viewed directly in the browser, making them easier to debug and style using standard web technologies.

---

## Evaluating the Output

### 1. Text Extraction Accuracy
- **Goal:**  
  - Ensure the CV text is accurately and completely extracted.
- **Evaluation:**  
  - Compare the extracted text with the original PDF manually.
  - Check for missing or mis-ordered text, especially in complex layouts.

### 2. Classification Relevance
- **Goal:**  
  - Validate that the classifier accurately maps CV content to the correct O-1A criteria.
- **Evaluation:**  
  - Manually review a set of sample CVs and compare the classifier’s output against expected classifications.
  - Verify that the model assigns appropriate scores (confidence levels) for each category.

### 3. Overall Rating Heuristic
- **Goal:**  
  - Provide a meaningful overall rating (Low, Medium, High) based on the aggregated classification scores.
- **Evaluation:**  
  - Test with multiple CVs to ensure that the threshold values (e.g., > 0.75 for High, > 0.5 for Medium) align with expert expectations.
  - Adjust the thresholds if necessary based on domain expert feedback.

### 4. Report Presentation
- **Goal:**  
  - Ensure the generated HTML report is clear, well-formatted, and informative.
- **Evaluation:**  
  - Manually inspect the HTML report via the browser.
  - Verify that the report includes:
    - An overall rating.
    - Detailed scores for each O-1A criterion.
    - The extracted CV text for reference.

---

## Additional Documentation and Developer Guidelines

- **README.md:**  
  - Contains setup instructions, dependency installation, and steps to run the FastAPI server.
- **API Documentation:**  
  - Accessible via FastAPI’s interactive docs at `/docs`.
- **Developer Notes:**  
  - Outline how to extend or modify components (e.g., switching to PDF report generation using ReportLab or pdfkit if needed).
  - Include coding conventions and tips for troubleshooting common issues (e.g., system dependency problems with PDF generation).

---

## Future Improvements

- **Enhancing Classification:**  
  - Explore fine-tuning a custom model using labeled CV data for improved accuracy.
- **PDF Generation Option:**  
  - Investigate alternative PDF generation libraries (e.g., ReportLab, pdfkit with wkhtmltopdf) if PDF output is desired in the future.
- **User Feedback Integration:**  
  - Develop a mechanism for immigration experts to provide feedback on the classification results, enabling iterative improvements.

---

This document is intended to provide clear insight into the design rationale and evaluation methods used in the application, helping both users and developers understand how the system works and how its performance can be assessed.
