import os


TESSERACT_CMD = os.getenv(
    "TESSERACT_CMD",
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

OUTPUT_DIR = os.getenv(
    "OUTPUT_DIR",
    "captured_images"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)