from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
import os
import uuid

from pdf_extractor import extract_text_from_pdf
from classifier import classify_text, get_overall_rating
from report_generator import generate_html_report

app = FastAPI()

# Directory for temporarily saving uploaded PDFs
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/", response_class=HTMLResponse)
async def upload_cv(file: UploadFile = File(...)):
    # Ensure the uploaded file is a PDF
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")
    
    # Save the uploaded file to a temporary location
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Extract text from the PDF
    try:
        cv_text = extract_text_from_pdf(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error extracting text from PDF.")
    
    # Classify the extracted CV text
    classification_result = classify_text(cv_text)
    overall = get_overall_rating(classification_result)
    
    # Generate the HTML report instead of a PDF report
    html_report = generate_html_report(classification_result, overall, cv_text)
    
    return HTMLResponse(content=html_report)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
