# High-Level Design — Invoice OCR System

## 1. Purpose

The system extracts structured information from invoices using OCR.

The application currently supports:

- PDF invoices
- JPG/JPEG images
- PNG images
- Webcam capture

## 2. High-Level Architecture

```text
                    User
                     |
                     v
                  main.py
                     |
        +------------+------------+
        |            |            |
        v            v            v
       PDF         Image        Webcam
        |            |            |
        +------------+------------+
                     |
                     v
              Processing Layer
                     |
                     v
              OCR Service
                     |
                     v
             Image Preprocessing
                     |
                     v
                Tesseract
                     |
                     v
              Invoice Parser
                     |
                     v
                JSON Output