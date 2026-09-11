from app.utils.logger import get_logger

logger = get_logger(__name__)


DEFAULT_Y_TOLERANCE = 10


def group_tokens_into_rows(
    tokens,
    y_tolerance=DEFAULT_Y_TOLERANCE
):
    """
    Group OCR tokens that belong to the same
    visual row based on their Y coordinates.
    """

    if not tokens:
        return []

    sorted_tokens = sorted(
        tokens,
        key=lambda token: (
            token["y"],
            token["x"]
        )
    )

    rows = []

    for token in sorted_tokens:

        added_to_row = False

        for row in rows:

            reference_y = row["y"]

            if abs(token["y"] - reference_y) <= y_tolerance:
                row["tokens"].append(token)

                row["tokens"].sort(
                    key=lambda item: item["x"]
                )

                added_to_row = True
                break

        if not added_to_row:
            rows.append(
                {
                    "y": token["y"],
                    "tokens": [token]
                }
            )

    result = []

    for row in rows:

        text = " ".join(
            token["text"]
            for token in row["tokens"]
        )

        result.append(
            {
                "y": row["y"],
                "tokens": row["tokens"],
                "text": text
            }
        )

    logger.info(
        "Grouped %d OCR tokens into %d rows",
        len(tokens),
        len(result)
    )

    return result