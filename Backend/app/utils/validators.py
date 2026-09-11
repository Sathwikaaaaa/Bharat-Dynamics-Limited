import os


SUPPORTED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png"
}

SUPPORTED_PDF_EXTENSIONS = {
    ".pdf"
}


def validate_file_exists(file_path):
    """
    Check whether the given file exists.
    """

    if not file_path:
        raise ValueError("File path cannot be empty.")

    if not os.path.isfile(file_path):
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )


def validate_image_file(file_path):
    """
    Validate that the file exists and has a supported image extension.
    """

    validate_file_exists(file_path)

    extension = os.path.splitext(file_path)[1].lower()

    if extension not in SUPPORTED_IMAGE_EXTENSIONS:
        raise ValueError(
            f"Unsupported image format: {extension}. "
            f"Supported formats: JPG, JPEG, PNG."
        )


def validate_pdf_file(file_path):
    """
    Validate that the file exists and is a PDF.
    """

    validate_file_exists(file_path)

    extension = os.path.splitext(file_path)[1].lower()

    if extension not in SUPPORTED_PDF_EXTENSIONS:
        raise ValueError(
            f"Unsupported file format: {extension}. "
            f"Expected a PDF file."
        )