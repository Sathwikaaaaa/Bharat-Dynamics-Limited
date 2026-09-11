# Low-Level Design — Invoice OCR System

## 1. Application Entry Point

File:

`app/main.py`

Responsibilities:

1. Display input options
2. Accept user selection
3. Receive file path
4. Call the appropriate processor
5. Handle exceptions
6. Save extracted data

---

## 2. Preprocessing Service

File:

`app/services/preprocessing.py`

Function:

`preprocess_image(image, augment=False)`

Processing steps:

```text
Input Image
    |
    v
Grayscale Conversion
    |
    v
Bilateral Filtering
    |
    v
Image Resizing
    |
    v
Normalization
    |
    v
Optional Rotation
    |
    v
Processed Image