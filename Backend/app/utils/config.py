import os
import shutil

TESSERACT_CMD = os.getenv(
    "TESSERACT_CMD",
    shutil.which("tesseract") or "tesseract"
)

OUTPUT_DIR = os.getenv(
    "OUTPUT_DIR",
    "captured_images"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)
