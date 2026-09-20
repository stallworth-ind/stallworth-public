
import logging


def setup_logging(level: str):
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    logging.basicConfig(
        level=numeric_level,
        format="%(message)s"
    )


def format_unexpected_error(error: BaseException) -> str:
    """Build a concise CLI error while preserving the original diagnostic."""
    if (
        isinstance(error, KeyError)
        and len(error.args) == 1
        and isinstance(error.args[0], str)
    ):
        detail = error.args[0].strip()
    else:
        detail = str(error).strip()

    error_name = type(error).__name__
    if not detail:
        return f"Unexpected error ({error_name})"
    return f"Unexpected error ({error_name}): {detail}"
