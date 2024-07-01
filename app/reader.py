# reader.py
import fitz  # PyMuPDF
import pandas as pd
import os

def read_transcript(filepath, output_data):
    with fitz.open(filepath) as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            filtered_info = extract_filtered_info(text)
            output_data.append(filtered_info)
    
    # return PDFs that were read

def extract_filtered_info(text):
    # TODO: edit
    return {"test": text.strip()}
