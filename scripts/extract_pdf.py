from pypdf import PdfReader
import os

pdf_path = r"c:\Users\HP\Desktop\Bootcamp AMA\bootcamp-ama.pdf"
output_path = r"c:\Users\HP\Desktop\Bootcamp AMA\bootcamp-ama-text.txt"

try:
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Successfully extracted text to {output_path}")
    print("--- CONTENT PREVIEW ---")
    print(text[:2000]) # Print first 2000 chars
except Exception as e:
    print(f"Error: {e}")
