import cv2
import os

from app.services.ocr_service import extract_text_from_image
from app.services.invoice_parser import parse_invoice_text
from app.utils.config import OUTPUT_DIR
from app.utils.logger import get_logger


logger = get_logger(__name__)
def process_webcam():

    logger.info("Starting webcam processing")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        logger.error("Could not open webcam")

        print("Error: Could not open webcam.")

        return []

    print("📷 Press 's' to save a frame | Press 'q' to quit")

    captured_data = []

    while True:

        ret, frame = cap.read()

        if not ret:

            logger.error("Failed to capture webcam frame")

            print("Failed to grab frame.")

            break

        cv2.imshow(
            "Webcam - Press 's' to Save, 'q' to Quit",
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):

            filename = os.path.join(
                OUTPUT_DIR,
                "captured_frame.jpg"
            )

            cv2.imwrite(filename, frame)

            logger.info(
                "Webcam frame saved to %s",
                filename
            )

            text = extract_text_from_image(
                frame,
                augment=True
            )

            data = parse_invoice_text(text)

            captured_data.append(data)

            logger.info(
                "Webcam invoice processing completed"
            )

            break

        elif key == ord('q'):

            logger.info(
                "Webcam processing cancelled by user"
            )

            print("👋 Exiting webcam...")

            break

    cap.release()
    cv2.destroyAllWindows()

    return captured_data