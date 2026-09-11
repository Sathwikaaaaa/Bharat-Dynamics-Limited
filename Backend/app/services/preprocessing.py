import cv2


def preprocess_image(image, augment=False):
    """
    Preprocess an image before OCR.

    Steps:
    1. Convert image to grayscale.
    2. Remove noise using bilateral filtering.
    3. Resize image by a factor of 2.
    4. Normalize pixel intensity.
    5. Optionally rotate the image slightly.

    Args:
        image: Input OpenCV image.
        augment: Whether to apply slight rotation.

    Returns:
        Preprocessed image suitable for OCR.
    """

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Noise removal with bilateral filter
    noise_removed = cv2.bilateralFilter(
        gray,
        d=9,
        sigmaColor=75,
        sigmaSpace=75
    )

    # Resize image
    height, width = noise_removed.shape
    scale_factor = 2

    resized = cv2.resize(
        noise_removed,
        (width * scale_factor, height * scale_factor),
        interpolation=cv2.INTER_LINEAR
    )

    # Normalize pixel intensity
    normalized = cv2.normalize(
        resized,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    # Optional slight rotation
    if augment:
        angle = 1

        center = (
            normalized.shape[1] // 2,
            normalized.shape[0] // 2
        )

        rotation_matrix = cv2.getRotationMatrix2D(
            center,
            angle,
            1.0
        )

        normalized = cv2.warpAffine(
            normalized,
            rotation_matrix,
            (
                normalized.shape[1],
                normalized.shape[0]
            ),
            flags=cv2.INTER_LINEAR
        )

    return normalized