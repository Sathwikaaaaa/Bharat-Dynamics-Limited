import pytesseract 
import cv2
import json
import os
import numpy as np
import re
from pdf2image import convert_from_path
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


output_dir = "captured_images"
os.makedirs(output_dir, exist_ok=True)

#image preprocessing
def preprocess_image(image, augment=False):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Noise removal with bilateral filter
    noise_removed = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)
    
    # Resize to make text more readable (optional scale factor or fixed width)
    height, width = noise_removed.shape
    scale_factor = 2  # You can adjust this
    resized = cv2.resize(noise_removed, (width * scale_factor, height * scale_factor), interpolation=cv2.INTER_LINEAR)
    
    # Normalize pixel intensity to improve contrast
    normalized = cv2.normalize(resized, None, 0, 255, cv2.NORM_MINMAX)
    
    # Data Augmentation: rotate if enabled
    if augment:
        angle = 1  # Slight rotation
        center = (normalized.shape[1] // 2, normalized.shape[0] // 2)
        rot_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        normalized = cv2.warpAffine(normalized, rot_matrix, (normalized.shape[1], normalized.shape[0]), flags=cv2.INTER_LINEAR)

    return normalized


def extract_text_from_image(image, augment=False):
    preprocessed = preprocess_image(image, augment=augment)
    text = pytesseract.image_to_string(preprocessed)
    return text


def parse_invoice_text(text):
    lines = text.split('\n')
    data = {}

    invoice_pattern = re.compile(r'invoice\s*(?:#|no\.?|number)?\s*[:#]?\s*(\S+)', re.IGNORECASE)

    for line in lines:
        line = line.strip()

        match = invoice_pattern.search(line)
        if match:
            data["invoice_number"] = match.group(1)

        if "order" in line.lower():
            data["order_number"] = line
        elif "date" in line.lower():
            data["date"] = line
        elif "total" in line.lower():
            data["total"] = line

    data["raw_text"] = text
    return data

# === Process PDF Invoices ===
def process_pdf(file_path):
    images = convert_from_path(file_path)
    all_data = []
    for img in images:
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        text = extract_text_from_image(img_cv, augment=True)
        data = parse_invoice_text(text)
        all_data.append(data)
    return all_data


def process_image(file_path):
    image = cv2.imread(file_path)
    text = extract_text_from_image(image, augment=True)
    return [parse_invoice_text(text)]


def process_webcam():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return []

    print("📷 Press 's' to save a frame | Press 'q' to quit")

    captured_data = []

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        cv2.imshow("Webcam - Press 's' to Save, 'q' to Quit", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            filename = os.path.join(output_dir, "captured_frame.jpg")
            cv2.imwrite(filename, frame)
            print(f"✅ Image saved to {filename}")
            text = extract_text_from_image(frame, augment=True)
            captured_data.append(parse_invoice_text(text))
            break

        elif key == ord('q'):
            print("👋 Exiting webcam...")
            break

    cap.release()
    cv2.destroyAllWindows()
    return captured_data

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
