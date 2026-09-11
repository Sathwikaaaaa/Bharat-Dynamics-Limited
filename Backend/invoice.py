import cv2
import json
import os
import numpy as np
import re

from pdf2image import convert_from_path
from app.services.invoice_parser import parse_invoice_text
from app.utils.config import OUTPUT_DIR
from app.services.ocr_service import extract_text_from_image
# pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
from app.processors.pdf_processor import process_pdf
from app.processors.image_processor import process_image
#image preprocessing
from app.processors.webcam_processor import process_webcam








# Save extracted data to JSON
def save_to_json(data, filename="invoice_data.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"✅ Extracted data saved to {filename}")

def main():
    print("Choose input type:")
    print("1 - PDF")
    print("2 - Image (JPG/PNG)")
    print("3 - Webcam")
    choice = input("Enter your choice (1/2/3): ").strip()

    if choice == "1":
        file_path = input("Enter path to PDF file: ")
        data = process_pdf(file_path)
    elif choice == "2":
        file_path = input("Enter path to image file (JPG/PNG): ")
        data = process_image(file_path)
    elif choice == "3":
        data = process_webcam()
    else:
        print("Invalid choice.")
        return

    if data:
        save_to_json(data)
    else:
        print("No data extracted.")

if __name__ == "__main__":
    main()
