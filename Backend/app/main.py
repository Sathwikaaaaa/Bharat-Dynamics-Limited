from app.processors.pdf_processor import process_pdf
from app.processors.image_processor import process_image
from app.processors.webcam_processor import process_webcam
from app.utils.logger import get_logger

import json


logger = get_logger(__name__)


def save_to_json(data, filename="invoice_data.json"):
    """
    Save extracted invoice data to a JSON file.
    """

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        logger.info(
            "Extracted invoice data saved to %s",
            filename
        )

        print(
            f"✅ Extracted data saved to {filename}"
        )

    except OSError:

        logger.exception(
            "Failed to write JSON file: %s",
            filename
        )

        print(
            "❌ Unable to save extracted data."
        )


def main():

    logger.info(
        "Invoice processing application started"
    )

    print()
    print("Choose input type:")
    print("1 - PDF")
    print("2 - Image (JPG/PNG)")
    print("3 - Webcam")

    choice = input(
        "Enter your choice (1/2/3): "
    ).strip()

    try:

        if choice == "1":

            file_path = input(
                "Enter path to PDF file: "
            ).strip()

            data = process_pdf(file_path)

            save_to_json(data)

        elif choice == "2":

            file_path = input(
                "Enter path to image file (JPG/PNG): "
            ).strip()

            data = process_image(file_path)

            save_to_json(data)

        elif choice == "3":

            data = process_webcam()

            if data:

                save_to_json(data)

            else:

                logger.warning(
                    "No invoice data captured from webcam"
                )

        else:

            logger.warning(
                "Invalid input choice: %s",
                choice
            )

            print(
                "❌ Invalid choice. "
                "Please select 1, 2, or 3."
            )

            return

    except FileNotFoundError as error:

        logger.error(
            "File not found: %s",
            error
        )

        print(
            f"❌ File not found: {error}"
        )

    except ValueError as error:

        logger.error(
            "Validation error: %s",
            error
        )

        print(
            f"❌ Invalid input: {error}"
        )

    except Exception:

        logger.exception(
            "Unexpected application error"
        )

        print(
            "❌ An unexpected error occurred. "
            "Check application.log for details."
        )

    logger.info(
        "Invoice processing application finished"
    )


if __name__ == "__main__":
    main()